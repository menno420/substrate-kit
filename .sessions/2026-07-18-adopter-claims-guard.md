# Session · 2026-07-18 · adopter-claims-guard

> **Status:** `in-progress`

Intent: propagate the claims-only fast-lane guard from the kit's own CI
(`.github/workflows/ci.yml`) into the GENERATED adopter CI produced by
`src/engine/adopt.py` `live_ci_workflow()` (the `substrate-gate` workflow
adopters run), so adopter repos get the same #451 fast-lane-race protection.

- **📊 Model:** [[fill: model]]
- ⚑ Self-initiated: no — owner-directed slice.

About to: mirror the ci.yml "Claims-only fast-lane guard" step into
`live_ci_workflow()` (between the inbox append-only gate and setup-python,
pure workflow bash — the engine never shells out, §3.2), rebuild
`dist/bootstrap.py` via `src/build_bootstrap.py`, pin the new step in
`tests/test_adopt.py` (+ retighten the inbox-gate test bound), and add an
adopter-propagation note to `docs/operations/auto-merge-guards.md` row 7.

## What shipped

[[fill: what shipped]]

## 💡 Session idea

[[fill: session idea]]

## ⟲ Previous-session review

[[fill: previous-session review]]
