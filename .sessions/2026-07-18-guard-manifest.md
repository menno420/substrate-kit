# 2026-07-18 · guard-manifest — single-source guard mapping

> **Status:** `complete`

## Scope
Replace the two-place hand-maintained kit↔adopter guard mapping with a single
declarative guard manifest (`src/engine/guards.py`) that both the adopter-CI
generator (`src/engine/adopt.py` `live_ci_workflow()`) and the guard-parity
meta-test (`tests/test_guard_parity.py`) read. Adding or renaming a guard
becomes a one-place edit; the parity test stops carrying its own hand-kept
REGISTRY.

## What I'm about to do
- Add `src/engine/guards.py` — the canonical manifest (kit-quality step →
  SETUP / MIRRORS(adopter step) / KIT_ONLY(reason)).
- Point `adopt.live_ci_workflow()` at the manifest's adopter step names.
- Point `tests/test_guard_parity.py` at the manifest instead of its inline
  REGISTRY; keep its three checks equivalent-or-stronger.
- Rebuild `dist/bootstrap.py` via `src/build_bootstrap.py`; verify pytest +
  `python3 dist/bootstrap.py check --strict` + sha256 reproducibility.

## Outcome — shipped
Single-sourced the kit↔adopter guard mapping into `src/engine/guards.py`, read by both `adopt.live_ci_workflow()` (adopter-CI generator) and `tests/test_guard_parity.py` (parity meta-test). The parity test no longer carries its own hand-kept `REGISTRY`; adding/renaming a guard is a one-place edit.

- `src/engine/guards.py` — new manifest: 3 SETUP / 5 MIRRORS / 10 KIT_ONLY, copied verbatim from the old inline registry; 5 adopter step-name constants.
- `adopt.live_ci_workflow()` — emits the 5 adopter `substrate-gate` step names from the manifest; YAML output byte-identical (empty diff, both toggles).
- `tests/test_guard_parity.py` — imports the manifest; 4 checks preserved, the mirror check now round-trips against the generator's manifest-sourced names.
- `dist/bootstrap.py` — rebuilt via `src/build_bootstrap.py` (not hand-edited); reproducible (double-build sha256 identical), byte-pin gate clean.

Verify: `python3 -m pytest tests/ -q` → 1765 passed, 1 skipped; guard-parity 4/4 green; `python3 dist/bootstrap.py check --strict` clean except this card's born-red hold. Commit `d5ac29f`.

📊 Model: Opus 4.8 (family) · effort high · task-class: kit engine refactor
💡 Session idea: drive ci.yml's kit-quality step NAMES from the same manifest (a `render`/`--emit-kit-ci` codegen), closing the last hand-kept guard copy so the parity test's "all classified" check becomes generation-verified rather than drift-detected. Dedup-checked against docs/ideas/ and the status baton — grep docs/ideas/ for "manifest"/"ci"/"guard" first and, if a near-duplicate exists, note it instead of adding.
⟲ Previous-session review — PR #459 (guard-parity meta-test): landed the verification harness that made THIS refactor safe (net positive — without its 4 checks this single-sourcing could not be verified byte-safe). What it could have done better: it added a third hand-copy of the guard list (its own inline REGISTRY) to police drift between the other two — detecting drift by re-typing the very constants it guards. System improvement surfaced: a meta-test that re-types production constants is an anti-pattern; prefer importing the source of truth (which this PR now provides). Worth a short convention note in the kit's testing guidance.
⚑ Self-initiated: none beyond the baton task — the `guards.py` public API (accessors + the 5 adopter step-name constants) and its `MODULE_ORDER` placement were my design calls under decide-and-flag; flagged here for review.
