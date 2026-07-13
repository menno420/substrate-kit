---
state: captured
origin: consumer:menno420/superbot-mineverse
shipped_pr: null
shipped_repo: null
merged_date: null
outcome: open
---

# Session gate: fix the born-red fail-open on PR-added cards (flip-race) (2026-07-13)

> **Status:** `ideas`
>
> **State:** captured → route: structured fix (gate logic in the engine,
> engine change → dist byte-pin).
> **Origin:** consumer — surfaced live on the 2026-07-12→13 night run at
> superbot-mineverse: PR #50 had to land stranded close-out flips for PRs
> #48/#49, root-caused in PR #52; finding preserved at mineverse
> `docs/findings/substrate-gate-born-red-fail-open-2026-07-12.md`, fix ask
> routed to this kit via mineverse control/outbox.md. Cross-cited by the
> night-run report `docs/reports/2026-07-13-night-run-adopter-outcomes.md`
> §c.

## The gap

The born-red session gate can fail open in a flip race on PR-added cards:
a card's flip can merge without the gate holding, leaving stranded
in-progress cards that a later PR must sweep. The mineverse finding file
carries the reproduction; the fix belongs in the kit's gate selection
logic so every adopter inherits it.

## Size / risk

Contained gate-logic change + regression test pinning the race; reversible;
engine change → dist byte-pin in the same PR.
