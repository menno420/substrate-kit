# Session · 2026-07-18 · fastlane-prefix-symmetry

> **Status:** `in-progress`

Intent: B-3 — pin the fast-lane branch-prefix set so the auto-merge-enabler,
the claims-only fast-lane guard, and the engine defaults can't silently drift
out of sync. A new seat prefix added to one surface but not another reopens a
card-less merge hole (enabler arms a prefix the guard doesn't card) or the
kit#293 green-and-unarmed stall (guard cards a prefix the enabler never arms).

- **📊 Model:** Opus 4.8 · high · kit-engine meta-test + guard registry
- ⚑ Self-initiated: none — B-3 is a groomed-baton slice (docs/planning/2026-07-19-grounded-skills-window-run.md) under the ORDER 048 standing grant. The lint DESIGN is decide-and-flag: registry-in-guards.py + test-only meta-test (no check --strict wiring, matching test_guard_surface_census.py); surfaces asserted = enabler workflow, ci.yml guard carded-case, adopt.DEFAULT_AUTOMERGE_BRANCH_PATTERNS, claim.BRANCH_PREFIX, adopter-enabler generator; deliberately OUT of scope = the label-keyed disarm workflow and the prose control/claims/README.md (neither holds a machine-checkable prefix set). Flagged for review.

About to: add `FASTLANE_PREFIX_REGISTRY` (+ kinds, floor, accessors) to
`src/engine/guards.py` and a stdlib-only meta-test
`tests/test_fastlane_prefix_symmetry.py` asserting all live surfaces agree
with the registry both directions; rebuild `dist/bootstrap.py`.
