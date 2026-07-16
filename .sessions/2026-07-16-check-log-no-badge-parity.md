# Session · 2026-07-16 · check-log-no-badge-parity

> **Status:** `in-progress`

Intent: graduate the **no-badge** Status-badge grammar finding into `check_log` (the modified-card / `--session-log` lane) for full parity with the added-card lane, and extract a shared `_status_grammar_findings(text)` helper both lanes call so the two card-check lanes cannot drift.

- **📊 Model:** [[fill: family-level model · effort · PL-004 task-class]]
- ⚑ Self-initiated: no — baton item 1 from the #428 `valueless-badge-check-log` card, coordinator-dispatched as the next buildable slice.

about to: graduate no-badge grammar finding into check_log's modified-card lane + extract shared _status_grammar_findings() helper for lane parity.

## What this session is about

`check_added_card` flagged a card carrying no Status badge line at all (`has_status_badge` → grammar finding), while `check_log`'s modified-card lane lacked that branch — the symmetric sibling of the valueless-badge gap PR #428 closed. A modified card stripped of its Status badge entirely, with all markers present, still passed `check_log` clean (and a valueless one was flagged only by a #428 branch that could drift from the added-card lane). This session extracts a single `_status_grammar_findings(text)` helper (no-badge → valueless, at most one finding) that both `check_added_card` and `check_log` call, adding no-badge parity to `check_log` AND deduping the valueless check so the two lanes cannot drift.

## 💡 Session idea

[[fill: one genuine idea]]

## ⟲ Previous-session review

[[fill: one genuine remark on the previous session + one system improvement]]
