# 2026-07-14 — check_idea_index merged-reality leg (grace-windowed git truth)

> **Status:** `in-progress`

About to (opening declaration): build the `check_idea_index.py`
merged-reality leg from PR #349's session-idea ender (ranked #2 in the
Night-12 triage) — cross-check shipped-idea frontmatter (`shipped_pr`,
`merged_date`, optional `merged_sha`) against actual local git history
(no GitHub API), with a grace window so ideas whose shipping PR is still
in flight never false-red, graceful self-skip on shallow/gitless trees,
plus the four-case mutation test arc.

- **📊 Model:** Claude (Fable family)

Run type: worker session (BUILD phase, coordinator-dispatched).
