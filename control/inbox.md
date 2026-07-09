# substrate-kit · inbox
> ORDERS to this Project. ONE writer: the manager. Never edit this file — report order progress
> in `control/status.md` (`orders: acked=… done=…`). Protocol: `control/README.md`.

## ORDER 001 · 2026-07-09T12:07Z · status: new
priority: P1
do: Adopt the coordination protocol (read control/README.md); confirm or correct your seeded control/status.md; then continue your roadmap — your next step is the B1 cold-start baseline benchmark firing per bench/README.md (agent-queue item 1 in docs/current-state.md; run by a session that did not author the rubric; append results to bench/results/cold-start/index.json; include the flagged CHANGELOG `[Unreleased]` heading-order fix in the same session), then cut v1.1.0. Report via control/status.md.
why: unblocked by PR #17's merge; named as the next agent-actionable step in your own docs/current-state.md.
done-when: B1 results appended + v1.1.0 cut (or blockers written to status); status reports acked=001, done=001.

## ORDER 002 · 2026-07-09T12:07Z · status: new
priority: P2
do: Ship the coordination-protocol kit band — menno420/superbot docs/planning/fleet-coordination-protocol-2026-07-09.md §2: (1) control/ scaffold in ADOPT_PLAN (inbox.md + status.md seeded skeletons, skip-if-exists); (2) generalized control/README.md.tmpl spec template; (3) check_status_current.py status-freshness checker (warn → graduates to the post-adopt gate); (4) CI paths-ignore for control/** on heavy suites. Cut a fresh release so adopters can `bootstrap upgrade`.
why: the fleet now runs this protocol via manager-seeded files (the MVP); the kit band makes it automatic for every future repo.
done-when: a kit release containing the control/ convention is cut; status reports done=002.
