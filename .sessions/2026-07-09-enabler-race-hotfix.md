# Session 2026-07-09 — enabler label-race hotfix (the #22 incident guard)

> **Status:** `in-progress`

**Scope (incident-driven hotfix):** deploy PR #17's fresh-label re-read
guard into `.github/workflows/auto-merge-enabler.yml` on main NOW — the
`do-not-automerge` gate was defeated live today when PR #22 (PL-010,
discuss-first program law) auto-merged mechanically: main's enabler checks
the label only via its job-level `if:` on the **stale PR-open event
payload**, the label landed +7 s after open, and a ~12-min runner-queue lag
armed auto-merge long after the label existed (incident comment on #22).
The guard exists but only inside unmerged, owner-gated PR #17 — this PR
extracts exactly that hunk (byte-identical) so it is live for the very next
labelled PR, and #17's eventual merge conflict on this file resolves
trivially/identically. Also fixes the post-#22 prose staleness on main
(`docs/current-state.md` owner gate 2 + the idea file's B4 frontmatter
still describe #22 as open/awaiting blessing).
