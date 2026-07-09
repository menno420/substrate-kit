# Session 2026-07-09 — gen-1 wind-down deliverables (kit-lab lane, phase 2)

> **Status:** `complete` *(PR #74 — opened READY at the born-red commit,
> auto-merge armed by this session via `enable_pr_auto_merge`)*

**Scope (about to do):** execute deliverables 1–6 of the owner's gen-1
wind-down directive for the kit-lab lane (wind-down claimed on main by
phase 1 via PR #72, `control/status.md` phase line, 2026-07-09T19:55:47Z).
One PR: (1) verify open PRs #26/#49 terminal-by-design + commit the
program queue state as `docs/gen2/queue-state.md`; (2) the wind-down
capstone project review `docs/retro/project-review-2026-07-09-gen1-winddown.md`
(+ index line); (3) `docs/gen2/next-boot.md` (gen-2 first-10-minutes,
walking skeleton, every known wall with exact error text); (4)
`docs/gen2/custom-instructions-proposal.md`; (5) `docs/gen2/environment-setup.md`
+ tested `docs/gen2/setup.sh`; (6) `docs/gen2/feedback-for-gen2-blueprint.md`;
plus a one-line next-action sharpening in `docs/current-state.md`.
Phase 3 (flipping `control/status.md` to wind-down complete) is NOT this
session's — status.md is untouched here (one writer per file; phase 3 owns
the overwrite).

## What shipped (PR #74)

All six deliverables, one PR (files above, plus `docs/gen2/README.md` as
the pack index, the `docs/retro/README.md` index line, the
`docs/current-state.md` gen-2 boot pointer, a `docs/succession/README.md`
cross-pointer, and a new `docs/CAPABILITIES.md` capability append).

**Verification results (deliverable 1):** #26 and #49 re-read fresh via
MCP at ~20:05Z — both open, READY (draft: false), `do-not-automerge`, all
3 check runs SUCCESS on their heads (#26 `f65816b`, #49 `65ba406`), both
`behind` main by design (not rebased — a push could invalidate the green
CI). Their OWNER-ACTION items 1–2 in `control/status.md` carry all six
required fields; nothing missing for the phase-3 overwrite.

**Fleet-manager reach (deliverable 4 prereq):** GitHub MCP
`get_file_contents` walled with the exact allowlist error (now including
`menno420/trading-strategy` in the allowlist — the error text drifts as
sessions gain repos), but `list_repos` showed fleet-manager public and
`add_repo` + `git clone --depth 1` succeeded → `docs/gen2-blueprint.md`
read IN FULL, so the instructions proposal aligns against the real
blueprint, not memory. New capability appended to `docs/CAPABILITIES.md`
per THE DISCOVERY RULE. (`register_repo_root` deliberately not called —
read-only need; loading a foreign repo's CLAUDE.md into a wind-down
session invites the inherited-instructions dissonance gen-1 already
ledgered as self-review B4.)

**Setup script tested (deliverable 5):** `docs/gen2/setup.sh` run
in-container from `/` and from the repo dir — exit 0 both; verbatim runs
pasted in `docs/gen2/environment-setup.md`.

**Gate before final push:** `python3 -m pytest tests/ -q` → `722 passed in
5.91s`; dist byte-pin green; `check_idea_index` OK; `check_program_law`
OK; `bench-integrity` OK (no bench/ changes); `check --strict` → the only
finding is this card's own born-red gate (a `[stamp]` D-0005
double-citation finding was hit and fixed by removing the ID from the
capstone — decisions stay stamped at one home).

**Deviation flags (decide-and-flag):** (a) added `docs/gen2/README.md`
(pack index) beyond the named six files — a one-hop index is what makes
the pack boot-usable; (b) appended the `add_repo` capability finding to
`docs/CAPABILITIES.md` — THE DISCOVERY RULE mandates same-session
recording; (c) one pointer line added to `docs/succession/README.md` so
the two lanes' packs reference each other — reversible, reachability only.

## Run report

- **📊 Model:** fable-5 · high · docs-only (wind-down succession pack)
- **⚑ Self-initiated:** the three flagged deviations above; nothing else.

### 💡 Session idea

`docs/CAPABILITIES.md` walls should carry a **last-verified date and a
re-probe hint** per entry: the fleet-manager wall recorded at ORDER 006
was already stale by wind-down (the `add_repo` workaround existed; the
allowlist in the error text had also drifted to include
trading-strategy). A tiny convention — append `last-verified: <date>` and
re-probe any wall older than N days before citing it in a VERIFIED-NEEDED
field — keeps the ledger from ossifying imagined walls, at near-zero cost
(the OWNER-ACTION↔CAPABILITIES cross-reference idea from the #68 card is
the natural home to build it into).

### ⟲ Previous-session review

Phase 1 (orient + claim, PR #72) did exactly what a claim phase should:
claim-on-main before any deliverable work, a fresh open-PR survey with
head SHAs, and a friction ledger with verbatim error texts that this
session lifted directly into `next-boot.md` — its report was genuinely
sufficient as a data package; nothing had to be re-derived. What it could
have done better: its report recorded `docs/gen2-blueprint.md` as
unreachable ("assume the same wall") without attempting the `add_repo`
path — the wall entry it trusted was stale, and one more attempt-once
probe would have caught it. The system improvement is this session's 💡
idea above (dated, re-probed capability entries); the general lesson —
re-verify a wall before propagating it into a new doc — held here and
should ride the discovery rule's wording eventually.

### Docs-drift check

Everything from this session lives in its durable home: the six
deliverables in `docs/gen2/` + `docs/retro/`, the capability delta in
`docs/CAPABILITIES.md`, the queue truth in `docs/gen2/queue-state.md`,
this card. `control/status.md` deliberately untouched (phase 3 owns it).
For phase 3's overwrite: no new ⚑ items needed; suggest the phase line
cite `docs/gen2/next-boot.md` as the boot pointer and keep all 11
OWNER-ACTION items verbatim.
