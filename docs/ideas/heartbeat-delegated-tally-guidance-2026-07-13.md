---
state: promoted
origin: consumer:menno420/superbot-mineverse
shipped_pr: 395
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-15
outcome: shipped
---

# Heartbeat currency: document the coordinator delegated-tally pattern (2026-07-13)

> **Status:** `ideas`
>
> **State:** shipped — kit PR #395 (2026-07-15, anticipated in-PR date):
> "Delegated tally" doctrine section in `control-README.md.tmpl` + the kit's
> own `control/README.md` (marker line + member-repo pointer convention +
> sweep rule), pointer sentence in `control-status.md.tmpl` seed notes.
> **Origin:** consumer — on the 2026-07-12→13 night run, several SHIPPED
> seats carried stale own-heartbeats (games 10:16Z, idle 10:17Z, trading
> 21:02Z vs 04:29Z activity, idea-engine ~5h lag) because coordinator seats
> wrote the authoritative tallies instead: mineverse wrote the whole
> SuperBot World tally ("COORDINATOR-DELEGATED heartbeat write — the
> coordinator seat authorized this status overwrite"). A sweep reading seat
> heartbeats alone would misclassify shipping seats as stalled. Cross-cited
> by `docs/reports/2026-07-13-night-run-adopter-outcomes.md` §f.

## The gap

The kit's status.md doctrine assumes one seat = one heartbeat. Multi-repo
seats (Q-0264 merged seats, coordinator lanes) legitimately delegate the
tally to the coordinator's status file, leaving member-repo heartbeats
stale by design. Two deltas: (1) a named convention for the delegated
write (the mineverse "COORDINATOR-DELEGATED heartbeat write" line, plus a
pointer in the member repo's status to where its live tally lives); (2)
sweep guidance — classify by PR record + coordinator status, never by
seat-heartbeat staleness alone.

## Size / risk

Docs/template-only; reversible; no gate changes.
