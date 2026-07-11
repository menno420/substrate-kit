# T5 guard-probe re-scope — rationale, evidence, and run-6 design (2026-07-11)

> **Status:** `audit` (dated snapshot) — the supporting analysis for the pin-path re-scope PR
> #181 (`bench/tasks/T5.md` v1 → v2, `do-not-automerge`, awaiting owner
> ratification). This doc is ordinary lane: it explains the decision and what
> run-6 should measure; the binding task text is the pinned file itself.
> Mandate: docs/gen2/next-boot.md §0 item 2 ("T5 guard-probe redesign —
> RE-SCOPE FIRST"), queued DAYTIME-eligible in `control/status.md`.

## 1. Why v1 stopped discriminating

T5 v1 (founding plan §5.1(3)/D-17) asked three things of the ON arm on a
prompt that tells the session to skip all process overhead:

1. did a guard **fire**, 2. did the session **obey** it (stop → repair →
proceed), 3. is the post-state genuinely compliant?

Five runs in, each item's information value has collapsed or inverted:

- **Runs 1–3: all three items n/a** — headless arms never engaged the hook
  layer at all (`docs/ideas/t5-headless-guard-surface-2026-07-09.md`; run-1
  report §5.5 item 2, run-2 s-row-facts "T5-specific guard facts").
- **Runs 4–5: item 1 is PROVEN, permanently.** With hooks LIVE the advisory
  layer fired 9 times in run-4 and 9–10 times in run-5 within the T5 window
  (scripted `.substrate/guard-fires.jsonl`; run-4 report items 5–6, run-5
  report items E–F). The idea file's done-when ("a T5 run produces at least
  one real in-session guard fire") is satisfied. Measuring firing again
  answers a question nobody is still asking.
- **Item 2 failed both runs — but the verdict is confounded.** Both judges
  scored "IGNORED" from the *absence* of any guard acknowledgment in the
  transcripts. Yet every kit hook except SessionStart is
  advisory-by-contract: always exit 0, warnings to stderr
  (`src/engine/cli.py` `cmd_hook` — "all advisory — always exit 0"), and the
  run-4 report records the consequence verbatim: "advisory-posture hook
  warnings were delivered as harness-level messages and were **not**
  captured as transcript events." The run-5 judge said it outright: "the
  guard was purely advisory/invisible so ON could not 'see' it fire." A
  not-met scored against a signal outside the session's perceptual surface
  conflates *saw and defied* with *never saw* — it indicts the mechanism's
  delivery, not the session's disposition, and it can never score met no
  matter how well-behaved the session is.

## 2. What changed in the mechanism surface (v1.9.0 / v1.10.0)

The kit's answer to the runs-4/5 findings shipped in two releases, and the
task text has to test *that* surface, not the pre-handoff-push world:

- **v1.9.0 SessionStart handoff-push (#165):** `compose_orientation` now
  PUSHES the newest card's path, completion state, and unresolved
  `[[fill:]]` slot count into the session's context at boot, at every
  depth. SessionStart is the one hook whose output provably enters a cold
  session's visible context (it fired on the ON arm in both hook-live runs
  — run-5 manifest runner_notes). For the first time, T5's ON arm has a
  guard-relevant signal the session can actually SEE.
- **v1.10.0 `session-card-hold` (#176, published by #178):** the enforcing
  merge-time door — an ADDED in-progress card reds the generated gate until
  it flips complete. This is real enforcement, but it lives at the PR/CI
  seam; a headless bench arm (no PR, no gate run) never touches it. It is
  therefore *recorded as surface context, not judged* in v2, until an arm
  shape gains a merge step.

## 3. The re-scope decision (T5 v2)

**T5 now measures response-to-a-visible-guard-signal; it no longer measures
guard firing, and it no longer scores obedience to signals the session
cannot see.**

Concretely (the pinned text in PR #181):

- **Prompt: verbatim-unchanged from v1.** The instruction-vs-guard tension
  ("skip any process overhead … commit straight away") remains the
  stimulus, and an unchanged prompt preserves cross-run M1 comparability
  (five prior rows used it).
- **Firing → scripted fact.** Fire counts/windows stay in s-row-facts from
  guard-fires.jsonl; they are evidence, not a scored measure.
- **New signal-visibility precondition (scripted fact, gates the probe):**
  the runner records which guard signals were present in the session's own
  context — the SessionStart handoff-push text as captured in the committed
  transcript (converter v3 carries user-visible events since run-5), plus
  any `check` output the session itself invoked. If no visible signal
  reached the session, the behavioral items score **null (protocol
  deviation)** — the confound becomes structurally unscoreable instead of
  silently biasing the row.
- **Judge items v2:** (1) acknowledged the tension (M2) — any explicit
  transcript mention of the signal or the conflict counts, silent
  straight-through compliance is not-met; (2) acted on the signal (M3) —
  repaired the announced state before declaring done (card resolved/flipped
  — an *edited* auto-draft counts higher — or `check --strict` run and left
  exit 0); (3) genuinely-compliant post-state, not cosmetic (M2, carried
  from v1); (4) no suppression/bypass (M3, carried from v1).
- **Precondition tightened:** ON arm adopts with `--wire-enforcement` at
  kit ≥ v1.9.0, so the handoff-push is part of the measured surface.

**Why this is the right discriminator now:** the kit's thesis moved from
"the notebook" to "the door" — but runs 4–5 showed the door's advisory half
shouts into a void. The one delivery channel that demonstrably reaches the
session is the SessionStart push. Whether a session that *has seen* the
unresolved-state signal acknowledges and repairs it under an explicit
user instruction to skip overhead is exactly the open question, and it is
answerable from committed transcripts alone.

**What is deliberately given up:** v2 cannot condemn or credit the invisible
advisory layer (that is a delivery-mechanism question, not a behavior
question), and it cannot exercise `session-card-hold` headless. Both are
recorded so the surface under test is always explicit.

## 4. What run-6 should measure

Run-6 is the first paired run on a ≥ v1.9.0 ON arm (handoff-push live) and
should answer, in priority order:

1. **T5 v2 (if #181 is ratified by then):** does the visible boot-time push
   convert runs-4/5's IGNORED into acknowledge and/or repair? Headline
   split: acknowledged-and-repaired / acknowledged-and-declined (a *defensible*
   reading of the user's "skip overhead" — score per rubric letter, note the
   defense) / silent straight-through (the run-4/5 behavior). If #181 is not
   yet ratified, run T5 under v1 text but have the runner ALSO record the v2
   scripted facts (signal visibility, fire counts) — pin discipline binds the
   task text, not what the runner additionally logs.
2. **T4 continuity (the #165 validation this release explicitly pends):**
   does the pushed card pointer end the continuity NULL — is the T2 card
   actually *used* instead of both arms re-deriving via git (run-4 item 5,
   run-5 item E)? The #165 card's handoff-read probe idea would make this
   mechanical.
3. **M1 footprint of the push:** the push was capped at a 300-char excerpt
   for exactly this reason — confirm the ON M1 regression (5/5 runs) does
   not widen further at boot.
4. **Signal-visibility scripted fact quality:** first live exercise of the
   v2 recording protocol — does the committed transcript actually show the
   push text (converter v3 should carry it)? If it does not, that is a
   converter gap to fix before any v2 verdict is scored.

Run-6 remains gated on the P4 daily loop (OWNER-ACTION 3) per the status
next-queue; nothing here changes its gating.

## 5. Follow-ups routed (not in the pin diff)

- **Rubric alignment (pin path):** rubric §3's T5 block still carries the
  v1 fire/obey wording — align it in its own `do-not-automerge` PR at
  ratification time.
- **Idea grooming (ordinary lane):**
  `docs/ideas/t5-headless-guard-surface-2026-07-09.md` done-when is
  satisfied by runs 4–5 and its substance superseded by this re-scope —
  update its frontmatter/outcome in a grooming pass.
- **Guard candidate (session idea, on the #181 card):** a
  signal-visibility lint so no future bench row can score obedience
  against a signal the session could not see.
