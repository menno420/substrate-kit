# Session — backlog-recipes (planning slice)

> **Status:** `complete`

## What I did
Turned the four NEEDS-PLANNING backlog items into turnkey recipes parked at
`docs/planning/2026-07-19-needs-planning-recipes.md`: folded-gate-diff-aware-card,
pinned-feed-contract, t5-headless-guard, control-board-kit-readiness-cell. Chased each
origin (docs/ideas/ + shipped sibling #19 + ORDER 003), stated the Q-0254 fuller picture,
classified each, and retargeted the heartbeat baton at the ranked results. Honest shrink:
2 buildable-now from this repo (pinned-feed doctrine; folded-gate advisory checker — its
"second occurrence" build trigger is now met), 1 owner-gated + cross-tree (t5-headless-guard,
pin-path bench/tasks/T5.md in kit-lab → six-field ⚑), 1 kit-half-done (readiness-cell —
ORDER 003 shipped the kit side; remaining is a cross-repo websites feature).

## Provenance
Coordinator planning dispatch under fm control/inbox.md ORDER 048 standing grant + the
standing "when no executable work is left, plan" resume order. Buildable backlog dry after
GSW-1..4, B-1..3, and the #479 harness graduation.

## Verify
pytest: 1811 passed / 1 skipped. `python3 dist/bootstrap.py check --strict` green after this
flip (born-red hold cleared; badge + orphan findings fixed).

## 💡 Session idea
**Planning-recipe as a first-class session type / skill.** This session ran a repeatable
arc — chase each backlog item's origin, state its Q-0254 fuller picture, classify
buildable-now / owner-gated / dead with a sized recipe or a six-field ⚑, then retarget the
baton — and that arc is re-derived by hand every time the buildable backlog goes dry. A
`docs/SKILLS.md` skill (e.g. `/scope-backlog-item`) that scaffolds exactly this structure
would make the standing "when no executable work is left, plan" order turnkey instead of
ad-hoc, and would make every scoping pass's output uniformly shaped for the next reader.
Deduped against `docs/ideas/` + `docs/SKILLS.md` — no existing planning-recipe/scope-backlog
skill idea.

## ⟲ Previous-session review
GSW-4 (PR #476 lineage, GitHub-API latency pass) was a strong card: it froze an auditable
JSON artifact with a cited sha256, kept the reachability link intact, and — its best move —
surfaced and *closed* a real gap it found in GSW-1..3 (open→merge latency was silently
out-of-scope rather than tracked as deferred-optional). What it left short: it named the fix
("make deferred-optional a standing nulls category") but only as prose in the review, so the
insight lives in one session card instead of being enforced. **Improvement it surfaces:** the
grounded-skills report template (§4 nulls) should carry an explicit `Deferred-optional`
subsection as a template field, so an optional-but-unrun measurement is structurally accounted
for on every future window run rather than depending on a reviewer remembering to log it —
enforce-don't-exhort applied to the report itself.

## 📊 Model: Opus 4.8 · high · planning / needs-planning-recipes
