# 2026-07-14 — ORDER 019 item 4: auto-merge-enabler INSTALL-time preflight

> **Status:** `in-progress`

About to: ship the install-time half of the enabler preflight
(`docs/ideas/enabler-install-preflight-2026-07-13.md`) — at adopt/upgrade
time, when the live enabler is planted/regenerated, best-effort verify the
owner-UI preconditions that leave it silently INERT ("Allow auto-merge" OFF,
zero required status-check contexts, required-context name mismatch) and
surface them as advisory report lines, degrading gracefully offline/tokenless.
The check-time branch-drift half shipped in PR #321 and is not duplicated.
