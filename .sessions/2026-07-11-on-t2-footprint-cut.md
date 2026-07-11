# Session 2026-07-11 — ON-T2 footprint cut (fresh-state handoff fast path + collect zero-events guard)

> **Status:** `in-progress`

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
