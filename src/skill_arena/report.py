from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from .config import resolve_path
from .filter_skills import load_jsonl
from .schema import SkillRecord


def build_leaderboard(cfg: dict[str, Any], run_dir: Path) -> Path:
    reports_dir = resolve_path(cfg, "reports")
    skills = {s.skill_id: s for s in load_jsonl(resolve_path(cfg, "catalog") / "skills_filtered.jsonl")}
    if not skills:
        skills = {s.skill_id: s for s in load_jsonl(resolve_path(cfg, "catalog") / "skills_raw.jsonl")}

    rows = []
    for path in sorted(run_dir.glob("*.json")):
        if path.name in ("meta.json",):
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if "skill_win_rate" not in data:
            continue
        sid = data["skill_id"]
        skill = skills.get(sid)
        rows.append(
            {
                "skill_id": sid,
                "name": skill.name if skill else sid,
                "category": skill.category.value if skill else "other",
                "source_url": skill.source_url if skill else "",
                "win_rate": data.get("skill_win_rate"),
                "trigger_success_rate": data.get("trigger_success_rate"),
                "task_id": data.get("task_id"),
            }
        )

    # Aggregate per skill
    agg: dict[str, dict[str, Any]] = {}
    for r in rows:
        a = agg.setdefault(
            r["skill_id"],
            {
                "skill_id": r["skill_id"],
                "name": r["name"],
                "category": r["category"],
                "source_url": r["source_url"],
                "win_rates": [],
                "triggers": [],
            },
        )
        if r["win_rate"] is not None:
            a["win_rates"].append(float(r["win_rate"]))
        if r["trigger_success_rate"] is not None:
            a["triggers"].append(float(r["trigger_success_rate"]))

    ranked = []
    for a in agg.values():
        wr = sum(a["win_rates"]) / len(a["win_rates"]) if a["win_rates"] else 0.0
        tr = sum(a["triggers"]) / len(a["triggers"]) if a["triggers"] else None
        ranked.append(
            {
                **{k: a[k] for k in ("skill_id", "name", "category", "source_url")},
                "avg_win_rate": round(wr, 4),
                "avg_trigger_success": None if tr is None else round(tr, 4),
                "n_pairs": len(a["win_rates"]),
                "beats_baseline": wr > 0.55,
            }
        )
    ranked.sort(key=lambda x: x["avg_win_rate"], reverse=True)

    by_cat: dict[str, list] = defaultdict(list)
    for r in ranked:
        by_cat[r["category"]].append(r)

    md = ["# Skill Arena Leaderboard\n"]
    md.append(f"Source run: `{run_dir}`\n")
    md.append("Win rate = fraction of blind A/B judgments preferring with-skill over baseline "
              "(order-swapped). Threshold for curated: **> 0.55**.\n")

    md.append("## Overall\n")
    md.append("| Rank | Skill | Category | Win rate | Trigger | Pairs | Source |\n")
    md.append("| --- | --- | --- | --- | --- | --- | --- |\n")
    for i, r in enumerate(ranked, 1):
        trig = "—" if r["avg_trigger_success"] is None else f"{r['avg_trigger_success']:.2f}"
        md.append(
            f"| {i} | {r['name']} | {r['category']} | {r['avg_win_rate']:.2f} | {trig} | "
            f"{r['n_pairs']} | [link]({r['source_url']}) |\n"
        )

    for cat, items in sorted(by_cat.items()):
        md.append(f"\n## Category: {cat}\n")
        md.append("| Rank | Skill | Win rate | Source |\n| --- | --- | --- | --- |\n")
        for i, r in enumerate(items, 1):
            md.append(
                f"| {i} | {r['name']} | {r['avg_win_rate']:.2f} | [link]({r['source_url']}) |\n"
            )

    out = reports_dir / "leaderboard.md"
    out.write_text("".join(md), encoding="utf-8")
    (reports_dir / "leaderboard.json").write_text(
        json.dumps(ranked, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    # curated copy pointers
    curated_dir = resolve_path(cfg, "curated")
    curated = [r for r in ranked if r["beats_baseline"]]
    (curated_dir / "index.json").write_text(
        json.dumps(curated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    # copy skill bodies when available
    filtered = resolve_path(cfg, "skills_filtered")
    for r in curated:
        src = filtered / f"{r['skill_id']}.md"
        if src.exists():
            (curated_dir / f"{r['skill_id']}.md").write_text(
                src.read_text(encoding="utf-8"), encoding="utf-8"
            )

    print(f"Leaderboard → {out} (curated={len(curated)})")
    return out


def write_patterns_stub(cfg: dict[str, Any]) -> Path:
    reports_dir = resolve_path(cfg, "reports")
    path = reports_dir / "patterns.md"
    if path.exists():
        return path
    path.write_text(
        """# Skill Writing Patterns (draft)

This report is filled after pilot / full eval. Early hypotheses to test:

## Length
- Too short (<150 words): often no measurable lift.
- Very long (>2k words): may dilute trigger compliance / waste tokens.

## Structure
- Clear `When to use` / trigger description correlates with higher trigger success.
- Numbered steps beat prose blobs for coding / review skills.

## Examples
- At least one concrete input→output example helps writing and coding categories.

## Failure modes
- Ads / promo language → coarse-filtered out.
- Skills that require external accounts excluded from v1 arena.
- Category mismatch (skill vs task) depresses win rate — match before judging.

## Method notes
- Executor: `gpt-5.6-luna`
- Judge: `gpt-5.6-sol` (blind A/B, order swapped)
- Load mode: skill body prepended as `instructions` (offline approximation of real trigger)

Update this file after inspecting curated winners vs losers.
""",
        encoding="utf-8",
    )
    return path
