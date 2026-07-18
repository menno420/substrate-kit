# Session · 2026-07-18 · guard-parity-strict

> **Status:** `in-progress`

Intent: pin the `bootstrap check --strict` sub-check surface by adding a `STRICT_SUBCHECKS` manifest to `engine/guards.py` and a set-equality parity test, so a strict sub-check (check_ledger, check_no_false_walls, etc.) can't be dropped or renamed silently.

- **📊 Model:** [[fill: model · effort · task-shape]]
- ⚑ Self-initiated: [[fill: yes/no + rationale]]

## What I'm about to do

Add a `STRICT_SUBCHECKS` manifest to `src/engine/guards.py` classifying each `bootstrap check --strict` sub-check, plus a new set-equality parity test in `tests/test_guard_parity.py` that asserts the manifest matches the actual `check_*()` calls in the live source (red in both directions), then rebuild `dist/bootstrap.py`. Mirrors the existing ci.yml-surface parity (`guards.REGISTRY` + `test_guard_parity.py`).

## 💡 Session idea

[[fill: one new genuine idea + why]]

## ⟲ Previous-session review

[[fill: one remark on the previous session + one workflow improvement]]
