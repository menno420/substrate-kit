# 2026-07-11 — Rubric §3 T5 block: v1 fire/obey → ratified v2 alignment (pin path)

> **Status:** `in-progress`

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
