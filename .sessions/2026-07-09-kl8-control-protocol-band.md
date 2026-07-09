# Session 2026-07-09 — band KL-8: the coordination-protocol kit band (ORDER 002)

> **Status:** `in-progress`

**Scope (about to do):** execute inbox ORDER 002 — make the `control/` fleet
coordination protocol a first-class kit capability per the canonical spec
(superbot `docs/planning/fleet-coordination-protocol-2026-07-09.md` §2):
(1) `control/` scaffold in `ADOPT_PLAN` — plant a generalized
`control/README.md` (new `control-README.md.tmpl`) + seeded-skeleton
`control/inbox.md` / `control/status.md`, skip-if-exists like every plant;
(2) the status-freshness checker (`engine/checks/check_status_current.py` —
engine-side so it ships in the dist to every adopter): missing/heartbeat-less
status gates strict RED (the born-red graduation the spec names), wall-clock
staleness warns advisory-only, and the Stop hook advises when `status.md`
wasn't overwritten this session; (3) the CI control fast lane — control-only
diffs short-circuit the heavy suite GREEN inside the required job (never
`paths-ignore`, which would leave required contexts pending and jam
auto-merge — today's heartbeat-lane lesson), in both the kit's own `ci.yml`
and the planted `substrate-gate.yml`; (4) tests for all of it, dist
regenerated + byte-pinned, CHANGELOG `[Unreleased]`, ledger KL-8 entry,
D-0007. Release v1.2.0 rides a separate follow-up PR per the #29 pattern;
the status overwrite is the deliberate LAST act of the whole order (its own
control-only PR, exercising the new lane live).

## What shipped

(close-out pending)
