# R6 — check --explain-wall / --why

> **Status:** `in-progress`

**Session:** 2026-07-19 · Self Improvement work-loop · substrate-kit
**Baton:** R6 (check --explain-wall / --why) from docs/planning/2026-07-19-night-run-idea-groom.md

## What I'm about to do

Add `bootstrap.py check --explain-wall <phrase>` (alias `--why`): a CLI lookup
that runs the false-wall blocklist matcher, reports which rule matched, prints a
one-line ground-truth correction for that rule, and points at the
`docs/CAPABILITIES.md` dated-append-row form for recording a genuine momentary
refusal.

Implementation: a per-rule `WALL_CORRECTIONS` map + `explain_wall()` helper +
`all_rule_names()` coverage surface in `src/engine/checks/check_no_false_walls.py`;
a `--explain-wall`/`--why` flag and an early-return lookup branch in
`src/engine/cli.py`; rebuild `dist/bootstrap.py` (byte-pin clean); mirrored test
`tests/test_explain_wall.py`. A lookup, never a gate — always exits 0; touches
neither `_extra_check_findings` nor `STRICT_SUBCHECKS`.

The close-out enders (💡 idea, 📊 Model line, ⟲ previous-session review,
⚑ Self-initiated line) are filled at flip, when the Status badge flips to
`complete`.
