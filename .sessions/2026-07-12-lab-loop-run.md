# 2026-07-12 — lab-loop: friction-inbox clear (stopgap run)

> **Status:** `in-progress`

Run type: routine · lab

- **📊 Model:** fable-5 · high · lab-loop

⚑ **Model-class deviation (D-11):** the lab loop's default is Sonnet-class;
this run executes on the seat's Fable-class model because the daily trigger
missed its 06:08Z fire again and the slice rides the coordinator's stopgap
doctrine in-session (PR #257's ROUTINE STATE record) — not a scheduled
fresh-session fire. D3's ≥3-fire count is NOT advanced by this run.

## Scope (what is about to happen)

Stopgap in-session execution of the daily kit-lab loop slice per
`docs/operations/lab-loop.md`. STEP 1 (friction triage) found the inbox
NON-empty: issues #36–#39, all filed 2026-07-09 from the fleet adoption
review, none ever dispositioned. STEP 2 pick — under the owner's 2026-07-11
feature FREEZE (v1.12.1 cut), the slice IS the friction-inbox clear: verify
each report against kit v1.12.1 source, disposition each issue
(comment + close per the runbook), route the still-real residuals into
`docs/ideas/` backlog files, and append the four triage rows to
`bench/results/friction/index.json` (the triage-time evidence family,
`bench/README.md` — append-only). Zero code, zero new checker/command/
template surface (freeze-compatible). Bench run-10 stays honestly gated:
⚑ 14/15 (pin PRs #220/#238) unratified, and this seat neither runs arms
inline nor spawns runners.

Claim handled in-PR (the #257 stopgap precedent): single-seat,
coordinator-directed slice; this born-red PR opened at session start is the
in-flight signal.

## Close-out

(written at flip time)
