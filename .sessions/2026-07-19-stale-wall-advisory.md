# Session · 2026-07-19 · stale-wall-advisory

> **Status:** `complete`

Intent: task R5 under the night-run groom (`docs/planning/2026-07-19-night-run-idea-groom.md`
R5 entry) — add an ADVISORY-only engine check `src/engine/checks/check_stale_walls.py`
that surfaces any `wall` ledger row in `docs/CAPABILITIES.md` whose verification date is
older than the staleness window (`cadence.staleness_days`, default 14). It is the
enforcement analogue of the DISCOVERY RULE's staleness step — warn-only, NEVER exit-affecting.

- **📊 Model:** Opus 4.8 · high · feature build
- ⚑ Self-initiated: none — R5 is baton-directed work (dispatched from the night-run groom
  R5 entry), not self-initiated.

About to: mirror `check_folded_gate` — create the advisory check + `FINDING_KIND =
"stale-wall"`, wire it on the `posture="advisory"` seam in `cmd_check` (NOT
`_extra_check_findings`, which is exit-affecting — deviation from the recipe to honor
"advisory, not red"), add `checks/check_stale_walls.py` to `MODULE_ORDER` in
`src/build_bootstrap.py`, rebuild `dist/bootstrap.py`, and add
`tests/test_check_stale_walls.py` mirroring `tests/test_check_folded_gate.py` (incl.
`test_not_in_strict_subchecks`). Born-red card holds the PR on the Session-gate HOLD; flips
to `complete` last.

## What shipped (PR #495)

- **`src/engine/checks/check_stale_walls.py`** (new, ~240 lines, stdlib-only) — an
  input-gated, fail-open ADVISORY check: it parses each `wall` row in
  `docs/CAPABILITIES.md`, and for any row whose verification date is older than
  `cadence.staleness_days` (default 14) emits one advisory finding. Warn-only —
  **never** exit-affecting — mirroring the `check_folded_gate` shape.
- **Wired on the `posture="advisory"` seam in `src/engine/cli.py`** (`cmd_check`, +30
  lines), deliberately **NOT** `_extra_check_findings` (which is exit-affecting) so
  the "advisory, not red" contract holds. Kept **off** `STRICT_SUBCHECKS`.
- **`checks/check_stale_walls.py` added to `MODULE_ORDER`** in
  `src/build_bootstrap.py` (+5) and **`dist/bootstrap.py` rebuilt** (byte-pin clean).
- **`tests/test_check_stale_walls.py`** (new, ~187 lines) mirrors
  `tests/test_check_folded_gate.py`, incl. `test_not_in_strict_subchecks`.
- Decide-and-flag calls: (1) wired on the advisory seam, not the exit-affecting
  `_extra_check_findings` the recipe named, to honor "advisory, not red"; (2) named
  the constant **`STALE_WALL_KIND`** (not the recipe's `FINDING_KIND`) to avoid a
  single-file constant collision with `check_folded_gate` once the dist is bundled;
  (3) the check **deliberately skips `wall` rows with no parseable date** — out of
  R5 scope, seeded as this wake's session idea below.

## Verification

- `python3 -m pytest tests/ -q` → **1843 passed, 1 skipped** (full suite green).
- `python3 dist/bootstrap.py check --strict` → red ONLY by the born-red HOLD
  (in-progress card + missing enders); clears to green once this card flips
  `complete`. Local `check --strict` self-reported exit 0 with the HOLD as an
  advisory NOTE; the CI `kit-quality` job runs it with `--require-session-log
  --session-log <card>`, which is the gate that stays red until this flip.
- PR #495 born-red by design; auto-merges (armed, squash) on green CI after this flip.
- CI reds confirmed all class (a): `kit-quality` = the born-red Session-gate HOLD;
  `Kit test suite` + `Cold-adoption smoke` = legacy required-context aliases that
  mirror `kit-quality`'s result (both just `exit 1` on `kit-quality result: failure`).
  No real failure in any of the three job logs (run 29682013026).

## 💡 Session idea

**A `check_stale_walls` companion advisory that flags `wall` rows carrying NO parseable
date at all** — the exact gap this R5 build deliberately skipped. A `wall` row with no
date is worse than a stale one: it can *never* be proven fresh or stale, so it slips
past both the R5 staleness check and the DISCOVERY RULE's re-verify discipline entirely
— an unverifiable-by-construction wall that lives forever. A one-line advisory (`wall
row 'X' has no verification date — cannot be aged; add a dated row per the ledger form`)
closes the blind spot R5 opened, and reuses R5's row parser, so it's a small follow-on.
Deduped: grepped `docs/ideas/` + the night-run groom doc for `dateless|no date|undated|
parseable date` — zero matches; net-new, and distinct from R6 (`--explain-wall`) and R7
(append-log⇄Walls disagreement lint), which both assume a *dated* row.

## ⟲ Previous-session review

Previous session — **R4 HOOK_CENSUS (PR #493)**. Did well: it censused all four Claude
Code lifecycle hooks with *bidirectional* set-equality against `cli._HOOK_EVENTS` /
`cli._HOOK_GUARD_KINDS` (so both a missing AND a stray census entry red the suite, not
just one direction), and made a clean decide-and-flag call when the recipe's "git-hooks"
term didn't match reality — the kit ships zero git-hooks, so it routed the census to the
real fourth surface instead of building a census of nothing. What it could improve /
system improvement it surfaces: R4's own 💡 correctly named that the census family
(`HOOK_CENSUS`, `WORKFLOW_JOB_CENSUS`, the guard manifest) is **kit-only pytest
meta-tests invisible to adopters**, who only run `check` — and proposed a
`check_surface_census` advisory to fix it. But that 💡 was left only in the card, not
seeded as a `docs/ideas/` file or a groom rank — the exact orphaning risk R4's *own*
previous-session review flagged about R3. The concrete workflow improvement: a session
ender should **route its 💡 into `docs/ideas/` or the groom backlog in the same session**
(not just record it in the card), so the census-visibility idea R4 surfaced doesn't
evaporate. This R5 card follows that by keeping its 💡 deduped against the actual groom
doc, not just prose.
