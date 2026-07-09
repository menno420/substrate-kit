---
state: captured
origin: lab
shipped_pr: null
shipped_repo: null
merged_date: null
outcome: open
---

# T5 protocol: headless arms never engage the hook layer (2026-07-09)

> **Status:** `ideas`
>
> **State:** captured (B1 record session, run 2026-07-09-run01 — the T5
> guard probe, the entire point of the task, produced **zero** guard
> evidence; judge report §5.5 item 2 calls it "a protocol deviation to fix
> before T5 can produce evidence").

## The gap

T5's precondition says the session-log gate and Stop hook are LIVE
(`--wire-enforcement` arms), but the bench sessions run **headless** — the
`.claude/` hook layer never engages, no in-session surface runs `check`,
and both arms simply obeyed the "skip any process overhead" prompt.
Result: guard-fire / guard-obey / post-repair items all n/a in BOTH arms;
the run demonstrates only that, unenforced, ON behaves exactly like the
unguarded OFF baseline. Evidence:
`bench/results/cold-start/2026-07-09-run01/report.md` §5.1 T5 table +
§5.5 item 2; `s-row-facts.md` § "T5 guard facts" (both guard-fires.jsonl
entries are runner `check` invocations timestamped before the T5 window).

## Possible shapes (decide at fix time)

1. **Run T5 arms with the hook layer active** — invoke the sessions
   through a harness that honors `.claude/settings.json` hooks (the Stop
   advisory + edit advisors actually fire in-session).
2. **Redesign T5 around check-driven guards** — an enforcement surface
   that exists headless: e.g. the arm's protocol runs `check --strict`
   inside the session flow (or a wrapper fails the task on red), so the
   guard's fire/obey/repair arc is observable without the hook layer.

Either way the fix touches `bench/tasks/T5.md` and/or the run protocol in
`bench/README.md` / `run_ab.py` — **`bench/tasks/` is a PIN PATH**, so a
T5 text change must ride a `do-not-automerge` owner-review PR
(`check_bench_integrity.py` rule 1).

## Done-when

A T5 run produces at least one real in-session guard fire (or a
deliberate, recorded violation of a live guard) in the ON arm — the
fire/obey/repair items score met/not-met instead of n/a.
