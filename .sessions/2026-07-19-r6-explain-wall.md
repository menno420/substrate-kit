# R6 — check --explain-wall / --why

> **Status:** `complete`

**Session:** 2026-07-19 · Self Improvement work-loop · substrate-kit
**Baton:** R6 (check --explain-wall / --why) from docs/planning/2026-07-19-night-run-idea-groom.md

- **📊 Model:** Opus 4.8 · high · feature build (CLI lookup + per-rule corrections)
- **⚑ Self-initiated:** R6 is baton work (backlog rung from the night-run groom
  R6 entry), but note the self-initiated expansion: added per-rule `WALL_CORRECTIONS`
  beyond the recipe's literal "the correction" (the checker had only a shared one),
  and left the checker's Finding message unchanged for minimal blast radius —
  decide-and-flag.

## What shipped (PR #497)

Added `bootstrap.py check --explain-wall <phrase>` (alias `--why`): a CLI lookup
that runs the false-wall `match_blocklist`, prints the matched rule + a per-rule
ground-truth correction for that rule + a pointer to the `docs/CAPABILITIES.md`
dated-append-row form for recording a genuine momentary refusal. A benign phrase
that matches no rule reports "no false-wall rule matched". A lookup, never a gate —
**always exits 0**; touches neither the exit-affecting `_extra_check_findings` nor
`STRICT_SUBCHECKS`.

- **`src/engine/checks/check_no_false_walls.py`** — added the per-rule
  `WALL_CORRECTIONS` map, an `all_rule_names()` coverage surface, and the
  `explain_wall()` helper; the checker's own Finding message is left unchanged
  (minimal blast radius).
- **`src/engine/cli.py`** — the `--explain-wall`/`--why` flag, an early-return
  lookup branch, and `_cmd_explain_wall`.
- **`dist/bootstrap.py`** — rebuilt (byte-pin clean).
- **`tests/test_explain_wall.py`** — 6 tests.

Evidence: full suite **1849 passed / 1 skipped**; all **19** blocklist rules
covered by a correction; implementation commit **123bfce**.

## 💡 Session idea

**Wire the per-rule `WALL_CORRECTIONS` into `check_no_false_walls`'s own Finding
message**, so `check --strict` prints the specific ground-truth correction for each
violation inline — turning every false-wall finding into a self-correcting
instruction, not just the shared generic message. R6 deliberately left the Finding
message unchanged for minimal blast radius; this closes the other half — the map
already exists and is proven, so it's a small, purely additive follow-on. Deduped:
grepped `docs/planning/2026-07-19-night-run-idea-groom.md` + `docs/ideas/` for
`correction` — R7 is a *disagreement lint* between `## Walls` and `## Append log`
(a CAPABILITIES.md self-consistency check), R12/others don't touch the checker's
Finding text; this idea is distinct — it upgrades the *checker's own* message, not
the ledger's consistency.

## ⟲ Previous-session review

Previous session — **R5 capability stale-wall advisory (PR #495)**. Did well: it
made two clean decide-and-flag calls the recipe didn't anticipate — wiring on the
`posture="advisory"` seam instead of the exit-affecting `_extra_check_findings` the
recipe named (to honor "advisory, not red"), and renaming the constant to
`STALE_WALL_KIND` to dodge a single-file collision with `check_folded_gate` once the
dist bundles — and it seeded its deliberately-skipped gap (dateless `wall` rows) as
a deduped groom-checked idea rather than orphaning it in the card. Concrete
system/workflow improvement this surfaces: the born-red HOLD currently reddens as
**three** separate required checks for one logical hold — `kit-quality` plus the two
legacy alias mirrors `Kit test suite` and `Cold-adoption smoke`, both of which just
`exit 1` on `kit-quality result: failure` (R5's own Verification section had to spend
three lines explaining that all three reds share one cause and none is a real
failure). The CI could collapse/rename these into one clear `session-gate: HOLD
(flip card to release)` red instead of three identical-cause failures — cutting the
watcher noise that R5 had to annotate away every session.
