# 2026-07-10 — EAP §6.10: auto-merge enabler workflow planted by the kit

> **Status:** `in-progress`

## What is about to happen

Coordinator-assigned slice (not an inbox order): EAP program review 2026-07-10
§6 item 10 — "auto-merge enabler workflow planted by the kit + repo-settings
one-time checklist in adopt". This repo runs its own
`.github/workflows/auto-merge-enabler.yml` (the superbot Q-0123 pattern: arm
GitHub-native auto-merge on agent PRs at open, refuse-to-arm when the base
requires no status contexts, `do-not-automerge` label carve-out with fresh
re-read). Adopters currently hand-fork it or lack it entirely.

Shipping kit-side, mirroring the substrate-gate.yml mechanism EXACTLY:

1. `automerge_enabler_workflow()` in `src/engine/adopt.py` — the generated,
   parameterized enabler; `AUTOMERGE_ENABLER_RELPATH =
   .github/workflows/auto-merge-enabler.yml` (same basename adopters
   hand-forked, so existing forks fall under kit ownership on upgrade).
2. Staged ALWAYS at `<state_dir>/ci/auto-merge-enabler.yml` next to the gate;
   installed LIVE only on `--wire-enforcement`; once it EXISTS it is
   KIT-OWNED — every adopt/upgrade regenerates it in place with the #137
   carve-out protection (detect host-added jobs/steps, bank the pre-regen
   copy content-hash-named under `<state_dir>/backup/`, report
   `carve-out:` lines that flow into upgrade-report.md).
3. Parameterization via the existing config surface:
   `substrate.config.json` → `automerge` (`branch_patterns`, default
   `["claude/*"]`; `required_context`, default `substrate-gate`) —
   fallback-on-empty like `heartbeat_files`.
4. Carve-out label: `do-not-automerge` (kit doctrine,
   docs/operations/auto-merge-guards.md guards 1–2) — job-level skip AND the
   fresh-label re-read race guard travel into the planted file.
5. Repo-settings one-time checklist emitted by adopt when the live enabler
   is present (Allow auto-merge ON · required check on the default branch ·
   optional auto-update/auto-delete branches).
6. Adopter boundaries DOCUMENTED (not fixed) in
   docs/operations/auto-merge-guards.md: trading-strategy's repo-level
   "Allow auto-merge" is OFF (a workflow cannot flip repo settings — standing
   owner item); fleet-manager's R21 wall (GitHub structurally refuses the arm
   on born-red / no-CI repo shapes — REST merge-on-green is that shape's
   landing path).
7. Tests mirroring the gate coverage (plant on wire-enforcement, never on
   default adopt, kit-owned regen + kept-when-current, carve-out banking,
   parameterization rendering) in tests/test_adopt.py + tests/test_upgrade.py.
8. CHANGELOG [Unreleased] (v1.8.0 payload); dist regenerated + byte-pinned.
   NO release cut this session.

Claim: `control/claims/eap-6.10-automerge-enabler.md` (PR #152, fast lane,
armed).
