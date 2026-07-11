# Session 2026-07-11 — ON-T2 footprint cut (fresh-state handoff fast path + collect zero-events guard)

> **Status:** `complete`

- **📊 Model:** fable-5 · high · kit-dev

**Scope (as declared, born-red):** cut run-9's sole failing axis — ON-T2 M1
2505 words vs OFF 675 (report §5.4: "'None regressing' — FAILS on M1"). The
run-9 ON-T2 transcript audit (this session, run-8 audit pattern) locates the
cost precisely: (1) **1724 of the 2505 words (69%) are ONE polluted grep** —
`grep -rn "raise\|ValueError\|…" --include="*.py" .` returned 75 lines from
`bootstrap.py` (862w) + 75 byte-identical lines from
`.substrate/backup/bootstrap-1.12.0.py` (862w), zero lines from project code;
the agent TRIED to exclude (`grep -v -E '^\./(bootstrap\.py|\.substrate)'`)
and the filter failed (output paths carried no `./` prefix). The kit's
existing countermeasures both missed this path: the planted `.ignore` (#165
mechanical half) only covers ripgrep-family tools, and the CLAUDE.md
search-hygiene recipe rode a channel that was ABSENT 0/6 (s-row-facts:
claudeMd injection never reached any measured arm). (2) **~224w of boot
surfaces bought nothing** — the HANDOFF pointed at the empty scripted
adoption card ("Open that card FIRST") and the agent obeyed (116w incl. ls)
then read the empty current-state scaffold (108w). Fix shipped here, on the
surfaces run-9 proves ARE delivered and read (HANDOFF.md + the SessionStart
push, 3/3): a **fresh-state fast path** in `handoff_lines` — when the newest
card is complete AND leaves no resolved pointer AND no evidence trail
(nothing to resume; exactly the ON-T2 boot shape), the handoff stops saying
"Open that card FIRST" and instead says fresh start / orient from the task,
plus ONE search-hygiene line carrying the byte-exact working exclusion
(`grep -r --exclude=bootstrap.py --exclude-dir=.substrate` / rg + planted
`.ignore`). **HARD CONSTRAINT honored:** the T4-shaped trail/card rendering
(in-progress/drafted + trail) and the T5-shaped rendering (complete +
resolved pointer) stay byte-equivalent — pinned by new byte-equality
regression tests against expected literal output. Rider 1: `run_ab.py
collect` gains an events_seen==0 abort (the run-9 convert_native argv-slip
class — six empty transcripts briefly scored M1=0) + test. Rider 2: run-10
spec note — a cheap scripted probe for the still-unvalidated #222
drafted-card advisory lane (run-9 measure (d) nuance). NOT touched:
`bench/tasks/` (parallel T5-probe session owns it). Claim:
`control/claims/on-t2-footprint-cut.md` (fast-lane PR #235). CHANGELOG
[Unreleased]; dist regen; NO release cut; run-10 fires it, not this session.

## Close-out (PR #236)

- **Shipped:** (1) the fresh-state fast path in `handoff_lines`
  (`src/engine/loop/handoff_pointer.py` — one composer, both surfaces):
  complete card + no resolved pointer + no evidence trail → "Fresh start —
  nothing in flight" + the working search exclusion
  (`grep -r --exclude=bootstrap.py --exclude-dir=.substrate` / planted
  `.ignore` for rg), no "Open that card FIRST" routing into a contentless
  card. Fires ONLY on that shape — in-progress cards, resolved pointers,
  and any trail bullet keep the old rendering byte-for-byte. (2) run-9
  byte-equality pins: `_RUN9_T4_EXPECTED_POINTER` / `_RUN9_T5_EXPECTED_POINTER`
  literals captured from the pre-change engine at main@fa921f4, asserted
  `==` post-change — the T4 M2/M3 double-win mechanism cannot drift
  silently. (3) `run_ab.py collect` events_seen==0 hard abort (+2 tests).
  (4) `bench/results/cold-start/run-10-spec-notes.md` — the #222
  drafted-card advisory-lane probe design (scripted post-T2/pre-T4
  checkpoint) + fresh-path watch items for run-10.
- **Verified:** `python3.10 -m pytest tests/ -q` → 1057 passed (1046 → 1057,
  +11); `python3.10 -m ruff check src/engine/` clean; dist byte-pin clean
  (rebuilt, 704108 B); check_idea_index / check_program_law /
  check_bench_integrity OK; fresh path live-driven end-to-end in a scratch
  adopter via the rebuilt dist (push + HANDOFF.md render it, 83 words ≤ the
  113 pin; the recipe cuts the 164-line kit pollution to 0 while the run-9
  failure mode — prefix-less paths through the agent's `-v '^\./…'` filter —
  replays 164/164).
- **Decisions made (decide-and-flag):** cut the footprint where the
  transcript says the words went (the polluted grep + the contentless card
  read), NOT the "defer the orientation push" candidate from the run-9
  next-slice line — the push is a user-turn event and costs 0 M1 words;
  hygiene line rides the fresh path only (the T4 shape is byte-pinned, and
  the polluting grep demonstrably happens in fresh sessions). Follow-up
  flagged, not taken: bank `.substrate/backup` dists under a non-`*.py`
  name (kills the 862w byte-copy half structurally, but touches the
  upgrade/rollback naming contract + already-banked adopter files).
- Next session should know: the [Unreleased] payload now carries #228 + #232
  + #236 — cut the release, run the wave, then fire run-10 with the
  spec-notes probe; `bench/tasks/` belongs to the parallel T5-probe claim.

## 💡 Session idea

The kit should ship a **planted `GREP.md`-style one-liner inside the repo
scaffold no — better: a `bootstrap grep` passthrough** — a tiny `check`-family
subcommand (`python3 bootstrap.py grep PATTERN`) that runs the repo's search
with the kit exclusions pre-applied and prints the exact flags it used. Cold
agents reach for whatever search tool is on PATH; giving the kit a
first-class, discoverable search verb makes the hygiene structural instead
of advisory (and its printed flag line teaches the recipe). Dedup-checked:
docs/ideas/ has the CLAUDE.md/#165 guidance and the `.ignore` plant, no
executable-search idea.

## ⟲ Previous-session review

The run-9 session's honest mechanism notes are what made this slice cheap:
"exit 0 via GENUINE completion, the advisory lane never exercised" and the
converter argv-slip deviation were both recorded verbatim instead of
smoothed over, and items 1 and 3 of this slice fell straight out of them.
One improvement: run-9's next-slice line proposed a mechanism ("defer
non-load-bearing orientation push content") that the transcript contradicts
— the push costs 0 M1 words; the words went to a polluted grep. Run reports
should separate the AXIS (T2 M1 regresses) from the MECHANISM GUESS, or the
next session inherits a plausible-but-wrong build target. (This slice
re-derived the mechanism from the transcript first — that step should stay
mandatory for any footprint work.)
