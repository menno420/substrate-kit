# R11 — recipe `applies-when:` structural-signature tag + advisory

> **Status:** `in-progress`

**Session:** 2026-07-19 · Self Improvement work-loop · substrate-kit
**Baton:** R11 (recipe `applies-when:` tag + advisory) from docs/planning/2026-07-19-night-run-idea-groom.md — fm ORDER 048.

**About to do:** give each docs/recipes/ graduation a machine-readable `applies-when:` structural-signature badge, document the schema in docs/recipes/README.md, and ship an advisory `check_recipe_applies_when.py` (warn-only, posture="advisory" seam) that keeps every graduation carrying a well-formed tag.

- **📊 Model:** Opus 4.8 · medium · feature build (recipe applies-when: badge + advisory check + tag on the real recipe + schema doc)
- **⚑ Self-initiated:** R11 is baton work (fm ORDER 048). Decide-and-flag calls within it: (1) the tag rides as a `> **applies-when:** \`...\`` blockquote badge (mirroring the existing `Status:` badge), NOT a top-of-file `--- ... ---` YAML block — the kit engine is deliberately PyYAML-free / has no frontmatter parser, so the badge-line form reuses the proven Status-badge regex with zero new parsing machinery; (2) the adopter-nudge discovery check is deferred until a 2nd recipe carries a signature (the recipe's own escalation rule — don't pre-build a check for a single instance); R11 ships only the tag + a well-formedness readout.

## What shipped (PR #[[fill: PR number]])

[[fill: what shipped summary]]

## 💡 Session idea

[[fill: session idea]]

## ⟲ Previous-session review

[[fill: previous-session review]]
