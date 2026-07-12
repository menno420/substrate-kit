# 2026-07-12 — grounded-skills program, slice 6: single-source seat-digest render (kit side)

> **Status:** `complete`

- **📊 Model:** fable-5 · seat-worker · grounded-skills slice 6

## Scope (what is about to happen)

Implementing the KIT SIDE of §7 slice 6 of the grounded-skills program plan
(`docs/planning/2026-07-12-grounded-skills-program.md`, merged PR #263):
canonical machine-extractable seat-digest blocks — a skills-index digest and
a venue-filtered WALLS digest (Project-seat default `autonomous-project` +
`any`) — each wrapped in NEW prefix-matched fence constants in
`src/engine/grammar.py` (the capability-seed pattern), rendered into ONE
kit-generated planted doc (`docs/seat-digest.md`, digest + pointer, never
inline, per-block budget enforced), regenerable via a `bootstrap.py
seat-digest` CLI surface + refreshed at upgrade, with an advisory PL-008
drift-guard checker proving the planted file equals a fresh render
byte-for-byte. Extraction contract + no-third-copy deferral chain documented
in the generated doc itself. Tests + CHANGELOG `[Unreleased]` + dist
rebuild. **Fleet-manager-side wiring is explicitly OUT of scope** — fm moved
to prompt system v3.3 (fence-extraction/byte-match consumption; the plan's
`{{ORIENTATION_PATH}}`/`{{WALLS}}` slots are retired), so the fm regen-tool
integration ships as a separate coordinated PR.

**Provenance flag:** Coordinator proceeded on plan §8 default **Q3=A** (kit
ships canonical blocks; fleet-manager's regen tool renders seat prompts from
them) — the LEAST-confirmed default in the program; this slice's design is
therefore kept strictly additive and cleanly reversible (new module, new
planted doc, advisory-only checker; nothing existing changes behavior).

Lane claim: `control/claims/claude-slice-6-fleet-manager-render.md`
(deleted at close, last commit).

## Close-out

Shipped (PR #279; work commit rebased onto the wave-B close-out #280):

- **Grammar — the machine extraction contract** (`src/engine/grammar.py`,
  new seat-digest section): `SKILLS_DIGEST_BEGIN_PREFIX/END_PREFIX`
  (`<!-- substrate-kit:skills-digest BEGIN` / `… END`) and
  `WALLS_DIGEST_BEGIN_PREFIX/END_PREFIX`
  (`<!-- substrate-kit:walls-digest BEGIN` / `… END`) — prefix-matched
  like the capability-seed pair so marker-wording tweaks can never orphan
  a fence; together with `CAPABILITY_SEED_BEGIN_PREFIX/END_PREFIX` these
  three pairs ARE the contract fleet-manager's v3.3 regen consumes
  (fence-prefix match + byte compare over committed files, never kit-code
  execution). Plus `WALLS_DIGEST_VENUES_RE` (the `venues=` marker token),
  `walls_digest_begin_marker(venues)`, `SEAT_DIGEST_DEFAULT_VENUES =
  (autonomous-project, any)` (Project-seat filter, drawn from the slice-5
  venue vocabulary — test-pinned), and `SEAT_DIGEST_BLOCK_BUDGET = 1500`.
- **Render surface** (`src/engine/seatdigest.py`, new module, in
  MODULE_ORDER before adopt.py): `skills_digest_block()` (one row per
  SKILLS entry — render-from-ONE-source), `walls_digest_block(ledger_text,
  venues, docs_root)` (seed-fence Walls rows + `wall`-tagged append-log
  entries, venue-filtered mechanically; legacy five-field lines read as
  venue `any`, the pinned compat contract; `LAST-VERIFIED` stamps
  stripped), `seat_digest_document()` / `seat_digest_text(root, config,
  context, venues)` — THE one render path adopt/upgrade/CLI/checker
  share, deterministic (no dates, no env reads). Blocks budget-truncate
  into a `+N more — read the source` pointer row (`_fit_rows`), never
  silently overflow. Live sizes at plant: skills 1424 B, walls 1045 B.
- **The planted doc** `docs/seat-digest.md` (docs_root-remapped): header
  (derived-render covenant, `reference` badge), both fenced blocks, the
  extraction-contract table (all three prefix pairs), and the
  no-third-copy section (§4.2e) stating the exact deferral chain:
  **the adopter's `docs/CAPABILITIES.md` ledger is the seat-local source
  of truth; the kit-rendered digest is a DERIVED RENDER (regenerated —
  adopt/upgrade/CLI — never edited, never a copy of record);
  fleet-manager's `docs/capabilities.md` master is the fleet aggregation
  point; no third authored copy is ever minted** (the venture-lab
  case-duplicate class fm tracks as I-44).
- **Distribution**: adopt plants it AFTER the ADOPT_PLAN loop (reads the
  just-planted ledger; `record_doc_hash`); upgrade `refresh_seat_digest`
  (new, wired as step 6c after the adopt pass + mirrored in
  `run_apply_docs_posthoc`) regenerates kit-written copies with the
  committed doc's own `venues=` filter preserved, downgrades hand-edited
  copies to a report line naming the regen command (never clobbers), and
  re-records the hash; upgrade report gains a "Seat-digest refresh"
  section. CLI: `bootstrap.py seat-digest` (`--venue` repeatable
  override; committed filter preserved otherwise; hash re-recorded only
  when an install exists).
- **Drift guard** (`src/engine/checks/check_seat_digest.py`, advisory-only
  §8 Q2=B, PL-008 unverified/kill-switch header): `seat-digest-stale`
  (committed bytes ≠ fresh render with the committed venue filter — the
  `--check-registry`-style proof that prompt blocks equal kit truth;
  message names the regen command) + `seat-digest-over-budget` (a
  hand-grown block past 1,500 — the one class that breaks the downstream
  8,000-char paste budget). Wired into `cmd_check` (full lane, emitted +
  guard-fire-recorded, never exit-affecting).
- **`SKILLS-index.md.tmpl`**: new "Machine consumption — the seat digest"
  section (reachability link + the never-edit/regenerate teaching).
- **Tests:** suite **1147 → 1174** (+27, `tests/test_seatdigest.py`:
  fence-prefix identities + roundtrip + distinct namespaces, default-venue
  vocabulary pin, venue parse fail-open, skills digest
  completeness/budget/determinism, walls venue filtering (in/out/legacy/
  capability-excluded) + parameterization + stamp stripping + budget
  truncation + missing/empty-ledger honesty, document fence order +
  contracts + no-placeholders, adopt plant/hash/keep, refresh
  regen/noop/never-clobber/venue-preserve/skip-missing, report section,
  CLI regen/override/preserve via `main()`, checker
  green/stale→fix→green loop/venue-aware/over-budget/absent).
- **CHANGELOG:** `[Unreleased]` slice-6 entry.
- **Dist:** rebuilt (`python3 src/build_bootstrap.py`) — 813101 B,
  byte-pin clean after the rebase; `_APPEND_LOG_HEADING` renamed
  `_LEDGER_APPEND_LOG_HEADING` in seatdigest.py (the dist
  constant-collision guard caught the clash with upgrade.py).

Verify (verbatim tails): `python3 -m pytest tests/ -q` → `1174 passed` ·
`python3 -m ruff check src/engine/` → `All checks passed!` ·
`git diff --exit-code dist/bootstrap.py` clean · `scripts/check_idea_index.py`
/ `check_program_law.py` / `check_bench_integrity.py` → OK ·
`python3 dist/bootstrap.py check --strict` → the designed born-red hold
naming this card, zero seat-digest advisories. Live e2e through the dist in
scratch: init → adopt (`planted: docs/seat-digest.md`) → block sizes
1424/1045 ≤ 1500 → `seat-digest` CLI regen clean.

Accept criteria (§7.6, kit side): `--check-registry`-style drift guard
proves prompt blocks equal kit truth ✔ (`seat-digest-stale` byte-compare
against the shared render path; test-pinned green/red/fix loop);
8,000-char budgets still fit ✔ (1,500/block budget enforced by truncation
+ over-budget advisory; digest + pointer, never inline). Fleet-manager
side (regen wiring, UNIVERSAL fetch-list vN bump + owner re-paste) =
separate coordinated PR by design (fm v3.3 staleness — see scope note).

**Decide-and-flag calls (plan silent on the detail):**

1. ⚑ Targeted fm's **v3.3 consumption model** (fence extraction +
   byte-match), NOT the plan's retired `{{ORIENTATION_PATH}}`/`{{WALLS}}`
   slots — fm@791772f retired the core+seat-block assembly; implementing
   the plan's letter would have shipped dead integration points.
2. ⚑ ONE planted doc (`docs/seat-digest.md`) carrying both blocks, not
   two docs — one tree-scan target for fm, one refresh surface, one
   drift guard.
3. ⚑ The doc lives OUTSIDE `ADOPT_PLAN` (planted by a dedicated adopt
   step): it is a derived render of live tree content, so template
   hash-classification would misread every ledger append as doc drift;
   check_engagement's unrendered scan correctly never covers it.
4. ⚑ Upgrade refresh covenant mirrors the capability-seed shape — a
   hand-edited copy is NEVER clobbered (report-line downgrade) even
   though the doc is kit-owned wholly; clobbering would destroy the
   evidence of what the consumer thought they were doing.
5. ⚑ Unlike the ledger refresh, digest regen/refresh DOES re-record the
   doc hash — the file must keep classifying kit-written so the next
   refresh reaches it.
6. ⚑ Venue filter persisted ON the walls BEGIN marker (`venues=`), not in
   config — the committed doc self-describes, regen/checker preserve a
   seat's choice with zero config surface, and fm can read the filter in
   the same scan.
7. ⚑ Walls digest ships WALLS only (seed Walls rows + `wall`-tagged
   appends; capabilities excluded) — the fm `{{WALLS}}`-class semantics
   the slice-5 prerequisite named.
8. ⚑ Missing/unreadable ledger → honest placeholder row, no template
   fallback — fewer moving parts; the normal adopt path plants the ledger
   first so the placeholder never fires there.
9. ⚑ Budget enforced by row truncation into an explicit `+N more` pointer
   row (row limit 160 chars, word-boundary) — mechanical, never trusted
   to content size.
10. ⚑ Refresh wired AFTER the upgrade's adopt pass (6c) so replanted
    docs and the (4b) ledger fence refresh precede the re-render.
11. ⚑ `cmd_seat_digest` carries no kit-tree guard (consumer #0 may regen
    its own digest; the command writes exactly one generated file) and
    never creates state in an uninitialized tree (hash recorded only when
    an install exists — the guard-fires precedent).
12. ⚑ Extraction contract + no-third-copy chain homed IN the generated
    doc itself (travels with the artifact to every adopter and to fm's
    tree scan) + the SKILLS-index pointer section — no separate planted
    contract doc (slices 1–5 precedent: doctrine rides existing homes).
13. ⚑ The kit's own tree receives no `docs/seat-digest.md` this session —
    consumer #0 takes it at its next self-upgrade (slice-5 flag-11
    precedent; hand-planting here would blur the mechanism's field test).
14. ⚑ `seat-digest-over-budget` kept as its own advisory kind beside
    `stale` — it is the one drift class that breaks the downstream paste
    budget outright and deserves the sharper message.

## Session enders

💡 **Session idea:** promote a canonical `extract_fenced_block(text,
begin_prefix, end_prefix)` helper into `engine.grammar` public API (and
document it in the extraction-contract table): the kit already carries two
near-identical private implementations (`upgrade._capability_fence`,
`check_seat_digest._fenced_block`) and fleet-manager's regen tool is about
to write a third — publishing ONE canonical extraction function (pure
stdlib, ~15 lines, vendorable verbatim) makes the extraction contract
executable instead of prose and kills the three-copies drift class this
very program exists to kill. Dedup-checked `docs/ideas/` (nearest:
control-board-kit-readiness-cell — status-line extraction, different
axis).

⟲ **Previous-session review:** slice 5's card was again the program's
strongest hand-off — all three slice-6 prerequisites held exactly as
written (the venue column made the walls filter a mechanical two-token
match; the fence-prefix pair was documented as the extraction contract
verbatim as instructed; the §4.2e no-third-copy chain was stated with the
exact deferral order it demanded). One genuine improvement: its
prerequisites block described the fm integration in the plan's
`{{WALLS}}`-slot vocabulary without pinning the fm HEAD it assumed —
fm had ALREADY moved to v3.3 (791772f, retiring those slots) when the
card was written, and only the coordinator's scout pass caught it. A
prerequisites block that names a cross-repo integration point should pin
the consumer repo's verified HEAD SHA (the same tree-over-registry
instinct the wave runbook already mandates), so the next worker inherits
a dated fact instead of a stale model.

