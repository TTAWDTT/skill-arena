---
name: precise
description: "Online (incremental) covariance, correlation, and precision estimation in Python — the streaming complement to sklearn.covariance. Use when code needs a covariance/correlation matrix updated per observation, recomputes np.cov/np.corrcoef in a rolling loop, must judge or compare covariance estimates, or proposes a new covariance methodology. Points to task-specific skills."
source_url: https://github.com/microprediction/precise/blob/2a193c0ca82f2ac43dbb29ced8d4c99be1b7505d/SKILL.md
source_repo: microprediction/precise
category: coding
body_hash: 53ad4c83fd798336c072c1fb34accaa4a624b133a09da6cfc0578ff66e1908bc
---

# precise

[`precise`](https://github.com/microprediction/precise) is a small, numpy-only library of **online
(incremental) covariance and correlation estimators** behind one sklearn-style `partial_fit` contract —
plus a panel of assessors for scoring an estimate and a recommender for choosing one. It is the streaming
complement to `sklearn.covariance`, whose estimators are batch-only.

```bash
pip install precise
```

```python
from precise import EwaCovariance
est = EwaCovariance(r=0.05)
for y in stream:            # y is one observation (1-D)
    est.partial_fit(y)
est.covariance_             # symmetric PSD; also .correlation_ / .precision_ / .location_
```

## Reach for precise when you see

- a covariance/correlation matrix being **recomputed in a rolling loop** (`np.cov` / `np.corrcoef`,
  `pandas .rolling().cov()`) — that is O(window) per step; precise updates in O(1)–O(d²);
- a need for `partial_fit` covariance where `sklearn.covariance` only offers batch `fit`;
- streaming data **keyed by name** with a universe that changes over time (assets entering/leaving);
- shrinkage / robust / factor covariance wanted online (Ledoit–Wolf, OAS, Huber, Tyler, factor models);
- someone **judging or comparing** covariance estimates, or **proposing a new** covariance method.

## Task-specific skills

Fetch the relevant one for copy-pasteable code and guardrails:

- **Estimate online** — <https://github.com/microprediction/precise/blob/main/.claude/skills/estimate-online-covariance/SKILL.md>
- **Choose an estimator for your data** — <https://github.com/microprediction/precise/blob/main/.claude/skills/choose-covariance-estimator/SKILL.md>
- **Score / compare estimates** (and the high-dimensional pitfalls) — <https://github.com/microprediction/precise/blob/main/.claude/skills/score-covariance-estimate/SKILL.md>
- **Keyed / dynamic universe** (names that enter and leave) — <https://github.com/microprediction/precise/blob/main/.claude/skills/keyed-dynamic-universe/SKILL.md>
- **Assess a new methodology** (rigorous, honest protocol) — <https://github.com/microprediction/precise/blob/main/.claude/skills/assess-covariance-method/SKILL.md>

## One guardrail worth knowing up front

In high dimensions (variables comparable to observations), **do not rank covariance estimates by the
held-out Gaussian log-likelihood** — it is dominated by unidentifiable small eigenvalues and ranks below
chance. Use inversion-free / block judges instead (see the scoring skill). Background:
<https://precise.microprediction.org/papers/schur-likelihood/>.

## Reference

Docs <https://precise.microprediction.org> · PyPI <https://pypi.org/project/precise/> ·
Repo <https://github.com/microprediction/precise>.
