---
state: captured
origin: consumer:menno420/superbot-next
shipped_pr: null
shipped_repo: null
merged_date: null
outcome: open
---

# Folded-gate hosts need the PR-diff-aware card selection too (2026-07-11)

> **Status:** `ideas`
>
> **State:** captured. **Origin:** consumer — superbot-next, live-verified
> during the v1.9.0 distribution wave.

## The finding

superbot-next does not run the kit's standalone `substrate-gate.yml`: it
FOLDED the session gate into its own CI as a `gate` job. That hand-folded
copy predates the PR-diff-aware card selection (`check --session-log
<file>` derived from the PR's diff, kit PR #19 / the generated gate's
current shape) — it still grades the **newest-by-mtime** card. In CI a
fresh checkout flattens every mtime, so during the wave the folded job
graded a SIBLING session's `complete` card while the PR's own card was
in-progress: a misgrade in the loosening direction (the same class the
diff-aware selection fixed everywhere else).

## Why this is not a kit-template fix

The folded workflow is host-authored and host-owned — it is not
`substrate-gate.yml`, so the kit-owned regen (adopt step 6b) never touches
it, and no kit template renders it (verified: no folded-gate artifact
exists in `src/engine/`; the kit's own `ci.yml` and the generated gate are
both already diff-aware). The v1.9.0-wave fixes slice therefore documents
the fix rather than shipping it kit-side.

## The fix superbot-next's lane should apply

Port the generated gate's card-derivation block into the folded `gate`
job: derive `card` from `git diff --name-only --diff-filter=d
"$range" -- '.sessions/*.md' ':!.sessions/README.md' | tail -1` and pass
it via `--session-log "$card"` (added-card diffs via `--added-card` —
which, since the wave-fixes slice, HOLDs an in-progress added card
instead of exempting it). The kit repo's own `.github/workflows/ci.yml`
session-gate step is the copyable reference.

## Kit-side option (if the class recurs)

If more hosts fold the gate, consider a `check` advisory that detects a
workflow grading sessions without `--session-log` (grep for a
`check --strict --require-session-log` invocation lacking the flag in
`.github/workflows/*.yml`) — enforce-don't-exhort, but only worth building
on a second occurrence.
