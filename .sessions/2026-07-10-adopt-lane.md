# 2026-07-10 — gen-2: `adopt --lane` — lane-aware adoption for shared repos (queue item 11)

> **Status:** `complete`

- **📊 Model:** model identity withheld (harness policy) · high · feature-build
  (one scoped engine PR: the lane-aware adopt scaffold)

## Scope (as declared)

Build queue item 11 — `adopt --lane <name>`: turn the documented multi-Project
per-lane heartbeat pattern (control/README.md § Multi-Project repos) into a
one-command shape — the self-review G1 fix for double-adoption (the
`.sessions/2026-07-09-order004.md` 💡 idea; checker shipped v1.4.0/ORDER 004,
this is the scaffold half of the enforce-don't-exhort arc). Claimed via #102
(`claimed-by: queue-item-11-adopt-lane kit-lab-gen2 2026-07-10T04:40:47Z`). No
pin paths; `control/` writes only in the claim (#102), one README doc line
(below), and the final status close.

## What shipped

1. **`adopt --lane <name>`** (`src/engine/adopt.py` + `cli.py`): with `--lane`,
   the `control-status.md.tmpl` dest is parametrized to
   `control/status-<lane>.md` — the singular `control/status.md` is never
   created (nor touched) by a lane adopt; `inbox.md`/`README.md` stay single
   and skip-if-exists. The planted lane heartbeat gets its provenance hash
   recorded under its own relpath (upgrade-diff contract §4.3 unchanged).
2. **`heartbeat_files` registration** (`_register_lane_heartbeat`), all
   idempotent: already-listed → no-op reported; list is the untouched default
   AND no Project owns the singular file (lane-shaped from the start) →
   the lane REPLACES the default entry (the gate must not hold strict RED on
   a heartbeat no lane owns); otherwise → APPEND, never dropping a sibling
   lane. Empty list expands to the default first (misconfiguration never
   silently disables the gate — the ORDER 004 instinct). Persisted via
   `save_config` in the same pass that records `kit_version`; config is
   mutated in place so `cmd_adopt`'s engagement checklist gates the lane
   file in the same run (verified live: the checklist's
   `status-no-heartbeat` finding names `control/status-mining.md`).
3. **Lane-name validation before any write** (`validate_lane_name`,
   `[A-Za-z0-9][A-Za-z0-9_-]*`): a lane name becomes a path component and a
   config entry, so `../evil`, separators, dots, and leading `-`/`.` refuse
   the whole adopt — `adopt: REFUSED — invalid lane name …`, exit 2 (the
   `UnsafeTargetError` posture).
4. **The planted contract advertises the command**: one bullet added to the
   Multi-Project section of `control-README.md.tmpl` (+ this repo's local
   `control/README.md` copy, the ORDER 003/004 precedent) — a second Project
   reads ONE command instead of three hand-edits.
5. **Tests**: 813 total (804 → 813; 9 new in `tests/test_adopt.py` mirroring
   the existing style): lane plant + no singular, join-existing-install
   (append), idempotent re-adopt (kept + no duplicate entry), two-lane
   sequence never drops a sibling, doc-hash under the lane relpath + no
   phantom singular hash, honest seed (no parseable heartbeat), 7-case
   unsafe-name refusal with nothing written, `cmd_adopt` end-to-end +
   refusal exit code, planted-README one-command line.
6. **CHANGELOG `[Unreleased]` ### Added** entry (MINOR: new capability on an
   existing command); dist regenerated + byte-pinned.

Field verification (scratchpad, real dist CLI): fresh repo `adopt --lane
mining` → `heartbeat_files ['control/status-mining.md']`, no singular file;
second `adopt --lane exploration` → both lanes listed, shared bus `kept:`;
`adopt --lane ../evil` → REFUSED exit 2.

## Gates (final head)

- `python3 -m pytest tests/ -q` → **813 passed**
- `python3 dist/bootstrap.py check --strict` → exit 0 (after this card flip;
  the pre-flip red was the born-red session gate itself, as designed)
- `python3 src/build_bootstrap.py && git diff --exit-code dist/bootstrap.py` →
  byte-pin green
- `python3 -m ruff check src/engine/` (CI's exact scope) → all checks passed

## Run report

### ⚑ Flags

1. **⚑ Self-initiated: none beyond scope** — queue item 11 was the claimed
   scope; the README/tmpl doc line and the local `control/README.md` mirror
   are the shipped feature's documentation half (ORDER 003/004 precedent).
2. **⚑ Replace-vs-append rule disclosed:** a lane adopt into a repo whose
   `heartbeat_files` is still the untouched default replaces that default
   only when `control/status.md` does not exist on disk; every other case
   appends. Deliberate: replacing while a first Project actually beats on
   the singular file would silently un-gate it.

### 💡 Session idea (dedup-checked against docs/ideas/ + roadmap)

**Plain-adopt lane-drift advisory.** The inverse gap of this feature: a PLAIN
`adopt` (no `--lane`) into a repo whose `heartbeat_files` already names lane
files plants the singular `control/status.md` seed WITHOUT declaring it —
the file exists but no gate validates it, the exact half-declared state the
ORDER 004 fail-safe exists to prevent. A one-line advisory in adopt ("this
repo is lane-shaped — did you mean `adopt --lane <name>`?") when
`heartbeat_files` ≠ default and `--lane` is absent would close the last
hand-edit path into the bus. No existing `docs/ideas/` file covers it.

### ⟲ Previous-session review (`.sessions/2026-07-10-pr92-adopt-owner-actions-xref.md`)

Genuinely strong: adopting the orphaned #92 through the claim ritual
(`pr92-adopt` as a claim scope) turned a stranded READY+green PR into merged
work with zero re-derivation, and the union-merge of the twice-restructured
ideas README was resolved coherently rather than by picking a side; the
mid-flight #99 token alignment (re-syncing the new checker to a sibling PR
that landed while it was open) is exactly the parallel-lane discipline the
bus is for. What it could have done better: its 💡 idea (CAPABILITIES
append-log format advisory) was left card-only — not filed into
`docs/ideas/`, which is where the grooming pass looks; an unfiled idea risks
becoming the orphan class its own session was busy rescuing. **Workflow
improvement:** the session-close drift question should include "is this
card's 💡 idea reachable from `docs/ideas/`?" — one line in the close ritual
turns card-only ideas into filed ones (or an explicit in-card "deliberately
card-only" note), keeping the grooming surface complete.

### Docs audit

Everything in a durable home: feature + tests in engine/tests (dist
byte-pinned); release note → CHANGELOG `[Unreleased]` ### Added; the planted
contract documents the command (tmpl + local README mirror); provenance →
this card + the `adopt()` docstring (G1 + the order004 card idea are named).
`docs/gen2/queue-state.md` untouched per the gen-2 convention (#95 card
documents why); the status close records the ship on the bus and clears the
#102 claim. No pin paths, no `control/inbox.md`.
