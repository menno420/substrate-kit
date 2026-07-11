# 2026-07-11 — v1.11.0 wave close-out: adopters registry regen

> **Status:** `complete`

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

## Close-out

Shipped the declared scope exactly. `docs/adopters.md` regenerated via
`python3 dist/bootstrap.py currency` (snapshot **2026-07-11T13:34:11Z**, 10
repos scanned). **All 8 engaged adopter trees now CURRENT at v1.11.0** —
the full fleet is on the release: the wave quad (superbot-next · websites ·
gba-homebrew · venture-lab) AND the sibling worker's trio (fleet-manager ·
superbot-games · trading-strategy) all scan tree v1.11.0 + config pin
v1.11.0. Drift rows are all the expected classes, none chased: quad
heartbeat lag (superbot-next/gba-homebrew/venture-lab self-report v1.10.1 —
lane-owed), trio chronic heartbeat lag (v1.7.x), the kit's chronic
config-pin v1.0.0. Two rows are fully clean: **websites** (self-report
v1.11.0 — its wave PR bumped the heartbeat in-lane) and the kit's own
self-report (v1.11.0, the mid-close DRIFT from the release session
self-healed here as the recipe predicts). **Parser-fix verification
POSITIVE:** venture-lab's bulleted `- **kit heartbeat:** kit: v1.10.1 · …`
line now parses — self-report column reads v1.10.1 + engaged yes (under
v1.10.1's parser it read "no kit: line" and lost the engaged signal; see
#192's card finding → fixed in v1.11.0, live-verified this regen).
Verified on this branch: `python3 -m pytest tests/ -q` → **1008 passed**;
pre-flip `check --strict` sole finding was this card's own designed
born-red hold.

## 💡 Session idea

The registry's drift report now carries 6 self-report-lag rows that are all
the SAME known class (heartbeat bump owed after an upgrade wave), and each
wave regenerates them as undifferentiated ⚠️ DRIFT noise a reader must
re-classify by memory. Teach the currency verdict a third state:
`lag (self-report < tree, tree current)` rendered distinctly from true
divergence (self-report > tree, or engaged-signal loss) — the registry
already has both numbers, so the classification is free, and the drift
report could then group "heartbeat bumps owed" into one actionable line per
wave instead of six look-alike warnings. That turns the post-wave drift
report from a wall of expected noise into a checklist the heartbeat-bump
lane can consume directly.

## ⟲ Previous-session review

#192 (v1.10.1 wave regen) is the direct predecessor in this lane and its
craft carried forward cleanly: its source-side finding (venture-lab's
bulleted heartbeat defeating the parser) was routed into the very next kit
release rather than parked, and this session got to close the loop with a
live positive verification — the ideal friction→fix→verify arc across three
sessions. One improvement it surfaces: #192 verified each wave repo's tree
truth by hand (merge-ancestry + raw-fetch at exact SHAs) before trusting
the regen, while this session leaned on the scan itself plus coordinator-
supplied merge SHAs; the lane recipe should say explicitly when the manual
ancestry pass is owed (first regen after a release) vs redundant (the scan
re-fetches live trees anyway), so each wave doesn't re-decide the depth of
verification ad hoc.
