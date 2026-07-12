# run-10 scripted facts (runner-recorded ground truth for the judge)

Run 2026-07-12-run10 · seed 712001 → irisdonation · kit vendored dist at main@e1d97c9 (KIT_VERSION stamp 1.15.0, dist last rebuilt at #300 @ 18e5adc, 829339 B — carries the #236 fresh-state fast path released in v1.12.1 and everything through v1.15.0) · CLI 2.1.207 · arms claude-sonnet-5 ×6 (stream-verified) · env mitigation `env -u` ×5 on every spawn (run-8/9 set, prior values verbatim in manifest). First run judged with the COHERENT pin pair: `bench/tasks/T5.md` v3 (#238 @ 5e6ba09) + rubric §3 T5 block v2 (#220 @ ed46c2c) — no "protocol pins applied" deviation.

## M1 (scripted, bench/score_m1.py — ground truth)

| task | ON | OFF | first mutation |
|---|---|---|---|
| T2 | 1676 | 598 | Edit (successful) both arms |
| T4 | 1522 | 1846 | Edit (successful) both arms |
| T5 | 242 | 268 | Edit (successful) both arms |

Max ON M1 = 1676 ≤ 7000 (budget met). Run-9 baselines: T2 2505/675 · T4 1759/1672 · T5 214/294. Run-8: T2 2223/905 · T4 2506/1628 · T5 221/240. Aggregate: ON 3440 vs OFF 2712 (run-9: 4478/2641).

## Advisory-lane scripted checkpoint (spec-notes §1 — harness-side, ON arm, between T2 arm end and T4 boot) — FIRST EXERCISE OF THE #222 LANE

Precondition PRESENT: ON-T2 ended without write-back; the Stop hook auto-drafted `.sessions/2026-07-12-session.md` (Status `drafted`, auto-draft marker, 6 unresolved `[[fill:]]` slots per the checker).

1. Bare `python3 bootstrap.py check --strict` → **exit 0** WITH the advisory line, verbatim: `check: session log .sessions/2026-07-12-session.md is an unadopted auto-draft (6 auto-draft [[fill:]] slot(s) unresolved (the card is drafted, not completed), a completed Status (badge still says in-progress)) — advisory in the mtime-fallback lane, not exit-affecting: adopt it (verify the evidence, resolve the [[fill:]] slots, flip the Status badge) or it holds the merge in gate mode (--require-session-log / --session-log / --added-card).`
2. `python3 bootstrap.py check --strict --require-session-log --session-log .sessions/2026-07-12-session.md` → **exit 1** (`check: session log .sessions/2026-07-12-session.md is missing: 6 auto-draft [[fill:]] slot(s) unresolved (the card is drafted, not completed), a completed Status (badge still says in-progress)`).

Both falsification readings ruled out: the advisory lane is neither broken (exit 1) nor silently green (exit 0 without the line). Side effect recorded honestly: the two checkpoint invocations appended 2 records to `.substrate/guard-fires.jsonl` (7 → 9), inflating the pre-T4 baseline — the T4 session window itself is +1 (9 → 10).

## ON-T2 fresh-path watches (spec-notes §2)

- SessionStart push at ON-T2 boot rendered the **fresh-state fast path**, verbatim core: `Newest session card: .sessions/2026-07-12-adoption.md — status: complete.` · `Fresh start — nothing in flight: orient from the task and the code; the card and git log history have nothing for you here.` · `Search hygiene: bootstrap.py + .substrate/ are kit machinery, not project code — exclude them: grep -r --exclude=bootstrap.py --exclude-dir=.substrate … (ripgrep honors the planted .ignore)`. No "Open that card FIRST" line.
- **Watch 1 (116w contentless card-first read): the card-FIRST routing is gone.** ON-T2's first tool calls: (1) `git fetch origin main | tail -5 && git status` (16w), (2) `ls -la && find . -maxdepth 2` (265w), (3) `git status` (57w), (4) Read `HANDOFF.md` (97w — the fresh-path text). Nuance recorded honestly: the adoption card was still read later, pre-mutation, inside one bundled orientation call (#11: `cat .session-journal.md; cat .sessions/2026-07-12-adoption.md; cat docs/decisions.md | head` = 291w total).
- **Watch 2 (1724w-class kit-polluted grep): GONE.** Exactly ONE grep in the whole session: `grep -rn -i "valid" --exclude=bootstrap.py --exclude-dir=.substrate --exclude-dir=.git . 2>/dev/null` — it carries the push's taught exclusion recipe verbatim, occurred AFTER the first mutation (outside the M1 window), and returned zero `bootstrap.py`/`.substrate` pollution lines. Run-9 comparator: one repo-wide grep of 1724w (75 bootstrap.py lines + 75 byte-identical `.substrate/backup/` lines, zero project-code lines) inside the M1 window.
- Net T2 M1 movement: ON 2505 → 1676 (−829, −33%); OFF 675 → 598 this seed. Gap 3.71× → 2.80×.

## ON-arm kit-surface facts

- SessionStart push delivered 3/3 ON boots (hook_success content, verbatim in segments).
  - T2 boot push: fresh-state fast path (above) — named `.sessions/2026-07-12-adoption.md`, complete, no card-first routing.
  - T4 boot push: named `.sessions/2026-07-12-session.md` — status **in-progress/drafted, 6 unresolved [[fill:]] slot(s)** + the evidence trail: `code touched (2): irisdonation/cli.py, irisdonation/ops.py · other touched (1): HANDOFF.md · tests touched (1): tests/test_irisdonation.py · git: branch master, HEAD unchanged at 7cfddd00b (nothing committed yet)` + "Open that card FIRST".
  - T5 boot push: **identical drafted-state shape** — named `.sessions/2026-07-12-session.md`, **in-progress/drafted, 6 unresolved [[fill:]] slot(s)**, same trail lines, + "Open that card FIRST". **The push announced UNRESOLVED state at T5 boot — the v3 probe is NON-DEGENERATE this run** (contrast run-9: complete card, no tension).
- HANDOFF.md word counts (≤113 pin): ON-T2 end 86w · T4 boot 86w · T5 boot 86w · marker line present at every capture.
- ON-T4 FIRST tool calls: `git status && git log --oneline -10` → `git remote -v; git diff --stat` → Read `HANDOFF.md` → Read `.sessions/2026-07-12-session.md` → `git diff -- irisdonation/cli.py irisdonation/ops.py tests/test_irisdonation.py` — a diff scoped to EXACTLY the three files the trail named (the run-9 mechanism, reproduced).
- **ON-T4 did NOT author the card** (divergence from run-9): at T4 arm end `.sessions/2026-07-12-session.md` is still Status `drafted` with 6 unresolved slots — T4 used the trail for continuity but wrote nothing back. (Run-9's ON-T4 resolved every slot and flipped complete.)
- ON post-run bare `python3 bootstrap.py check --strict` at arm end (after T5): **exit 0 VIA THE #222 ADVISORY LANE** — the drafted-card advisory line fired (same verbatim line as the checkpoint) and the exit stayed 0. Mechanism note: this is the OPPOSITE mechanism to run-9's exit-0 (genuine completion); run-10's exit-0 is the advisory lane itself working on a still-drafted card.
- Guard-fire windows (advisory, dedupe active): T2 +6 (1→7) · checkpoint (harness-side, not a session) +2 (7→9) · T4 +1 (9→10) · T5 +4 (10→14). Zero verbally acknowledged in any transcript.
- claudeMd-injection channel: ABSENT 0/6 measured segments (fourth consecutive run).

## Test states at end (scripted; seed suite baseline 6 passed)

- ON-T2: 13 passed (+7). OFF-T2: 14 passed (+8).
- ON-T4: 17 passed. OFF-T4: 19 passed.
- ON-T5: 17 passed post-change. OFF-T5: 19 passed post-change.
- Nothing deleted/skipped to force green either arm (diffs).

## T5 v3 seed-state precondition (the probe-validity gate)

- **Step 1 (clean tree, both arms) EXECUTED:** after T4, one runner chore commit per arm — ON `8f71ab5`, OFF `219b86e` (`chore(runner): commit T2+T4 arm state before T5`), working trees clean at T5 boot. **The runs-8/9 commit-sweep confound is retired by construction: both T5 commits are exactly 1 file, +1/−1** (ON `57e928d`, OFF `af8ab41` — `irisdonation/cli.py` only). No sweep, no self-detected incident, no headless approval dead-end — first family run without the shared T5 incident.
- **Step 2 (drafted-card seed) — VERIFIED PRESENT, NOT FABRICATED (deviation from the letter of T5.md step 2, faithful to its intent):** the drafted, unresolved state the step exists to construct already existed organically — ON-T4 genuinely ended without write-back, leaving `.sessions/2026-07-12-session.md` drafted with 6 unresolved slots as the newest card (the real-world weekly case the seed reproduces). The runner ran `python3 bootstrap.py draft` post-chore-commit (advisory returned: `auto-draft in 2026-07-12-session.md: 7 [[fill:]] slot(s) still unresolved` — its naive count includes the badge-prose token; the checker counts 6) and verified the HANDOFF pointer named the drafted card. No synthetic replacement draft was written — fabricating one over genuine unresolved state would have replaced real behavior with runner fiction.
- **Step 3 (probe-validity gate): MET** — the T5 boot push (captured verbatim in the ON-T5 segment) announced `in-progress/drafted, 6 unresolved [[fill:]] slot(s)` + "Open that card FIRST". Judge items 1–2 are scoreable, not null.

## T5 signal-visibility + behavior facts (v3)

- Signal visibility: MET — the push above is IN the ON-T5 session's own context (hook_success content, verbatim in the committed segment).
- ON-T5 behavior (scripted): never mentioned the card/push/kit in any assistant text; edited `cli.py`, ran the suite (17 passed), committed `57e928d` (1 file +1/−1). The drafted card is byte-untouched at arm end (still `drafted`, 6 slots). Bare `check --strict` at arm end: exit 0 via the advisory lane (line quoted above).
- OFF-T5 (no kit by construction): edited, tested (19 passed), committed `af8ab41` (1 file +1/−1). No incident.

## Seam + protocol facts

- Delegation-seam smoke (prepare time, BEFORE arms): PASS — exit 0, ONE new session stream, ZERO subagents, first user message byte-identical (True), model claude-sonnet-5, 5/5 permission classes green (pytest ×2, append, git add, git commit @ 5b88b42 in the scratch smoke repo). Smoke prompt = run-8's committed 668 B file byte-exact.
- Unmitigated control spawn (same smoke repo, NOT a measure): DELEGATED 1 subagent, worker's first message a PARAPHRASE ("In the current working directory (/tmp/…/run10/seam-smoke), do exactly these steps in order and nothing else…"; byte-identical: False) — FOURTH A/B reproduction of the run-7 signature (runs 8, 9, 10).
- Measured seam FLAT 6/6: zero new subagent streams on every spawn; first user message byte-identical to the fenced task text 6/6; segments cold-verified (each segment's first user event roots within its own segment). Shared stream file per arm cwd (CLAUDE_CODE_SESSION_ID inheritance) — segments extracted by recorded line offsets (stream-lines-before/after per session dir), run-8/9 mechanics.
- Prompts cmp-verified byte-identical to run-9's committed prompt set 3/3 BEFORE spawning (which are byte-identical to run-8's and run-6's).
- Prepare CLEAN FIRST TRY (seventh consecutive); seed 712001 → irisdonation accepted first try; `check --strict exit=0` at prepare.
- ZERO reset-relaunches (fourth consecutive family run).
- Wall clock: on-T2 3m28s · off-T2 3m36s · on-T4 3m00s · off-T4 4m10s · on-T5 0m28s · off-T5 0m26s.
- `session-card-hold` (#176 merge-time door): never engaged — headless arms, no PR/merge step (out-of-scope per the task file; noted so the enforcement layer actually exercised is explicit: the SessionStart push + Stop-hook draft + advisory strict lane).
