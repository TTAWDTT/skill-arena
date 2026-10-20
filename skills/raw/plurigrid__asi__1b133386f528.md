---
name: gh
description: "GitHub CLI (212 man pages)."
source_url: https://github.com/plurigrid/asi/blob/293ce9f76e3abcd5ba18db284688bc0d9ac6691d/skills/gh/SKILL.md
source_repo: plurigrid/asi
category: coding
body_hash: 1b133386f528cba230c885f589c4e49846cf8abfd04a9a3e83bb14db2674759d
---

# gh

GitHub CLI (212 man pages).

## Auth

```bash
gh auth login
gh auth status
gh auth token
```

## Repo

```bash
gh repo clone owner/repo
gh repo create name --public
gh repo view --web
```

## PR

```bash
gh pr create --title "Title" --body "Body"
gh pr list --state open
gh pr checkout 123
gh pr merge --squash
```

## Issue

```bash
gh issue create
gh issue list --label bug
gh issue close 42
```

## API

```bash
gh api repos/{owner}/{repo}/issues
gh api graphql -f query='{ viewer { login } }'
```

## Actions

```bash
gh run list
gh run view 12345
gh workflow run deploy.yml
```
