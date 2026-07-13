# 2026-07-13 — announce guard-fire ledger writes during `check`

> **Status:** `complete`

About to happen: make `cmd_check` aggregate its `record_guard_fires()`
return counts and print one summary line when a run appended records to
`.substrate/guard-fires.jsonl` (naming it the telemetry ledger — commit the
delta with your session, do not revert), add the commit-the-delta doctrine
note to `telemetry/README.md`, pin the behavior in tests, regenerate
`dist/bootstrap.py`, and verify with the full pytest suite +
`python3 dist/bootstrap.py check --strict`.

## What happened

- Friction (PR #328 card's ⟲ finding): `check` appends to the TRACKED
  `.substrate/guard-fires.jsonl` silently on every mid-session run (the
  born-red card always trips the session-log guard), so sessions puzzled
  over the dirty tree and `git checkout --`'d the telemetry away.
- Fix chosen: **announce + doctrine** (decide-and-flag, flagged on PR
  #331). `cmd_check` (`src/engine/cli.py`) now sums all ~14 of its
  `record_guard_fires()` call sites into `fires_written` and, when > 0,
  emits one line on every return path (incl. `--status-only`):
  `check: N guard-fire record(s) appended to .substrate/guard-fires.jsonl
  — telemetry ledger; commit the delta with your session (do not revert).`
  Alternatives rejected: gitignore/relocate (design intent is a committed
  ledger — founding plan KF-11; house posture `handoff_pointer.py:22`),
  suppress the write (the fires ARE the B3 datum; dedupe already handles
  echo noise). `cmd_hook`'s choke point deliberately does NOT announce —
  hook output is a noise-sensitive advisory surface with no close-out
  moment.
- Doctrine: `telemetry/README.md` guard-fires section gained a 3-sentence
  committed-ledger note (stage the delta with your close-out, never revert
  it). No template home: nothing under `src/engine/templates/` carries
  guard-fires/telemetry or session-close mechanics, so README only.
- Tests (`tests/test_telemetry.py`): announcement appears exactly once
  with the real written count; absent on an unadopted tree; absent on a
  dedupe-window re-run (tracks ACTUAL writes, not finding counts).
- Verification: `python3 -m pytest` → **1250 passed in 22.83s**;
  `ruff check src/engine/` + repo-scope ruff clean; dist regenerated via
  `python3 src/build_bootstrap.py`, second rebuild byte-identical
  (sha256 808bbc02…); functional repro with this in-progress card:
  `check --strict` printed the new announcement line after the designed
  HOLD banner. This session commits its own guard-fires delta per the new
  doctrine.
- PR #331 opened born-red right after the first commit (76e2f50); claim
  `control/claims/claude-guard-fires-clean-check.md` rode that commit and
  is deleted in the flip commit. Auto-merge deliberately not armed by this
  session.

## Enders

- **📊 Model:** Claude (Fable family) · high · runtime bugfix

💡 **Session idea:** the commit-the-delta doctrine still relies on memory —
`session-close` (the skill/stop-hook close-out path) should explicitly
stage the session's telemetry deltas (`.substrate/guard-fires.jsonl`,
`telemetry/model-usage.jsonl`) as a named checklist step, so the ledger
rides the close-out commit by tooling, not by exhortation (PL-007
enforce-don't-exhort). Dedup'd vs `docs/ideas/`: closest is
`archive-ready-close-out-surface-2026-07-11.md` (archive surface, different
concern); no existing guard-fires/staging entry.

⟲ **Previous-session review (PR #328 heartbeat case fix / #329 ASK
routing):** #328 is a model friction→guard slice — and its ⟲ review is
what surfaced THIS session's fix (it named the guard-fires dirty-tree
puzzle precisely, with the revert it had to do). The gap: that finding
lived only in the card's review prose — it became work because a
coordinator happened to read it. Workflow improvement: a ⟲ review that
names a concrete, fixable friction should also file it (a `docs/ideas/`
seed or an inbox line), so the capture doesn't depend on card readership.
