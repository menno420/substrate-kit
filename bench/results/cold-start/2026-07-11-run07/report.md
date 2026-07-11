# B1 cold-start A/B — run 2026-07-11-run07 — RUN REPORT

> ## VERDICT: **ABORTED (harness delegation-seam failure — environment, not kit)**
>
> No measured sessions, no scripted M1, no judge invocation, no row. This report is
> written by the runner/recorder, **not** a judge — there was nothing valid to judge.
> The scored family trend is **UNCHANGED: 1 PASS / 5 FAIL at 6 rows.** Nothing in this
> run is a kit result; the failure is the runner environment's orchestrator delegation
> policy. Seed 711701 → `mossreading`. Kit = vendored dist v1.11.0 (the first prepared
> arm carrying the #203 worker-visible `HANDOFF.md` pointer). CLI 2.1.207 (same as
> run-6). All deviations are recorded VERBATIM in `manifest.json` `runner_notes`
> (11 entries); the fact table is `s-row-facts.md`.

## §0 Orientation to the evidence

- Prepare was **clean first try** (fourth consecutive clean scripted prepare):
  13 deterministic slots, `render --live`, enforcement pre-wired, adoption card,
  heartbeat, commit; seed suites green both arms; smoke green; `check --strict`
  exit=0 (`manifest.json` `smoke`).
- The prepare-time **permission-surface smoke** (run-6 protocol) ran BEFORE any
  measured spawn: all four allowlisted command classes green, zero walls
  (`harness-evidence/perm-smoke/agent-ac2283d0e54cd8914.jsonl`). Early warning
  recorded: the orchestrator **paraphrased** the smoke meta-prompt instead of
  forwarding it verbatim — the first hint the delegation seam had changed since run-6.
- Prompt payloads were byte-validated BEFORE spawning: the extractor output for
  T2/T4/T5 is byte-identical to run-6's six committed worker first user messages, 6/6
  (`harness-evidence/prompts/prompt-T{2,4,5}.txt`, `harness-evidence/extract_prompt.py`).
- Planted-CLAUDE.md state verified on disk at prepare (measure (e) precondition):
  ON `.claude/CLAUDE.md` present with `HANDOFF.md` at read-first slot 2; OFF arm has
  **no** CLAUDE.md anywhere.

## §1 What broke — the delegation seam decomposed every spawn

The run-6 protocol requires the headless `claude -p` orchestrator to delegate to
**exactly ONE worker agent** that receives the task text **byte-identical** — that
worker is the measured cold session (run-6: 6/6 verbatim). In this runner environment,
**every spawn decomposed the task across multiple subagents and 0/3 spawns delivered a
verbatim single-worker prompt**:

| Spawn | Window (UTC) | Subagents | Verbatim-prompt workers | Evidence |
|---|---|---:|---:|---|
| ON-T2 attempt 1 | 14:01:13–14:05:57 | **6** (3 no-op stubs, 1 git/pytest checker, 1 orientation reader, 1 implementer) | **0** | `harness-evidence/on-T2-attempt1/` (6 agent streams + `orchestrator.jsonl`); window facts `harness-evidence/windows-on-T2-attempt1-decomposed/` |
| ON-T2 attempt 2 — the ONE allowed reset-relaunch (arm reset to bb3f3da; attempt-1 evidence archived first) | 14:07:57–14:16:54 | **9** (6 stubs, 1 HANDOFF/orientation reader, 1 file dumper, 1 implementer) | **0** | `harness-evidence/on-T2-attempt2/` (9 agent streams + `orchestrator-full.jsonl`); windows `harness-evidence/windows-on-T2/` |
| OFF-T2 diagnostic (already-scheduled spawn run once to localize) | 14:17:53–14:22:47 | **5** (2 stubs, 1 explorer, 1 file reader, 1 implementer) | **0** | `harness-evidence/off-T2-diagnostic/` (5 agent streams + `orchestrator.jsonl`); windows `harness-evidence/windows-off-T2/` |

Decomposition occurred on **both arms** — kit present or absent — so it is an
**environment-wide orchestrator-policy change at the harness seam, not a kit or
pointer effect**. A decomposed spawn is unusable as a measured session: orientation
happens at the orchestrator layer and in sibling reader agents, so no single worker
stream carries an M1/M2 comparable to rows 1–6.

