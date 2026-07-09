# Session 2026-07-09 — Control protocol adoption: land #27 + first status heartbeat

> **Status:** `in-progress`

**Scope (about to do):** land the manager's control-plant PR #27 (it sat
open behind main with no CI runs — the fleet bus was dark on main): merge
origin/main into `manager/control-plant` (trivial, no overlapping files),
push forward-only to the manager's branch (⚑ flagged below), wait for CI
green on the new head, squash-merge. Then run the `control/README.md`
per-session ritual for the first time: read `control/inbox.md` (ORDER 001
P1, ORDER 002 P2), execute by priority, and — as the deliberate LAST step —
overwrite `control/status.md` with the real picture. One-line protocol
notes in `docs/current-state.md` + `.session-journal.md`. No engine code,
no `bench/` pin paths, no release files (a parallel session is cutting
v1.1.0 in PR #29 — its files are avoided entirely).
