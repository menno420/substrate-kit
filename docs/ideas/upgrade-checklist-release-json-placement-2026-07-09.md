---
state: promoted
origin: lab
shipped_pr: 92
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-10
outcome: shipped
---

# Upgrade checklist should say: put `release.json` next to `bootstrap.py.new` — or sha verification silently skips (2026-07-09)

> **Status:** `ideas`
>
> **State:** captured (v1.6.0 fleet rollout — field finding from the two
> consumer upgrade runs, superbot-next#96 + websites#45).

## The finding

The in-flow sha256/version self-verification is **opportunistic**: `upgrade`
verifies against `--release-json <path>` when supplied, else against a
`release.json` sitting in the SAME directory as the running
`bootstrap.py.new` (`candidate = release_json or running.parent /
"release.json"`, src/engine/upgrade.py:320) — and when neither exists it
**silently skips** verification (no report line, no warning). The adopter
upgrade checklist (`ADOPTER_CHECKLIST`, src/build_release_json.py — appended
to every release's notes) says only "download `bootstrap.py` from this
release next to your vendored copy as `bootstrap.py.new`"; it never mentions
`release.json`. An operator following the checklist to the letter gets an
unverified upgrade and no signal that the tamper/corruption check never ran.

## The fix to build

One checklist line closes it: step 1 gains "also download `release.json`
from the release next to `bootstrap.py.new` — the upgrade verifies the
file's sha256 against it (and self-cleans both afterwards); without it the
verification silently skips." Optionally (nice-to-have, second line of
defense): when verification skips, the upgrade report should say so —
`note: no release.json found — sha256 self-verification skipped` — so the
silent path stops being silent.

**Guard recipe:** `ADOPTER_CHECKLIST` in `src/build_release_json.py`; the
`candidate` lookup + `verify_against_release_json` call in
`src/engine/upgrade.py` (~line 320); test targets — the release-notes test
asserting the checklist names `release.json`, and a `test_upgrade.py` case
asserting the skip path emits its note.

## Done-when

The published checklist tells adopters to place `release.json` beside
`bootstrap.py.new`, and (if the second line ships) an upgrade that ran
unverified says so in its report.
