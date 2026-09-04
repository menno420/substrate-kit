# 2026-09-04 · Adoption profiles — K1–K5 for the `estate` seed

> **Status:** `in-progress`

- **📊 Model:** opus-5 · high · feature

💡 Session idea: **five "the hub needs a different shape" requirements were
one missing abstraction, not five flags.** `ADOPT_PLAN` was already a data
table and `Config` already carried `sessions_dir`/`docs_root`/`claims_dir`;
what the kit lacked was a name for *which shape an install was born in*, so
every consumer that iterates the plan (`check_engagement`,
`check_template_sync`, `check_skill_grounds`) assumed the one shape. The
smallest honest fix is a declared profile on the config plus one accessor
every consumer reads — not five conditionals at five call sites.

## previous-session review

`2026-08-28` (kit #587/#588) fixed the false-negative family in
`check_no_false_walls` and reconciled the kit's own `current-state.md`, each
fix reproduced against the published asset before it was written. This
session inherits that discipline in a harder place: the change is to
**adoption itself**, where the regression surface is every existing adopter,
so every K item ships with a paired negative test — a mutant that must go red
— and the generated `dist/bootstrap.py` is exercised through the same public
interface a future `estate` seed will use, not just the source package.

## Why this session exists

fleet-manager `[D-0035]` (owner, live, 2026-09-01, all defaults on question E)
sets the `estate` build order and puts **K1–K5 in substrate-kit, one release**
ahead of the seed, because they shape the tree at birth and would cost renames
later — against his no-renames condition (`[D-0025]`). The requirement text is
`fleet-manager:docs/planning/2026-09-01-estate-structure-proposal/kit-prerequisites-and-migration.md`;
the decided form (which resolves each of the proposal's either/ors) is
`fleet-manager:docs/decisions.md` `[D-0035]`.

## What this ships

[[fill: written at flip — the profile, the five K items, the tests]]

## Verify

[[fill: real exit codes at flip]]

## Honest null

[[fill: what is deliberately deferred]]
