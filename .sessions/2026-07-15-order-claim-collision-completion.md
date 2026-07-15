# 2026-07-15 · order-claim-collision-completion

> **Status:** `complete`

- **📊 Model:** Fable (Claude 5 family) · medium · docs+drift-fix
- Scope: baton item 2 — complete the cross-branch ORDER-collision idea
  (docs/ideas/order-claim-cross-branch-collision-2026-07-14.md). One PR
  (#397), docs-only.

About to (opening declaration, retained): complete the cross-branch
ORDER-collision baton item — the #365 mechanism (claim `--order` segment +
`claims-order-collision` advisory + verb refusal) shipped 2026-07-14 but
three doc segments never landed: the idea lifecycle flip (frontmatter still
`captured` / `shipped_pr: null` — drift, fix on sight), the local
`control/claims/README.md` lagging the shipped template, and the idea's
part 3 — the lab-loop prompt STEP 2 claim-the-ORDER-before-building line.

## Record

- Boot: hard-synced to origin/main 311841d (#396); inbox tops at ORDER 024
  (all acked+done per the heartbeat orders line; the "ORDER 025" text at
  ~line 210 verified as the fm relay inside ORDER 019, not a new order);
  control/claims/ held README only; zero open PRs at the ~15:5xZ scan;
  `currency --check` exit 0 (registry current, 12 repos) — no regen slice
  due, so the baton-named idea was the slice. Born-red card + claim
  (written by the `bootstrap claim` verb itself — dogfood) = first commit
  7d7f00e; PR #397 opened READY immediately after.
- Finding that re-scoped the slice: PR #365 (merged 2026-07-14) had
  already built the idea's parts 1–2 (grammar segment `WORK_CLAIM_ORDER_RE`
  / `work_claim_order_ids()`, `claim --order NNN` with round-trip verify +
  cross-branch refusal, `check_claims` `claims-order-collision` advisory)
  — but never flipped the idea file, never synced the local claims README,
  and never landed part 3. So the honest remaining work was the doc
  completion, recorded as such everywhere (shipped_pr: 365 carries the
  mechanism; #397 carries the doc segments).
- Shipped (fa118d7): (1) idea frontmatter flip `promoted` / `shipped_pr:
  365` / `merged_date: 2026-07-14` / `outcome: shipped` + prose State +
  the "Why now / cost" Next→Shipped rewrite; README index row Backlog →
  Shipped (window closes 2026-08-13). (2) control/claims/README.md synced
  to control-claims-README.md.tmpl: the `[--order NNN]` verb line + the
  "Serving an inbox ORDER? Pass `--order NNN`" paragraph + the
  `claims-order-collision` advisory row — a live instance of the
  template↔local-copy lag class (now baton item 2 as a groom target with
  this evidence). (3) lab-loop STEP 2 CLAIM-BEFORE-BUILD line (scan
  control/claims/ at HEAD, claim with `--order NNN` before consuming an
  ORDER — the #362/#363 twin-build lesson); console re-paste of the fenced
  prompt pending post-merge per the file's change discipline, noted on the
  heartbeat.
- Verify (at fa118d7): `python3 scripts/preflight.py` → 8/8 legs green
  (pytest 1608 passed, 1 skipped; dist-byte-pin; ruff; idea-index;
  retro-index; changelog-structure; program-law; bench-integrity).
  `dist/bootstrap.py check --strict` → designed born-red HOLD only (this
  card, pre-flip) + known staged-regen-lag ×3. Guard-fires telemetry
  deltas committed per the checker instruction.

## Session enders

- 💡 Session idea: **idea-flip-lag advisory in check_idea_index.** This
  wake's drift class, made mechanical: a Backlog idea (state
  `captured`/`groomed`) whose filename is named as *built* by a merged
  main commit subject/body (the #365 commit literally says "Builds
  docs/ideas/order-claim-cross-branch-collision-2026-07-14.md") sat
  unflipped for a day and cost a wake's re-discovery. New advisory leg:
  for each non-shipped idea file, grep `git log origin/main --grep
  <basename>` for build-verb subjects ("Builds"/"Building"/"ships") and
  warn `idea-flip-lag: <file> named as built by <sha> but frontmatter
  still captured`. Self-skips on shallow clones exactly like the existing
  merged-reality leg (same history caveat, same home). Dedup: no
  docs/ideas/ file mentions flip-lag/unflipped; check_idea_index's
  merged-reality leg verifies the OPPOSITE direction (shipped claims are
  real), not captured-but-built.
- ⟲ Previous-session review (2026-07-15-adopt-lane-drift-advisory, #396):
  a clean engine slice — honest edit-lesson recording (the split-assert
  local red) and a genuinely useful decide-and-flag on the upgrade-path
  advisory. The gap it surfaces: its refreshed baton named this idea as
  the next *buildable* item without checking whether the mechanism already
  existed — a two-line `git log --grep <idea-basename>` would have found
  #365 and re-scoped the baton line to "doc completion" up front, saving
  this wake's re-discovery. That check is exactly this session's 💡 above,
  filed so the class gets a mechanical answer rather than a habit.
