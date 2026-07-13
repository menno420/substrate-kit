# Session: rider graduation — Q-0271 + Q-0272 into templates

> **Status:** `complete`

Did: ORDER 016 seat-item 4 (owner night-run directive P0; supersedes the
2026-07-11 feature freeze for this program) — graduated the autonomy rider
(Q-0271, superbot fleet-rearm-2026-07-12.md §3 @ cdb2680) and the multi-repo
reading path (Q-0272, superbot docs/fleet-reading-path.md @ cdb2680) into the
kit. PR #317.

## What shipped

- `docs/program/rulings.md`: **[PL-012]** — the rider's twelve items as the
  ruling body, provenance Q-0271 + the fleet-rearm §3 travel clause.
  Decide-and-flag: appended a new block **extending PL-002** rather than
  generalizing PL-002 in place — the register's own grammar is append-only
  ("blocks are superseded, never deleted or rewritten") and PL-010 set the
  amends-not-supersedes precedent; PL-002's Q-0241 history untouched.
- `src/engine/templates/CONSTITUTION.md.tmpl`: "Autonomy rails — act vs.
  ask" rewritten (updated, not stacked) to the rider's adopter-side form —
  items 1–8, 11–12 folded tightly, each citing PL-012 for depth; the old
  "Ask before … large / cross-cutting (architectural)" rail retired for
  reversible calls; owner-attention/OWNER-ACTION bullet kept; Program-law
  example list now names PL-012.
- `src/engine/templates/routines.md.tmpl`: new "Seat wake discipline"
  section — rider items 9–10 (wake hygiene + end-of-turn invariant).
- `src/engine/templates/reading-path.md.tmpl` (new), planted at
  `docs/reading-path.md` via ADOPT_PLAN: standing read-authorization,
  one-command orient, sibling/truth-file map, tier 0–3 ladder, truth rules,
  incident rationale; resolution method cross-links the `chase-references`
  skill via `docs/SKILLS.md` instead of duplicating it. Slot-driven:
  `fleet_dark_repos` / `fleet_status_command` / `fleet_siblings`
  (Q-014..Q-016, none critical — a solo repo graduates with them unfilled).
  Routed from `AGENT_ORIENTATION.md.tmpl` (planted-doc list + a when-to-open
  pointer), NOT the K0 boot set — Q-0272 doctrine keeps the path routed.
- `bench/run_ab.py` ENGAGE_SLOTS + the ci.yml cold-adopt slot walk extended
  to the three new slots (the bench engagement-arc test caught the miss);
  `tests/test_hook_session_start.py` quota-suffix pin made bank-derived.
- `tests/test_rider_graduation.py`: pins for both workstreams (rails rider
  phrases + retired-rail negative pin + portability pins; PL-012 register
  presence with intact PL-002; reading-path structure/slots/badge/routing +
  end-to-end planted-reachability).
- `docs/ideas/engage-slot-list-derived-2026-07-13.md` + README entry.
- `dist/bootstrap.py` regenerated (byte-pin).

## Flags

- ⚑ **Expected red on the program-law CI check:** this PR touches
  `docs/program/rulings.md` and `check_program_law.py --label-gate` holds
  red unless the PR carries `do-not-automerge` — a label this session is
  instructed not to apply. The red is the law gate working as designed
  (law changes sit for owner review); labeling is the owner/coordinator's
  move, then re-run CI.
- ⚑ Self-initiated: the bank-derived quota-suffix test fix and the
  engage-slot-list idea file (both contained, reversible).

## Verify

- `python3 -m pytest tests/ -q` → 1249 passed
- `python3 dist/bootstrap.py check --strict` → exit 1 pre-flip with only
  this card's designed born-red hold; green after this flip commit
- `python3 -m ruff check src/engine/` → All checks passed!
- `python3 scripts/check_program_law.py` → OK (label gate is PR-context)
- `python3 scripts/check_idea_index.py` → OK

## Enders

💡 **Session idea:** engage slot lists — three surfaces enumerate "every
interview slot" (the bank, bench `ENGAGE_SLOTS`, the ci.yml cold-adopt
loop) and nothing asserts the pinned two still cover the bank; each bank
growth is a latent red (paid this session when Q-014..016 missed both).
Dedup-grepped `docs/ideas/` (no slot-list/engage entry); landed as
`docs/ideas/engage-slot-list-derived-2026-07-13.md` + README entry.

- **📊 Model:** Claude Fable · high · feature-build

⟲ **Previous-session review (PR #316, rationalization layer):** clean scope
discipline — the checkpoint doctrine went into the constitution as six
tight lines with the method routed to an on-demand skill (boot budget
respected), and the session executed its own doctrine live (the
CROSS_SKILL_REFS pin shipped the #315 review's improvement instead of
parking it). What it could have done better: the rationalize routing table
names "template" as a lesson destination, yet the checkpoint was never
pointed at the template text adjacent to the edit — the stale
ask-on-architectural rail this session retired sat in the same file #316
was editing, one section below, already contradicted by Q-0271 earlier
that day. System improvement: when a session edits a binding template,
run the rationalize question over the surrounding sections too ("does
adjacent doctrine still match current law?") — cheap at edit time,
expensive one session later; folded into this session's rails rewrite
rather than a new mechanism.
