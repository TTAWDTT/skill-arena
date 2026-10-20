from __future__ import annotations

import argparse
import json
from pathlib import Path

from .collect import collect_from_github, seed_builtin_skills
from .config import load_config
from .evaluate import evaluate_pilot
from .filter_skills import coarse_filter
from .ingest_local import ingest_skill_md_tree
from .modelhub import ModelHubClient
from .report import build_leaderboard, write_patterns_stub


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="skill-arena", description="Agent Skill Arena")
    parser.add_argument("--config", type=Path, default=None)
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("seed", help="Seed builtin skills for dry-run")
    p_collect = sub.add_parser("collect", help="Collect skills from GitHub")
    p_collect.add_argument("--also-seed", action="store_true")

    p_ingest = sub.add_parser("ingest-local", help="Ingest SKILL.md from a local tree")
    p_ingest.add_argument("root", type=Path)

    sub.add_parser("filter", help="Dedup + coarse filter + categorize")

    p_eval = sub.add_parser("eval-pilot", help="Run pilot A/B evaluation")
    p_eval.add_argument("--dry-run", action="store_true")
    p_eval.add_argument("--run-dir", type=Path, default=None, help="Existing run dir for report-only")

    p_report = sub.add_parser("report", help="Build leaderboard from a run dir")
    p_report.add_argument("--run-dir", type=Path, required=True)

    p_ping = sub.add_parser("ping-model", help="Smoke-test ModelHub with executor model")
    p_ping.add_argument("--prompt", default="Reply with exactly: pong")

    sub.add_parser("status", help="Show catalog / task counts")

    args = parser.parse_args(argv)
    cfg = load_config(args.config)

    if args.cmd == "seed":
        seed_builtin_skills(cfg)
        write_patterns_stub(cfg)
    elif args.cmd == "collect":
        if args.also_seed:
            seed_builtin_skills(cfg)
        collect_from_github(cfg)
    elif args.cmd == "ingest-local":
        ingest_skill_md_tree(cfg, args.root)
    elif args.cmd == "filter":
        coarse_filter(cfg)
    elif args.cmd == "eval-pilot":
        run_dir = evaluate_pilot(cfg, dry_run=args.dry_run)
        build_leaderboard(cfg, run_dir)
        write_patterns_stub(cfg)
    elif args.cmd == "report":
        build_leaderboard(cfg, args.run_dir)
        write_patterns_stub(cfg)
    elif args.cmd == "ping-model":
        mh = cfg["modelhub"]
        client = ModelHubClient(mh["base_url"], api_key=mh["api_key"], ak=mh["ak"])
        model = cfg["models"]["executor"]
        raw = client.responses_create(model=model, input=args.prompt, max_output_tokens=64)
        print(json.dumps({"model": model, "text": ModelHubClient.extract_text(raw), "usage": raw.get("usage")}, ensure_ascii=False, indent=2))
    elif args.cmd == "status":
        root = Path(cfg["root"])
        def count(p: Path) -> int:
            return len(list(p.glob("*"))) if p.exists() else 0
        print(
            json.dumps(
                {
                    "skills_raw": count(root / "skills" / "raw"),
                    "skills_filtered": count(root / "skills" / "filtered"),
                    "catalog_jsonl": {
                        "raw": _lines(root / "catalog" / "skills_raw.jsonl"),
                        "filtered": _lines(root / "catalog" / "skills_filtered.jsonl"),
                    },
                    "tasks": len(list((root / "tasks").rglob("*.yaml"))),
                    "runs": count(root / "runs"),
                    "models": cfg["models"],
                    "modelhub_base_url": cfg["modelhub"]["base_url"],
                    "has_api_key": bool(cfg["modelhub"]["api_key"] or cfg["modelhub"]["ak"]),
                },
                indent=2,
            )
        )


def _lines(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


if __name__ == "__main__":
    main()
