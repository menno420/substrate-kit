# 2026-07-11 — upgrade carve-out scanner: three-way compare

> **Status:** `complete`

- **📊 Model:** fable-5 · high · fix

## Scope (what is about to happen)

Fix the v1.11.0-wave carve-out false positive (evidenced on the wave cards
of fleet-manager #72 · superbot-games #45 · trading-strategy #60 ·
gba-homebrew #44 · venture-lab #37): when a kit release changes the kit's
OWN generated gate content (the #199/#195 checkout@v5 / setup-python@v6
pin bumps), the kit-owned workflow regen compares the adopter's LIVE gate
against the NEW template only, misreads the kit's own outgoing template
content as "host-added" steps (phantom carve-outs), and banks a pre-regen
copy that is byte-identical to the OLD template (unnecessary bank).

The fix is a THREE-WAY compare in `_regen_kit_owned_workflow`
(`src/engine/adopt.py`): live vs OLD template (recovered from the staged
copy at `<state_dir>/ci/` captured BEFORE the staging pass overwrites it)
vs NEW template. A diff is a host carve-out ONLY when present in live and
explained by NEITHER template; kit-side evolution is a one-line
informational note; a live gate byte-identical to the old template
produces zero flags and NO bank. Old template unrecoverable → degrade to
today's two-way compare with an explicit warning, never a crash.
Regression tests: pin-bump-only (no flags, no bank) · genuine host
addition (still detected + banked) · mixed (only the host step flagged).
CHANGELOG under [Unreleased]; dist rebuilt (byte-pin); NO release cut, NO
version bump. Claimed via `control/claims/carveout-three-way-compare.md`
(PR #208). NEVER touching `bench/` or its trend/result homes (parallel
run-7 lane) and never `control/inbox.md`.

## Close-out

Shipped the declared scope exactly. `_regen_kit_owned_workflow`
(`src/engine/adopt.py`) now takes `old_text` — the previous kit template,
captured by `adopt()` from the staged copies under `<state_dir>/ci/`
via the new `_staged_previous_text` helper BEFORE the staging pass
overwrites them — and runs the three-way compare: a detection survives as
a host carve-out only when it fires against BOTH templates (present in
live, explained by neither); kit-side evolution is a one-line
`kit-updated N step(s)/job(s)` informational note; live byte-identical to
the old template short-circuits to a clean scan + regen with NO bank; no
recoverable old template degrades to the two-way compare with an explicit
warning (and the existing dirty-regen test now pins that warning). The
banked dist was ruled out as a recovery source without execution: the gate
and enabler are code-generated (`live_ci_workflow` /
`automerge_enabler_workflow`), not `_TEMPLATES` entries, so
`load_old_templates`-style `ast.literal_eval` cannot re-render them.
Regression tests:
`test_pin_bump_only_regen_yields_no_phantom_carveouts_and_no_bank`,
`test_genuine_host_carveout_still_detected_with_old_template`,
`test_mixed_kit_change_and_host_addition_flags_only_the_host_step`
(tests/test_adopt.py) +
`test_upgrade_pin_bump_only_gate_reports_no_phantom_carveouts`
(tests/test_upgrade.py, end-to-end report shape). CHANGELOG under
`[Unreleased]` (next release payload — no cut, no bump); dist rebuilt
(678781 B, byte-pin). Verified on this branch: `python3 -m pytest tests/
-q` → **1012 passed** (was 1008); `python3 -m ruff check src/engine/`
clean; `check_idea_index` / `check_program_law` / `check_bench_integrity`
all OK; pre-flip `check --strict` sole finding was this card's own
designed born-red hold (CI run 29155193802 confirmed: kit-quality red =
the hold notice only; the two fast-fail jobs are its legacy-alias
mirrors). NEGATIVE finding, recorded honestly: the "filed idea" for this
fix cited at dispatch does NOT exist in this repo — `grep -rniE
"three-way|phantom|carve" docs/ideas/` has no hit; the evidence lives
only on the adopter wave cards. Design followed the wave evidence + the
dispatch spec directly.

## 💡 Session idea

The three-way compare's old-template recovery leans entirely on the
staged copy under `<state_dir>/ci/` surviving between upgrades — a host
that deletes or hand-edits its staged tree silently knocks the scanner
back to two-way mode (it warns, but the precision is gone). The kit
already solves exactly this provenance problem for planted docs with
`planted_doc_hashes` in state.json. Record the same for kit-owned live
workflows: at every regen, store the shipped render's sha256 (e.g.
`kit_owned_workflow_hashes`). Then "live == what the kit last shipped" is
answerable from state.json alone — no staged bytes needed — and the
two-way fallback shrinks to genuinely-first adopts. Cheap (one dict, one
hash per regen), and it makes the phantom-carve-out class structurally
unreachable rather than staged-copy-dependent. Dedup: grep of docs/ideas/
finds no existing entry; distinct from `planted_doc_hashes` (docs) and
from the archive bank (full bytes, rollback-oriented).

## ⟲ Previous-session review

The predecessor in this lane, #207 (v1.11.0 wave close-out regen), was a
model close-out: it live-verified the v1.11.0 currency-parser fix against
the exact adopter row that motivated it and recorded the expected drift
classes without chasing them. What it — and the whole wave lane — missed
is the capture discipline this session tripped over: six adopter wave
cards documented the SAME phantom-carve-out false positive, yet nobody
filed it into this repo's `docs/ideas/` (my preflight grep found no
trace), so the fix had to arrive as coordinator dispatch instead of
through the kit's own idea pipeline. Concrete improvement: the wave-regen
recipe should end with "route any kit-side finding observed on adopter
cards into docs/ideas/ same session" — the finding was known fleet-wide
for hours while remaining invisible to this repo's backlog.
