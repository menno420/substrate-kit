# docs/program/ — the program-governance home

> **Status:** `binding`
>
> **What this directory is:** the canonical home of **program law** — the
> rulings that bind *every* repo in the program (superbot, superbot-next, the
> kit-lab itself, the trading repo), as opposed to any one repo's local rules.
> Established by the kit-lab founding plan §8
> (`docs/planning/kit-lab-founding-plan-2026-07-07.md`, KF-6).

## What lives here

| File | Role |
|---|---|
| [`rulings.md`](rulings.md) | **THE [PL-NNN] register** — program-level rulings imported with provenance (superbot router Q-numbers for the founding census), D-ledger grammar, append-only |
| [`collaboration-model.md`](collaboration-model.md) | Canonical program copy: how the owner and agents work together, program-wide |
| [`agent-decision-authority.md`](agent-decision-authority.md) | Canonical program copy: the PL-001/PL-002 decision-authority model (decide-and-flag, never-wait, silence=consent) |

The kit's own opinionated defaults (markers, badge taxonomy, born-red
doctrine) are **house style**, not program law — those live in
[`../house-style.md`](../house-style.md).

## The citation rule — cite, never copy

1. **One home.** The canonical text of a program ruling exists **only here**.
   New program-level rulings are minted here as PL-blocks by whichever session
   obtains the owner ruling — cross-repo, that means filing a kit-repo PR.
2. **Consumers cite PL-IDs, never copy bodies.** Planted
   CONSTITUTION/collaboration-model templates carry a short "Program law"
   pointer section (this directory's URL + the PL-IDs). A consumer's local
   decision ledger / question router holds **repo-local** rulings only; when a
   local ruling is promoted program-wide, its local block is replaced by a
   pointer to the new PL. A copied ruling body in a consumer repo is drift by
   construction — two texts, one law, no sync mechanism.
3. **Origin blocks get pointers.** The superbot router Q-blocks this register
   imports receive a one-line "canonical home: kit `docs/program/rulings.md`
   PL-NNN" rider (the KL-2 superbot companion PR). History stays in place; the
   pointer kills drift.
4. **Enforced, not exhorted (PL-007):** `scripts/check_program_law.py` runs in
   the `kit-quality` CI gate — PL-block grammar, monotonic IDs,
   provenance-required on every block, and a template-side assertion that the
   planted pointer sections cite PL-IDs without copying ruling bodies.

## Register conventions

- **Append-only.** Next free PL-number; blocks are superseded
  (`- status: superseded` + `- superseded-by: PL-NNN`), never rewritten or
  deleted.
- **Provenance is mandatory.** Every block names the owner ruling it imports
  (or, for lab-minted law like PL-009, its own decision chain). Law never
  diverges from provenance.
- **Repo-local stays local.** Rulings about one repo's product (pricing,
  trading scope, session logistics) do **not** graduate here — the founding
  census deliberately left Q-0243–0246/0250–0253 repo-local (plan §8.2,
  D-13). The bar: law that must bind three repos.
