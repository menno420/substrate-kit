# Night-run idea groom — 2026-07-18/19 session cards (#455–#486)

> **Status:** `plan` · 2026-07-19
>
> **Succeeded by** `docs/planning/2026-07-19-night-run-idea-groom-wave2.md` — the
> R1–R13 ladder below is exhausted (all shipped) and R14/#513 + R15/#514 closed the
> two coordinator-directed born-red exit-gates; the wave-2 groom ranks the next
> buildable-now ladder (S2–S16).
>
> Swept: all `.sessions/2026-07-18-*.md` + `2026-07-19-*.md` `💡` lines + friction
> flags, and `docs/ideas/`. Deduped against what shipped in the night run (#455–#486).
> Classified: buildable-now (S/M + one-line recipe) · needs-planning · owner-gated /
> cross-repo · dead / duplicate.

## Why this doc exists
The night chain shipped #455–#486 but left `control/status.md` asserting the buildable-now
backlog was "DRY" — because the baton sweep read only
`docs/planning/2026-07-19-needs-planning-recipes.md`, not the ~14 unbuilt `💡` ideas
accumulating on the night's session cards. This groom collects and ranks them so the next
wakes have slices.

## Already shipped in the night run — deduped as DONE
| Idea (source card) | Shipped as |
|---|---|
| guard-parity meta-test | #459 |
| claims-only fast-lane guard (both surfaces) | #455 / #457 |
| no-false-walls guard fleet-wide | #444–#450 |
| declarative guard-manifest | #463 |
| guard-parity 3rd surface (check --strict) | #466 |
| B-1 guard-surface census (WORKFLOW_JOB_CENSUS) | #470 |
| B-2 self-row registry-stamp automation | #472 |
| B-3 fast-lane prefix symmetry lint | #474 |
| GSW-5 opt-in --api-latency harness mode | #479 |
| pinned-feed-contract doctrine graduation | #482 |
| folded-gate diff-aware advisory sub-check | #484 |
| v1.19.0 release | tag v1.19.0 |

## RETIRED — do NOT re-queue
- **Codegen kit-ci step names from the guard-manifest** (guard-manifest card) — retired
  in #465 as a verification-covered null; the parity test already covers drift.

## Buildable-now — ranked (S/M + one-line recipe)

**R1 (S) — cut_release dist-before-self-restamp reorder.** `scripts/cut_release.py`
restamps the self-row before the aftermath dist rebuild, so a version-bump PR momentarily
commits a `docs/adopters.md` whose own self-row shows DRIFT against the kit. *Recipe:*
reorder so the dist rebuild precedes `restamp_self_row` (or write a `pending-rebuild`
marker into the self-row tree cell); + a test asserting the post-cut committed
`adopters.md` self-row is non-DRIFT. (from #472 card)

**R2 (S) — `/scope-backlog-item` skill.** *Recipe:* add a `docs/SKILLS.md` skill that
scaffolds the planning-recipe arc (chase origin → Q-0254 fuller picture → classify
buildable/owner-gated/dead + sized recipe or six-field ⚑ → retarget baton), making the
standing "when no exec work is left, plan" order turnkey; index it in docs/SKILLS.md.
(from #480 card)

**R3 (S) — shallow-clone REFUSE marker.** *Recipe:* `scripts/measure_grounded_skills.py`
emits a loud REFUSE marker / exits non-zero when `--json` is requested on a shallow clone
(M4 would be zeroed); + test. Turns a prose trap into an enforced refuse-to-publish.
(from plan-grounded-skills-window card)

**R4 (S/M) — HOOK_CENSUS (second fourth-surface vector).** *Recipe:* mirror
`WORKFLOW_JOB_CENSUS` (#470) with a `HOOK_CENSUS` in `src/engine/guards.py` +
`tests/test_guard_surface_census.py` that enumerates repo git-hooks and classifies each
(enforcing-and-pinned / advisory / dev-convenience). (from guard-surface-census card)

**R5 (M) — capability stale-wall advisory.** *Recipe:* `src/engine/checks/check_stale_walls.py`
(advisory, not red) surfaces any `wall` ledger row in CAPABILITIES.md whose LAST-VERIFIED
date is > N days old — the enforcement analogue of the DISCOVERY RULE; wired into
`_extra_check_findings`. (from generalize-wall-guard card)

**R6 (S/M) — check --explain-wall / --why.** *Recipe:* `bootstrap.py check --explain-wall
<phrase>` (or `--why` on a false-wall finding) prints which blocklist rule matched + the
one-line ground-truth correction + a pointer to the capabilities-ledger dated-row form.
(from propagate-wall-guard card)

**R7 (S/M) — append-log ⇄ Walls correction disagreement lint.** *Recipe:* a kit-side lint
that flags when a `## Walls` correction and the newest `## Append log` entry in
CAPABILITIES.md disagree on the same capability (merge/arm/flip) — catches the
self-contradiction that persisted a full day. (from capabilities-mergedoctrine-correction card)

**R8 (M) — fast-lane prefix symmetry as runtime check --strict advisory.** *Recipe:*
promote the B-3 kit-only pytest meta-test to `src/engine/checks/check_fastlane_symmetry.py`
so ADOPTERS catch their own enabler↔guard prefix drift; wired into `_extra_check_findings`
+ `guards.STRICT_SUBCHECKS`. (from fastlane-prefix-symmetry card)

**R9 (S) — harness --commit-results PATH.** *Recipe:* a `--commit-results PATH` flag on
`measure_grounded_skills.py` (or a plan mandate) so a GSW-style measure→verify→publish
chain commits its raw results.json as a durable artifact surviving ephemeral-container
splits. (from gsw-1 card)

**R10 (S) — harness --freeze self-citing reproduce block.** *Recipe:* a `--freeze`
companion that, given `--json`, also emits the output's sha256 + a ready-to-paste
reproduce block (the exact command that produced it), making every window run self-citing.
(from api-latency-harness-mode card)

**R11 (S/M) — recipes `applies-when:` frontmatter tag.** *Recipe:* `docs/recipes/`
graduations carry an `applies-when:` frontmatter tag (a cheap structural signature) so a
future engine check can *nudge* an adopter that grows a matching seam toward the relevant
recipe — discovery, not enforcement. (from pinned-feed-contract card)

**R12 (M) — check_folded_gate remediation snippet.** *Recipe:* extend the #484 advisory to
also emit the exact diff-aware card-derivation block to port, so a host fixes the fold in
one paste; recurs across hosts (superbot-next `gate`, websites `quality.yml`).
(from folded-gate-check card)

**R13 (S/M) — exit-affecting PL-004 task-class gate on the session card the born-red gate
already grades.** *Recipe:* an off-taxonomy `📊 Model:` task-class (`kit-feature`) reached a
MERGED card because `check_model_line` (which *does* validate the segment against the 9 PL-004
classes — `src/engine/checks/check_model_line.py:181` — and *does* scan cards — same file
`check_model_line(...)` L214) is **advisory-only** (never exit-affecting; `cli.py` emits it on
the `posture="advisory"` seam) AND **windowed to the 10 newest cards** (`MODEL_LINE_LINT_WINDOW`),
so a drifted class merges green and ages out of the window unfixed. The gap is not "doesn't
validate / doesn't scan" — it's that nothing *gates* on it. Buildable slice: fold the
task-class check (segment-3 ∈ the 9 classes) into the **born-red session-gate** that already
grades the PR's own added card (`scripts/check_session_gate.py` / the `check --strict`
added-card grading in `cli.py`), so an off-PL-004 card on the PR's OWN card reds at CI —
enforce-don't-exhort, scoped to the one card the PR adds (never the fleet-wide window, whose
advisory posture stays). Recurs: the 2026-07-11 retro W-10a flagged the same drift class.
(from R7 (#498) card ⟲ previous-session review + this R8 session's investigation)

## Needs-planning
- **Config-driven stale-doctrine guard** (false-wall-guard card): generalize
  `check_no_false_walls` into a `substrate.config.json` `stale_doctrine` list
  (`{name, blocklist_regex[], clear_cue[]}`) so a new correction ships a config entry
  instead of a new script. M/L — refactors an enforcing guard; design the config schema +
  back-compat first.

## Dead / duplicate
- **kill-false-merge-walls lint** (kill-false-merge-walls card): scan templates + guard-tests
  for standing-prohibition phrasings — DUPLICATE of the shipped `check_no_false_walls`
  campaign (#444–#450). Dead.

## Owner-gated / cross-repo (not kit-landable now)
- **check_folded_gate host ports** — superbot-next `gate` job, websites `quality.yml`:
  cross-repo follow-ons, routed to fm via outbox (#486). Not kit-landable.
- **v1.19.0 adopter wave** — owner-gated (⚑ in control/status.md).
- **23-proposal veto menu** (`docs/planning/2026-07-16-overnight-veto-menu.md`) — owner-gated.

## Note — the phantom "#466 claims-guard add-vs-delete exemption"
The dispatch referenced a "claims-guard add-vs-delete exemption veto item (#466)". No
idea/flag with that description exists in the tree (searched `.sessions/` + `docs/`); the
honesty note in `docs/planning/2026-07-19-grounded-skills-window-run.md` records the same
finding. #466's card 💡 is the guard-surface census (→ B-1 #470); its ⚑ is the
`STRICT_SUBCHECKS` public-API design call. The nearest real items are B-3 (shipped #474)
and veto-menu item 15 (lane-parity added-vs-modified meta-test, owner-gated). Recorded,
not guessed.

## Baton retarget
`control/status.md` Next-2 baton now points at **R1 (cut_release dist-order fix)** and
**R2 (`/scope-backlog-item` skill)** — the top buildable-now slices.
