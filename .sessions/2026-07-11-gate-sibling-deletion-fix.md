# 2026-07-11 — gate fixes: grade modified siblings + red on card deletions (disposition of #226)

> **Status:** `in-progress`

- **📊 Model:** fable-5 · high · engine gate fix (one scoped PR)

## Scope (what is about to happen)

Coordinator-dispatched worker slice (claim
`control/claims/claude-gate-sibling-deletion-fix.md`, main @ b441b22).
Disposition of the external gate-generation review, PR #226: two verified-real
findings fixed, one refuted.

1. **G-1 (real)** — in the generated adopter gate (`live_ci_workflow()`,
   `src/engine/adopt.py`), sibling cards MODIFIED by a diff that also adds
   card(s) are advisory-only, so a PR adding one good card can silently break
   a sibling (flip it in-progress, strip markers) and still merge. Fix: grade
   modified siblings through the SAME `--require-session-log` locked door the
   modified-only branch uses — strictly tighter, cannot reintroduce the
   tail-1 shadowing #187 fixed. Supersedes #187's advisory-sibling design
   (decide-and-flag).
2. **G-2 (real)** — both the generated gate and the kit's own dogfood gate
   (`.github/workflows/ci.yml`) build the card list with `--diff-filter=d`
   (excludes deletions), so a deletion-only PR falls to the no-card path and
   can merge while erasing session memory. Fix: capture `--diff-filter=D`
   deletions and hard-red the gate on both surfaces.
3. **B-1 (refuted)** — dist MODULE_ORDER completeness is already proven by
   `tests/test_bootstrap.py::test_module_order_covers_every_engine_module`
   (PR #147, 6f87900), in CI. No change.

Tests for both fixes (static + behavioral via the #187 scratch-git harness),
CHANGELOG `[Unreleased]` entries, dist regenerated (byte-pin). After merge:
comment per-finding on #226 and close it, then status heartbeat.
