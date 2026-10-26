# Evaluation Methodology

## Models

| Role | Exact model id | Notes |
|------|----------------|-------|
| Executor | `gpt-5.6-luna` | Runs baseline and with-skill attempts |
| Judge | `gpt-5.6-sol` | Blind preference; different model family variant from executor |

IDs confirmed against local model catalogs (not date-suffixed Azure deployment names).

## API

Model gateway **Responses** API:

```http
POST {MODEL_GATEWAY_URL}/responses
Authorization: Bearer <MODEL_GATEWAY_USER_TOKEN>
Content-Type: application/json

{
  "model": "gpt-5.6-luna",
  "instructions": "<optional skill body>",
  "input": "<task prompt>"
}
```

Set `MODEL_GATEWAY_URL` (placeholder below is not a real host):

`<YOUR_MODEL_GATEWAY>`

When the gateway is reachable, set `MODEL_GATEWAY_API_KEY` or `MODEL_GATEWAY_USER_TOKEN`, and optionally `MODEL_GATEWAY_AK`.

Reference docs:

- [Azure Responses API](<INTERNAL_DOC>)
- [模型使用手册](<INTERNAL_DOC>)

## Skill loading

v1 approximates “real trigger” by prepending the skill markdown as `instructions` when the task category matches the skill category (pilot also allows fallback tasks). True host-native trigger routing is v2.

## A/B protocol

For each (skill, task):

1. Baseline: no skill, N=3
2. With-skill: skill loaded, N=3
3. Judge compares first successful texts, order swapped once
4. Win rate = fraction of non-tie judgments preferring skill

Curated threshold: average win rate **> 0.55**.
