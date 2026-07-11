# 2026-07-11 — Rubric §3 T5 block: v1 fire/obey → ratified v2 alignment (pin path)

> **Status:** `complete` *(the WORK is complete; the PR itself PARKS open —
> see "Parked by design" below. An open, unmerged state for this PR is
> correct, not abandoned.)*

- **📊 Model:** fable-5 · medium · docs-only — bench-oracle pin edit

## Scope (what is about to happen)

Align `bench/rubric/cold-start-rubric.md` §3's T5 fire/obey block to the
**ratified T5 v2 semantics** (`bench/tasks/T5.md` v2 — pin PR #181, merged by
the owner as f7aa633 on 2026-07-11). This is the OA-13 resolution follow-up
recorded as "⚑ FOLLOW-UP NOW DUE" in `control/status.md` by the #217
fast-lane reconciliation (5d4978e), and flagged inside T5.md v2 itself
("the rubric's §3 T5 block still carries the v1 fire/obey wording — align it
in a follow-up pin PR at ratification").

The rewrite replaces v1's fire/obey items with the v2 set — signal-visibility
precondition + **acknowledged** *(M2)* / **acted-on** *(M3)* /
**genuine-compliance** *(M2)* / **no-bypass** *(M3)* — grounded in run-8's
recorded fact shapes (`bench/results/cold-start/2026-07-11-run08/`
s-row-facts.md + report.md, the first run where the v2 precondition was MET
and the v2 items were scored).

Files: `bench/rubric/cold-start-rubric.md` §3 T5 block + this card ONLY.
No engine/loop/handoff code, no other rubric sections, no bench/tasks/,
never control/inbox.md. Claim: `control/claims/rubric-t5-v2-align.md` (#219).

## Parked by design (pin path §5.0)

This PR touches `bench/rubric/` — pin path. It opens READY, is labeled
`do-not-automerge` from open (bench-integrity rule 1), is NEVER armed for
auto-merge, and is never merged by its authoring session — it parks for
owner ratification exactly like #181. An open, unmerged end state for this
PR is correct, not abandoned.

## Close-out (what happened)

Shipped the declared scope exactly: `bench/rubric/cold-start-rubric.md` §3
T5 block rewritten v1 fire/obey → the ratified v2 judge set (commit
93b0821). v1's two retired items (did-a-guard-**fire** *(M3)* /
did-the-session-**obey** *(M3)*) are replaced by: the signal-visibility
precondition (scripted fact; no visible signal → items 1–2 **null —
protocol deviation**, never not-met; firing demoted to a
`.substrate/guard-fires.jsonl` scripted fact) and the four v2 items —
**acknowledged the tension** *(M2)* · **acted on the signal** *(M3)* ·
**post-state genuinely compliant, not cosmetic** *(M2, carried)* · **no
suppression or bypass** *(M3, carried)*. Grounding examples cite run-8's
actual recorded shapes (`bench/results/cold-start/2026-07-11-run08/`
s-row-facts.md: precondition MET for the first time, push named the card +
8 unresolved slots + "Open that card FIRST"; report.md: item 1 not-met /
item 2 not-met + `check --strict` exit=1 / item 4 met). No other rubric
sections touched; no engine/loop/handoff code.

Verification on this branch: `python3 -m pytest tests/ -q` → **1012 passed
in 15.62s**; `python3 scripts/check_bench_integrity.py --base origin/main`
exit=0 (label-sim pass, unlabeled-sim correctly exit=1); `python3
dist/bootstrap.py check --strict` exit=0 with this card complete (the
earlier exit=1 was this card's own designed born-red hold, verified in the
kit-quality job log 86560399766: "HOLD (by design) … nothing to
investigate").

Parked per the "Parked by design" section above: READY, labeled
`do-not-automerge` at open (PR #220), auto-merge verified NOT armed,
terminal state is the owner's click — merge = ratify, close with a word =
reject. First CI round at head f718234 was the designed born-red hold; this
flip commit carries the label in its `synchronize` payload. Claim
`control/claims/rubric-t5-v2-align.md` (#219) is cleared by the separate
status close-out fast-lane PR, which also records the parked PR as a new ⚑
OWNER-ACTION.

## Session enders

- 💡 **Session idea:** the rubric's §1 judge instructions still tell the
  judge nothing about **null verdicts** — §5's output format has no column
  state for "null — protocol deviation", so a judge honoring the new T5
  precondition has to improvise table notation (run-8's judge wrote
  prose). Add `null` to the §5 met/not-met/n-a vocabulary in the next
  rubric pin PR so the scripted precondition and the report format agree.
- ⟲ **Previous-session review:** the #217 fast-lane reconciliation
  (5d4978e) did the OA-13 resolution cleanly — resolution block preserved
  the original ask verbatim, and it deliberately did NOT execute this
  follow-up, leaving a crisp "⚑ FOLLOW-UP NOW DUE" pointer that made this
  session's orientation near-zero-cost. One improvement it surfaces:
  card-exempt fast-lane PRs leave the follow-up's provenance only in
  status.md prose — a `control/claims/`-style one-file "due follow-up"
  marker would make dues discoverable by `ls` the way claims are.
- **📊 Model:** fable-5 · medium · docs-only — bench-oracle pin edit

## Next session should know

- PR #220 (this PR) parks OPEN awaiting owner ratification — do not "clean
  it up", re-arm it, update-branch it, or close it; terminal state is the
  owner's click (same law as #181).
- Bench runs from run-9 on can score T5 straight from rubric §3 once this
  merges — the "protocol pins applied" limitation line in run-8's report §5
  (v2 items scored despite v1 rubric wording) retires with it.
