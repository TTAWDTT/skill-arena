---
name: ouros-security-audit
description: "Coordinate an authorized security audit of Ouros repositories and QA/local services. Use when the user asks for a broad security review, red-team-style assessment, attack-surface audit, pre-release security pass, or autonomous security campaign across multiple Ouros components."
source_url: https://github.com/Ouros-App/ouros-skills/blob/75ea1555e966ba2728fff328cc215472002932e5/skills/ouros-security-audit/SKILL.md
source_repo: Ouros-App/ouros-skills
category: review
body_hash: 336a6e6644e27531b1435e34d8f8f645e3f36a3cc8ba34968dcd1419cf65d56b
---

# Ouros Security Audit

Act as the **security lead**, not as an unrestricted attacker.

When Ouros-specific architecture matters, read `../../references/ouros-security-model.md`.

## Inputs to establish

Use available repository/config context to resolve these without repeatedly asking the operator:

- repositories/components in scope;
- allowed runtime environments;
- available test identities and fixtures;
- whether runtime mutation is permitted;
- where findings should be written.

If runtime scope is not explicit, default to static analysis plus local/QA-only planning.

## Workflow

### 1. Build the attack-surface map

Group discovered surfaces into identity/authentication, authorization/object ownership, APIs/business logic, AI/MCP/tools, data stores, secrets/configuration, CI/CD/supply chain, and deployment/observability.

Record only concrete surfaces found in code/config. Do not invent endpoints.

### 2. Prioritize hypotheses

Prefer tests that could demonstrate authentication/authorization bypass, cross-user or cross-tenant access, tool/MCP privilege expansion, sensitive-data exposure, secret exposure, or unsafe business-logic mutation.

Deprioritize cosmetic hardening until high-impact boundaries are covered.

### 3. Delegate by test type

- Runtime hypothesis -> load `../safe-runtime-testing/SKILL.md`.
- MIDAS/MCP/agent hypothesis -> load `../ouros-ai-security/SKILL.md`.
- Any candidate finding -> hand to `../finding-verifier/SKILL.md` before calling it confirmed.

### 4. Maintain finding states

Use exactly: `hypothesis`, `testing`, `candidate`, `confirmed`, `rejected`, `blocked`.

Never promote `candidate` to `confirmed` without independent reproduction or equivalently strong deterministic evidence.

### 5. Output

Maintain a compact campaign table with: `surface | hypothesis | state | severity-if-confirmed | evidence-ref | owner/next-step`.

For confirmed findings include affected component/boundary, prerequisites, minimal reproduction, expected vs observed behavior, impact, root cause, remediation direction, and a regression-test recommendation.

## Hard safety boundaries

Do not target production by default, third-party infrastructure, perform destructive tests, persistence, credential harvesting, load/flood testing, modify pre-existing business data for convenience, or tamper with audit evidence.

Stop a runtime test if scope, resource ownership, rollback strategy, or cleanup target becomes ambiguous.
