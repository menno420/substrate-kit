# Auto-merge guards — what holds, what is advisory, what enforces

> **Status:** `reference`
>
> Written 2026-07-09 (audit follow-ups, PR #24) after the kit#22 incident: a
> `do-not-automerge`-labelled program-law PR auto-merged mechanically. This
> is the honest map of the guard stack — including the hole that **cannot**
> be closed workflow-side.

## The stack, in firing order

| # | Guard | Where | Defeats | Class |
|---|-------|-------|---------|-------|
| 1 | Label carve-out at PR open (`!contains(labels, 'do-not-automerge')`) | `auto-merge-enabler.yml` job `if:` | a label present in the PR-open event payload | advisory |
| 2 | Fresh label re-read before arming (15 s grace + API read; hotfix #23, from #17's diff) | `auto-merge-enabler.yml` step | labels landing *before* the arm step executes — the stale-payload race **and** runner-queue lag (the #22 root cause) | advisory |
| 3 | Label-added disarm (`on: pull_request: [labeled]` → `gh pr merge --disable-auto`) | `auto-merge-disarm.yml` (PR #24) | a label applied at *any* time **after** arming | advisory |
| 4 | Owner-gate label gate: PR diff touching `docs/program/rulings.md` / the canonical program-law docs without the label → **red required check** | `check_program_law.py --label-gate` in `kit-quality` (PR #24) | *forgetting the label entirely* on a law change | **enforcing** |
| 5 | Bench pin-path label gate (`bench/rubric\|tasks\|seeds`) | `check_bench_integrity.py` (rides open PR #17) | forgetting the label on an oracle change | **enforcing** (once #17 merges) |
| 6 | Born-red session gate (an `in-progress`/drafted card holds `kit-quality` red) | `dist/bootstrap.py check` in CI | merging before the close-out exists | **enforcing** |

## The hole that stays open — and why that is OK

**Direct arming bypasses guards 1–3 entirely.** Arming auto-merge is a
GitHub *platform feature*, not our workflow: any human or agent can call
`enable_pr_auto_merge` (MCP), the REST/GraphQL API, or the UI button at any
moment, and no workflow can intercept that — workflows only *react* to
events after the fact. Guard 3 narrows the window (a label re-disarms), but
an actor that arms *without* the label ever being applied is invisible to
all three. Verified true at the 2026-07-09 audit; do not try to close this
workflow-side — it is not closable.

**The real enforcement is the required-check gate (guards 4–6).** GitHub
will not merge an armed PR while a *required* status check is red, no matter
who armed it or how. An unlabeled law change is red by guard 4; an
incomplete session is red by guard 6. So the honest model is:

> **The `do-not-automerge` label is advisory routing** (it tells the
> enabler/disarm pair to keep native auto-merge off so a green PR can sit
> for review). **The required check going red is the enforcement** (it makes
> merging impossible, armed or not, until the gate condition is met).

Corollary: anything that must *never* merge un-reviewed needs a **red
required check**, not (only) a label. The label's job is to stop a *green*
PR from merging while the owner looks at it.

## Operational notes

- Guard 4 re-reads labels **fresh from the API at step execution time**
  (`ci.yml` Program law step), never from the event payload — the #22
  lesson. Workflow: label the PR, then re-run `kit-quality`; the re-run
  sees the label and goes green (then the PR still won't *auto*-merge:
  guard 3 disarmed it when the label landed — merge by hand when review is
  done, or remove the label and re-arm).
- Guards 1–3 depend on repo settings (P10): until the `main` ruleset
  requires `kit-quality` directly, the two legacy alias contexts carry the
  required-check role (they report `kit-quality`'s result, hard-failing on
  non-success — the #7 skipped-alias hole is closed).
- Provenance/reliability: guards 2–4 are Q-0105/PL-008 **unverified** at
  ship time (guard 3 live-verified once on PR #24) — confirm against ground
  truth across a few labelled PRs; delete any of them if they prove
  unreliable over multiple sessions.
