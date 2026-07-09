# Kit-lab run report — 2026-07-09 (owner day-report)

> **Status:** `audit` (dated snapshot — written at the audit-follow-ups
> session, PR #24; source code and merged PRs win over this file)
>
> One findable consolidation of today's run for owner review: what was
> built, what the independent audit found, both incidents with their guards,
> and the open owner gates. **Links, not duplication** — the per-session
> stories live in [`.sessions/`](../../.sessions/), the living status in
> [`docs/current-state.md`](../current-state.md).

## 1. Run summary — bands KL-0…KL-6 built in one day

The founding plan ([`docs/planning/kit-lab-founding-plan-2026-07-07.md`](../planning/kit-lab-founding-plan-2026-07-07.md))
band ladder was built KL-0 through KL-6 (KL-5's bench half and KL-6's
blocked pieces pending owner gates). Band-by-band detail: current-state
[§ Stability baseline](../current-state.md#stability-baseline).

**Merged PRs (this repo, 18):**
[#4](https://github.com/menno420/substrate-kit/pull/4) ·
[#5](https://github.com/menno420/substrate-kit/pull/5) (KL-0 seed) ·
[#6](https://github.com/menno420/substrate-kit/pull/6) (CI delta) ·
[#7](https://github.com/menno420/substrate-kit/pull/7) (card-only; merged by
the instant-merge footgun — see current-state 👤 P10) ·
[#8](https://github.com/menno420/substrate-kit/pull/8) ·
[#9](https://github.com/menno420/substrate-kit/pull/9) ·
[#10](https://github.com/menno420/substrate-kit/pull/10) ·
[#11](https://github.com/menno420/substrate-kit/pull/11) (KL-1 → release
[v1.0.0](https://github.com/menno420/substrate-kit/releases/tag/v1.0.0)) ·
[#12](https://github.com/menno420/substrate-kit/pull/12) (KL-2 governance) ·
[#13](https://github.com/menno420/substrate-kit/pull/13) (KL-3 telemetry) ·
[#14](https://github.com/menno420/substrate-kit/pull/14) (KL-4 lab loop) ·
[#16](https://github.com/menno420/substrate-kit/pull/16) (KL-5 1/2
auto-draft) ·
[#18](https://github.com/menno420/substrate-kit/pull/18) (KL-6 unblocked
half) ·
[#19](https://github.com/menno420/substrate-kit/pull/19) (groomed ideas) ·
[#20](https://github.com/menno420/substrate-kit/pull/20) ·
[#21](https://github.com/menno420/substrate-kit/pull/21) (run close-out) ·
[#22](https://github.com/menno420/substrate-kit/pull/22) (PL-010 — incident,
§3) ·
[#23](https://github.com/menno420/substrate-kit/pull/23) (enabler-race
hotfix).

**Consumer/companion PRs (9):** superbot
[#1879](https://github.com/menno420/superbot/pull/1879) (kit-version pin) ·
[#1881](https://github.com/menno420/superbot/pull/1881) (KL-2 provenance
riders) ·
[#1882](https://github.com/menno420/superbot/pull/1882) (in-tree kit copy
removed) ·
[#1883](https://github.com/menno420/superbot/pull/1883) (exporter telemetry
family) ·
[#1884](https://github.com/menno420/superbot/pull/1884) (pinned feed
contract); superbot-next
[#42](https://github.com/menno420/superbot-next/pull/42) (pin) ·
[#44](https://github.com/menno420/superbot-next/pull/44) (⚑ incident, §3) ·
[#46](https://github.com/menno420/superbot-next/pull/46) (v1.0.0 vendored
upgrade, completing #44); websites
[#11](https://github.com/menno420/websites/pull/11) (consumer-side feed
contract pass).

**Open:** [#17](https://github.com/menno420/substrate-kit/pull/17) — the
`bench/` tree, `do-not-automerge` by design, awaiting owner blessing (owner
gate 1). [#24](https://github.com/menno420/substrate-kit/pull/24) — the
audit follow-ups shipping this report.

## 2. Independent audit — verdict

An independent audit of the run (its follow-ups shipped in
[#24](https://github.com/menno420/substrate-kit/pull/24), verify-then-fix
per Q-0120/PL-006): **claims verified, hygiene clean** — the band/PR/release
claims above checked out against live GitHub. Caveats it raised, honestly
carried:

- **The websites repo has no CI** — its feed-contract pass (#11) is
  reviewer-verified only; nothing gates regressions there yet.
- **Telemetry `task_class` labels are imprecise pre-PL-010** — rows written
  before the 9th class existed squeezed guard/feature work into the 8-class
  taxonomy; interpret early `telemetry/model-usage.jsonl` rows accordingly.
- Residual auto-merge label-guard holes → closed/documented by #24 (§3 and
  [`docs/operations/auto-merge-guards.md`](../operations/auto-merge-guards.md)).

## 3. Incidents — TWO, each with its guard

The run's honest incident count is **two** (the original run-closeout ledger
counted one; corrected by #24 — also recorded in `.session-journal.md`
§ Recurring problems):

1. **kit#22 — PL-010 gate slip.** A `do-not-automerge`-labelled,
   discuss-first program-law PR auto-merged mechanically: the enabler read
   labels from the stale PR-open event payload; the label landed +7 s after
   open and a ~12-min runner-queue lag armed auto-merge anyway (full
   timeline: incident comment on
   [#22](https://github.com/menno420/substrate-kit/pull/22)). **Guards:**
   [#23](https://github.com/menno420/substrate-kit/pull/23) fresh-label
   re-read before arming; [#24](https://github.com/menno420/substrate-kit/pull/24)
   labeled-event disarm workflow + `check_program_law.py --label-gate`
   (unlabeled law changes go **red** on the required check — enforcement,
   not advice). PL-010 itself is live pending owner ratify-or-veto (owner
   gate 2).
2. **superbot-next#44 — card-gate slip.** Merged **65 s** after opening
   (04:22:21→04:23:26Z) carrying only its born-red `in-progress` session
   card: that repo's old vendored dist's `check` predates the
   in-progress-badge gate, so nothing held the required check red.
   Self-reported in [#46](https://github.com/menno420/superbot-next/pull/46)'s
   card, which completed #44's work. **Guard:** the v1.0.0 vendored-dist
   upgrade #46 itself shipped — the current engine holds an `in-progress`
   card red (the kit-side fix existed since kit#10; #44 proves a consumer is
   only as gated as its vendored dist version).

## 4. Owner gates — the checklist

Canonical, with exact steps and one-line unblocks: current-state
[§ Next action ▸ Owner gates](../current-state.md#next-action) (kept
current there; not restated here). Headline list:

1. Bless the bench rubric → merge [#17](https://github.com/menno420/substrate-kit/pull/17).
2. Ratify or veto PL-010 ([#22](https://github.com/menno420/substrate-kit/pull/22) — merged mechanically, §3).
3. 👤 P4 — arm the kit-lab loop (Schedules; prompt in
   [`docs/operations/lab-loop.md`](../operations/lab-loop.md) § Arming).
4. 👤 P10 — required-check swap to `kit-quality`.
5. 👤 P5 — Railway project `kit-lab` (then the P6 console move).
6. 👤 P11 — public flip, or veto → 👤 P13 read-only PAT.
7. 👤 P8 — confirm the MIT license.
