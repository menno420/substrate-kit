# 2026-07-12 — grounded-skills program, slice 3: the /intake owner-request skill

> **Status:** `complete`

- **📊 Model:** fable-5 · seat-worker · grounded-skills slice 3

## Scope (what was about to happen)

Implementing §7 slice 3 of the grounded-skills program plan
(`docs/planning/2026-07-12-grounded-skills-program.md`, merged PR #263):
the `/intake` skill — superbot's Q-0254 understand-and-reflect doctrine made
executable — as one `SKILLS` list entry per §5's draft body (consolidate →
restate → map via `docs/SKILLS.md` → possibility space → decide-and-flag,
with owner questions only as Q-0263.2 structured choices carrying a bolded
recommendation). Index row comes free (engine-computed table). Tests +
CHANGELOG `[Unreleased]` entry + dist rebuild. No other slices, no adopter
work, no release.

**Provenance flag:** proceeded on the plan's §8 recommended defaults per
the coordinator — **Q2=B** (advisory-first; grammar checks graduate to
CI-red only once proven) and **Q4=A** (the program supersession covers this
slice under the 2026-07-11 freeze). Vetoable at the owner's normal window.

Lane claim: `control/claims/claude-grounded-skills-slice3-intake.md`
(deleted at close, this commit).

## Close-out

Shipped (PR #270; implementation commit e7efee1):

- **`intake` skill** (`src/engine/skills/skills.py`) — new SKILLS entry
  placed right after the ops-playbook cluster (session-close /
  upgrade-distribution / release), superbot skill anatomy (purpose → What
  this does → Invocation → numbered Instructions → mandated report
  format). The five §5 steps ship verbatim as the instruction titles:
  1. CONSOLIDATE (fragmented ask → its few MAIN IDEAS, 1–3, one line
     each; idea order ≠ implementation order),
  2. RESTATE (the fuller picture inline in the first substantive
     response, never a separate blocking question — verification +
     idea-expansion, the two Q-0254 payoffs),
  3. MAP (each idea → known step patterns via `docs/SKILLS.md`, exact
     skill/doc cited per idea; `docs/CAPABILITIES.md` before assuming
     walls),
  4. POSSIBILITY SPACE (feasibility-uncertain asks surface what is
     achievable FIRST; target = the most advanced capability reachable by
     the simplest, most efficient implementation),
  5. DECIDE-AND-FLAG (reversible calls decided with recommendation +
     one-line rationale + a run-report flag; owner questions ONLY as
     structured choices — A/B(/C), bolded recommendation, answerable with
     one letter, never parse/derive/transform work — Q-0263.2; unattended
     questions append to `docs/question-router.md`).
  Calibration retained from the doctrine: trivial/unambiguous asks stay
  exempt (one-line "doing X because Y"); big/vague ideas earn a delegated
  research pass reviewed same-session or their own session.
- **Doctrine mined from source, not memory:** superbot origin/main
  `.claude/CLAUDE.md` Q-0254 bullet, router Q-0254 (all three addenda —
  the owner's own mechanism words, the feasibility-first shape, the
  guiding-questions filter + kit graduation) and Q-0263 directive 2
  (paste-ready structured choices), `docs/owner/maintainer-working-
  profile.md`; kit templates `CONSTITUTION.md.tmpl` +
  `collaboration-model.md.tmpl` (the graduated prose the skill wraps).
  The body cites Q-0254 and Q-0263.2 explicitly (test-pinned).
- **Slice-2 prerequisites all satisfied:** `grounds` key present (`[]` —
  read-only, runs no commands); capabilities `[]` (read implicit, matching
  §5 "Declared capabilities: read"); every backticked body span resolves
  under `check_skill_grounds` at kit root AND on an empty adopter tree
  (all doc references are ADOPT_PLAN destinations / kit-shipped paths —
  NO new `_EXECUTABLES` / `_KIT_SHIPPED_PATHS` vocabulary needed, so the
  checker is untouched); report-format line ·-separated so the grounds
  scan skips it; `${...}` usage = `${project_name}` only (bank slot);
  `test_starter_pack_present_and_ordered` updated with the new order.
- **Index row** — renders automatically from the single `SKILLS` source
  (`skills_index_table`); no template or hand edits (the slice-1 rule:
  `docs/SKILLS.md` is never hand-edited).
- **Tests:** suite **1086 → 1093** (+7: step-title order pin, index-map
  routing, Q-0254 doctrine-content pin, structured-choice/Q-0263.2 pin,
  §5 report-format pin, read-only + grounds-empty pin, grounded-at-kit-
  root-and-empty-target pin).
- **CHANGELOG:** `[Unreleased]` entry added (release-skill precondition 1).
- **Dist:** rebuilt via `python3 src/build_bootstrap.py`; byte-pin clean.

Verify (verbatim tails): `python3 -m pytest tests/ -q` → `1093 passed in
16.58s` · `python3 -m ruff check src/engine/` → `All checks passed!` ·
`python3 dist/bootstrap.py check --strict` → sole red pre-flip = this
card's designed hold ("HOLD (by design)… nothing to investigate").

Accept criteria (§7.3): skill stages + installs ✔ (the SKILLS-driven adopt
tests count every entry; `cmd_skills --build` emits it); report format
matches §5 ✔ (`test_intake_report_format_matches_plan_section_5`, verbatim
section tokens).

**Decide-and-flag calls (plan silent on the detail):**

1. ⚑ SKILLS order: `intake` sits 4th, right after the ops-playbook
   cluster — slice 2 decided "the ops cluster leads the index"; inserting
   intake first would re-litigate that settled ordering for no functional
   gain. The ordering test pins the choice.
2. ⚑ `grounds: []` — the procedure runs no commands (it reads the index,
   the ledger, the profile), exactly the slice-2 card's prediction;
   grounding the doc reads as pseudo-commands would dilute the "grounds =
   exact commands" contract.
3. ⚑ Kept §5's five-step order (consolidate → restate → map → possibility
   space → decide-and-flag) over the coordinator summary's ordering
   (possibility-space before map) — the task brief says §7/§5 wins on
   divergence, and §7.3's accept criterion pins the §5 report format.
