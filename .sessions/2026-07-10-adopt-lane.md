# 2026-07-10 — gen-2: `adopt --lane` — lane-aware adoption for shared repos (queue item 11)

> **Status:** `in-progress`

**Scope (about to do):** build queue item 11 — `adopt --lane <name>`: turn the
documented multi-Project per-lane heartbeat pattern (control/README.md § Multi-Project
repos) into a one-command shape. Plant `control/status-<lane>.md` from the status
template (skip-if-exists), append the lane's heartbeat file to
`Config.heartbeat_files` via `save_config` (idempotent, never duplicating), leave
`inbox.md`/`README.md` single — the self-review G1 fix for double-adoption (the
`.sessions/2026-07-09-order004.md` 💡 idea). Tests in the existing test_adopt.py
style; dist regenerated + byte-pinned. Claimed via #102
(`claimed-by: queue-item-11-adopt-lane kit-lab-gen2 2026-07-10T04:40:47Z`). No pin
paths; `control/` writes only in the claim (#102) and the final status close.
