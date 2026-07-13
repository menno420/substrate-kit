---
state: captured
origin: consumer:menno420/superbot-mineverse
shipped_pr: null
shipped_repo: null
merged_date: null
outcome: open
---

# Heartbeat currency: document the coordinator delegated-tally pattern (2026-07-13)

> **Status:** `ideas`
>
> **State:** captured → route: quick-win (doctrine lines in the control
> README / status template + sweep guidance).
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
