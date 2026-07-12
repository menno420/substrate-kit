# 2026-07-12 — Wave B: v1.13.0 distribution to the last four adopters

> **Status:** `in-progress`

- **📊 Model:** fable-5 · medium · distribution-wave

## Scope (what is about to happen)

Wave B of the v1.13.0 distribution (tag v1.13.0, annotated eb5edd0 →
828e450, release run 29191006519, asset sha256
`982b2667b2158aa77639fd44bca72ab8e047fb3bdabbde580937dd1325730959`,
735,972 B — download + release.json field verified this session; matches
the committed-dist hash at the bump SHA, three-way ✔).

Registry order (docs/adopters.md, generated 2026-07-11T22:36:49Z; superbot
excluded — owner-held v1.0.0 pin-only row): Wave A = first five, Wave B =
LAST FOUR: **gba-homebrew · pokemon-mod-lab · venture-lab · fleet-manager**
(all four trees at v1.12.1 → v1.13.0).

Recipe: the `upgrade-distribution` skill (kit PR #265) per adopter — stage
the verified asset as `bootstrap.py.new` + `release.json` in each adopter
root → `python3 bootstrap.py.new upgrade` (verify the banked
`bootstrap-1.12.1.py` rollback) → carve-out scan read → per-repo verify +
`check --strict` → born-red card PR per adopter, merged on green,
tree-verified afterward.

Kit-side this PR touches ONLY this card + the wave-B claim file
(`control/claims/claude-wave-b-v1130.md`). NO engine/dist/src changes;
NEVER `control/inbox.md`, `bench/`, or pin PRs #220/#238; heartbeat `kit:`
bumps stay lane-owed per Q-0261.3; adopters regen (currency) belongs to the
wave close-out slice, not this card's first commit.

This card opens the PR born-red by design (session gate HOLD); the 💡 idea
and ⟲ review sections below are stubs to be filled at flip time.

## Close-out

Per-repo outcomes (all four verified on merged main):

- gba-homebrew: v1.12.1 → v1.13.0 · sha256 3-way ✔ · bank ✔ · carve-outs:
  5 consumer-edited, 0 diverged · PR #67 merged @ e09a297 · CI runs
  29192159136 + 29192159100 green · tree-verified ✔ (`--apply-docs`
  applied the ORDER 015 pointer fix + SKILLS.md wiring)
- pokemon-mod-lab: v1.12.1 → v1.13.0 · sha256 3-way ✔ · bank ✔ ·
  carve-outs: 5 consumer-edited, 0 diverged · PR #54 merged @ 03309d6 ·
  CI runs 29191675960 + 29191675931 green · tree-verified ✔
  (`--apply-docs` cleared the SKILLS.md orphan)
- venture-lab: v1.12.1 → v1.13.0 · sha256 3-way ✔ · bank ✔ · carve-outs:
  5 consumer-edited, 0 diverged · PR #64 auto-merged (repo enabler,
  squash) @ 2bad7c1 · CI 29191693264/29191693257 green · tree-verified ✔
- fleet-manager: v1.12.1 → v1.13.0 · sha256 3-way ✔ · bank ✔ ·
  carve-outs: 6 (5 consumer-edited + 1 diverged AGENT_ORIENTATION) ·
  PR #114 merged @ 791772f · CI 29191670012 + 29191670005 green ·
  tree-verified ✔ (minimal SKILLS.md hunk hand-merged into the diverged
  AGENT_ORIENTATION, rest lane-owed)

All four heartbeat `kit:` bumps left lane-owed per Q-0261.3.

Wave-B findings:

1. **SKILLS.md orphan — both variants fired this wave.** The replanted
   `docs/SKILLS.md` reds `check --strict` on a fresh v1.13.0 upgrade in
   two shapes: the plain orphan (pokemon-mod-lab — cleared by
   `--apply-docs`) and the dead-pointer + missing-wiring shape
   (gba-homebrew — `--apply-docs` applied the ORDER 015 pointer fix +
   SKILLS.md wiring). A fresh v1.13.0 upgrade is guaranteed strict-red
   until `upgrade --apply-docs` runs — the two-command upgrade
   (`upgrade` then `upgrade --apply-docs`) is mandatory doctrine, not an
   optional follow-up.
2. **venture-lab landing-path change.** Its auto-merge enabler is LIVE
   and squash-merged the wave PR (#64) on green — the old
   "merge via MCP merge-commit" path recorded for that repo is STALE.
3. **gba-homebrew `guard-fires.jsonl` union-merge conflict.** The wave
   PR conflicted cross-PR on the append-only guard-fires.jsonl;
   resolved as a clean union in-lane. Idea filed below (merge=union
   gitattribute) to end the class.

Kit-side close-out (this PR #269): merged origin/main (wave A's #268)
into the branch clean; re-ran `python3 dist/bootstrap.py currency` — the
gba-homebrew + pokemon-mod-lab rows (still v1.12.1 at wave A's regen)
now read tree v1.13.0; all four wave-B rows current (DRIFT rows = the
chronic self-report heartbeat-lag class + the kit's deliberate
tree-internal pin row). control/status.md wave-B section recorded
surgically; wave-b-v1130 claim deleted in the flip commit.

## 💡 Session idea

Make the two-command upgrade self-driving: `upgrade` should either
auto-run the docs pass when it detects template-improved/diverged
deltas, or at minimum print a loud terminal hint — "N template deltas
staged; run `bootstrap.py upgrade --apply-docs` now, `check --strict`
will fail until you do" — as its last line. Evidence: v1.13.0 is the
first release where a fresh upgrade is *guaranteed* strict-red until
`--apply-docs` (replanted docs/SKILLS.md), and the orphan fired on all
four wave-B repos (both variants) plus 3/4 of wave A. Every future wave
pays the red→diagnose→apply-docs loop per adopter until the pairing is
automatic. Related, smaller: plant a `merge=union` gitattribute for
append-only JSONL evidence files (guard-fires.jsonl) at adopt/upgrade —
the gba-homebrew cross-PR conflict is a class, not an instance.

## ⟲ Previous-session review

Wave A (#268) ran the same recipe cleanly and its close-out regenerated
adopters.md promptly — but its regen necessarily froze our two
still-in-flight rows at v1.12.1, which this close-out had to re-run;
workflow improvement: when two waves run in parallel, the runbook §6
regen belongs to whichever close-out lands LAST (or should be re-run by
it, as here) — a one-line note in the release runbook would make that
explicit instead of discovered.
