# 2026-07-12 — grounded-skills program, slice 8: self-propagation doctrine

> **Status:** `complete`

- **📊 Model:** fable-5 · seat-worker · grounded-skills slice 8

## Scope (what is about to happen)

Implementing §7 slice 8 of the grounded-skills program plan
(`docs/planning/2026-07-12-grounded-skills-program.md`, merged PR #263) —
the SELF-PROPAGATION DOCTRINE: a CONSTITUTION.md.tmpl working-agreement
clause making skill registration the expected reflex when a recurring
action has no skill (or an inadequate body) — extension = a registry entry,
not ad-hoc prose; growth loop prose workflow → index row → promoted skill —
with the propose-don't-apply boundary preserved (skill bodies/grounds/index
rows free to ship directly, flagged self-initiated; binding
working-agreement text + executable config route through the
question-router lane as a proposal, never self-applied; in-session
owner-directed change is the one exception, recorded with its provenance
id). Executable twin of superbot doctrine Q-0194 (2026-06-22 → binding
2026-06-28), Q-0106 (2026-06-12), Q-0172 (2026-06-17) — cited, not
paraphrase drift. Pinned phrases homed in `src/engine/grammar.py` (the
slice-4/5 one-home pattern); the SKILLS-index template's "Growing the set"
section carries the same phrases as the clause's pointer target. Tests +
CHANGELOG `[Unreleased]` entry + dist rebuild. No new skill, no checker
changes, no adopter work, no release, no other slices.

**Provenance flag:** collaboration-model.md.tmpl NOT wired — plan §7 slice 8
names CONSTITUTION.md.tmpl only (the coordinator's brief delegated that
question to the plan).

Lane claim: `control/claims/claude-grounded-skills-slice8.md`
(deleted at close, in-lane per the slice-4/5 precedent).

## Close-out

