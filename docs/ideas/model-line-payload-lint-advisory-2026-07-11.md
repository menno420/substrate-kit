---
state: promoted
origin: lab
shipped_pr: 352
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-14
outcome: shipped
---

# 📊 Model-line payload lint advisory (2026-07-11)

> **Status:** `ideas`
>
> **State:** captured — groomed off the `control/status.md` heartbeat at the
> archive-prep close-out (it had been carried only as a 💡 line in the
> heartbeat's next-queue since the #170 session card; the heartbeat is
> overwrite-on-every-session, so this file is its durable home) →
> **shipped** (kit PR #352, 2026-07-14: `engine.checks.check_model_line`
> advisory in `check`'s full lane + the model-line grammar moved to
> `engine.grammar`, telemetry consuming the same objects; scope grew from
> effort/task-class to also cover shape + exact-ID per the fleet reporting
> bar, and the scan is bounded to the newest-10 completed cards — the
> unbounded measure found 124/178 drifted).

## The idea

The `- **📊 Model:** <model> · <effort> · <task-class>` run-report line is
grammar-checked for shape, but its PAYLOAD values drift silently: 4 of the 5
newest complete cards at the ORDER 013 self-review carried off-PL-004
segment-2/3 values (W-10a — fixed by hand in PR #199's flip commit), and the
telemetry harvest then records the drifted values as ground truth. Add an
**advisory** lint (never exit-affecting, PL-008 posture): warn when the
effort segment is not one of the taxonomy values or the task-class segment
does not prefix-match one of the 9 PL-004 classes — the same
writer/enforcer-shared-constants pattern as `grammar.py` (EAP §6.8), so the
checker and the card-authoring docs cannot drift apart.

## Why it is worth having

W-10a proved the drift class recurs under session velocity, and the fix was
a manual sweep a later session had to notice; a one-line advisory at
`check` time converts that to friction→guard (Q-0194 instinct) at near-zero
cost. Telemetry quality (band KL-3 / PL-004 allocation dataset) is only as
good as the harvested line.

## Route

Quick-win lane: one advisory check in the session-log checker + shared
constants + tests; no gate semantics change (advisory only).
