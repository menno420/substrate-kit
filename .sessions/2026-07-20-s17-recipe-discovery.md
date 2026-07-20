# Session — S17 recipe-discovery advisory (applies-when discovery nudge)

> **Status:** `in-progress`

- **📊 Model:** Opus 4.8 · medium · feature build
- **Branch:** `claude/s17-recipe-discovery`
- **About to do:** Build wave-2 groom rank **S17** — a warn-only
  `check_recipe_discovery` advisory that, for an adopter tree exhibiting a
  recipe's `applies-when:` structural signature, nudges toward that recipe
  (discovery, not enforcement). The deferred-nudge threshold is now MET (≥2
  signed recipes carry `applies-when:` signatures). Distinct from S8
  (signature-HONESTY: tokens-vs-body): this is DISCOVERY — match a recipe's
  signature against the adopter's OWN tree.

## Collision-guard finding (headline)

**S16 (`--api-latency` harness mode) was ALREADY SHIPPED** — present in
`scripts/measure_grounded_skills.py` (`run_api_latency` / `render_api_latency` /
`--api-latency` flag) with hermetic tests in
`tests/test_measure_grounded_skills.py`, added by **PR #479** (commit `812b7c7`,
"GSW-5: graduate PR-latency into the harness as an opt-in --api-latency mode"),
which predates the wave-2 groom doc. The baton pointing at S16 was advisory and
stale — exactly the #506/#509 collision the guard warns about. Honest-null on
S16; swapped to **S17**, the last genuinely-unbuilt S-rank. Decided from tree
evidence (Q-0120).

## S17 design

New `src/engine/checks/check_recipe_discovery.py`, mirroring the R11/S8 seam:
- Reuses the badge grammar (`_RE_APPLIES_WHEN` / `_RE_TOKEN` / `_HEADER_LINES` /
  `_RECIPES_RELDIR`) imported from `check_recipe_applies_when` as the single
  source of truth — the three recipe lints can never drift on token grammar.
- For each recipe with a well-formed signature, matches ALL tokens against the
  **adopter tree** (`path:<glob>` → a file path matches; `content:<marker>` → a
  file contains the marker). Full-signature conjunction = the repo grew the shape.
- **Two correctness guards** (the discovery-not-nagging semantic):
  1. **Self-reference exclusion** — `docs/recipes/` is excluded from the scan, so
     a recipe describing its own markers is not adopter evidence (tree-level
     analogue of S8's body-minus-badge guard).
  2. **Already-known suppression** — if the recipe is already referenced anywhere
     in the tree outside `docs/recipes/` (a doc links it, a card cites it), the
     adopter already knows it → no nudge. Keeps the authoring kit repo quiet
     while firing on a fresh adopter that grew the shape but never heard of the
     recipe.
- Kit-machinery / VCS noise excluded (`bootstrap.py`, `.substrate/`, `.git/`,
  `__pycache__/`, `node_modules/`, `.venv`/`venv`); files > 512 KiB and
  non-UTF-8 skipped (fail-open). Input-gated (no `docs/recipes/` → `[]`).
  Advisory-only, off `STRICT_SUBCHECKS`, never exit-affecting. Stdlib only.
- Wired on the `posture="advisory"` seam in `cli.py`; added to `MODULE_ORDER`
  in `build_bootstrap.py` after `check_recipe_applies_when` (grammar source);
  dist rebuilt + byte-pinned.
- Hermetic tests in `tests/test_check_recipe_discovery.py` (no network).

[[fill: final result — tests, byte-pin, PR #, CI]]
