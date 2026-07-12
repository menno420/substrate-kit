# 2026-07-12 — grounded-skills program, slice 4: the owner-assist output standard

> **Status:** `in-progress`

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
(deleted at close).
