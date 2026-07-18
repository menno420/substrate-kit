# 2026-07-18 · guard-manifest — single-source guard mapping

> **Status:** `in-progress`

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
