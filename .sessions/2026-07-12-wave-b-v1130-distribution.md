# 2026-07-12 — Wave B: v1.13.0 distribution to the last four adopters

> **Status:** `in-progress`

- **📊 Model:** fable-5 · medium · distribution-wave

## Scope (what is about to happen)

Wave B of the v1.13.0 distribution (tag v1.13.0, annotated eb5edd0 →
828e450, release run 29191006519, asset sha256
`982b2667b2158aa77639fd44bca72ab8e047fb3bdabbde580937dd1325730959`,
735,972 B — download + release.json field verified this session; matches
the committed-dist hash at the bump SHA, three-way ✔).

Registry order (docs/adopters.md, generated 2026-07-11T22:36:49Z; superbot
excluded — owner-held v1.0.0 pin-only row): Wave A = first five, Wave B =
LAST FOUR: **gba-homebrew · pokemon-mod-lab · venture-lab · fleet-manager**
(all four trees at v1.12.1 → v1.13.0).

Recipe: the `upgrade-distribution` skill (kit PR #265) per adopter — stage
the verified asset as `bootstrap.py.new` + `release.json` in each adopter
root → `python3 bootstrap.py.new upgrade` (verify the banked
`bootstrap-1.12.1.py` rollback) → carve-out scan read → per-repo verify +
`check --strict` → born-red card PR per adopter, merged on green,
tree-verified afterward.

Kit-side this PR touches ONLY this card + the wave-B claim file
(`control/claims/claude-wave-b-v1130.md`). NO engine/dist/src changes;
NEVER `control/inbox.md`, `bench/`, or pin PRs #220/#238; heartbeat `kit:`
bumps stay lane-owed per Q-0261.3; adopters regen (currency) belongs to the
wave close-out slice, not this card's first commit.

This card opens the PR born-red by design (session gate HOLD); the 💡 idea
and ⟲ review sections below are stubs to be filled at flip time.

## Close-out

(to be written at flip time — per-repo outcome lines:
`<repo>: v1.12.1 → v1.13.0 · sha256 3-way ✔ · bank ✔ · carve-outs: <n> · PR #<n> merged @ <sha> · tree-verified ✔`)

## 💡 Session idea

(stub — filled at flip time)

## ⟲ Previous-session review

(stub — filled at flip time)
