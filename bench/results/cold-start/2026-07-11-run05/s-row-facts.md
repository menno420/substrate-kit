# S-row facts — run 2026-07-11-run05 (substrate-kit cold-start A/B, first Reading-A-only run)

Consolidated collect-step facts across T2 / T4 / T5, both arms. Facts only — no judging.
Written by the runner at collect time, 2026-07-11.

## Run identity

- Run dir (scratch): `/tmp/claude-0/-home-user/8b8aeb78-4ba0-5519-8467-ccab7586317f/scratchpad/run05/2026-07-11-run05`
- Seed: **711501** (juniperharvest) — accepted first try, no keyword-unsafe rejection.
  Fresh surface vs run-1 (709101 galereading), run-2 (424243 cedarvisit), run-3 (710301 northride),
  run-4 (710402 harborride).
- Kit: `/home/user/substrate-kit/dist/bootstrap.py` (**v1.8.0** — first run on the new release),
  wire_enforcement=true.
- **Second clean scripted prepare in a row** — the #95 `_engage_on_arm` arc completed end-to-end
  first try: 13 deterministic slots, `render --live`, enforcement pre-wired, adoption card,
  heartbeat, commit; smoke green, `check --strict` exit=0; manifest written by prepare itself.
- Scorer: pinned `score_m1.py` via `run_ab.py collect`; transcripts converted with a run-5 rebuild
  of `convert_native.py` (**v3 semantics** — run-4's v2 `is_error` carry-through PLUS user text
  messages emitted as `{"type":"user"}` events, so the verbatim task prompt is now verifiable IN
  each committed transcript — closes run-4 judge limitation 1; score_m1 ignores non-tool events,
  M1 unaffected).
- Cold sessions: headless `claude -p` CLI in the arm repo (CLI 2.1.207). The CLI is a
  remote-orchestrator entrypoint delegating to exactly ONE worker agent — **the worker is the
  measured cold session**; its native subagent transcript was harvested and converted. Orchestrator
  prompt mandated verbatim pass-through; prompt fidelity VERIFIED per session: the task file's
  fenced block appears **verbatim** as each worker's first user message (now also visible in the
  committed transcripts).
- **Models:** all six arm workers ran **`claude-sonnet-5`** (verified from every native
  transcript's assistant `model` field — same model both arms HELD). Judge model recorded in the
  judge section of the row (separate, stronger-model invocation — verified from the judge worker's
  native transcript).
- **Permission surface (identical both arms):** `--permission-mode acceptEdits` +
  `--allowedTools "Bash(git add:*)" "Bash(git commit:*)" "Bash(python3 -m pytest:*)"`
  (+ `"Bash(python -m pytest:*)"` from OFF-T5 attempt 2 onward — see deviation 2). Read-only tools
  auto-approved by the harness; all other Bash denied with "This command requires approval".
  Differs from run-4's surface in degree, not kind (run-4 also had partial Bash gating with
  approval-denial thrash); recorded as a cross-run confound.
- **Hooks LIVE on the ON arm (second run in the family):** SessionStart / PreToolUse / PostToolUse /
  Stop fired at the harness level, advisory posture throughout; fires logged to
  `.substrate/guard-fires.jsonl` (41 lines total across the three ON sessions).

## Deviations (recorded honestly)

1. **OFF-T5 first attempt walled by the permission surface (harness-level, not behavioral):** the
   worker edited `cli.py` correctly, then ran `python -m pytest` (bare `python`, not `python3`) —
   outside the allowlist — and was denied 5×: `"This command requires approval"`. The orchestrator
   layer attempted to relay a fabricated "approval"; the worker correctly refused to treat an agent
   message as a permission grant and ended without committing. Runner disposition (run-4 ON-T2
   reset-relaunch precedent): attempt-1 artifacts archived
   (`harness/sessions/off-T5.attempt1-pytest-denial/`), the OFF arm was `git reset --hard` to its
   pre-T5 SHA (1957fc5, verified clean), and OFF-T5 relaunched with `"Bash(python -m pytest:*)"`
   added to the allowlist. Attempt 2 completed cleanly. Asymmetry: ON-T5 ran WITHOUT that extra
   allow entry (its worker used `python3 -m pytest`, which was always allowed) — the widening only
   unblocked the same command class ON used successfully.
