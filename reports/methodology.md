# Evaluation Methodology

## Models

| Role | Exact model id | Notes |
|------|----------------|-------|
| Executor | `gpt-5.6-luna` | Runs baseline and with-skill attempts |
| Judge | `gpt-5.6-sol` | Blind preference; different model family variant from executor |

IDs confirmed against local AGIHub / Magpie model catalogs (not date-suffixed Azure deployment names).

## API

AGIHub ModelHub **Responses** API:

```http
POST {MODELHUB_BASE_URL}/responses
Authorization: Bearer <AGIHUB_USER_TOKEN>
Content-Type: application/json

{
  "model": "gpt-5.6-luna",
  "instructions": "<optional skill body>",
  "input": "<task prompt>"
}
```

Set `MODELHUB_BASE_URL` or `MODEL_GATEWAY_URL` (placeholder below is not a real host):

`<YOUR_MODEL_GATEWAY>`

Credential bootstrap (when corp network / gateway is up):

```bash
agihub-cli modelhub get_modelhub_token
agihub-cli modelhub get_modelhub_examples
agihub-cli modelhub list_modelhub_models
```

Reference docs:

- [ModelHub—Azure Responses API](<INTERNAL_DOC>)
- [ModelHub 平台-模型使用手册](<INTERNAL_DOC>)

## Skill loading

v1 approximates “real trigger” by prepending the skill markdown as `instructions` when the task category matches the skill category (pilot also allows fallback tasks). True host-native trigger routing is v2.

## A/B protocol

For each (skill, task):

1. Baseline: no skill, N=3
2. With-skill: skill loaded, N=3
3. Judge compares first successful texts, order swapped once
4. Win rate = fraction of non-tie judgments preferring skill

Curated threshold: average win rate **> 0.55**.
