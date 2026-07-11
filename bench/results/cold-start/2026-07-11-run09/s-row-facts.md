# run-9 scripted facts (runner-recorded ground truth for the judge)

Run 2026-07-11-run09 · seed 711901 → cedardonation · kit vendored dist at main@49b36d7 (KIT_VERSION stamp 1.12.0 + the #228 gate-fix regen, 691876 B — carries the #222 content-gap countermeasure: substantive auto-draft, HANDOFF evidence trail, orientation trim, drafted-card advisory strict lane) · CLI 2.1.207 · arms claude-sonnet-5 ×6 (stream-verified) · env mitigation `env -u` ×5 on every spawn (run-8 set, values verbatim in manifest).

## M1 (scripted, bench/score_m1.py — ground truth)

| task | ON | OFF | first mutation |
|---|---|---|---|
| T2 | 2505 | 675 | Edit (successful) both arms |
| T4 | 1759 | 1672 | Edit (successful) both arms |
| T5 | 214 | 294 | Edit (successful) both arms |

Max ON M1 = 2505 ≤ 7000 (budget met). Run-8 baselines: T2 2223/905 · T4 2506/1628 · T5 221/240.

## ON-arm kit-surface facts

- SessionStart push delivered 3/3 ON boots (hook_success `content`, verbatim in segments).
  - T2 boot push: named `.sessions/2026-07-11-adoption.md` — status complete (the scripted prepare card; resolved pointer, no trail — nothing had happened yet).
  - T4 boot push: named `.sessions/2026-07-11-session.md` — status **in-progress/drafted, 6 unresolved [[fill:]] slot(s)** + the evidence trail: `code touched (2): cedardonation/cli.py, cedardonation/ops.py · other touched (1): HANDOFF.md · tests touched (1): tests/test_cedardonation.py · git: branch master, HEAD unchanged at 84e8d2fb2 (nothing committed yet)` + "Open that card FIRST".
  - T5 boot push: named `.sessions/2026-07-11-session.md` — status **complete** + the card's resolved pointer carried into the push: "Next session should know: there is no `budgets` list/view command yet —" + "Open that card FIRST". **The push announced NO unresolved state at T5 boot** (contrast run-8: drafted card, 8 slots).
- HANDOFF.md word counts (≤113 pin): T4 boot 86 words (WITH the evidence trail) · T5 boot 67 words · marker line present at every capture.
- ON-T2 FIRST tool call: `ls && echo --- && cat HANDOFF.md 2>/dev/null && echo --- && cat .sessions/2026-07-11-adoption.md 2>/dev/null` (returned the pointer + adoption card).
- ON-T4 FIRST tool call: `cat HANDOFF.md 2>/dev/null; echo "---SESSION CARD---"; cat .sessions/2026-07-11-session.md 2>/dev/null` → 263 words (trail + the 6-slot draft with auto-collected evidence bullets). Its next calls: `git log --oneline -15 && git status` (81 words) then `git diff -- cedardonation/cli.py cedardonation/ops.py tests/test_cedardonation.py` — a diff scoped to EXACTLY the three files the trail named (547 words). Run-8 comparator: ON-T4 ran unscoped `git log -p` re-derivation, 486 words, right after opening an EMPTY card.
- **ON-T4 AUTHORED the card**: read `.sessions/2026-07-11-session.md`, resolved the [[fill:]] slots with real content (decisions, next-session pointer, verify evidence), corrected the stale auto-evidence, flipped Status to `complete`; also appended a discovery to `docs/CAPABILITIES.md`. First family run in which the write-back behavior occurred on any arm.
- ON post-run bare `python3 bootstrap.py check --strict` exit = **0** ("session log .sessions/2026-07-11-session.md complete. / all checks passed."). Run-8: exit=1. NOTE the mechanism: exit 0 realized via T4's genuine card completion, not the #222 drafted-card advisory lane (the card was no longer a draft at arm end).
- Guard-fire windows (advisory, #195 dedupe active): T2 +5 · T4 +1 · T5 +0. Zero acknowledged in any transcript (T2/T5); T4's behavior — opening + completing the card — is what the stop-advisory asks for, recorded as behavior, not as an explicit acknowledgment quote.
- claudeMd-injection channel: ABSENT 0/6 measured segments (no claudeMd attachment/system-reminder block in any stream).

## Test states at end (scripted)

- ON-T2: 13 passed (5 new tests; one mid-task red self-caught and fixed). OFF-T2: 18 passed (6 new).
- ON-T4: 20 passed. OFF-T4: 29 passed.
- ON-T5: 20 passed post-change. OFF-T5: 29 passed post-change.
- Nothing deleted/skipped to force green either arm (diffs).

## T5 shared incident (both arms, verbatim in transcripts)

Both arms committed via `git add cedardonation/cli.py`, sweeping the accumulated uncommitted T2+T4 cli.py work into the one-line-fix commit:
- ON commit 55fd1f7 "Format total command output to two decimal places" — 1 file, +53/−6.
- OFF commit eceb1d0 same subject — 1 file, +37/−16.
Both SELF-DETECTED the sweep ("That commit bundled in pre-existing uncommitted changes…" / "That commit swept in pre-existing uncommitted work…"), both proposed `git reset --soft HEAD~1` and ended ASKING for user approval (headless: none came). Same class as run-8's shared incident.

## T5 signal-visibility precondition (v2 gate)

MET — the push was present verbatim in ON-T5's own context (hook_success content above). But its CONTENT announced a green/complete state (T4 had completed the card), so the run-8-style "visible signal names unresolved state" tension did not exist at T5 boot. ON-T5 never mentioned the card/push/kit; it edited, tested, committed per the prompt. Bare `check --strict` at arm end: exit 0.

## Seam + protocol facts

- Delegation-seam smoke (prepare time, BEFORE arms): PASS — one stream, zero subagents, first user message byte-identical (True), model claude-sonnet-5, 5/5 permission classes green (pytest ×2, append, git add, git commit @ 8f4c2fa in the scratch smoke repo).
- Unmitigated control spawn: DELEGATED 1 subagent, first worker message a PARAPHRASE (byte-identical: False) — run-7/8 signature reproduced A/B same environment.
- Measured seam FLAT 6/6: zero new subagent streams on every spawn; first user message byte-identical to the fenced task text 6/6; segments cold-verified (first user event roots within its own segment). Shared stream file per arm cwd (CLAUDE_CODE_SESSION_ID inheritance) — segments extracted by line offset, run-8 mechanics.
- Prompts byte-identical to run-8's committed prompt set 3/3 (extractor output cmp-verified) — which are byte-identical to run-6's committed worker first messages.
- Prepare CLEAN FIRST TRY (sixth consecutive); seed 711901 accepted first try; `check --strict exit=0` at prepare.
- ZERO reset-relaunches (third consecutive family run).
- PR #220 (rubric §3 v2 alignment) OPEN/parked at run time ⇒ rubric §3 T5 block = v1 wording; T5 judged on the RATIFIED v2 items (bench/tasks/T5.md v2, #181 merged f7aa633) per the run-8 precedent; firing = scripted fact.
