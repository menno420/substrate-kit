# 2026-08-13 · kit-release-v1.21.0 — the seven-defect cut

> **Status:** `in-progress`

- **📊 Model:** fable-5 · high · runtime bugfix
- ⚑ Self-initiated: no — owner-directed. The 2026-08-09 ruling was *"both, in
  order"*: fleet-manager took released v1.20.2 (fm #833), and the v1.21.0 cut
  is this dedicated session, re-confirmed live by the owner 2026-08-13.

💡 Session idea: **every one of the seven defects survived because the
scanner's author was its only reader.** Codex found all seven by reading the
vendored dist inside an fm upgrade diff — probably the first non-author read
since the code shipped. The defect-6/7 pair is the sharp version: one
deliberate, correct boundary (the conjunction split) shipped with its
complement missing (the subordinator split) and its price unmeasured (the
quoted-mention false positive). A fix reviewed only by its author is tested
against exactly the cases its author thought of — which is why this cut's
verification is an A/B harness someone else wrote (fm `tools/ab_kit_scan.py`)
run against the published asset, not this session's word.

## previous-session review

The four 2026-08-06 cards (#577–#580 era) check out against the tree:
`ADVISORY_CENSUS` + the six-site promotion + `--gate-preview`/`--advisories`
are live in `src/engine/guards.py`/`cli.py` under `## [Unreleased]`;
`check_boot_path` ships DETERMINISTIC and deliberately un-gated;
`docs/planning/2026-08-06-provenance-review-mandate.md` exists as its card
says. One honest gap this session must close rather than inherit: the
promotion entry's 12-tree `--gate-preview` sweep is dated **2026-08-06** and
the trees have moved since — fm's own record rules that one tree's zero is not
evidence for twelve, so the sweep is re-run here against the NEW dist before
anything is published. Result recorded below before the flip.

## Intent

Cut and publish **substrate-kit v1.21.0**: close the seven-defect worklist
(fleet-manager `docs/findings/2026-08-09-substrate-kit-defects.md` — defect 7
first, a false NEGATIVE on the required gate), upstream the three
substrate-gate hardenings fleet-manager re-applies by hand at every upgrade,
retract the three capability-seed walls its 2026-08-11 audit refuted (plus the
same refuted wall in the `enforcement-required-unverified` NOTE and the
branch-sweep template), bump the version homes, transform the CHANGELOG,
rebuild the dist, land born-red, publish via `release.yml`
`workflow_dispatch`, and verify the published asset three ways plus
`ab_kit_scan.py` (all seven rows + the fresh-adopter template contract).

Scope: `src/engine/checks/check_no_false_walls.py` ·
`src/engine/checks/check_engagement.py` · `src/engine/adopt.py` ·
`src/engine/guards.py` · `src/engine/templates/SKILLS-index.md.tmpl` ·
`src/engine/templates/CAPABILITIES.md.tmpl` · `tests/` (three new files, three
updated) · `CHANGELOG.md` · the three version homes · `dist/bootstrap.py` ·
this card · `control/claims/release-v1-21-0.md`.

## The intake-graduation call — deferred, stated here as the fm prompt requires

Roadmap § 7 allocates *generalised intent resolution* to substrate-kit, and
the § 4.8 bar closed 2026-08-13 (produce AND score, fresh, PARTIAL confirmed
3/3 scorings) — so the promotion rule's "measure first" condition has fired
and the map COULD ride this release. **Deferred, three reasons.** (1) This
release's job is repairing the required gate's false negative; grafting a
feature graduation onto the same cut couples a correctness fix twelve adopters
need to a design migration none has asked for. (2) fm #852 added a hard
prerequisite the graduation does not yet meet: imprecision counts proved
scorer-relative (4–11 on identical maps), so the checker-side needle rule must
be pinned before the kit ships a generalised form. (3) The hazard the ride
would close — the hand-run copy loop reverting fm's `intake` — fires on the
loop, not the upgrade (fm #833 measured), and the loop's own template now
warns diff-before-copy, so the exposure is narrower than the OPEN item's
phrasing. The graduation is its own session, after the needle rule is pinned.

## Verification (each box checked only when its command has actually run)

- [x] `python3 -m pytest tests/ -q` — **2152 passed, 1 skipped** (2026-08-13,
      this tree, before the version bump)
- [x] `python3 -m ruff check src/engine/` — clean
- [x] `python3 dist/bootstrap.py check --strict` — **exit 0** before this
      card existed; with the card in-progress the added-card lane holds the
      PR red BY DESIGN until the flip
- [x] corpus A/B v1.20.2 vs this tree — 93,811 md lines across both repos,
      **0 newly flagged**, 4 old→clear, each hand-verified as the defect-6
      quoted-mention class (three document the repro itself; the fourth is
      the seat-era grant digest fm allowlisted 2026-07-20)
- [x] fresh 12-adopter `--gate-preview` sweep with the NEW dist, run
      2026-08-13 against every tree in `docs/adopters.md` at that hour's
      HEADs — **the six PROMOTED sites carry 0 findings on 12/12 trees**, so
      shipping the promotion reds no adopter. Every would-red row on the
      sweep belongs to a site this release deliberately does NOT promote:
      `boot_path` fires on 10 of 12 trees (consistent with its changelog
      entry's 0-of-11 measurement — promoting it would red nearly the whole
      fleet, which is exactly why it ships un-gated) and
      `automerge_preflight` on 2 (superbot-next, superbot — the enabler
      allowlist drift the census entry records). superbot has no vendored
      dist (pin-only v1.0.0); the new dist ran against its tree directly.
- [ ] `python3 src/build_release_json.py --version 1.21.0 --verify-only`
- [x] Codex round 1 at head `a7f6c59` — **6 inline findings (2×P1, 4×P2),
      every one reproduced before disposition**: P1 quoted-wall over-clear
      `[conceded]` (line-wide widening → mention REGION stopping at
      contrast/subordinator boundaries; quotation is not repudiation);
      P1 subordinator gaps `[conceded]` for `if`, `[partial]` for causal
      `as` — deliberately deferred with the fm #836 evidence (fm's own `as`
      boundary needed a negated-complement exemption chain across three
      review rounds and still banked an over-exemption residual; that trade
      belongs to the checker-contract bank, stated in the code comment);
      P2 blockquote-prefixed fences `[conceded]`; P2 leaving-a-blockquote
      `[conceded]` (state-differs both directions); P2 `bash -c`-wrapped
      sentinel append `[conceded]` (direct-invocation anchor); P2 custom
      `state_dir` copy loop `[partial]` (no template slot carries state_dir;
      all 12 registry adopters run the default; adjust-if-customized caveat
      added). Each fix carries a fixture named `r2_*` / `d7_subordinator_if`.
- [ ] Codex round 2 at the post-fix head — the second and final re-review
      round `session-close` allows; result recorded here before the flip
- [ ] three-way asset verification after publish — release record appended
      below with run id, tag SHA and sha256

## Release record

*(empty until the publish step actually runs — the record is appended with
the real run id, tag SHA and three-way sha256, never pre-filled.)*
