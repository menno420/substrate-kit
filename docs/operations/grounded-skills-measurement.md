# Grounded-skills measurement — pre-registered protocol

> **Status:** `reference`
>
> The frozen before/after measurement protocol for the grounded-skills
> program (wrap report `../reports/2026-07-12-grounded-skills-wrap.md` §3d),
> following the PR #247 methodology precedent
> (`../reports/2026-07-11-adopter-outcomes-measurement.md` — every number
> carries its n and window; honest nulls are headlines). **Pre-registered
> 2026-07-15, before the ~2026-07-19..26 window opens** (#247 §7.1: measure
> against a pre-registered protocol, never retrospectively). Any change to
> the metric definitions below after 2026-07-15 is a protocol amendment —
> record it here with a date and reason, never silently.

## Why this exists

All 8 grounded-skills slices, three releases, and both distribution waves
shipped on 2026-07-12; the program's actual effect on agent behavior was
unmeasurable that day (no post-adoption window existed — wrap report §3d).
The proposal: after a 1–2 week window, compare skill-index usage vs procedure
improvisation, owner-ask field compliance, capability-wall discipline, and
recurring-action throughput against the pre-2026-07-12 session-card record.
This doc freezes the metrics and mechanics now so the window-run session is
turnkey: clone, run one command, interpret, publish.

## The run (turnkey)

1. Confirm the window: run on or after **2026-07-19** (target 2026-07-19..26,
   heartbeat baton; owner silence accepts).
2. From a substrate-kit checkout at origin/main:

   ```
   python3 scripts/measure_grounded_skills.py --clone --workdir /tmp/gsm \
       --json /tmp/gsm/results.json --out /tmp/gsm/report-skeleton.md
   ```

   Read-only throughout (KF-2 — the lab never writes to consumers). The
   roster is `docs/fleet-repos.txt`; a private repo that fails to clone
   (pokemon-mod-lab, expected) is recorded as an honest skip, never guessed.
3. Write the findings report at
   `docs/reports/2026-07-<DD>-grounded-skills-measurement.md` (Status badge
   `audit`), link it from `docs/operations/README.md`, and carry the
   harness's skeleton tables plus the interpretation sections below.
4. Optional API pass (only if latency claims are wanted): PR open→merge
   latency per #247 §2 via the GitHub API — the harness deliberately does
   not fake this from git data. This is available two ways: the standalone
   `scripts/measure_pr_latency.py` (the frozen GSW-4 run, report §7), or the
   harness's opt-in `--api-latency` mode below (same pure logic, re-runnable
   alongside M1–M4).

## Opt-in `--api-latency` mode (graduated from GSW-4)

The harness's default path is local/git-only (M1–M4, no network). Passing
`--api-latency` **also** measures open→merge PR latency via the GitHub API, so
latency is a first-class, re-runnable metric alongside M1–M4 instead of a
one-off script:

```
python3 scripts/measure_grounded_skills.py --clone --workdir /tmp/gsm \
    --json /tmp/gsm/results.json --out /tmp/gsm/report.md --api-latency
```

- **Reuses `scripts/measure_pr_latency.py`'s pure logic — no duplication.**
  The mode loads that script by path (there is no package under `scripts/`)
  and calls its pure bucketing / percentile / aggregation functions plus its
  isolated direct-egress GitHub-API fetch. The frozen GSW-4 artifacts (report
  §7, `docs/reports/data/2026-07-19-grounded-skills-latency.json`) are the
  authoritative run; the `--api-latency` section is the modest re-runnable
  readout (per-repo before/after medians + the pooled fleet aggregate).
- **Token.** Requires a GitHub token in `GITHUB_PAT` / `GH_TOKEN` /
  `GITHUB_TOKEN` (direct egress — the proxied REST path 403s).
