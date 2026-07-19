# Session card — GSW-4 PR open->merge latency pass (GitHub-API)

> **Status:** `in-progress`
> **📊 Model:** Opus 4.8 · [[fill: effort · task-class at flip]]

## Scope
Implement GSW-4, the (optional) GitHub-API PR open->merge latency pass — the
#247 §2 method over the same grounded-skills windows measured by GSW-1..3. Baton
item GSW-4 from `docs/planning/2026-07-19-grounded-skills-window-run.md` (the
harness deliberately does not fake latency from git data, so this needs the
GitHub-API pass). Coordinator-dispatched worker lane.

## What I'm about to do
- Add from-scratch `scripts/measure_pr_latency.py` + a companion test — the
  #247 §2 GitHub-API PR open->merge latency method over the grounded-skills
  measurement windows.
- Freeze the latency data as a committed JSON artifact (auditable, reproducible).
- Add a latency section to `docs/reports/2026-07-19-grounded-skills-measurement.md`.
- Mark GSW-4 done in `docs/planning/2026-07-19-grounded-skills-window-run.md` and
  keep the reachability link (`docs/operations/README.md`) intact.

## Provenance
Coordinator dispatch; baton item GSW-4 from
`docs/planning/2026-07-19-grounded-skills-window-run.md` (on main since PR #476),
building on the GSW-1..3 grounded-skills window run.

## Shipped
[[fill: what shipped — populated by a later commit before the card flips to complete]]

## 💡 Session idea
[[fill: Q-0089 one genuine new idea + why it's worth having — at flip]]

## ⟲ Previous-session review
[[fill: Q-0102 one remark on the previous session + one concrete system improvement — at flip]]

## Docs audit
[[fill: Q-0104 ledger/reachability audit result — at flip]]
