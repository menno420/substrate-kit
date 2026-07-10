# 2026-07-10 — EAP §6.5: setup-script contract (template + checker)

> **Status:** `in-progress`

## What is about to happen

Coordinator-assigned slice (not an inbox order): EAP program review 2026-07-10
§6.5 — the setup-script contract. The fleet runs six divergent hand-rolled
environment setup scripts; the manager's archetype material (fleet-manager
`environments/archetypes.md` + 5 tested archetype scripts + the canonical
`templates/setup-universal.sh` shim, verified present at fleet-manager@ced65b4)
defines ONE contract every per-repo script must satisfy: **always exit 0 ·
defensive posture (`set +e`) · no secret values · guarded installs**. Every
archetype script prefers a repo's own `scripts/env-setup.sh` when it exists —
but the kit never plants one, so no adopter has the durable per-repo hook.

Shipping kit-side:
1. `env-setup.sh.tmpl` planted at `scripts/env-setup.sh` (ADOPT_PLAN,
   skip-if-exists; slot-free by design so a shell file never carries the
   markdown UNRENDERED banner) — rendered FROM the archetype contract.
2. `check_setup_script` — advisory-only checker (writer/enforcer pair):
   `setup-fatal-posture` / `setup-no-exit0` / `setup-secret-value`, engaging
   only when the script exists.
3. cli wiring + MODULE_ORDER + tests pinning template↔checker agreement +
   CHANGELOG [Unreleased] + kit-local `scripts/env-setup.sh` + dist regen.
   NO release cut this session.

Claim: `control/claims/eap-6.5-setup-script.md` (PR #146, fast lane, armed).
