# Session · 2026-07-16 · registry-refresh

> **Status:** `complete`

Intent: regenerate `docs/adopters.md` from live discovery — registry truth by discovery — resolving the committed-registry drift that accrued while the kit-lab daily regeneration cron is parked.

- **📊 Model:** Opus 4.8 · medium · mechanical refactor
- ⚑ Self-initiated: regenerated docs/adopters.md from live discovery (registry truth by discovery) in the kit-lab currency cron's absence — contained, reversible, read-only sibling discovery, no adopter-repo writes; rung (c) mission increment.

## Scope / What this session does

Regenerate docs/adopters.md from live discovery — registry truth by discovery. The kit-lab daily cron that normally regenerates this is currently missing (parked A/B owner ask), so the committed registry (Generated 2026-07-16T02:14:56Z) had drifted from source truth. This refresh resolves the substrate-kit self-report drift row (its control/status.md now truthfully reports v1.18.0) and updates fleet-manager's self-report to the truthful 'no kit: line' live read. 12 repos scanned, COMPLETE, no degraded reads; gate + adopters format test green.

## 💡 Session idea

Adopters staleness self-signal — `check --strict` should emit a NON-gating advisory when docs/adopters.md's `Generated:` timestamp is older than one daily currency cycle + slack (~26h). Root cause seen this session: the kit-lab daily currency cron is currently missing, so the registry went stale silently with no signal — caught only by manual regen. A timestamp-age advisory turns a missing/failed cron into a visible nudge (enforce-don't-exhort, PL-007) without needing the cron itself.

## ⟲ Previous-session review

The previous session graduated the no-badge status-grammar finding into check_log and extracted the shared `_status_grammar_findings()` helper — cleanly DRY, one home for badge + no-badge grammar checks. Gap it left: the `model-line-class` advisory currently fires on a recent session card whose `📊 Model:` task-class is off the PL-004 taxonomy — a card-authoring session left its own model line invalid. Concrete system improvement: have the born-red session-gate validate the FLIPPING card's own `📊 Model:` task-class against the taxonomy at flip time (not just a post-hoc advisory), so a card can't merge with an off-taxonomy model line.
