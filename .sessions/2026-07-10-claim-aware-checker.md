# 2026-07-10 — gen-2: claim-aware checker (duplicate + stale claim advisory)

> **Status:** `complete`

- **📊 Model:** claude-opus-4-8 · high · gen-2 kit-side checker (single scoped
  PR: enforce the ORDER 007 order-claim convention as an advisory check)

## Scope

Gen-2 queue item 7 / the #69 card idea. The ORDER 007 order-claim convention
(`control/README.md` § "Claiming an order") makes every `new` order
single-executor: a lane appends `claimed-by: <order-ids> <lane-or-session>
<ISO8601>` to the `orders:` line of its OWN heartbeat (`control/status*.md`)
and lands it on main FIRST, so two readers of the same `status: new` order
cannot both execute it. That convention was born from a realized failure
(PRs #50/#51: two lanes executed the same ORDER 005 the same day) — but it
shipped **doc-only**, enforced by nothing.

Fix: a new `check_claims` checker (`src/engine/checks/check_claims.py`) that
scans every configured heartbeat file's `orders:` line for `claimed-by:`
annotations and flags two things, **advisory-only** (never exit-affecting,
the same posture as `check_owner_actions` and the staleness warning):

- `claims-duplicate` — two or more DISTINCT heartbeat files claim the SAME
  order id (the twin-execution race itself; the tiebreak is a human call, so
  the checker surfaces the collision rather than picking a winner).
- `claims-stale` — a live claim for an order already reported in some lane's
  `done=` (the executor was meant to DROP the claim when moving the id into
  `done=`), or a claim older than the convention's ~24h abandonment horizon
  (`control/README.md` § "Claims expire").

Wired into `cmd_check` next to the owner-action advisory (rides both CI lanes
— claims live on the heartbeat `orders:` line the fast lane already
validates) and into `build_bootstrap.py` MODULE_ORDER after
`check_status_current` (reuses its `heartbeat_relpaths` + path constants).
Pure stdlib (§3.2 subprocess ban), input-gated on the `control/` protocol,
fail-open on unreadable / claim-less files. No dedicated `ci.yml` step needed
— advisory checkers ride the existing `check` invocation, exactly like
`check_owner_actions` and `check_engagement`.

Touches only `src/engine/checks/` (+ its cli/build registration),
`dist/bootstrap.py` (regenerated), `tests/`, and this card. NEVER touched:
`control/inbox.md`, `control/status.md`, or anything under `bench/`.

## 💡 Session idea

The three control-band checkers now form a family — `check_status_current`
(heartbeat freshness), `check_owner_actions` (OWNER-ACTION format), and
`check_claims` (order-claims) — all advisory, all reading the same
`heartbeat_relpaths` set, all "enforce the convention that lives in the
status file, nudge don't gate." A shared "control-band advisory" harness (one
scan of the heartbeat files, N field-checkers over it) would let the next
such convention inherit the plumbing instead of re-reading the files.

## ⟲ Previous-session review

The prior card (2026-07-10 gen-2: close issue #36 README note) closed
`complete` with `check --strict` green (shipped as #88's predecessor line).
No defect inherited; this session picks up queue item 7, the claim-aware
checker the gen-2 next-boot queue explicitly lists.
