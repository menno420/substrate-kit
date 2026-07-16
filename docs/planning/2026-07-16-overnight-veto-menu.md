# Overnight veto-ready proposal menu — substrate-kit (2026-07-16)

> **Status:** `plan`
>
> **Provenance:** ORDER 025 (owner overnight autonomy order) — PLANNING MODE. Backlog verified dry beyond owner-gated / date-parked items. Repo @ origin/main `9ca23fb`. (ORDER 025 itself is classifier-walled from landing in control/inbox.md; verbatim order lives in the coordinator transcript + session brief.)
> Evidence base: session cards #422–#432, `docs/CAPABILITIES.md`, `docs/adopters.md`, `src/engine/templates/`, `src/engine/checks/`, `docs/program/rulings.md`, `docs/ideas/README.md`, `docs/planning/`, `src/engine/adopt.py`.
> Grep route: §How to read · §1 Landing/branch hygiene · §2 Registry/adopters · §3 Templates/graduation · §4 Gates/checks · §5 Release/cadence · §6 Docs/hygiene · §7 Ambitious · §8 Non-goals.

---

## How to read this menu

This is a **veto menu**, not a plan of record. ORDER 025 asked for breadth — "plan excessively… my veto is the filter, so don't pre-filter down to a few safe picks." So every honest candidate is listed, S→L, safe→ambitious; nothing here is committed. Each entry carries **effort** (S = <½ PR · M = ~1 PR · L = 2–3 PRs / cross-repo), **risk/reversibility**, and **unblocks**. Status tags: `buildable` (safe now) · `owner-gated` (needs owner console/decision) · `date-parked` (window not open). M/L items are planning-only; contained + reversible S items may be built as separate PRs.

Dupe-guard: items already captured in `docs/ideas/` or `docs/planning/` are cross-referenced, not re-proposed.

---

## §1 — Landing / branch hygiene

**1. Dogfood branch-sweep in the kit's own repo.** `S` · reversible (one workflow file; deletes only spent refs) · `buildable` · unblocks: the kit stops littering its own hundreds of spent `claude/*` refs. The kit *ships* `branch_sweep_workflow()` (`src/engine/adopt.py`, `BRANCH_SWEEP_RELPATH`) but its own `.github/workflows/` never installed it. Wire via `adopt --wire-enforcement` on the kit repo, or commit the generated file. Deletes real refs, so pair with item 2 first for confidence.

**2. `bootstrap.py sweep --dry-run` local preview.** `M` · read-only, zero-risk · `buildable` · unblocks: trust for the first fleet-wide large ref deletion. Renders the sweep plan (existing ∩ spent − open-PR-heads − default) against the live API without dispatching. (ORDER-023 card idea.)

**3. Auto-update-branch mitigation workflow template.** `M` · reversible · `buildable` · unblocks: the "green-but-behind-main, armed-but-won't-fire" stall class the CAPABILITIES ledger flags as OWNER-ACTION. A kit-templated workflow that merges origin/main into a green-but-behind armed PR and pushes, closing the residual without the owner "automatically update branches" repo setting.

**4. Landing-protocol doctrine consolidation.** `S` · docs-only · `buildable` · unblocks: one canonical landing recipe. The auto-merge walls (self-merge classifier, behind-main, fast-CI arm race, enabler-fires-once) are scattered across ~6 CAPABILITIES entries + `docs/operations/auto-merge-guards.md`. Consolidate into one decision-tree doc adopters copy.

**5. Landing-protocol redesign (sibling-PR / self-merge wall).** `L` · higher-risk (touches merge policy) · planning-only · unblocks: the AUTHORSHIP-scoped self-merge classifier wall that forces every green PR through the enabler backstop (and blocked ORDER 025's own landing tonight). Explore a review-attestation lane (a second session's review-then-merge PASSES the classifier) as a first-class kit-templated landing option rather than a workaround. Ambitious.

## §2 — Registry / adopters

