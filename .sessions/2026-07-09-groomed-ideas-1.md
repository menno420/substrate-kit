# Session 2026-07-09 — groomed-ideas-1: post-band idea increment

> **Status:** `in-progress`

**About to do (groomed from recent session cards, best value/size first):**

1. **PR-diff-aware session-card selection** (💡 from the kl1-ci-delta card):
   `check --session-log <file>` in the engine; the kit's own `ci.yml` and the
   planted `substrate-gate.yml` pass the card the PR's diff touches instead of
   relying on newest-by-mtime + the CI mtime-restore shim. Fail-open,
   backward-compatible (no argument → mtime selection unchanged).
2. **Reflection-miner line-start markers** (kl5-era observation): the miner
   currently harvests mid-prose 💡/⚑ fragments ("see 💡 below…") as junk
   lessons; tighten passes 1–2 to marker-led lines with a regression test.
3. **Guard-recipe convention in session cards** (⟲ improvement from the
   kl1-ci-delta review): friction→guard entries carry a one-line recipe
   (function + file + test anchors) so the next session lands the guard
   without re-deriving it by grep. Convention text in both `.sessions/README`s.

Plus the B4 ledger exercise: each shipped idea gets a `docs/ideas/` entry with
outcome frontmatter. Avoids all PR #17 files (bench/, its card, its
current-state hunks).

- **📊 Model:** fable-5 · high · kernel/architecture design
