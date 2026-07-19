# S8 — signature-honesty lint for `applies-when:` tokens

> **Status:** `in-progress`

**Session:** 2026-07-19 · Self Improvement work-loop · substrate-kit
**Baton:** wave-2 groom rank S8 (docs/planning/2026-07-19-night-run-idea-groom-wave2.md) — "signature-honesty lint for applies-when: tokens — cross-check tokens against recipe body." Provenance: fm ORDER 048 standing grant + coordinator dispatch (S7 shipped #524; baton advanced to S8).

## What I'm about to do

R11 (#506) gave every `docs/recipes/` graduation a well-formed `> **applies-when:** \`<signature>\`` badge (`path:<glob>` / `content:<marker>` tokens) and `check_recipe_applies_when` warns when the badge is missing/empty/malformed — a WELL-FORMEDNESS lint. S8 adds the complementary HONESTY lint: cross-check each token against the recipe's own body, so a signature that names a signal the recipe never actually documents (a drifted/dishonest token) surfaces as an advisory. New advisory checker `check_recipe_signature_honesty.py` on the `posture="advisory"` seam (input-gated, fail-open, off STRICT_SUBCHECKS), mirroring its R11 sibling; ships in dist → rebuilt + byte-pinned.

<!-- born-red HOLD: this card opens the PR red via the session-gate until it is flipped `complete` as the deliberate last step. -->
