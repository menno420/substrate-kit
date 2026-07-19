# R7 — append-log ⇄ Walls-correction disagreement lint

> **Status:** `in-progress`

**Session:** 2026-07-19 · Self Improvement work-loop · substrate-kit
**Baton:** R7 (append-log ⇄ Walls-correction disagreement advisory lint) from docs/planning/2026-07-19-night-run-idea-groom.md

**About to do:** add `src/engine/checks/check_wall_ledger_agreement.py` — an
advisory (warn-only, never exit-affecting) lint that fires when a `## Walls`
correction and the newest same-capability `## Append log` entry in
`docs/CAPABILITIES.md` disagree on a capability's status; wire it on the
`posture="advisory"` seam in `cli.py`, add it to `MODULE_ORDER`, rebuild dist,
and add a test — a straight structural sibling of R5's `check_stale_walls`.

- **📊 Model:** [[fill: model · effort · task-class]]
- **⚑ Self-initiated:** [[fill: baton vs self-initiated]]

## What shipped (PR #TBD)

[[fill: what shipped summary + file list + evidence]]

## 💡 Session idea

[[fill: one genuine new idea, deduped against groom doc + docs/ideas/]]

## ⟲ Previous-session review

[[fill: one remark on R6 + one concrete system/workflow improvement]]
