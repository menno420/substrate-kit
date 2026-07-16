# Session · 2026-07-16 · check-log-no-badge-parity

> **Status:** `complete`

Intent: graduate the **no-badge** Status-badge grammar finding into `check_log` (the modified-card / `--session-log` lane) for full parity with the added-card lane, and extract a shared `_status_grammar_findings(text)` helper both lanes call so the two card-check lanes cannot drift.

- **📊 Model:** Opus 4.8 · medium · feature build (check_log no-badge lane parity + shared `_status_grammar_findings` helper + landing)
- ⚑ Self-initiated: no — baton item 1 from the #428 `valueless-badge-check-log` card, coordinator-dispatched as the next buildable slice.

## What this session is about

`check_added_card` flagged a card carrying no Status badge line at all (`has_status_badge` → grammar finding), while `check_log`'s modified-card lane lacked that branch — the symmetric sibling of the valueless-badge gap PR #428 closed. A modified card stripped of its Status badge entirely, with all markers present, still passed `check_log` clean (and a valueless one was flagged only by a #428 branch that could drift from the added-card lane). This session extracts a single `_status_grammar_findings(text)` helper (no-badge → valueless, at most one finding) that both `check_added_card` and `check_log` call, adding no-badge parity to `check_log` AND deduping the valueless check so the two lanes cannot drift.

## 💡 Session idea

A **lane-parity meta-test** (or checker) that enumerates the dual-lane checks — every place the codebase runs one grammar/completeness rule from two entry points (added-card `check_added_card` vs modified-card `check_log` being the canonical pair) — and asserts each such pair routes through **one shared helper**, structurally. This session fixed the specific drift by extracting `_status_grammar_findings`; the meta-test would enforce the *pattern* for any future dual-lane check, so the next symmetric-gap class (a finding shipped to one lane and not its twin — exactly what #426→#428→#429 chased across three PRs) fails the suite instead of shipping and being caught a PR later. Dedup-checked docs/ideas/ — not captured (`gate-bites meta-tests` is per-checker known-bad fixtures, a different axis).

## ⟲ Previous-session review

PR #428 (`valueless-badge-check-log`) did the right diagnostic work and left a precise, buildable baton — its own 💡 named this exact no-badge parity gap and even proposed the shared-helper approach, which seeded this session cleanly. What it missed: it extracted only a shared *constant* (`VALUELESS_BADGE_MESSAGE`) and added the valueless branch inline in each lane, so the no-badge finding stayed added-card-only — a half-parity that cost a second PR (#429) to finish. **System improvement:** the shared-*helper* refactor `_status_grammar_findings` (this session's core) is what #428 should have done then — extracting the whole grammar routine, not just one message string, would have made adding no-badge parity a one-line change in both lanes at once and closed the class in a single PR. Generalized as this session's 💡 (the lane-parity meta-test).
