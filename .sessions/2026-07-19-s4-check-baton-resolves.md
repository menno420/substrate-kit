# S4 — check_baton_resolves advisory

> **Status:** `in-progress`

**Session:** 2026-07-19 · Self Improvement work-loop · substrate-kit
**Baton:** wave-2 groom rank S4 (docs/planning/2026-07-19-night-run-idea-groom-wave2.md, #515) — a `check_baton_resolves` advisory that verifies every `## Next-2 baton` entry in `control/status*.md` names a real resolvable path/anchor. Provenance: fm ORDER 048 standing grant + coordinator dispatch.

**About to do:** add `src/engine/checks/check_baton_resolves.py` — an advisory (warn-only, off STRICT_SUBCHECKS) that parses the `## Next-2 baton` section of each `control/status*.md`, extracts the repo-relative path/anchor references it cites, and warns for any that no longer resolve on disk; wire it on the `posture="advisory"` seam in `cli.py`, add it to `MODULE_ORDER`, rebuild + byte-pin `dist/bootstrap.py`, and ship both-directions tests. Hold the PR red until the checker + tests + verify land.

- **📊 Model:** opus-4.8 · medium · feature build
