# 2026-07-11 — v1.12.0 wave close-out: adopters registry regen

> **Status:** `in-progress`

- **📊 Model:** fable-5 · medium · docs-only

## Scope (what is about to happen)

Kit-seat close-out of the v1.12.0 distribution wave: regenerate
`docs/adopters.md` via `python3 dist/bootstrap.py currency` after the four
wave repos landed v1.12.0 (superbot-next #198 @ e81bc9e · websites #146 @
31cfd9f · gba-homebrew #49 @ 399bb01 · venture-lab #42 @ 881445c). The
parallel trio (fleet-manager · superbot-games · trading-strategy) is a
SIBLING worker's lane — their rows are recorded as-of snapshot time;
still-v1.11.0 / mid-flight there is expected, not chased. Expected ⚠️ DRIFT
rows for the quad minus websites (tree v1.12.0, self-report lags — heartbeat
bump is lane-owed, deliberate; websites bumped in-lane on #129 but NOT on
#146, so it lags this wave too) and the kit's chronic config-pin v1.0.0 row
— all truthful output, committed as generated, never hand-edited. Tree truth
for every row is re-verified against each adopter's origin/main via the
local clones (`git fetch` + `git show origin/main:bootstrap.py`), per the
#192-style manual ancestry pass owed on the first regen after a release.
Files: `docs/adopters.md` (regen only) and this card. NO engine/dist/src
changes; NEVER `control/inbox.md` or `bench/`. Touching ONLY this card in
`.sessions/`. No claim file (registry-regen precedent #142/#161/#174/#192/#207).
