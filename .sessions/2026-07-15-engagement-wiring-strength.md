# Session · 2026-07-15 · engagement-wiring-strength

> **Status:** `complete`

Intent: ship the engagement wiring-STRENGTH advisory (baton item 1, idea engagement-wiring-strength-verification-2026-07-12) — an advisory-only `enforcement-weak-form` finding when the wired `check --strict` door is the plain form while the staged substrate-gate carries the stronger legs (`--require-session-log`, diff-aware `--session-log`, `--inbox-base`), plus the `enforcement-required-unverified` honesty NOTE; sibling of the merged #401 native-gate class.

- **📊 Model:** fable-5 · medium · feature build

## What shipped (PR #402)

- Layer 1 — `check_enforcement_strength` (`src/engine/checks/check_engagement.py`): advisory-only `enforcement-weak-form` finding on `check`'s full lane when the wired plain-form door skips staged-gate legs the staged `<state_dir>/ci/substrate-gate.yml` demonstrably carries. Missing legs named with what each costs (session-log locked door / diff-aware card selection / inbox append-only gate); staged file named as the one-copy fix. Never strict-red — the idea's letter ("a hand-rolled gate is legitimate"); the kit's own ci.yml carries all three legs and self-silences, verified live. Token-boundary matching (`--require-session-log` never satisfies the `--session-log` leg) on comment-stripped text only; input-gated on adoption evidence + a wired door; silent without a staged reference (nothing to copy).
- Layer 2 — `required_unverified_note`: the `enforcement-required-unverified` honesty NOTE beside the `enforcement-native` NOTE — whether the CI door is a REQUIRED status check is owner-UI state the stdlib engine cannot read (#36 r3; proven: superbot-next #51/#68 merged with red non-required legs); the note names the expected context (`native_gate.required_context` on the native path, else `automerge.required_context`). NOTE-only: honesty on a green path, never telemetry, never exit-affecting.
- 5 new tests (27 total in the file); idea flipped shipped (window closes 2026-08-14) + index entry moved to Shipped; CHANGELOG under `[Unreleased]` `### Added`; dist byte-pin regenerated.
- Verify at ed04666: `scripts/preflight.py` 8/8 green (pytest 1629 passed, 1 skipped); live `check --strict` on the kit tree shows the required-unverified NOTE firing, no weak-form advisory (strong-form self-silence), and only the designed born-red HOLD red.
- Rider (the #400 card's own rule of thumb applied): fixed the #400 card's `📊 Model:` payload to the taught three-field form in this flip commit — one-token copy-edit that self-silences the model-line advisory the last two wakes carried as "next tidy pass".

## 💡 Session idea

NOTE-emission telemetry: `check`'s NOTE lines (`enforcement-native`, `enforcement-required-unverified`, inbox self-skip, preflight self-skip, mtime-fallback) are honesty output that never reaches `guard-fires.jsonl` — advisories are telemetry-recorded, NOTEs vanish with the terminal scroll. As NOTEs accumulate (this session added one that fires on every full check of every wired adopter, forever), nothing measures fleet-wide NOTE volume or spots a NOTE that has gone stale/noisy. Record NOTE emissions in the guard-fires ledger with `posture: "note"` so B4-style sweeps can rank NOTE noise and retire or gate the chronic ones — the same enforce-don't-exhort instinct, applied to the kit's own honesty channel. Dedup: no existing idea file covers NOTE telemetry (grepped docs/ideas/ for NOTE/telemetry pairings).

## ⟲ Previous-session review

The #401 session (native_gate evidence class) did clean, well-fenced work: the declared-evidence design (malformed shapes never widen the gate, dead declarations stay red with the path named, acceptance always visible) is exactly the right doctrine shape, and its fixtures pinned all three arms. Miss: it spotted the #400 card's broken `📊 Model:` payload and parked it as "noted for the next tidy pass, not this PR's scope" — a one-token copy-edit whose rule of thumb ("fix the trivial subset in the same PR, baton only the judgment-heavy remainder") was written on the very card carrying the defect. This session applied the rule instead: the mechanical fix rode this PR. System improvement worth keeping: when a new advisory fires on an already-merged artifact and the fix is a one-line mechanical edit, the fix belongs to the CURRENT PR, never the baton — a batoned one-liner costs every subsequent wake an advisory line and a "known, ignore it" context load.
