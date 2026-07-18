# Session · 2026-07-18 · kit-release-v1.19.0-aftermath

> **Status:** `complete`

Intent: release aftermath — regen `docs/adopters.md` + update `docs/current-state.md`
to v1.19.0 released (self-row v1.19.0; adopters stay stale pending the owner-gated wave).

- **📊 Model:** Opus 4.8 · medium · docs-only
- ⚑ Self-initiated: registry-truth aftermath of the v1.19.0 release — regenerated
  the adopter registry so its self-row records the freshly-released kit version, and
  corrected the state docs (current-state / status) from "v1.18.0 released-not-distributed"
  to "v1.19.0 released + verified". Reversible docs-only truth reconciliation of a just-shipped
  release; per the standing decide-and-flag grant.

Did: regenerated the adopter registry via `python3 dist/bootstrap.py currency`
(all 12 repos scanned; self-row → v1.19.0 current, every adopter row correctly stale
at v1.17.0-or-older; the superbot-games DRIFT row is carried adopter-side self-report
lag, owner-gated). Updated `docs/current-state.md`
v1.18.0-released-not-distributed → v1.19.0 released + verified (tag v1.19.0, sha256
three-way PASS, release URL), and corrected `control/status.md`'s Recently-shipped
release record to the completed truth (tag v1.19.0, run 29656601475 success, sha256
three-way PASS). `git diff --exit-code dist/bootstrap.py` clean — the dist was NOT
touched. `pytest tests/`: 1765 passed, 1 skipped. `check --strict`: only the born-red
HOLD on this card (pre-flip) + a pre-existing out-of-scope model-line advisory on
another card.

Scope: `docs/adopters.md` · `docs/current-state.md` · `control/status.md` · this
card · `control/claims/release-v1-19-0-aftermath.md`.

## 💡 Session idea (Q-0089)

**CI self-row stamp — close the release→aftermath registry-lag window without a
sibling fetch.** The adopter registry self-row (menno420/substrate-kit) is derived
purely from the *local* committed tree (`dist/bootstrap.py` header +
`substrate.config.json` pin) — it needs **no** sibling-repo access. Yet today the
whole `docs/adopters.md` regen is a single manual agent-side aftermath step, so
between a version-bump merge and the aftermath session the self-row lags the just-released
version and only the `adopters-version-lag` advisory (fired again this session) catches
it after the fact. Idea: teach `release.yml` (or `kit-quality`) to deterministically
re-stamp **only the self-row + header** from the local tree — self-only, zero network,
CI-safe — leaving the sibling adopter rows to the existing agent-side full regen. That
makes the registry's own version-of-record self-heal the instant a release lands, and
demotes the manual aftermath regen to *just* the sibling rows. Distinct from the shipped
`currency --check` verb (PR #392), which detects row deltas via a sibling scan; this
writes the self-row with no fetch. Worth a `docs/ideas/*.md` entry when groomed.

## ⟲ Previous-session review (Q-0102)

Of the 2026-07-18 kit-release-v1.19.0 card (PR #461, the release-cut): genuine credit —
it correctly split the release into a born-red version-bump PR (three version homes +
CHANGELOG transform + dist rebuild) and left publish (tag + Release via `release.yml`
`workflow_dispatch`) plus the registry regen as deliberately separate later steps, which
is exactly what kept this aftermath pass clean and small. Small miss: its own `📊 Model:`
line used task-class `release cut`, which does not prefix-match any of the 9 PL-004
classes — the guard-fire ledger recorded it verbatim as an unmatched class (visible in
`.substrate/guard-fires.jsonl` this session); the taught class for a version-bump build is
`feature build`, which the card's own `⚑` line actually used. System improvement it
surfaces: the CI self-row stamp above (💡) — the release-cut card explicitly deferred the
registry regen to "the aftermath," which is precisely the manual hop that leaves the
self-row stale in the interim; automating the self-only half removes that hop.
