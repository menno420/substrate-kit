# 2026-07-15 · adopt-lane-drift-advisory

> **Status:** `in-progress`

About to: build the baton-named idea
docs/ideas/plain-adopt-lane-drift-advisory-2026-07-10.md — a one-line
advisory in `adopt` when a plain (no `--lane`) adopt targets a repo whose
`heartbeat_files` is already lane-shaped (non-default), so the operator is
nudged toward `adopt --lane <name>` instead of silently planting an
undeclared singular `control/status.md`. Advisory only, never a refusal.
Engine change + tests + dist byte-pin regen + CHANGELOG + idea lifecycle
flip, one PR.
