# 2026-07-11 — v1.11.0 wave close-out: adopters registry regen

> **Status:** `in-progress`

- **📊 Model:** fable-5 · medium · docs-only

## Scope (what is about to happen)

Kit-seat close-out of the v1.11.0 distribution wave: regenerate
`docs/adopters.md` via `python3 dist/bootstrap.py currency` after the four
wave repos landed v1.11.0 (superbot-next #182 @ c0a5f61 · websites #129 @
00685e43 · gba-homebrew #44 @ a3104ae · venture-lab #37 @ a447f1a). The
parallel trio (fleet-manager · superbot-games · trading-strategy) is a
SIBLING worker's lane — their rows are recorded as-of snapshot time;
still-v1.10.1 / mid-flight there is expected, not chased. Expected ⚠️ DRIFT
rows for the quad (tree v1.11.0, self-report v1.10.1 — heartbeat bump is
lane-owed, deliberate) and the kit's chronic config-pin v1.0.0 row — all
truthful output, committed as generated, never hand-edited. Riding
verification: v1.11.0's currency-parser fix (bulleted `kit:` lines) should
keep venture-lab's self-report parsed as v1.10.1 instead of "no kit: line".
Files: `docs/adopters.md` (regen only) and this card. NO engine/dist/src
changes; NEVER `control/inbox.md` or `bench/`. Touching ONLY this card in
`.sessions/`. No claim file (registry-regen precedent #142/#161/#174/#192).
