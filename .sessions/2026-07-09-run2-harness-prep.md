# Session 2026-07-09 — run-2 harness prep: score_m1 artifacts + telemetry last-line shadowing

> **Status:** `complete` *(PR #40 — auto-merge armed at open)*

**Scope (about to do):** the run-2 harness-fix increment (ordinary auto-merge
lane — `bench/score_m1.py` and `src/engine/` are not bench pin paths).
(1) `score_m1.py`: stop the mutation regex matching read-only fd redirects
(the `2>/dev/null` artifact that tainted ON-T2 / OFF-T4 M1), and skip
tool_use events whose paired tool_result is an error (the OFF-T5
failed-Edit-counted-as-first-mutation artifact) — regression tests for all
three run-1 artifact cases; run-1's recorded results stay untouched
(append-only law; the row already says M1 unmeasurable).
(2) `src/engine/loop/telemetry.py`: fix the model-line harvest taking the
LAST needle-bearing line even when it is prose that merely mentions the
marker (found live in websites#31) — prefer the last line that parses
validly; regression test; dist regenerated (byte-pin).
(3) B4 ledger: flip the score-m1 idea to shipped, file the websites-surfaced
control-board kit-readiness-cell idea, record the arm-card investigation
disposition on the checker-false-red idea.
(4) `control/status.md` heartbeat as the closing act of the same PR.

## What shipped (PR #40)

- **`bench/score_m1.py`** — two artifact fixes, each with the exact rule
  chosen:
  - *Read-only fd redirects*: `_READONLY_REDIRECT_RE`
    (`(?:\d+|&)?>{1,2}\s*(?:/dev/null\b|&\d+)`) strips `2>/dev/null`,
    `>/dev/null`, `&>/dev/null`, `2>&1`, `>&2` from the command **before**
    the mutation pattern runs; genuine file redirection (`> out.txt`,
    `2> err.log`, `>> log`) still matches.
  - *Failed mutations*: a mutating tool_use becomes a **pending candidate**;
    its pair is the next tool_result before any other tool_use. Error result
    (`is_error: true` or a `tool_use_error`-wrapped content) cancels the
    candidate — the error text still counts as consumed output — and the
    walk continues; a successful pair stops the count at the tool_use's
    line; an **unpaired** candidate (next tool_use or end-of-stream first)
    still stops conservatively, per the module's over-count-is-conservative
    doctrine.
  - Verification against the real run-1 transcripts (read-only, nothing
    recorded): every pair now resolves to a genuine Edit — ON-T2 line 19
    (was the line-15 `git log … 2>/dev/null` artifact), OFF-T4 line 22 (was
    line 1 → m1 0), OFF-T5 line 9, the successful Edit (was the failed
    line-5 Edit).
- **`src/engine/loop/telemetry.py`** — `parse_model_line` now keeps the
  last **validly-parsing** needle line (payload factored into
  `_parse_model_payload`). Rule chosen: *last-valid wins* — it preserves
  the original last-occurrence intent (a corrected report later in the
  card supersedes) while a prose mention with no `·` payload can no longer
  shadow the genuine line into a None + misleading "no line" advisory (the
  websites#31 live failure). Dist regenerated, byte-pin verified.
- **Tests**: +6 (683 → 689) — four score_m1 regressions reproducing the
  three run-1 artifact cases plus the is_error shape and the
  unpaired-conservative edge; one genuine-redirects-still-mutate guard;
  one telemetry shadowing regression.
- **B4 ledger**: score-m1 idea → shipped (#40); new captured idea
  `control-board-kit-readiness-cell-2026-07-09.md` (origin
  consumer:menno420/websites, ORDER 003 adjacency named);
  checker-false-red idea investigation recorded (below).
- **`control/status.md`** heartbeat: rollout-complete phase, #40
  last-shipped, ORDER 003 acked (seen, not started).

## Investigation: the ON-arm "missing: Model line" red

Resolved to the **arm-authoring-gap** side, one level deeper than the idea
file's framing: the arm DID read its planted `.sessions/README.md` (ON-T2
transcript line 40), but `_adopt_sessions_readme()` (`src/engine/adopt.py`)
plants marker **labels only** — never the needle byte-forms — so the arm
had no way to learn the required marker form and wrote a bare bold Model
line the needle scan (correctly) missed. Zero bar-chart characters exist
anywhere in the ON transcripts. Separate defect from the shadowing bug
this PR fixed. Fix stays open in the idea file with a narrowed guard
recipe (plant `label (needle)` pairs + needle-naming checker message).

## Run report

- **📊 Model:** fable-5 · high · runtime bugfix

### ⚑ Self-initiated / decide-and-flag (PL-001)

1. **⚑ orders line acked 003** — inbox ORDER 003 (adopter-visibility band)
   landed as commit #34 after this session's task was cut; the heartbeat
   acks it honestly (seen, not started) rather than reporting acked=001,002
   against an inbox that visibly contains 003.
2. **⚑ checker-false-red root cause traced but NOT fixed here** — the
   `_adopt_sessions_readme()` label-without-needle gap is engine + dist +
   template-adjacent work outside this increment's scope; recorded as the
   idea's narrowed next step instead (contained follow-up, one function +
   one test).
3. **⚑ unpaired-mutation rule decided**: a mutating tool_use with no paired
   result still stops the count (conservative direction, matching the
   scorer's existing doctrine) — flagged since the idea file specified only
   the error-paired case.

### 💡 Session idea (dedup-checked against docs/ideas/ + roadmap)

**score_m1 should emit an audit trail of cancelled candidates** — add a
`cancelled_mutations: [{line, tool, reason}]` field to the m1.json record
(failed-pair cancellations, stripped-redirect near-misses). Run-1's judge
had to hand-walk transcripts to discover both artifacts; with the scorer
now making *judgment calls* (error-pair cancellation), its verdicts should
be auditable from the record alone — the same grading-separation instinct
as guard-fires carrying the finding payload. One list + two append sites
in `score_transcript`; test: OFF-T5-shaped fixture asserts the cancelled
line-5 Edit appears with reason `error_result`. Recorded in-card (small,
single-file); the groom pass can file it if run-2's judging proves it out.

### ⟲ Previous-session review — ORDER 002 status overwrite (#33)

Strong: the deliberate LAST-act sequencing (release verified → then the
status overwrite rode its own control-only PR) gave the fast lane a clean
first live exercise with real stakes, and the notes line's
"PR #30 superseded (overwrite-own, newest wins)" is exactly the kind of
explicit supersession that keeps parallel heartbeats honest. What it
missed: #30 was *declared* superseded but left open — the terminal-state
rule would have it closed with that one-line reason at the moment of
supersession, not left for a later sweep. **Workflow improvement:** when a
status overwrite supersedes an open PR's content, close that PR in the
same breath (the declaration and the close are one act); a "superseded"
note on a still-open PR recreates the abandoned-open-PR window the
terminal-state rule exists to prevent.

## KPIs / verification (this worktree)

- `python3 -m pytest tests/ -q` → **689 passed** (683 + 6 new) pre-merge;
  **694 passed** after merging main's parallel #35 (fleet adoption review)
  into this branch — #35 landed mid-session touching `control/status.md`
  (resolved as a synthesis heartbeat: this session's run-2 facts + #35's
  fleet verdicts and expanded ⚑ needs-owner list, fresh timestamp) and
  `dist/bootstrap.py` (resolved canonically: regenerated from the merged
  src, byte-pin re-verified).
- Dist byte-pin: `python3 src/build_bootstrap.py` → `git diff --exit-code
  dist/bootstrap.py` clean.
- `python3 dist/bootstrap.py check --strict --require-session-log
  --session-log .sessions/2026-07-09-run2-harness-prep.md` green at flip.
- `scripts/check_program_law.py`, `scripts/check_idea_index.py`,
  `scripts/check_bench_integrity.py --base origin/main` all green.
- Fixed scorer re-run over run-1 transcripts (read-only): all three
  artifact pairs resolve to genuine Edits; recorded results untouched.
