# 2026-07-12 — Model line: family-level naming mandate (close the exact-model-ID gap)

> **Status:** `complete` — PR #286 (`claude/model-line-family-level`).

- **📊 Model:** fable-5 · high · runtime bugfix

## Scope (what was about to happen)

Coordinator-directed bounded slice (fleet reporting bar: family-level model
names only in repo artifacts, never exact model-ID tokens; context: a
websites-repo cleanup PR, websites #178 @ 6664b5f, corrected a card that
followed the narrower old wording). The kit's planted `.sessions/README.md`
model doctrine (`src/engine/adopt.py` `_model_doctrine_text`) banned only a
"full dated model ID" — but exact model IDs are not always dated (e.g. a
`claude-`-prefixed exact ID token with no date suffix), so cards following
the letter of the doctrine still recorded exact IDs.

Lane claim: `control/claims/claude-model-line-family-level.md` (deleted by
this flip commit).

## Close-out

Shipped (PR #286, work commit 1b276e3):

- **Doctrine reworded** (`src/engine/adopt.py` `_model_doctrine_text`, the
  ONE home both the fresh `.sessions/README.md` plant and the retroactive
  `_merge_model_doctrine` append render from): the ban is now "never record
  an exact model ID — family-level names only, never an exact model-ID
  token (dated or not)", superseding the dated-only wording. The
  idempotency detection phrase (`_MODEL_DOCTRINE_PHRASE`) is deliberately
  untouched, so READMEs already carrying the ORDER 012 paragraph are never
  re-appended; those adopters pick the reworded text up at the next release
  + `upgrade --apply-docs`. **No adopter repo is retro-edited by this PR.**
- **Kit's own `.sessions/README.md`** carries the identical reworded
  sentence (same-file sibling of the planted copy).
- **Telemetry advisory aligned** (`src/engine/loop/telemetry.py`): the one
  code path that scans card `📊 Model:` lines — `harvest_model_usage`
  (KL-3 session-close harvest) — now flags a model segment matching
  `_EXACT_MODEL_ID_RE` (provider-prefixed `claude-…` / `us.anthropic.…`
  or `-YYYYMMDD`-dated shapes) with a never-exit-affecting advisory, the
  same contract as the task-class advisory beside it; the row still records
  verbatim. No checker previously enforced ANY model-segment format —
  nothing had to be loosened, only this advisory added.
- **Tests** 1184 → 1187: widened doctrine assertions in
  `test_sessions_readme_teaches_family_level_model_attribution` (incl. a
  regression pin that "full dated model ID" is gone) + three new harvest
  tests (exact-ID token advisory fires & still records; dated-suffix shape
  caught; the doctrine's own family-level examples `fable-5` / `opus-4.8` /
  `sonnet-5` never false-fire).
- **CHANGELOG** `[Unreleased]` → `### Fixed` entry; **dist rebuilt**
  (`python3 src/build_bootstrap.py`, 818119 B, byte-pin clean).

**Verification (pre-flip):** `python3 -m pytest tests/ -q` → **1187
passed**; `python3 -m ruff check src/engine/` → all checks passed;
`python3 dist/bootstrap.py check --strict` → red ONLY with the designed
born-red hold naming this card (which this flip clears); dist byte-pin
clean after rebuild.

**Friction (self-inflicted, caught by the suite):** the CHANGELOG edit
initially swallowed the `## [1.14.0]` heading line (an Edit anchored on the
text right above it) — `test_release_assets` caught it immediately
("CHANGELOG.md has no '## [1.14.0]' section"), heading restored. Evidence
the enforce-don't-exhort release guard works exactly as designed; no new
guard needed.

## 💡 Session idea

The `_EXACT_MODEL_ID_RE` advisory currently lives only in the session-close
harvest path. A sibling advisory in `reconcile_model_usage` is deliberately
NOT added (it would re-flag every historical card on every sweep — noise,
not signal). Idea worth having instead: a one-shot `bootstrap.py`
maintenance surface (or a lab-loop slice) that reports — never edits — the
count of historical cards whose model segment matches the exact-ID shapes,
per repo, so the owner can decide once whether a websites-#178-style
cleanup wave is worth it fleet-wide, with data instead of grep archaeology.

## ⟲ Previous-session review

The grounded-skills slice-8 session (PR #282) closed the 8-slice program
cleanly with the propose-don't-apply boundary test-pinned — strong finish,
and its status.md close-out made this session's orientation fast. What it
(and the whole ORDER 012 chain) missed is exactly what this slice fixed:
the doctrine it shipped said "never a full **dated** model ID" while the
current model generation's exact IDs carry no date, so the ban was
letter-followable and wrong — a reminder that wording lifted from one
provider era silently rots; prefer banning the CLASS ("exact model-ID
token") over its current SHAPE ("dated ID"). Workflow improvement: when a
doctrine sentence encodes an empirical shape, pin the shape in a test AND
state the class in the prose (this slice does both).
