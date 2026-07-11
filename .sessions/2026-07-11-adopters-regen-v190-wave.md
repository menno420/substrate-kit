# 2026-07-11 — adopters regen after the v1.9.0 distribution wave

> **Status:** `complete`

- **📊 Model:** fable-5 · medium · registry-regen — post-wave currency
  snapshot of the fleet adopter registry

## Scope (what is about to happen)

Regenerate `docs/adopters.md` via `python3 dist/bootstrap.py currency` now
that the kit-seat v1.9.0 distribution wave is merged: superbot-next #150
(d653ba1), websites #101 (7da9fbf), gba-homebrew #36 (31c8672), venture-lab
#32 (9b504e8). A PARALLEL worker is upgrading fleet-manager / superbot-games /
trading-strategy — their rows snapshot at whatever their main trees say at
regen time; the card's close-out records which of those three read v1.9.0
vs v1.8.0, tree-verified. Files: `docs/adopters.md` (generated output,
shipped as the tool emits it) and this card. No claim file — registry-regen
sessions ride the born-red card + immediately-opened PR as the in-flight
signal (precedent #135/#142/#161). NEVER `control/` or `bench/`.

## Close-out

Shipped the declared scope exactly: `docs/adopters.md` regenerated via
`python3 dist/bootstrap.py currency` (Generated: 2026-07-11T05:33:10Z, 10
repos scanned), output committed as the tool emitted it — no hand edits.
Snapshot: **8 tree-current rows at v1.9.0** (substrate-kit, superbot-next,
websites, superbot-games, trading-strategy, gba-homebrew, venture-lab,
fleet-manager); superbot stays pin-only stale v1.0.0; pokemon-mod-lab not
adopted. **Timing note on the parallel trio:** fleet-manager,
superbot-games, and trading-strategy were ALL already v1.9.0 at snapshot
time — tree-verified via the GitHub MCP (`substrate.config.json`
`kit_version: 1.9.0` on main @ 6dedff6 / 4689e5a / 3833fcc respectively),
never from heartbeats. Six DRIFT rows remain, all the known
lagging-heartbeat class (lane-owed `kit:` line bumps, NOT distribution
work): websites v1.8.0, superbot-games v1.7.1×2 lanes, trading-strategy
v1.7.1, gba-homebrew v1.8.0, fleet-manager v1.7.0 — plus the kit's own
chronic tree-internal pin drift (config pins v1.0.0, dist v1.9.0). The
recipe's predicted mid-close self-report DRIFT on the kit's own row
self-healed exactly as documented (self-report now v1.9.0). Verified
locally on this branch: `python3 -m pytest tests/ -q` → 973 passed; dist
byte-pin green (`src/build_bootstrap.py` then `git diff --exit-code
dist/bootstrap.py`); `check --strict` sole pre-flip finding was this
card's own designed born-red hold.

## 💡 Session idea

Every regen re-prints the same lagging-heartbeat DRIFT rows and each one
costs a lane owner a re-derivation ("what exactly do I paste where?").
Cheap fix in `cmd_currency`: for each self-report-vs-tree drift, append a
paste-ready fix line to the drift report — e.g. `fix: set 'kit: v1.9.0 ·
check: green · engaged: yes' in control/status.md` — so the lane owner's
bump is a one-paste act and the drift report becomes self-clearing
instructions instead of a recurring complaint.

## ⟲ Previous-session review

The release close-out session (#173) predicted its own registry row would
snapshot DRIFT mid-close and self-heal at the next regen — this regen
confirmed that prediction exactly (kit self-report now v1.9.0, drift line
gone), which is the review loop working as designed. What it left
standing: the kit's own `substrate.config.json` pins `kit_version: 1.0.0`
while dist is v1.9.0 — a tree-internal DRIFT re-reported by every regen
for multiple releases now. That is spotted drift, not backlog: a kit-lane
session should either bump the pin at source or make `cmd_currency`
exempt/explain the kit-lab's own pin semantics, so the registry stops
re-printing a permanent warning nobody acts on.
