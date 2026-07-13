# Session: rationalization layer prototype

> **Status:** `complete`

Did: prototyped the RATIONALIZATION LAYER (ORDER 016 seat-item 3, provenance
Q-0273, owner night-run directive P0; supersedes the 2026-07-11 feature
freeze for this program) — the checkpoint question generalized from
friction→guard incidents to opportunities. PR #316.

## What shipped

- `src/engine/templates/CONSTITUTION.md.tmpl`: the "Skills self-propagate"
  clause extended (6 tight lines, inside the same bullet so the
  self-propagation phrase pins keep holding) with the rationalization
  checkpoint — at natural pauses ask *"should this action also be
  executed?"* and *"does this lesson deserve a permanent home — skill /
  checker / template / idea — I can ship NOW?"*; method routed to the
  `rationalize` skill, deep material kept out of the boot-metered file.
- `src/engine/templates/collaboration-model.md.tmpl`: one-line hook in
  "Friction → guard" — the reflex runs on opportunities, not only
  interruptions.
- `src/engine/skills/skills.py`: new read-only method skill `rationalize`
  (13th entry, after `prep-owner-steps`, mirroring the PR #315 seed-skill
  shape): when the checkpoint fires (slice end · any workaround/discovery/
  lesson · session enders, paired with `session-close`), the two questions,
  and the lesson/action routing table (lesson → skill body / checker /
  template / idea file; action → execute now if contained + reversible,
  else idea file / owner queue). Q-0273 provenance in the body;
  `capabilities: []`, `grounds: []` (slice-2 rule — no commands run).
- `src/engine/seatdigest.py`: description clip 85 → 72. Decide-and-flag:
  the 13th skill left the 85-char digest 75 chars over the 1500 budget and
  the every-name test would fail; 72 fits all 13 names with headroom
  (digest len 1399).
- Decide-and-flag (no new advisory hook): the planted `docs/SKILLS.md`
  index and the seat digest both render from the SKILLS list, so the new
  skill is boot-discoverable with zero added surface — a session-card
  grading hook stays out of a prototype by design (ORDER 016 scope).
- `tests/test_skills.py`: order pin (13 skills); 5 rationalize tests
  mirroring the seed-skill coverage (method pins, routing-table pins,
  session-close pairing, read-only + grounds-[] invariants, grounds checker
  green at kit root and on an empty target); plus the CROSS_SKILL_REFS pin —
  ⚑ self-initiated: PR #315's own 💡 (cross-skill name refs unvalidated)
  became due the moment the new body referenced `session-close`, and the
  rationalize checkpoint's question 1 rules it contained + reversible →
  executed now, not parked.
- `docs/ideas/seat-digest-adaptive-clip-2026-07-13.md` + README backlog
  entry: the follow-up home for retiring the manual clip ratchet.
- `dist/bootstrap.py` regenerated (byte-pin); claim file reshaped to the
  parseable `check_claims` bullet grammar after the checker's
  `claims-format` advisory fired on the initial free-form line.

## Verify

- `python3 -m pytest tests/ -q` → 1234 passed
- `python3 dist/bootstrap.py check --strict` → green except this card's own
  designed born-red hold (pre-flip)
- `python3 -m ruff check src/engine/` → All checks passed!

## Enders

💡 **Session idea:** seat digest adaptive clip — the 120→85→72 ratchet means
every new registry skill is a latent digest-test failure until someone
hand-lowers the clip (paid in #315 and again this session); compute the
largest clip that fits every name in the budget instead. Dedup-grepped
`docs/ideas/` (no digest/clip entry); landed as
`docs/ideas/seat-digest-adaptive-clip-2026-07-13.md` + README entry, per
#312→#315's own review lesson that a concrete 💡 deserves an idea FILE.

- **📊 Model:** fable-5 · high · feature-build

⟲ **Previous-session review (PR #315, seed skills):** strong generalization
discipline — the negative pins (`fleet_status`, superbot doc names asserted
ABSENT) guard against the likeliest regression (re-importing host-specific
text on a future sync), and flagging the Q-0272 reading-path slot as a
follow-up instead of hardcoding it was the right scope call. What it could
have done better: its digest fix (clip 120 → 85) patched the symptom at the
current skill count and left the ratchet in place — this session hit the
identical overflow one skill later. System improvement: when a fix contains
a constant chosen to "just fit" current data, the friction→guard move is to
make it derived or add the growth headroom note as an idea file immediately;
that improvement is landed this session as the adaptive-clip idea file (and
its cross-ref 💡 was executed as the CROSS_SKILL_REFS pin).
