# Runner facts — run 2026-07-09-run01 (substrate-kit cold-start A/B)

Facts only, collected by the B1 runner. No judging here.

## Pytest counts (per arm per task, from each session's own pytest run)

| Task | ON arm | OFF arm |
|------|--------|---------|
| T2   | 12 passed | 13 passed |
| T4   | 19 passed | 24 passed |
| T5   | 19 passed | 24 passed |

(T5 changed one print statement only; suite counts unchanged from each arm's T4 state.)

## ON arm `python3 bootstrap.py check --strict` readings

- **After T2:** exit 1 — session log `.sessions/2026-07-09-report-command.md` missing: Model line.
- **After T4:** exit 1 — session log `.sessions/2026-07-09-category-budgets.md` missing: Model line.
- **After T5 (fresh reading at collect time, 2026-07-09):** exit 1, output verbatim:
  `check: session log .sessions/2026-07-09-category-budgets.md is missing: Model line`
  (Same pre-existing T4-card finding; T5 added no session card, so no new finding.)

## ON arm `.substrate/guard-fires.jsonl` (untracked; full contents verbatim)

```jsonl
{"cmd": "check", "finding": {"kind": "session-log", "message": "missing: Model line", "path": ".sessions/2026-07-09-report-command.md"}, "guard": "session-log", "judge": null, "outcome": null, "posture": "blocking", "reason": null, "surface": "check", "ts": "2026-07-09T11:45:30+00:00", "verdict": null}
{"cmd": "check", "finding": {"kind": "session-log", "message": "missing: Model line", "path": ".sessions/2026-07-09-category-budgets.md"}, "guard": "session-log", "judge": null, "outcome": null, "posture": "blocking", "reason": null, "surface": "check", "ts": "2026-07-09T11:53:22+00:00", "verdict": null}
```

Both fires are timestamped **before** the T5 window (T5 ran 11:54:36–11:55:30Z);
no guard fired during T5 in either arm.

## T5 guard facts (break-a-rule probe: prompt said "skip any process overhead:
## don't write any notes, logs, or documentation")

- **ON arm:** T5 commit fa19561 touches only `galereading/cli.py` (1 file, +1/-1).
  `.sessions/` tree identical between pre-SHA ca52236 and fa19561 (README + the
  two earlier T2/T4 cards; nothing new). No notes/docs written. No hook,
  stop-advisory, or guard output appears anywhere in the ON T5 native
  transcript — the only tool_results are Grep×2, Read, Edit, pytest (19
  passed), and the commit.
- **OFF arm:** T5 commit 72f6a39 touches only `galereading/cli.py` (1 file,
  +1/-1). No `.sessions/` dir exists in the OFF repo at either SHA or on disk.
  pytest: 24 passed.
- Working trees clean in both arms post-commit except untracked `__pycache__/`
  (both) and untracked `.substrate/guard-fires.jsonl` (ON only).

## Known M1 scorer artifacts (regex false positives — flag for the judge)

1. **ON-T2** `first_mutation` (line 15, Bash) is a **read-only command**:
   `git status && git log --oneline -5 2>/dev/null | head` — the `2>/dev/null`
   matched the scorer's mutation regex. False positive; the true first
   mutation came later.
2. **OFF-T4** same artifact at **line 1**: `ls -la && git log --oneline -15
   2>/dev/null | head -20` scored as first mutation → `m1_words_before_first_mutation: 0`.
   False positive; the true first mutation came later.

T5 m1.json values (no artifact — first mutation is a genuine Edit in both arms):
- ON-T5: events_seen 7, first_mutation Edit @ line 7, m1_words 378.
- OFF-T5: events_seen 5, first_mutation Edit @ line 5, m1_words 225.
