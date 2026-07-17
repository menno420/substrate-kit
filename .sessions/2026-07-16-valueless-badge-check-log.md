# Session · 2026-07-16 · valueless-badge-check-log

> **Status:** `complete`

Intent: graduate the valueless Status-badge grammar finding — shipped in PR #426 for the gate's ADDED-card lane (`check_added_card`) — into the MODIFIED-card lane (`check_log`) in `src/engine/checks/check_session_log.py`, closing the symmetric false-green where a modified card whose Status badge declares no value passes clean.

- **📊 Model:** opus-4.8 · medium · feature build (gate-integrity: kit-quality gate source, check_log lane)
- ⚑ Self-initiated: no — the filed 💡 from the #426 `valueless-badge-coverage-pin` card, coordinator-dispatched as the next buildable slice.

## What this session is about

`check_log` (the modified-card / `--session-log` lane) had the same blind spot PR #426 closed on the added-card lane only: a valueless badge makes `status_in_progress` return False (no value → not in-progress), so a card carrying every marker needle with a `> **Status:**` line that declared nothing passed `check_log` completely clean. This session shipped the `check_log` valueless branch: it extracts the finding message to a module constant reused by `check_added_card`, and adds a `not _status_badge_value(text)` branch to `check_log` so a valueless modified card is flagged with the same "Status badge VALUE" grammar finding the added-card lane already blocks. Landed with 2 mirror tests + dist regen; suite 1716→1718; `check --strict` exit 0.

## 💡 Session idea

Graduate the **no-badge** grammar finding into `check_log` for full lane parity. `check_added_card` flags a card carrying no Status badge at all (`has_status_badge` → grammar finding); `check_log`'s modified-card lane still lacks that branch — the symmetric sibling of the valueless-badge gap this session closed. A card stripped of its Status badge entirely, with all markers present, still passes `check_log` clean. Next slice: mirror `has_status_badge` into `check_log`, and extract a shared `_status_grammar_findings(text)` helper both lanes call so a card-grammar finding can never live in one lane and not the other.

## ⟲ Previous-session review

PR #426 (valueless-badge-coverage-pin) chained cleanly — it shipped the added-card valueless finding and left a precise, buildable next-idea that seeded this session directly, plus a residue-coverage regression pin. What the lane's history missed: the valueless finding landed in only one of the two symmetric card-check lanes (`check_added_card`), leaving `check_log` silently exposed — a recurring gate-drift class. **System improvement:** author card-grammar findings once in a shared helper both lanes call, so a finding can never exist in one lane and not the other (captured as this session's 💡 idea toward the no-badge sibling).
