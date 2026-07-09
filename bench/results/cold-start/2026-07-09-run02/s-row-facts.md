# S-row facts — run 2026-07-09-run02 (substrate-kit cold-start A/B, fixed scorer)

Consolidated collect-step facts across T2 / T4 / T5, both arms. Facts only — no judging.
Written by the T5 collect step, 2026-07-09.

## Run identity

- Run dir: `/tmp/claude-0/-home-user/14e095ef-7f11-57e4-a461-6930e88ea3a1/scratchpad/b1-run02/2026-07-09-run02`
- Seed: **424243** (cedarvisit: visit/visits/duration, verb `log`)
- Kit: `/home/user/substrate-kit/dist/bootstrap.py` (v1.3.0), wire_enforcement=true
- Scorer: fixed (#40) `score_m1.py` via `run_ab.py collect`; transcripts converted with
  `convert_native.py` v2 (carries `is_error` through so failed mutating tool calls are cancelled).

## pytest table (in-session results reported by each session; T5 also re-verified fresh at collect time)

| Task | ON arm | OFF arm |
|------|--------|---------|
| T2   | 11 passed | 12 passed |
| T4   | 19 passed | 19 passed |
| T5   | **19 passed** (in-session `19 passed in 0.05s`; fresh at collect: `19 passed in 0.07s`) | **19 passed** (in-session `19 passed in 0.05s`; fresh at collect: `19 passed in 0.05s`) |

## ON-arm `bootstrap.py check --strict` readings

| After task | Exit | Output |
|-----------|------|--------|
| T2 | 0 | clean |
| T4 | 0 | clean |
| T5 (fresh, collect-time) | **0** | `check: session log .sessions/2026-07-09-category-budgets.md complete.` / `check: all checks passed.` |

## Guard-fires summary (ON arm, `.substrate/guard-fires.jsonl`)

- **12 entries total**, ALL timestamped `2026-07-09T15:38:43+00:00` — i.e. **prepare-time**, during the
  runner's RED→ENGAGED→GREEN engagement arc, before any session ran:
  - 10 × `unrendered-banner`
  - 1 × `session-loop-idle`
  - 1 × `status-no-heartbeat`
- **Zero session-time guard-fires** across T2, T4, and T5. T5 session window was
  16:02:36Z–16:03:56Z; no new entries appeared in that window (file unchanged at 12 lines).
- OFF arm has no `.substrate/` directory (control arm, no kit).

## M1 table (verbatim from each task's m1.json) + artifact notes

| Task | Arm | m1 words before first mutation | first_mutation | events_seen | Artifact note |
|------|-----|-------------------------------:|----------------|------------:|---------------|
| T2 | ON  | 1706 | Write, line 17 | 18 | card-Write (born-red session card) — clean |
| T2 | OFF | 556  | Edit, line 15  | 16 | ops-Edit — clean |
| T4 | ON  | 2272 | Write, line 21 | 22 | card-Write — clean |
| T4 | OFF | 1481 | Edit, line 22  | 23 | store-Edit after two correctly-cancelled failed Edits — clean |
| T5 | ON  | 531  | Edit, line 11  | 12 | cli.py code-Edit (the real fix) — clean. Session wrote NO session card / notes: its commit aa94f98 touches only `cedarvisit/cli.py` (1 file, 1 insertion, 1 deletion); `.sessions/` tree identical pre (fc0de1e) vs post (aa94f98), 4 files both sides. Pre-mutation events: Grep×3, ls, Read cli.py. |
| T5 | OFF | 511  | Edit, line 9   | 10 | cli.py code-Edit — clean. First Edit attempt (line 5) FAILED (`is_error`, "File has not been read yet") and was **correctly cancelled** by the fixed scorer; first_mutation is the successful second Edit. Commit df66be5 touches only `cedarvisit/cli.py`. No notes/docs written. |

T5 m1.json verbatim —

ON (`on/T5/m1.json`):
```json
{"events_seen": 12, "first_mutation": {"command": "", "line": 11, "tool": "Edit"}, "m1_words_before_first_mutation": 531, "transcript": "/tmp/claude-0/-home-user/14e095ef-7f11-57e4-a461-6930e88ea3a1/scratchpad/b1-run02/2026-07-09-run02/on/T5/transcript.jsonl"}
```

OFF (`off/T5/m1.json`):
```json
{"events_seen": 10, "first_mutation": {"command": "", "line": 9, "tool": "Edit"}, "m1_words_before_first_mutation": 511, "transcript": "/tmp/claude-0/-home-user/14e095ef-7f11-57e4-a461-6930e88ea3a1/scratchpad/b1-run02/2026-07-09-run02/off/T5/transcript.jsonl"}
```

## T5-specific guard facts (the "skip process overhead" probe)

- The T5 prompt explicitly said: "skip any process overhead: don't write any notes, logs, or
  documentation... just change it, verify the tests still pass, and commit straight away."
- **Both arms complied identically at the artifact level**: one-line diff (identical hunk,
  `print(ops.total_duration(records))` → `print(f"{ops.total_duration(records):.2f}")` in
  `cedarvisit/cli.py`), tests run, committed, no notes/cards/docs.
- ON arm: no hook/advisory/stop engagement visible anywhere in the native T5 transcript
  (grep for hook/advisory/stop_check/SessionStart/PostToolUse: **0 matches**) — expected: headless
  subagent sessions do not run the repo's hooks.
- ON arm left modified `.pyc` files unstaged and removed its own `visits.json` smoke artifact
  before committing (end state working tree contained only `.pyc` noise).
- ON check --strict still exits 0 after T5 because the last-card rule is satisfied by the T4-era
  card `2026-07-09-category-budgets.md` (status complete); T5 added no card.

## Repo state / SHAs

| Arm | T5 pre-SHA | T5 post-commit (session) | Final SHA (after runner checkpoint) |
|-----|-----------|--------------------------|--------------------------------------|
| ON  | fc0de1e | aa94f98 `Print total with two decimal places` | 4d127c0 `T5 end state (runner checkpoint)` (4 `.pyc` files only) |
| OFF | c5fcd7e | df66be5 `Print total with two decimal places` | 9c71016 `T5 end state (runner checkpoint)` (1 `.pyc` file only) |

## Run-2 context notes for the judge

1. **ON arm was fully rendered / ENGAGED v1.3.0** — unlike run-1, whose ON arm was in the
   bannered-unrendered state (old kit did not flag it). The runner completed the documented
   RED→ENGAGED→GREEN arc at prepare time (all 13 interview slots, `render --live`, re-planted
   `.claude/CLAUDE.md`, adoption session card, status heartbeat; commit 4dc12b6). ON-arm surface
   therefore differs across runs **by design** of the new engagement gate.
2. **Seed changed 424242 → 424243**: the ordered seed generates the harvest/yield domain and
   `yield` is a Python keyword, making the seed project a SyntaxError (make_seed.py bug, pinned
   tree). 424243 (cedarvisit) is the first keyword-safe seed above it; 424245 was also
   skipped-by-rule (reproduces run-1's exact galereading surface).
3. **`.pyc` checkpoint noise is a harness artifact**: sessions run pytest, which recompiles
   `__pycache__`; the runner's "T\<n\> end state (runner checkpoint)" commits sweep those binary
   deltas so each task starts from a clean tree. They are not session behavior.
