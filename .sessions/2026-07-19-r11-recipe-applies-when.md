# R11 — recipe applies-when: structural-signature tag

> **Status:** `complete`

**Session:** 2026-07-19 · Self Improvement work-loop · substrate-kit
**Baton:** R11 (recipes `applies-when:` frontmatter tag) from docs/planning/2026-07-19-night-run-idea-groom.md — taken after a sibling claimed R10 (PR #505).

**About to do:** give graduated recipes a machine-readable `applies-when:` structural signature + an advisory check that every graduation carries a well-formed one.

- **📊 Model:** Opus 4.8 · medium · feature build (recipe applies-when structural-signature tag + advisory check_recipe_applies_when)
- **⚑ Self-initiated:** R11 is baton work — a sibling claimed R10 (PR #505), so I took R11, the next unclaimed rung. Decide-and-flag calls: (1) shipped the tag as a blockquote BADGE line, not top-of-file `--- … ---` YAML, to avoid introducing the engine's first frontmatter parser (the kit is deliberately PyYAML-free); (2) deferred the adopter-nudge discovery check to a later rung — it needs a 2nd recipe with a signature first, per the recipe's own escalation rule; (3) defined the `applies-when:` value grammar (comma-separated `path:<glob>` / `content:<marker>` tokens). Also self-caught + fixed an invalid-escape backtick sequence I had introduced in the checker's docstring/messages.

## What shipped (PR #506)

Gave `docs/recipes/` graduations a machine-readable `applies-when:` structural signature so a FUTURE discovery check can nudge an adopter that grows a matching seam toward the relevant recipe — discovery, not enforcement. Three parts: (1) a `> **applies-when:** \`content:raw.githubusercontent.com, path:*.json\`` badge on the one existing recipe (`docs/recipes/pinned-feed-contract.md`); (2) the field's grammar documented in `docs/recipes/README.md` (comma-separated `path:<glob>` / `content:<marker>` tokens); (3) `src/engine/checks/check_recipe_applies_when.py`, an advisory (warn-only, never exit-affecting) check that flags any graduation with a missing/empty/malformed tag, wired on the `posture="advisory"` seam (mirroring R7), added to `MODULE_ORDER`, dist rebuilt byte-pin clean.

Files: `src/engine/checks/check_recipe_applies_when.py` (new), `src/engine/cli.py`, `src/build_bootstrap.py`, `dist/bootstrap.py` (rebuilt), `docs/recipes/pinned-feed-contract.md`, `docs/recipes/README.md`, `tests/test_check_recipe_applies_when.py` (8 tests incl. a `test_not_in_strict_subchecks` negative).

Evidence: full suite **1881 passed / 1 skipped**; `dist/bootstrap.py check --strict` exit 0 (aside from the by-design born-red hold, cleared by this flip); byte-pin `tests/test_bootstrap.py` green; the advisory is silent on the kit's own now-tagged recipe; the checker compiles clean under `-W error::DeprecationWarning` after the escape fix.

## 💡 Session idea

**A signature-honesty lint for `applies-when:` tokens.** R11's advisory verifies a recipe *carries* a well-formed tag, but not that its tokens point at anything real — a typo'd `path:*.jsonn` glob or a `content:` marker that appears nowhere would silently match nothing when the future nudge check runs, which is worse than no signature (a false "no adopter matches"). A small, additive follow-on: cross-check each recipe's `applies-when:` tokens against the recipe's own body (its "When this applies" / estate-proof prose) and warn when a token references a path/marker that appears nowhere in the recipe — keeping the structural signature honest to the recipe it annotates. Deduped: grepped the groom doc + docs/ideas for `applies-when` / `signature` / `recipe` — R12 is folded-gate remediation, R13 is the PL-004 task-class gate; none touch signature validation. Distinct.

## ⟲ Previous-session review

Previous session — **R10 harness --freeze self-citing reproduce block (PR #505, sibling)**. Did well — and notably fixed the exact failure R8 exhibited two rungs earlier: its heartbeat was *complete and consistent* (This wake / Recently-shipped / PR-state / baton all advanced to R10 together), so this session had no drift to reconcile — a clean contrast to R8's mid-flight partial. One thing worth a look: per its claim summary R10 hashes the *exact output bytes* (sha256 of the emitted artifact). Because the payload bakes a wall-clock `generated` timestamp, that sha changes on every run — so the "self-citing reproduce" command can verify *this* artifact's integrity but can never be re-run to reproduce the same hash. A content-hash computed over the payload with `generated` excluded would make "re-run → same hash" actually hold (the reproduce block becomes verifiable, not just an integrity stamp). Concrete system/workflow improvement: a "reproduce block" is only as strong as its determinism — worth a follow-on that adds a stable content-digest alongside the byte-hash, so self-citation is genuinely re-runnable.
