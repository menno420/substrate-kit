# Program law — the [PL-NNN] rulings register

> **Status:** `living-ledger`
>
> **THE canonical home of program-level law** — the rulings that bind every
> repo in the program (superbot, superbot-next, the kit-lab, the trading repo).
> Append-only D-ledger grammar: blocks are superseded, never deleted or
> rewritten. Every block carries **provenance** (the owner ruling it imports —
> superbot router Q-numbers for the founding census). Consumers **cite PL-IDs,
> never copy bodies** — see [`README.md`](README.md) for the citation + sync
> rule. Enforced by `scripts/check_program_law.py` (kit-quality CI).

<!-- Grammar: ## [PL-NNN] <title> / - status: decided|superseded|retired /
     - date: YYYY-MM-DD / - supersedes: PL-NNN (opt) / - superseded-by: PL-NNN
     (opt) / - provenance: <origin ruling + home> (REQUIRED) / - verdict:
     <the canonical statement> / - why: <1-3 lines> (opt) / - scope: (opt) -->

## [PL-001] Decide-and-flag over route-up

- status: decided
- date: 2026-07-06
- provenance: superbot Q-0240 (docs/owner/maintainer-question-router.md); owner
  directive, applied in-session. Full model: superbot
  docs/owner/agent-decision-authority.md → canonical program copy
  [`agent-decision-authority.md`](agent-decision-authority.md).
- verdict: When a decision is **reversible until a downstream gate** — which is
  nearly every planning/design/technical call, since nothing executes until the
  owner's go/no-go — the agent **decides it itself** (recommendation + one-line
  rationale + a ⚑ flag on the run report) and does **not** route it to the
  owner. This explicitly includes "too-technical" / architectural *design*
  calls. Irreversible / production / external work is **decided-and-flagged
  for veto, not blocked**; the sole stop-and-wait is *executing* something
  irreversible before the gate. The owner's control point is one review pass
  over the flagged set at the gate, not per-decision gatekeeping.
- why: The owner usually takes the recommended decision and prefers reviewing
  a coherent set of already-made calls once, at the gate, over answering them
  one at a time. A recommendation he'll almost certainly accept is a decision
  with a checkbox, not a question.

## [PL-002] Never-wait autonomy for the rebuild — silence = consent = done

- status: decided
- date: 2026-07-07
- provenance: superbot Q-0241 (docs/owner/maintainer-question-router.md); owner
  directive, applied in-session — *"it should just build everything in logical
  order and live test it so I can see the results in a server, but it should
  never wait for me, if I don't say something about it it should be considered
  done."* Extends PL-001 (decide-and-flag) into decide-and-proceed.
- verdict: For the **rebuild program** (building `superbot-next` + porting the
  bot), the owner's control model is *reaction-after-visibility*, not
  approval-before-execution. (1) **No owner gates** — the G1 go/no-go, G2
  verdict-acceptance, and every 👤 owner-gated step are retired as blockers;
  the coordinator builds everything in logical order without pausing for
  sign-off. (2) **Live-test replaces owner verification** — each piece is
  exercised live in a real server (an agent drives all commands in a live bot
  session); live-green is the coordinator's own gate. (3) **Silence = consent
  = done** — the coordinator never waits; if the owner says nothing about a
  piece it is accepted, and his control point is reacting to what he sees.
  One flagged rider (vetoable, not a gate): the **destructive tier only**
  (prod data import over real balances/audit, the CUT-3 token swap, deleting
  old-bot data) still never waits but executes via the reversible-equivalent
  path the plan specifies — shadow-first / restored-snapshot DB, the N=7d
  rollback window, the declared-loss reverse-import valve — zero pause, just a
  reaction window. Merge=deploy still requires **CI green** (never-wait ≠
  bypass CI), and decisions are still recorded + flagged (PL-001).
