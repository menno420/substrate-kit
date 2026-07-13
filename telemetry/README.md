# telemetry/ — the kit repo's own JSONL feeds

> **Status:** `living-ledger`
>
> Band KL-3 (founding plan §5.2/§5.3, D6). This directory is the kit repo's
> **per-repo** telemetry home — the same shape every adopted consumer carries.
> Feeds are append-only JSONL (atomic appends beat rewriting a JSON array,
> plan D-10); the console exporter renders declared JSON arrays from them.

## `model-usage.jsonl` — the PL-004 model-allocation dataset (B2)

One record per session, harvested by `session-close` from the session card's
run-report line:

```
- **📊 Model:** <model> · <effort> · <task-class>[ · <tokens_out>]
```

Record shape (nulls are honest gaps, never fabricated — KF-9):

```json
{"session": "2026-07-09-kl3-telemetry", "date": "2026-07-09",
 "model": "fable-5", "effort": "high", "task_class": "test writing",
 "tokens_out": null,
 "outcome": {"ci_green_first_push": null, "checker_findings": null,
             "merged_pr": null, "reverted_within_window": null}}
```

- `task_class` ∈ the 9 PL-004 classes verbatim (the 8 founding Q-0248
  classes + the PL-010 amendment): docs-only · mechanical refactor ·
  test writing · runtime bugfix · kernel/architecture design ·
  review/verify · research · idea/planning · feature build.
- `tokens_out` is null until a programmatic meter exists; estimates are
  labeled estimates (KF-9).
- `outcome` fields are backfilled by the lab loop's telemetry sweep (CI
  result + merged PR via the GitHub API; `reverted_within_window` after the
  14-day KF-8 window) — a session never grades its own outcome.

## Guard fires — `.substrate/guard-fires.jsonl` (B3)

Guard-fire records live in the install's state dir (`.substrate/`), not
here: they are written by the two local choke points (`check`'s finding
loop, `hook`'s dispatch) in every adopted repo, this one included. The `ci`
surface and `did_not_run` rows are **derived by readers from the GitHub
Checks API, never written in CI** (a JSONL appended in an Actions runner
dies with the job). Triage happens through the reasons-required allowlist
(`.substrate/check-exceptions.yml`): creating an entry IS the
false_positive/accepted_risk verdict event, and reason-less entries are
refused. Lab-side aggregation lands in `bench/results/guards/` (band KL-5+).

The JSONL is a **committed ledger** (founding plan KF-11), so a `check` run
that appends records legitimately dirties the tracked file — `check` prints
one summary line whenever it did. Stage the guard-fires delta with your
session's close-out commit; never `git checkout --` it away.

## `allocation-ladder.md`

The program-wide model-for-task ladder (PL-004 layer 2) — seeded from the
founding plan §5.2, revised **only with a citation to dataset rows** from
`model-usage.jsonl` / the B2 paired A/Bs.
