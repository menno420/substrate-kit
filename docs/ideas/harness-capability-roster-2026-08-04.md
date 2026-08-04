---
state: captured
origin: owner
shipped_pr: null
shipped_repo: null
merged_date: null
outcome: open
---

# A capability roster injected by the harness, not recalled by the model (2026-08-04)

> **Status:** `ideas`
>
> **Origin:** owner, verbatim: *"a simple list of things like for example:
> Github integration, image creation, websearch, context window, etc. Such a
> list available to each model which accurately describes the general basis of
> things that are possible, would be a huge help."* Prompted by a day
> (2026-08-04) in which three providers' models each misreported their own
> abilities: a stale model table on the model's own provider, a free-tier
> context self-report 30× too high, and a session declaring a hard
> image-generation wall that did not exist.

**One line:** every seat prompt / rendered agent file should open with a short
harness-supplied roster of static capabilities — model + context + max output,
modalities, shell yes/no, network posture, repo scope, generation abilities —
because the harness is the only component that knows these with certainty and
the model's own account of them is training data, not telemetry.

**The division that makes it tractable** (owner-ratified): the roster carries
only the **static layer** — rows that change how a session approaches a task.
It never tries to carry the **empirical layer** (which hosts answer, which
paths 403, what a tool does today); that stays in each repo's
`docs/CAPABILITIES.md` under the discovery rule. Harness owns "what exists";
ledger owns "what was measured"; the discovery rule bridges them.

**Why the kit:** vendors have not shipped this (only fragments — model id and
cutoff appear in some system prompts; tool schemas are deferred for context
economy). The kit already plants the measured half; planting the static half
as a template block in the rendered seat/agent files would close the gap the
same way `CAPABILITIES.md` closed the empirical one. A ~10-line block; the
cost of one wrong "I can't do X" exceeds it by orders of magnitude.

**Sizing:** template block + slot answers per environment archetype; no engine
change. **Risk:** the roster drifting from the real environment — mitigate by
keeping rows static-only and dating the block.

**Evidence file:** fleet-manager `docs/findings/2026-08-04-generated-art-pipeline.md`
(the day's misreports and their costs are threaded through it and the
2026-08-04 `CAPABILITIES.md` entries).
