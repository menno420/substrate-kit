# Turnkey recipes — the four needs-planning backlog items (2026-07-19)

> **Status:** `plan`
>
> Scopes the four items parked as "Needs-planning — scope before building" in
> `docs/planning/2026-07-19-grounded-skills-window-run.md:115` and the baton in
> `control/status.md`, so a future session executes each without re-derivation.
> Provenance: coordinator planning dispatch under fm ORDER 048 + the standing
> "when no executable work is left, plan" resume order.

## Honest shape first

The buildable backlog was reported dry, and scoping confirms a **shrink**, not four
fresh build slices. Of the four:

- **2 are buildable-now from this kit repo** — the pinned-feed doctrine and the
  folded-gate advisory checker (its "second occurrence" build trigger has now been met).
- **1 is owner-gated + cross-tree** — t5-headless-guard: the actionable artifact is a
  PIN-PATH `bench/tasks/T5.md` change requiring a `do-not-automerge` owner-review PR,
  and `bench/` lives in the kit-lab harness, not this repo.
- **1 has its kit half already shipped** — the readiness cell: ORDER 003 landed the
  `kit:` line + `docs/adopters.md`; all that remains is a cross-repo `websites`
  board-rendering feature, self-startable in that repo's lane.

None is dead. Ranked by value for the baton: **pinned-feed-contract > folded-gate
advisory > readiness cell > t5-headless-guard**.

---

## 1 · pinned-feed-contract doctrine — BUILDABLE-NOW (rank 1)

**Origin:** `docs/ideas/pinned-feed-contract-doctrine-2026-07-09.md` (captured;
consumer-proven end-to-end: superbot PR #1884 producer + websites PR #11 consumer,
2026-07-09). Indexed in `docs/ideas/README.md`.

