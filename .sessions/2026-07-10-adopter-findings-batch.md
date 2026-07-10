# 2026-07-10 — gen-2: adopter findings batch (owner-action tokens + fast-CI arm-race + parallel-worker worktree)

> **Status:** `in-progress`

- **📊 Model:** claude-opus-4-8 · high · gen-2 kit-lab deliberate adopter-findings session

## Scope

Goal: gen-2: adopter findings — owner-action token align + fast-CI arm-race doc +
parallel-worker worktree recipe. Three small kit-side items from the venture-lab
adopter (fresh kit v1.6.0 adopter), bundled into ONE PR.

1. **ITEM 1 — owner-action-fields checker token agreement (code + test).**
   The checker (`src/engine/checks/check_owner_actions.py`) and every template
   (`control-README.md.tmpl`, `CONSTITUTION.md.tmpl`, `collaboration-model.md.tmpl`)
   plus canonical `control/README.md` already use the SAME canonical labels —
   `WHY-IT-MATTERS` / `VERIFIED-NEEDED`. The reported `WHY` / `VERIFIED-WHEN`
   spelling exists nowhere in the kit; it is the adopter's inline shorthand.
   Canonical stays `WHY-IT-MATTERS` / `VERIFIED-NEEDED`; the checker now ALSO
   accepts the `WHY:` / `VERIFIED-WHEN:` shorthand (backward-compatible — an
   accepted alternate only ever *withholds* the advisory nag, never adds one,
   so no valid ledger is newly reddened). Tests pin agreement: shorthand block
   is clean, and the checker's canonical labels are asserted present in the
   shipped template.

2. **ITEM 2 — fast-CI auto-merge arm race (docs).** On a repo with sub-~10 s CI,
   a direct `enable_pr_auto_merge` races: the PR flips `pending`→`clean` before
   the arm lands and GitHub returns "already in clean status … merge directly".
   Fast-CI fallback note added to `docs/operations/auto-merge-guards.md` §
   Operational notes and to `docs/CAPABILITIES.md` append-log: fall back to REST
   merge-on-green, or add a small delay / slower second gate job. Not a concern
   for the kit's own event-driven `auto-merge-enabler.yml`.

3. **ITEM 3 — parallel file-mutating subagents race in a shared clone (docs).**
   Two file-mutating workers in the same checkout raced; one worker's
   `git add -A` swept the other's uncommitted files into the wrong PR. The
   worktree-per-worker convention already lives in the gen-2 succession pack;
   the realized failure-mode recipe (isolated worktrees OR serialize; only
   read-only parallel workers are safe in a shared clone; never `git add -A`
   from a shared-checkout writer) is now pinned on the adopter-facing
   `docs/CAPABILITIES.md`.

`src/` touched → `dist/bootstrap.py` regenerated. No `control/inbox.md`,
`control/status.md`, or `bench/` touched. PRs #26/#49 untouched; B1 run-3 not run.

## Verification

- `python3 dist/bootstrap.py check --strict` → green.
- Full suite → 781 passed; ruff clean.

Card flips to `complete` in the last commit.
