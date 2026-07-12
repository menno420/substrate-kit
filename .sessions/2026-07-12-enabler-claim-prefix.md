# 2026-07-12 — auto-merge-enabler: arm claim/* branches (end the #293 stall class)

> **Status:** `in-progress`

- **📊 Model:** fable-5 · seat worker slice

## Scope (what is about to happen)

Widen the auto-merge-enabler's branch-prefix arming from `claude/`-only to
`claude/` + `claim/` — the verified stall class from kit PR #293 (a control
fast-lane claim PR on a `claim/*` head sat green+clean unarmed for ~2 h until
superseded by #297 on a claude/* branch). Both copies: (1) the kit's OWN
`.github/workflows/auto-merge-enabler.yml`; (2) the kit-owned generated
adopter enabler (`engine.adopt.automerge_enabler_workflow` defaults +
`config._default_automerge`), so the fix reaches the fleet at the next
release wave. Plus: regression tests, the guards-playbook note, CHANGELOG
`[Unreleased]`, dist rebuild (byte-pin). Claim: kit PR #299.
