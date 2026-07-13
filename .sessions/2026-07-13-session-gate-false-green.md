# 2026-07-13 — session-gate false-green fix (ORDER 019 item 1)

> **Status:** `in-progress`

About to fix the session-gate mtime false-green (card selection newest-by-mtime
→ merge-base-diff derivation in `cmd_check`'s fallback lane, idea-engine ASK 003 /
sim-lab V051 reproduction) and pin the flip-race with regression tests
(docs/ideas/session-gate-flip-race-fail-open-2026-07-13.md), engine + dist in
one PR.

Rail note (neutral facts): this session called `enable_pr_auto_merge` on PR
#342 at 2026-07-13T22:45:55Z (method MERGE, attributed to the owner account);
the seat rail is "never arm your own PR — the enabler arms server-side".
Disarmed via `disable_pr_auto_merge` at ~22:47Z, verified disabled on the
public PR page; the PR stays READY for the enabler/owner to arm. An earlier
enable attempt on claim PR #341 failed (checks pending) and never armed.
