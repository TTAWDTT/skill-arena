from __future__ import annotations

import json
import re
import uuid
from pathlib import Path
from typing import Any, Optional

import yaml

from .config import resolve_path
from .filter_skills import load_jsonl
from .modelhub import ModelHubClient
from .schema import JudgeVerdict, PairResult, RunAttempt, SkillRecord, TaskSpec


def load_tasks(tasks_dir: Path, categories: Optional[list[str]] = None) -> list[TaskSpec]:
    tasks: list[TaskSpec] = []
    for path in sorted(tasks_dir.rglob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if categories and data.get("category") not in categories:
            continue
        tasks.append(TaskSpec.model_validate(data))
    for path in sorted(tasks_dir.rglob("*.yml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if categories and data.get("category") not in categories:
            continue
        tasks.append(TaskSpec.model_validate(data))
    # de-dupe by task_id
    by_id = {t.task_id: t for t in tasks}
    return list(by_id.values())


def build_messages(
    task: TaskSpec,
    skill: Optional[SkillRecord],
    load_mode: str = "system_prepend",
) -> tuple[Optional[str], Any]:
    """Return (instructions, input) for Responses API."""
    user = (
        f"# Task\n{task.title}\n\n"
        f"## Prompt\n{task.prompt}\n\n"
        f"## Expected behavior (for your planning, still produce the answer)\n"
        f"{task.expected_behavior}\n"
    )
    if skill is None:
        return None, user

    skill_block = (
        f"# Active Skill: {skill.name}\n\n"
        f"## Trigger / when to use\n{skill.trigger_description or skill.description}\n\n"
        f"## Skill body\n{skill.body}\n"
    )
    if load_mode == "system_prepend":
        return skill_block, user
    # user_append mode
    return None, skill_block + "\n---\n\n" + user


def run_attempt(
    client: ModelHubClient,
    *,
    model: str,
    task: TaskSpec,
    skill: Optional[SkillRecord],
    attempt: int,
    condition: str,
    temperature: float,
    max_output_tokens: int,
    load_mode: str,
) -> RunAttempt:
    instructions, inp = build_messages(task, skill, load_mode=load_mode)
    prompt_log = (instructions or "") + "\n\n" + str(inp)
    try:
        raw = client.responses_create(
            model=model,
            input=inp,
            instructions=instructions,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        )
        text = ModelHubClient.extract_text(raw)
        inp_tok, out_tok = ModelHubClient.usage_tokens(raw)
        latency = int((raw.get("_skill_arena") or {}).get("latency_ms") or 0)
        triggered = None
        if skill is not None:
            # Heuristic: skill name or distinctive phrase appears / structure followed
            triggered = bool(
                skill.name.lower() in text.lower()
                or any(
                    phrase.lower() in text.lower()
                    for phrase in _distinctive_phrases(skill.body)[:3]
                )
            )
        return RunAttempt(
            attempt=attempt,
            condition=condition,  # type: ignore[arg-type]
            model=model,
            skill_id=skill.skill_id if skill else None,
            prompt=prompt_log[:20000],
            response_text=text,
            raw_response={"id": raw.get("id"), "usage": raw.get("usage")},
            latency_ms=latency,
            input_tokens=inp_tok,
            output_tokens=out_tok,
            triggered=triggered,
        )
    except Exception as e:
        return RunAttempt(
            attempt=attempt,
            condition=condition,  # type: ignore[arg-type]
            model=model,
            skill_id=skill.skill_id if skill else None,
            prompt=prompt_log[:20000],
            error=str(e),
        )


def _distinctive_phrases(body: str) -> list[str]:
    lines = [ln.strip("# ").strip() for ln in body.splitlines() if ln.strip()]
    return [ln for ln in lines if 8 <= len(ln) <= 80][:10]


JUDGE_SYSTEM = """You are a blind preference judge for Agent Skill evaluation.
Compare answer A and answer B for the same task. Ignore which might use a skill.
Decide which answer better satisfies the scoring rubric.
Return STRICT JSON only:
{
  "winner": "A" | "B" | "tie",
  "rationale": "short reason",
  "scores": {"A": 0-10, "B": 0-10}
}
"""


def judge_pair(
    client: ModelHubClient,
    *,
    judge_model: str,
    task: TaskSpec,
    text_a: str,
    text_b: str,
    order_label: str,
) -> dict[str, Any]:
    rubric = "\n".join(f"- {x}" for x in task.scoring_rubric)
    user = (
        f"Task: {task.title}\n\nPrompt:\n{task.prompt}\n\n"
        f"Expected behavior:\n{task.expected_behavior}\n\n"
        f"Scoring rubric:\n{rubric}\n\n"
        f"Answer A:\n{text_a}\n\nAnswer B:\n{text_b}\n"
    )
    raw = client.responses_create(
        model=judge_model,
        input=user,
        instructions=JUDGE_SYSTEM,
        temperature=0.0,
        max_output_tokens=800,
    )
    text = ModelHubClient.extract_text(raw)
    parsed = _parse_json_object(text)
    parsed["_raw_text"] = text
    parsed["_order"] = order_label
    return parsed


def _parse_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    try:
        return json.loads(text)
    except Exception:
        m = re.search(r"\{[\s\S]*\}", text)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                pass
    return {"winner": "tie", "rationale": f"unparseable_judge_output: {text[:300]}", "scores": {}}


def preference_for_skill(winner: str, order: str) -> str:
    if winner == "tie":
        return "tie"
    skill_is_b = order.startswith("A=baseline")
    if skill_is_b:
        return "win" if winner == "B" else "lose"
    return "win" if winner == "A" else "lose"


def evaluate_pilot(cfg: dict[str, Any], *, dry_run: bool = False) -> Path:
    catalog_dir = resolve_path(cfg, "catalog")
    tasks_dir = Path(cfg["root"]) / cfg["paths"]["tasks"]
    runs_dir = resolve_path(cfg, "runs")
    run_id = uuid.uuid4().hex[:10]
    run_dir = runs_dir / f"pilot_{run_id}"
    run_dir.mkdir(parents=True, exist_ok=True)

    skills = load_jsonl(catalog_dir / "skills_filtered.jsonl")
    if not skills:
        skills = load_jsonl(catalog_dir / "skills_raw.jsonl")
    pilot_n = int(cfg.get("eval", {}).get("pilot_skill_count", 30))
    skills = skills[:pilot_n]
    tasks = load_tasks(tasks_dir)
    if not tasks:
        raise RuntimeError(f"No tasks found under {tasks_dir}")

    repeats = int(cfg.get("eval", {}).get("repeats", 3))
    executor = cfg["models"]["executor"]
    judge_model = cfg["models"]["judge"]
    load_mode = cfg.get("eval", {}).get("load_skill_mode", "system_prepend")

    client = None
    if not dry_run:
        mh = cfg["modelhub"]
        client = ModelHubClient(mh["base_url"], api_key=mh["api_key"], ak=mh["ak"])

    meta = {
        "run_id": run_id,
        "executor_model": executor,
        "judge_model": judge_model,
        "skills": [s.skill_id for s in skills],
        "tasks": [t.task_id for t in tasks],
        "repeats": repeats,
        "dry_run": dry_run,
    }
    (run_dir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    results: list[PairResult] = []
    for skill in skills:
        # Match tasks by category when possible, else all
        matched = [t for t in tasks if t.category == skill.category]
        if not matched:
            matched = tasks[:2]
        for task in matched[:2]:  # pilot: 2 tasks/skill to bound cost
            baseline_attempts: list[RunAttempt] = []
            skill_attempts: list[RunAttempt] = []
            for i in range(1, repeats + 1):
                if dry_run or client is None:
                    baseline_attempts.append(
                        RunAttempt(
                            attempt=i,
                            condition="baseline",
                            model=executor,
                            prompt=task.prompt,
                            response_text=f"[dry-run baseline] {task.title}",
                        )
                    )
                    skill_attempts.append(
                        RunAttempt(
                            attempt=i,
                            condition="with_skill",
                            model=executor,
                            skill_id=skill.skill_id,
                            prompt=task.prompt,
                            response_text=f"[dry-run with-skill:{skill.name}] {task.title}",
                            triggered=True,
                        )
                    )
                else:
                    baseline_attempts.append(
                        run_attempt(
                            client,
                            model=executor,
                            task=task,
                            skill=None,
                            attempt=i,
                            condition="baseline",
                            temperature=float(cfg["eval"].get("temperature_executor", 0.2)),
                            max_output_tokens=int(cfg["eval"].get("max_output_tokens", 4096)),
                            load_mode=load_mode,
                        )
                    )
                    skill_attempts.append(
                        run_attempt(
                            client,
                            model=executor,
                            task=task,
                            skill=skill,
                            attempt=i,
                            condition="with_skill",
                            temperature=float(cfg["eval"].get("temperature_executor", 0.2)),
                            max_output_tokens=int(cfg["eval"].get("max_output_tokens", 4096)),
                            load_mode=load_mode,
                        )
                    )

            # Use first successful attempt each side for judging (pilot)
            b_text = next((a.response_text for a in baseline_attempts if a.response_text), "")
            s_text = next((a.response_text for a in skill_attempts if a.response_text), "")
            verdicts: list[JudgeVerdict] = []
            orders = [
                ("A=baseline,B=skill", b_text, s_text),
                ("A=skill,B=baseline", s_text, b_text),
            ]
            if not cfg.get("judge", {}).get("swap_order", True):
                orders = orders[:1]
            for order_label, a_text, b_side in orders:
                if dry_run or client is None:
                    parsed = {"winner": "B" if order_label.startswith("A=baseline") else "A", "rationale": "dry-run", "scores": {"A": 6, "B": 7}}
                else:
                    parsed = judge_pair(
                        client,
                        judge_model=judge_model,
                        task=task,
                        text_a=a_text,
                        text_b=b_side,
                        order_label=order_label,
                    )
                winner = str(parsed.get("winner") or "tie")
                if winner not in ("A", "B", "tie"):
                    winner = "tie"
                verdicts.append(
                    JudgeVerdict(
                        task_id=task.task_id,
                        skill_id=skill.skill_id,
                        pair_id=f"{task.task_id}__{skill.skill_id}",
                        order=order_label,  # type: ignore[arg-type]
                        winner=winner,  # type: ignore[arg-type]
                        preference_for_skill=preference_for_skill(winner, order_label),  # type: ignore[arg-type]
                        rationale=str(parsed.get("rationale") or ""),
                        scores=parsed.get("scores") or {},
                        judge_model=judge_model,
                        raw=parsed,
                    )
                )

            wins = sum(1 for v in verdicts if v.preference_for_skill == "win")
            loses = sum(1 for v in verdicts if v.preference_for_skill == "lose")
            decided = wins + loses
            win_rate = (wins / decided) if decided else 0.5
            trig = [a.triggered for a in skill_attempts if a.triggered is not None]
            trig_rate = (sum(1 for t in trig if t) / len(trig)) if trig else None

            pair = PairResult(
                task_id=task.task_id,
                skill_id=skill.skill_id,
                baseline_attempts=baseline_attempts,
                skill_attempts=skill_attempts,
                judge_verdicts=verdicts,
                trigger_success_rate=trig_rate,
                skill_win_rate=win_rate,
            )
            results.append(pair)
            out = run_dir / f"{task.task_id}__{skill.skill_id}.json"
            out.write_text(pair.model_dump_json(indent=2) + "\n", encoding="utf-8")
            print(f"[pair] {skill.skill_id} × {task.task_id} win_rate={win_rate:.2f}")

    summary_path = run_dir / "pairs.jsonl"
    with summary_path.open("w", encoding="utf-8") as f:
        for p in results:
            f.write(
                json.dumps(
                    {
                        "task_id": p.task_id,
                        "skill_id": p.skill_id,
                        "skill_win_rate": p.skill_win_rate,
                        "trigger_success_rate": p.trigger_success_rate,
                    }
                )
                + "\n"
            )
    print(f"Pilot run written to {run_dir}")
    return run_dir