- scope: The rebuild program. The live production bot keeps superbot's Q-0213
  ask-first `*Delete`/`*Restore` brake and prod-data safety until the owner
  generalizes this — he can extend PL-002 to all work at any time. The
  kit-lab's own autonomy is *shaped* like this ruling but scoped separately —
  that is [PL-009](#pl-009-the-kit-labs-own-autonomy--pl-002-shaped-scoped-to-its-own-surfaces),
  not this block.

## [PL-003] Rail before scale — the multi-repo sequencing

- status: decided
- date: 2026-07-07
- provenance: superbot Q-0247 (docs/owner/maintainer-question-router.md); owner
  ratification of the recommended sequencing in the multi-repo program capture.
- verdict: Program repos launch **in sequence, each proving its guardrails
  before the next starts**: (1) `superbot-next` first; (2) the substrate-kit
  extracts to its own repo at the second-consumer moment (both repos created
  in the same kickoff); (3) the trading-research repo third, on a matured kit.
  Repo-start mechanics: **fresh-from-kit**, the old repo attached read-only as
  the oracle, never clone-as-base.
- why: Each repo's autonomy loop is a rail that must hold weight before
  another loop leans on the same pattern — scale multiplies whatever the rail
  actually is, proven or not.

## [PL-004] Model-for-task allocation is an empirical, rule-based discipline

- status: decided
- date: 2026-07-07
- provenance: superbot Q-0248 (docs/owner/maintainer-question-router.md); owner
  ruling — *"we should have a way to test this reliably and a proper rule to
  define when it is necessary and what decides the result."*
- verdict: Model allocation graduates from a static table to a **measured
  discipline**, three layers: (1) **instrument** — every session/run logs
  `model · effort · task-class · outcome`, outcome objective-first (CI green
  on first push, checker findings, rework/revert within the window, tokens per
  merged PR); (2) **taxonomy + default ladder** — the 8 task classes
  (docs-only · mechanical refactor · test writing · runtime bugfix ·
  kernel/architecture design · review/verify · research · idea/planning) each
  seed a default tier, stakes modify upward; (3) **mechanical
  escalation/de-escalation triggers** — e.g. two red CI rounds on the same
  task or a review with ≥N confirmed defects escalate one tier; a cheaper tier
  matching outcome quality for M consecutive tasks of a class de-escalates.
  **What decides:** objective gates first, judge-scored quality second (paired
  same-task A/Bs), cost as tiebreaker. Covers **both planes**: the agent plane
  (which model runs a session/routine) and the product plane (which
  provider/model each runtime API call uses, enforced at the gateway task
  registry and judged by per-use-case evals). The kit-lab owns the
  program-wide dataset and runs the paired A/Bs (founding plan §5.2, B2).
- why: "The right model for the right task" is an empirical question; rules
  without telemetry are vibes, telemetry without rules is a spreadsheet.

## [PL-005] Observe-first budgets — telemetry before caps

- status: decided
- date: 2026-07-07
- provenance: superbot Q-0249 (docs/owner/maintainer-question-router.md); owner
  ruling — *"budget so far is not really a problem, I'd like to test it for a
  while to see the average of a couple of months before deciding on anything."*
- verdict: Budget caps (Railway caps, token budgets) are **deferred, not
  adopted**: instrument spend per repo/session/routine now (the PL-004
  telemetry carries cost — same dataset), let ~2 months of real usage accrue,
  then decide caps from the measured average. **Security rails are not budget
  rails and stand regardless:** scoped credentials (a repo/lab never holds
  another repo's prod secrets or the live bot token) and
  irreversibility brakes (e.g. the trading repo's real-money caps + kill
  switch) guard irreversibility, not spend.
- why: Data over guesses — a cap chosen before the measured average exists is
  a guess that either strangles the loops or protects nothing.

## [PL-006] Source wins; a false green is the check's bug

- status: decided
- date: 2026-06-16
- provenance: superbot Q-0120 (docs/owner/maintainer-question-router.md); owner
  decision promoting the journal-earned rules (items b + c).
- verdict: Two halves of one discipline. (1) **Cross-agent output**
  (Codex/Gemini/ChatGPT reviews, "rewrite X" reports, any other agent's
  claims) is **input to verify against shipped source, never orders** — check
  each specific before acting. (2) **A green check that contradicts visible
  evidence is a bug in the *check*, not a clearance** — when a tool reports
  clean but the defect it should have caught is visible, verify the tool
  against ground truth before trusting its green. In both directions the tie
  goes to source: when a doc and a source file disagree, the source file wins.
- why: The canonical failures — a cross-agent report sound at the conclusion
  level but wrong on 4 specifics, and checkers that matched one merge-message
  style and reported green while 5 merged PRs were missing.

## [PL-007] Enforce, don't exhort

- status: decided
- date: 2026-06-14
- provenance: superbot Q-0132 (docs/owner/maintainer-question-router.md), the
  strategy-chat capture that named the doctrine; hardened by Q-0194 (friction →
  guard, promoted binding 2026-06-28).
- verdict: Durable behavior comes from **mechanized enforcement, never from
  per-session discipline**. A claim that must stay true is **CI-backed** (a
  check that fails on divergence) or explicitly date-stamped as a snapshot —
  never kept fresh by asking every future session to remember. Anything that
  interrupts a session's workflow — a wrong-branch slip, a stale file, a
  checker that lied, a footgun — is converted into the **cheapest enforcing
  prevention before the session ends**, in order: checker / CI / test → hook →
  written rule.
- why: At tens of PRs a day, human (or agent) discipline is the one mechanism
  guaranteed to drift; a door that locks beats a sign that asks.

## [PL-008] Adopt tooling freely, with a kill-switch

- status: decided
- date: 2026-06-12
- provenance: superbot Q-0105 (docs/owner/maintainer-question-router.md); owner
  directive — *"implement whatever you think would work, but make sure another
  agent knows it should be deleted if it's been proven unreliable over
  multiple sessions."*
- verdict: Agents may implement or adopt **any tooling or check they judge
  will help — custom or third-party — without asking first**. The price of
  that autonomy is a **provenance + reliability header** on every adopted
  tool: *why* it was added, the *date*, an *"unverified: confirm its output
  against ground truth a few times across sessions before trusting it"* note,
  and an explicit *"delete this if it proves unreliable over multiple
  sessions"* instruction. Load-bearing checks graduate out of "unverified"
  once proven across sessions; a misfiring convenience guard gets **removed**
  by a later agent, never silently worked around.
- why: A lying check left in place is worse than no check; the kill-switch
  makes disposability explicit so later agents delete instead of route around.

## [PL-009] The kit-lab's own autonomy — PL-002-shaped, scoped to its own surfaces

- status: decided
- date: 2026-07-07
- provenance: the owner-ratified multi-repo program capture, Part 2 row 5
  ("complete freedom" gets the Q-0241 shape) + its Q-0247 ratification +
  the kit-lab founding plan §6.3 / decision D-12
  (`docs/planning/kit-lab-founding-plan-2026-07-07.md`) — the lab's own chain,
  so law never diverges from provenance. PL-002's letter covers the rebuild;
  this block is the lab's.
- verdict: The kit-lab operates under PL-002's *shape* — reversible by
  default, telemetry not caps (PL-005), scoped credentials only, everything
  audited, the owner vetoes reactively — **scoped to its own repo and
  surfaces**. **Build freely** (flagged on the run report): anything in the
  kit repo, its own Railway project, its own sites, its own
  benchmark/telemetry stores. **Decide-and-flag prominently:** releases
  (reversible by supersession — published releases are never deleted), ladder
  revisions, governance-home edits (which additionally require this
  register's provenance discipline). **Ask-first (the true safety brake):**
  the lab's enumerated destructive tier (founding plan §6.4) and anything
  touching another repo's production or credentials — which it structurally
  cannot hold. One structural guard above all others: **the lab measures
  itself on cold sessions and throwaway repos; a warm session never grades
  its own substrate** — graded subject ≠ grader ≠ rubric author.
- why: "Complete freedom" without the shape is how a self-improving loop
  grades its own homework; the scope line keeps the lab's never-wait inside
  surfaces where every action is reversible or enumerated.

## [PL-010] The 9th task class: `feature build` — amends PL-004's taxonomy

- status: decided
- date: 2026-07-09
- provenance: consumer friction — superbot's hand-authored report (friction
  issue [#15](https://github.com/menno420/substrate-kit/issues/15) report 3,
  filed per plan §9.1) + the kit's own KL-3 session idea
  (`.sessions/2026-07-09-kl3-telemetry.md`), triaged verified-real at the
  KL-4 disposition and routed **discuss-first** via
  `docs/ideas/feature-build-task-class-2026-07-09.md`; owner ratification =
  the owner-reviewed merge of this ruling's own dedicated
  `do-not-automerge` PR (kit PR #22) — a program-law change ships as its
  own PR, never bundled into a band PR (§8.3).
- verdict: PL-004's layer-2 taxonomy gains a ninth class, **`feature
  build`** (exact string, verbatim in `TASK_CLASSES`): a session whose
  dominant work is **building a net-new capability** — a new engine
  feature, verb, checker, template, subsystem, or consumer-facing surface —
  as opposed to designing contracts (`kernel/architecture design`),
  reshaping existing code (`mechanical refactor`), or repairing behavior
  (`runtime bugfix`). Mixed sessions file their dominant-cost class.
  Existing dataset rows are **never rewritten** — `telemetry/
  model-usage.jsonl` keys class strings per-date, so the class exists from
  this ruling's merge date forward. Its allocation-ladder row starts
  **observe-first with no seeded tier** (PL-005: telemetry before defaults
  — B2 data seeds it), unlike the eight founding classes whose defaults
  were seeded at KL-3.
- why: The taxonomy's most common real session shape had no home — KL-2
  filed an off-taxonomy compound the harvest warns on, and KL-3 and KL-4
  both filed as nearest-neighbor `kernel/architecture design` — so every
  band was quietly mislabeling B2 allocation rows; cheap to fix at row 7,
  expensive at row 1000.
- scope: Amends (extends) PL-004; does not supersede it — every other part
  of the PL-004 discipline stands unchanged.
