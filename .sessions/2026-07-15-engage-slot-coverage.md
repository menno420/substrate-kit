# 2026-07-15 · engage-slot-coverage

> **Status:** `complete`

- **📊 Model:** Fable · medium · test writing
- Scope: ship the captured idea `docs/ideas/engage-slot-list-derived-2026-07-13.md`
  (cheapest fix shape) — coverage tests holding both deliberately-pinned
  interview-slot lists (bench `ENGAGE_SLOTS` + the ci.yml cold-adopt slot loop)
  to set-equality with the question bank — plus the idea's lifecycle move.
- ⚑ Self-initiated: work-ladder rung 3 — no inbox ORDER above 024 (heartbeat
  reports done=001–024), adopter kit-lines match the registry at the ~11:00Z
  read-only spot-check (next/mineverse v1.16.0, websites/games v1.15.0 — no
  currency slice due), claims empty, zero open PRs at the 11:0xZ scan.

## Record

- Boot: hard-synced to origin/main c5380dc (#386). Born-red card + claim =
  first commit bc4d09a; PR #387 opened READY immediately after.
- Shipped (af64390): `tests/test_bench.py` —
  `test_engage_slots_cover_the_question_bank` (no duplicates + set equality
  with `{q["slot"] for q in QUESTIONS}`) and
  `test_ci_cold_adopt_slot_loop_covers_the_question_bank` (parses the ci.yml
  `for slot in …; do` backslash-continued loop and holds it to the same set).
  Both pinned lists keep their pinned ORDER — the arc stays byte-reproducible;
  only SET coverage becomes checked, so the next bank growth trips a named
  test instead of a latent red (the Q-014..016 rider-graduation miss was the
  paid instance). Tests-only: no engine change, dist byte-pin untouched.
- Lifecycle: idea flipped promoted/shipped (frontmatter PR #387, anticipated
  in-PR merged_date per the leg-6 grace convention); README entry moved
  Backlog → Shipped; CHANGELOG `[Unreleased]` note added.
- Drift fixed on sight (Q-0166 instinct, same README edit):
  model-line-payload-lint-advisory sat in the pointer-stub section reading
  `state: captured … next: quick-win` while its frontmatter says shipped kit
  PR #352, merged 2026-07-14 — relocated to § Shipped with the ship record.
  This is a fresh instance of the exact class the #383 card's leg-7 💡
  (index-section⇄frontmatter agreement) targets — more evidence for that
  card-carried idea, not a new one.
- Verify: preflight 7/7 legs green (1585 passed, 1 skipped, incl. the 2 new
  tests; ruff, dist-byte-pin, idea-index, changelog-structure, program-law,
  bench-integrity); `dist/bootstrap.py check --strict` red only on this
  card's designed born-red hold. Heartbeat overwritten pre-flip (f439de5):
  wake record, baton refreshed, ⚑ blocks preserved byte-identical, `kit:`
  line plain.

## Session enders

- 💡 **Session idea:** groom-intake bridge for card-born ideas — a
  `bootstrap groom`/`check` advisory listing 💡 lines from recent completed
  session cards that have no corresponding `docs/ideas/` file, so an idea
  born in a card cannot rot un-captured. Evidence: the #386 card's genuinely
  useful `VERIFY:`-vs-six-field-grammar idea lives only in its card today —
  invisible to anyone reading the README backlog conveyor, and the conveyor's
  own promise is "every idea ends implemented, on a roadmap, in discussion,
  or rejected". The reflection miner already lifts 💡 lines into the lessons
  buffer (`_REF_IDEA_MARK`, `engine/loop/reflections.py`), so the scan is
  built — what is missing is the bridge to backlog intake (loose match on
  card 💡 text vs idea-file titles, advisory-only). Dedup: grepped
  docs/ideas/ — retro-docs-reachability and taxonomy-surface-sync cover other
  index surfaces; the #383 leg-7 card idea covers README⇄frontmatter
  placement, not card→backlog intake; no existing file covers this.
- ⟲ **Previous-session review:** the grounded-skills-harness session (#386)
  set the quality bar for instrument work — it spot-checked its own measure
  against ground truth before first use and caught two real defects (the
  ⚑-token prose false-positive, the shallow-clone M4 zero), and its card
  grammar is fully clean (three-field model line — the miss it had itself
  flagged in its predecessor). Gap: both of its findings-shaped leftovers
  (the `VERIFY:` grammar idea, the free-form-ask blind spot) live only in
  card/protocol prose — nothing routes them into the backlog conveyor, which
  is exactly the intake gap this session's 💡 proposes to close; until such a
  bridge exists, the concrete improvement is that a shipping session's groom
  rung should include "capture the previous card's 💡 as an idea file when it
  is still unclaimed" (this session kept its slice lean and did not — flagged
  honestly rather than silently).
