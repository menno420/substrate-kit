# 2026-07-15 · heartbeat-delegated-tally

> **Status:** `complete`

- **📊 Model:** Fable (Claude 5 family) · medium · docs-only
- Scope: baton item 2 — the delegated-tally heartbeat doctrine (idea
  docs/ideas/heartbeat-delegated-tally-guidance-2026-07-13.md, consumer
  origin: the mineverse "COORDINATOR-DELEGATED heartbeat write" precedent,
  night-run report §f). Docs/template only, one PR (#395).

About to (opening declaration, retained): name the coordinator
delegated-tally heartbeat convention (member-repo pointer line +
"COORDINATOR-DELEGATED heartbeat write" marker) and the sweep guidance
(classify by PR record + coordinator status, never seat-heartbeat staleness
alone) in the control README/status templates and the kit's own
control/README.md; flip the idea's lifecycle.

## Record

- Boot: hard-synced to origin/main 0d33d55 (#394); inbox tops at ORDER 024
  (all acked+done per the heartbeat orders line); control/claims/ held
  README only; zero open PRs at the ~14:4xZ scan; `currency --check` exit 0
  (registry current, 12 repos) — no regen slice due, so the baton-named
  idea was the slice. Born-red card + claim = first commit 0546c08; PR #395
  opened READY immediately after.
- Shipped (84ea511): new "Delegated tally — coordinator-written heartbeats"
  section in `src/engine/templates/control-README.md.tmpl` and mirrored in
  the kit's own `control/README.md` — (1) the marked delegated write (the
  `COORDINATOR-DELEGATED heartbeat write …` line, first line after
  `updated:`; one-writer-per-file preserved as one writer *at a time*);
  (2) the member repo's standing `notes:` pointer to where its live tally
  lives; (3) the sweep rule: classify a seat by PR record + coordinator
  status, never by seat-heartbeat staleness alone (stale + pointer =
  healthy delegated lane; stale + no pointer + no PRs = the real dark-lane
  signal). `control-status.md.tmpl` seed notes gain a one-line pointer to
  the section. Idea lifecycle flipped (frontmatter state promoted /
  shipped_pr 395 / outcome shipped + README Backlog → Shipped), CHANGELOG
  [Unreleased] ### Added entry, dist byte-pin regen.
- Grammar lesson (cost: one local red, fixed pre-push): idea frontmatter
  has no `state: shipped` — the valid vocabulary is
  captured/routed/promoted/historical with `outcome: shipped` carrying the
  ship fact (check_idea_index [bad-state] + [outcome-inconsistent] fired on
  first preflight; matched the #394 exemplar and went green).
- Verify (at 84ea511): `python3 scripts/preflight.py` → 8/8 legs green
  (pytest 1604 passed, 1 skipped; dist-byte-pin; ruff; idea-index;
  retro-index; changelog-structure; program-law; bench-integrity).
  `dist/bootstrap.py check --strict` → designed born-red HOLD only (this
  card, pre-flip) + known staged-regen-lag ×3. Guard-fires telemetry delta
  committed with the heartbeat (14fc2c2).

## Session enders

- 💡 Session idea: **template↔local-copy sync advisory.** The kit's own
  rendered copies of planted docs (e.g. `control/README.md`) and their
  templates (`src/engine/templates/control-README.md.tmpl`) are hand-synced
  and verifiably diverged (observed live this session: the local copy
  carries an "Enforced vs. convention" block the template lacks, and
  per-lane wording differs) — every doctrine edit must land twice by hand,
  and a miss ships adopters a different contract than the kit itself runs.
  A cheap advisory (compare `## ` section-heading sets between each
  template and its kit-local rendered counterpart, advisory-only) would
  catch a doctrine section present in one but not the other. Dedup-grepped
  docs/ideas/ (`template.*sync|drift`, `local copy`): no existing capture.
- ⟲ Previous-session review (2026-07-15-model-line-unrecorded-marker, PR
  #394): strong slice — it shipped the engine carve-out with the harvest
  behavior test-pinned AND used the new mechanism immediately on the #393
  malformed card (fix-on-sight rider, properly flagged), so the feature
  arrived with its first live proof. Its card also recorded the
  `bootstrap claim --scope` backtick refusal it hit — which this session
  benefited from by writing the claim file directly. Improvement it
  surfaces: the frontmatter grammar (`state:` vocabulary vs `outcome:`)
  is only discoverable via checker error or exemplar-matching — a one-line
  grammar comment atop docs/ideas/README.md's Backlog section (like the
  decisions.md grammar comment) would have saved this session's red
  preflight round; folded into the session idea's family but small enough
  to ride any docs slice.
