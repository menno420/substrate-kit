# 2026-08-06 · Promote the deterministic tier, and instrument the boot path

> **Status:** `in-progress`

- **📊 Model:** opus-5 · high · feature build

💡 Session idea: **the 2026-07-12 boot-pointer fix moved the deadness instead
of removing it, and nothing noticed for 25 days.** That fix replaced a router
step naming `.claude/CLAUDE.md` with one naming the working agreement. Measured
today across 11 adopter trees: 5 carry the new text pointing at an agreement
that has **no boot section**, and 6 still carry the old dead form. **0 of 11
have a working boot read path.** Both forms are dead; the second is just harder
to see. Nothing in the kit ever asserted that a boot pointer resolves — the
`[reachable]` checker verifies docs are reachable *from* the read path, never
that the read path's own targets exist. This is the inverse of an instrument
that already ships.

## previous-session review

`2026-08-06-checker-census.md` (#577) classified all 29 advisory sites and
routed the heuristic ones off the agent's channel. It deferred the promotion of
the 8 deterministic sites on the reasoning that flipping them would be "a fleet
bomb during version skew" across ~22 adopters.

**That reasoning was wrong and this card corrects it.** Adopters do not track
kit HEAD: each vendors a pinned, generated `bootstrap.py` (fleet-manager runs
1.20.1 against the kit's 1.20.2), and a new checker arrives only through an
explicit one-repo-at-a-time upgrade PR that sha256-verifies a release and lands
born-red with a banked rollback. A promoted checker cannot red the fleet at
once; it reds one repo, on its own upgrade PR, where a session is already
looking. The previous card built `--gate-preview` to turn the promotion into a
measurement and then did not run the measurement. This card runs it.

⚠ Also caught: the previous card's own `template-local-heading-drift` finding
was surfaced INLINE by the deterministic tier exactly as designed, and the
session missed it by reading the gate output through `tail -4`. An advisory you
can miss by tailing is not a gate — which is itself the argument for the
promotion.

## The sweep `MEASURED` — 12 trees, 3 findings

| checker | trees firing | verdict |
|---|---|---|
| `staged_regen` · `enforcement_strength` · `folded_gate` · `fastlane_symmetry` · `recipe_applies_when` · `baton_resolves` | **0 of 12** | promote |
| `template_sync` | 1 (substrate-kit — self-inflicted, fixed here) | promote |
| `automerge_preflight` | 2 (superbot, superbot-next — real defects) | promote; they red on their own upgrade PR, which is the designed path |

## What this lands

- `CONSTITUTION.md.tmpl` — a `Boot read path` section, so the working agreement
  every adopter renders actually carries the list its router points at. Fixes
  the destination the 07-12 fix assumed existed.
- `check_boot_path` — a deterministic checker asserting the boot pointer chain
  resolves: the named agreement exists, it carries a boot section, and every
  path that section names is on disk.
- The 8 deterministic advisory sites promoted to exit-affecting.
- `--gate-preview` corrected: it reported "N sites ran" while counting only
  sites that produced findings.

## Verification

Filled at close. Born red.