**Fuller picture (Q-0254):** the estate keeps growing repos where repo A commits a
generated artifact (`console.json`, `site.json`, `dashboard.json`) and repo B consumes
it over a raw URL. They share an *implicit* schema — no shared CI, no shared types — so
a producer-side family/field rename silently blanks or corrupts the consumer page
(superbot's BUG-0022 desync class). The kit has zero doctrine for this seam, yet the
three-part pattern is already proven estate-side. What it is really for: give every
future adopter a named, enforceable contract discipline the moment it grows a cross-repo
committed feed, so the desync class cannot recur silently. Implied scope: this is a
doctrine graduation into templates (ORDER 048's named ladder rung), not a one-off doc.

**Classification:** buildable-now, docs/doctrine only, additive, reversible. **Size: M.**

**Recipe:**
1. Author the doctrine capturing the proven three-part pattern: (a) producer commits a
   *versioned contract file* next to the artifact (`version` + top-level families +
   guaranteed fields per record); (b) producer stamps the version into the artifact
   (`meta.schema_version`) and enforces fail-closed parity in CI (constants⇄contract,
   family whitelist both directions, per-record field whitelists); (c) consumer pins the
   contract copy it built against and runs two cheap render-time checks (version match +
   contracted families present), surfacing drift as an honest banner — never fake data.
2. Home (recommend both, in order):
   - **(a) standalone recipe** `docs/recipes/pinned-feed-contract.md` (create
     `docs/recipes/` if absent) — full pattern + the estate reference (superbot #1884 /
     websites #11) + a copy-paste contract-file skeleton. The immediately-shippable half.
   - **(b) template rider** — a short paragraph into
     `src/engine/templates/CONSTITUTION.md.tmpl` (147 lines) pointing adopters at the
     recipe: "a committed artifact consumed by another repo carries a committed,
     versioned shape contract; producer enforces fail-closed in CI; consumer pins the
     version and verifies at render time." The graduation half — every re-render carries it.
3. Files: `docs/recipes/pinned-feed-contract.md` (new); `src/engine/templates/CONSTITUTION.md.tmpl`
   (rider); flip `docs/ideas/pinned-feed-contract-doctrine-2026-07-09.md` frontmatter
   `state: promoted` (+ `shipped_pr:` on merge); update `docs/ideas/README.md` index state.
4. Tests: touching a `*.tmpl` triggers the render/adopt tests — run `python3 -m pytest tests/ -q`.
   Add a cheap test asserting the CONSTITUTION render contains the doctrine anchor string
   (mirror an existing template-content test in `tests/`). Then `python3 dist/bootstrap.py check --strict`.
5. Acceptance: a fresh `adopt` renders a CONSTITUTION carrying the pinned-feed doctrine
   pointer; the standalone recipe is reachable (docs-gate); the idea file reads `promoted`.
6. Traps: do NOT ship the heavier escalation (a template contract-FILE + parity-test
   scaffold, or an engine check that a declared feed names its contract) — the idea says
   build the doctrine note first and escalate "only if instances repeat." Doctrine-only
   this pass. Never hand-edit generated packs — edit the `.tmpl`, regenerate, verify.

---

## 2 · folded-gate diff-aware advisory checker — BUILDABLE-NOW (rank 2)

**Origin:** `docs/ideas/folded-gate-diff-aware-card-2026-07-11.md` (captured; origin
consumer superbot-next, live-verified in the v1.9.0 distribution wave). Shipped sibling:
`docs/ideas/session-gate-diff-aware-selection-2026-07-09.md` (kit PR #19).

**Fuller picture (Q-0254):** PR #19 made the engine (`check --session-log`), the kit's
own `ci.yml`, and the generated `substrate-gate.yml` PR-diff-aware. But some hosts do not
run the planted gate — they hand-FOLDED the session-gate step into their own CI
(superbot-next as a `gate` job; websites in `quality.yml`). Those host-authored copies
froze at the pre-#19 newest-by-mtime picker, so in a fresh CI checkout (flat mtimes) they
can grade a SIBLING's `complete` card instead of the PR's own in-progress one — a misgrade
in the loosening direction. The kit never regenerates host-authored workflows, so a
template change cannot fix it. What it is really for: catch the loosening misgrade at the
kit's own `check` layer (which DOES run in adopter repos) instead of relying on each host
to remember to port #19. The idea gated this on "a second occurrence" — and it has arrived:
superbot-next's `gate` job AND websites' folded `quality.yml`
(`docs/retro/2026-07-11-continuous-run-retro.md:74`) both carry the stale tail-1 picker.
The build trigger is met.

**Classification:** buildable-now, kit-side advisory `check` sub-check, additive,
reversible. **Size: S.** (Plus a cross-repo follow-on — the actual host ports — that is
NOT part of this recipe.)

**Recipe:**
1. Add an advisory check that scans `.github/workflows/*.yml` in the repo being checked
   and flags any workflow invoking the session gate (`check ... --require-session-log`, or
   the `check --strict` session-gate shape) WITHOUT passing `--session-log`/`--added-card`
   — i.e. a folded gate still relying on the mtime picker.
2. Files: new `src/engine/checks/check_folded_gate.py` (mirror
   `src/engine/checks/check_adopters_current.py` for module shape); wire it into the `check`
   aggregation (grep where `checks/check_*` are registered — `src/engine/checks/__init__.py`
   or the `check` command in `src/engine/cli.py`). Make it **advisory** (warning, never
   exit-affecting) — same tier as the claims-format / model-line advisories.
3. Tests: add a fixture workflow (folded gate lacking `--session-log`) asserting the
   advisory fires, and a clean fixture (planted gate / diff-aware) asserting it stays
   silent. `python3 -m pytest tests/ -q`; then rebuild dist and `python3 dist/bootstrap.py check --strict`.
4. Acceptance: `check` on a repo whose workflow folds the gate without diff-awareness emits
   one advisory naming the file; a repo using the planted `substrate-gate.yml` is silent.
5. Traps: keep it ADVISORY — a hard failure would redden every adopter that legitimately
   folds its gate before they can react, and would fire on the kit's OWN `ci.yml` if the
   matcher is sloppy (the kit's ci.yml passes `--session-log`, so match precisely on
   "require-session-log present AND session-log absent"). Do NOT auto-fix host workflows —
   the kit cannot regen them. The actual PORT of the diff-aware block into superbot-next's
   `gate` job and websites' `quality.yml` (copy `.github/workflows/ci.yml` lines ~302–353)
   is a **cross-repo follow-on for those repos' own lanes** — route via the fleet-manager
   inbox; not landable from substrate-kit.

---

## 3 · control-board kit-readiness cell — KIT HALF DONE → cross-repo websites recipe (rank 3)

**Origin:** `docs/ideas/control-board-kit-readiness-cell-2026-07-09.md` (captured;
consumer menno420/websites#31).

**Fuller picture (Q-0254):** the fleet control-plane board (websites-rendered view over
each repo's `control/status.md`) has no cell answering the coordinator's two per-adopter
questions: which kit version, and is it ready. The idea explicitly routes as "kit side
ships with ORDER 003; then travel to websites." **ORDER 003 shipped:** `docs/adopters.md`
exists (per-repo `kit:` self-report column) and the
`kit: v<X.Y.Z> · check: green|red · engaged: yes|no` line is a first-class template
feature (`src/engine/templates/control-README.md.tmpl:154-185`), with engine support in
`cli.py`, `render.py`, and `currency.py` (the fleet kit-currency scanner owning
`docs/adopters.md`). So from substrate-kit there is **zero remaining work**.

**Classification:** kit-side COMPLETE. Remaining = a cross-repo `websites` feature,
self-startable in that repo's lane (decide-and-flag, no owner decision needed). Not dead,
not kit-buildable. **Size (websites side): S.**

**Recipe (for the websites lane — route via the fleet-manager inbox):**
1. In the websites `review/` service status-card parser (already splits heartbeat
   `key: value` lines), add `kit:` extraction.
2. Render a three-state badge per repo row: green (`check: green` + `engaged: yes`), red
   (any red / no), absent (no `kit:` line = a pre-ORDER-003 adopter — render honestly,
   never fake).
3. Test: a fixture `status.md` with and without the `kit:` line asserts version + badge vs
   the absent state.
4. Acceptance: the board shows, per adopted repo, the last self-reported kit version + a
   readiness badge, with "absent" honest for non-upgraded repos.
5. Traps: cross-repo — not landable from substrate-kit; confirm the exact file paths in the
   websites repo (`review/` service). No new access path — the board already reads status
   files (KF-2-clean).

---

## 4 · t5-headless-guard — OWNER-GATED + cross-tree (rank 4)

**Origin:** `docs/ideas/t5-headless-guard-surface-2026-07-09.md` (captured; B1 record
session, runs 2026-07-09-run01/run02).

**Fuller picture (Q-0254):** T5's precondition says the session-log gate + Stop hook are
LIVE, but the bench sessions run HEADLESS — the `.claude/` hook layer never engages, so
guard-fire/obey/repair items are all n/a in both arms; the run only shows that,
unenforced, ON behaves exactly like the unguarded OFF baseline. Run-2 reconfirmed it and
surfaced an adjacent hole: the one headless guard surface (`check --strict`) exits 0 after
a cardless T5 session because the last-card rule is satisfied by a previous `complete`
card — a session that skips its card is invisible whenever any prior complete card exists.
What it is really for: make T5 actually able to score the guard probe. Two shapes (decide
at fix time): (1) run T5 arms through a harness that honors `.claude/settings.json` hooks,
or (2) redesign T5 around check-driven guards that exist headless.

**Why not buildable-now here:** the fix touches `bench/tasks/T5.md` and/or
`bench/README.md` / `run_ab.py` — **`bench/tasks/` is a PIN PATH**, so a T5 text change
must ride a `do-not-automerge` owner-review PR (`check_bench_integrity.py` rule 1). And the
`bench/` tree is **not in the substrate-kit checkout** — it is the kit-lab harness — so the
primary artifact is not even in this repo. The one ordinary-lane sliver (an engine-side
last-card freshness fix in `src/engine/checks/`) is likely already covered by the shipped
`--require-session-log` anchor (#19), so it may be moot; verify before building.

**Classification:** OWNER-GATED (pin-path, do-not-automerge) + cross-tree (kit-lab).
Six-field below. Not landable from here.

**⚑ FOR OWNER — six-field:**
- **WHAT:** fix the T5 bench probe so it produces a real in-session guard fire in the ON
  arm. Recommend **shape 2 (check-driven guards)** — needs no hook-honoring harness rebuild
  and the enforcement surface exists headless.
- **WHERE:** kit-lab repo, `bench/tasks/T5.md` (PIN PATH) + `bench/README.md` / `run_ab.py`;
  optional engine sliver `src/engine/checks/` (substrate-kit) for the last-card freshness
  anchor — verify it is not already covered by #19's `--require-session-log`.
- **HOW:** shape 2 — the arm's protocol runs `check --strict` inside the session flow (or a
  wrapper fails the task on red) so the guard's fire/obey/repair arc is observable without
  the hook layer.
- **WHY:** without it, T5 scores all guard items n/a — the ON arm demonstrates nothing over
  the unguarded baseline; the guard-probe purpose of T5 is unmet.
- **UNBLOCKS:** a T5 run that scores guard fire/obey/repair met/not-met instead of n/a;
  closes judge report §5.5 item 2.
- **VERIFY:** a T5 run produces ≥1 real in-session guard fire (or a recorded deliberate
  violation) in the ON arm.
- **RISK:** ⚠️ pin-path change → must land via a `do-not-automerge` owner-review PR in
  kit-lab; not landable from substrate-kit.

---

## Baton retarget

`control/status.md` Next-2 / baton now points here, ranked:
1. **pinned-feed-contract doctrine** (buildable-now, M) — graduate into `docs/recipes/` +
   a `CONSTITUTION.md.tmpl` rider.
2. **folded-gate advisory checker** (buildable-now, S) — second-occurrence trigger met; add
   the advisory `check` sub-check.
3. **readiness cell** — kit half DONE; route the websites board-render recipe to the
   websites lane via the fm inbox.
4. **t5-headless-guard** — owner-gated (pin-path, do-not-automerge) + cross-tree (kit-lab);
   six-field ⚑ above.
