# 2026-07-11 — v1.10.1 wave close-out: adopters registry regen

> **Status:** `in-progress`

- **📊 Model:** fable-5 · medium · docs-only — wave close-out (adopters registry regen)

## Scope (what is about to happen)

Kit-seat close-out of the v1.10.1 distribution wave: regenerate
`docs/adopters.md` via `python3 dist/bootstrap.py currency` after the four
wave repos landed v1.10.1 (superbot-next #166 @ 5c064dd · websites #113 @
6663e6c4 · gba-homebrew #38 @ 78bacbc · venture-lab #34 @ 4c32ca3 — each
already verified an ancestor of its origin/main, with tree truth
`KIT_VERSION = "1.10.1"` + config pin 1.10.1 raw-fetched at that exact HEAD
SHA, never heartbeats). The parallel trio (fleet-manager · superbot-games ·
trading-strategy) is a SIBLING worker's lane — their rows are recorded
as-of snapshot time; still-v1.10.0 / mid-flight there is expected, not
chased. The kit's own row may snapshot as self-report DRIFT mid-close (the
known regen-recipe quirk — self-heals next regen; not chased). Files:
`docs/adopters.md` (regen only, never hand-edited),
`control/claims/wave-v1.10.1-adopters-regen.md` (deleted in the flip
commit), and this card. NO engine/dist/src changes; NEVER `control/inbox.md`
or `bench/`. Touching ONLY this card in `.sessions/`.

## Close-out

(pending — flipped complete as the deliberate last step)
