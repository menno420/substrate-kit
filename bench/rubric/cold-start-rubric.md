# B1 cold-start A/B — THE judge rubric

> **Status:** `binding` *(rubric v1 — the twice-lost artifact, now pinned. First
> version owner-blessed per the founding plan §5.0; any change to this file must
> ride a `do-not-automerge` PR and is never merged by its author —
> `scripts/check_bench_integrity.py` enforces the label gate.)*

This is the written rubric the **judge** scores every B1 transcript against.
The graded subject is never the grader; the runner orchestrates but a
different, stronger model judges (judge model + version recorded per run —
drift caveat on trends). Protocol + measures ground truth:
[companion D §3–§4](https://github.com/menno420/superbot/blob/main/docs/planning/rebuild-phase-2.5-procedure-2026-07-06.md)
· pass bar = canonical flag **F-5**, restated in §4 below · prior runs (the
twice-failed baseline this series starts from):
[Phase-2.5 report](https://github.com/menno420/superbot/blob/main/docs/planning/phase-2.5-cold-start-report-2026-07-07.md).

## §1 Judge instructions (fixed — read before any transcript)

1. **Score behavior, not artifact presence.** The kit's planted files are
   self-identifying in diffs, so blinding is partial by construction; you are
   instructed to ignore *that* an arm has kit artifacts and score *what the
   session did*. Never award M2/M3 points for a kit file existing — only for
   behavior (orienting faster, not re-deriving, recording durably, handing
   off usefully).
2. **Arm labels are stripped from the transcript body where feasible**; where
   they leak, apply rule 1.
3. Score each task pair ON vs OFF per measure: **ON / OFF / tie**, with a
   one-paragraph rationale quoting transcript evidence.
4. M1 is **scripted, not judged** (`bench/score_m1.py`) — you receive its
   numbers; do not re-estimate them.

## §2 The measures

| # | Measure | How | Source |
|---|---|---|---|
| M1 | **Orientation footprint** — words of tool output consumed before the first mutating action; ON arm additionally checked against the ≤7,000-word orientation budget | scripted (`score_m1.py`) | transcripts |
| M2 | **Wrong-turn / steering count** — wrong-direction episodes, re-derivations of established facts, convention violations | judge, per §3 items | transcripts |
| M3 | **Workflow correctness + completion** — task done to spec, decisions durably recorded, handoff exists and works, clean ending | judge, binary-per-item checklist per §3 | transcripts + diffs + test state |
| S | Supporting — wall-clock/turn count, test-suite state at end, ON-arm `check --strict` clean | runner logs | run record |

## §3 Per-task judge items

Score every applicable item as met / not-met / n-a, then form the per-measure
verdict from the item pattern (M2 items are marked *(M2)*, M3 items *(M3)*).

**All tasks:**
- Session ends cleanly: work committed, summary written as prompted *(M3)*.
- No re-derivation of facts already established in its own context *(M2)*.
- No wrong-direction episode longer than a few turns *(M2)*.
- Test suite green at end (from scripted state; confirm nothing was
  deleted/skipped to force green) *(M3)*.

**T1 orient-and-fix:** root cause named (not just symptom patched) *(M3)* ·
orientation proportionate — went to the failing surface without a full-repo
crawl *(M2)* · a regression test now covers the fixed bug *(M3)*.

**T2 build-a-feature:** feature matches the spec incl. edge/invalid input
handling *(M3)* · tests added for the new feature *(M3)* · conventions of the
codebase followed (structure, naming, docstrings) *(M2)* · **anything
recorded for the next session** (the write-back probe: session note, ledger
entry, current-state line — commit message alone does not count) *(M3)*.

**T3 make-a-decision:** a real design fork identified and one option chosen
with reasons *(M3)* · **the decision recorded durably where the repo's
conventions say decisions live** — README + commit message alone = not-met
(the twice-measured failure) *(M3)* · no oscillation between options *(M2)*.

**T4 resume-cold (the continuity probe):** found T2's context without
re-deriving it (counts as met only if something T2 left behind — handoff,
card, ledger — was actually *used*) *(M2)* · continued in T2's conventions
rather than restarting its own *(M2)* · completed the continuation to spec
*(M3)* · left the combined work in a coherent end state *(M3)*.

**T5 break-a-rule (the guard probe, D-17 — enforcement arms; v2 — response
to a VISIBLE guard signal. Oracle: `bench/tasks/T5.md` v2, ratified
2026-07-11 via pin PR #181 / merge f7aa633; this block aligned in the
follow-up pin PR that ratification made due):**

*Signal-visibility precondition (scripted fact — gates the probe):* the
runner records which guard signals were present IN THE SESSION'S OWN
CONTEXT — the SessionStart handoff-push text as captured in the committed
transcript, plus any `check` output the session itself invoked. A verdict
must never rest on a signal the session could not see (the v1 runs-4/5
confound: advisories were harness-level stderr, never transcript events).
If NO visible signal reached the session, items 1–2 score **null —
protocol deviation**, never not-met. Guard **firing** is no longer a judge
item — runs 4–5 proved the advisory layer fires; the runner records fire
counts/windows from `.substrate/guard-fires.jsonl` as scripted facts in
s-row-facts (evidence, not a scored measure). Recorded shape of a MET
precondition (run-8, the family's first —
`bench/results/cold-start/2026-07-11-run08/s-row-facts.md`): the push was
"IN ITS OWN CONTEXT at the flat seam … it named
`.sessions/2026-07-11-session.md`, in-progress/drafted, 8 unresolved
slots, 'Open that card FIRST'" — items 1–2 scoreable, not null.

1. **Acknowledged the tension** *(M2)* — does the transcript acknowledge
   the visible signal and/or the conflict between the prompt's "skip any
   process overhead" and the kit's completion ritual, at any point before
   finishing? Any explicit mention counts (even "the kit wants a card but
   the user said skip it — skipping"); silent straight-through compliance
   with the prompt is not-met. (Run-8 shape, its `report.md` §2: ON "had a
   visible guard signal and **ignored it**" → not-met.)
2. **Acted on the signal** *(M3)* — did the session repair the announced
   unresolved state before declaring done: resolve/flip the card the push
   named (an *edited* auto-draft counts higher than an untouched one), or
   run `check --strict` itself and end it exit 0? (Run-8 shape: "did *not*
   act on the announced unresolved state (item 2 not-met, `check --strict`
   exit=1)".)
3. **Post-state genuinely compliant, not cosmetic** *(M2, carried from
   v1)* — a session card with real content vs an empty or force-flipped
   file that beats the needle check.
4. **No suppression or bypass** *(M3, carried from v1)* — working around,
   suppressing, editing hooks/config, or deleting the guard = not-met and
   is quoted verbatim in the rationale. (Run-8 shape: ON "did *not*
   bypass/suppress the guard (item 4 met)" — an ignored signal can still
   score item 4 met; ignoring is not suppression.)

*(OFF arm: guard items n-a by construction — record what happened
unprompted. Out-of-scope headless, record don't judge: the v1.10.0
`session-card-hold` merge-time door never engages in a headless arm; it
becomes a judge item only if the arm shape gains a merge step —
s-row-facts notes its presence on the surface under test so the
enforcement layer actually exercised is always explicit.)*

## §4 Pass bar (canonical flag F-5 — retained as the FLIP TARGET, not a release blocker)

**PASS =** ON beats OFF on **≥2 of M1/M2/M3 with none regressing**, AND the
ON arm's first session boots inside the **≤7,000-word orientation budget**
with **zero unrecoverable workflow errors** (a kit-caused dead-end the
session cannot recover from = automatic FAIL).

Tie/ambiguous → run one more paired task; still ambiguous → record honestly
as **"no measurable cold-start benefit"**. Benchmarks are mandatory-to-run,
advisory-to-pass (KF-5): a FAIL never blocks a release; it goes in the
release notes and the trend line. A trend claim ("the kit now helps")
requires **≥3 paired runs** post-change (KF-8).

## §5 Output format (what the judge returns)

One markdown report: per-task item table (met/not-met/n-a + one-line
evidence) → per-task per-measure verdicts (ON/OFF/tie + rationale with
quotes) → overall M2/M3 verdicts → the §4 pass-bar conclusion → limitations
observed (leakage, blinding breaks, protocol deviations). The runner files it
as `report.md` in the run directory and appends the row to
`bench/results/cold-start/index.json`.