**6. Adopters staleness self-signal.** `S` · advisory, non-gating · `buildable` · unblocks: a missing/failed currency cron becomes a visible nudge instead of silent drift. `check --strict` emits an advisory when `docs/adopters.md` `Generated:` is older than ~26h. (registry-refresh card idea; enforce-don't-exhort / PL-007.)

**7. Recreate the kit-lab daily currency cron (owner A/B "A").** `S` · reversible · `owner-gated` · unblocks: honest lab-loop doctrine + auto-fresh registry. `docs/operations/lab-loop.md` asserts a `0 6 * * *` cron "stays armed"; nothing arms it. Build = arming doc + template; owner arms in console. (Standing owner ask.)

**8. Fix lab-loop.md doctrine drift (owner A/B "B" fallback).** `S` · docs-only · `owner-gated` (A/B with item 7) · unblocks: removes the false "stays armed" claim so a rebooted seat doesn't trust a dead loop.

**9. Fix the kit's own substrate.config.json pin drift.** `S` · trivial, reversible · `owner-gated` (tied to the open §7 self-pin version-truth ruling) · unblocks: clears the kit's own DRIFT row in adopters.md. The kit runs v1.18.0 but substrate.config.json still pins kit_version 1.0.0. Mechanically trivial once the ruling lands.

**10. Adopter-upgrade wave automation.** `L` · higher-risk (cross-repo writes) · planning-only · unblocks: the manual, classifier-denied adopter wave. Every wave is hand-driven and hit a permission denial. Propose an issue-driven or PR-generating mechanism so the fleet upgrades without a live-owner-authorized seat each time. Ambitious.

## §3 — Templates / graduation

**11. Generated-workflow bodies: Python-string → data-file + substitution.** `M` · refactor, test-covered/reversible · `buildable` · unblocks: kills the quote-escaping bug class. Three generated workflows (gate, enabler, sweep) are each one long string concatenation; the ORDER-023 author hit an escaping bug. Move bodies to data files rendered with a tiny substitution pass. (ORDER-023 card review.)

**12. Template-add checklist as a checker.** `S/M` · advisory · `buildable` · unblocks: the predictable first-red every src/engine/templates/ addition hits. Enforce: badge token from the allowed set · pointer-guard resolution tables · no unrendered slots outside the bank · dist regen. (archive-s1 card review.)

**13. Canonicalize draft-state badge doctrine.** `S` · docs+test · `buildable` · unblocks: the next drafting verb rediscovering the badge-allowlist wall. Rule: "badges are terminal; unresolved fill slots are the draft signal" — one line in the badge-checker docstring + a test. (archive-s1 card idea.)

**14. KL-5 / PL-008 residue-advisory → hard gate graduation.** `S` · reversible (flip advisory to error) · `date-parked` (awaits quiet period) · unblocks: session-card-slot-residue + archive advisories become merge-blocking once proven quiet. Named as the standing next step in control/status.md Backlog.

## §4 — Gates / checks

**15. Lane-parity meta-test.** `M` · test-only, reversible · `buildable` · unblocks: the symmetric-gap class that cost 3 PRs (#426→#428→#429). Enumerate dual-lane checks (added-card vs modified-card) and assert each pair routes through one shared helper. (no-badge-parity card idea.)

**16. Model-line taxonomy validation at flip-time.** `S` · reversible · `buildable` · unblocks: a card can't merge with an off-taxonomy model line. Today only a post-hoc advisory (which already fired on a real card). Have the born-red gate validate the flipping card's own model line. (registry-refresh card review.)

**17. check_idea_index leg 7 — frontmatter⇄README-section agreement.** `S` · advisory-first · `buildable` · unblocks: shipped-idea flips silently accumulating in the Backlog section (8 drifted over 4 days undetected). Assert outcome=shipped files sit in Shipped, captured in Backlog. (idea-index-shipped-drift card idea.)

**18. Blast-radius note convention on bug-idea filing.** `S` · docs/checklist (optional checker) · `buildable` · unblocks: the fixing session re-deriving caller sets. A bug filed on a card carries a one-line grep-count + affected-lanes note; costs the filer one grep. (status-badge-value-parse card review.)

## §5 — Release / cadence

**19. bootstrap release-prep X.Y.Z verb.** `M` · reversible · `buildable` · unblocks: turnkey release cutting. The prep bump is a hand-assembled 4-part ritual (KIT_VERSION + pyproject + CHANGELOG section + dist re-pin). One verb stages all four, then release.yml dispatch removes the recurring hand-sequence.

**20. CI cost review / path-filtered fast lane.** `M` · reversible · `buildable` · unblocks: cheaper CI. ci.yml runs a cold-adoption smoke (two full renders), the full pytest suite (1700+), ruff, and ~6 script checks on every PR incl. docs-only. Propose path filters / a fast lane for docs-only diffs (extend the existing control fast lane pattern).

## §6 — Docs / hygiene

**21. docs/planning/ index.** `S` · docs-only · `buildable` — **being shipped alongside this menu** · unblocks: planning-doc discoverability. docs/ideas/ has a README index with lifecycle; docs/planning/ had none.

**22. Prune / retire stale planning briefs.** `S` · reversible (git-recoverable) · `buildable` (owner-confirm on deletes) · unblocks: repo cleanliness for the "fresh seat picks up from repo alone" goal (ORDER 025 item 3). Four ~530-byte rebuild-phase briefs from 2026-07-06/07 are likely spent; mark historical (done in the new index) or remove on owner nod.

## §7 — Ambitious

**23. bootstrap.py doctor self-audit verb.** `M/L` · read-only · `buildable` · unblocks: one-command health readout. A verb that runs the DISCOVERY-RULE sweep (config-pin drift, registry staleness, un-dogfooded shipped workflows, armed-vs-documented routines, dist byte-equality) and prints a green/red ledger — turning the scattered fix-on-sight classes (items 1, 6, 9) into one observable surface. Ambitious — but every leg reuses an existing checker. (This session's idea.)

---

## §8 — Non-goals (tonight)

- Do **not** build the ambitious (L) items — planning only (ORDER 025 item 2).
- Do **not** touch draft #431 or held #433 — owner / coordinator lanes.
- Do **not** re-arm routines — ORDER 024 EAP freeze through 2026-07-21.
- Do **not** run the v1.18.0 adopter wave or recreate the kit-lab cron without the owner — both are standing owner-gated asks.
- Adopter writes = kit distribution only; bench-oracle changes = second-session review.

_Morning: owner skims this menu, vetoes what he doesn't want; survivors become buildable slices for the next seat._
