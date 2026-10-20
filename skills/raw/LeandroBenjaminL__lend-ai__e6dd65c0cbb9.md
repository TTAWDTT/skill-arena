---
name: ci-cd-pilot
description: "Diseña y optimiza pipelines de CI/CD — GitHub Actions, GitLab CI, automatización de tests, linting, builds y deploys. Trigger: Cuando hay que automatizar tests, linting, builds o deploys, o configurar un pipeline de CI/CD."
source_url: https://github.com/LeandroBenjaminL/lend-ai/blob/66e70bfe7cb152c331df398caa42661da1a217c6/skills/ci-cd-pilot/SKILL.md
source_repo: LeandroBenjaminL/lend-ai
category: coding
body_hash: e6dd65c0cbb9b6efbc8737a54948a0cf9d7e3004291c14d21800e0da87a11dd1
---

# Skill: ci-cd-pilot

Pipelines que no se rompen los viernes a las 18.

## Trigger

- Querés que los tests corran solos en cada PR
- Necesitás automatizar el deploy a staging/prod
- Hay que configurar linting + type checking en CI
- Un pipeline existente tarda 20 minutos y hay que optimizarlo
- Vas a mergear y querés que pase por controles automáticos

## Workflow LEND

```
1. ANALIZAR
   ├── Stack: Python (ruff, pytest), Node (eslint, vitest), Go (golangci-lint)
   ├── ¿Hay tests? ¿Hay linter? ¿Hay type checker?
   ├── ¿Dónde deploya? (Railway, Vercel, AWS, Docker Hub)
   └── ¿Ambientes? (dev, staging, prod)

2. OFRECER (Menú del Senior)
   ├── A) Scout: lint + type check + build. Rápido, mínimo.
   ├── B) Guardian: lint + tests + build + security scan. No mergea si falla.
   └── C) Ironclad: todo + auto-deploy + notificaciones + matrix builds

3. ELEGIR → el usuario confirma

4. HACER
   ├── .github/workflows/main.yml o .gitlab-ci.yml
   ├── Secrets bien configurados (nunca hardcodeados)
   ├── Dependency caching (pip cache, npm cache, go mod cache)
   ├── Matrix builds si aplica (3.10, 3.11, 3.12)
   └── Documentación en inglés técnico del pipeline

5. VERIFICAR
   ├── El workflow corre sin errores
   ├── Los secrets están configurados en GitHub/GitLab
   └── El caché funciona (segundo run es más rápido)
```

## Patrones

- **Caching**: siempre cachear dependencias entre runs
- **Secrets**: usar GitHub Secrets / GitLab CI variables, nunca en el yaml
- **Fail fast**: primero lint, después tests, después build
- **Matrix**: testear contra 2-3 versiones del runtime
- **Trigger condicional**: CI en PRs y push a main; CD solo en tags o main
- **Notificaciones**: solo fallos, no saturar con éxitos

## Anti-patrones

- Hardcodear API keys o tokens en el workflow yaml
- CI que tira warning pero pasa igual (poné `--error-on-warning`)
- Deploy automático sin pasar por PR
- Un solo workflow de 500 líneas — partí en workflows reusables
- Cachear sin key — la cache se vuelve obsoleta
