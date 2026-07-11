# 2026-07-11 — upgrade carve-out scanner: three-way compare

> **Status:** `in-progress`

- **📊 Model:** fable-5 · high · fix

## Scope (what is about to happen)

Fix the v1.11.0-wave carve-out false positive (evidenced on the wave cards
of fleet-manager #72 · superbot-games #45 · trading-strategy #60 ·
gba-homebrew #44 · venture-lab #37): when a kit release changes the kit's
OWN generated gate content (the #199/#195 checkout@v5 / setup-python@v6
pin bumps), the kit-owned workflow regen compares the adopter's LIVE gate
against the NEW template only, misreads the kit's own outgoing template
content as "host-added" steps (phantom carve-outs), and banks a pre-regen
copy that is byte-identical to the OLD template (unnecessary bank).

The fix is a THREE-WAY compare in `_regen_kit_owned_workflow`
(`src/engine/adopt.py`): live vs OLD template (recovered from the staged
copy at `<state_dir>/ci/` captured BEFORE the staging pass overwrites it)
vs NEW template. A diff is a host carve-out ONLY when present in live and
explained by NEITHER template; kit-side evolution is a one-line
informational note; a live gate byte-identical to the old template
produces zero flags and NO bank. Old template unrecoverable → degrade to
today's two-way compare with an explicit warning, never a crash.
Regression tests: pin-bump-only (no flags, no bank) · genuine host
addition (still detected + banked) · mixed (only the host step flagged).
CHANGELOG under [Unreleased]; dist rebuilt (byte-pin); NO release cut, NO
version bump. Claimed via `control/claims/carveout-three-way-compare.md`
(PR #208). NEVER touching `bench/` or its trend/result homes (parallel
run-7 lane) and never `control/inbox.md`.
