# 2026-07-18 · guard-surface-census — pin the SET of enforcing guard surfaces

> **Status:** `complete`

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
Added the FOURTH-surface guard: a workflow-job **census** that pins the SET of
enforcing guard surfaces, not just each surface's steps. The three surfaces were
each parity-pinned at step/sub-check granularity, but a new gating **workflow
job** (the concrete "fourth surface ships unpinned" vector) could appear with no
parity assertion. The census forces every job across all workflow files to be a
parity-pinned gate, a temporary legacy alias, or non-enforcing automation.

- `src/engine/guards.py` — new `WORKFLOW_JOB_CENSUS` (6 jobs, read from ground
  truth across all 4 `.github/workflows/*.yml` files): `ci.yml::kit-quality`
  (GATE_PINNED — parity-pinned by REGISTRY + MIRRORS + STRICT_SUBCHECKS) ·
  `ci.yml::legacy-alias-test` / `legacy-alias-smoke` (ALIAS — delete after P10) ·
  `auto-merge-enabler.yml::enable-auto-merge` / `auto-merge-disarm.yml::disarm` /
  `release.yml::release` (AUTOMATION — never reds a PR). Plus `CENSUS_*` kind
  constants, `CENSUS_KINDS`, `PINNING_MECHANISMS` (the three registries
  enumerated), `EXPECTED_CENSUS_GATES=1` floor, and 4 accessors — matching the
  house REGISTRY / STRICT_SUBCHECKS style.
- `tests/test_guard_surface_census.py` — 8 tests, stdlib-only workflow parsing
  (no yaml, no subprocess), mirroring `test_guard_parity.py`: bidirectional
  set-equality between the live `jobs:` keys and the census, per-file job floor,
  gate-pin resolution, out-of-scope reason quality, known-kinds, gate floor,
  pinning-mechanism completeness, copy-accessor.
- `dist/bootstrap.py` — rebuilt via `src/build_bootstrap.py`; byte-clean on a
  fresh double-build (byte-pin gate clean).
- `.sessions/2026-07-18-guard-manifest.md` — conformed its two PL-004 model-line
  advisories (`effort high`→`high`; `kit engine refactor`→`mechanical refactor`).

Verify: `python3 -m pytest tests/ -q` → 1776 passed, 1 skipped; census+parity
15/15; `python3 dist/bootstrap.py check --strict` red only on this card's
born-red hold (no other findings); dist byte-clean on fresh rebuild.

📊 Model: Opus 4.8 · high · test writing
💡 Session idea: extend the census to the SECOND fourth-surface vector — repo git-hooks. The original B-1 idea named "a new git-hook, a new workflow job" as the two ways a fourth enforcing surface ships; this wake censused workflow jobs (the concrete gating vector) but a `.pre-commit-config.yaml` hook or a `.githooks/` script is an un-censused enforcing surface too. A `HOOK_CENSUS` + meta-test enumerating any repo-level hooks and classifying each (enforcing-and-pinned / advisory / dev-convenience) would close the remaining named vector. Dedup-checked: no `git-hook`/`pre-commit` census idea exists under docs/ideas/ (grepped git|precommit|pre-commit → none); the nearest, `guard-parity-kit-vs-adopter-2026-07-18.md`, is the workflow-parity thread this builds beside, not a dup.
⟲ Previous-session review: PR #469 (grounded-skills window plan + backlog groom) — genuine credit: its Part-B groom produced the B-1/B-2/B-3 slices that made THIS wake fully turnkey and self-authorizing (the executed baton came straight from it, no re-planning needed — the groom did its job). What it could improve: it labelled B-1 as "guard-surface census meta-test" without naming WHICH surface-addition vector to census (workflow jobs? git-hooks? both?), so this wake had to pick the vector under decide-and-flag. System improvement surfaced: a groom slice that spawns implementation should name the concrete mechanism/vector — or explicitly flag "executing wake chooses the vector" — so scope isn't silently re-derived at build time; a one-line "vector:" field on each Part-B slice would carry it.
⚑ Self-initiated: the census DESIGN is decide-and-flag adaptation of the B-1 baton concept to ground truth — I chose the workflow-job vector (the concrete gating "fourth surface" path), the three `CENSUS_*` kinds, the `PINNING_MECHANISMS` enumeration + its completeness test, and the `EXPECTED_CENSUS_GATES=1` shrinkage floor. All contained, reversible, test-only; flagged here for review.
