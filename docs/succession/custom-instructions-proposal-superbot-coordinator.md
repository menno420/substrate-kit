# Custom Instructions proposal — gen-2 SuperBot coordinator (2026-07-09)

> **Status:** `owner-guidance` — the gen-1 SuperBot-rebuild COORDINATOR
> lane's rewrite of its own Custom Instructions, from lived experience at
> wind-down. Every keep/drop/add carries one line of why, evidence-anchored
> in [the project review](../retro/project-review-2026-07-09-superbot-coordinator.md)
> and [the wind-down review](../retro/wind-down-review-2026-07-09-superbot-coordinator.md).
> Suffixed `-superbot-coordinator` per the multi-lane rule.

## KEEP (proven in gen-1)

1. **Dispatch-to-children rule** (the coordinator steers, children build) —
   the 13.6h/49-PR rebuild worked precisely because the coordinator never
   held the keyboard; sequential workers with progress-log handoffs had
   zero duplicated bands.
2. **Verify-child-claims-against-GitHub** — the ledger said "~87 merged
   PRs"; the live API said 86; the habit of checking caught every drift of
   this kind before it entered a report.
3. **Band-boundary reporting** — per-band reports made "done" checkable
   and made the 20+ live-found bugs attributable; the bands without them
   are the ones the audit had to hedge on.
4. **Owner-flag ledgering (⚑)** — the consolidated flag list is the only
   reason the owner's clicks (intents, repo creation, ruling 13) were
   trackable at all; every stall in gen-1's blocked/waiting slice resolved
   through it.

## ADD (gen-1 paid for each of these)

1. **Lane-suffix rule in every broadcast order** — today's ORDER-005
   three-way race is the evidence: identical order text to multiple lanes
   with no suffix/claim clause produced a merged duplicate (#51) and a
   stranded dirty PR (#50). Every order the coordinator writes MUST name
   the target lane and the suffixed paths it may touch.
2. **The relay-worker pattern, documented as THE child-steering
   mechanism** — the coordinator has no direct child-messaging tool; a
   relay worker calling `send_message` is the sanctioned channel. Gen-1
   improvised it; gen-2 should be told it on line one so no time is lost
   probing for a direct tool that does not exist.
3. **Wind-down / succession protocol as a standing section** — gen-1 had
   to be told to wind down by ad-hoc order; the instructions should carry
   the deliverable list (next-boot doc, instruction rewrite, env spec,
   blueprint feedback, retro addendum, final heartbeat) so any session can
   execute succession without a bespoke brief.
4. **Webhook-noise triage rule** — subscribe/auto-merge/merge notices are
   never actionable; ~150 wakes in gen-1 produced zero actions. One
   instruction line ("never act on subscribe/merge notices") deletes the
   whole class.
5. **Walking-skeleton before first real dispatch** — trivial branch → PR →
   checks run → auto-merge on green, in every repo the lane writes to,
   before real work; would have pre-empted the #35 "Expected" freeze.
6. **Model + time line on every session card** — the gen-1 audit's biggest
   cannot-determine was "which model ran my children"; the two cards that
   carried Model lines were the only cheaply-verifiable ones. Blueprint §1
   already mandates this; the coordinator's instructions should restate it
   for every child brief.

## DROP / CHANGE

1. **Drop anything forcing the coordinator to hand-manage timers** —
   `send_later` binds to the arming session (no session-target param), so
   watchdog timers all routed through the coordinator as noise. Change to:
   ask the platform for a session-targetable `send_later`; until it
   exists, arm timers from the session that should receive the wake.
2. **Soften "always create PR after push" for control-file heartbeats** —
   if the repo's convention has a control fast lane (as substrate-kit's
   does; blueprint delta #9 says batch heartbeats), a full PR round per
   heartbeat overwrite is pure overhead. Change to: follow the repo's
   convention; PR by default, fast-lane heartbeats where the repo grants
   it.

## Blueprint alignment (gen2-blueprint.md was readable at wind-down)

Read live from `menno420/fleet-manager` `docs/gen2-blueprint.md`
(status `binding`, finalized 2026-07-09 late evening). Alignment:

- **Agrees** with ADD-1 (blueprint §2 delta 5: order claim/lease, citing
  the same #50/#51 incident), ADD-5 (§1 walking skeleton "in the first 20
  minutes"), ADD-6 (§1 Model+time from card #1), and CHANGE-2 (§2 delta 9:
  control fast lane + batched heartbeats).
- **Extends** the blueprint in two places it is thin: the relay-worker
  pattern (ADD-2 — the blueprint fixes the ORDER pickup loop but says
  nothing about coordinator→child steering mid-flight) and the
  webhook-noise triage rule (ADD-4 — no blueprint line covers wake noise).
- **No disagreements found.** One nuance: blueprint §2a's hourly Class-A
  wake cadence is right for order pickup, but a coordinator lane under
  webhook subscription wakes far more often than hourly — the cadence
  table should note that webhook wakes do NOT count as ritual wakes (they
  skip the inbox re-read that §2a rule 1 requires).
