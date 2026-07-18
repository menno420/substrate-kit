# Session · 2026-07-18 · propagate-wall-guard

> **Status:** `complete`

Intent: close the last gap in the fleet's false-limitation enforcement — make the no-false-walls check (`tools/check_no_false_walls.py`, PR #448/#449) run inside `bootstrap.py check --strict` so EVERY adopter reds its own CI when a session documents a false agent-capability limitation into its own local docs, not only substrate-kit's own tree.

- **📊 Model:** Claude Opus · high · feature build
- ⚑ Self-initiated: no — owner-directed task (propagate the wall guard to all adopters). Reversible, test-covered, additive-only finding class.

## What shipped (PR follows)

Seam chosen: **`bootstrap.py check` leg** (least-invasive of the two options; no fallback to adopt-planting was needed).

- `src/engine/checks/check_no_false_walls.py` — NEW engine module. The #449 grammar (`_SUBJECT`/`_NEGATION`/`_CAP_VERB`/`_INFRA_OBJ`/`_OWNER_AUTHORITY`/`_CAP_NOUN` fragments, the full `_BLOCKLIST`, the dated/repudiated/historical/`FALSE "…"` CLEARING layer) is ported **verbatim** and is now the single home for the logic. Exposes `scan_text(text) -> [RawHit]` (the stateful per-line scanner, factored out of the old `check_file`), `iter_adopter_files(root, docs_root, …)` (the surfaces an adopter has: live `docs/**/*.md` minus historical/dated, root `CONSTITUTION.md`/`CAPABILITIES.md`, live `.claude/**/*.md`), and `check_no_false_walls(target, config) -> [Finding]` (engine `Finding`, kind `false-wall:<rule>`). Stdlib-only, no print/subprocess (passes the §3.2 engine lint bans).
- `src/engine/cli.py` — import + one line in `_extra_check_findings`: `findings += check_no_false_walls(target, config)`. That rides the full-lane `doc_findings`, so it is **exit-affecting under `--strict`** exactly like the ledger/namespace/seam legs. Additive: no existing check semantics, exit codes, or other findings changed; not run on the control fast lane (docs are not control-lane traffic).
- `src/build_bootstrap.py` — `checks/check_no_false_walls.py` added to `MODULE_ORDER` right after `check_docs.py` (its only engine reference is `check_docs.Finding`). `dist/bootstrap.py` regenerated (byte-pin green, idempotent, module baked in).
- `tools/check_no_false_walls.py` — rewritten as a **thin wrapper** that delegates to the engine core (no duplicate logic). Keeps `check_tree`/`main`/`Finding(path,line,phrase,rule)` for the kit's own CI + `tests/test_no_false_walls.py`; scans the kit-only surfaces (`src/engine/templates/*.tmpl` + `skills/skills.py`) *plus* the adopter surfaces via `iter_adopter_files`.
- `tests/test_check_no_false_walls_leg.py` — NEW, 16 tests: shared-core parity on the #449 must-fail/must-pass spread, the leg on each adopter surface (docs, CONSTITUTION, `.claude` skill body), exclusions (historical dir, dated filename, dated ledger bullet, `FALSE "…"` repudiation), self-gating (bare tree silent, honors a non-default `docs_root`, skips `.sessions`/`.substrate`), and the exit-affecting wiring through `cmd_check` (strict reds + names the leg in the HARD block; clean docs leave it silent). `tests/test_no_false_walls.py` unchanged and green.
- `CHANGELOG.md` — `[Unreleased] > Added` entry (MINOR — new checker propagated).

## Non-regression proof (the load-bearing guardrails)

- Full suite: **1759 passed, 1 skipped** (was 1743+; +16 new). Includes the cold-adoption smoke `test_prepare_walks_the_engagement_arc_to_green` (adopt → `check --strict` exit 0) — stays green.
- `ruff check src/engine/` — All checks passed (no print/assert/subprocess in the new module).
- `dist/bootstrap.py check --strict` on substrate-kit's own tree → **`all checks passed`**, zero `false-wall` findings.
- Real cold adopt (`adopt --include-claude --wire-enforcement` into a fresh git repo) → **zero `false-wall` findings**; then injecting `agents cannot merge …` into the adopter's `docs/current-state.md` → the leg reds it (`[false-wall:agent-negated-capability] docs/current-state.md`), `check` exit 1. The adopter's generated `substrate-gate.yml` runs the full-lane `check --strict --require-session-log --session-log "$card"` → so a freshly-adopted repo's CI now runs the check. Propagation proven end-to-end.
- Dist byte-equality pin green (fresh build == committed); build idempotent.

## 💡 Session idea

Add a `bootstrap.py check --explain-wall <phrase>` (or a `--why` on a false-wall finding) that prints, for a flagged line, WHICH blocklist rule matched and the one-line ground-truth correction ("merging is normal agent work — proven ~20× on 2026-07-18"), plus a pointer to the capabilities-ledger dated-row form for a genuine momentary refusal. The failure mode this guard exists to break is a session reading a wall and *not even trying*; a red check that also hands the agent the corrected phrasing turns the gate from "you're wrong" into "write this instead", closing the loop the same turn instead of leaving the next session to reverse-engineer why CI is red. Dedup: no `explain-wall`/`why-wall` idea in `docs/ideas/` (grepped); the existing false-wall work is all detection, none is remediation-guidance.

## ⟲ Previous-session review

PR #449 did the hard part exceptionally well: the grammar was already written *to be portable* — every fragment is a named constant, the surface list was a single `_iter_target_files`, and the clearing layer was a standalone function — so lifting it into the engine was a near-mechanical extraction rather than a rewrite, and the verbatim port kept all 17 original fixtures green with zero grammar edits. The one thing #449 left on the table (understandably — it was scoped to the kit's own guard) is exactly this session's whole point: it wired the check only into the kit's `tools/`-based CI step, where an adopter's own local false wall was invisible. Workflow improvement surfaced: a guard that protects *a doctrine template* should, at authoring time, carry an explicit note of WHICH consumers enforce it (kit-only vs every-adopter) — #449's tool docstring said "forward-binding surfaces" without distinguishing the kit's surfaces from an adopter's, so the propagation gap was only visible by reading `adopt.py` + `_iter_target_files` together. The new engine module's docstring now states the split explicitly (kit-only surfaces vs adopter surfaces), so the next reader sees the enforcement boundary without cross-referencing.