**Abort decision** (briefing stop rule, verbatim: "If the harness fails in a way you
cannot recover within the one-reset rule, STOP, record it verbatim, and report the
failure — do not improvise a different methodology"): ON's one reset-relaunch was
exhausted (attempt 2 also decomposed); the OFF diagnostic proved the failure
arm-independent (its own reset deliberately not spent — nothing a reset could change).
**ON-T4 / OFF-T4 / ON-T5 / OFF-T5 were never spawned.** No collect, no M1, no judge,
no index row.

**Suspected mechanism (observed, cause not proven):** run-6 ran the SAME CLI 2.1.207
earlier the same day (11:18–11:35Z) with clean single-worker delegation 6/6. This
runner session's environment has **async background-task delegation active**
(`CLAUDE_AUTO_BACKGROUND_TASKS` set and inherited by the spawned CLIs); its signature
is visible in the orchestrator streams — `queued_command`/`task-notification`
attachments, "Async agent launched successfully" tool_results, and the 'wait'/'no-op
placeholder' stub spawns used to await async results (see the stub agent streams in
each spawn dir). Recorded as the named suspect, not a proven cause.

## §2 Measures (a)–(e): NOT MEASURED — protocol precondition failed

All five run-7 measures (HANDOFF.md worker-stream visibility; visibility→conversion;
T4 card-continuity via the pointer; pointer M1 footprint; T5 zero-surface negative)
are **NOT MEASURED**. The only measure-adjacent item that survives is a pin fact:
the pointer file on disk was 63 words ≤ the 113-word pin (below). No scores, no
verdict, no trend movement.

## §3 Genuine recovered facts (evidence from the aborted attempts — NOT measures)

The protocol was invalid, so none of these score; they are honest observations with
artifact citations:

1. **HANDOFF.md was regenerated on disk at every ON boot** by the SessionStart hook —
   **63 words ≤ the 113-word pin**, marker line `<!-- substrate:handoff-pointer -->`
   present. Snapshots: `harness-evidence/on-T2-attempt1/HANDOFF-at-end.md`,
   `harness-evidence/on-T2-attempt2/HANDOFF-at-end.md`.
2. **The SessionStart push reached the ORCHESTRATOR at both ON boots** (`hook_success`
   attachment carrying `# Session orientation — c8a75bc878e8 … ## Handoff —`), same as
   run-6. Evidence: `harness-evidence/on-T2-attempt*/orchestrator*.jsonl`.
3. **The orchestrator converted the pointer both times** — its reader-worker prompts
   name "`HANDOFF.md` if present at repo root", and the readers actually opened it
   (attempt 1: `Read` on the exact path; attempt 2: `cat HANDOFF.md`). This is the
   **first family observation of any spawned agent layer opening the pointer file** —
   recorded under an invalid protocol, so it is a fact, not a measure of (a)/(b).
4. **claudeMd-injection channel absent at the worker seam: 0/20 spawned worker
   streams** (ON + OFF, all three spawns) carried a `<system-reminder>`/claudeMd block
   in their first user message; every worker-visible `HANDOFF.md` mention was
   orchestrator-authored prompt text. The T5 zero-surface "planted CLAUDE.md channel"
   does **not exist at this delegation seam in this environment**.
5. **Planted-CLAUDE.md state held at prepare**: ON carries `HANDOFF.md` at read-first
   slot 2; OFF has none (s-row-facts.md § Run identity).
6. **Models**: orchestrators and all substantive workers, every spawn incl. the
   permission smoke, ran `claude-sonnet-5` (verified from native transcript `model`
   fields; two 4-line placeholder stubs contain no assistant events, hence no model
   field). No judge was invoked.
7. **Guard fires** (ON arm, scripted, harness-level): attempt-1 window appended 7
   fires (`harness-evidence/on-T2-attempt1/guard-fires.jsonl`); advisory posture
   throughout, worker-invisible — unchanged from run-6.

## §4 Deviations — verbatim record

All 11 deviation/context entries are recorded **verbatim** in `manifest.json`
`runner_notes` (this run dir), per the family deviation rule. Summary index:
abort declaration · clean prepare · permission smoke (+ paraphrase warning) ·
DEVIATION 1 ON-T2 attempt 1 decomposition · DEVIATION 2 reset-relaunch + attempt 2
decomposition (ON budget exhausted) · DEVIATION 3 OFF-T2 diagnostic decomposition
(environment-wide localization) · abort decision · environment-delta context ·
genuine pointer evidence · artifacts-staged note · Phase-3 recommendation.

