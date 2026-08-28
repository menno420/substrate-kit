# 2026-08-28 — OD-24 review round session 3: the current-state reconcile

> **Status:** `complete` — landed after three Codex rounds (2 + 1 conceded
> and fixed; R3's one P1 was the born-red hold itself, consumed by this
> flip). Flip exemption per the close discipline: the reviewed SHA is
> `7f98438` (R3's `Reviewed commit`), and the only commit after it is this
> card's own close-out and badge flip — nothing reviewable changed.

- **📊 Model:** fable-5 · high · docs-only
- **📍 Venue:** cloud-container

## Mission

The supersede's terminal-state table (docs/NEXT-TASKS.md, kit #587) marks its
old task 4 — reconcile `docs/current-state.md`, body still v1.20.2 — "still
open — belongs to the review round". This is that reconcile, records only,
scoped by the round's session-3 truth pass (fm
`docs/findings/2026-08-28-kit-tree-truth-pass.md`, which read all 187
doc-surface files at `a9acc41` and itemized this file's false claims):

1. `docs/current-state.md`: a dated reconcile block at the top carrying the
   true state (v1.21.0 since 2026-08-13; #552 merged 2026-08-04; 0 open PRs;
   the fm-side worklist route; the live-verified required-check state), the
   two flat-wrong headline lines corrected in place with strikethrough, the
   2026-07-17 block demoted from "READ THIS FIRST" to a dated snapshot, and
   the Next-action section routed to the live worklist first.
2. `control/status.md`: the same false claim in its "Open PRs (terminal
   states)" section (#552 "parked for owner ratification") and the stale
   adopters clause on the `last-shipped:` line, corrected; grammar lines
   preserved for the status gate.

Everything larger stays recommendations in the fm finding's §5 — no engine
code, no release, nothing owner-gated.

## Shipped

- `docs/current-state.md`: a dated **Reconcile — current truth (2026-08-28)**
  block now heads the file (v1.21.0; #552 merged 2026-08-04; 0 open PRs; the
  fm-side worklist route; adopter registry state incl. the five-repo roster
  gap; the P10 stack historical with the required-check swap verified DONE
  against the live rules endpoint; both `release.yml` triggers stated
  precisely). The two flat-wrong headline lines corrected in place with
  strikethrough; the 2026-07-17 block demoted from "READ THIS FIRST" to a
  dated snapshot; Next-action routed to the live worklist first.
- `control/status.md`: the "Open PRs (terminal states)" section's
  "#552 = parked for owner ratification" corrected; the `last-shipped:`
  adopters clause updated to the registry's 2026-08-14 regen; both unreleased
  changes (#587 + this #588) named; grammar lines preserved.
- `docs/NEXT-TASKS.md`: terminal-state row 4 flipped to **reconciled
  2026-08-28 (kit #588)**; its header's release line gained the same
  agent-runnable qualifier (Codex R1).

## Verify

- `python3 scripts/preflight.py` after every change batch: OK — 9 legs green
  (real exit 0, three runs).
- The P10/required-check claim is a live read, not a doc echo:
  `GET /repos/menno420/substrate-kit/rules/branches/main` returned exactly
  one required check, `kit-quality`, strict-up-to-date false (2026-08-28).
- Scope basis: the round's session-3 truth pass (fm
  `docs/findings/2026-08-28-kit-tree-truth-pass.md`) — all 187 doc-surface
  files judged at `a9acc41`; this PR executes only its reconcile pair.

## Codex review (kit #588)

- **R1 on `742fb75`: 2 inline P2 — 2 `[conceded]`, fixed in `bb4ee3b`:**
  (1) "only via workflow_dispatch" contradicted `release.yml`'s own
  two-trigger header — both files now state tag push (owner-side canonical)
  and dispatch (the only agent-runnable path); (2) NEXT-TASKS row 4 would
  have read "still open" the moment this PR made it false — flipped in the
  same PR.
- **R2 on `bb4ee3b`: 1 inline P2 — `[conceded]`, fixed in `7f98438`:** both
  ledgers called #587 the latest unreleased change, going one-behind at this
  PR's own merge; both now name #588 itself.
- **R3 on `7f98438`: 1 inline P1 — the born-red hold itself** (card
  in-progress, close-out markers absent → kit-quality red). That is the
  designed hold, and its fix is this flip; consumed here per the
  two-re-review cap's land condition, no residue routed.

💡 **Session idea:** R3 spent its whole round reporting the designed
born-red hold as a P1 — a reviewer reading the diff cannot tell the
deliberate hold from an abandoned card. A one-line convention (the PR body
and the card's Status line already say "flips only as the last commit";
Codex still flagged it) suggests the kit's PR template or reviewer prompt
should name the born-red contract explicitly, saving a review round on
every records PR.

## ⟲ previous-session review

Session 2's kit card (#587) held up in execution: its NEXT-TASKS
supersede's terminal-state table routed this exact session to this exact
file (row 4 "belongs to the review round" — the routing worked end-to-end),
and its two tree-checkable rows re-verified true here. One narrowing: the
release line it wrote into NEXT-TASKS ("cut only via workflow_dispatch")
lacked the agent-runnable qualifier — Codex R1 caught this PR inheriting
that imprecision, and both files now carry the precise two-trigger form.
