# 2026-07-15 · model-line-payload-sweep

> **Status:** `complete`

- **📊 Model:** Claude 5 family · medium · docs-only (model-line payload sweep)
- Scope: baton item 2 of the 12:14Z heartbeat — retro-fix the 4 older session cards with malformed/off-taxonomy `📊 Model:` payloads (PR #390, branch claude/model-line-payload-sweep).

About to (opening declaration, retained): baton item 2 — retro-fix
2026-07-14-seat-digest-adaptive-clip, 2026-07-14-v1.16.0-wave,
2026-07-15-adopters-currency-refresh, 2026-07-15-idea-index-shipped-drift so
the PL-004 harvest records them; heartbeat re-stamped in the same PR.

## Record

- Boot: hard-synced to origin/main 30a2a53; inbox newest ORDER 024 (already acked+done per the heartbeat `orders:` line; the "ORDER 025" text near inbox line 210 is the acked fm relay inside ORDER 019, not a new order). control/claims/ held README only; zero open PRs at the 12:3xZ scan — no backpressure.
- Adopter-bump precheck first: live raw-content scan of every registry row matched docs/adopters.md @ 30a2a53 exactly (websites/venture-lab/idea-engine v1.17.0; superbot-next + superbot-mineverse v1.16.0; superbot-games `kit: substrate-kit v1.15.0` + lanes v1.7.1 — all known DRIFT, already recorded; no-`kit:`-line repos unchanged) — no new bump, no currency re-run.
- The sweep (docs-only): all 4 flagged lines now carry shape-valid three-field payloads. Honesty rule (decide-and-flag): original self-reported model tokens kept verbatim (`Fable`, `Fable-class`); task-class mapped from each card's own recorded content (`feature build` for the seatdigest engine slice; `docs-only` for the wave close-out + the two registry/index slices, original `distribution/ceremony` wording kept as in-field decoration); effort backfilled ONLY where the authoring session recorded it (the wave card's `medium`). The other 3 never self-reported effort — their segment reads `unrecorded` rather than an invented tier, deliberately trading 4 shape/class advisories for 3 `model-line-effort` nags (advisory-only; they age out of the newest-10 lint window). Terminal: later wakes must NOT re-fix these by inventing low/medium/high.
- Verify: `python3 scripts/preflight.py` 8/8 legs green (pytest 1594 passed, 1 skipped in 39.28s; ruff; dist-byte-pin; idea-index; retro-index; changelog-structure; program-law; bench-integrity). `check --strict`: the 4 targeted advisories cleared; remaining = designed born-red HOLD (this card, pre-flip) + known staged-regen-lag ×3 + the 3 deliberate `unrecorded` nags.
- Heartbeat overwritten wholesale before this flip: sweep facts + terminal disposition recorded; ⚑ blocks carried byte-identical; `kit:` line plain; baton refreshed (1: grounded-skills window ~07-19..26 · 2: currency re-run conditional on adopter lane bumps, else next backlog idea).

## Session enders

- 💡 **Session idea:** model-line `unrecorded` effort marker — sanction `unrecorded` as an advisory-silent terminal effort value for retroactive payload repairs in `check_model_line` (harvest still records verbatim; live off-taxonomy values still nag), so honest repairs stop looking like zero progress and stop inviting a later wake to invent a tier. Captured with a build sketch at docs/ideas/model-line-unrecorded-effort-marker-2026-07-15.md + README § Backlog entry. Dedup: grepped docs/ideas/ — the shipped payload-lint idea (#352) covers the lint itself, model-line-checker-false-red covers needle detection; nothing covers a sanctioned repair marker.
- ⟲ **Previous-session review:** the adopters-currency wake (PR #389) was tight — it re-ran currency only on a verified live bump (websites v1.17.0), retired exactly one DRIFT row, and converted its own claim-format friction into a same-session `bootstrap claim` re-render. Its best property showed up here: the baton item it wrote named the 4 target cards verbatim from checker output, so this session executed it with zero re-derivation. Concrete improvement it suggests: baton items should also carry a one-line done-when (e.g. "done when the 4 named advisories clear or a terminal disposition is recorded") — this session had to make the honest-vs-advisory-free judgment call itself; a done-when would have made that call once, at baton-writing time.
