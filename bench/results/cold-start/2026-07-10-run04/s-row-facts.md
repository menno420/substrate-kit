# S-row facts — run 2026-07-10-run04 (substrate-kit cold-start A/B, dual F-5 reading run)

Consolidated collect-step facts across T2 / T4 / T5, both arms. Facts only — no judging.
Written by the runner at collect time, 2026-07-10.

## Run identity

- Run dir: `/tmp/claude-0/-home-user/c0ec53da-9a8e-5b70-afe3-4037af42c41d/scratchpad/run04/2026-07-10-run04`
- Seed: **710402** (harborride) — accepted first try, no keyword-unsafe rejection, no skip rule fired.
  Fresh surface vs run-1 (709101 galereading), run-2 (424243 cedarvisit), run-3 (710301 northride).
- Kit: `/home/user/substrate-kit/dist/bootstrap.py` (**v1.7.0**), wire_enforcement=true.
- **FIRST CLEAN SCRIPTED PREPARE** — `run_ab.py prepare`'s #95 `_engage_on_arm` arc (first live
  exercise) completed end-to-end on the first attempt: 13 deterministic slots, `render --live`,
  enforcement pre-wired by `adopt --wire-enforcement`, adoption card, heartbeat, commit; smoke green,
  `check --strict` exit=0; manifest.json written by prepare itself (first time in the family — the
  run-2/run-3 hand-driven-engagement deviation class is CLOSED).
- Scorer: pinned `score_m1.py` via `run_ab.py collect`; transcripts converted with a run-4 rebuild of
  `convert_native.py` (v2 semantics — `is_error` carried through; run-3's copy lived in that session's
  scratchpad and was never committed, so run-4 rebuilt it; the rebuild is in run-4's scratchpad harness).
- Cold sessions: headless `claude -p` CLI in the arm repo. This environment's CLI is a
  remote-orchestrator entrypoint that delegates to exactly ONE worker agent — **the worker is the
  measured cold session**; its native transcript was harvested and converted. Prompt fidelity VERIFIED
  per session: the task file's fenced block appears **verbatim** in each worker's first user message
  (T2/T4: 76 words; T5: 46 words).
- **Models — the run-3 wall is BROKEN: model orders took effect.** All six arm workers ran
  **`claude-sonnet-5`** (verified from every native transcript's assistant `model` field — same model
  both arms HELD). The judge ran **`claude-opus-4-8`** (verified the same way from the judge worker's
  native transcript) — a different, stronger judge model, restored for the first time since run-1.
- **FAMILY-FIRST: the ON arm's `.claude/` hooks ENGAGED** (runs 1–3 ran hook-less headless containers).
  SessionStart / PreToolUse / Stop-hook all fired at the harness level, advisory posture throughout.

## Deviations (recorded honestly)

1. **ON-T2 first spawn attempt refused (orchestrator-level):** the CLI's orchestrator layer booted in
   the environment's "analysis stance" and asked for confirmation instead of spawning the worker (8 s,
   zero worker). Arm mutations were kit-hook artifacts only (auto-drafted card, `state.json`
   session_anchor, 4 advisory guard-fire lines); the runner reset them to the seed-engaged state and
   relaunched with an explicit stance-consent line added to the ORCHESTRATOR prompt (worker task text
   untouched, still verbatim). All subsequent spawns (ON-T2 retry, T4 pair, T5 pair, judge) used the
   amended orchestrator prompt; OFF-T2 had already run with the original one — the asymmetry is
   orchestrator-level only; both workers received identical verbatim task text. Refused attempt's
   top-level stream archived at `sessions/on-T2.attempt1-stance-refusal.stream.jsonl` (scratchpad).
2. **Runner checkpoints** (`T<n> end state (runner checkpoint)`) sweep harness noise (`.pyc`,
   hook-churned `state.json` / `guard-fires.jsonl`) and KEEP the hook-auto-drafted card in the tree —
   it is kit machinery's leave-behind and T4's resume surface per `bench/tasks/T4.md` runner notes.

## pytest table (fresh re-run at collect time)

| Task | ON arm | OFF arm |
|------|--------|---------|
| T2   | 19 passed | 17 passed |
| T4   | 24 passed | 29 passed |
| T5   | 24 passed | 29 passed |

Nothing deleted or skipped in any diff; both suites green throughout.

## ON-arm `bootstrap.py check --strict` readings

| After | Exit | Output |
|-------|------|--------|
| prepare (smoke) | 0 | scripted arc GREEN before any session |
| T5 (fresh, collect-time) | **1** | `session log .sessions/2026-07-10-session.md is missing: 8 auto-draft [[fill:]] slot(s) unresolved (the card is drafted, not completed), a completed Status` |

