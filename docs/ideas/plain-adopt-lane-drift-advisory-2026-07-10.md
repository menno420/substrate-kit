---
state: captured
origin: lab
shipped_pr: null
shipped_repo: null
merged_date: null
outcome: open
---

# Plain-adopt lane-drift advisory — nudge `--lane` in lane-shaped repos (2026-07-10)

> **Status:** `ideas`
>
> **State:** captured (filed by the 2026-07-10 night-cap groom from the
> `adopt --lane` session's card-only 💡 idea —
> `.sessions/2026-07-10-adopt-lane.md`; queue item 11 / PR #103 shipped the
> lane-aware adopt itself, this is its inverse gap).

## The gap

`adopt --lane <name>` (PR #103) makes a second Project joining a SHARED
repo one command: the heartbeat plants as `control/status-<lane>.md` and is
declared in `substrate.config.json` → `heartbeat_files`. But the inverse
path is still open: a **plain** `adopt` (no `--lane`) into a repo whose
`heartbeat_files` already names lane files plants the singular
`control/status.md` seed **without declaring it** — the file exists on disk
but no gate validates it. That is exactly the half-declared state the
ORDER 004 fail-safe (empty list expands to the default) exists to prevent,
recreated by the one hand-path left into the bus.

## The fix shape

A one-line advisory in `adopt` when `heartbeat_files` ≠ the untouched
default AND `--lane` is absent:

```
adopt: this repo is lane-shaped (heartbeat_files: [...]) — did you mean `adopt --lane <name>`?
```

Advisory-only (never refuses — a deliberate singular adopt into a
lane-shaped repo may be intended, e.g. a consolidating Project), printed
before any write so the operator can abort. Optionally the same nudge as a
`check` finding when a singular `control/status.md` exists but is absent
from a non-default `heartbeat_files` (the drift may predate the kit).

## Guard recipe

- Function: the advisory branch in `adopt()` (`src/engine/adopt.py`),
  keyed off `load_config().heartbeat_files` vs `DEFAULT_HEARTBEAT_FILES`.
- Tests (`tests/test_adopt.py`, mirroring the #103 nine): lane-shaped repo
  + plain adopt → advisory printed, files still planted (advisory, not
  refusal); default-shaped repo + plain adopt → no advisory; lane adopt →
  no advisory.
- Ordinary lane: engine change → dist regen + byte-pin; MINOR-adjacent
  (advisory text only) → CHANGELOG `### Fixed` or `### Added` one-liner.

## Next

A groomed-ideas increment ships advisory + tests (small, contained,
ordinary lane — quick-win shaped).
