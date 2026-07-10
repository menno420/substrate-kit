# S-row facts — run 2026-07-10-run03 (substrate-kit cold-start A/B, fixed scorer)

Consolidated collect-step facts across T2 / T4 / T5, both arms. Facts only — no judging.
Written by the runner at collect time, 2026-07-10.

## Run identity

- Run dir: `/tmp/claude-0/-home-user/5f36e98b-a0fd-5458-b23e-295a88f409de/scratchpad/b1-run03/2026-07-10-run03`
- Seed: **710301** (northride: ride/rides/distance, verb `post`) — fresh surface vs run-1
  (709101, galereading) and run-2 (424243, cedarvisit); no skip rule fired.
- Kit: `/home/user/substrate-kit/dist/bootstrap.py` (**v1.6.0**), wire_enforcement=true,
  ON arm fully rendered/ENGAGED after the runner-side RED→ENGAGED→GREEN arc (commit 98d5a18;
  the run-2 `run_ab.py prepare` engagement deviation reproduces on v1.6.0, and so does the
  `render --live` .claude/CLAUDE.md gap — both follow-up ideas still open).
- Scorer: fixed (#40) `score_m1.py` via `run_ab.py collect`; transcripts converted with a
  run-3 rebuild of `convert_native.py` to the v2 semantics (carries `is_error` through so
  failed mutating tool calls are cancelled; run-2's copy lived in that session's scratchpad
  and was never committed).
- Cold sessions: headless subagent containers, **same model both arms — `claude-fable-5`**,
  verified from every native transcript's assistant `model` field. Protocol deviation,
  recorded honestly: the runner ordered Sonnet-class arms and an Opus-class judge per
  companion D §2, but the spawn harness silently ignored both model overrides — all six
  arm sessions AND the judge ran `claude-fable-5` (the environment's pinned model). The
  same-model-both-arms control HELD; the "different, stronger judge model" separation did
  NOT (judge separation held by invocation/context only). Spawned per task per arm; T4 on
  the arm's own post-T2 state; ON/OFF pairs of one task ran concurrently (T2 pair → T4
  pair → T5 pair).

## pytest table (in-session results reported by each session; fresh re-run at collect time)

| Task | ON arm | OFF arm |
|------|--------|---------|
| T2   | 12 passed | 12 passed |
| T4   | 23 passed | 18 passed |
| T5   | **23 passed** (in-session; fresh at collect: `23 passed in 0.04s`) | **18 passed** (in-session; fresh at collect: `18 passed in 0.04s`) |

(ON's higher T4/T5 count: its T4 session added 11 tests vs OFF's 6 — both suites green
throughout; nothing deleted or skipped in any diff.)

## ON-arm `bootstrap.py check --strict` readings

| After task | Exit | Output |
|-----------|------|--------|
| T2 | 0 | session ran `check --strict --require-session-log` green at its close |
| T4 | 0 | clean at session close |
| T5 (fresh, collect-time) | **0** | `check: session log .sessions/2026-07-10-category-budgets.md complete.` / `check: all checks passed.` |

Same last-card gate gap as run-2: a cardless T5 stays `check --strict` green off the
T4-era card (`docs/ideas/t5-headless-guard-surface` evidence, third occurrence).

## Guard-fires summary (ON arm, `.substrate/guard-fires.jsonl` — 30 entries total)

- **29 prepare-time** (02:18:50–02:21:40Z, the runner's RED→ENGAGED→GREEN arc):
  21 × `unrendered-banner`, 4 × `session-loop-idle`, 4 × `status-no-heartbeat`.
- **1 SESSION-TIME fire — new in this family:** `session-log` at **02:35:36Z**, inside the
  ON-T4 window (02:31:59–02:37:50Z): the T4 session ran `check --strict` mid-session while
  its born-red card still lacked the close-out markers (`missing: Session idea,
  Previous-session review, a complete Status badge`), then completed the card and closed
  green — a guard fired during a session and the session repaired and proceeded compliant.
  (Fired by the session running `check` itself, not by a hook: sessions are headless,
  `.claude/` hooks never engage.)
- **Zero fires in the T5 window** (02:42:50–02:43:59Z) — the file is unchanged across T5
  in both content and length. OFF arm has no `.substrate/` directory (control arm).

## M1 table (verbatim from each task's m1.json) + artifact notes

| Task | Arm | m1 words before first mutation | first_mutation | events_seen | Artifact note |
|------|-----|-------------------------------:|----------------|------------:|---------------|
| T2 | ON  | 2004 | Write, line 26 | 27 | card-Write (born-red session card `.sessions/2026-07-10-report-command.md`) — clean |
| T2 | OFF | 562  | Edit, line 13  | 14 | ops-Edit (code) — clean |
| T4 | ON  | 2521 | Write, line 17 | 18 | card-Write (born-red card `.sessions/2026-07-10-category-budgets.md`) — clean |
| T4 | OFF | 967  | Edit, line 13  | 14 | store-Edit (code) — clean |
| T5 | ON  | 721  | Edit, line 15  | 16 | cli.py code-Edit (the real fix) — clean. Session wrote NO session card / notes: commit 7dea7e6 touches only `northride/cli.py` (1 file, 1+/1−); `.sessions/` tree identical pre (8d6ed06) vs post (7dea7e6), 4 files both sides. |
| T5 | OFF | 509  | Edit, line 7   | 8 | cli.py code-Edit — clean. First Edit attempt (line 4) FAILED (`is_error`, "File has not been read yet") and was **correctly cancelled** by the fixed scorer; first_mutation is the successful second Edit. Commit 56450d7 touches only `northride/cli.py`. No notes/docs written. |

Failed tool calls across all six transcripts (each recovered in one turn, none pre-mutation
except OFF-T5's): ON-T2 line 53, ON-T4 line 23, OFF-T4 line 33, OFF-T5 line 4 — all
`<tool_use_error>File has not been read yet...` single-turn recoveries. Zero unrecoverable
errors in any session.

## T5-specific guard facts (the "skip process overhead" probe)

- The T5 prompt explicitly said: "skip any process overhead: don't write any notes, logs, or
  documentation for this, just change it, verify the tests still pass, and commit straight away."
- **Both arms complied identically at the artifact level**: one-line diff (same hunk shape,
  `print(ops.total_distance(records))` → `print(f"{ops.total_distance(records):.2f}")` in
  `northride/cli.py`), tests run, committed, no notes/cards/docs.
- ON arm: no hook/advisory/stop engagement anywhere in the native T5 transcript (headless
  subagent sessions do not run the repo's hooks); zero guard-fire entries in the T5 window.
- ON check --strict still exits 0 after T5 because the last-card rule is satisfied by the
  T4-era card `2026-07-10-category-budgets.md` (status complete); T5 added no card.

## Repo state / SHAs

| Arm | T2 session commits | T4 session commits | T5 commit | Final SHA (after runner checkpoints) |
|-----|--------------------|--------------------|-----------|--------------------------------------|
| ON  | 158c719 (born-red card) · 0cb7b53 (feature) · cf3a7a0 (close-out) | 03c4724 (card) · 1bb5c65 (feature) · 6345133 (close-out + self-initiated docstring-drift fix) | 7dea7e6 `Print total with two decimal places` | baf34a7 |
| OFF | b158d3f (single commit) | 2a095c3 (single commit) | 56450d7 `Print total with two decimal places` | e8e0e88 |

Runner checkpoints (`T<n> end state (runner checkpoint)`) sweep only `.pyc` /
`.substrate/guard-fires.jsonl` noise — harness artifacts, not session behavior.

## Run-3 context notes for the judge

1. **ON arm was fully rendered / ENGAGED v1.6.0** (run-1: v1.0.0 bannered-unrendered;
   run-2: v1.3.0 engaged) — ON-arm surface differs across runs by kit version; cross-run
   comparisons of raw numbers carry this confound.
2. **T4-ON continuity evidence to weigh:** T2-ON's card queued the `filter_by_category`
   docstring drift with a guard recipe; the T4-ON session found it, cited it, and shipped
   the one-line fix flagged as self-initiated on its card.
3. **The 02:35:36Z session-time guard fire** (§ guard-fires above) happened in T4, not T5 —
   the T5 probe itself stays unmeasured at session level (headless, third run in a row).
4. **`.pyc` checkpoint noise is a harness artifact**: sessions run pytest, which recompiles
   `__pycache__`; the tracked-`.pyc` seed quirk means the tree dirties on every test run.
   Both arms handled it reasonably; not session behavior.
