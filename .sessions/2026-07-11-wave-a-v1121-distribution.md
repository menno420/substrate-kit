# 2026-07-11 — wave A: v1.12.1 distribution (registry rows 1–3, 5–6)

> **Status:** `complete`

- **📊 Model:** fable-5 · high · distribution-wave

## Scope (what is about to happen)

Wave A of the v1.12.1 distribution (tag v1.12.1 → 203bb09, run 29170017074,
dist sha256 `1055ca2cfd32a83e3dab7a978b05fbec2a82932a3375de0b1034f2519c16e4aa`,
704108 bytes — re-verified on this session's HEAD 27b0250). Lane claim:
`control/claims/wave-a-v1121.md` (PR #249, control fast lane).

- **Kit row (registry row 1):** verified already current at v1.12.1 via the
  release itself — no-op, hash re-verified on this session's HEAD.
- **Upgrade PRs** in the four wave-A adopters: **superbot-next, websites,
  superbot-games, trading-strategy** — vendor `dist/bootstrap.py` v1.12.1
  (carries the substrate-gate false-green fix), bump `substrate.config.json`
  pin, per-repo check + PR.
- **Close-out here:** `control/status.md` wave-A rows ONLY (the parallel
  wave-B session owns its four rows: gba-homebrew, pokemon-mod-lab,
  venture-lab, fleet-manager) + flip this card + delete the claim file.

This card opens the PR born-red by design (session gate HOLD); the 💡 idea
and ⟲ review sections below are stubs to be filled at flip time.

## Close-out

All five wave-A rows verified at v1.12.1 (upgrade workers' results, cited):

- **substrate-kit (row 1):** already current at v1.12.1 — `dist/bootstrap.py`
  sha256 `1055ca2c…16e4aa` matches the release asset. Verified no-op.
- **superbot-next:** PR #215, squash merge **977bb27** — all required checks
  green (gate / tests / code-quality etc.), carve-outs 0, **1468 tests passed**.
- **websites:** PR #155, merge commit **ebcc42f** — quality run 29170557594
  success, exact-pin test bumped to 1.12.1, carve-outs 0, **202 tests passed**.
  Follow-up PR #156 (merge 8f97654) fixed the card's model line to
  family-level.
- **superbot-games:** PR #58, squash merge **5ddfbee** — substrate-gate run
  29170525148 + tests run 29170525147 success, carve-outs 0, **310 tests
  passed**. Live gate regenerated with the false-green fix.
- **trading-strategy:** PR #63, squash merge **ea22323** — substrate-gate run
  29170538316 + pytest run 29170538307 success, carve-outs 0, **223 tests
  passed**. Live gate regenerated with the false-green fix.

**Adopters regen (runbook §6, owed to this lane):** `python3 dist/bootstrap.py
currency` regenerated `docs/adopters.md` against kit release v1.12.1 — 10
repos scanned, all 9 vendored trees read **v1.12.1** (superbot stays the
deliberate v1.0.0 pin-only row). Wave B's four rows scanned current because
their session had already merged; had it not, their rows would show whatever
their trees said at scan time (their session regens again later) — expected
either way. DRIFT rows are the known self-report heartbeat-lag class (see ⚑
FOR MANAGER) plus the kit's own deliberate tree-internal pin row (v1.0.0
config pin vs v1.12.1 dist — the §7 question, not chased per the known quirk:
the kit's own row can snapshot as DRIFT mid-close and self-heals next regen).

**Close-out mechanics:** merged origin/main into the branch (absorbed wave
B's close-out #248, the adopter-outcomes close-out #251/#247 — clean, no
conflicts), recorded ⚑ WAVE A DONE in `control/status.md` (phase line +
blockers claim note + next-queue top item; wave-A scope only — wave-B rows,
pin-PR notes #220/#238, and the other lanes' text untouched), deleted
`control/claims/wave-a-v1121.md`, flipped this card. With wave B's record,
**the v1.12.1 distribution is COMPLETE — all 9 vendored adopters at v1.12.1.**

## 💡 Session idea

`.substrate/upgrade-report.md` is overwritten wholesale on each upgrade,
silently dropping still-unapplied template-delta flags (observed this wave:
superbot-games' AGENT_ORIENTATION v1.12.0 delta note vanished when the
v1.12.1 upgrade rewrote the report). The report should carry forward an
"outstanding" section for deltas not yet applied, so lane-owed doc merges
survive across upgrades instead of losing their only pointer.

## ⟲ Previous-session review

The v1.12.1 release session (#244/#246): a clean cut — three-way sha
verification (downloaded asset == release.json == committed dist) and a
proper freeze-compliant deferral of the distribution wave. Improvement it
surfaces: it left no wave-tracking scaffold in `control/status.md`, so each
wave session invents its own row format; release runbook §6 could pre-plant
a wave-record block (repo · PR · merge sha · run citation columns) at cut
time.

## ⚑ FOR MANAGER (non-kit, lane-owed observations from the wave)

- **Heartbeat drift compounding:** superbot-games `control/status-mining.md:8`
  + `control/status-exploration.md:11` still say v1.7.1 (5 releases behind);
  superbot-next `control/status.md:5` says v1.10.1; websites and
  trading-strategy say v1.12.0 (stale-by-one). Heartbeat-bump ownership is
  still unresolved (3rd+ consecutive wave this class re-flags).
- **superbot-games and trading-strategy still have no live root CLAUDE.md**
  (staged copy only).
- **trading-strategy:** `docs/CAPABILITIES.md` landing-constraints entry and
  the AGENT_ORIENTATION v1.12.0 manual doc merge still owed (repeat flags).