Documentation audit: CHANGELOG entry present (prior slices kept); the
extraction contract + no-third-copy statement live in the generated doc +
grammar comments + CHANGELOG (their durable homes); SKILLS-index tmpl
carries the pointer; no new doc needs an ideas-index entry; the
decide-and-flag list above is the complete set of unrecorded judgment
calls; status.md overwritten per the block grammar (rebased onto #280
first — wave content preserved verbatim). Claim file deleted in the flip
commit. Capability delta: none — branch push, MCP PR open (#279),
rebase, and the dist e2e all behaved as already recorded for this venue.

**Slice-7/8 + fm-side prerequisites discovered:**

- **fm-side PR (the coordinated follow-up, NOT slice 7/8):** consume
  `docs/seat-digest.md` per seat repo via the three grammar prefix pairs
  (tree scan, fence-prefix match, byte compare — the currency.py-precedent
  scan shape); the walls venue filter rides the committed `venues=`
  marker (per-seat class overrides = regen each adopter's doc with
  `--venue`); UNIVERSAL wake fetch list gains the digest/index (vN bump +
  owner re-paste per fm's edit-registry-first flow); budgets verified fit
  (blocks 1424/1045 ≤ 1500 against CI_HARD=8000/CI_AIM=7500).
- **Next release + wave:** every adopter upgrade replants
  `docs/seat-digest.md` (`planted:` line — the adopt pass replants
  missing docs) and thereafter emits `seat-digest:` refresh lines; the
  wave runbook reading should treat a `NOT regenerated (hand-edited)`
  line as a lane-owed item, not a wave failure. The doc arrives
  reachable only where `docs/SKILLS.md` takes the template improvement
  (`upgrade --apply-docs`) — diverged-orientation repos may need the
  same one-hunk hand-merge class as the v1.13.0 wave's SKILLS.md wiring.
- **Slice 7 (websites guard widening):** unchanged by this slice; note
  the digest doc is exactly the phone-readable artifact the control-plane
  `/journal/{repo}/file` render shows well once lane repos are allowed.
- **Slice 8 (self-propagation doctrine):** the registration reflex clause
  should name the digest as self-maintaining (a new SKILLS entry reaches
  every adopter's digest via the normal upgrade refresh — no extra step
  to teach); the 💡 above (public extraction helper) is a natural rider
  if slice 8 touches grammar anyway.
