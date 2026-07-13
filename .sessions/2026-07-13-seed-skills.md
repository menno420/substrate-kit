# Session: seed skills into registry

> **Status:** `complete`

Did: generalized superbot's two seed skills (chase-references +
prep-owner-steps, provenance Q-0273) into the kit's skill registry —
ORDER 016 seat-item 2 (owner night-run directive, P0; supersedes the
2026-07-11 feature freeze for this program). PR #315.

## What shipped

- `src/engine/skills/skills.py`: two new SKILLS entries after `intake` —
  `chase-references` (inventory → resolve each → unfound-is-a-SEARCH-TASK →
  state the assembled picture) and `prep-owner-steps` (deep-link →
  paste-ready blobs → walk his path once → batch to one sitting → payoff +
  verify, shape template preserved via a 4-backtick outer fence). Both
  method skills: `capabilities: []` (read implicit), `grounds: []`
  (slice-2 rule — no commands run). Superbot-specifics stripped to generic
  phrasing ("the repo's documented reading path / sibling registry, where
  one exists"); the Q-0272 reading-path slot is flagged in the PR body as a
  follow-up for the Q-0272 graduation slice, not built here. Q-0273
  provenance + founding incidents kept inside the bodies, as superbot's
  copies carry them.
- `src/engine/seatdigest.py`: skills-digest description clip 120 → 85.
  Decide-and-flag: at 12 skills the 120-char rows overflowed the 1500-char
  block budget and `_fit_rows` silently dropped the tail three skills from
  the boot digest — names are the digest's whole job, so every name now
  fits; the overflow line stays as the growth safety net.
- `tests/test_skills.py`: order pin updated (12 skills); 4 new tests —
  method-content pins, generalization negatives (no `fleet_status`, no
  superbot doc names), read-only + grounds-[] invariants, and grounds-
  checker green at kit root AND on an empty target.
- `dist/bootstrap.py` regenerated (byte-pin).
- Boot discoverability verified, no gap to fix: the planted `docs/SKILLS.md`
  index renders from the live SKILLS list (`skills_index` context key),
  adopt stages both bodies to `.substrate/skills/<name>/SKILL.md` (kit never
  live-writes `.claude/`), and the seat digest now names all 12.

## Verify

- `python3 -m pytest tests/ -q` → 1228 passed
- `python3 dist/bootstrap.py check --strict` → green except this card's own
  designed born-red hold (pre-flip)
- `python3 -m ruff check src/engine/` → All checks passed!

## Enders

💡 **Session idea:** cross-skill name references in registry bodies are
unvalidated — `chase-references` says "pair with the `intake` skill", and a
future rename of `intake` would orphan that pointer silently (the grounds
checker skips bare single words by design). Add a registry-shape test: any
backticked span in a skill body that exactly matches another skill's name
must resolve against `skill_names()` at all times — one loop, no new
checker. Dedup-grepped `docs/ideas/` — nothing covers registry cross-refs.

📊 Model: Claude 5 family

⟲ **Previous-session review (PR #312, idea drift guard):** genuinely strong
friction→guard execution — it shipped the class fix (body-state drift
checker, hard-fail with a zero-false-positive marker set designed from the
full 35-file corpus) instead of just reconciling the four drifted files,
and its ⚑ verification flag catching the dispatch brief's wrong repo
pointer (fleet-manager 404 vs the frontmatter's correct kit citation) is
exactly the verify-don't-trust posture. What it could have done better: its
own 💡 (README blurb drift, the same class one level up) was left as an
idea without an idea FILE or README index entry — the capture convention
its own guard polices — so the follow-up lives only in a session card and
the PR body. System improvement: when a session's 💡 names a concrete,
small guard extension, spend the extra two minutes landing it as a
`docs/ideas/` file so the grooming pass can route it; this session's 💡 is
deliberately small enough to state fully inline with a dedup note instead.
