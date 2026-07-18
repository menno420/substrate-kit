# 2026-07-18 · guard-surface-census — pin the SET of enforcing guard surfaces

> **Status:** `in-progress`

## Scope
B-1 (from the groomed baton): a guard-surface **census** meta-test. The three
enforcing guard surfaces are each parity-pinned at step/sub-check granularity
(ci.yml `kit-quality` steps ⇄ `REGISTRY`; adopter `substrate-gate` steps ⇄
`MIRRORS`; `bootstrap check --strict` sub-checks ⇄ `STRICT_SUBCHECKS`), but
nothing pins the SET OF SURFACES itself — a FOURTH enforcing surface, concretely
a new **workflow job**, could ship with no parity assertion. The census closes
that vector: every job across all `.github/workflows/*.yml` must be classified
as a pinned gate, a temporary legacy alias, or non-enforcing automation.

## What I'm about to do
- Add `WORKFLOW_JOB_CENSUS` + kind constants + accessors to
  `src/engine/guards.py`, populated from the live workflow `jobs:` keys.
- Add `tests/test_guard_surface_census.py` — bidirectional set-equality between
  discovered jobs and the census, plus reason/kind quality checks (stdlib
  parsing, matching `tests/test_guard_parity.py`'s style).
- Rebuild `dist/bootstrap.py` via `src/build_bootstrap.py`; verify pytest +
  `check --strict` + dist byte-cleanliness.
- Conform the two model-line advisories on the guard-manifest card to PL-004.

## Outcome — shipped
[[fill: outcome summary]]

📊 Model: [[fill: model line]]
💡 Session idea: [[fill: one deduped idea]]
⟲ Previous-session review: [[fill: review + system improvement]]
⚑ Self-initiated: [[fill: self-initiated flag]]
