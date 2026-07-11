# 2026-07-11 — Wave B: v1.12.1 distribution to the last four adopters

> **Status:** `in-progress`

- **📊 Model:** fable-5 · medium · distribution-wave

## Scope (what is about to happen)

Wave B: distribute kit v1.12.1 to the last four adopters in registry order.

Registry order (docs/adopters.md, 9 adopters at v1.12.0; superbot excluded —
owner-held pin-only row): Wave A = first five, Wave B = LAST FOUR:
**gba-homebrew · pokemon-mod-lab · venture-lab · fleet-manager**.
Recipe per docs/operations/release-runbook.md §6 + the wave records' shape
(kit-upgrade-distribution-gotchas): stage the three-way-verified v1.12.1
asset (sha256 1055ca2cfd32a83e3dab7a978b05fbec2a82932a3375de0b1034f2519c16e4aa,
704108 B, tag v1.12.1 → 203bb09, run 29170017074) as `bootstrap.py.new` +
`release.json` in each adopter root → `python3 bootstrap.py.new upgrade` →
`check --strict` → born-red card PR per adopter, merged on green.

Kit-side this PR touches ONLY this card + the wave-B claim file
(`control/claims/claude-wave-b-v1121.md`). NO engine/dist/src changes; NEVER
`control/inbox.md` or `bench/`; adopters regen (currency) belongs to the
wave close-out slice, not this card's first commit.

## Close-out

_(pending — flipped with the badge as the deliberate last step)_
