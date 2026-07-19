# R11 — recipes `applies-when:` frontmatter tag

> **Status:** `in-progress`

**What.** Give `docs/recipes/` graduations an `applies-when:` frontmatter tag — a cheap structural signature (a `signal:` phrase + matchable `signatures:`) — so a future engine check can *nudge* an adopter that grows a matching seam toward the relevant recipe. Discovery, not enforcement.

**About to do.** Add the YAML frontmatter schema to `docs/recipes/pinned-feed-contract.md` (the only recipe today), document the convention in `docs/recipes/README.md`, and enforce the schema on the kit's own recipes via a standalone `scripts/check_recipe_frontmatter.py` + `tests/test_check_recipe_frontmatter.py` (a real-repo assertion, so a future untagged recipe reds the kit suite). No dist rebuild — recipes + scripts are not in MODULE_ORDER. Rank R11 from docs/planning/2026-07-19-night-run-idea-groom.md; claim `claude/r11-recipes-applies-when`.

[[fill: enders resolved at flip — 💡 idea · ⟲ prev-session review · ⚑ Self-initiated · 📊 Model]]
