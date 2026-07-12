# 2026-07-12 — wave A: v1.13.0 distribution (registry rows 1–3, 5–6)

> **Status:** `complete`

- **📊 Model:** fable-5 · high · distribution-wave

## Scope (what is about to happen)

Distribution Wave A: upgrade 5 vendored adopters to v1.13.0.

The five wave-A targets, in `docs/adopters.md` registry order (first five
vendored adopters, superbot skipped — deliberate v1.0.0 pin):

- **menno420/substrate-kit** (row 1) — verify no-op: `dist/bootstrap.py` at
  HEAD already reads v1.13.0 (release #266/#267); re-verify sha vs the
  release asset.
- **menno420/superbot-next** — vendored v1.12.1 → v1.13.0.
- **menno420/websites** — vendored v1.12.1 → v1.13.0.
- **menno420/superbot-games** — vendored v1.12.1 → v1.13.0.
- **menno420/trading-strategy** — vendored v1.12.1 → v1.13.0.

Per-target procedure: the `upgrade-distribution` playbook skill (kit PR
#265) — preflight hard-reset, release download, sha256 three-way compare,
banked rollback verify, carve-out scan, born-red PR per target,
tree-verified merge. Wave B (gba-homebrew, pokemon-mod-lab, venture-lab,
fleet-manager) runs in parallel; this lane touches only its own wave-A rows
at close-out. Lane claim: `control/claims/wave-a-v1130.md`.

This card opens the PR born-red by design (session gate HOLD); the 💡 idea
and ⟲ review sections below are stubs to be filled at flip time.

## Close-out

All five wave-A rows verified at v1.13.0 (upgrade workers' results, cited):

- **substrate-kit (row 1):** verified no-op — `dist/bootstrap.py` at tag
  v1.13.0 / release close-out 2aa0a5b sha256
  `982b2667b2158aa77639fd44bca72ab8e047fb3bdabbde580937dd1325730959`
  (735,972 B) == the release asset, KIT_VERSION 1.13.0. Current main's dist
  differs only by the unreleased post-release #270 regen (grounded-skills
  slice 3), still KIT_VERSION 1.13.0 — expected, not drift.
- **superbot-next:** PR #251, merged **559a0d8** — sha256 3-way ✔, bank ✔,
  carve-outs none (10 consumer-edited, nothing to apply). Tree-verified;
  final head 11/12 green (`report` born-red by design, not required).
  `--apply-docs` applied CONSTITUTION.md + AGENT_ORIENTATION.md (the ORDER
  015 dead boot-pointer fix landed); docs/SKILLS.md replanted.
- **websites:** PR #164, merge commit **263f63b** — sha256 3-way ✔, bank ✔,
  carve-outs none (2 diverged docs handled/preserved). Quality run
  29191726237 success. Exact-pin test bumped to 1.13.0; AGENT_ORIENTATION
  SKILLS.md wiring hand-merged; CONSTITUTION.md delta left lane-owed
  (preserved at `git show 263f63b:.substrate/upgrade-report.md`).
- **superbot-games:** PR #62, squash merge **93b739a** — sha256 3-way ✔,
  bank ✔, carve-outs none (scan ran, 0 found). Gate run 29191737360 + tests
  run 29191737361 success. Replanted docs/SKILLS.md fired a real
  `[reachable]` orphan red; fixed via the report's AGENT_ORIENTATION manual
  merge (dead pointer `.claude/CLAUDE.md` → `CONSTITUTION.md`), which also
  closed the outstanding v1.12.0 AGENT_ORIENTATION delta.
- **trading-strategy:** PR #72, squash merge **8cc0208** — sha256 3-way ✔,
  bank ✔, carve-outs none (0 found, both workflows). Gate run 29191678228 +
  pytest run 29191678269 success. AGENT_ORIENTATION diverged delta
  hand-merged. NOTE: this repo now has a LIVE auto-merge enabler (installed
  post-#63 by its PR #65) that armed on the wave PR — its "auto-merge OFF"
  reputation is stale.

**Wave-level findings:** the release asset (sha256 `982b2667…0959`,
735,972 B) downloaded clean first try on all four repos; every repo banked
exactly one new `bootstrap-1.12.1.py` (sha256 `1055ca2c…e4aa`) with
pre-existing banks byte-identical. v1.13.0 is the FIRST wave with the
`template-improved`/`diverged` report classes — upgrade is now a two-command
affair (`upgrade` then `upgrade --apply-docs`) — and the replanted
docs/SKILLS.md reds `check --strict` with a `[reachable]` orphan on any
diverged-orientation repo until the AGENT_ORIENTATION delta is hand-merged
(hit 3/4: websites + superbot-games + trading-strategy; superbot-next's was
consumer-untouched so `--apply-docs` handled it).

**Adopters regen (runbook §6, owed to this lane):** `python3
dist/bootstrap.py currency` regenerated `docs/adopters.md` — 10 repos
scanned, all five wave-A rows read tree **v1.13.0**. DRIFT rows are the
chronic self-report heartbeat-lag class plus the kit's own deliberate
tree-internal pin row (v1.0.0 config pin vs v1.13.0 dist — the §7 question).
Wave-B repos (gba-homebrew, pokemon-mod-lab) scanned at v1.12.1 — their
parallel lane owns those rows and regens again at its own close-out.

**Close-out mechanics:** merged origin/main into the branch (absorbed the
grounded-skills slice 3 #270/#271 — clean, no conflicts), recorded ⚑ WAVE A
v1.13.0 DONE in `control/status.md` (phase + blockers claim note +
next-queue parenthetical + notes line; wave-A scope only — wave-B rows,
pin-PR notes #220/#238, and other lanes' text untouched), deleted
`control/claims/wave-a-v1130.md`, flipped this card.

## 💡 Session idea

`upgrade` should predict-and-prescribe the docs/SKILLS.md `[reachable]`
orphan red it just introduced: at plant time it already knows whether the
repo's AGENT_ORIENTATION.md is classified `diverged` (i.e. `--apply-docs`
will NOT wire the SKILLS.md pointer in), so it can print a paste-ready
fix-it hint — "docs/SKILLS.md was planted but AGENT_ORIENTATION.md is
diverged; `check --strict` will red with a [reachable] orphan until you
hand-merge this line: <the exact pointer line from the template>". This
wave hit that red on 3 of 4 adopters, and each worker independently
re-derived the same fix from the upgrade report; the tool had every fact
needed to emit the fix as one line.

## ⟲ Previous-session review

The v1.13.0 release session (#266/#267): the runbook's sixth consecutive
clean exercise — premise verified, three-way sha256 verified at the cut,
claim/bump/close-out phases each cited. What it could have done better: the
release shipped the first `template-improved`/`diverged` report classes and
the replanted docs/SKILLS.md, but its close-out record carried no
"distribution impact" note — so the wave discovered the two-command upgrade
sequence and the predictable SKILLS.md orphan red live, on 3/4 repos, in
parallel. Concrete improvement: release runbook §5/§6 should add a cut-time
"what distributors will see" line whenever a release introduces new report
classes or planted docs, so the wave prompt inherits the expectation instead
of each worker rediscovering it.

## ⚑ FOR MANAGER (non-kit, lane-owed observations from the wave)

- **websites:** CONSTITUTION.md template delta left lane-owed (preserved at
  `git show 263f63b:.substrate/upgrade-report.md`).
- **trading-strategy:** stale-doc reputation — any note saying its
  auto-merge is OFF is wrong since its PR #65; the live enabler armed on
  this wave's PR #72.
- Heartbeat `kit:` bumps remain lane-owed across the wave repos (chronic
  self-report class, Q-0261.3; ownership ruling still open).