4. ⚑ Body enrichments beyond the §5 draft, all sourced from the mined
   provenance rather than invented: the "What this does" two-payoff
   paragraph (Q-0254 addendum 1), the trivial-ask exemption + big-idea
   research escalation (§5 closing note + Q-0254 addendum 3.4), the
   no-live-owner router-append route (Q-0254 addendum 3.2, matching the
   kit's own CONSTITUTION ask-rail), and explicit Q-0254/Q-0263.2
   citations (the phase-1 "must cite this provenance" mandate).
5. ⚑ `capabilities: []` (not a new READ constant in the list) — §5 says
   "Declared capabilities: read" and read is implicit for every skill;
   `question`/`analysis` are the exact precedent.

## Session enders

💡 **Session idea:** an intake-report grammar advisory — the /intake report
format is now test-pinned kit-side, but nothing checks that a session that
SAYS it ran intake actually printed the six sections (MAIN IDEAS … QUESTIONS
FOR OWNER). A cheap `check_skill_grounds`-style advisory could grep session
cards that cite `/intake` for the section tokens, the same
writer/enforcer-share-grammar pattern as `check_claims` — and it graduates
under Q2=B once proven. Dedup-checked against `docs/ideas/` (nearest:
slice-2's grounds-vs-CI parity idea — command parity, not report grammar).

⟲ **Previous-session review:** slice 2's card was the best handoff in the
program so far — its "slice-3 prerequisites discovered" block (grounds key
required, body span rules, checker vocabulary rule, ordering test) was a
complete, accurate spec; this slice needed zero re-derivation and the
checker needed zero changes exactly as predicted. One genuine improvement:
the prerequisites block named the RULES but not the fastest proof — a
one-line "add a per-skill `check_skill_grounds(root, skills=[new])` test
at kit root + empty target" recipe would have saved the only design pause
this slice had (how to prove span resolution without running the full
checker mentally). Workflow improvement: prerequisite blocks should carry
the verification recipe alongside each rule (the guard-recipe convention
`.sessions/README.md` already asks for friction entries).

Documentation audit: `check --strict` green at flip (this card's designed
hold excepted); durable homes are this card, the skills/test diff, the
CHANGELOG entry, and PR #270's description; the decide-and-flag list above
is the complete set of unrecorded judgment calls. Claim file deleted this
commit.

**Slice-4 prerequisites discovered (owner-assist output standard):**

- §3's rules land in TEMPLATES (`control-README.md.tmpl` OWNER-ACTION
  section + `collaboration-model.md.tmpl`), not skill bodies — planted-doc
  edits, so existing adopters only receive them via upgrade doc-classify
  (`template-improved` applies only under `--apply-docs` to
  consumer-untouched docs); state that expectation in the PR.
- The intake body now carries slice-4 language (structured choices, bolded
  recommendation, never parse/derive/transform) — slice 4 should reuse
  those exact phrases in the templates so skill and template text can't
  drift; the pins live in `test_intake_owner_questions_are_structured_choices`.
- `check_owner_actions.py` is the checker to extend (risk-class token
  `✅ / ↩️ / ⚠️` presence on manual steps; bare "go to settings"-class
  destination flags) — advisory posture per Q2=B, same
  provenance/kill-switch header convention as `check_skill_grounds`.
- Worked example: plan §3.4 is ready-made template content; the
  control-plane deep-link rules (§3.2/§3.3) reference the websites repo's
  live render — keep them as prose + example, no new engine keys needed.
