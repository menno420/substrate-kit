---
state: promoted
origin: consumer:menno420/venture-lab
shipped_pr: 187
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-11
outcome: shipped
---

# Gate card picker `tail -1` lets a multi-card diff shadow the born-red hold (2026-07-11)

> **Status:** `ideas`
>
> **State:** captured. **Origin:** consumer — venture-lab, live-verified
> during the v1.10.0 distribution wave (first exercise of the regenerated
> gate). **Priority: HIGH — target v1.10.1.** It partially reopens the
> superbot-games #40 card-only loophole the v1.10.0 release closed.

## The finding (first-exercise evidence, venture-lab #33)

The generated gate (and the kit's own `ci.yml` session-gate step) derives
the card to grade as:

```
card="$(git diff --name-only --diff-filter=d "$range" -- '.sessions/*.md' ':!.sessions/README.md' | tail -1)"
```

`tail -1` means a MULTI-CARD diff grades only the **last card in the
diff's (path-sorted) order** — every other card in the diff, including a
PR-ADDED in-progress card, never reaches the gate:

- venture-lab head `798a3d0` (added in-progress card + a provenance-marked
  grammar backfill on the sibling `session-001.md`) went **GREEN under the
  NEW v1.10.0 gate** — run 29144734514, log line
  `session gate card: .sessions/session-001.md` (the modified, compliant,
  alphabetically-last sibling was graded; the added in-progress card was
  shadowed).
- Single-card head `60e91f8` (same added card, backfill reverted)
  correctly **HELD** — run 29144777017, HOLD-by-design banner.

An accident (a mid-PR sibling-card backfill — exactly what the
superbot-next mtime-lottery lesson encourages) or an attacker needs only
to touch any later-sorting sibling card to ship an in-progress card green.
The `session-card-hold` finding itself (kit #176) is sound — the card
never reaches it.

## Why this partially reopens superbot-games #40

The v1.10.0 release closed the card-only born-red loophole by making an
ADDED in-progress card a locked-door HOLD. That fix assumed the added card
is the one graded. On a multi-card diff the picker, not the hold, decides
— so the pre-armed-auto-merge premature-merge class (#40, merged 24 s
after arming) is reachable again via any two-card diff.

## Proposed fix direction (deliberately NOT attempted in the filing PR)

Grade **EVERY card in the diff**, not the tail: loop the diff list, route
each ADDED card through the added-card/locked-door lane and each modified
card through the ordinary grammar check; **HOLD if ANY added card is
in-progress/drafted**. Surfaces to change in lockstep: the generated-gate
template, the kit's own `.github/workflows/ci.yml` session-gate step, and
`--simulate-added-card` docs/tests (regression pair: multi-card diff with
shadowing sibling → HOLD; all-complete multi-card diff → green). Adopters
inherit on next upgrade.

## Interim wave doctrine (until fixed)

Land sibling-card backfills pre-PR or in the SAME commit that flips your
own card complete — never mid-PR — and touch ONLY your own card in a
born-red PR (recorded in the v1.10.0 wave notes + team memory).
