# 2026-07-10 — visiting adopter lane: gate-template sentinel fixes (gba-homebrew Track B)

> **Status:** `complete`

- **📊 Model:** Claude (ID withheld) · high · single scoped PR: port two
  adopter-found `live_ci_workflow()` fixes upstream (visiting lane; claim
  landed first via #105 on `control/status-gba-homebrew-trackb.md`)

## Scope

Session goal: upstream two defects in the planted `substrate-gate.yml`
template (`live_ci_workflow()`, `src/engine/adopt.py`), found, fixed and
validated live on the adopter menno420/gba-homebrew (public; validated across
its PRs #3–#14 — every heartbeat, feature and close-out PR there ran the fixed
gate green, and close-out cards still hit the locked door when incomplete):

1. **No-card sentinel** (gba-homebrew PR #3): with no session card in the PR
   diff the template ran `check --strict --require-session-log` bare, believed
   fail-open — but on a fresh CI checkout every mtime flattens, the engine's
   newest-by-mtime fallback latches onto the mid-session in-progress card, and
   EVERY unrelated PR reds. Fix: pass an explicitly named nonexistent sentinel
   (`--session-log <sessions_dir>/__no-card-in-diff__.md`) WITHOUT
   `--require-session-log` — advisory per the engine contract ("a named file
   that does not exist is treated exactly like an absent log").
2. **Added-card advisory** (gba-homebrew PR #2, merged red): a heartbeat PR
   that ADDS the born-red card (first-commit conventions require an
   in-progress card at birth) can never satisfy the locked door, because under
   `--strict` the engine reds ANY existing-but-incomplete card. Fix: a card
   ADDED by the PR (`--diff-filter=A`) gates advisory via the absent sentinel;
   a card MODIFIED by the PR (close-out flips) keeps the full
   `--require-session-log` locked door.

Touches: `src/engine/adopt.py` (template + docstring), `tests/test_adopt.py`
(updated diff-selection test + new added-vs-modified test), `CHANGELOG.md`
`[Unreleased]` Fixed entry, `dist/bootstrap.py` regen (byte-pin), this card,
and the visiting-lane heartbeat close on `control/status-gba-homebrew-trackb.md`.
No pin paths, no `control/status.md`/`inbox.md`/`substrate.config.json` writes
(one writer per file).

## 💡 Session idea

The kit's own `ci.yml` solves the flattened-mtime problem a third way (restore
card mtimes from commit times); adopters get the diff-derived card. A tiny
`check --session-log-from-diff BASE..HEAD` engine mode (or documented recipe)
would collapse the three bash reimplementations (kit ci.yml, planted template,
adopter forks) into one tested code path — the template's bash card-selection
block is now 20+ lines that every adopter carries verbatim.

## ⟲ Previous-session review

Previous card (`2026-07-10-adopt-lane.md`, queue item 11 / #103) closed
`complete` with `adopt --lane` shipped and the suite green — no defect
inherited; this visit builds on its multi-lane pattern (the visiting-lane
heartbeat file this claim rode in on is exactly that pattern's suffixed-file
convention, precedent #52/#73).
