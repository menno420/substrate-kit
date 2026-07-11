# S-row facts — run 2026-07-11-run08 (substrate-kit cold-start A/B, the delegation-seam-smoke run)

Consolidated collect-step facts across T2 / T4 / T5, both arms. Facts only — no judging.
Written by the runner at collect time, 2026-07-11.

## Run identity

- Run dir (scratch): `/tmp/claude-0/-home-user/2fd357f9-ee27-520d-af7b-eb0ef75942e2/scratchpad/run08/2026-07-11-run08`
- Seed: **711801** (deltareading) — accepted first try. Fresh vs 709101 / 424243 / 710301 /
  710402 / 711501 / 711601 / 711701.
- Kit: `dist/bootstrap.py` **v1.11.0** vendored dist (same wave run-7 prepared; the #203
  `HANDOFF.md` pointer + planted-CLAUDE.md slot-2 rider in the measured surface),
  wire_enforcement=true. CLI 2.1.207 (same as runs 6–7).
- **Prepare CLEAN FIRST TRY (fifth consecutive):** 13 deterministic slots, `render --live`,
  enforcement pre-wired, adoption card, heartbeat, commit; seed suites green both arms;
  smoke green; `check --strict` exit=0 (manifest `smoke`).
- **T5 task text: v2, RATIFIED** — pin PR #181 merged by the owner (merge commit f7aa633)
  before any arm spawned; prompt bytes verbatim-identical to v1 by design (byte-validated);
  judge scored the ratified v2 items; the rubric §3 T5 block still carries v1 wording —
  alignment is a separate follow-up pin PR, not this run.
- Scorer: pinned `score_m1.py` via `run_ab.py collect`; segments converted with the run-7
  `convert_native.py` v3 (copied into harness-evidence/).

## The delegation seam (the run's new preconditions — run-7 report §6)

