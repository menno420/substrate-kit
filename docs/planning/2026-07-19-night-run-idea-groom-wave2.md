# Wave-2 idea groom — post-R15 buildable-now ladder

> **Status:** `plan` · 2026-07-19
>
> Swept: the `📊 Model:`-line exit-gate trilogy session cards
> (`2026-07-19-*` R13/R14/R15), their `💡` session ideas + `⟲` reviews + friction
> flags, and `docs/ideas/`. Deduped against everything the R1–R13 groomed ladder,
> R14 (#513), and R15 (#514) already shipped. Classified: buildable-now (S/M +
> one-line recipe) · needs-planning · owner-gated / cross-repo.

## Why this doc exists
This groom **succeeds the exhausted R1–R13 ladder** (`docs/planning/2026-07-19-night-run-idea-groom.md`),
**R14** (the coordinator-directed segment-1 exact-model-ID exit-gate, #513), and
**R15** (the segment-2 effort exit-gate, #514, which completed the `📊 Model:`
line exit-gate trilogy — model-ID #513, task-class #512, effort #514). With the
trilogy shipped, `control/status.md` was left asserting the buildable-now backlog
was exhausted and warning "do NOT fabricate an R15" — now false, since R15 merged.
This doc collects and ranks the fresh wave-2 slices so the next wakes have real
buildable work again, and retargets the baton forward at them.

## Buildable-now — ranked (S/M + one-line recipe)

- **S1 — segment-2 effort exit-gate** — completed the 📊 Model line exit-gate trilogy (model-ID #513, task-class #512, effort). → **SHIPPED as PR #514.**
- **S2 — advisory→born-red-gate graduation recipe** (docs/recipes/, carrying R11's applies-when: badge) — documents the exact pattern #512/#513/#514 followed.
- **S3 — un-groomed-idea counter advisory** — counts 💡 lines on cards newer than the newest groom doc; blocks a false "backlog DRY."
- **S4 — check_baton_resolves advisory** — verify every `## Next-2 baton` entry names a real resolvable path/anchor.
- **S5 — shared require_full_history() helper** — extract in git_truth.py, harden measure_pr_latency.py.
- **S6 — inline WALL_CORRECTIONS into check_no_false_walls message** — wire per-rule corrections into the Finding.
- **S7 — check --remediate <finding-kind>** — print paste-ready remediation blocks only.
- **S8 — signature-honesty lint for applies-when: tokens** — cross-check tokens against recipe body.
- **S9 — --freeze --verify companion** — re-hash sidecar, non-zero on mismatch.
- **S10 — check_surface_census advisory** — surface guards/jobs/hooks census in check output.
- **S11 — reverse fastlane symmetry** — ci.yml self-declares cardless prefixes (# fastlane-cardless:).
- **S12 — auto-derive lint families from ledger bold titles.**
- **S13 — clone-depth provenance on results.json** (clone_depth + git_sha).
- **S14 — dateless-wall advisory** — flag wall rows with no parseable date.
- **S15 — cut_release --rebuild-dist** — fold FOLLOWUP dist rebuild into the cut.
- **S16 — --api-latency harness mode** (opt-in, env-gated on GITHUB_PAT) — larger, needs live GH.

## Needs-planning
- **Config-driven stale-doctrine guard** (carried from wave-1): generalize
  `check_no_false_walls` into a `substrate.config.json` `stale_doctrine` list
  (`{name, blocklist_regex[], clear_cue[]}`) so a new correction ships a config entry
  instead of a new script. M/L — refactors an enforcing guard; design the config schema +
  back-compat first.

## Owner-gated / cross-repo (carry forward — not kit-landable now)
- **v1.20.0 cut** — DEFERRED pending adopter-wave authorization; carries the R13/R14/R15
  born-red exit-gates + the #482 pinned-feed rider + the #484 folded-gate checker to
  adopters. Held decision in `control/status.md`.
- **The 5 ⚑ FOR-OWNER blocks** in `control/status.md` — kit-lab daily cron recreate/retire,
  v1.19.0 adopter-wave authorization, CAPABILITIES denial-record entry, public-flip-or-PAT,
  t5-headless-guard fix. All await one live owner turn each; carried forward verbatim.

## Baton retarget
`control/status.md` Next-2 baton now points forward at the wave-2 ladder — **S2
(advisory→born-red-gate graduation recipe)** is the top buildable-now rank,
superseding the stale "ladder COMPLETE / do NOT fabricate an R15" text.
