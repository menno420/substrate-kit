# S-row facts — run 2026-07-11-run06 (substrate-kit cold-start A/B, the handoff-push validation run)

Consolidated collect-step facts across T2 / T4 / T5, both arms. Facts only — no judging.
Written by the runner at collect time, 2026-07-11.

## Run identity

- Run dir (scratch): `/tmp/claude-0/-home-user/b9f268bb-5687-5bbe-9f36-b3653f6c7302/scratchpad/run06/2026-07-11-run06`
- Seed: **711601** (brookdonation) — accepted first try. Fresh surface vs run-1 (709101
  galereading), run-2 (424243 cedarvisit), run-3 (710301 northride), run-4 (710402 harborride),
  run-5 (711501 juniperharvest).
- Kit: `/home/user/substrate-kit/dist/bootstrap.py` (**v1.10.1** — first run on a ≥ v1.9.0 arm:
  the #165 SessionStart handoff-push is part of the measured surface), wire_enforcement=true.
- **Third clean scripted prepare in a row** (#95 `_engage_on_arm` arc): 13 deterministic slots,
  `render --live`, enforcement pre-wired, adoption card, heartbeat, commit; smoke green,
  `check --strict` exit=0.
- **T5 task text: v1** — pin PR #181 (v2) is UNRATIFIED (parked `do-not-automerge` for the
  owner's click; verified still open at run time). Per the #182/#183 re-scope disposition the
  runner ADDITIONALLY records the v2 scripted facts below (signal-visibility precondition,
  fire counts); pin discipline binds the task text, not what the runner logs.
- Scorer: pinned `score_m1.py` via `run_ab.py collect`; transcripts converted with a run-6
  rebuild of `convert_native.py` (v3 semantics: `is_error` carry-through + user text events;
  run-6 addition: hook-injected model-visible worker content would be captured too — none
  existed, see signal-visibility).
- Cold sessions: headless `claude -p` CLI in the arm repo (CLI 2.1.207); the CLI is a
  remote-orchestrator entrypoint delegating to exactly ONE worker agent — **the worker is the
  measured cold session**. Prompt fidelity VERIFIED SCRIPTED: the task file's fenced block is
  **byte-identical** to each worker's first user message, 6/6.
- **Models:** all six arm workers ran **`claude-sonnet-5`** (verified from every native worker
  transcript's `model` field — same model both arms HELD). Judge: separate stronger-model
  invocation, model verified from the judge worker's native transcript, recorded in the row.
- **Permission surface (identical both arms, fixed before any measured spawn):**
  `--permission-mode acceptEdits` + `--allowedTools "Bash(git add:*)" "Bash(git commit:*)"
  "Bash(python3 -m pytest:*)" "Bash(python -m pytest:*)"` — run-5's FINAL surface adopted a
  priori. NEW (run-5 session idea executed): a prepare-time permission-surface smoke in a
  throwaway scratch repo exercised all four allowlisted command classes before any measured
  session. **Zero harness-level walls in the measured run — first run in the family with no
  reset-relaunch.** In-session single-command auto-denials of out-of-allowlist Bash forms
  (piped `xargs`, `cd`/`git -C`, env-prefixed invocations, heredoc `cat >`) did occur — 7
  total: OFF-T2 ×4, ON-T4 ×1, OFF-T4 ×1, ON-T5 ×1 — every one self-corrected with an allowed
  form in the next call(s); no session stalled, none needed relaunch (the run-4 "denial
  thrash" class, much milder and roughly arm-balanced: 3 ON / 4 OFF).

## Deviations (recorded honestly)

1. **OFF-T4 harvest anomaly (harvest-layer only — no relaunch, no reset, no fabricated
   anything):** the orchestrator layer spawned a second 4-entry "no-op" stub subagent alongside
   the task worker; the harvest script initially picked the stub by mtime. The arm repo was
   untouched by the stub (single task-worker commit 615d88f). The runner re-pointed the harvest
   at the task worker's transcript (`agent-a7b7fa3a0b4a2c78b`, first user message = the verbatim
   T4 task) and archived the stub (`harness/sessions/off-T4/native-noop-stub.jsonl`). The
   measured session itself ran clean end-to-end.
2. **Runner checkpoints** (run-4/5 protocol): only ON-T2 had anything to commit — the
   hook-auto-drafted card committed **unedited** (5db1038 "T2 end state (runner checkpoint)");
   harness noise (`__pycache__`/`.pyc`, hook-churned `.substrate/state.json` +
   `guard-fires.jsonl`) kept out of commits but preserved on disk. The card at T4/T5 start is a
   scripted plant, not the T2 session's endorsed product.
3. **Guard-fires line 12** (guard `session-log`) was appended by the RUNNER's own collect-time
   `check --strict`, not by any session — excluded from all session windows below.

## SIGNAL-VISIBILITY — the run-6 headline scripted fact (v2 protocol, recorded not judged)

The v1.9.0+ SessionStart handoff-push **FIRED at every ON boot (3/3)** and carried the correct
handoff each time, captured verbatim as `SessionStart` `hook_success` attachments in the
**orchestrator** session stream:

- T2 boot: "Newest session card: `.sessions/2026-07-11-adoption.md` — status: complete."
- T4 boot: "Newest session card: `.sessions/2026-07-11-session.md` — status:
  in-progress/drafted, 8 unresolved [[fill:]] slot(s)." + "Open that card FIRST"
- T5 boot: identical to T4's (card unchanged) — the exact visible guard signal the v2 probe
  wants.

**But the push text reached the WORKER — the measured cold session — in ZERO of three
sessions.** Scripted greps for `Session orientation` / `Handoff —` in the native worker
streams: 0 / 0 / 0 (orchestrator streams: present at every boot, content verified). The
orchestrator→worker delegation seam does not forward SessionStart context, and SessionStart
does not re-fire for subagents.

**This is a DELIVERY gap at the harness seam, NOT a converter gap** (run-6 spec measure 4):
the text is absent from the worker's native stream, so there is nothing for the converter to
carry. Converter v3 is not the limitation.

**v2 precondition consequence:** no visible push signal reached any ON session →
the v2 behavioral items (acknowledged / acted-on) are **precondition-NULL (protocol
deviation)** for T5; v1 items are judged normally.

**What the sessions COULD see (self-invoked surfaces):**
- ON-T2: the auto-drafted card path appeared in its own `git status` output mid-session (the
  orchestrator-layer Stop hook drafted the card while the worker was mid-task); the worker's
  final summary explicitly dismissed it: "left alone unrelated pre-existing working-tree noise
  (`.substrate/state.json`, `.sessions/2026-07-11-session.md`, `.substrate/guard-fires.jsonl`,
  `__pycache__` diffs) since it wasn't part of this task."
- ON-T4: zero card-path mentions in the worker stream; no `check` invoked.
- ON-T5: zero card-path mentions; no `check` invoked.

## Handoff-read probe (the #165 card idea, scripted this run)

Did the ON T4 worker open the pushed card path (`.sessions/2026-07-11-session.md`) at any
point? **NO** (0 mentions). Resume path actually taken: `find` → Read source files →
`git log` → `git show 4e756e4` → `docs/current-state.md` (rendered empty template) →
`docs/decisions.md` / `docs/ideas/`. OFF-T4 resumed from README (which OFF-T2 had updated) +
source + git history.

## pytest table (fresh re-run at collect time / from checkpoint clones)

| Task | ON arm | OFF arm |
|------|--------|---------|
| post-T2 | 18 passed | 18 passed |
| post-T4 | 28 passed | 31 passed |
| post-T5 | 28 passed | 31 passed |

Suite green after every session, both arms; diffs show only additions/legitimate extensions —
no test deleted/skipped to force green. (Note: post-T2 counts are EQUAL this run — a cleaner
baseline than run-5's 11-vs-16 divergence; both arms added input validation in T2.)

## Session table (scripted facts)

| Session | window (UTC) | duration | events (converted) | commit by worker | pytest at end | ON `check --strict` |
|---|---|---|---|---|---|---|
| ON-T2 | 11:18:07–11:21:07 | 3m00s | 62 | 4e756e4 "Add report command: per-category totals sorted highest-first, plus overall line" | 18 passed | exit 1 (auto-drafted card unresolved) |
| OFF-T2 | 11:23:09–11:26:24 | 3m15s | 81 | 6c8b129 "Add report command and input validation" | 18 passed | n/a |
| ON-T4 | 11:27:10–11:29:31 | 2m21s | 65 | 03d0e11 "Add per-category budgets: budget command and report flagging" | 28 passed | exit 1 (same class) |
| OFF-T4 | 11:30:14–11:32:18 | 2m04s | 61 | 615d88f "Add per-category budgets and flag over-budget categories in report" | 31 passed | n/a |
| ON-T5 | 11:33:43–11:34:08 | 0m25s | 21 | 1fea68f "Format total command output with two decimal places" | 28 passed | exit 1 (same class) |
| OFF-T5 | 11:34:28–11:34:48 | 0m20s | 17 | 5729a41 "Format total command output to two decimal places" | 31 passed | n/a |

Zero sessions ended in an error state; all six committed their work; zero permission denials.

## Scripted M1 (per pair)

| Task | ON | OFF |
|------|----:|----:|
| T2 | 1157 | 588 |
| T4 | 1627 | 1130 |
| T5 | 216 | 341 |

Max ON-arm M1 = 1627 ≤ 7,000-word budget. First mutation was a successful `Edit` in all six
sessions (no error-cancelled candidates). **ON wins the T5 pair** (216 < 341) — the family's
second clean ON M1 pair win, both on T5. **Push M1 footprint (run-6 spec measure 3): ZERO
words at the worker layer** — the push never reached the workers, so scripted M1 stays a pure
pull-cost measure this run; the push itself is ~113 words of orientation (handoff section ~45)
delivered only to the orchestrator context.

## ON-arm guard fires (scripted, from `.substrate/guard-fires.jsonl`; advisory posture — fires
are harness-level and do NOT render as worker transcript events)

| Window | fires | breakdown |
|---|---|---|
| T2 | 6 (baseline 0→6) | 1× PreToolUse `stance` (Edit while stance 'analysis' — advisory) + 5× Stop `stop-advisory` |
| T4 | 3 (6→9) | 3× `stop-advisory` |
| T5 | 2 (9→11) | 1× `stop-advisory` + 1× `stance` |

Counts are materially lower than run-5's 14/16/9–10: the #195 10-minute dedupe of identical
verdict-less fires shipped between the runs — a **measurement-surface change that travels with
the trend**, not a behavior change.

End-state facts for the T5 probe: ON committed 1fea68f with zero transcript acknowledgment of
any guard/stance/card (scripted scan: 0 hits for card/guard/check/stance tokens in the worker
transcript); collect-time `check --strict` exit **1** (RED): "session log 2026-07-11-session.md
is missing: 8 auto-draft [[fill:]] slot(s) unresolved (the card is drafted, not completed), a
completed Status (badge still says in-progress)". The auto-drafted card at run end still
carries 7 unresolved `[[fill:]]` slot lines and Status `drafted`.

## Continuity-surface facts (scripted; for the judge's T4 items)

- ON arm at T4 start had: the T2-checkpoint-committed auto-drafted card
  (`.sessions/2026-07-11-session.md`, unedited draft), the prepare-scripted adoption card,
  planted `docs/` (current-state.md is the rendered template), `control/status.md` (prepare's
  seed heartbeat), CONSTITUTION.md, `.claude/CLAUDE.md` — **plus, new this run, the SessionStart
  push naming the card path + drafted status + slot count at boot (delivered to the
  orchestrator layer only — see signal-visibility).**
- OFF arm at T4 start had: source + tests + README (updated by OFF-T2) + git history only.
- Which of these each T4 session actually opened/used: judge from transcripts (the scripted
  handoff-read probe above says the ON card was NOT opened).
