# Session · 2026-07-18 · adopter-claims-guard

> **Status:** `complete`

Intent: propagate the claims-only fast-lane guard from the kit's own CI
(`.github/workflows/ci.yml`) into the GENERATED adopter CI produced by
`src/engine/adopt.py` `live_ci_workflow()` (the `substrate-gate` workflow
adopters run), so adopter repos get the same #451 fast-lane-race protection.

- **📊 Model:** Opus 4.8 · high · feature build
- ⚑ Self-initiated: no — owner-directed slice.

About to: mirror the ci.yml "Claims-only fast-lane guard" step into
`live_ci_workflow()` (between the inbox append-only gate and setup-python,
pure workflow bash — the engine never shells out, §3.2), rebuild
`dist/bootstrap.py` via `src/build_bootstrap.py`, pin the new step in
`tests/test_adopt.py` (+ retighten the inbox-gate test bound), and add an
adopter-propagation note to `docs/operations/auto-merge-guards.md` row 7.

## What shipped

- `src/engine/adopt.py` `live_ci_workflow()`: the "Claims-only fast-lane
  guard" step is now mirrored into the GENERATED adopter CI (`substrate-gate`),
  placed between the inbox append-only gate and setup-python — fast-lane only
  (`control_only == 'true'`), `claude/*` heads only (a non-`claude/*` head
  exits 0), red (`::error::` + `exit 1`) when every changed path is under
  `control/claims/`. Pure workflow bash; the engine never shells out (§3.2).
  So adopter repos now get the same #451 fast-lane-race protection the kit's
  own `ci.yml` gained in PR #455.
- `dist/bootstrap.py` rebuilt from the engine via `src/build_bootstrap.py`
  (byte-pin), so the shipped single-file distributable carries the new
  generated step.
- `tests/test_adopt.py`: textual pin asserting the mirrored step exists in
  `live_ci_workflow()` output (lane-conditioned, `claude/*` head-gated,
  `grep -v '^control/claims/'` detection), plus the inbox-gate test bound
  retightened. Full suite green (1761 pytest pass).
- `docs/operations/auto-merge-guards.md`: row 7 gains the adopter-propagation
  note recording that the guard now ships to generated adopter CI too.
- ⚑ Self-initiated: no — owner-directed slice (baton item queued by the
  PR #455 session).

## 💡 Session idea (Q-0089)

**Guard-parity meta-test: kit-vs-adopter guard drift detector.** Add a kit
test (or a kit-quality lint step) that asserts every *enforcing* guard step in
`.github/workflows/ci.yml`'s `kit-quality` job has a mirrored counterpart in
`src/engine/adopt.py` `live_ci_workflow()` — or an explicit allowlist entry
marking it kit-only-by-design. This session existed *only* because the
claims-only guard shipped to the kit's own CI (PR #455) but not to the
generated adopter CI, and nothing detected that drift until a human queued it
as a baton item. A parity check would catch kit-vs-adopter guard drift
automatically — turning "notice it later, queue it as a baton" into a red CI
signal the same PR that opens the gap. Deduped against `docs/ideas/` (no
near-duplicate; the added-vs-modified lane-parity meta-test in
`docs/planning/2026-07-16-overnight-veto-menu.md` asserts two *lanes* of one
surface share a helper — this asserts two *surfaces* share a guard set).
Dropped as a durable one-file idea so it survives heartbeat rewrites:
`docs/ideas/guard-parity-kit-vs-adopter-2026-07-18.md` (indexed in the backlog
README). Small, test-only, reversible; not built this session.

## ⟲ Previous-session review (Q-0102)

Of the 2026-07-18 claims-only-fastlane-guard session (PR #455): genuine
credit — it correctly added the enforcing guard to the kit's OWN `ci.yml`
(`kit-quality` step "Claims-only fast-lane guard"), pinned it with a textual
test (`tests/test_ci_control_lane.py`), and documented it as guard-stack row 7
— closing the #451 card-less-merge race for the kit's own repo. Reasonable
split, small miss: it scoped adopter propagation OUT as a follow-up baton item
rather than shipping the kit-own gate and the generated adopter gate in one
pass — a defensible "kit-own first, generated second" ordering, but it meant
adopters ran without the guard for a window (which this PR #457 closed). The
concrete system improvement it surfaces: the **guard-parity meta-test** above
(💡) — a checker that asserts the kit-own `ci.yml` guard stack and the
adopter-generated `live_ci_workflow()` guard stack can't silently drift, so a
future guard added to one surface can't ship without the other (or an explicit
kit-only-by-design allowlist entry). That converts this exact "propagate it
later" gap from a hand-queued baton into an automatic red-CI signal.