Shipped (PR #282; work commit a9438ce):

- **Grammar — one home** (`src/engine/grammar.py`, new self-propagation
  section): `SELF_PROPAGATION_PHRASES` = the reflex ("add or extend the
  skill"), the registry rule ("a registry entry, not ad-hoc prose"), the
  growth loop ("prose workflow → index row → promoted skill"), the free
  lane ("free to ship directly"), the bound lane ("never self-applied");
  `SELF_PROPAGATION_PROVENANCE` = "superbot Q-0194 · Q-0106 · Q-0172".
  Full mined provenance with dates lives in the section comment (Q-0194
  friction→guard 2026-06-22 → binding 2026-06-28 with the ownership split;
  Q-0106 propose-don't-apply 2026-06-12 with the in-session owner-directed
  exception; Q-0172 ship-anytime-with-accountability 2026-06-17) — the
  templates cite compactly because they state current value only, per
  their own header rule.
- **`CONSTITUTION.md.tmpl`**: one clause, placed directly after the
  slice-1 "Recurring actions run through the skill index" bullet — the
  registration reflex + growth loop + pointer into `docs/SKILLS.md`
  § "Growing the set" + the two-lane boundary, deferring to (not
  duplicating) the existing "Changing the rules — propose, don't apply"
  section. Binding text + executable config route through
  `docs/question-router.md` as a proposal.
- **`SKILLS-index.md.tmpl`** § "Growing the set": teaches the same reflex
  at the clause's pointer target (where agents actually look at boot);
  reverse pointer rides the engine-computed `${agreement_home}` key —
  never a hardcoded filename (the ORDER 015 dead-boot-pointer lesson).
- **Tests:** suite **1174 → 1184** (+10, `tests/test_self_propagation.py`:
  tuple identity + uniqueness, provenance cite, both templates pinned
  against the one home — whitespace-insensitive via a `_flat()` collapse so
  markdown rewrapping can't break a pin — clause→index pointer, bound-lane
  routing, boundary-intact accept criterion, fresh-adopt slot-free render
  of both templates).
- **CHANGELOG:** `[Unreleased]` slice-8 entry prepended; slice-6 entry
  kept.
- **Dist:** rebuilt via `python3 src/build_bootstrap.py` — 816995 B
  written; byte-pin suite green.

Verify (verbatim tails): `python3 -m pytest tests/ -q` → `1184 passed in
20.36s` · `python3 -m ruff check src/engine/` → `All checks passed!` ·
`scripts/check_idea_index.py` / `check_program_law.py` /
`check_bench_integrity.py` → OK · `python3 dist/bootstrap.py check
--strict` → the designed born-red hold naming this card, nothing else.

Accept criteria (§7.8): clause renders in fresh adopts ✔ (slot-free render
pin with the fresh-adopt context, both templates); wording keeps the
existing propose-don't-apply boundary intact ✔ (test pins the untouched
"Changing the rules" section AND the clause's deference to it).

**Decide-and-flag calls (plan silent on the detail):**

1. ⚑ collaboration-model.md.tmpl NOT wired — plan §7.8 names
   CONSTITUTION.md.tmpl only; the coordinator's brief made the plan
   authoritative on exactly this question.
2. ⚑ The clause routes binding-text proposals through
   `docs/question-router.md` (the kit's ask lane, per the autonomy-rails
   bullet) while deferring to the existing "Changing the rules" section
   for the decision-ledger half — proposal lane and provenance ledger are
   complements, not competitors.
3. ⚑ Phrase pins are whitespace-insensitive (`_flat()` in the test) rather
   than the templates being wrap-constrained — a rewrap can't silently
   break a pin, and template prose stays freely editable.
4. ⚑ SKILLS-index "Growing the set" carries the full phrase set (not just
   the loop) — the index is the planted doc agents actually read at boot;
   the clause and its target teach the same doctrine from one grammar home.
5. ⚑ Q-0194's friction→guard *chain* (checker/CI/test → hook → journal
   rule) lives in the grammar comment, not the clause — the clause's job
   is the reflex + boundary; the chain is superbot's enforcement-ladder
   detail the kit already practices via PL-007/PL-008.
6. ⚑ Claim landed in-lane (created+deleted within this PR), the slice-4/5
   precedent, rather than a separate control fast-lane claim PR.
7. ⚑ The kit's own root `CONSTITUTION.md` / planted docs are left on the
   normal upgrade channel (consumer #0 receives the clause at its next
   self-upgrade) — the slice-5 precedent.

**Program completeness (this closes the plan's 8 slices):** slices 1–6 and
8 shipped in-kit (#264, #265, #270, #272, #274, #279, this PR); slice 7 is
websites-repo scope, running in a parallel lane per the coordinator.
Still-open plan remainders, with citations: the §7 tail names
`routines.md.tmpl` doctrine, the verify-don't-trust Evidence block, and the
preflight fetch+hard-reset first step as riding "slices 2 and 8's template
edits or a small follow-on" — slice 2 shipped playbook bodies and slice 8
ships doctrine-of-growth only, so those three graduation-map ❌ rows
(plan §6) remain a small follow-on, not covered by any shipped slice.
Fleet-manager-side wiring of slice 6 (regen tool consuming the kit blocks,
UNIVERSAL vN bump + owner re-paste, plan §7.6 second half) is
fleet-manager-repo work, outside the kit lane.

## Session enders

💡 **Session idea:** a `check_doctrine_pins` advisory that walks every
`# ── … ──` grammar section carrying a `PHRASES` tuple and asserts the
declared taught-in templates actually contain each phrase — generalizing
what test_owner_assist/test_self_propagation now do per-slice by hand into
one data-driven scan (a `TAUGHT_IN` map next to each tuple). Payoff: the
next doctrine slice gets its template↔grammar pins for free, and a
template edit that drops a phrase is caught even when nobody wrote the
per-slice test. Dedup-checked `docs/ideas/` (nearest:
model-line-payload-lint-advisory — different surface; nothing on
grammar-pin generalization).

⟲ **Previous-session review:** slice 6's card (#279) hands slice-consumers
exactly what they need — the fence-prefix extraction contract and the
budget invariant are stated as contracts, not narration, and its
"prerequisites discovered" section is the reason this slice knew
`${agreement_home}` injection is universal without re-deriving it. One
genuine improvement: the program's slice cards each restate the plan's
§7-tail remainder ("routines.md.tmpl / Evidence block / preflight ride
slices 2 and 8") without any slice ever claiming it — a plan whose tail
work is assigned to "slices 2 and 8's template edits" should have been
re-pointed at a named follow-on the moment slice 2 shipped without it;
this card now says so explicitly in its completeness section, but the
drift class (tail work assigned to a slice that doesn't know it owns it)
is worth a plan-authoring rule: every "rides slice N" line gets a matching
line in slice N's scope or an explicit follow-on entry.

Documentation audit: CHANGELOG entry present; no new doc needs an index
entry; the doctrine text lives in templates + grammar + tests, all
self-indexing; the decide-and-flag list above is the complete set of
unrecorded judgment calls. Claim file deleted this commit. Capability
delta: none — no new wall or capability discovered in this venue (branch
push, PR open via MCP, checkers, and the designed-hold gate all behaved
as recorded).
