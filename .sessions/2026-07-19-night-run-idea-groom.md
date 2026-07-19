# Session — night-run idea groom + heartbeat refresh

> **Status:** `complete`

📊 Model: Opus 4.8 · high effort · planning (groom sweep) + heartbeat refresh
🌿 Branch: `claude/night-run-idea-groom`
📅 2026-07-19

## Scope
Swept the night run's ~25 session-card `💡` ideas + docs/ideas/, deduped against what
shipped (#455–#486), classified + ranked into a groom planning doc, retargeted the
`control/status.md` baton, and refreshed the seat heartbeat wholesale.

## What shipped
- `docs/planning/2026-07-19-night-run-idea-groom.md` — 12 buildable-now ideas (R1–R12),
  1 needs-planning, 2 dead/dup, owner-gated/cross-repo noted; night cards + docs/ideas/
  swept and deduped against #455–#486.
- `control/status.md` refreshed wholesale: night run #455–#486 merged; backlog REFILLED
  (was falsely "DRY"); baton retargeted at R1 (cut_release dist-order fix) + R2
  (`/scope-backlog-item` skill).
- `docs/planning/README.md` index updated (reachability).

## 💡 Session idea (genuine, deduped)
**Un-groomed-idea counter — never assert "backlog DRY" while N `💡` card lines sit
ungroomed.** The night chain left `control/status.md` claiming the buildable-now backlog
was DRY while ~14 unbuilt buildable ideas accumulated on the night's session cards —
because the baton/groom sweep reads only the recipe planning doc, not the `💡` lines on
`.sessions/*.md`. A cheap advisory (kit-quality or `check`) that counts `💡 …` lines on
session cards dated after the newest `docs/planning/*groom*.md` and flags when the count
exceeds a small threshold would make "backlog DRY" mechanically impossible while
ungroomed ideas exist. Not in the tree (grepped `.sessions/` + `docs/`).

## ⟲ Previous-session review (#486 — outbox routing to fm)
Did well: routed the folded-gate host ports + readiness cell to the fleet-manager via the
outbox rather than reaching into adopter repos — correct Q-0261.3 cross-repo discipline.
Missed: #486 (and the whole night chain) left `control/status.md` asserting "buildable-now
kit backlog DRY" while ~14 buildable `💡` ideas piled up ungroomed on the night's cards —
the DRY claim was a sweep gap, not a true empty. System improvement: the 💡 above
(un-groomed-idea counter) closes exactly this gap so the baton can't run dry silently again.
