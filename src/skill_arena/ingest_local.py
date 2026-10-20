from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .config import resolve_path
from .schema import SkillRecord
from .skill_parse import parse_skill_markdown


def ingest_skill_md_tree(cfg: dict[str, Any], root: Path) -> list[SkillRecord]:
    """Ingest all SKILL.md under a local directory tree (e.g. cloned repos)."""
    raw_dir = resolve_path(cfg, "skills_raw")
    catalog_dir = resolve_path(cfg, "catalog")
    catalog_path = catalog_dir / "skills_raw.jsonl"

    existing: dict[str, dict] = {}
    if catalog_path.exists():
        for line in catalog_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                obj = json.loads(line)
                existing[obj["body_hash"]] = obj

    seen_hashes = set(existing.keys())
    added: list[SkillRecord] = []
    for path in sorted(root.rglob("SKILL.md")):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        # Infer repo from skills/_work/<owner>__<repo>/...
        parts = path.parts
        repo = ""
        for i, p in enumerate(parts):
            if p == "_work" and i + 1 < len(parts):
                repo = parts[i + 1].replace("__", "/", 1)
                break
        rel = str(path.relative_to(root)) if path.is_relative_to(root) else str(path)
        source_url = (
            f"https://github.com/{repo}/blob/main/{path.name}"
            if repo and "/" in repo
            else path.as_uri()
        )
        # better path in url
        if repo and "_work" in parts:
            idx = parts.index("_work")
            repo_root = Path(*parts[: idx + 2])
            try:
                rel_in_repo = path.relative_to(repo_root).as_posix()
                source_url = f"https://github.com/{repo}/blob/HEAD/{rel_in_repo}"
            except Exception:
                pass

        rec = parse_skill_markdown(
            text,
            source_url=source_url,
            source_repo=repo,
            source_path=rel,
            author=repo.split("/")[0] if "/" in repo else "",
        )
        if rec.body_hash in seen_hashes:
            continue
        if len(rec.body.strip()) < 80:
            continue
        seen_hashes.add(rec.body_hash)
        added.append(rec)
        existing[rec.body_hash] = json.loads(rec.model_dump_json())
        (raw_dir / f"{rec.skill_id}.md").write_text(
            f"---\nname: {rec.name}\ndescription: {json.dumps(rec.description, ensure_ascii=False)}\n"
            f"source_url: {rec.source_url}\nsource_repo: {rec.source_repo}\n"
            f"category: {rec.category.value}\nbody_hash: {rec.body_hash}\n---\n\n{rec.body}\n",
            encoding="utf-8",
        )

    with catalog_path.open("w", encoding="utf-8") as f:
        for obj in existing.values():
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    print(f"Ingested +{len(added)} from {root} (catalog={len(existing)})")
    return added
