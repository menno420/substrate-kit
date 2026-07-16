# Session · 2026-07-16 · archive-prep-s2

> **Status:** `complete`

Intent: baton item 1 — archive-ready close-out slice S2 (the `archive-prep` draft verb: evidence-draft half, sibling of ensure_draft; add_parser + dispatch in src/engine/cli.py; fail-open; tests for draft/re-run/never-touch-complete) per docs/planning/2026-07-15-archive-ready-close-out-plan.md §5 S2.

- **📊 Model:** Claude Fable · medium · feature build
- ⚑ Self-initiated: no — baton-named (control/status.md Next-2 item 1 at sync HEAD 4892436); coordinator-dispatched worker slice, no ORDER >024, `currency --check` exit 0, zero open PRs at orient.

## What shipped (PR #413)

- `src/engine/loop/archive.py` — the KL-5 evidence-draft seam (`ensure_draft`) pointed at the archive ritual: `ensure_archive_draft` drafts `docs/retro/archive-ready-<date>.md` from the embedded S1 template with tree-evidence pre-fills (claims-dir scan · heartbeat ⚑ line extraction, capped · CHANGELOG `[Unreleased]` park, fenced + capped), reports unresolved `[[fill:]]` slots on re-run, and never touches a completed note. REQUIRES-PROBE slots and the chat-only confirmation are never auto-filled, guarded on the doctrine tokens themselves (plan §4.2); fail-open returns the hand-copy fallback advisory instead of raising.
- `src/engine/cli.py` — `archive-prep` verb (`cmd_archive_prep`, parser entry, dispatch); separate verb, not a `session-close` flag (plan §4.1).
- `src/build_bootstrap.py` — MODULE_ORDER entry placed after `render.py` (the drafter consumes `load_templates`).
- `tests/test_archive.py` — 12 tests: draft-with-evidence, REQUIRES-PROBE/confirmation never prefilled, no-evidence soft path, re-run reports + touches nothing, complete-note never touched, prior-complete drafts today's, prior-unresolved blocks a new draft, fail-open advisory, template composition, CLI verb + no-state refusal, and the dist regression below.
- Doctrine doc ritual step 1 now names the verb; CHANGELOG `[Unreleased]` entry; dist regenerated.
- **Bug found + fixed en route (dist flat-namespace shadowing):** the single-file build concatenates every module into ONE namespace, so `check_template_sync._SLOT_RE` (a `${}` matcher, later in MODULE_ORDER) silently replaced archive's `[[fill:]]` slot regex at dist runtime — src tests were green while the shipped dist drafted a note with ZERO evidence substituted (caught by driving the built artifact in a scratch repo, not by the suite). Fixed by unique naming (`_ARCHIVE_SLOT_RE`, `_judgment_slot`) and pinned by `test_dist_flat_namespace_does_not_shadow_archive_symbols`, which builds the artifact and drives `init` + `archive-prep` end-to-end.
- Drift fixed on sight: the S1 card's `📊 Model:` task-class `docs build` was not a PL-004 class (standing `check --strict` advisory) — corrected to `docs-only` in this flip commit.
- Verified at 62fd620: `scripts/preflight.py` 9/9 green (pytest `1664 passed, 1 skipped in 34.50s`); `dist/bootstrap.py check --strict` shows only the designed born-red HOLD (this card, pre-flip), the known staged-regen-lag ×3, and the required-unverified NOTE; guard-fires telemetry delta committed with the heartbeat commit.

## 💡 Session idea

Build-time duplicate top-level symbol guard in `src/build_bootstrap.py`: the dist concatenates ~60 modules into one flat namespace, and NOTHING detects two modules defining the same top-level name — the later def silently wins for everyone, producing the exact src-green/dist-broken class this session hit live (`check_template_sync._SLOT_RE` shadowing `loop/archive.py`'s slot regex; a second live pair already exists — `handoff._fill` was identical to archive's by luck, renamed defensively). The guard is cheap: at build time, AST-walk each module's top-level `def`/assign names, fail the build on a cross-module duplicate not on an explicit allowlist (some same-name-same-body pairs may be deliberate). One realized failure + one near-miss in a single session says this class recurs as the engine grows. Dedup: zero hits for dist/build symbol shadowing in docs/ideas/ (grepped this session; `gate-tail1-multi-card-shadowing-2026-07-11.md` is card-selection shadowing, unrelated).

## ⟲ Previous-session review

The S1 session (#412) left S2 close to turnkey: the baton line named the module split, the seam (`ensure_draft`), and the fail-open contract; its card's "What shipped" bullets flagged the badge-token wall in advance and its 💡 idea (badges terminal, `[[fill:]]` slots as the draft-state signal) was exactly the convention S2's drafter and tests keyed on — zero re-derivation. Miss, small but instructive: S1's verification was template-only (docs slice), so nothing exercised the dist artifact end-to-end, and the flat-namespace shadowing class stayed invisible until this session drove the built file in a scratch repo. Workflow improvement: any slice that adds a MODULE to the dist should carry one built-artifact drive test as a standing pattern (this session's `test_dist_flat_namespace_does_not_shadow_archive_symbols` is the reusable shape) — and the durable fix is this session's 💡 build-time guard, which turns the whole class from runtime surprise into a red build.