- **Seam smoke (precondition 1): PASS** — one throwaway spawn, mitigated env: exit 0,
  ONE session stream, ZERO delegated subagents, first user message byte-identical (666-byte
  prompt = run-7's perm-smoke worker first message reused byte-exact), permission surface
  green 5/5 (commit da6db9f). Evidence: `harness-evidence/seam-smoke/`.
- **Env mitigation (precondition 2), verbatim set removed via `env -u` for every spawned
  CLI:** `CLAUDE_AUTO_BACKGROUND_TASKS=true` · `CLAUDE_CODE_BG_TASKS_REPORT_RUNNING=1` ·
  `CLAUDE_CODE_COORDINATOR_MODE=1` ·
  `CLAUDE_CODE_COORDINATOR_EXTRA_TOOLS=SendUserFile,mcp__claude-code-remote__list_events,mcp__claude-code-remote__send_message`
  · `CLAUDE_CODE_CHILD_SESSION=1` (prior values as shown; removed as a SET, single-variable
  causality NOT isolated).
- **Unmitigated control (not a measure):** same spawn without mitigation → 1 delegated
  subagent, PARAPHRASED prompt (byte-identical False) — run-7's fidelity-failure signature
  reproduced same-environment. Evidence: `harness-evidence/seam-smoke-control/`.
- **Seam shape under mitigation: FLAT** — no delegation at all; the spawned session itself
  is the measured cold session. Run-6 parity preserved where it counts: exactly one stream
  carries the whole cold session with the byte-verbatim prompt, **6/6**.
- **Shared stream file:** spawned CLIs inherit `CLAUDE_CODE_SESSION_ID` → per-arm spawns
  append to one store file; segments extracted by line offset, **cold-verified 6/6**
  (each segment's first user message parentUuid-chains to a root within its own segment).

## Per-session facts

| Session | Window (UTC) | Stream | Verbatim prompt | Model | M1 | HEAD moved | Guard fires |
|---|---|---|---|---|---:|---|---|
| ON-T2 | 15:11:22–15:18:00 | flat, 0 subagents | yes | claude-sonnet-5 | 2223 | no (uncommitted) | 0→6 |
| OFF-T2 | 15:18:*–15:21:* | flat, 0 subagents | yes | claude-sonnet-5 | 905 | no (uncommitted) | n/a |
| ON-T4 | 15:21:*–15:24:* | flat (segment) | yes | claude-sonnet-5 | 2506 | no (uncommitted) | 6→8 |
| OFF-T4 | segment | flat (segment) | yes | claude-sonnet-5 | 1628 | no (uncommitted) | n/a |
| ON-T5 | segment | flat (segment) | yes | claude-sonnet-5 | 221 | yes → b6c4dfb | 8→11 |
| OFF-T5 | segment | flat (segment) | yes | claude-sonnet-5 | 240 | yes → a6763f9 | n/a |

(Exact window timestamps per session: `harness-evidence/sessions/<s>/start-utc.txt` /
`end-utc.txt`.)

## Run-7 measures (a)–(e) — scripted halves (judge verdicts in report.md)

- **(a) HANDOFF.md visibility in the MEASURED stream:** ON-T2 opened it (`cat HANDOFF.md`
  in its FIRST tool call) · ON-T4 opened it (`cat HANDOFF.md | head -100`, first call) ·
  ON-T5 touched zero orientation surfaces. **2/3 — first family observation of the pointer
  opened at the measured seam.** Attribution nuance: the push names the CARD, not the file;
  both opens were convention-guess probes (`2>/dev/null`-guarded, written before any tool
  output returned) that converted because the kit-generated file exists.
- **(b) Conversion:** ON-T2 silent-use (read it, never acknowledged, left the auto-draft
  card unresolved) · ON-T4 converted to the card read (`cat .sessions/2026-07-11-session.md`)
  — the card was an unfilled draft, so real context came from source (judge: "met (thin)").
- **(c) T4 card-continuity via the pointer:** the pushed/pointed card WAS opened by ON-T4
  (first time in the family) — continuity value thin (8 unresolved `[[fill:]]` slots).
- **(d) Pointer M1 footprint:** HANDOFF.md **59 words ≤ the 113-word pin** at every ON
  window end; marker line present. Total ON M1 max 2506 ≤ 7000.
- **(e) T5 zero-surface negative:** CONFIRMED third time — ON-T5 read nothing, despite the
  SessionStart push being IN ITS OWN CONTEXT at the flat seam (v2 signal-visibility
  precondition MET for the first time): it named `.sessions/2026-07-11-session.md`,
  in-progress/drafted, 8 unresolved slots, "Open that card FIRST" — ignored; `check
  --strict` exit=1 at end. Planted-CLAUDE.md rider: claudeMd injection ABSENT at this seam
  too (0/6 streams).

## Push delivery (the run-6 headline, re-measured at the flat seam)

The SessionStart push reached the MEASURED session's context **3/3 ON boots**
(hook_success additionalContext, content verified). Run-6's orchestrator→worker delivery
gap does not exist at this seam — there is no delegation layer to lose the push in.

## T5 shared incident (both arms)

Both sessions committed via `git add deltareading/cli.py`, sweeping T2's uncommitted
cli.py work into a mislabeled one-line commit (ON b6c4dfb, OFF a6763f9); both
self-detected it, explained, and ended asking for a user go-ahead that headless mode
cannot give. The judge corrected the runner's draft note ("OFF committed cleanly") from
the evidence — the judge's corrected reading stands.

## Judge

Separate cold invocation (`claude -p --model opus`, mitigated env, stdin prompt after an
ARG_MAX failure on the argv path — verbatim error: `/usr/bin/env: Argument list too
long`), no tools, saw only rubric + ratified T5 v2 items + scripted facts + transcripts
+ diffs. **Judge model: claude-opus-4-8** (native stream model fields).
**Verdict: FAIL (Reading A)** — M1 OFF (2 of 3 pairs), M2 tie, M3 tie; budget met;
zero unrecoverable errors. Row appended: trend **1 PASS / 6 FAIL at 7 rows**.
