# S5 — shared require_full_history() helper

> **Status:** `in-progress`

**Session:** 2026-07-19 · Self Improvement work-loop · substrate-kit
**Baton:** wave-2 groom rank S5 (docs/planning/2026-07-19-night-run-idea-groom-wave2.md) — extract a shared `require_full_history()` helper in the `_git_truth` seam and route the duplicated shallow-clone "history truncated → refuse/degrade" logic through it. Provenance: fm ORDER 048 standing grant + coordinator dispatch (S4 shipped #518; baton advanced to S5).

## What I'm about to do
Add `require_full_history(run) -> HistoryVerdict` to `scripts/_git_truth.py` (the single home of the shallow→degrade decision, built on the existing `is_shallow` primitive), and reimplement `scripts/measure_grounded_skills.py._is_shallow` as a thin adapter over it — deleting the duplicate `rev-parse --is-shallow-repository` subprocess. Behavior-preserving; tests for the three verdicts (FULL / SHALLOW / UNKNOWN). Born-red until this card flips complete.

<!-- exit-gate placeholders resolved at flip -->
- **📊 Model:** opus-4.8 · medium · mechanical refactor
