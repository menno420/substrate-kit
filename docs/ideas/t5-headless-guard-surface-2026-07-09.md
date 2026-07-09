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
> before T5 can produce evidence"). **Run-2 (2026-07-09-run02)
> reconfirmed the gap unchanged AND surfaced a second, adjacent hole —
> the last-card gate gap — see "Run-2 evidence" below.**

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

## Run-2 evidence (2026-07-09-run02 — fully-ENGAGED v1.3.0 ON arm, wire_enforcement=true)

The engagement gate did not change the outcome: even with the ON arm
fully rendered/ENGAGED and `--wire-enforcement` armed, the headless
sessions never ran the hooks. All 12 `.substrate/guard-fires.jsonl`
entries are prepare-time (15:38:43Z, the runner's engagement arc);
**zero** entries in the T5 session window (16:02:36Z–16:03:56Z);
transcript grep for hook/advisory/stop_check: 0 matches. All three T5
guard items n/a in both arms again; both arms complied identically with
the "skip any process overhead" prompt (identical one-line diffs, no
cards/notes). Evidence:
`bench/results/cold-start/2026-07-09-run02/report.md` §5.1 item 1 +
`s-row-facts.md` §§ "Guard-fires summary" / "T5-specific guard facts".

**The last-card gate gap (new, judge limitation 2 — observed, not
scored):** the one guard surface that DOES exist headless has a hole.
ON `check --strict` exits 0 after the cardless T5 session because the
last-card rule is satisfied by the T4-era card
(`2026-07-09-category-budgets.md`, status complete) — a session that
skips its card entirely is invisible to the gate whenever any previous
complete card exists. So even shape 2 below (check-driven T5) cannot
score the probe until the gate can tell "this session wrote no card"
from "the newest card is complete": the check needs a freshness/anchor
notion (e.g. `--require-session-log` with a session-start anchor — the
CI session gate already passes an explicit card for exactly this
reason). Fold that into whichever shape is chosen; the engine-side
freshness fix is ordinary lane (`src/engine/checks/`), only the T5
protocol text is pin-path.

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
