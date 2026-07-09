# Agent decision authority — decide-and-flag, never-wait (canonical)

> **Status:** `owner-guidance`
>
> **Canonical program copy** (kit-lab founding plan §8.1) of the decision-
> authority model — how much an agent decides for itself vs. hands to the
> owner, program-wide. Generalized from superbot's
> `docs/owner/agent-decision-authority.md`; the enforceable rulings are
> [PL-001] and [PL-002] in [`rulings.md`](rulings.md) (the lab's own shape is
> [PL-009]). Applies to every capable agent, in every program repo.

## The rule ([PL-001], ← superbot Q-0240)

**Default: decide, don't route.** When a decision is **reversible until a
downstream gate**, make the call yourself — recommendation, one-line
rationale, ⚑ flag — and keep going. Do not park it for the owner. This covers
the vast majority of planning, design, and technical calls, because in a
planning artifact nothing executes until the owner's go/no-go, so every
decision on paper is reversible with a single veto at that gate.

This explicitly includes decisions that feel **"too technical,"
"architectural," or "the owner's call":** his standing instruction is that he
usually takes the recommended decision and would rather spend his attention
**once, at the gate**, reviewing a coherent set of already-made calls than
answer them one at a time. A recommendation he'll almost certainly accept is
not a question — it's a decision with a checkbox.

## The carve-out — and even it is decide-and-flag, not block

| Decision shape | What the agent does |
|---|---|
| Reversible-until-a-gate (nearly all planning/design/technical calls) | **Decide + one-line rationale + flag on the run report.** No routing. |
| Irreversible **once executed** but decided *on paper* now (a migration contract, a schema shape) | **Decide the recommended ruling**, flag it **prominently** as "veto at the gate." Don't block. |
| Formally reserved by a prior owner-endorsed gate | **Pre-fill the recommended ruling per item** so the owner's sitting is a fast bless-or-override. |
| Would *execute* something irreversible before the gate (prod write, data move, external publish) | **Stop and ask** — the real brake. *(Overridden inside PL-002's and PL-009's scopes — below.)* |

## The never-wait override ([PL-002], ← superbot Q-0241)

Inside its scope (the rebuild program), even the last row retires as a
blocker: the owner's control shifts from *approval-before-execution* to
**reaction-after-visibility** —

- **No owner gates.** Build everything in logical order; never pause between
  phases for sign-off.
- **Live-test replaces owner verification.** Each piece is exercised live
  where the owner can see it; live-green is the agent's own gate.
- **Silence = consent = done.** If the owner says nothing about a piece, it
  is accepted; a message from him stops or redirects it.
- **The reversibility rider (vetoable, not a gate):** the destructive tier
  still never waits, but executes via the reversible-equivalent path the plan
  specifies, so a reaction window stays open when he does speak.
- **What never relaxes:** merge=deploy requires CI green, and every decision
  is still recorded + flagged so the after-the-fact review has a trail.

The kit-lab runs the same *shape* scoped to its own repo and surfaces —
[PL-009] enumerates its build-freely / decide-and-flag / ask-first tiers and
its destructive tier (founding plan §6.3–§6.4).

## How the owner stays in control

Not by gatekeeping each decision — by reviewing the **flagged set**:

- Every self-made decision is recorded (decision · options weighed ·
  rationale) in the artifact's own decisions log, and flagged on the session
  run report's `⚑ Self-initiated:` line.
- High-stakes decisions surface in a short **flag-for-gate list** at the top
  of the deliverable, each phrased as a one-line veto item (the founding
  plan's §1 KF-table is the house example).
- The owner's review is **one pass**: skim the flags, veto what he disagrees
  with, silence blesses the rest.

## What still goes to a question router

Each repo's question router is for **genuine product/vision/intent ambiguity
an agent cannot resolve from source, the goal, or a defensible default** —
"which of two *products* do you want," not "which of two *implementations* is
better." A technical decision with a defensible best answer is not a router
question; decide it and flag it. The litmus test: *would the owner plausibly
reject the recommended option?* If not, it's a decision, not a question.
New **program-level** rulings are minted as PL-blocks in
[`rulings.md`](rulings.md) (see [`README.md`](README.md) for the rule);
repo-local rulings stay in that repo's router/ledger.
