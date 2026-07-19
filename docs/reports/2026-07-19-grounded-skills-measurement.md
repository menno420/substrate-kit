# Grounded-skills program — before/after measurement (2026-07-19)

> **Status:** `audit` (dated snapshot) — findings report for the GSW-1..3
> grounded-skills measurement window run. Plan
> `docs/planning/2026-07-19-grounded-skills-window-run.md`; claim
> `control/claims/claude-gsw-1-grounded-skills.md`; PR #476. Frozen raw data:
> `docs/reports/data/2026-07-19-grounded-skills-results.json`
> (sha256 `dc8d8399005254bac48e6b8a8998bd55f5be0dab448ca7acba9b965a3af10fc9`).
> Source files win; negative findings are the headlines; every number carries
> its n and window.

## 1. Method

The harness `scripts/measure_grounded_skills.py --clone` (frozen; PL-008 now
spot-checked, see §3) was run once over **full/non-shallow clones** of the
12-repo roster in `docs/fleet-repos.txt`. The pre-registered protocol is
`docs/operations/grounded-skills-measurement.md` (PR #247 precedent). Window:
**before = 2026-07-01 .. 2026-07-11**, **boundary-day 2026-07-12 excluded from
both buckets**, **after = 2026-07-13 .. 2026-07-19** (i.e. before = 07-01..07-12
exclusive, after = 07-12 exclusive..07-19). Card dates are filename dates (day
resolution). Generated `2026-07-19T00:15:24Z`. All clones were verified
non-shallow (M4 `shallow:false` on every repo), so M4 history is complete and
valid. This report adds only frozen data + the report + a reachability link;
the measurement code and protocol are unchanged, keeping the harness
reproducible at `--end=2026-07-19`.

## 2. Results

Numbers are carried verbatim from the harness skeleton (`/tmp/gsm/report-skeleton.md`)
and the frozen `results.json`.

### M1 — skill-grounding rate (cards referencing a shipped skill / cards)

| repo | before | after |
|---|---|---|
| menno420/substrate-kit | 21/125 (17%) | 18/111 (16%) |
| menno420/superbot-next | 3/70 (4%) | 26/168 (15%) |
| menno420/websites | 10/86 (12%) | 36/139 (26%) |
| menno420/superbot | 39/226 (17%) | 4/25 (16%) |
| menno420/superbot-games | 0/44 (0%) | 1/69 (1%) |
| menno420/trading-strategy | 1/27 (4%) | 6/53 (11%) |
| menno420/gba-homebrew | 1/27 (4%) | 5/97 (5%) |
| menno420/pokemon-mod-lab | 10/33 (30%) | 9/29 (31%) |
| menno420/venture-lab | 4/48 (8%) | 2/113 (2%) |
| menno420/fleet-manager | 11/79 (14%) | 7/112 (6%) |
| menno420/idea-engine | 8/124 (6%) | 3/210 (1%) |
| menno420/superbot-mineverse | 0/22 (0%) | 2/48 (4%) |

### M2 — OWNER-ACTION six-field + risk-class compliance (dated cards)

| repo | before | after | status*.md now (undated) |
|---|---|---|---|
| menno420/substrate-kit | null (n=0) | null (n=0) | 0/5 (0%) |
| menno420/superbot-next | null (n=0) | null (n=0) | null (n=0) |
| menno420/websites | null (n=0) | null (n=0) | null (n=0) |
| menno420/superbot | null (n=0) | null (n=0) | null (n=0) |
| menno420/superbot-games | null (n=0) | null (n=0) | 0/1 (0%) |
| menno420/trading-strategy | null (n=0) | null (n=0) | null (n=0) |
| menno420/gba-homebrew | null (n=0) | null (n=0) | null (n=0) |
| menno420/pokemon-mod-lab | null (n=0) | null (n=0) | null (n=0) |
| menno420/venture-lab | null (n=0) | null (n=0) | null (n=0) |
| menno420/fleet-manager | null (n=0) | null (n=0) | null (n=0) |
| menno420/idea-engine | null (n=0) | null (n=0) | null (n=0) |
| menno420/superbot-mineverse | null (n=0) | null (n=0) | null (n=0) |

### M3 — capability append-log lines (count · venue compliance)

| repo | before | after |
|---|---|---|
| menno420/substrate-kit | 10 · venue null (n=0) | 5 · venue null (n=0) |
| menno420/superbot-next | 1 · venue null (n=0) | 16 · venue null (n=0) |
| menno420/websites | 10 · venue null (n=0) | 9 · venue null (n=0) |
| menno420/superbot | 0 · venue null (n=0) | 0 · venue null (n=0) |
| menno420/superbot-games | 0 · venue null (n=0) | 0 · venue null (n=0) |
| menno420/trading-strategy | 0 · venue null (n=0) | 1 · venue null (n=0) |
| menno420/gba-homebrew | 0 · venue null (n=0) | 0 · venue null (n=0) |
| menno420/pokemon-mod-lab | 1 · venue null (n=0) | 1 · venue null (n=0) |
| menno420/venture-lab | 1 · venue null (n=0) | 8 · venue 8/8 (100%) |
| menno420/fleet-manager | 0 · venue null (n=0) | 31 · venue 30/30 (100%) |
| menno420/idea-engine | 4 · venue null (n=0) | 1 · venue null (n=0) |
| menno420/superbot-mineverse | 6 · venue null (n=0) | 1 · venue null (n=0) |

### M4 — merged-PR throughput proxy ((#N) subjects on the default branch)

| repo | before | boundary-day | after |
|---|---|---|---|
| menno420/substrate-kit | 192 | 67 | 158 |
| menno420/superbot-next | 207 | 88 | 252 |
| menno420/websites | 145 | 53 | 200 |
| menno420/superbot | 71 | 3 | 13 |
| menno420/superbot-games | 50 | 7 | 104 |
| menno420/trading-strategy | 59 | 16 | 71 |
| menno420/gba-homebrew | 18 | 8 | 93 |
| menno420/pokemon-mod-lab | 31 | 5 | 43 |
| menno420/venture-lab | 44 | 35 | 160 |
| menno420/fleet-manager | 83 | 54 | 193 |
| menno420/idea-engine | 163 | 55 | 323 |
| menno420/superbot-mineverse | 40 | 7 | 85 |

### Fleet aggregate (before vs after)

| metric | before | after |
|---|---|---|
| M1 skill-grounding | 108/911 (12%) | 119/1174 (10%) |
| M3 capability lines | 33 | 73 |
| M4 merged-PR (#N) subjects | 1103 | 1695 |

(M2 is null fleet-wide in both dated buckets — no field-formatted ask blocks
were detected in dated cards; the only non-null M2 signal is the undated
`status*.md`-now column, itself 0/6 compliant where n>0.)

## 3. Spot-check verification (PL-008)

The harness is PL-008 UNVERIFIED at first run; the protocol requires ≥3 per-repo
numbers hand-checked against the raw files before publishing. Four checks were
run across M1/M3/M4:

| # | metric · repo · bucket | harness | ground-truth | result |
|---|---|---|---|---|
| 1 | M4 · substrate-kit · after | 158 | 158 | MATCH |
| 2 | M4 · substrate-kit · before | 192 | 192 | MATCH |
| 3 | M3 · fleet-manager · after | 31 lines, venue 30/30 | 31 lines, venue 30/30 | MATCH |
| 4 | M1 · substrate-kit · after | 18/111 | 18/111 | MATCH |

**Note on the M4 bucketing method.** A naive `git log` **commit-date** grep
diverges from the harness's documented **author-date** bucketing *by design*
(substrate-kit after: 156 naive vs 158 harness; before: 204 naive vs 192
harness). This is not a mismatch — the harness buckets by author date per the
protocol, and a harness-faithful replication (author-date, same suffix regex)
reproduces the harness numbers **exactly**. The divergence is the expected
consequence of two different, documented bucketing rules, not a defect.

**Conclusion:** the harness numbers are TRUSTED for this window.

## 4. Honest deviations & nulls

- **pokemon-mod-lab was measured, not skipped.** The plan pre-registered
  `pokemon-mod-lab` as an expected private-repo **honest-null (skip)**. That
  expectation **did not hold this run**: this container had read access, so the
  repo cloned (full/non-shallow) and was measured like any other. Its numbers
  appear in every table above (M1 before 10/33, after 9/29; M4 before 31,
  after 43).
- **Skipped repos: none.** The harness's honest-null list is empty
  (`Skipped repos: none`). This corrects the plan's pre-registered skip
  expectation — reported here plainly rather than silently.
- **M2 nulls are published, not dropped.** Every M2 dated-card cell is
  `null (n=0)`; those nulls are carried verbatim per the "nulls are published"
  protocol rule.
- **The optional open→merge latency pass WAS run** (previously an unrecorded
  gap). The harness marks PR open→merge latency as out of scope (it needs the
  GitHub API); the GSW-4 API pass now supplies it in **§7** with its own frozen
  data (`docs/reports/data/2026-07-19-grounded-skills-latency.json`) and two
  flagged method decisions (all merged PRs included / no squash exclusion; bucket
  by `merged_at` date). All 12 repos returned data — no per-repo nulls.

## 5. Confounds

Carried **verbatim** from PR #247 §6 (`../reports/2026-07-11-adopter-outcomes-measurement.md`):

1. **Born-with-kit design** — 9/10 adopters have no before period (gen-2
   blueprint seeds are born-right on purpose).
2. **Pin-only superbot** — kit machinery never engaged; the kit was extracted
   from superbot's native workflow.
3. **Model-mix shift at the boundary** — the EAP 3-model fleet (Fable 5 /
   Opus 4.8 / Sonnet 5) launched via superbot #1877/#1878 merged
   07-09T01:18/01:39Z, hours before the pin.
4. **Fleet program launch same day (07-09)** — post-boundary owner attention
   and throughput reflect the program, not the kit.
5. **Window asymmetry** — the after-window is 2.7 days; p90 on n=98 is noisy.
6. **Agent-under-owner-identity** — direct human steering invisible to any
   author-based metric (§4).

## 6. Interpretation

Sober reading, with n and confounds attached to every delta. **Not measured
beats invention.**

- **M1 (skill-grounding) shows no fleet-wide uptake signal.** The fleet
  aggregate *fell* slightly (12% → 10%), and per-repo movement is mixed:
  websites (12% → 26%) and superbot-next (4% → 15%) rose, while idea-engine
  (6% → 1%), venture-lab (8% → 2%) and fleet-manager (14% → 6%) fell. The
  protocol pre-commits that **M1-before ≈ 0 is expected** (skills did not exist
  in adopter trees before the boundary), so a low *after*-rate is the honest
  negative headline: **improvisation proxy = 1 − M1-after ≈ 90% fleet-wide**.
  The rises are consistent with adoption but are **not** separable from the
  born-with-kit and fleet-program-launch confounds, and several repos have small
  denominators (superbot after n=25). This delta does **not** demonstrate that
  the skills caused grounding; it shows uptake remains low and uneven.
- **M2 (owner-ask compliance) is unmeasurable this window** — null (n=0) in
  every dated bucket. No field-formatted `⚑`/`WHAT:` ask blocks were detected in
  dated cards, so there is nothing to report beyond "not measurable," which is
  itself the finding. The undated `status*.md`-now column (0/6 where n>0) is not
  a before/after signal.
- **M3 (capability-ledger activity) rose in raw count** (33 → 73 lines
  fleet-wide), driven almost entirely by fleet-manager (0 → 31) and venture-lab
  (1 → 8). Venue-compliance is judged non-null only where lines carry
  venue-shaped field-3 values: fleet-manager 30/30 and venture-lab 8/8 (100%);
  everywhere else venue is `null (n=0)` (old-format lines fail open). The count
  rise is real but concentrated in two repos and is confounded by the fleet
  program launch — it does **not** establish a fleet-wide behavior change.
- **M4 (merged-PR throughput proxy) rose sharply** (1103 → 1695 fleet-wide),
  but this is a throughput *proxy*, not a kit effect: the after window sits
  inside the post-07-09 fleet-program-launch period (confound 4) and the windows
  are asymmetric (confound 5). superbot itself *fell* (71 → 13), consistent with
  it being pin-only (confound 2). **No causal attribution to the kit is
  warranted** — M4 measures activity, and activity here is dominated by the
  program launch, not by grounded skills.

**Bottom line:** this run establishes measured baselines with published nulls,
not a proven kit effect. Given the born-with-kit design and the same-day fleet
program launch, the before→after deltas are **descriptive only**; where a delta
is small or moves against the hypothesis (M1 aggregate down, superbot M4 down)
it is reported as such rather than explained away. The durable value is the
frozen, spot-checked dataset and an honest negative headline on skill uptake.

## 7. Open→merge latency (GSW-4 · GitHub-API pass)

This is the optional **GSW-4** PR open→merge latency pass, per the
pre-registered protocol (`docs/planning/2026-07-19-grounded-skills-window-run.md`
GSW-4) and the PR #247 §2 method. The harness (§1–§6) deliberately does **not**
measure latency — its M4 is a git-log throughput *proxy* — because open→merge
latency needs the GitHub API for exact `created_at`/`merged_at` timestamps. This
section supplies that pass from a from-scratch GitHub-API measurement
(`scripts/measure_pr_latency.py`; tests `tests/test_measure_pr_latency.py`).

**Metric.** latency = `merged_at − created_at` in minutes, per (repo × bucket):
`merged` count, `latency_n` (rows in the stat), median, p90, max. Only
actually-merged PRs count. **Percentile convention:** the harness has no
percentile helper, so this pass uses the **numpy-style linear-interpolation**
percentile (`h = (n−1)·p/100`, interpolate between the two nearest ranks;
median = p50, p90 = p90, max = p100) — stated here so the numbers read alongside
M1–M4.

**Frozen data:** `docs/reports/data/2026-07-19-grounded-skills-latency.json`
(sha256 `c0fb65ba08dc10c7a8b9f5ab32dd55db811dc2285e1d0d977f6d607638ebf59d`).
**Reproduce:**

```
python3 scripts/measure_pr_latency.py \
    --start 2026-07-01 --boundary 2026-07-12 --end 2026-07-19 \
    --repos docs/fleet-repos.txt \
    --json docs/reports/data/2026-07-19-grounded-skills-latency.json \
    --generated 2026-07-19T01:00:00Z
```

Generated `2026-07-19T01:00:00Z`. **All 12 roster repos returned data; no repo
errored or nulled.** Window: **before = 2026-07-01 .. 2026-07-11**,
**boundary-day 2026-07-12 excluded from both buckets**, **after = 2026-07-13 ..
2026-07-19**. Each PR is bucketed by its `merged_at` UTC calendar date.

### Two flagged method decisions (authored deviations from #247 §2)

1. **All merged PRs are included in the latency stat with their exact API
   timestamps — squash-merges are NOT excluded** (so `latency_n == merged` in
   every bucket). #247 §2 excluded squash PRs only because its *git-derived
   open-time proxy* couldn't time them; the GitHub API returns exact
   `created_at`/`merged_at` for every merged PR regardless of merge method, so
   the exclusion is unnecessary and inclusion is strictly **more complete**.
   This is the one authored method deviation from #247 §2.
2. **PRs are bucketed by `merged_at` calendar date (day resolution, UTC)** to
   parallel harness M4 (which buckets by merge-commit author date). The boundary
   DAY (2026-07-12) is reported separately and excluded from before/after.

### Per-repo latency (minutes) — before · boundary-day · after

| repo | before n·med·p90·max | boundary-day n·med | after n·med·p90·max |
|---|---|---|---|
| menno420/substrate-kit | 241 · 0.8 · 19.0 · 747.4 | 60 · 4.2 | 160 · 6.5 · 15.6 · 2195.2 |
| menno420/superbot-next | 215 · 1.9 · 14.2 · 318.5 | 94 · 8.6 | 249 · 7.1 · 165.5 · 4193.1 |
| menno420/websites | 153 · 2.4 · 14.0 · 248.6 | 67 · 4.6 | 191 · 6.2 · 108.5 · 1814.5 |
| menno420/superbot | 391 · 7.5 · 80.0 · 7352.2 | 36 · 6.8 | 95 · 7.2 · 229.5 · 2332.4 |
| menno420/superbot-games | 57 · 4.7 · 396.1 · 861.5 | 6 · 7.8 | 104 · 2.4 · 11.6 · 662.2 |
| menno420/trading-strategy | 63 · 1.9 · 10.1 · 265.1 | 15 · 0.4 | 72 · 2.4 · 11.8 · 803.4 |
| menno420/gba-homebrew | 59 · 2.5 · 7.2 · 44.8 | 15 · 21.0 | 107 · 6.5 · 1004.1 · 2282.6 |
| menno420/pokemon-mod-lab | 50 · 3.3 · 8.0 · 25.1 | 4 · 7.6 | 43 · 652.5 · 1554.0 · 2504.4 |
| menno420/venture-lab | 55 · 3.1 · 12.3 · 42.3 | 44 · 0.4 | 154 · 1.6 · 19.1 · 498.7 |
| menno420/fleet-manager | 88 · 8.2 · 25.6 · 1000.2 | 56 · 13.8 | 193 · 2.9 · 25.0 · 811.6 |
| menno420/idea-engine | 218 · 0.4 · 4.3 · 14.6 | 59 · 0.6 | 322 · 1.9 · 12.4 · 848.2 |
| menno420/superbot-mineverse | 40 · 0.2 · 1.2 · 1.8 | 14 · 1.4 | 78 · 2.3 · 14.8 · 489.9 |

### Fleet aggregate (pooled PR latencies, minutes)

| bucket | n | median | p90 | max |
|---|---|---|---|---|
| before | 1630 | **3.5** | 24.1 | 7352.2 |
| boundary-day | 470 | 3.7 | 147.0 | 1657.6 |
| after | 1768 | **4.5** | 41.4 | 4193.1 |

**Headline: median open→merge latency barely moved across the grounded-skills
boundary — 3.5 min before → 4.5 min after** (a +1.0-minute shift on a pooled
n=1630 → n=1768). Fleet-wide, PRs open and merge in **single-digit minutes**
median in both windows; the +1.0-min move is directionally *up* (slightly
slower), i.e. it does not show the grounded-skills program speeding merges — and
given its size it is best read as noise/confound, not a program effect.

### Honest interpretation (descriptive only)

- **This latency is a confound-heavy proxy, not a kit/program effect.** Auto-
  merge-on-green predates the grounded-skills program **fleet-wide** — the whole
  fleet already lands PRs the instant CI goes green — so open→merge latency
  mostly measures **CI duration + queue depth**, not agent behavior the program
  changed. The single-digit-minute medians in *both* windows are consistent with
  that: merges are gated by CI wall-clock, which the program did not touch. All
  §5 confounds (born-with-kit, model-mix shift, same-day 07-09 program launch,
  window asymmetry, agent-under-owner-identity) carry by reference and apply
  here unchanged.
- **The aggregate medians are well-powered; the tails and small buckets are
  not.** before/after pool n≥1630, so the median shift is a real (if tiny)
  descriptive fact. But p90/max are dominated by long-tail outliers (a 7352-min
  = ~5-day before-window PR in superbot; a 4193-min after-window PR in
  superbot-next) — these are individual stuck PRs, not distribution shifts, and
  p90 should be read as noisy.
- **Two per-repo movements are real but small-n / outlier-driven, flagged not
  explained away.** `pokemon-mod-lab` after shows median **652.5 min on n=43** —
  a genuine jump, but n<50 and outlier-heavy, so the stat is **noisy**; it is
  reported, not attributed. `gba-homebrew` after p90 = 1004 min (median still
  6.5) is likewise a tail artifact. The `boundary-day` bucket for
  `pokemon-mod-lab` is **n=4 (<5) → too small to interpret**; treat its median
  (7.6) as not-measured.
- **Bottom line:** open→merge latency is **flat-to-slightly-slower** across the
  boundary (median 3.5 → 4.5 min) with no signal attributable to the grounded-
  skills program. Because auto-merge-on-green already governs merge timing fleet-
  wide, this metric cannot isolate a program effect and is best read as a
  **measured baseline with honest nulls**, exactly like M1–M4.
