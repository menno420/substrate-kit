# 2026-07-11 — T5 probe v3 re-shape: runner-seeded drafted state (pin path)

> **Status:** `complete` *(the WORK is complete; the PR itself PARKS open —
> see "Parked by design" below. An open, unmerged state for this PR is
> correct, not abandoned.)*

- **📊 Model:** fable-5 · high · bench-pin

## Scope (what is about to happen)

About to re-shape `bench/tasks/T5.md` to v3 per run-9 report §5.5
(`bench/results/cold-start/2026-07-11-run09/report.md`) — pin path.

## Parked by design (pin path §5.0)

This PR touches `bench/tasks/` — pin path. It opens READY, is labeled
`do-not-automerge` from open (bench-integrity rule 1), is NEVER armed for
auto-merge, and is never merged by its authoring session — it parks for
owner ratification exactly like #181 and #220. An open, unmerged end state
for this PR is correct, not abandoned.

## Close-out (what happened)

Shipped the declared scope exactly: `bench/tasks/T5.md` re-shaped v2 → v3
in three edits, diff = T5.md + this card ONLY. (1) Status paragraph
rewritten to v3 provenance: run-9 proved v2 degenerate post-#222 — T4 now
authors and flips the session card, so the SessionStart push at T5 boot
announces a COMPLETE state and the skip-vs-ritual tension never arises
(run-9: v2-1 not-met/silent but low-stakes, v2-2 n-a). (2) New
**Seed-state precondition** block inserted after the existing
Precondition: runner clean-tree chore commit on both arms (retires the
runs-8/9 4/4-identical `git add <pkg>/cli.py` commit-sweep confound — ON
b6c4dfb/55fd1f7, OFF a6763f9/eceb1d0), drafted-card seed on the ON arm
(regenerate the engine auto-draft post-T4, dated newer, so the push
announces an unresolved card and "Open that card FIRST"), and a
probe-validity gate (seed failed → items 1–2 null — protocol deviation,
never not-met). (3) Judge-items intro parenthetical updated: v2 set
unchanged in v3; rubric alignment rides pin PR #220, which needs no
re-cut because v3's seeded state reproduces the run-8 drafted-card shape
its grounding examples cite. Task prompt, runner-notes firing/visibility
bullets, judge items 1–4, and the out-of-scope-headless paragraph are
byte-identical to v2.

Verification on this branch: `python3 -m pytest tests/ -q` → **1046
passed in 17.90s**; `python3 scripts/check_bench_integrity.py --base
origin/main` exit=0 ("1 bench/ change(s) — OK"); `python3
dist/bootstrap.py check --strict` exit=1 at the born-red stage was this
card's own designed hold ("HOLD (by design) … nothing to investigate"),
green once this flip lands.

Parked per the "Parked by design" section above: READY, labeled
`do-not-automerge` at open, auto-merge verified NOT armed, terminal state
is the owner's click — merge = ratify, close with a word = reject. Claim
`control/claims/t5-v3-probe-reshape.md` (#237) is cleared by the separate
status close-out fast-lane PR, which also records the parked PR as ⚑
OWNER-ACTION 15 pairing with #220 (⚑ 14).

## Session enders

- 💡 **Session idea:** the v3 seed steps are specified as runner
  *procedure* in task text only — `run_ab.py` has no `--seed-t5` support,
  so run-10's runner must hand-execute the clean-tree commit and
  drafted-card regen between T4 and T5. Implement them as a harness step
  (with the seeded facts auto-written into s-row-facts) so the
  probe-validity gate can never fail from a forgotten manual step — the
  same "script the precondition you score against" move that made the v2
  signal-visibility fact reliable.
- ⟲ **Previous-session review:** the run-9 scoring session's report §5.5
  did exactly what a bench report should — it didn't stop at scoring the
  degenerate v2 rows, it diagnosed WHY they were degenerate (T4's
  post-#222 write-back), separated kit behavior from chain artifacts (the
  4/4 commit-sweep), and left a buildable re-shape spec this session
  executed nearly verbatim. One improvement it surfaces: the report
  flagged the commit-sweep confound as "unmeasured for two runs" — a
  confound first seen in run-8 should trigger a same-run harness/task fix
  proposal rather than waiting for a second confirming run.
- **Docs audit:** everything from this session lives in its durable homes
  — the re-shape rationale in T5.md's Status paragraph (self-documenting,
  like v2), the parked-PR record + pairing in control/status.md ⚑ 15 (the
  close-out PR), provenance in this card. Nothing chat-only remains.

## Next session should know

- This PR parks OPEN awaiting owner ratification — do not "clean it up",
  re-arm it, update-branch it, or close it; terminal state is the owner's
  click (same law as #181/#220).
- PAIRING: #220 (rubric §3 v2 alignment, ⚑ 14) + this PR (⚑ 15) ratify
  independently but land best together — judge items are unchanged from
  v2, so #220's rubric text scores v3 as-is; one click each gives run-10
  a coherent text+rubric pair.
- Run-10's runner must execute the v3 seed steps manually (task text is
  the spec); harness support in `run_ab.py` is an optional follow-up (see
  💡 above).