- **Cleanly SKIPPED, never errored, offline.** With no token the mode returns
  `status: skipped` **without touching the network** (the token is resolved
  before any session opens); a network / rate-limit failure is likewise an
  honest SKIP, not a crash. The report prints an
  `API latency: SKIPPED — <reason>` line and the harness still exits 0. The
  standalone `scripts/measure_pr_latency.py` keeps its own `BLOCKER:` / exit-2
  behavior — the graceful SKIP lives only in this harness mode.
- **Default-off is byte-identical to today.** Without the flag there is no
  latency section and no `api_latency` JSON key, and `requests` stays a lazy
  import inside the network path only.

## Window and buckets (frozen)

- **start** = 2026-07-01 · **boundary** = 2026-07-12 · **end** = run date.
- Session cards carry day resolution (filename `YYYY-MM-DD-<slug>.md`), and
  the v1.15.0 distribution completed mid-day (18:31:47Z, wrap report §1) —
  so the **boundary day is excluded from both buckets** and reported
  separately: before = start..07-11, after = 07-13..end.

## Metrics (frozen)

Definitions are executable in `scripts/measure_grounded_skills.py`; grammar
constants are imported from `engine.grammar` and skill names are read live
from the engine SKILLS list — one source, no drift copies.

| id | metric | definition | denominator |
|---|---|---|---|
| M1 | skill-grounding rate | cards referencing a shipped skill (`/name`, `.claude/skills/<name>`, or `docs/SKILLS.md`) | dated session cards per bucket |
| M2 | owner-ask compliance | field-formatted `⚑` ask blocks (a `⚑`-at-line-start paragraph carrying a `WHAT:` label — covers both `⚑ OWNER-ACTION` and named asks like `⚑ P10 …`) that carry all six fields (accepted alternates per `OWNER_ACTION_FIELDS`) + a risk-class token | detected ask blocks in dated cards (plus a separate undated current-state column from `control/status*.md`). Known limitation: a fully free-form ask with no `WHAT:` is invisible — M2 measures compliance among field-formatted asks, not formatting adoption. The line-start + `WHAT:` rule was spot-check-calibrated 2026-07-15: the naive `⚑ OWNER-ACTION`-token scan counted 29 prose *mentions* and 0 real blocks in the kit's own cards |
| M3 | capability-ledger activity | append-log lines matching `CAPABILITY_LOG_LINE_RE`, bucketed by their own date; venue compliance judged only on venue-shaped field-3 values (old-format lines fail open) | lines / venue-judged lines |
| M4 | throughput proxy | commits on the default branch whose subject ends `(#N)` (merge/squash suffixes) per bucket. Shallow clones truncate history silently (verified 2026-07-15 on a container clone: 0 before-window merges vs a real count in the hundreds) — the harness flags shallow repos and the row prints as a null; re-clone full before publishing M4 | — (count; latency is the optional API pass) |

## Pre-committed interpretation rules

- **M1 before ≈ 0 is expected, not a finding** — the skills did not exist in
  adopter trees before 2026-07-12. The question M1 answers is after-window
  **uptake**; a low after-rate is an honest negative headline.
- **Improvisation proxy** = 1 − M1 in the after window, stated with n.
- **Nulls are published** — a repo or bucket with n=0 prints `null (n=0)`
  and is reported as such, never dropped.
- **Confounds carried verbatim from #247 §6** and restated in the report:
  born-with-kit design, model-mix shift at the fleet boundary, the fleet
  program launch, window asymmetry, agent-under-owner-identity (no
  author-based steering metric is valid).
- The harness is PL-008 UNVERIFIED at first run: spot-check at least 3
  per-repo numbers against the raw files before publishing (e.g. hand-count
  one repo's after-window cards and its M1 hits).

## Provenance

- Gap + proposal: wrap report §3d (`../reports/2026-07-12-grounded-skills-wrap.md`).
- Methodology precedent: PR #247 (`../reports/2026-07-11-adopter-outcomes-measurement.md`),
  merged 2026-07-11, squash b862e9a.
- Window + acceptance: heartbeat baton (`control/status.md` Next-2), owner
  silence accepts.
- Harness pre-build: PR #386 (2026-07-15, self-initiated slice).
