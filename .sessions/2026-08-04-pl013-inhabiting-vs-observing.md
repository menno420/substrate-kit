# 2026-08-04 · PL-013 — inhabiting beats observing

> **Status:** `complete`

- **📊 Model:** opus-5 · high · docs-only

## What shipped

`docs/program/rulings.md` gains **[PL-013] Inhabiting beats observing** — the
owner's live ruling that read access is not integration. Both citation
templates (`CONSTITUTION.md.tmpl`, `collaboration-model.md.tmpl`) name the new
PL-ID per the register's cite-never-copy rule; `dist/bootstrap.py` rebuilt.

> **Read access is not integration.** An agent that can read a repo is
> *informed* by it; an agent that runs inside it is *subject* to it — its tests
> fail, its gates go red, its pushes get rejected, its claims meet exit codes.
> Only the second is corrected by the environment rather than by the owner.

Three binding consequences: **readable is not binding** (enforcement is the
active ingredient — PL-007 restated as *why* it works); **decomposition is an
environment property, not a prompt property**; **diverge cheaply, converge
expensively**.

## Why this is the kit's law and not a consumer's finding

Its rationale is a claim about what the kit is *for*. Inhabitants are temporary
and amnesiac — every session is a new tenant, the container is reclaimed, and
none of them remember the last one. **Living inside makes rules enforceable;
the kit makes them persist.** Either half alone gives a known failure mode: the
observer that drifts off a convention it can read, or the inhabitant that
solves something well and takes the solution with it when the container dies.

## Evidence

fleet-manager `docs/findings/2026-08-04-generated-art-pipeline.md` — derived
from six ChatGPT art-production transcripts plus the spider-swing tree. Two
instances carry the ruling: a non-integrated session **drifted off the
six-visible-leg convention while having read access to the committed docs that
state it**, and a 41-item queue collapsed into a single generation call because
a plain chat has no execution boundary between items.

## The guard that caught this session

`check_program_law.py --label-gate` refused the PR for lacking
`do-not-automerge` after a bot armed auto-merge — *"law changes sit for owner
review, never auto-merge (the kit#22 lesson)"*. Then the session-card gate held
the merge until this file existed. Both are PL-013 demonstrating itself: rules
that would have been ignored as prose were enforced because the session was
subject to them.

## Verify

```bash
python3 -m pytest                        # 2081 passed, 1 skipped
python3 scripts/check_program_law.py     # OK
```

## Honest null

PL-013 is owner-ruled, not measured. Nothing here tests the counterfactual — a
multi-item queue run *inside* an integrated environment — so the decomposition
claim rests on the owner's direct experience of both surfaces, not on an
experiment this program ran.
