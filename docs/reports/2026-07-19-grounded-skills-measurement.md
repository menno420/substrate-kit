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
