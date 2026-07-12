# 2026-07-12 — grounded-skills program, slice 2: playbook bodies + grounds + advisory checker

> **Status:** `complete`

- **📊 Model:** Claude 5 family · seat-worker · grounded-skills slice 2

## Scope (what was about to happen)

Implementing §7 slice 2 of the grounded-skills program plan
(`docs/planning/2026-07-12-grounded-skills-program.md`, merged PR #263):
upgrade `session-close` to the full landing-path playbook, add
`upgrade-distribution` (wave runbook) and `release` (cut runbook) as
playbook-grade skill bodies with exact command groundings; add a per-skill
`grounds` field surfaced as a new `skills_index_table()` column (the exact-
commands column slice 1 deferred); ship the slice-1 💡 idea as an advisory
grounds checker (`src/engine/checks/`), never exit-affecting (Q2=B); tests +
dist rebuild.

**Provenance flag:** proceeded on the plan's §8 recommended defaults per the
coordinator — **Q2=B** (advisory-first; graduation to CI-red only once
proven) and **Q4=A** (program supersession covers this slice under the
2026-07-11 freeze). Vetoable at the owner's normal window.

Lane claim: `control/claims/claude-grounded-skills-slice2.md` (deleted at
close, this commit).

## Close-out

Shipped (PR #265; implementation commit 2f40efa):

- **Playbook bodies** (`src/engine/skills/skills.py`), superbot anatomy
  (purpose → What this does → numbered Instructions → mandated report
  format → known failure modes):
  - `session-close` upgraded from a 7-step checklist to the full landing
    path: claim-first (one file, `check_claims` grammar), born-red card as
    FIRST commit, open PR READY immediately, never self-arm/self-merge
    (server-side enabler; deny-wins classifier), batch pushes, designed-red
    reading (verify reds against the job log; alias jobs mirror
    `kit-quality`), close-out doc set (capability delta, OWNER-ACTION
    fields, idea grooming — all retained from the old body), flip
    `complete` as the deliberate LAST step, delete own claim.
  - `upgrade-distribution` (NEW): preflight `git fetch origin main && git
    reset --hard origin/main` → `gh release download` → sha256 three-way
    (asset vs `release.json` field vs kit `dist/bootstrap.py` at bump SHA)
    → born-red PR → `python3 bootstrap.py.new upgrade` (bank verified) →
    carve-out scan (`.substrate/upgrade-report.md`: consumer-edited /
    diverged listed verbatim) → tree-over-registry merge verification.
    Report: one outcome line per repo. Failure modes: W-8 label-race →
    empty-commit cure; ~25-min stale MCP PR reads → probe the tree; W-9
    designed-hold red-pings → job-log truth.
  - `release` (NEW): the cut runbook (mined from
    `docs/operations/release-runbook.md` + `release.yml`): both version
    homes in ONE commit, CHANGELOG machine comment, dist regen + byte-pin,
    exact five-command local verify battery, `gh workflow run release.yml
    -f version=X.Y.Z`, post-release three-way verification, adopter wave +
    `currency` regen aftermath. Failure modes: tag-push 403 (dispatch path
    tags in-Actions), refuse-to-release guard, never-delete-releases.
- **`grounds` field** — structured per-skill list of exact command strings.
  Test-pinned invariants: present on every skill; non-empty for the three
  playbook skills; every entry appears VERBATIM as a backticked body span
  (no body/grounds drift possible); bank-slots only; no multiline entries.
  Read-only skills ground `[]`.
- **Index column** — `skills_index_table()` grew `Grounds (exact
  commands)`, `<br>`-joined backticked entries, `—` when empty. Slot refs
  fill from the context `build_context` now passes in; unfilled slots
  display as `<slot_name>` — raw `${...}` NEVER survives into the planted
  `docs/SKILLS.md` (it would re-banner the index forever: render() cannot
  fill a substitution value, re.sub never rescans).
- **Advisory checker** — `src/engine/checks/check_skill_grounds.py`
  (provenance/kill-switch header: added 2026-07-12, PL-008 UNVERIFIED,
  delete-if-unreliable). Extracts backticked spans from SKILLS bodies +
  `grounds` + the target's rendered skill docs (`.claude/skills/`,
  `<state_dir>/skills/`); first token must resolve (whitelisted
  executable / gh-mcp verb, target file, or kit-shipped path incl.
  ADOPT_PLAN destinations); fail-open skip ladder (slots, non-ASCII
  report-format prose, placeholders, flags, dirs, state-dir artifacts,
  bare status tokens). Wired into `cmd_check`'s advisory loop
  (`src/engine/cli.py`) — surfaced + guard-fire-recorded, **never
  exit-affecting** (§8 Q2=B); full lane only. MODULE_ORDER slot after
  `adopt.py` (`src/build_bootstrap.py`).
- **Tests:** suite **1065 → 1086** (+21: grounds invariants, playbook-body
  content pins, index grounds column + context fill, checker detection /
  skip-ladder / fail-open / cmd_check-advisory-posture integration; kit
  self-grounding pinned both at kit root and on an empty target).
- **CHANGELOG:** `[Unreleased]` entry added (the release skill's own
  precondition 1).

Verify (verbatim tails): `python3 -m pytest tests/ -q` → `1086 passed in
28.07s` · `python3 src/build_bootstrap.py` → `wrote …dist/bootstrap.py
(735972 bytes)`, `git diff --exit-code dist/bootstrap.py` clean ·
`python3 -m ruff check src/engine/` → `All checks passed!` ·
`python3 dist/bootstrap.py check --strict` → sole red pre-flip = this
card's designed hold (job-log-verified on CI run 29190493556: "HOLD (by
design)… nothing to investigate"; both alias jobs mirror) ·
`scripts/check_idea_index.py` / `check_program_law.py` /
`check_bench_integrity.py` all OK.

