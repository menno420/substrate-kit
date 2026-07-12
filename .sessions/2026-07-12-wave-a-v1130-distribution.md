# 2026-07-12 — wave A: v1.13.0 distribution (registry rows 1–3, 5–6)

> **Status:** `in-progress`

- **📊 Model:** fable-5 · high · distribution-wave

## Scope (what is about to happen)

Distribution Wave A: upgrade 5 vendored adopters to v1.13.0.

The five wave-A targets, in `docs/adopters.md` registry order (first five
vendored adopters, superbot skipped — deliberate v1.0.0 pin):

- **menno420/substrate-kit** (row 1) — verify no-op: `dist/bootstrap.py` at
  HEAD already reads v1.13.0 (release #266/#267); re-verify sha vs the
  release asset.
- **menno420/superbot-next** — vendored v1.12.1 → v1.13.0.
- **menno420/websites** — vendored v1.12.1 → v1.13.0.
- **menno420/superbot-games** — vendored v1.12.1 → v1.13.0.
- **menno420/trading-strategy** — vendored v1.12.1 → v1.13.0.

Per-target procedure: the `upgrade-distribution` playbook skill (kit PR
#265) — preflight hard-reset, release download, sha256 three-way compare,
banked rollback verify, carve-out scan, born-red PR per target,
tree-verified merge. Wave B (gba-homebrew, pokemon-mod-lab, venture-lab,
fleet-manager) runs in parallel; this lane touches only its own wave-A rows
at close-out. Lane claim: `control/claims/wave-a-v1130.md`.

This card opens the PR born-red by design (session gate HOLD); the 💡 idea
and ⟲ review sections below are stubs to be filled at flip time.

## Close-out

(to be written at flip time)

## 💡 Session idea

(stub — filled at flip time)

## ⟲ Previous-session review

(stub — filled at flip time)
