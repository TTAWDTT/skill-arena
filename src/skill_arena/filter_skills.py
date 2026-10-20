from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from .config import resolve_path
from .schema import SkillRecord


def load_jsonl(path: Path) -> list[SkillRecord]:
    rows: list[SkillRecord] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(SkillRecord.model_validate_json(line))
    return rows


def coarse_filter(cfg: dict[str, Any]) -> list[SkillRecord]:
    catalog_dir = resolve_path(cfg, "catalog")
    filtered_dir = resolve_path(cfg, "skills_filtered")
    raw = load_jsonl(catalog_dir / "skills_raw.jsonl")

    # Dedup by body_hash (keep highest coarse_score)
    by_hash: dict[str, SkillRecord] = {}
    for rec in raw:
        prev = by_hash.get(rec.body_hash)
        if prev is None or rec.coarse_score > prev.coarse_score:
            by_hash[rec.body_hash] = rec
    deduped = list(by_hash.values())

    min_desc = int(cfg.get("filter", {}).get("min_description_chars", 20))
    survivors: list[SkillRecord] = []
    rejected: list[SkillRecord] = []
    for rec in deduped:
        reasons = []
        if len(rec.body.strip()) < int(cfg.get("filter", {}).get("drop_empty_body_chars", 80)):
            reasons.append("empty_body")
        if len(rec.description.strip()) < min_desc:
            reasons.append("weak_trigger")
        if "ad_penalty" in " ".join(rec.coarse_notes):
            reasons.append("ad_like")
        if not rec.structure_ok and rec.coarse_score < 0.35:
            reasons.append("poor_structure")
        if reasons:
            rec.excluded_reason = ",".join(reasons)
            rejected.append(rec)
        else:
            survivors.append(rec)

    survivors.sort(key=lambda r: r.coarse_score, reverse=True)
    keep_ratio = float(cfg.get("filter", {}).get("keep_ratio_hint", 0.5))
    keep_n = max(1, int(len(survivors) * keep_ratio)) if survivors else 0
    # Keep at least all above 0.45, plus top keep_n
    kept = [r for r in survivors if r.coarse_score >= 0.45]
    for r in survivors:
        if len(kept) >= max(keep_n, len(kept)):
            break
        if r not in kept:
            kept.append(r)

    out_path = catalog_dir / "skills_filtered.jsonl"
    with out_path.open("w", encoding="utf-8") as f:
        for rec in kept:
            f.write(rec.model_dump_json() + "\n")
            # also write body for eval loader
            (filtered_dir / f"{rec.skill_id}.md").write_text(
                f"---\nname: {rec.name}\ndescription: {json.dumps(rec.description, ensure_ascii=False)}\n"
                f"category: {rec.category.value}\n---\n\n{rec.body}\n",
                encoding="utf-8",
            )

    rej_path = catalog_dir / "skills_rejected.jsonl"
    with rej_path.open("w", encoding="utf-8") as f:
        for rec in rejected + [r for r in survivors if r not in kept]:
            if rec not in rejected:
                rec.excluded_reason = rec.excluded_reason or "below_keep_cutoff"
            f.write(rec.model_dump_json() + "\n")

    cats = Counter(r.category.value for r in kept)
    summary = {
        "raw": len(raw),
        "deduped": len(deduped),
        "kept": len(kept),
        "rejected": len(rejected) + max(0, len(survivors) - len(kept)),
        "by_category": dict(cats),
    }
    (catalog_dir / "filter_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False))
    return kept