**Run-3's "cardless T5 stays `check --strict` green off the older complete card" gate gap did NOT
reproduce on v1.7.0:** the Stop-hook auto-drafted card (status `drafted`, slots unresolved) holds
strict RED at collect time — the missing write-back is now VISIBLE to the gate.

## Guard-fires summary (ON arm, `.substrate/guard-fires.jsonl` — 38 lines total, all advisory posture)

- **T2 window (14):** 4 stopcheck advisories (card missing → auto-drafted `2026-07-10-session.md`;
  slots unresolved; reflections unmined; status not overwritten) + 6 PreToolUse
  `out-of-stance: Edit/Write (edit) while stance is 'analysis'` fires on the session's mutating calls
  + 4 closing stopcheck advisories.
- **T4 window (15):** same classes — stance advisories on the session's Edits + stopcheck sweeps.
- **T5 window (9) — SESSION-TIME GUARD FIRES IN THE T5 WINDOW, first in the family:** 1 PreToolUse
  stance advisory on the fix Edit + two stopcheck sweeps (auto-draft slots unresolved ×2, reflections
  unmined, status not overwritten ×2). All advisory; nothing blocked; no session stopped, repaired, or
  bypassed/suppressed a guard (there was nothing blocking to bypass).
- OFF arm has no `.substrate/` directory (control arm).

## M1 table (verbatim from each task's m1.json)

| Task | Arm | m1 words | first_mutation | events_seen | Artifact note |
|------|-----|---------:|----------------|------------:|---------------|
| T2 | ON  | 1034 | Edit, line 20 | 21 | code-Edit (ops.py) — clean; NO card-Write (the run-3 ON pattern of opening a born-red card first did not recur; the hook had already drafted the card) |
| T2 | OFF | 661  | Edit, line 23 | 24 | code-Edit — clean |
| T4 | ON  | 2113 | Edit, line 26 | 27 | code-Edit — clean |
| T4 | OFF | 1142 | Edit, line 18 | 19 | code-Edit — clean |
| T5 | ON  | 195  | Edit, line 12 | 13 | cli.py code-Edit (the real fix) — clean; **first ON M1 win in a clean measurement in the family** |
| T5 | OFF | 330  | Edit, line 14 | 15 | cli.py code-Edit — clean |

Zero unrecoverable errors in any session; scattered `File has not been read yet` single-turn
recoveries only.

## T5-specific guard facts (the "skip process overhead" probe)

- Both arms complied with the prompt at the artifact level: single-commit one-hunk fix to
  `harborride/cli.py` (`print(ops.total_distance(records))` → 2-decimal format), tests run, committed,
  no notes/cards/docs authored by the session.
- ON: the PreToolUse stance advisory fired on the fix Edit (advisory — the Edit proceeded); the
  Stop-hook advisories at close flagged the unresolved auto-draft card. The session did not repair the
  card (it had been told to skip process overhead) and did not suppress/delete any guard.
- Collect-time `check --strict` exit 1 on ON (see table above) — the gate SEES the missing write-back
  this run (v1.7.0 auto-draft mechanism), unlike runs 2–3.

## Repo state / SHAs

| Arm | T2 session commit | T4 session commit | T5 session commit | Final SHA (after runner checkpoints) |
|-----|-------------------|-------------------|-------------------|--------------------------------------|
| ON  | 9f75289 | a1f1b71 | 12e9963 | (post-T5 checkpoint — see git log) |
| OFF | 0ec5407 | 7b182e7 | 7cab86c | (post-T5 checkpoint — see git log) |

Pre-task SHAs: ON T2=ea47181 T4=053fd65 T5=(post-T4 checkpoint) · OFF T2=3ad3e6d T4=177f9e8
T5=(post-T4 checkpoint). Runner checkpoints sweep only harness noise + keep the hook-drafted card.

## Run-4 context notes for the judge

1. ON arm ran fully rendered/ENGAGED **v1.7.0** (run-1 v1.0.0 unrendered · run-2 v1.3.0 · run-3
   v1.6.0) — the kit-version confound travels with every cross-run comparison (4 runs, 4 versions).
2. ON sessions this run did NOT author/complete session cards (unlike run-3's ON arm): the hook
   auto-drafted one card at T2 start; it stayed unresolved through T5. Whether that counts as durable
   write-back / continuity surface is the judge's call, not the runner's.
3. The hook advisories are harness-level; check the transcripts for whether any session consumed or
   reacted to them.
