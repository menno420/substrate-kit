# Session · 2026-07-18 · kit-release-v1.19.0

> **Status:** `in-progress`

Intent: cut the substrate-kit **v1.19.0** release — the born-red version-bump
PR that stamps the three version homes to 1.19.0, transforms CHANGELOG
`[Unreleased]` → `[1.19.0] - 2026-07-18`, and rebuilds the pinned
`dist/bootstrap.py`. Publish (tag + GitHub Release via `release.yml`
`workflow_dispatch`) is a later step, NOT this PR.

- **📊 Model:** Opus 4.8 · high · release cut
- ⚑ Self-initiated: no — owner-directed release cut.

About to: cut substrate-kit v1.19.0 — reconcile CHANGELOG `[Unreleased]`
completeness against the merges since v1.18.0 (fold in #455/#457/#459 +
the already-listed #444–#450 / #426 / #424 / #420–#422 / #414), run
`scripts/cut_release.py 1.19.0 --write` (three version homes +
CHANGELOG transform), regenerate `dist/bootstrap.py` via
`src/build_bootstrap.py`, verify locally per the release runbook, and open
the born-red bump PR. This card holds the PR red until a deliberate final
flip (which this session does NOT perform — the PR is left born-red per
the owner's instruction).

Scope: `CHANGELOG.md` · `src/engine/lib/config.py` · `pyproject.toml` ·
`substrate.config.json` · `dist/bootstrap.py` · this card ·
`control/claims/release-v1-19-0.md`.
