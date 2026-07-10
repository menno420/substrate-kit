# Session 2026-07-10 — adopter-registry regen after the v1.7.0 upgrade wave

> **Status:** `complete`

- **📊 Model:** claude-fable-5 · medium · docs-regen (fleet registry currency)

**Scope (as declared, born-red):** distribution-wave close-out — regenerate
the GENERATED `docs/adopters.md` via `python3 dist/bootstrap.py currency` now
that four adopters merged their v1.6.0 → v1.7.0 upgrades on green
(superbot-next #116 @ a700975 · websites #62 @ e671cb3 · gba-homebrew #26 @
bc73da7 · venture-lab #13 @ ce22315). Registry-only + this card; NEVER
touched: `control/inbox.md`, `control/status.md` (the coordinator owns the
seat heartbeat — which is also why no `claimed-by:` line accompanies this
session; this born-red card + the immediately-opened PR is the in-flight
signal). Verified pre-flight: no open PRs, no live claim touching
`docs/adopters.md` or the currency checker.

## Close-out

**Shipped (session PR #135):** `docs/adopters.md` regenerated from live tree
truth (10 repos scanned). The four wave repos now read **tree=v1.7.0 ·
pin=v1.7.0**: superbot-next, websites, gba-homebrew, venture-lab — the
upgrade wave is registry-visible. Verified locally: `python3 -m pytest
tests/ -q` → **852 passed**; dist rebuild byte-pin clean; `check --strict`
green except this card's own born-red hold (this flip clears it).

**Surfaced, not resolved (registry protocol — reconcile at the SOURCE):**
6 DRIFT rows, all self-report lag, none tree-level: superbot-next / websites
/ gba-homebrew heartbeats still say `kit: v1.6.0` (their upgrade PRs didn't
bump the status `kit:` line — the release checklist's last step);
superbot-games claims v1.2.0 on both lane heartbeats vs tree v1.7.0;
fleet-manager claims v1.4.0 vs tree v1.7.0; the kit's own tree-internal pin
drift (config v1.0.0) stays pending the §7 version-truth ruling. Also
noteworthy: superbot-games, trading-strategy and fleet-manager turn out
ALREADY at tree v1.7.0 (upgraded since the 18:31Z regen by other lanes) —
the wave reached 8 of 10, only superbot (pin-only v1.0.0) and
pokemon-mod-lab (not adopted) remain.

**💡 Session idea:** the four fresh DRIFT rows share one cause — `upgrade`
completes without touching the adopter's own `control/status.md` `kit:`
line, so every upgrade wave mints a self-report drift by construction. The
upgrade verb (or its printed checklist's last step) could rewrite the `kit:
vX.Y.Z` token in the heartbeat it already knows how to find (adopt plants
it), making the self-report column self-healing instead of
checklist-dependent.

**⟲ Previous-session review:** the §6.3 session (#132/#133) shipped the
scanner this session leaned on — the injectable-fetcher seam and `--dry-run`
made pre-claim feasibility a one-command check, exactly right. One
improvement it surfaces: its verdict column renders self-report drift as
`⚠️ DRIFT · current`, which buries the actionable half (who is stale on
WHAT) in the drift report below; a per-row drift-kind tag (tree-internal vs
self-report-lag) would make the table triageable at a glance.
