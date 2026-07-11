# 2026-07-11 — v1.10.1 wave close-out: adopters registry regen

> **Status:** `complete`

- **📊 Model:** fable-5 · medium · docs-only

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

Shipped the declared scope exactly. `docs/adopters.md` regenerated via
`python3 dist/bootstrap.py currency` (snapshot **2026-07-11T09:49:16Z**, 10
repos scanned). **All 8 engaged adopter trees now CURRENT at v1.10.1.** The
four wave rows verified against TARGET trees, never heartbeats: cited merges
confirmed ancestors of each repo's origin/main (`git merge-base
--is-ancestor` for the moved-HEAD pair; gba-homebrew/venture-lab HEAD == the
cited merge), and `bootstrap.py` `KIT_VERSION = "1.10.1"` + config pin
1.10.1 raw-fetched at each exact HEAD SHA — superbot-next @ 6a0921c ·
websites @ 02adf7c · gba-homebrew @ 78bacbc · venture-lab @ 4c32ca3. The
parallel trio's TREES were already v1.10.1 at snapshot (their upgrade PRs
had landed); only their self-reports lag (superbot-games mining/exploration
v1.7.1 · trading-strategy v1.7.1 · fleet-manager v1.7.0) → the 4 DRIFT rows
are the known lane-owed heartbeat lag plus the kit's chronic config-pin
v1.0.0 tree-internal drift — all expected, none chased. The kit's own
mid-close self-report DRIFT from #190 SELF-HEALED here exactly as the recipe
predicts (status.md reads v1.10.1). Claim
`control/claims/wave-v1.10.1-adopters-regen.md` (#191 @ 8bcc7d5) deleted in
this flip commit. Verified on this branch: `python3.10 -m pytest tests/ -q`
→ **989 passed**; `check_idea_index` OK; `check --strict` sole pre-flip
finding was this card's own designed born-red hold.

**Finding (source-side, not chased):** venture-lab's heartbeat DOES carry a
v1.10.1 kit line, but embedded as `- **kit heartbeat:** kit: v1.10.1 · …`
(control/status.md line 14 @ 4c32ca3) — the currency parser expects the
line to start at `kit:`, so the registry reads `no ` + backtick-kit-line and
loses the engaged=yes signal. Reconcile at the source (venture-lab reformats
its line) per the registry's own protocol; row verdict is unaffected
(tree-truth `current`).

## 💡 Session idea

The venture-lab miss above is a parser/emitter contract gap: adopters write
the `kit:` heartbeat line free-hand and the kit's currency scan silently
degrades any formatting variant to `no kit-line` (this wave: a bolded
bullet prefix). Ship the heartbeat line the same way the claim grammar was
shipped — kit-owned regex constants in `src/engine/grammar.py` consumed by
BOTH the emitter (adopt/upgrade plant + the status checker that nags each
adopter) and the currency parser, with a leniency rule (match `kit:`
anywhere after leading bullet/emphasis) plus a `heartbeat-format` advisory
in the ADOPTER's own `check` so the drift is flagged where it can be fixed,
not just observed in the registry.

## ⟲ Previous-session review

The #190 release close-out executed the release recipe cleanly (regen +
heartbeat + claim clear in one squash, card discipline intact) — and its
predicted mid-close self-report DRIFT on the kit's own row indeed
self-healed in this regen, confirming the recipe's model. One improvement
it surfaces: #190's regen ran ~6 minutes after the wave PRs started landing,
so its four "stale v1.10.0" rows were obsolete within the hour and a second
full regen session (this one) was always going to be needed. The release
recipe could name this explicitly: the release-close regen is the BEFORE
snapshot, and the wave close-out regen is the AFTER — schedule them as one
paired lane instead of rediscovering the sequencing each release.
