# Session · 2026-07-16 · release-v1-18-0-closeout

> **Status:** `complete`

Intent: runbook §6 aftermath for the v1.18.0 cut (same worker session as the #418 bump PR; its card is `.sessions/2026-07-16-release-v1-18-0.md`) — release record on the heartbeat, `docs/adopters.md` currency regen, claim delete. This card exists because this PR touches `docs/adopters.md`, so it takes kit-quality's full lane (session card required in the merge-base diff), not the control fast lane the pure-control close-outs (#276, #291 class) rode.

- **📊 Model:** Claude Fable · medium · review/verify (release close-out)
- ⚑ Self-initiated: no — runbook §6 aftermath of the baton-named S5 release cut.

## What shipped (PR #419)

- `control/status.md` wholesale heartbeat with the RELEASE RECORD: v1.18.0 · `release.yml` run 29466068874 (workflow_dispatch, success) · tag object cd4f84281925 → commit 4c8e1d1f6141 (#418 squash-merge) · sha256 `d83a8a29bce90188ac4a6d01ebbfe1190e4568a85d12c63e7dbd23d9a5eef6c1` three-way PASS via `scripts/verify_release.py` (tag + sha256 legs PASS; workflow leg SKIPPED on the known proxy 403 — run watched green via GitHub MCP, disclosed).
- `docs/adopters.md` regenerated (`dist/bootstrap.py currency`): all adopter rows stale v1.17.0 < v1.18.0 as expected post-cut; kit's own DRIFT row is the known mid-close self-heal; NEW: superbot-games also reports DRIFT (tree vs self-report) — recorded for the manager sweep, not chased (adopter repos read-only).
- Claim `control/claims/release-v1.18.0.md` deleted (cycle closed).
- Retro-fix on the #418 card's `📊 Model:` line: task-class `release cut` → `mechanical refactor (release cut)` — the `model-line-class` advisory fired on the first kit-quality run of this PR (`release cut` prefix-matches no PL-004 class); same sanctioned repair class as the #390 sweep.
- Red round-trip, cause + fix: kit-quality run 29466263869 held this PR red — `--require-session-log` found no card in the merge-base diff (this PR initially shipped card-less on the assumption non-card PRs skip the gate; that is true only for the `control/**`-only fast lane, and `docs/adopters.md` takes the full lane). Fix: this card.

## 💡 Session idea

Add one release-agnostic line to `ADOPTER_CHECKLIST` in `src/build_release_json.py` — e.g. step 1.5: "Read this release's **Added** section above: `upgrade` plants any new verbs/templates it names (they work immediately after step 1, no extra install)". The S5 plan wanted a "release-notes line in the adopter upgrade checklist" for the archive-ready surface; a version-specific line would pollute every future release's notes (the checklist is deliberately release-agnostic, "enforce, don't exhort"), but a generic pointer line satisfies the same intent for THIS and every future capability wave — adopters stop learning about newly planted verbs only by diffing their tree. Dedup: `docs/ideas/upgrade-checklist-release-json-placement-2026-07-09.md` (shipped #92) touched the same constant for a different clause; no what's-new/Added-pointer idea exists (grepped `checklist`, `adopter`, `release-notes`).

## ⟲ Previous-session review

Reviewing the bump half of this same wake (PR #418): the cut itself was clean — the runbook + `cut_release.py` + `verify_release.py` mechanization carried a ninth consecutive verified release, and the pre-cut payload sweep caught a real gap (#386's missing entry). Two self-inflicted costs, both card-grammar shaped: the invented task-class `release cut` (the taxonomy is nine fixed classes; the advisory caught it) and the card-less close-out PR (one full red CI round-trip). Workflow improvement, concrete: the release runbook §6 should say "the aftermath PR touches `docs/adopters.md`, so it needs a session card — only pure-`control/**` PRs ride the fast lane", one line that converts this session's paid lesson into the next cutter's checklist; the team-memory release recipe should carry the same line.
