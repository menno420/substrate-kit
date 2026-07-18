# Claims-only fast-lane guard — close the #451 race

> **Status:** `in-progress`

Closing the #451 claims-only fast-lane race: adding a red `kit-quality` guard
step that fails a `claude/*` work PR whose ENTIRE diff is only
`control/claims/**` (card-less fast-lane auto-merge), while leaving `claim/*`
standalone-claim PRs green.

## What this session does

- `.github/workflows/ci.yml`: new `kit-quality` step beside the Inbox
  append-only gate — fast-lane only, `claude/*` heads only, red when the
  whole diff is `control/claims/**`.
- `tests/test_ci_control_lane.py`: a textual pin for the new step.
- `docs/operations/auto-merge-guards.md`: guard-stack doc row (enforcing).

## Before / after

[[fill: before/after summary — filled in final commit]]

## 📊 Model

[[fill:model line — final commit]]

## 💡 Session idea (Q-0089)

[[fill:session idea — final commit]]

## ⟲ Previous-session review (Q-0102)

[[fill:previous-session review — final commit]]
