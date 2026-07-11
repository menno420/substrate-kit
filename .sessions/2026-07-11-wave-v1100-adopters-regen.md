# 2026-07-11 — v1.10.0 wave close-out: adopters regen + findings intake

> **Status:** `complete`

- **📊 Model:** Claude (Fable family) · medium · docs-only — wave close-out
  (adopters registry regen + wave-findings idea intake)

## Scope (what is about to happen)

Close-out of the v1.10.0 distribution wave's kit-seat half (superbot-next
#159 @ 72db87b · websites #105 @ eb447a2 · gba-homebrew #37 @ c7592d6 ·
venture-lab #33 @ a94a8611 — all confirmed ancestors of their origin/main).
Files: `docs/adopters.md` (regenerated via `python3 dist/bootstrap.py
currency` at kit v1.10.0; every row verified against the TARGET repo's tree,
never heartbeats; the parallel trio fleet-manager / superbot-games /
trading-strategy recorded as-of snapshot time — mid-flight is expected, not
chased), `docs/ideas/` (two new idea files + README backlog entries: the
tail-1 multi-card gate-shadowing loophole found live on venture-lab #33 —
HIGH priority, partially reopens the superbot-games #40 class — and the
`_MODEL_DOCTRINE_PHRASE` emphasis-blind match nit found on websites #105),
`control/claims/wave-v1.10.0-adopters-regen.md` (deleted at close), and this
card. NO engine/dist changes — the loophole fix itself is deliberately NOT
attempted here (filed for the next kit-fixes slice). NEVER `control/inbox.md`
or anything under `bench/`. Touching ONLY this card in `.sessions/` — no
sibling-card edits (per the very tail-1 finding this PR files).

## Close-out

Shipped the declared scope exactly. **Job 1** — `docs/adopters.md`
regenerated at kit v1.10.0 (snapshot **2026-07-11T07:47:24Z**): all 8
engaged adopter trees CURRENT at v1.10.0, each row independently verified
against the target repo's HEAD tree (`git ls-remote` SHA + raw-fetch of
`bootstrap.py` `KIT_VERSION` AND `substrate.config.json` `kit_version` at
that exact SHA, never heartbeats) — superbot-next @ 0a29d37 · websites @
eb447a2 · superbot-games @ b7a6073 · trading-strategy @ 569fae8 ·
gba-homebrew @ c7592d6 · venture-lab @ a94a861 · fleet-manager @ 1afca50;
kit itself @ 59ede0a (dist header v1.10.0). The parallel trio
(fleet-manager, superbot-games, trading-strategy) had ALREADY landed
v1.10.0 by snapshot time — nothing mid-flight. Non-adopters unchanged:
superbot pin-only v1.0.0 @ 58040c6 (no vendored dist — raw fetch 404s on
bootstrap.py, config pin confirmed); pokemon-mod-lab not adopted @ ebc704e
(no substrate.config.json — 404). Self-report DRIFT rows are the known
lane-owed heartbeat lag (6 repos), plus the kit's chronic config-pin
v1.0.0 tree-internal drift; the kit's own mid-close self-report DRIFT from
regen #179 SELF-HEALED here exactly as the recipe predicts (status.md now
reads v1.10.0 → row verdict `DRIFT · current` on the pin only). **Job 2**
— two wave findings filed as `docs/ideas/` intake (fix deliberately NOT
attempted): `gate-tail1-multi-card-shadowing-2026-07-11.md` (HIGH,
v1.10.1 target — evidence venture-lab #33 heads 798a3d0 GREEN-by-shadowing
/ 60e91f8 correctly HELD, runs 29144734514 / 29144777017; the kit's own
`ci.yml` uses the same `tail -1`) and
`model-doctrine-emphasis-blind-phrase-2026-07-11.md` (minor, websites
#105). Claim `control/claims/wave-v1.10.0-adopters-regen.md` (#184 @
59ede0a) deleted. Verified on this branch: `python3.10 -m pytest tests/
-q` → **983 passed**; `check_idea_index` OK; `check --strict` sole
pre-flip finding was this card's own designed born-red hold.

## 💡 Session idea

The two gate-picker idea files now in the backlog (tail-1 shadowing +
superbot-next's folded-gate mtime grading) are the same root defect —
"the gate grades ONE card chosen by a heuristic, not the diff" — and the
fix for both is the same loop-every-card block. When the v1.10.1 slice
picks up the HIGH item, it should ship a single `check --cards-from-diff
<range>`-style engine entry point that gates templates AND folded hosts
can call, instead of each workflow re-implementing the shell derivation:
one implementation, one regression suite, and hand-folded copies stop
drifting from the template (the class both findings share).

## ⟲ Previous-session review

The T5 re-scope session (#182/#183) modeled the parked-pin discipline
well: pin PR #181 left `do-not-automerge`, never armed, with the
behavioral non-merge proof recorded on the heartbeat — exactly the
owner-gate contract. One improvement it surfaces: its status overwrite hit
a behind-stall (915ee4c merge to clear it) because the close-out branch
was cut before its own support PR merged; the release-lane's known play
(cut the close-out branch from post-claim/post-sibling main) is recorded
only in heartbeat prose — it belongs in the claims README step 3 or the
session-close checklist so every lane inherits it, not just the one that
learned it.

