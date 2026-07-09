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

## ORDER 003 · 2026-07-09T14:15Z · status: new
priority: P2
do: Substrate-coordinator visibility band (rider to ORDER 002, ship together or right after): (1) add a `kit:` line to the kit's control/status.md template — `kit: v<X.Y.Z> · check: green|red · engaged: yes|no` — so every adopter self-reports kit state in its heartbeat; (2) create docs/adopters.md in this repo (sole writer: kit-lab) — registry of adopted repos (repo · kit_version · engaged · last-seen), seeded from what you know (superbot-next, websites, trading-strategy, + coming game repos); (3) publish a short "adopter upgrade checklist" section in each release's notes (run upgrade → check --strict green → engagement green → update status kit-line). Context: manager research 2026-07-09 — the kit has the improvement engine but no adopter visibility; this closes it with zero new access, KF-2-clean (you never write adopter repos; the manager relays orders).
why: kit-lab is the fleet's substrate coordinator; it needs to see who runs what version without write access.
done-when: next kit release ships all three; docs/adopters.md exists; status reports done=003.

## ORDER 004 · 2026-07-09T15:30Z · status: new
priority: P2
do: Rider to ORDER 003 (adopter visibility band), relayed from a real adopter finding: superbot-games is a SHARED repo with per-lane heartbeats (control/status-mining.md + control/status-exploration.md per its control/README.md multi-Project extension), but the kit's check_status_current hardcodes control/status.md — misfiring on multi-Project repos. Make the status-file path(s) configurable (e.g. substrate.config.json key listing heartbeat files, default control/status.md), and include the per-lane pattern in the control/README.md.tmpl. Ship with the ORDER 003 band or next release.
why: multi-Project cohabitation is now a live pattern; the kit should support it first-class.
done-when: configurable heartbeat paths released; adopters.md notes superbot-games as the two-lane adopter; status acks 004.
