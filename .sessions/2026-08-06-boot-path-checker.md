# 2026-08-06 · Promote the deterministic tier, and instrument the boot path

> **Status:** `complete`

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

## What actually shipped — the sweep was corrected twice

The table above is what the 12-tree sweep said. **Two of its three "promote"
verdicts did not survive**, and both corrections came from instruments rather
than from re-reasoning:

- **`automerge_preflight` → held.** Its 2 findings are real, but my own stated
  rule is *promote on a clean sweep*, and two live findings is not a clean
  sweep. Promoting anyway would also spend the §6.4 compat guarantee. The rule
  I wrote applied to me before it applied to anyone else.
- **`staged_regen` → held.** It fires on **zero of 12 trees** and still cannot
  be promoted: it fires **three times on the cold-adoption arc**, so promoting
  it would make every NEW adoption born-red on a defect `adopt` itself creates.
  My sweep swept mature trees and had no way to see this — `tests/
  test_check_engagement.py` caught it. **A clean sweep across adopters is
  necessary evidence for promotion, not sufficient**; the arc a new adopter
  walks is part of the fleet too. That is a flaw in my method, not in the data.

Final: **6 of 9 deterministic sites gate**; `automerge_preflight`,
`staged_regen` and `boot_path` wait in `gate_pending_advisories()`.

## Verification

- `python3 -m pytest tests/ -q` → **2132 passed, 1 skipped** (exit 0, read
  directly).
- `python3 -m ruff check src/engine/` → exit 0 · `tools/check_no_false_walls.py`
  → exit 0 · `dist/bootstrap.py check --strict` → exit 0 (post-commit).
- **Promotion verified live, not argued:** `check --strict` re-run across all
  12 adopter trees after wiring → **0 promoted reds**.
- **The new checker verified against the fleet:** boot-path findings on **10 of
  12** trees; the two clean ones are substrate-kit and fleet-manager, both
  repaired earlier today in #577/fm #789.

⚠ **Two bugs in my own checker, both caught by tests I did not write.**

1. It did not self-quiet on a bare tree, so `check` would red a repo before it
   had adopted. `test_check_boot_path.py::test_bare_tree_is_silent` — a test
   whose docstring I had written claiming behaviour the code did not have.
2. Its `from engine.render import agreement_home` was **lazy, inside the
   function**, which survives into the built single-file dist where no `engine`
   package exists — `build_bootstrap` strips only *module-level* engine
   imports. The source layout passes; the dist raises `ModuleNotFoundError` on
   first call. Caught by `tests/test_bench.py`'s cold-adoption arc, the one
   test that exercises the built dist rather than the source tree. Worth the
   journal: **src-layout green says nothing about the artifact adopters run.**

**Honest nulls.**

- **The fleet is not converged.** 10 of 12 trees still have a dead boot path.
  This ships the instrument, not the cleanup — each repo needs a `Boot read
  path` section added by hand, because planted docs are skip-if-exists and
  `upgrade` will not add one.
- **`boot_path` is not gated**, so nothing yet stops the defect recurring; it
  is only visible. Promotion waits on the fleet converging.
- **The two `automerge_preflight` defects are recorded, not fixed** — the kit
  never writes to consumers (KF-2), so they need a session in each repo.
- **`--gate-preview` still cannot distinguish "ran clean" from "did not
  engage".** The wording was corrected to stop implying coverage, but the
  underlying limitation stands: a site only reaches the report when it produces
  a finding.
