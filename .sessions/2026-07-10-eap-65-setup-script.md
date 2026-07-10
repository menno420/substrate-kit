# 2026-07-10 — EAP §6.5: setup-script contract (template + checker)

> **Status:** `complete`

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

## What happened (close-out)

Shipped exactly the plan above. Build commit e26abde on PR #147 (claim #146
squash 2a8e2ae landed first, branch updated to pre-empt the behind-stall).

- **Writer**: `env-setup.sh.tmpl` → planted at `scripts/env-setup.sh`
  (ADOPT_PLAN tail entry, skip-if-exists). Slot-free by contract — pinned by
  `test_template_is_slot_free` — so a shell plant can never carry the
  markdown UNRENDERED banner and shell `$var` never reads as a slot.
- **Enforcer**: `src/engine/checks/check_setup_script.py` —
  `setup-fatal-posture` / `setup-no-exit0` / `setup-secret-value`, advisory-
  only (never exit-affecting; pinned by `test_findings_never_red_strict_check`),
  input-gated on the script existing, fail-open on unreadable. Wired into
  `cmd_check` (full lane only — the hook is not control-lane traffic) and
  `MODULE_ORDER`.
- **Writer/enforcer agreement pin**: `test_template_passes_the_enforcer` —
  the planted template passes the checker byte-for-byte; drift in either
  half reds the suite.
- **Surface fix found mid-build**: `check_engagement.scan_relpaths` (shared
  with `render --live`) would have flagged a host's hand-rolled hook carrying
  shell `${VAR}` as `unrendered-slot` and let `render --live` rewrite an
  executable file — `.sh` plants are now excluded from that surface
  (`test_shell_plants_excluded_from_unrendered_scan`).
- **Kit-local copy**: `scripts/env-setup.sh` (template + python-lab baseline
  per fleet-manager archetypes.md), smoke-run live: exit 0, editable install
  + pytest/ruff/build baseline installed.
- Verified: `python3 -m pytest tests/ -q` → **903 passed** (was 876; +27);
  `python3 -m ruff check src/engine/` clean; idea-index / program-law /
  bench-integrity OK; dist regenerated (byte-pin clean by construction);
  `python3 dist/bootstrap.py check --strict` → sole finding is this card's
  own born-red hold (verified, PL-006 — same class as #140/#144; the
  coordinator's mid-flight red ping on run 29129022244/job 86480552090 was
  exactly this, verified in the job log before dismissing).

Design decisions (decided-and-flagged):
1. **Plant, don't stage**: `scripts/env-setup.sh` goes in ADOPT_PLAN
   (skip-if-exists) rather than the staged `.claude`/CI opt-in set — the
   hook is inert unless the OWNER's environment shim calls it (the opt-in
   already lives owner-side in the pasted archetype script), and the
   archetypes doc itself names the per-repo hook as the durable fix.
2. **Path is a house-style constant** (`SETUP_SCRIPT_RELPATH`), not config:
   the fleet's archetype shims hardcode `scripts/env-setup.sh`, so a config
   knob could only produce a hook the shims never call (D-7 posture).
3. **No missing-file nag**: absence is adopt's job to fix (upgrade replants
   missing docs); a nag would spam never-adopted repos that `check` supports
   linting pre-onboarding.

- **💡 Session idea**: `bootstrap doctor --env` — a one-shot self-diagnosis
  verb that runs the setup-script checker + a dry-run trace of what
  `scripts/env-setup.sh` WOULD install (parse the guarded manifests) and
  prints the archetype the repo maps to; gives the owner a paste-ready
  answer to "is this environment wired right?" without booting a session.
  Dedup-checked against docs/ideas/ (no existing env-diagnosis idea).
- **⟲ Previous-session review**: the §6.4 claims session (#143/#144) left a
  clean convention + checker and its status record made this session's
  claim mechanics unambiguous — the claim-first fast-lane pattern worked
  exactly as documented. One improvement it missed: it queued §6.5 as
  "next" without noting the §6.5 inputs (the archetype material) live in a
  DIFFERENT repo (fleet-manager), so this session had to re-derive the
  feasibility check; queue entries for cross-repo-input slices should name
  the input's home repo + a freshness hint. Applied here: the status
  close-out's next-slice line names input homes.
- **📊 Model:** fable · high effort · kit dev slice (template + checker +
  tests + dist regen)
- Docs audit: CHANGELOG [Unreleased] carries the band; no new owner
  decisions to route; the new checker + template are reachable from the
  CHANGELOG entry and this card; control/status.md close-out rides the
  follow-up fast-lane PR (deliberate last step, per convention).
