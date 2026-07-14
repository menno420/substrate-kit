# 2026-07-14 · kit-side scripts/preflight.py (CI-convergence dogfood)

> **Status:** `complete`

About to happen (opening declaration): build the kit-repo-local
`scripts/preflight.py` so the kit dogfoods its own ORDER 018 preflight
mechanism — `config.py::_default_preflight_scripts()` defaults to
`["scripts/preflight.py"]` but the file doesn't exist here, so every full
`check` prints a standing NOTE and local `check --strict` runs none of the
7 CI kit-quality legs (the local-green→CI-red class from ASK 002 /
idea-engine #274/#299). Pure kit-repo addition: no engine/src change, no
dist regen, no adopter surface.

- **📊 Model:** fable-5 · high · feature build

Run type: worker session (coordinator-dispatched BUILD+LAND).

## What shipped (PR #354)

- `scripts/preflight.py` (new, stdlib-only): the idea-engine convergence
  pattern — a module-level `CHECKS` table of the seven ci.yml kit-quality
  legs (pytest · dist byte-pin as build-then-diff · ruff with a skip-NOTE
  when not importable locally · idea-index · changelog-structure ·
  program-law WITHOUT `--label-gate`, labels being CI-only ·
  bench-integrity) + a worst-exit runner where a red leg never stops the
  rest. Recursion guard verified against `_run_preflight_scripts`
  (src/engine/cli.py:898) first: the cli stamps `SUBSTRATE_KIT_PREFLIGHT=1`
  into the script's OWN child env, so this script self-skips exit-0 with a
  one-line note when the marker is set — the direct run
  (`python3 scripts/preflight.py`) is the seven-leg entry point, exactly the
  idea-engine convention; a check-spawned run (always marked) can never
  recurse into the pytest leg. `--list` prints leg names running nothing;
  `--only <name>` runs one leg; module-level `CHECKS` is the test-injection
  surface.
- `tests/test_kit_preflight.py` (16 tests, no test ever spawns the real
  pytest leg): worst-exit aggregation with injected fake legs (0,0→0;
  0,2→2; first-fails-still-runs-rest), multi-command-leg stop-at-first-
  nonzero, uncallable-command→2, main() red-fixture mutation proof
  (inject-red exit 3 propagates; fixed→0), the SUBSTRATE_KIT_PREFLIGHT
  self-skip path (failing leg never runs, exit 0), the ruff-absent NOTE
  path (would-red ruff leg skipped, not red) + ruff-present runs,
  `--list` pins the 7-leg set / runs nothing, `--only` selection + unknown
  name→2, guard-name identity pin (`preflight.NESTED_ENV ==
  cli._PREFLIGHT_NESTED_ENV`), and CI-command-shape pins on the real table
  (incl. program-law must never carry `--label-gate`).
- `CHANGELOG.md` `### Added` entry under `[Unreleased]`
  (check_changelog_structure green).
- Idea graduated: `docs/ideas/kit-preflight-dogfood-2026-07-14.md`
  (frontmatter promoted/shipped, shipped_pr 354) + README index line in the
  "Shipped (survive window open)" section (window closes 2026-08-13).
- `.substrate/guard-fires.jsonl` delta committed per the ledger instruction
  (includes the DEMO-RED stub fire below — the ledger records what fired).
- Park state: NO auto-merge armed by this session — parked green for a
  non-author review-merge (the server-side enabler may arm non-draft
  `claude/*` PRs on its own, as with #349/#351/#352).

## Decide-and-flag

- **Cold-adoption smoke excluded from the local leg set.** ci.yml's §3.2
  item 4 (scratch adopt + the RED→ENGAGED→GREEN arc) is shell-heavy and
  slow; including it would make every local preflight minutes-long for a
  leg that never depends on local state. CI keeps it. Reversible: one
  CHECKS entry.
- **Idea frontmatter `merged_date` set to the anticipated date
  (2026-07-14), not null.** The dispatch left this to whatever
  `check_idea_index.py` enforces — it enforces `outcome: shipped` ⇒ ALL
  three ship fields non-null (validate_fields, `outcome-inconsistent`), so
  a null merged_date would red the index. Matches the #349/#351/#352
  in-PR flip convention; noted in the idea file's State chain.

## Verify

- Baseline at HEAD a67ccda: 1394 passes (SELECT phase). Final:
  `python3 -m pytest -q` → `1410 passed in 26.69s` (+16, zero failures).
- **Before** (clean tree, kit-preflight stash-popped away):
  `python3 dist/bootstrap.py check --strict` printed the standing NOTE —
  `check: NOTE — preflight script scripts/preflight.py not found — skipped
  (config preflight_scripts; plant one to converge the local ritual and
  the CI gate on one check list).`
- **After** (script planted): the same run has ZERO `preflight script`
  NOTE lines; the only red is this card's own designed born-red hold
  (`check: HOLD (by design): session card … declares an in-progress
  Status`), flipped at close.
- **Proof the check leg executes the file** (a green leg is silent by
  design — capture_output): temporarily stubbed `scripts/preflight.py`
  to `sys.exit(1)`; `check --strict` then emitted
  `[preflight-script] scripts/preflight.py: exit 1: DEMO-RED: temporary
  stub — the CI substrate-gate runs this same preflight; fix it before
  pushing.` — restore verified byte-identical (`cmp`).
- **Failing-leg live demo via the override mechanism** (module-level
  CHECKS injection), verbatim:

  ```
  preflight: FAIL — inject-red (exit 1)
  preflight: PASS — still-runs (exit 0)
  preflight: FAIL — worst exit 1
  demo main() returned: 1
  ```

- **Full real run end-to-end** (direct, unmarked env): all seven legs —
  tail verbatim: `preflight: PASS — bench-integrity (exit 0)` /
  `preflight: OK — 7 leg(s) green`. Nested self-skip live:
  `SUBSTRATE_KIT_PREFLIGHT=1 python3 scripts/preflight.py` →
  `preflight: skipped — nested run (SUBSTRATE_KIT_PREFLIGHT set; the outer
  run owns the legs).`
- Dist untouched + byte-stable: `python3 src/build_bootstrap.py` twice →
  sha256 `bbe4b57414fd618db958990a16f6b1c3e8b75184edae6a3bfeac6542afb17372`
  both times; `git diff --exit-code dist/bootstrap.py` clean.
- `python3 scripts/check_idea_index.py` / `check_changelog_structure.py` /
  `check_program_law.py` → all OK.

## Enders

💡 **Session idea:** make the preflight leg's green run POSITIVELY visible
in `check` output — today `_run_preflight_scripts` captures the child's
output and discards it on exit 0, so a green run is indistinguishable (in
the transcript) from the script self-skipping or silently doing nothing;
this session had to stub the script RED just to prove the leg executes the
file. One `check: preflight script <rel> — exit 0` note per executed
script (optionally echoing the child's last line, which for this script is
`preflight: OK — N leg(s) green` / the nested-skip note) would make the
convergence leg auditable from the check transcript alone. Dedup-grepped
`docs/ideas/` (42 files): `enabler-install-preflight` and the parity ideas
cover different surfaces; nothing covers leg-run evidence.

⟲ **Previous-session review** (the #353 check_claims own-date fix): a
model friction→guard turnaround — the #352 card recorded the claims-stale
false positive with an exact guard recipe (last date on the bullet line,
file + line number), and #353 shipped precisely that fix the same night
with a dated-filename fixture, suite 1391 → 1394. The loop worked because
the recipe was unusually concrete. Concrete workflow improvement: guard
recipes live only in session-card "Friction → guard candidates" sections,
consumed by the next session remembering to read them — a tiny sweep
(check-time advisory or a groom step) listing UNCONSUMED guard recipes
from recent cards would make the #352→#353 handoff mechanical instead of
memory-dependent.

**Documentation audit:** CHANGELOG entry rides the PR; idea file +
README index line shipped with checker-verified frontmatter; the
decide-and-flag calls are recorded here and in the PR body; the outcome
line added to `control/status.md` ## Open PRs; claim file deleted in the
close-out commit; nothing chat-only remains.
