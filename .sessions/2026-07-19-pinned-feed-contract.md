# Session — pinned-feed-contract graduation

> **Status:** `complete`

**Scope:** Graduate the proven cross-repo pinned-feed-contract discipline
(superbot PR #1884 producer + websites PR #11 consumer) into portable kit
doctrine — a `docs/recipes/pinned-feed-contract.md` recipe + a
`CONSTITUTION.md.tmpl` rider (+ a `docs/recipes/README.md` index) — so the
cross-repo feed-desync bug class is killed for every adopter. Rank-1
buildable-now from `docs/planning/2026-07-19-needs-planning-recipes.md`.

(Born-red: this card's `in-progress` status held the PR red via the
kit-quality Session-gate until the work was complete; the badge flipped to
`complete` as the deliberate last step.)

- **📊 Model:** opus-4.8 · high · docs-only

## What shipped (PR #482)

- `docs/recipes/pinned-feed-contract.md` (new, badge `reference`) — the full
  three-part pattern (versioned contract file · producer-side fail-closed CI
  parity + `meta.schema_version` stamp · consumer-side pin + render-time
  verify with an honest drift banner), a copy-paste contract-file skeleton,
  the estate proof (superbot #1884 / websites #11), and the escalation
  boundary (doctrine-only first; scaffolding only if instances repeat).
- `docs/recipes/README.md` (new, badge `reference`) — the recipes index; a
  README, so it is an auto-root for the docs-gate reachability walk and gives
  future recipes a home.
- `src/engine/templates/CONSTITUTION.md.tmpl` — one Working-agreement bullet
  ("Cross-repo feeds carry a pinned contract") pointing adopters at the recipe
  by canonical URL, mirroring the Program-law rulings-register pointer style.
- `dist/bootstrap.py` — regenerated (`python3 src/build_bootstrap.py`) so the
  byte-pinned single-file artifact matches the edited template
  (`test_committed_bootstrap_is_current` green; byte-pin re-verified clean
  post-commit).
- `tests/test_render.py::test_constitution_carries_pinned_feed_doctrine` —
  asserts the rendered CONSTITUTION carries the anchor string `committed,
  versioned shape contract`.
- `docs/ideas/pinned-feed-contract-doctrine-2026-07-09.md` +
  `docs/ideas/README.md` — idea promoted → shipped (frontmatter
  `state: promoted` / `outcome: shipped` / PR #482; body State reconciled with
  an arrow-chain + a `## Shipped` section so the idea-index body-state-drift
  leg passes; README entry moved Backlog → Shipped).

The template change ships to adopters via the **next kit release**
(release.yml dispatch) — this PR touches no adopter repo (Q-0261.3).

## Verification

- `python3 -m pytest tests/ -q` — 1812 passed, 1 skipped (includes the new
  render test).
- `python3 dist/bootstrap.py check --strict` — exit 0; the only red is the
  designed born-red Session-gate HOLD (cleared by this flip). No enforcing
  findings.
- `python3 src/build_bootstrap.py && git diff --exit-code dist/bootstrap.py`
  — clean post-commit (dist byte-matches templates).

## 💡 Session idea

A `docs/recipes/` graduation could carry a one-line `applies-when:`
frontmatter tag (a cheap structural signature — e.g. "a committed `*.json`
feed + a raw-URL fetch in the same repo") so a future engine check can
*nudge* an adopter that grows a matching seam toward the relevant recipe.
Discovery, not enforcement: the recipe stays a pattern-to-copy, but the kit
gains a way to say "you just grew the shape this recipe is for" instead of
relying on an agent to remember the recipe exists. Deduped against
`docs/ideas/` — no `applies-when` / recipe-discovery idea present.

## ⟲ Previous-session review

The previous work (the needs-planning recipes planning band, PRs #480/#481)
did the right thing by ranking the backlog into buildable-now recipes with an
explicit rank-1 pick — this session inherited a clean, unambiguous target and
spent zero time re-deciding what to build, which is exactly the payoff of a
planning pass that lands a *ranked* list rather than a bag. One concrete
workflow improvement it surfaces: the planning doc named the rank-1 recipe but
not its acceptance-shaped checker constraints (that a `reference` badge is
required because `recipe` is not in the taxonomy; that the idea flip must
reconcile the body State line for the body-state-drift leg). A planning band
that graduates a doc into a *checked* docs tree could carry a one-line
"gates it must satisfy" note per item, so the build session doesn't
rediscover them by red preflight — cheaper than the round-trip.

## Baton

Next rank-2 from the recipes band: the folded-gate advisory checker (S).
