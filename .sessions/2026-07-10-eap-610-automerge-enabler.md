# 2026-07-10 — EAP §6.10: auto-merge enabler workflow planted by the kit

> **Status:** `complete`

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

## What happened (close-out)

Shipped the plan above, whole. Build commit 7f89e57 on PR #153.

- **Generator**: `automerge_enabler_workflow()` in `src/engine/adopt.py` +
  `AUTOMERGE_ENABLER_RELPATH` (`.github/workflows/auto-merge-enabler.yml` —
  the shared basename means adopter hand-forks fall under kit ownership on
  their next upgrade) + `AUTOMERGE_CARVEOUT_LABEL` (`do-not-automerge`, a
  constant not config — program-wide vocabulary). Safety shape carried from
  the origin workflow: same-repo fork guard, branch-pattern arming,
  refuse-to-arm on zero required CONTEXTS (base-branch rules API,
  generalized from hardcoded `main` to `github.base_ref`), label carve-out
  at job level + the fresh-API-re-read race guard, `synchronize` re-arm.
  Rendered output validated as parseable YAML.
- **Lifecycle = the gate's, exactly (decided-and-flagged)**: staged always
  at `<state_dir>/ci/auto-merge-enabler.yml`; live install ONLY on
  `--wire-enforcement`; existence = opt-in for kit-owned regen. Rationale:
  "the kit never installs live CI silently" is the standing safety
  doctrine, and a live enabler is the more dangerous artifact class (it
  arms merges) — no reason to be looser than the gate. The gate's inline
  regen block was factored into a shared `_regen_kit_owned_workflow()`
  (byte-identical report strings for the gate path; pre-existing suites
  pass unchanged), so the #137 carve-out protection (detect host-added
  jobs/steps → bank content-hash-named under `<state_dir>/backup/` →
  report `carve-out:` lines that flow into upgrade-report.md) applies to
  both workflows via ONE mechanism.
- **Parameterization (decided-and-flagged)**: `substrate.config.json` →
  `automerge` dict — `branch_patterns` (default `["claude/*"]`; trailing
  `*` = prefix match, else exact; empty / blank / bare-`*` lists fall back
  to the default per the heartbeat_files fallback-on-empty doctrine — a
  misconfiguration must never silently widen arming to every branch) and
  `required_context` (default `substrate-gate`, the planted gate's job
  name; informational only — the refuse-to-arm guard counts contexts
  generically, so a wrong name mislabels a log line, never the guard).
- **Repo-settings one-time checklist** (§6.10's second half): emitted in
  the adopt report whenever the live enabler is present — Allow auto-merge
  ON · require the configured context on the default branch · optional
  auto-delete/auto-update branches.
- **Adopter boundaries documented (not fixed)** in
  `docs/operations/auto-merge-guards.md` § "The kit-planted enabler":
  trading-strategy's repo-level "Allow auto-merge" is OFF (owner item — a
  workflow cannot flip repo settings); fleet-manager's R21 wall (GitHub
  structurally refuses the arm on born-red/no-CI shapes; REST
  merge-on-green is that shape's landing path — the planted enabler's
  failure warning says so).
- **Tests (+7, suite 920 → 927)** mirroring the gate coverage in the
  existing modules: workflow shape + carve-out label + refuse-to-arm
  (test_adopt), parameterization + fallback-on-empty (test_adopt), staged
  always / never live by default / no checklist without a live enabler
  (test_adopt), wire-enforcement plant + checklist (test_adopt), kit-owned
  regen of a hand-fork rendered from host config + kept-when-current
  (test_adopt), carve-out banking on adopt (test_adopt), carve-out
  surfacing in upgrade-report.md (test_upgrade).
- CHANGELOG `[Unreleased]` §6.10 entry (v1.8.0 payload; NO release cut).
  Dist regenerated (`python3 src/build_bootstrap.py`), compiles, byte-pin
  suite green.
- Verified: `python3 -m pytest tests/ -q` → **927 passed** (was 920, +7);
  `python3 -m ruff check src/engine/` clean; `python3 dist/bootstrap.py
  check --strict` → sole finding was this card's own born-red hold before
  this flip. Mid-flight coordinator red ping on head 1ad7b89 root-caused
  per PL-006 (job log 86486411915 read before dismissing): the designed
  born-red session-gate hold (the #140/#144/#147 class) — missing close-out
  markers + in-progress badge; no defect.

- **📊 Model:** Fable 5 · high effort · kit-dev-slice (feature + tests)

💡 Session idea: an `adopt --check-repo-settings` (or `doctor --repo`)
probe — the repo-settings checklist is currently exhortation; when a
GH_TOKEN is ambient the kit could ATTEMPT the read-only halves (rules API
context count, `allow_auto_merge` via `GET /repos/{owner}/{repo}`) and
print VERIFIED per-item state instead of a blind checklist — turning the
§6.10 checklist from "please check" into "checked: item 1 OFF, item 2
missing" (enforce-don't-exhort applied to owner asks; pairs with the
carried `bootstrap doctor --env` idea).

⟲ Previous-session review (§6.8, #149/#150/#151): clean writer↔enforcer
slice — its factor-to-one-home pattern is exactly what this session reused
for `_regen_kit_owned_workflow`, and its status HEADLINE (the `${VAR}`
poison) plus queued fix (4) let this session write close-out prose that
deliberately avoids dollar-brace literals. What it could have done better:
its card's "grammar deliberately NOT injected as render slots" decision is
recorded only in prose — a tiny agreement test asserting templates carry no
grammar slots would pin it. Concrete workflow improvement carried forward:
the queued kit-fixes batch (4 items) should land as ONE dev slice before
v1.8.0 so the release notes describe a scanner that no longer false-reds.

Docs audit: CHANGELOG carries the payload entry; the guards doc carries the
enabler section + boundaries; status close-out (squash SHA + CI run +
next-slice pointers) follows as the fast-lane heartbeat PR per the #148/#151
precedent; claim `control/claims/eap-6.10-automerge-enabler.md` is deleted
there. No inbox ORDER 012+ existed at preflight (highest 011, done).
