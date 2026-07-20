# Session — S17 recipe-discovery advisory (applies-when discovery nudge)

> **Status:** `complete`

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

## Result

- **Shipped:** `src/engine/checks/check_recipe_discovery.py` (new), wired in
  `src/engine/cli.py` (posture="advisory" seam), added to `MODULE_ORDER` in
  `src/build_bootstrap.py` after its grammar source, `dist/bootstrap.py` rebuilt
  + byte-pinned (1304582 bytes, build idempotent), `tests/test_check_recipe_discovery.py`
  (+11 hermetic tests).
- **Verify:** full suite `2025 passed, 1 skipped` (2014 baseline + 11);
  `python3 dist/bootstrap.py check --strict` green (only red = the by-design
  born-red HOLD on this card while in-progress); `ruff check src/` clean.
- **Behavior confirmed:** fires ONE nudge on a fresh adopter tree that grew a
  recipe's full signature but never references it; silent on the kit's own tree
  (both shipped recipes are already-referenced → suppression guard); silent on
  self-reference (recipe's own markers), partial signatures, kit machinery.
- **PR #543** — https://github.com/menno420/substrate-kit/pull/543
- **Baton → wave-3 groom (backlog dry):** with S17 landed and S16 found
  already-shipped (#479), the wave-2 buildable-now ladder S2–S17 is EXHAUSTED.

## 💡 Session idea

**A shared, lazily-cached tree-content corpus for content-scanning advisories.**
S17 is the FIRST `check` advisory that does a *full-tree content scan* — it walks
the whole adopter tree and reads every file's text once (`_iter_files` +
`_read_text_lc`) to match `content:<marker>` tokens. Every other advisory reads
only a handful of named files. The moment a SECOND full-tree content scanner
arrives — and the S8 card's own "adopter-tree-aware surface census" idea is
exactly that (parse the adopter's `.github/workflows/*.yml` + hooks) — it will
re-walk and re-read the entire tree independently, doubling the I/O on every
`check`. Idea: build a single **`TreeCorpus`** (rel-paths list + per-file
lowercased content, with the shared prune-set + size/UTF-8 fail-open already in
`check_recipe_discovery`) constructed once per `check` run and passed on
`config`, so discovery and any future tree-scanning advisory amortize one walk
instead of N. It also gives the prune/skip policy (`_PRUNE_DIRS`, `_MAX_BYTES`,
kit-machinery exclusion) a single home instead of a copy per scanner. Deduped
against `docs/ideas/` (grep `tree.corpus`/`content.index`/`amortiz`/`tree.scan` —
the one hit in `README.md` is about template-dir scanning, a different surface)
and the wave-2 doc. Genuinely believe it: I just wrote the first such walk, and
the second consumer is already an accepted idea on the S8 card.

## ⟲ Previous-session review

Previous session was **S15 — cut_release --rebuild-dist (#541)**. Done well: it
folded the one deterministic FOLLOWUP step (dist regen + byte-pin) into the cut
behind an opt-in `--rebuild-dist` flag while rigorously honoring the HARD
BOUNDARY (no version bump / tag / release.json / workflow dispatch) — a clean
contained slice. What it (and the whole S4→S15 chain) MISSED: each card
propagated the `Next-2 baton → S16 (--api-latency harness — needs live GH)`
pointer **without tree-verifying that S16 was unbuilt** — and it wasn't
(`run_api_latency` shipped in #479/GSW-5, predating the wave-2 doc). That stale
baton is exactly what dispatched THIS worker at an already-built rank; only the
collision-guard grep caught it. **System improvement it surfaces:** the S4
`check_baton_resolves` advisory verifies a baton names a resolvable *path/anchor*
but NOT that the named *deliverable* is genuinely unbuilt. A natural next rung —
a **baton-deliverable-freshness advisory**: when a `## Next-2 baton` entry names
a concrete symbol/flag deliverable (e.g. a `--flag` or `check_*` name), grep the
tree for it and warn if it already exists, so a "build X" baton pointing at
already-shipped work reds at check time instead of burning a worker's session.
That would have flagged the stale S16 baton before this session started.
Recommend it as a top mechanical rank in the coming wave-3 groom.

## ⚑ Self-initiated

- **Honest-null + rank swap (collision guard):** S16 was found already-shipped
  (#479) from tree evidence; per the guard's step-4 rule I swapped to S17, the
  last unbuilt S-rank, and decided from the tree (Q-0120) rather than the stale
  baton. No owner sign-off needed — S17 is a contained, reversible, advisory-only
  addition that lands on green CI.

