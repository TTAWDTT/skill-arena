from skill_arena.skill_parse import body_hash, infer_category, parse_skill_markdown
from skill_arena.schema import Category


def test_body_hash_stable():
    assert body_hash("Hello  world") == body_hash("Hello world")


def test_parse_frontmatter():
    text = """---
name: demo
description: Use when writing unit tests for Python helpers.
---

# Demo

## Example
```python
assert 1 + 1 == 2
```
"""
    rec = parse_skill_markdown(
        text,
        source_url="https://example.com/SKILL.md",
        source_repo="ex/repo",
        source_path="skills/demo/SKILL.md",
    )
    assert rec.name == "demo"
    assert rec.has_examples
    assert rec.structure_ok
    assert rec.coarse_score >= 0.4
    assert infer_category(rec.name, rec.description, rec.body) == Category.coding
