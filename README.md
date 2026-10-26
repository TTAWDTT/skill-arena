# Skill Arena

Collect Agent Skills from GitHub, coarse-filter them, then run **baseline vs with-skill** A/B evaluation to find skills that actually improve model performance.

## Models (v1)

| Role | Model id |
|------|----------|
| Executor (run tasks) | `gpt-5.6-luna` |
| Judge (blind A/B) | `gpt-5.6-sol` |

Calls go through the model gateway **Responses API**:

```text
POST {MODEL_GATEWAY_URL}/responses
```

Set `MODEL_GATEWAY_URL` in `.env`. If it is unset, the placeholder below is used and will not resolve:

```text
<YOUR_MODEL_GATEWAY>
```

Also set `MODEL_GATEWAY_API_KEY` or `MODEL_GATEWAY_USER_TOKEN`, and optionally `MODEL_GATEWAY_AK` (see `.env.example`).

## Layout

```text
skills/raw/          # collected skill markdown
skills/filtered/     # after coarse filter
catalog/             # jsonl metadata + filter summary
tasks/<category>/    # task bank (yaml)
runs/                # per-run attempt + judge artifacts
reports/             # leaderboard.md, patterns.md
curated/             # skills that beat baseline
src/skill_arena/     # pipeline code
```

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # set MODEL_GATEWAY_URL, MODEL_GATEWAY_API_KEY or MODEL_GATEWAY_USER_TOKEN, and MODEL_GATEWAY_AK

# Stage 0 smoke (no API)
skill-arena seed
skill-arena filter
skill-arena eval-pilot --dry-run

# Stage 1 collect (needs GitHub auth: gh auth login)
skill-arena collect --also-seed
skill-arena filter

# Stage 3 pilot (needs the model gateway)
skill-arena ping-model
skill-arena eval-pilot
```

## Method (short)

1. **Collect** `SKILL.md` via GitHub code search; dedupe by body hash.
2. **Coarse filter** on structure, trigger clarity, examples, ad-likeness; auto-tag category.
3. **Tasks** per category with rubric (and optional rule checks / tests).
4. **Eval**: for each (skill, task), run baseline × N and with-skill × N on `gpt-5.6-luna`.
5. **Judge**: `gpt-5.6-sol` blind A/B with order swap → win rate vs baseline.
6. **Curate** skills with win rate > 0.55; write `reports/patterns.md`.

### Out of scope (v1)

- Skills that need real external accounts
- Multi-model cross evaluation (v2)
- Rewriting upstream skill text (filter + label only)

## License

Apache-2.0 (code). Collected skills retain their upstream licenses; see each catalog entry.
