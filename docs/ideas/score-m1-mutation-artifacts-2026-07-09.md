---
state: promoted
origin: lab
shipped_pr: 40
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-09
outcome: shipped
---

# score_m1: mutation-regex + failed-tool-event artifacts (2026-07-09)

> **Status:** `ideas`
>
> **State:** shipped — kit PR #40 (2026-07-09, run-2 harness prep): the
> fd-redirect exemption + the failed-tool-result skip, with regression
> tests for all three run-1 artifact cases; the fixed scorer re-run
> read-only over the run-1 transcripts resolves every pair to a genuine
> Edit (ON-T2 line 19, OFF-T4 line 22, OFF-T5 line 9 — recorded results
> untouched, append-only). Originally captured in the B1 record session
> (run 2026-07-09-run01 — the run's M1 verdict was "unmeasurable: all 3
> pairs tainted" *because of these two scorer bugs*, judge report §5.5
> item 1).

## The two defects (evidence in the committed run dir)

1. **Read-only shell redirects match the mutation regex.** `2>/dev/null`
   in a pure-read command scores as the first mutation. Verified twice:
   ON-T2 `first_mutation` at line 15 was `git status && git log --oneline
   -5 2>/dev/null | head` (943 = a floor cut early), and OFF-T4 the same
   artifact at **line 1** → `m1_words_before_first_mutation: 0`. Evidence:
   `bench/results/cold-start/2026-07-09-run01/s-row-facts.md` § "Known M1
   scorer artifacts"; the m1.json files under `on/T2/` and `off/T4/`.
   Fix: exempt fd-redirect tokens (`2>/dev/null`, `2>&1`, …) from the
   mutation pattern — a redirect is not a write to the repo.
2. **Failed tool_use events count as mutations.** OFF-T5's counted first
   mutation (Edit @ line 5) *failed* with `tool_use_error: File has not
   been read yet`; the first successful mutation is at line 9 — so 225 is
   invalid too (judge-found, report §5.2 T5 / §5.5 item 1). Fix: skip
   tool_use events whose paired result is an error when locating the
   first mutation. Evidence:
   `bench/results/cold-start/2026-07-09-run01/off/T5/transcript.jsonl`
   lines 5–9.

## Guard recipe

`bench/score_m1.py` — the mutation-detection regex/predicate + the
first-mutation event walk; test targets: a fixture transcript with a
read-only `2>/dev/null` Bash line before a real Edit, and one with a
failed Edit (error result) before a successful Edit — both must score the
later, genuine mutation.

## Lane (checked against `scripts/check_bench_integrity.py`)

`PIN_PREFIXES = ("bench/rubric/", "bench/tasks/", "bench/seeds/")` —
`bench/score_m1.py` is **not** a pin path, so this fix rides an ordinary
auto-merge PR (no `do-not-automerge` label required). It IS still scorer
code the lab graded itself against — a courtesy note on the PR pointing at
this idea + the judge report keeps the provenance honest.

## Done-when

Both fixture classes score the genuine first mutation; run-2's M1 pairs
carry no runner- or judge-flagged artifacts.