## §5 index.json decision: NO row appended (6 rows stand)

The results-home schema (`bench/run_ab.py` `INDEX_ROW_KEYS`) requires `m1_on`,
`m1_off`, `m2`, `m3`, `verdict`, and `judge_model` **verbatim on every row**, and
`cmd_record` rejects a row missing any of them. This run has **no honest value for
any of those keys**: nothing was measured and no judge ran. Every existing consumer
of the index treats a row as a scored run (the KF-8 trend headline counts rows), so
an "ABORTED" row would either fabricate the required measure keys (null-stuffing a
schema that nowhere admits nulls — all 6 existing rows carry real values) or
silently inflate the scored-row count. **Decision: leave `index.json` at 6 rows,
byte-untouched.** The abort is recorded here, in the trend homes narratively
(control/status.md B1 FAMILY VERDICTS · docs/current-state.md · CHANGELOG
[Unreleased]), and in this run dir's manifest — the append-only history keeps a
full-fidelity record without a fabricated row.

## §6 Run-8 measurement spec

**Run-8 = re-run run-7's exact measures** — nothing about the measurement design
failed, the environment did:

- Same protocol as run-6/run-7: fresh seed (used: 709101, 424243, 710301, 710402,
  711501, 711601, 711701), scripted prepare `run_ab.py prepare --tasks T2,T4,T5
  --wire-enforcement`, kit = vendored dist (v1.11.0 or current wave), permission
  smoke, six cold `claude -p` sessions, scripted M1 at collect, independent
  stronger-model judge on the pinned rubric, Reading A only.
- Same measures (a)–(e): (a) scripted HANDOFF.md signal-visibility in WORKER streams;
  (b) visibility → acknowledged-repaired / acknowledged-declined / silent conversion;
  (c) T4 card-continuity via the pointer; (d) pointer M1 footprint (≤113-word pin);
  (e) T5 zero-surface negative with the planted-CLAUDE.md rider fact. T5 runs v1 text
  (pin PR #181 unratified) + v2 scripted facts, per the run-6 disposition.
- **NEW precondition 1 — delegation-seam smoke at prepare time**: extend the
  permission smoke to double as a delegation-seam smoke — assert the smoke worker
  arrives **ALONE** (exactly one delegated agent in the harness project store for the
  spawn) **with the byte-verbatim prompt** as its first user message. If the
  assertion fails, **abort BEFORE spawning the arms** — zero measured-arm state is
  ever created in a broken environment (this run burned ON's reset budget learning
  what the smoke can now detect for free).
- **NEW precondition 2 — an environment reproducing run-6's single-worker seam**:
  the named suspect is **async background-task delegation**
  (`CLAUDE_AUTO_BACKGROUND_TASKS` inherited by spawned CLIs) decomposing `claude -p`
  spawns across multiple subagents. Run the runner from an environment where the
  spawned CLI's delegation seam demonstrably yields ONE worker (verified by
  precondition 1); if the variable is present in the runner environment, prevent it
  from reaching the spawned CLI's environment and re-verify — treating the smoke, not
  the env var, as the ground truth (the variable is the suspect, not the proven cause).
- Everything else unchanged: append-only row 8 only if measured; deviations verbatim;
  one reset-relaunch per arm max; approvals never fabricated.

## §7 Limitations

- **Nothing here is a kit result.** The ON arm's pointer surface was never exposed to
  a valid measured worker; the §3 facts are delegation-seam observations.
- **The mechanism is a named suspect, not a proven cause** — the run-6-vs-run-7 delta
  is confounded by everything that differs between the two runner sessions'
  environments; `CLAUDE_AUTO_BACKGROUND_TASKS` is the observed, signature-matched
  candidate. Run-8's smoke converts this from post-hoc forensics into a scripted
  precondition.
- **The §3 pointer-conversion observation (orchestrator → reader opened HANDOFF.md)
  is encouraging but unusable**: it happened at the wrong layer (a sibling reader
  agent, not the measured worker) under an invalid protocol; only run-8 can say
  whether it converts at the measured seam.
