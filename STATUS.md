# Overnight status (2026-10-21)

## Done

- Repo scaffold at `~/Projects/skill-arena` (dirs, schema, CLI, tasks, reports).
- Model ids locked: executor **`gpt-5.6-luna`**, judge **`gpt-5.6-sol`**.
- Gateway client uses the Responses API (see `reports/methodology.md`).
- Collected **350** unique skills (GitHub `gh api` search); coarse filter kept **300**.
- Task bank seeded (12 tasks across categories).
- Dry-run pilot pipeline green (`skill-arena eval-pilot --dry-run`) — **not real model scores**.

## Blocked / needs you when awake

1. **Corp network / model gateway** currently times out from this machine  
   (endpoint comes from `MODEL_GATEWAY_URL`).  
   Fill `.env` from `.env.example`:
   ```bash
   # set MODEL_GATEWAY_API_KEY or MODEL_GATEWAY_USER_TOKEN
   skill-arena ping-model
   skill-arena eval-pilot                  # real A/B on ~30 skills
   ```
2. Expand tasks to 10–15 per category (`tasks/`).
3. Human-spot-check ~10% of judge verdicts after real pilot.

## Commands

```bash
cd ~/Projects/skill-arena
source .venv/bin/activate
skill-arena status
python scripts/collect_gh.py    # gather more SKILL.md
skill-arena filter
skill-arena eval-pilot --dry-run
```
