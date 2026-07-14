# 2026-07-14 · model-line payload lint (advisory)

> **Status:** `in-progress`

About to happen: build the `📊 Model:` payload lint from
`docs/ideas/model-line-payload-lint-advisory-2026-07-11.md` (Night-8 triage #3,
measured 4-of-5-card drift) — an advisory-only, never exit-affecting `check`
finding when a completed card's Model line breaks the three-field `·` shape,
carries an exact model-ID token instead of a family-level name, or files an
off-taxonomy effort / task-class segment; shared writer/enforcer constants land
in `engine.grammar` (EAP §6.8 pattern), telemetry consumes the same constants,
dist regenerated.

- **📊 Model:** fable-5 · high · feature build
