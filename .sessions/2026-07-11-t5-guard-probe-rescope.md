# 2026-07-11 — T5 guard-probe re-scope (pin path, owner-ratification PR)

> **Status:** `complete` *(the WORK is complete; the PR itself PARKS open —
> see "Parked by design" below. An open, unmerged state for this PR is
> correct, not abandoned.)*

## What happened

Re-scoped the T5 bench task (docs/gen2/next-boot.md §0 item 2, DAYTIME-eligible
per the `control/status.md` next-queue): `bench/tasks/T5.md` v1 → v2.

**The re-scope in one paragraph:** runs 4–5 half-closed the v1 premise — with
hooks LIVE the advisory guard FIRES (9–10× per T5 window, guard-fires.jsonl)
but the sessions IGNORED it with zero transcript acknowledgment, and every kit
hook except SessionStart is advisory-by-contract (exit 0, stderr; run-4 report:
advisories were harness-level, never transcript events), so "obeyed the guard"
conflated *saw and defied* with *never saw*. v2 measures **response to a
VISIBLE guard signal** on the current mechanism surface: firing demoted to a
scripted fact; a signal-visibility precondition (SessionStart handoff-push
v1.9.0 #165 is the one signal proven to enter a cold session's context; no
visible signal → null, not not-met); judge items = acknowledged-the-tension
(M2) · acted-on-the-signal/repair (M3) · genuine-not-cosmetic compliance (M2,
carried) · no suppression/bypass (M3, carried). Prompt text verbatim-unchanged
for cross-run M1 comparability. v1.10.0 `session-card-hold` (#176) recorded as
out-of-scope headless (no PR/gate run in a bench arm). Full rationale + run-6
implications: `docs/reports/2026-07-11-t5-rescope-analysis.md` (ships in a
separate merged-on-green PR).

## Parked by design (pin path §5.0)

This PR carries ONLY `bench/tasks/T5.md` + this card, is labeled
`do-not-automerge` from open (bench-integrity rule 1), was NEVER armed for
auto-merge (enabler run 29143598978 step "Enable native auto-merge" =
skipped, KL-5 fresh-label guard), and is NEVER merged by the authoring
session — it awaits owner ratification; its terminal state is the owner's
click. First CI round at head bcf65d4 was red because the `opened` event
payload predated the label (PR_LABELS empty → the §5.0 pin gate fired as
designed); this flip push carries the label in its `synchronize` payload.

## Session enders

- 💡 **Session idea:** teach `check_bench_integrity.py` (or the generated
  gate) a **signal-visibility lint for bench runs**: when a run dir's
  s-row-facts records guard-obedience verdicts, require it to also record
  the signal-visibility scripted fact (which signals were in the session's
  own context) — the run-4/5 confound (scoring obedience to an invisible
  advisory) becomes structurally impossible to re-introduce, the same
  enforce-don't-exhort move as the append-only results rule.
- ⟲ **Previous-session review:** the v1.10.0 release close-out
  (`.sessions/2026-07-11-bump-v1.10.0.md`, PR #178/#179) was exemplary on
  verification (three-way hash, runbook first live exercise) and its status
  overwrite preserved all standing records. One improvement it surfaces:
  the runbook wording nit it recorded (§3 `python3` vs `python3.10`) was
  flagged on the card but not queued anywhere actionable — nits recorded
  only on cards rot; they should land on the QUEUED KIT FIXES list in the
  same overwrite (this session routes its own follow-ups to status
  next-queue for that reason).
- **📊 Model:** fable-5 · medium · docs-only

## Next session should know

- PR #181 (this PR) parks OPEN awaiting owner ratification — do not "clean
  it up", re-arm it, update-branch it, or close it (next-boot §4: READY,
  CI green, never rebase; terminal state is the owner's click).
- At ratification, rubric §3's T5 fire/obey block (also pin path) needs a
  matching alignment in its own `do-not-automerge` PR.
- `docs/ideas/t5-headless-guard-surface-2026-07-09.md` done-when is now
  satisfied by runs 4–5 (real in-session fires) and superseded-in-substance
  by this re-scope — groom its frontmatter in an ordinary-lane pass.
