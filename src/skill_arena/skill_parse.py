from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any, Optional

import yaml

from .schema import Category, SkillRecord

CATEGORY_KEYWORDS: dict[Category, tuple[str, ...]] = {
    Category.coding: (
        "code",
        "coding",
        "programming",
        "refactor",
        "debug",
        "implement",
        "python",
        "typescript",
        "git",
        "test",
        "tdd",
    ),
    Category.review: (
        "review",
        "pr",
        "pull request",
        "code review",
        "critique",
        "security review",
    ),
    Category.writing: (
        "writ",
        "blog",
        "docs",
        "documentation",
        "copy",
        "编辑",
        "写作",
        "文案",
    ),
    Category.slides: ("slide", "pptx", "presentation", "deck", "演讲", "幻灯"),
    Category.data: (
        "data",
        "sql",
        "pandas",
        "analytics",
        "etl",
        "sheet",
        "表格",
        "数据",
    ),
    Category.research: (
        "research",
        "search",
        "investigate",
        "literature",
        "调研",
        "研究",
    ),
}


def body_hash(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text.strip()).lower()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _frontmatter_and_body(text: str) -> tuple[dict[str, Any], str]:
    text = text.lstrip("\ufeff")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                meta = yaml.safe_load(parts[1]) or {}
                if not isinstance(meta, dict):
                    meta = {}
                return meta, parts[2].lstrip("\n")
            except Exception:
                return {}, text
    return {}, text


def infer_category(name: str, description: str, body: str) -> Category:
    blob = f"{name}\n{description}\n{body[:2000]}".lower()
    scores: dict[Category, int] = {c: 0 for c in Category}
    for cat, kws in CATEGORY_KEYWORDS.items():
        for kw in kws:
            if kw in blob:
                scores[cat] += 1
    best = max(scores.items(), key=lambda x: x[1])
    return best[0] if best[1] > 0 else Category.other


def has_examples(body: str) -> bool:
    patterns = [
        r"```",
        r"(?i)\bexample\b",
        r"(?i)\b示例\b",
        r"(?i)\bfor example\b",
        r"(?i)##\s*examples?",
    ]
    return any(re.search(p, body) for p in patterns)


def structure_ok(meta: dict[str, Any], body: str, description: str) -> bool:
    desc = description.strip() or str(meta.get("description") or "").strip()
    if len(desc) < 20:
        return False
    headings = re.findall(r"^#{1,3}\s+.+$", body, flags=re.M)
    # Cursor / Anthropic style: frontmatter name + heading, or substantial body
    if meta.get("name") and headings:
        return True
    if len(body.strip()) >= 80 and (headings or bool(meta.get("name"))):
        return True
    return False


def coarse_score(
    *,
    description: str,
    body: str,
    has_ex: bool,
    struct: bool,
    updated_at_remote: Optional[str],
) -> tuple[float, list[str]]:
    score = 0.0
    notes: list[str] = []
    if struct:
        score += 0.35
        notes.append("structure_ok")
    if len(description.strip()) >= 40:
        score += 0.25
        notes.append("clear_trigger")
    elif len(description.strip()) >= 20:
        score += 0.12
        notes.append("short_trigger")
    if has_ex:
        score += 0.2
        notes.append("has_examples")
    if len(body.strip()) >= 400:
        score += 0.1
        notes.append("substantial_body")
    if updated_at_remote:
        score += 0.1
        notes.append("has_remote_mtime")
    # Penalize obvious ads
    ad_hits = len(
        re.findall(
            r"(?i)\b(buy now|subscribe|discord\.gg|promo code|限时|加微信)\b", body
        )
    )
    if ad_hits:
        score -= 0.3 * ad_hits
        notes.append(f"ad_penalty:{ad_hits}")
    return max(0.0, min(1.0, score)), notes


def parse_skill_markdown(
    text: str,
    *,
    source_url: str,
    source_repo: str = "",
    source_path: str = "",
    author: str = "",
    updated_at_remote: Optional[str] = None,
    skill_id: Optional[str] = None,
) -> SkillRecord:
    meta, body = _frontmatter_and_body(text)
    name = str(meta.get("name") or Path(source_path).parent.name or "unnamed").strip()
    description = str(meta.get("description") or "").strip()
    if not description:
        # First non-empty non-heading line as weak trigger
        for line in body.splitlines():
            s = line.strip()
            if s and not s.startswith("#") and not s.startswith("```"):
                description = s[:300]
                break
    trigger = description
    h = body_hash(body if body.strip() else text)
    sid = skill_id or f"{source_repo.replace('/', '__')}__{h[:12]}"
    cat_raw = str(meta.get("category") or "").strip().lower()
    try:
        cat = Category(cat_raw) if cat_raw else infer_category(name, description, body)
    except ValueError:
        cat = infer_category(name, description, body)
    has_ex = has_examples(body)
    struct = structure_ok(meta, body, description)
    score, notes = coarse_score(
        description=description,
        body=body,
        has_ex=has_ex,
        struct=struct,
        updated_at_remote=updated_at_remote,
    )
    return SkillRecord(
        skill_id=sid,
        name=name,
        description=description,
        body=body.strip(),
        source_url=source_url,
        source_repo=source_repo,
        source_path=source_path,
        author=author or str(meta.get("author") or ""),
        license=str(meta.get("license") or ""),
        category=cat,
        tags=[str(t) for t in (meta.get("tags") or [])]
        if isinstance(meta.get("tags"), list)
        else [],
        trigger_description=trigger,
        body_hash=h,
        updated_at_remote=updated_at_remote,
        coarse_score=score,
        coarse_notes=notes,
        has_examples=has_ex,
        structure_ok=struct,
        meta={"frontmatter_keys": sorted(meta.keys())},
    )


def load_skill_file(path: Path, **kwargs: Any) -> SkillRecord:
    return parse_skill_markdown(path.read_text(encoding="utf-8", errors="replace"), **kwargs)
