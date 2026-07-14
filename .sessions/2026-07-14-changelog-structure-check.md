# 2026-07-14 — CHANGELOG `[Unreleased]` structure checker

> **Status:** `in-progress`

About to (opening declaration): build
`docs/ideas/changelog-unreleased-structure-checker-2026-07-09.md` — a
kit-repo-only checker `scripts/check_changelog_structure.py` (stdlib) that
validates the `[Unreleased]` section's keep-a-changelog shape (known
headings only, each at most once, canonical order, no bullet before the
first heading, prose/KF-5 blocks in the preamble only), wired as a
`ci.yml` kit-quality step next to `check_idea_index.py`, with a mutation
test arc — so release cuts stop hand-reordering the section.

- **📊 Model:** Claude 5 family

Run type: worker session (BUILD phase, coordinator-dispatched).