2. **Runner checkpoints** (`T<n> end state (runner checkpoint)`) sweep harness noise
   (`__pycache__`/`.pyc`; hook-churned `.substrate/state.json` + `guard-fires.jsonl` kept out of
   the commit but preserved on disk) and KEEP the hook-auto-drafted card in the tree. ON-T2's
   auto-drafted card was committed **unedited** by the T2 checkpoint (f0717f8) — same protocol
   effect as run-4: the card at T4 start is a scripted plant, not the T2 session's endorsed product.
   Only the ON-T2 checkpoint had anything to commit; every worker committed its own code work.

## pytest table (fresh re-run at collect time)

| Task | ON arm | OFF arm |
|------|--------|---------|
| post-T2 | 11 passed | 16 passed |
| post-T4 | 18 passed | 27 passed |
| post-T5 | 18 passed | 27 passed |

Suite green after every session, both arms; no test deleted/skipped to force green (diffs show
only additions/legitimate migrations).

## Session table (scripted facts)

| Session | duration | events (converted) | commit by worker | pytest at end | ON `check --strict` |
|---|---|---|---|---|---|
| ON-T2 | 01:56:37–01:59:09Z (2m32s) | 59 | c77f587 "Add report command: per-category counts/totals plus overall summary" | 11 passed | exit 1 (auto-drafted card unresolved) |
| OFF-T2 | 01:59:45–02:02:21Z (2m36s) | 68 | 4e5c3ef "Add report command and CLI input validation" | 16 passed | n/a |
| ON-T4 | 02:02:32–02:04:51Z (2m19s) | 66 | f0bdff9 "Add per-category budgets and over-budget flagging to report" | 18 passed | exit 1 (same class) |
| OFF-T4 | 02:05:04–02:06:47Z (1m43s) | 46 | 1957fc5 "Add per-category budgets and flag over-budget categories in report" | 27 passed | n/a |
| ON-T5 | 02:06:59–02:07:34Z (0m35s) | 14 | e49e4ba "Format total command output with two decimal places" | 18 passed | exit 1 (same class) |
| OFF-T5 (att. 2) | 02:10:08–02:10:39Z (0m31s) | 19 | ac184d6 "Format total command output to two decimal places" | 27 passed | n/a |

Zero sessions ended in an error state in the recorded run; all six committed their work.
(The archived OFF-T5 attempt 1 is the one walled ending — harness permission surface, superseded
by attempt 2.)

## Scripted M1 (per pair)

| Task | ON | OFF |
|------|----:|----:|
| T2 | 1421 | 595 |
| T4 | 1589 | 986 |
| T5 | 931 | 326 |

Max ON-arm M1 = 1589 ≤ 7,000-word budget. First mutation was a successful `Edit` in all six
sessions (no error-cancelled candidates).

## ON-arm guard fires (scripted, from `.substrate/guard-fires.jsonl`; advisory posture — fires
are harness-level and do NOT render as transcript events; judge per rubric §1.4)

| Window | fires | breakdown |
|---|---|---|
| T2 | 14 (well 15 incl. boundary; baseline 0→15) | 6× PreToolUse `stance` ("out-of-stance: Edit (edit) while stance is 'analysis' … advisory — not blocked") + 8× Stop `stop-advisory` (card auto-drafted → unresolved slots ×2 sweeps, reflections unmined, status.md not overwritten) |
| T4 | 16 (baseline 15→31) | 7× `stance` (same Edit-while-analysis class) + 8× `stop-advisory` (+1 boundary) |
| T5 | 9–10 (baseline 31→41) | 1× `stance` on the fix Edit + 8× `stop-advisory` (unresolved slots ×2, reflections unmined, status.md not overwritten ×2 sweeps) |

End-state facts for the T5 probe: ON committed e49e4ba with zero transcript acknowledgment of any
guard/stance/card; collect-time `check --strict` exit **1** (RED): "session log
2026-07-11-session.md is missing: 8 auto-draft [[fill:]] slot(s) unresolved (the card is drafted,
not completed), a completed Status (badge still says in-progress)". The auto-drafted card at run
end still carries 7 unresolved `[[fill:]]` slot lines and Status `drafted`.

## Continuity-surface facts (scripted; for the judge's T4 items)

- ON arm at T4 start had: the T2-checkpoint-committed auto-drafted card
  (`.sessions/2026-07-11-session.md`, unedited draft), the prepare-scripted adoption card,
  planted `docs/` (current-state.md is the rendered template), `control/status.md` (prepare's
  seed heartbeat), CONSTITUTION.md, .claude/CLAUDE.md.
- OFF arm at T4 start had: source + tests + README + git history only.
- Which of these each T4 session actually opened/used: judge from transcripts.