Accept criteria (§7.2): each body names only commands that exist ✔
(checker + `test_kit_skill_set_fully_grounded_at_kit_root`); suite green ✔;
bodies regenerate at upgrade ✔ (staged artifacts always regenerate — the
existing adopt/upgrade machinery, unchanged).

**Decide-and-flag calls (plan silent on the detail):**

1. ⚑ Grounds ⊆ body invariant — every grounds entry must appear verbatim
   as a backticked body span (test-pinned), so the structured field can
   never drift from the prose procedure.
2. ⚑ New skills sit right after `session-close` in SKILLS order (the ops-
   playbook cluster leads the index); the ordering test was updated.
3. ⚑ `quality-gate` / `repo-health` bodies' `bootstrap check` spellings
   upgraded to the exact `python3 bootstrap.py check [--strict]`
   invocation — two lines outside the named three bodies, taken for
   grounds honesty (`bootstrap` shorthand stays whitelisted for legacy
   staged copies).
4. ⚑ `release` body names substrate-kit explicitly (the runbook is
   kit-repo-specific by content; `${project_name}` appears only as the
   consumer framing) — avoids a misleading "cut a <adopter> release"
   rendering.
5. ⚑ Grounds-column slot handling: `skills_index_table(context)` fills
   from the project's slots; unfilled → `<slot_name>` display, never raw
   `${...}` (the re-banner trap). Signature change is back-compatible
   (optional arg).
6. ⚑ Checker also scans the target's RENDERED skill docs, and skips
   non-ASCII spans (·/→/✔ = report-format prose) — the two judgment calls
   that kept kit-root findings at zero without weakening fake-command
   detection.
7. ⚑ `control/status.md` last-shipped line surgically prepended
   (coordinator-directed); everything else in the heartbeat untouched.
8. ⚑ CHANGELOG `[Unreleased]` entry added this PR (slice 1 did not add
   one; the release skill's precondition 1 makes per-PR entries the
   playbook — follow-on sessions should keep doing this).

## Session enders

💡 **Session idea:** grounds-vs-CI parity check — the `release` and
`quality-gate` grounds now duplicate command lines that also live in
`ci.yml` / `release.yml` / the runbook; a small advisory could parse those
workflow files and verify each grounds entry for kit-ops skills appears in
(or prefixes) a real CI/workflow step, so the playbook can never drift from
the pipeline it describes. Dedup-checked against `docs/ideas/` (nearest:
`staged-artifact-regen-lag-checker-2026-07-12.md` — regen lag, not command
parity; `engagement-wiring-strength-verification-2026-07-12.md` — gate
wiring, not skill grounds).

⟲ **Previous-session review:** slice 1 (PR #264) seeded this slice
unusually well — the deferred-grounds-column rationale, the 💡 checker
spec, and the ${slot}/MODULE_ORDER notes on its card were exactly the
prerequisites needed, and near-zero re-derivation was spent. One miss: it
did not name the SURFACES where rendered skill bodies live
(`.claude/skills/` vs `<state_dir>/skills/` staging), which this slice had
to re-derive before the checker could scan them. Workflow improvement:
when a session card seeds a follow-on checker/scanner, include a one-line
"scan surfaces" inventory (exact paths) alongside the idea.

Documentation audit: `check --strict` green at flip (this card's designed
hold excepted); durable homes are this card, the engine/test diff, the
CHANGELOG entry, and PR #265's description; the decide-and-flag list above
is the complete set of unrecorded judgment calls. Claim file deleted this
commit.

**Slice-3 prerequisites discovered:**

- Adding a skill = one SKILLS entry + updating
  `test_starter_pack_present_and_ordered` (order is pinned); ADOPT_PLAN
  generics and the index pick it up automatically; the grounds key is now
  REQUIRED on every entry (well-formed test) — `/intake` will likely ground
  `[]` unless its steps name commands.
- Body rules a new skill must obey (test-pinned): `${...}` only from the
  interview bank (no engine keys), grounds verbatim-in-body, no multiline
  grounds, command spans on one line, report-format template lines either
  non-ASCII-separated (`·`) or placeholder-led so the grounds scan skips
  them.
- New command vocabulary in future bodies must resolve for
  `check_skill_grounds` — extend `_EXECUTABLES` / `_KIT_SHIPPED_PATHS` in
  `src/engine/checks/check_skill_grounds.py` in the same PR.
- `skills_index_table` now takes an optional context; anything else that
  renders the index should route through `build_context` rather than
  calling the table bare, or slot-bearing grounds display as `<slot>`.
