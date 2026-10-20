#!/usr/bin/env python3
"""Collect SKILL.md files via `gh api` code search (more reliable than raw git clone)."""

from __future__ import annotations

import json
import subprocess
import time
import urllib.parse
from pathlib import Path

from skill_arena.config import load_config
from skill_arena.skill_parse import parse_skill_markdown


def gh_api(path: str, extra_headers: list[str] | None = None) -> str:
    cmd = ["gh", "api", path]
    for h in extra_headers or []:
        cmd.extend(["-H", h])
    return subprocess.check_output(cmd, text=True)


def main() -> None:
    cfg = load_config()
    target = int(cfg.get("collect", {}).get("target_raw", 350))
    raw_dir = Path(cfg["root"]) / "skills" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    catalog = Path(cfg["root"]) / "catalog" / "skills_raw.jsonl"
    catalog.parent.mkdir(parents=True, exist_ok=True)

    existing: dict[str, dict] = {}
    if catalog.exists():
        for line in catalog.read_text(encoding="utf-8").splitlines():
            if line.strip():
                obj = json.loads(line)
                existing[obj["body_hash"]] = obj

    queries = cfg.get("collect", {}).get("queries") or [
        "filename:SKILL.md path:skills",
        'filename:SKILL.md "description:"',
    ]
    seen_urls: set[str] = set()
    added = 0

    for q in queries:
        for page in range(1, 8):
            if len(existing) >= target:
                break
            url = "search/code?" + urllib.parse.urlencode(
                {"q": q, "per_page": 50, "page": page}
            )
            try:
                data = json.loads(gh_api(url))
            except subprocess.CalledProcessError as e:
                print("search fail", getattr(e, "output", e) )
                break
            items = data.get("items") or []
            print(f"q={q!r} page={page} hits={len(items)} catalog={len(existing)}")
            if not items:
                break
            for hit in items:
                if len(existing) >= target:
                    break
                html = hit.get("html_url") or ""
                if not html or html in seen_urls:
                    continue
                seen_urls.add(html)
                api = hit.get("url")
                if not api:
                    continue
                try:
                    # api path is full URL; gh api accepts path after api.github.com/
                    api_path = api.replace("https://api.github.com/", "")
                    text = gh_api(
                        api_path, ["Accept: application/vnd.github.raw"]
                    )
                except Exception:
                    continue
                repo = (hit.get("repository") or {}).get("full_name") or ""
                path = hit.get("path") or ""
                author = ((hit.get("repository") or {}).get("owner") or {}).get("login") or ""
                rec = parse_skill_markdown(
                    text,
                    source_url=html,
                    source_repo=repo,
                    source_path=path,
                    author=author,
                )
                if rec.body_hash in existing or len(rec.body.strip()) < 80:
                    continue
                existing[rec.body_hash] = json.loads(rec.model_dump_json())
                (raw_dir / f"{rec.skill_id}.md").write_text(
                    f"---\nname: {rec.name}\ndescription: {json.dumps(rec.description, ensure_ascii=False)}\n"
                    f"source_url: {rec.source_url}\nsource_repo: {rec.source_repo}\n"
                    f"category: {rec.category.value}\nbody_hash: {rec.body_hash}\n---\n\n{rec.body}\n",
                    encoding="utf-8",
                )
                added += 1
            time.sleep(1.2)
        if len(existing) >= target:
            break

    catalog.write_text(
        "\n".join(json.dumps(o, ensure_ascii=False) for o in existing.values()) + "\n",
        encoding="utf-8",
    )
    print(f"DONE added={added} catalog={len(existing)} → {catalog}")


if __name__ == "__main__":
    main()
