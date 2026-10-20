---
name: railway-docs
description: "Busque documentação atualizada do Railway para responder perguntas com precisão. Use quando o usuário perguntar sobre recursos do Railway, como o Railway funciona, ou compartilhar uma URL docs.railway.com."
source_url: https://github.com/artubss/SKILLS-CLAUDE-CODE/blob/ac67ed85889b15fa9e784e2a93a83f8916870698/skills/skills/railway/railway-docs/SKILL.md
source_repo: artubss/SKILLS-CLAUDE-CODE
category: writing
body_hash: c94e7c1e1470b8424a1f2713abd6d1e84962c7591426d0c14807e7fde2404c36
---

# Documentação do Railway

Busque documentação atualizada do Railway para responder perguntas com precisão.

## Quando Usar

- Usuário pergunta como algo funciona no Railway (projetos, deployments, volumes, etc.)
- Usuário compartilha uma URL docs.railway.com
- Usuário precisa de informações atuais sobre recursos ou preços do Railway
- Antes de responder perguntas sobre Railway de memória - verifique a documentação primeiro

## Fontes Otimizadas para LLM

Comece aqui para informações abrangentes e atualizadas:

| Fonte              | URL                                         |
| ------------------ | ------------------------------------------- |
| **Documentação completa** | `https://docs.railway.com/api/llms-docs.md` |
| **Índice llms.txt** | `https://railway.com/llms.txt`              |
| **Templates**      | `https://railway.com/llms-templates.md`     |
| **Changelog**      | `https://railway.com/llms-changelog.md`     |
| **Blog**           | `https://blog.railway.com/llms-blog.md`     |

## Buscando Páginas Específicas

Adicione `.md` a qualquer URL docs.railway.com:

```
https://docs.railway.com/guides/projects
→ https://docs.railway.com/guides/projects.md
```

## Caminhos Comuns da Documentação

| Tópico       | URL                                              |
| ----------- | ------------------------------------------------ |
| Projetos    | `https://docs.railway.com/guides/projects.md`    |
| Deployments | `https://docs.railway.com/guides/deployments.md` |
| Volumes     | `https://docs.railway.com/guides/volumes.md`     |
| Variáveis   | `https://docs.railway.com/guides/variables.md`   |
| CLI         | `https://docs.railway.com/reference/cli-api.md`  |
| Preços      | `https://docs.railway.com/reference/pricing.md`  |
