# 2026-07-14 — ORDER 022: stop-hook merged-head final-push guard

> **Status:** `in-progress`

About to (opening declaration): execute inbox ORDER 022 — guard the kit
stop-hook session-close final-push path so a session whose branch head is
already merged to origin/main (after a fetch) is loudly told to SKIP the
final push instead of silently re-creating the branch GitHub just deleted
(PROPOSAL 003 + ADDENDUM: primary cause is GitHub-side auto-delete not
firing for bot-merged PRs; this closes the proven secondary re-creation
path). Fail-open on unprovable ancestry (shallow clone / failed fetch):
push proceeds with a NOTE. Engine-shipped port of the scripts/_git_truth.py
ancestry primitive (parity-pinned), new `_stop_push_guard` advisory in
`evaluate_stop`, tests for all three decision branches + mutation-tested,
dist regenerated.

- **📊 Model:** Claude Fable 5 · high · feature build

Run type: worker session (coordinator-dispatched, ORDER 022).
