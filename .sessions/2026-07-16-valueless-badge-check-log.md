# Session · 2026-07-16 · valueless-badge-check-log

> **Status:** `in-progress`

Intent: graduate the valueless Status-badge grammar finding — shipped in PR #426 for the gate's ADDED-card lane (`check_added_card`) — into the MODIFIED-card lane (`check_log`) in `src/engine/checks/check_session_log.py`, closing the symmetric false-green where a modified card whose Status badge declares no value passes clean.

- **📊 Model:** (to fill at flip) · medium · gate-integrity build
- ⚑ Self-initiated: no — the filed 💡 from the #426 `valueless-badge-coverage-pin` card, coordinator-dispatched as the next buildable slice.

## What this session is about

`check_log` (the modified-card / `--session-log` lane) has the same blind spot PR #426 closed on the added-card lane only: a valueless badge makes `status_in_progress` return False (no value → not in-progress), so a card carrying every marker needle with a `> **Status:**` line that declares nothing passes `check_log` completely clean. This session extracts the finding message to a module constant (`VALUELESS_BADGE_MESSAGE`), reuses it in `check_added_card`, and adds a `not _status_badge_value(text)` branch to `check_log` so a valueless modified card is flagged with the same "Status badge VALUE" grammar finding the added-card lane already blocks. Mirror tests + dist regen.

## 💡 Session idea

(brief real content — to be finalised at flip)

## ⟲ Previous-session review

(brief real content — to be finalised at flip)
