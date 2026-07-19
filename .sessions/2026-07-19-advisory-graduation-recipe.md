# S2 — advisory→born-red-gate graduation recipe

> **Status:** `complete`

**Session:** 2026-07-19 · Self Improvement work-loop · substrate-kit
**Baton:** wave-2 groom rank S2 (docs/planning/2026-07-19-night-run-idea-groom-wave2.md, #515) — graduate the advisory→born-red-gate pattern that #512/#513/#514 followed into a docs/recipes/ recipe. Provenance: fm ORDER 048 standing grant + coordinator dispatch.

**About to do:** add docs/recipes/advisory-to-born-red-gate.md (+ README index bullet) documenting the graduate-on-repeat-leak / own-card scoping / fail-open / underscore-helper / mutation-test discipline; hold the PR red until the recipe + verify land.

## What shipped

Added `docs/recipes/advisory-to-born-red-gate.md` — a portable recipe teaching when and how to promote a warn-only advisory check into an exit-affecting born-red merge gate, drawn from the `📊 Model:` line exit-gate trilogy (#512 task-class, #513 exact-model-ID, #514 effort) and their advisory precedents (#495/#498/#500). Indexed in `docs/recipes/README.md`. Carries the `applies-when:` badge per the R11 convention (advisory-checked by `check_recipe_applies_when`). Docs-only; no engine change, no dist rebuild.

Teaches five parts: (1) graduate on a *repeat* real leak, never the first sighting — the advisory is the probation; (2) scope the gate to the PR's OWN added card so it can never retroactively redden an existing/merged card across the fleet (the not-a-fleet-bomb discipline); (3) fail open on any artifact you did not come to grade; (4) add exit-affecting behavior via a leading-underscore helper called outside `_extra_check_findings`, so the STRICT_SUBCHECKS parity floor stays untouched; (5) mutation-test both directions (a mutated segment reds, the held-constant card stays green) and pin the fail-open. Plus the cold-adoption smoke as the fleet-wide safety net.

- **📊 Model:** opus-4.8 · medium · docs-only
- **⚑ Self-initiated:** NOT self-initiated — built from wave-2 groom rank S2 per fm ORDER 048 standing grant + coordinator dispatch. Decide-and-flag calls: (1) filename `advisory-to-born-red-gate.md` (kebab-case, names the pattern); (2) applies-when signature `content:posture="advisory", content:check_added_card` — the two structural markers a repo grows when it has advisory checks + a born-red added-card gate; (3) task-class `docs-only` — pure recipe + index, no engine/dist change.
- **💡 Session idea:** a `check_recipe_estate_proof` advisory — verify every `docs/recipes/*.md` `## Estate reference` section cites at least one `#NNN` PR. The recipes/ contract is "graduated from the estate"; a recipe with no PR proof is a pattern nobody has actually shipped. Cheap regex, advisory-only, input-gated on `docs/recipes/` like `check_recipe_applies_when`. Deduped against groom ladder S2–S16 and docs/ideas/ — distinct from S3/S4.
- **⟲ Previous-session review:** #515 (wave-2 groom + baton retarget) left an unambiguous ranked buildable-now ladder and pointed the status baton straight at S2 — exactly the handoff that let this session start building without re-deciding scope. Miss: the groom ranked S2 as "carrying R11's applies-when: badge" but did not pre-pick the signature tokens, leaving that decision to the build. System improvement surfaced: with this recipe `docs/recipes/` now carries **2** signed recipes, so the README's "nudge deferred until >=2 recipes carry signatures" threshold is now met — the deferred applies-when discovery check is buildable and should enter the ladder as a fresh S-rank.
