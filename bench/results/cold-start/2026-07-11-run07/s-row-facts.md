# S-row facts — run 2026-07-11-run07 (cold-start continuity re-validation) — RUN ABORTED AT SPAWN

Facts only — no judging. Written by the runner at abort time, 2026-07-11.
**This run produced NO measured sessions, NO M1, NO judge report, and NO verdict.**
The full verbatim deviation record is in `manifest.json` `runner_notes`; this file is the
fact table for what *did* run.

## Run identity

- Run dir (scratch): `/tmp/claude-0/-home-user/2568bc4d-6464-5fda-b39e-b82c5674376c/scratchpad/run07/2026-07-11-run07`
- Seed: **711701** (mossreading) — accepted first try. Fresh vs run-1 (709101), run-2 (424243),
  run-3 (710301), run-4 (710402), run-5 (711501), run-6 (711601).
- Kit: `/home/user/substrate-kit/dist/bootstrap.py` (**v1.11.0** — the first prepared arm carrying
  the #203 worker-visible `HANDOFF.md` pointer), wire_enforcement=true.
- Prepare: **clean first try** (fourth consecutive clean scripted prepare): 13 deterministic slots,
  `render --live`, enforcement pre-wired, adoption card, heartbeat, commit; seed suites green both
  arms; smoke green; `check --strict` exit=0.
- Planted-CLAUDE.md state (run-7 measure (e) precondition, verified on disk at prepare):
  ON `.claude/CLAUDE.md` present with `HANDOFF.md` at read-first slot 2; OFF arm has **no**
  CLAUDE.md anywhere.
- Permission surface (identical to run-6, verified by prepare-time smoke in a throwaway repo
  BEFORE any measured spawn): `--permission-mode acceptEdits` + `--allowedTools "Bash(git add:*)"
  "Bash(git commit:*)" "Bash(python3 -m pytest:*)" "Bash(python -m pytest:*)"` — all four classes
  green, zero walls.
- CLI: 2.1.207 (same as run-6). Spawn command per session: headless `claude -p "<fenced task
  text>"` + the surface above + `--model sonnet`, cwd = arm repo.
- Prompt payloads byte-validated BEFORE spawning: the extractor's output for T2/T4/T5 is
  byte-identical to run-6's six committed worker first-user-messages (6/6).

## WHY THE RUN ABORTED — the delegation seam changed under the harness

The run-6 protocol requires the CLI's remote orchestrator to delegate to **exactly ONE worker
agent** receiving the task text **byte-identical** — the worker is the measured cold session
(run-6: 6/6). In this runner environment, **every spawn decomposed the task across multiple
subagents** and **zero** workers received the verbatim prompt:

| Spawn | window (UTC) | subagents | verbatim-prompt workers | repo commit |
|---|---|---|---|---|
| ON-T2 attempt 1 | 14:01:13–14:05:57 | **6** (3 no-op stubs, 1 git/pytest checker, 1 orientation reader, 1 implementer) | **0** | 0734051 (implementer) |
| ON-T2 attempt 2 (the one allowed reset-relaunch; arm reset to bb3f3da first) | 14:07:57–14:16:54 | **9** (6 stubs, 1 HANDOFF/orientation reader, 1 file dumper, 1 implementer) | **0** | yes (implementer) |
| OFF-T2 diagnostic | 14:17:53–14:22:47 | **5** (2 stubs, 1 explorer, 1 file reader, 1 implementer) | **0** | yes (implementer) |

Decomposition occurred on **both** arms (kit present or absent) → environment-wide
orchestrator-policy change at the harness seam, not a kit effect. ON reset budget exhausted →
**STOP** per the one-reset rule; ON-T4 / OFF-T4 / ON-T5 / OFF-T5 were **never spawned**.
A decomposed spawn is unusable as a measured session: orientation happens at the orchestrator
layer and in sibling reader agents, so no single worker stream carries an M1/M2 comparable to
rows 1–6.

Environment delta (observed, cause unproven): run-6 ran the same CLI 2.1.207 earlier the same
day (11:18–11:35Z) with clean 1-worker delegation. This session's environment has async
background-task delegation active (`CLAUDE_AUTO_BACKGROUND_TASKS` set, inherited by spawned
CLIs; the `task-notification`/`queued_command` machinery and 'wait'/'no-op' stub spawns in the
orchestrator streams are its signature).

## Models (verified from native transcript `model` fields)

Orchestrators and all substantive workers, every spawn incl. the permission smoke:
**`claude-sonnet-5`**. (Two 4-line placeholder stubs contain no assistant events, hence no model
field.) No judge was invoked — nothing valid to judge.

## Run-7 measures (a)–(e): NOT MEASURED — precondition failed at the harness seam

Genuine pointer FACTS from the aborted attempts (evidence, not measures):

1. **HANDOFF.md regenerated on disk at every ON boot** by the SessionStart hook — 63 words
   (≤ the 113-word pin), marker `<!-- substrate:handoff-pointer -->` present. Snapshots:
   `harness-evidence/on-T2-attempt*/HANDOFF-at-end.md`.
2. **SessionStart push reached the ORCHESTRATOR at both ON boots** (`hook_success` attachment,
   `# Session orientation — c8a75bc878e8 … ## Handoff —`), same as run-6.
3. **The orchestrator converted the pointer both times** — its reader-worker prompts name
   "`HANDOFF.md` if present at repo root", and the readers actually opened it (attempt 1:
   `Read` on the exact path; attempt 2: `cat HANDOFF.md`). First family observation of any
   spawned agent layer opening the pointer file — but under an invalid protocol.
4. **claudeMd-injection channel: absent.** 0 of 20 spawned worker streams (ON + OFF) carried a
   `<system-reminder>`/claudeMd block in the first user message; every worker-visible
   `HANDOFF.md` mention was orchestrator-authored prompt text. The T5 zero-surface
   "planted CLAUDE.md channel" does not exist at this delegation seam in this environment.

## Guard fires (ON arm, scripted)

Attempt-1 window appended 7 fires (archive: `harness-evidence/on-T2-attempt1/guard-fires.jsonl`);
attempt-2 arm state carries its own post-reset file (left in scratch). Advisory posture
throughout; fires are harness-level, worker-invisible — unchanged from run-6.

## Verdict / trend

**No verdict — run aborted (harness-seam failure).** Trend UNCHANGED: **1 PASS / 5 FAIL at 6
rows.** Recommendation flagged for Phase 3: no index row (schema fields have no honest values);
record the abort narratively; re-run run-7 from an environment whose delegation seam reproduces
run-6's single-worker behavior (the permission smoke now doubles as a delegation-seam smoke).
