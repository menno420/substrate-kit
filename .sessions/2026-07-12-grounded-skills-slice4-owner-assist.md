# 2026-07-12 — grounded-skills program, slice 4: the owner-assist output standard

> **Status:** `complete`

- **📊 Model:** fable-5 · seat-worker · grounded-skills slice 4

## Scope (what is about to happen)

Implementing §7 slice 4 of the grounded-skills program plan
(`docs/planning/2026-07-12-grounded-skills-program.md`, merged PR #263):
the owner-assist output standard — §3's paste-ready block rules, risk-class
rules, exact-destination link rules, and the Q-0263.2 structured-choice
question format — landed in the kit's TEMPLATES (`control-README.md.tmpl`
as the canonical home, extending the OWNER-ACTION section, plus
`collaboration-model.md.tmpl`, with pointer-weight lines in
`CONSTITUTION.md.tmpl` and `question-router.md.tmpl`), the §3.4 worked
example included verbatim-grade, plus `check_owner_actions.py` extended
advisory per §7.4 (risk-class token on manual steps; bare "go to
settings"-class destination asks flagged). Shared constants in
`src/engine/grammar.py` pin skill ↔ template ↔ checker agreement (the
slice-3 card's prerequisite: reuse the intake body's test-pinned Q-0263.2
phrases — shared constants/test-pins, not textual copies). Tests +
CHANGELOG `[Unreleased]` entry + dist rebuild. No other slices, no adopter
work, no release.

**Provenance flag:** coordinator proceeded on plan §8 defaults — **Q1=A**
(control-plane link + 3-line digest as the default large-output delivery,
with full-text-in-chat fallback where the control plane can't render),
**Q2=B** (advisory-first checking; grammar checks graduate to CI-red only
once proven), **Q4=A** (the program supersession covers this slice under
the 2026-07-11 freeze). Vetoable at the owner's normal window.

Lane claim: `control/claims/claude-grounded-skills-slice4-owner-assist.md`
(deleted at close, this commit).

## Close-out

Shipped (PR #272; work commit 90a24d5):

- **Grammar — one home for the standard** (`src/engine/grammar.py`, new
  "Owner-facing output" section): `RISK_CLASS_TOKENS` (base characters
  `✅ ↩ ⚠` so plain and emoji-presentation spellings both match),
  `RISK_CLASS_LABEL`, `OWNER_ACTION_BLOCK_TOKEN`,
  `STRUCTURED_CHOICE_PHRASES` (the three Q-0263.2 phrases the intake body
  was already test-pinned to — **bolded recommendation** · answerable with
  one letter · parse, derive, or transform), `VAGUE_DESTINATION_WORDS` +
  `DESTINATION_SHAPE_MARKS`, canonical `risk_class_line_example` /
  `structured_choice_example`, and a `RISK:` line added to
  `owner_action_block_example`. The slice-3 prerequisite is satisfied as
  shared constants + shared test-pins: `tests/test_skills.py` (intake) and
  `tests/test_owner_assist.py` (templates) both assert the SAME grammar
  constants, so skill text, template text, and enforcer cannot drift.
- **`control-README.md.tmpl`** (canonical home): `RISK:` line in the
  OWNER-ACTION format block, plus the new section **"Owner-assist output
  standard — every owner-facing output, not just asks"** carrying §3.1
  rules 1–5 (paste-ready finished values + exact link to where each paste
  goes; exact destination, never a bare "go to settings"; risk class on
  every manual step; structured choices, recommendation first; large
  outputs as digest + rendered link with the Q1=A default and full-text
  fallback), the §3.2 link rules (deep-link the exact file / rendered
  view to read, blob URL to edit / `ref=main` post-merge / `&refresh=1`
  against the 180 s cache), the §3.4 worked example near-verbatim (a
  `RISK:` line added; PAT wording generalized), and the grammar
  source-of-truth pointer line.
- **`collaboration-model.md.tmpl`**: the standard's doctrine paragraph
  appended to "Routing work to the owner" (all three phrases + risk
  classes + Q1=A delivery, pointing at the canonical home).
- **`CONSTITUTION.md.tmpl`** + **`question-router.md.tmpl`**:
  pointer-weight lines — the ask-rail bullet extends with the standard's
  one-sentence form; the router's Options field is defined as a
  structured choice.
- **`check_owner_actions.py`** extended per §7.4, advisory-only (§8 Q2=B),
  PL-008 unverified/kill-switch header on the new checks:
  `owner-action-risk-class` (an `⚑ OWNER-ACTION` block whose contiguous
  paragraph carries no risk token — a token elsewhere in the file never
  vouches) and `owner-action-vague-destination` (a `WHERE:` value with a
  settings-like word AND no deep shape mark — URL/arrow/path). Same
  needs-owner≠none input gate as the fields nag; no cli.py changes needed
  (the advisory wiring was already in place).
- **Tests:** suite **1093 → 1116** (+23: grammar identity/examples, the
  two new advisory kinds + boundary/gating/exit-code pins, the shared-pin
  module `tests/test_owner_assist.py` covering intake body + all four
  templates + worked-example completeness + a dogfood scan that the
  example's own WHERE never trips the checker + a no-unrendered-slot
  guard on the new text).
- **CHANGELOG:** `[Unreleased]` entry incl. the distribution note.
- **Dist:** rebuilt via `python3 src/build_bootstrap.py`; byte-pin clean.

Verify (verbatim tails): `python3 -m pytest tests/ -q` → `1116 passed in
16.14s` · `python3 -m ruff check src/engine/` → `All checks passed!` ·
`python3 scripts/check_idea_index.py` / `check_program_law.py` /
`check_bench_integrity.py` → OK · `python3 dist/bootstrap.py check
--strict` → sole red pre-flip = this card's designed hold; plus ONE
expected advisory: `owner-action-risk-class` on the kit's own
`control/status.md` (13 blocks, none carrying a risk token yet) — the
designed migration pressure, cleared by this session's close-out status
overwrite (RISK lines added to all 13 blocks). Cold-adopt smoke run
locally: fresh adopt renders the standard section + RISK lines cleanly.

Accept criteria (§7.4): checker green on well-formed asks ✔ (structured
block + RISK line = zero findings, test-pinned); flags the Q-0263-incident
anti-patterns ✔ (`go to settings` fires vague-destination; unrisked manual
steps fire risk-class); worked examples included ✔.

**Distribution note (prerequisite (a), stated in the PR body too):** the
§3 rules land in planted-doc TEMPLATES — existing adopters receive them
only via upgrade doc-classification: `template-improved` applies only
under `upgrade --apply-docs` (consumer-untouched docs); edited copies get
a report line. The next distribution wave must run `--apply-docs` or
hand-merge the deltas from each repo's `.substrate/upgrade-report.md`.

**Decide-and-flag calls (plan silent on the detail):**

1. ⚑ Template homes: the coordinator brief named the
   CONSTITUTION/collaboration-model/question-router families; plan §7.4
   names control-README + collaboration-model. Landed the full standard
   in the two plan-named homes and pointer-weight lines (cite, don't
   copy — the house rule) in CONSTITUTION + question-router: both
   readings satisfied without duplicating rule bodies.
2. ⚑ `RISK:` ships as a taught line in the OWNER-ACTION block, NOT a 7th
   entry in `OWNER_ACTION_FIELDS` — a REQUIRED field would double-nag
   every existing structured ask through the fields check; §7.4's own
   wording ("risk-class token present on manual steps") is a separate
   advisory, which is what shipped.
3. ⚑ Risk tokens as base characters (no VS16) so both spellings match;
   coarse by design (a ⚠ used as prose inside a block passes it) —
   bounded by the contiguous-paragraph block rule, test-pinned.
4. ⚑ Vague-destination = intersection of a settings-like word AND no
   deep-shape mark — chosen so "any channel" reply-anywhere asks and
   every deep click path stay clean; verified zero vague findings on the
   kit's own 13-ask heartbeat.
5. ⚑ Worked example keeps the live control-plane URL from §3.4 (the
   fleet's real render surface — an invented placeholder URL would
   violate the standard's own exact-destination rule inside its one
   worked example).

## Session enders

💡 **Session idea:** enforce-by-generation for the standard's writer half —
a `session-close` step (or small `bootstrap` helper) that, given the
session's merged PR number and a report path, PRINTS the ready-made
§3.4-shaped output: digest skeleton + the correctly-formed control-plane
rendered link (`/journal/<repo>/file?path=…` at `ref=main`) + an
OWNER-ACTION block skeleton with the RISK line pre-filled. The enforcer
half shipped this slice; generating the correct shape mechanically beats
nagging after the fact (the same writer/enforcer-share-grammar move, one
step earlier). Dedup-checked `docs/ideas/` (nearest: slice-3's
intake-report grammar advisory — checker-side, not writer-side).

⟲ **Previous-session review:** slice 3's card again delivered a complete,
accurate prerequisites block — all four slice-4 items held exactly as
written (template homes, the pins' test location, the checker to extend,
§3.4 as ready-made content), and naming the precise test
(`test_intake_owner_questions_are_structured_choices`) made the
shared-constant wiring minutes, not a grep hunt. One genuine improvement:
the drift-proofing would have been cheaper still if slice 3 had homed the
Q-0263.2 phrases in `grammar.py` when it authored them — the writer knows
at authoring time which of its phrases are contract-grade; a slice that
declares "must not drift" text should create the shared constant in the
SAME PR rather than deferring the extraction to the consuming slice.

Documentation audit: CHANGELOG entry present; this card + the PR body
carry the distribution note; no new doc needs an index entry
(`check --strict` doc checks green); the decide-and-flag list above is
the complete set of unrecorded judgment calls. Claim file deleted this
commit. Capability delta: none — no new wall or capability discovered.

**Slice-5 prerequisites discovered (capability refresh + venue-scoping):**

- The checker-extension pattern is now twice-proven (slice 2
  `check_skill_grounds`, this slice): PL-008 header + advisory-by-contract
  docstring + the existing cmd_check advisory wiring — extend
  `check_capability_xref` in place; NO cli.py changes needed.
- Home the venue tokens (`owner-live · autonomous-project · routine-fired
  · subagent · any`) and the extended CAPABILITIES append-line grammar in
  `grammar.py` FROM THE START (this session's ⟲ lesson) so template,
  checker, and any writer helper share one constant from day one.
- The marker-fenced seed refresh (§4.2c) is a NEW upgrade mechanism —
  re-rendering ONLY a fenced block inside a `consumer-edited` doc is not
  hash-classification; budget it as the slice's main engineering with a
  fixture test on a consumer-edited ledger, and note it is the ONLY
  channel by which new seeds reach adopters (CAPABILITIES.md is
  consumer-edited by design, so `--apply-docs` never covers it).
- Verify the exact `staleness_days` config knob name in
  `src/engine/lib/config.py` before wiring discovery-rule step 5 to it.
- The superbot Q-0270 collapse (venue posture rule replacing local prose)
  must be documented in the upgrade report per §7.5's accept criterion —
  plan the wording as part of the slice, not the wave.
