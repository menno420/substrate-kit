# R7 — append-log ⇄ Walls-correction disagreement lint

> **Status:** `complete`

**Session:** 2026-07-19 · Self Improvement work-loop · substrate-kit
**Baton:** R7 (append-log ⇄ Walls-correction disagreement advisory lint) from docs/planning/2026-07-19-night-run-idea-groom.md

**About to do:** add `src/engine/checks/check_wall_ledger_agreement.py` — an
advisory (warn-only, never exit-affecting) lint that fires when a `## Walls`
correction and the newest same-capability `## Append log` entry in
`docs/CAPABILITIES.md` disagree on a capability's status; wire it on the
`posture="advisory"` seam in `cli.py`, add it to `MODULE_ORDER`, rebuild dist,
and add a test — a straight structural sibling of R5's `check_stale_walls`.

- **📊 Model:** Opus 4.8 · high · feature build (append-log ⇄ Walls-correction disagreement advisory lint)
- **⚑ Self-initiated:** R7 is baton work (backlog rung from the night-run groom
  R7 entry). Self-initiated route-arounds within it, decide-and-flag: (1) read
  "the newest append-log entry" as the newest entry *mentioning the family*
  (a same-capability comparison), not the globally-newest row; (2) `_WLA_`-prefixed
  four top-level names to dodge the dist single-namespace collision with
  `check_stale_walls` (the same discipline the module already applies to its KIND
  constant); (3) backticked the claim's branch token to clear the claims-format
  advisory (fix-on-sight). Also folded in the flagged fix-on-sight: R6 card
  `📊 Model` `kit-feature` → `feature build` (PL-004).

## What shipped (PR #498)

Added `src/engine/checks/check_wall_ledger_agreement.py` — an advisory
(warn-only, never exit-affecting) lint that, per capability family (seeded:
merge/arm/flip), compares the newest same-capability `## Append log` verdict
(its `capability|wall` type token) against a `## Walls` *correction* row's
polarity (a "not a wall" phrasing = available, else blocked) and emits ONE
advisory when they disagree — the enforcing readout for the merge/arm/flip
self-contradiction that persisted a full day. Wired on the `posture="advisory"`
seam in `src/engine/cli.py` (import + call + surface block, mirroring R5's
`check_stale_walls`); added to `src/build_bootstrap.py` `MODULE_ORDER`;
`dist/bootstrap.py` rebuilt byte-pin clean.

Files: `src/engine/checks/check_wall_ledger_agreement.py` (new),
`src/engine/cli.py`, `src/build_bootstrap.py`, `dist/bootstrap.py` (rebuilt),
`tests/test_check_wall_ledger_agreement.py` (9 tests, incl.
`test_not_in_strict_subchecks`). Fix-on-sight folded:
`.sessions/2026-07-19-r6-explain-wall.md` `📊 Model` `kit-feature` → `feature build`.

Evidence: full suite **1858 passed / 1 skipped**; `dist/bootstrap.py check
--strict` exit 0; byte-pin `tests/test_bootstrap.py` 14 passed; the new advisory
does NOT fire on the real `docs/CAPABILITIES.md` (real ledger agrees — both sides
say available since 2026-07-18). Not a STRICT_SUBCHECK (nothing added to
`guards.py` / `_extra_check_findings`; a `test_not_in_strict_subchecks` negative
pins it advisory).

## 💡 Session idea

**Auto-derive the lint's capability families from the ledger's own titles.**
`check_wall_ledger_agreement` currently keys on a hardcoded `_FAMILIES` tuple
seeded only with merge/arm/flip, so a NEW capability contradiction (e.g. about
branch-deletion or tag-push) goes uncaught until someone hand-adds a family. A
small, purely-additive follow-on: extract the `**bold title**` noun-phrase of
each `## Walls` correction row and each `## Append log` entry, canonicalize it to
a key, and cross-check EVERY capability that appears in both sections — turning
R7 from "catches the one known contradiction" into "catches any Walls⇄Append-log
disagreement," the fuller form of the same lint. Deduped: grepped
`docs/planning/2026-07-19-night-run-idea-groom.md` + `docs/ideas/` for
`capabilit` / `disagree` / `families` — R8 is fastlane-symmetry, R9–R12 are
harness / recipes / folded-gate; nothing covers auto-deriving R7's families.

## ⟲ Previous-session review

Previous session — **R6 check --explain-wall/--why (PR #497)**. Did well: a clean
decide-and-flag implementing `--explain-wall` as a pure lookup (always exits 0)
rather than forcing it onto the exit-affecting or advisory seam — the right shape
for a read-only CLI query — covered all 19 blocklist rules with per-rule
`WALL_CORRECTIONS`, and it *flagged* its own `📊 Model` `kit-feature` drift for
pickup (which this session closed). What it missed: it introduced `kit-feature`
— a value off the PL-004 9-class taxonomy — as the `📊 Model` task-class in the
first place, and handed the fix downstream instead of conforming it in-session.
Concrete system/workflow improvement: this is the same recurring drift the
2026-07-11 retro flagged (W-10: "4 of 5 newest cards carry off-PL-004 `📊 Model:`
values"). A `📊 Model:` advisory already exists on the `posture="advisory"` seam,
yet `kit-feature` reached a merged card — so either that advisory doesn't validate
segment-3 against the 9 PL-004 class strings, or it doesn't scan session cards.
Closing that one gap (validate the task-class segment against the 9 PL-004/PL-010
classes, on cards) is the enforce-don't-exhort fix that catches the next
`kit-feature` at CI instead of a session later — a good R-rung candidate.
