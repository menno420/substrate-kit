# 2026-07-13 — session-gate false-green fix (ORDER 019 item 1)

> **Status:** `in-progress`

About to fix the session-gate mtime false-green (card selection newest-by-mtime
→ merge-base-diff derivation in `cmd_check`'s fallback lane, idea-engine ASK 003 /
sim-lab V051 reproduction) and pin the flip-race with regression tests
(docs/ideas/session-gate-flip-race-fail-open-2026-07-13.md), engine + dist in
one PR.
