from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import quote

import httpx

from .config import resolve_path
from .schema import SkillRecord
from .skill_parse import parse_skill_markdown


def _gh_token() -> str:
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN") or ""
    if token:
        return token
    try:
        out = subprocess.check_output(
            ["gh", "auth", "token"], text=True, stderr=subprocess.DEVNULL
        ).strip()
        return out
    except Exception:
        return ""


def github_search_code(query: str, *, per_page: int = 50, max_pages: int = 2) -> list[dict[str, Any]]:
    token = _gh_token()
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "skill-arena",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    items: list[dict[str, Any]] = []
    with httpx.Client(timeout=60.0, headers=headers) as client:
        for page in range(1, max_pages + 1):
            url = (
                "https://api.github.com/search/code"
                f"?q={quote(query)}&per_page={per_page}&page={page}"
            )
            resp = client.get(url)
            if resp.status_code == 403:
                # rate limit — stop gracefully
                break
            if resp.status_code >= 400:
                raise RuntimeError(f"GitHub search failed {resp.status_code}: {resp.text[:400]}")
            data = resp.json()
            batch = data.get("items") or []
            items.extend(batch)
            if len(batch) < per_page:
                break
            time.sleep(1.2)
    return items


def fetch_raw_file(html_url: str, download_url: str | None = None) -> str:
    """Fetch raw file contents from a GitHub code search hit."""
    headers = {"User-Agent": "skill-arena"}
    token = _gh_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"

    candidates = []
    if download_url:
        candidates.append(download_url)
    # Convert blob URL → raw.githubusercontent.com
    if "github.com" in html_url and "/blob/" in html_url:
        candidates.append(
            html_url.replace("https://github.com/", "https://raw.githubusercontent.com/").replace(
                "/blob/", "/"
            )
        )
    candidates.append(html_url)

    with httpx.Client(timeout=60.0, headers=headers, follow_redirects=True) as client:
        for url in candidates:
            try:
                r = client.get(url)
                if r.status_code == 200 and r.text.strip():
                    # Prefer text/markdown-ish
                    return r.text
            except Exception:
                continue
    raise RuntimeError(f"Failed to fetch {html_url}")


def collect_from_github(cfg: dict[str, Any]) -> list[SkillRecord]:
    raw_dir = resolve_path(cfg, "skills_raw")
    catalog_dir = resolve_path(cfg, "catalog")
    queries: Iterable[str] = cfg.get("collect", {}).get("queries") or []
    max_per_query = int(cfg.get("collect", {}).get("max_per_query", 100))
    target = int(cfg.get("collect", {}).get("target_raw", 300))

    seen_urls: set[str] = set()
    seen_hashes: set[str] = set()
    records: list[SkillRecord] = []

    for q in queries:
        if len(records) >= target:
            break
        pages = max(1, max_per_query // 50)
        hits = github_search_code(q, per_page=min(50, max_per_query), max_pages=pages)
        for hit in hits:
            if len(records) >= target:
                break
            html_url = hit.get("html_url") or ""
            if not html_url or html_url in seen_urls:
                continue
            seen_urls.add(html_url)
            repo = (hit.get("repository") or {}).get("full_name") or ""
            path = hit.get("path") or ""
            author = ((hit.get("repository") or {}).get("owner") or {}).get("login") or ""
            try:
                text = fetch_raw_file(html_url, hit.get("url"))
            except Exception as e:
                # GitHub code search contents_url needs Accept raw — try contents API
                contents_url = hit.get("url")
                if not contents_url:
                    continue
                try:
                    text = _fetch_contents_api(contents_url)
                except Exception:
                    print(f"[skip] {html_url}: {e}")
                    continue

            if "SKILL.md" not in path and "name:" not in text[:500]:
                # keep only skill-like files
                if "skills/" not in path.lower():
                    continue

            rec = parse_skill_markdown(
                text,
                source_url=html_url,
                source_repo=repo,
                source_path=path,
                author=author,
            )
            if rec.body_hash in seen_hashes:
                continue
            if len(rec.body.strip()) < int(cfg.get("filter", {}).get("drop_empty_body_chars", 80)):
                rec.excluded_reason = "empty_body"
                continue
            seen_hashes.add(rec.body_hash)
            records.append(rec)

            # Persist raw
            out = raw_dir / f"{rec.skill_id}.md"
            out.write_text(
                f"---\nname: {rec.name}\ndescription: {json.dumps(rec.description, ensure_ascii=False)}\n"
                f"source_url: {rec.source_url}\nsource_repo: {rec.source_repo}\n"
                f"source_path: {rec.source_path}\nauthor: {rec.author}\n"
                f"body_hash: {rec.body_hash}\n---\n\n{rec.body}\n",
                encoding="utf-8",
            )

    catalog_path = catalog_dir / "skills_raw.jsonl"
    with catalog_path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(rec.model_dump_json() + "\n")
    print(f"Collected {len(records)} skills → {catalog_path}")
    return records


def _fetch_contents_api(api_url: str) -> str:
    token = _gh_token()
    headers = {
        "Accept": "application/vnd.github.raw",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "skill-arena",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with httpx.Client(timeout=60.0, headers=headers, follow_redirects=True) as client:
        r = client.get(api_url)
        if r.status_code >= 400:
            raise RuntimeError(f"contents api {r.status_code}")
        return r.text


def seed_builtin_skills(cfg: dict[str, Any]) -> list[SkillRecord]:
    """Ship builtin skills so the pipeline can dry-run without GitHub quota."""
    from .seed_bank import BUILTINS

    raw_dir = resolve_path(cfg, "skills_raw")
    catalog_dir = resolve_path(cfg, "catalog")
    builtins = BUILTINS
    records: list[SkillRecord] = []
    for b in builtins:
        text = (
            f"---\nname: {b['name']}\ndescription: {b['description']}\n"
            f"category: {b.get('category', 'other')}\n---\n\n{b['body']}\n"
        )
        rec = parse_skill_markdown(
            text,
            source_url=f"builtin://{b['name']}",
            source_repo="builtin/skill-arena",
            source_path=f"skills/{b['name']}/SKILL.md",
            author="skill-arena",
            skill_id=f"builtin__{b['name']}",
        )
        records.append(rec)
        (raw_dir / f"{rec.skill_id}.md").write_text(text, encoding="utf-8")

    path = catalog_dir / "skills_raw.jsonl"
    # append/merge unique
    existing = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                obj = json.loads(line)
                existing[obj["skill_id"]] = obj
    for rec in records:
        existing[rec.skill_id] = json.loads(rec.model_dump_json())
    with path.open("w", encoding="utf-8") as f:
        for obj in existing.values():
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    print(f"Seeded {len(records)} builtin skills (catalog size={len(existing)})")
    return records
