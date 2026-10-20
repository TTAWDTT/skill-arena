# Skill Arena

Collect Agent Skills from GitHub, coarse-filter them, then run **baseline vs with-skill** A/B evaluation to find skills that actually improve model performance.

## Models (v1)

| Role | Model id |
|------|----------|
| Executor (run tasks) | `gpt-5.6-luna` |
| Judge (blind A/B) | `gpt-5.6-sol` |

Calls go through **AGIHub ModelHub Responses API**:

```text
POST {MODELHUB_BASE_URL}/responses
```

Default base URL (AGIHub proxy):

```text
https://agihub.bytedance.net/api_proxy/modelhub/agent-cn-01/api/modelhub/online
```

Set credentials in `.env` (see `.env.example`). When the AGIHub gateway is reachable:

```bash
agihub-cli modelhub get_modelhub_token
agihub-cli modelhub get_modelhub_examples
agihub-cli modelhub list_modelhub_models
```

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
cp .env.example .env   # fill MODELHUB_API_KEY / MODELHUB_AK

# Stage 0 smoke (no API)
skill-arena seed
skill-arena filter
skill-arena eval-pilot --dry-run

# Stage 1 collect (needs GitHub auth: gh auth login)
skill-arena collect --also-seed
skill-arena filter

# Stage 3 pilot (needs ModelHub)
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
