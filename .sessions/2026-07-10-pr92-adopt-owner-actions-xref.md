# 2026-07-10 — gen-2: adopt orphaned #92 + OWNER-ACTION ↔ CAPABILITIES cross-reference advisory (queue item 8)

> **Status:** `complete`

- **📊 Model:** claude-fable-5 · high · adopt+engine (adopt PR #92, then one scoped
  checker PR: the OWNER-ACTION ↔ CAPABILITIES cross-reference advisory)

## Scope (as declared)

Adopt the orphaned PR #92 (queue item 10, four upgrade-UX fixes — READY, CI green,
behind main, no claim; status.md hands off the branch update): merge origin/main into
its branch, resolve the docs/ideas/README.md conflict (both #92 and #95 restructured
it), land it. Then build queue item 8: an advisory checker cross-referencing
⚑ OWNER-ACTION items in control/status.md against docs/CAPABILITIES.md, mirroring
check_claims.py's advisory posture (warns, never fails the strict gate). Claimed on
`control/status.md` via PR #97 (`claimed-by: pr92-adopt+queue-item-8 kit-lab-gen2
2026-07-10T04:11:37Z`). No pin paths; `control/` writes only in the claim (#97) and
the final status close.

## What shipped

1. **#92 adopted and MERGED** (squash `d8a95cc`). The branch was 4 merges behind
   main with one real conflict: `docs/ideas/README.md` — #92 flipped its three
   upgrade-* ideas to the Shipped section while #95 had restructured the same
   section with its own three shipped entries. Resolved as the coherent union
   (#92's three entries, then #95's three, matching the section's conventions;
   each idea file appears exactly once). `dist/bootstrap.py` auto-merged and the
   byte-pin was re-verified after the merge (green — no regeneration needed).
   Merge commit `a641a05` on the #92 branch; auto-merge was already armed by the
   enabler at PR open and fired on green. #92's own session card untouched (it is
   the previous session's record).
2. **Queue item 8 — `check_capability_xref`** (this PR): the #68 card's 💡 idea
   built faithfully. Every wall-shaped ⚑ OWNER-ACTION (VERIFIED-NEEDED citing
   403 / access-denied / owner-only evidence) is token-matched against the
   `docs/CAPABILITIES.md` Walls/Capabilities sides (section headings + tagged
   append-log entries). Advisory-only, never exit-affecting (the `check_claims`
   posture, wired at the same cmd_check registration point, both CI lanes):
   `owner-ask-wall-unrecorded` (cited wall nowhere in the ledger → append it,
   THE DISCOVERY RULE step 4) and `owner-ask-capability-resolved` (only the
   verified-working side matches → the wall may have fallen; re-verify or
   withdraw). Judgment-shaped asks (product/owner judgment, "not a technical
   wall") are out of the ledger's scope and skipped. 16 new tests mirror
   `tests/test_check_claims.py` (gating, fail-open, both findings, wall-side
   precedence, cmd_check integration: strict stays green, both lanes warn,
   quiet-when-clean). MODULE_ORDER + dist regenerated; CHANGELOG [Unreleased]
   ### Added entry (MINOR: new checker).

Field verification: run against this repo's own `control/status.md` (10 live
OWNER-ACTION items) the checker is **quiet** — the 3 judgment asks (1, 5, 8) skip
and all 7 wall-shaped asks match recorded walls, i.e. this repo's ask↔ledger loop
is already closed, which is exactly the clean baseline the nudge is for.

## Gates (final head, run in the session worktree)

- `python3 -m pytest tests/ -q` → **795 passed** (779 post-#92 + 16 new)
- `python3 dist/bootstrap.py check --strict` → exit 0
- `python3 src/build_bootstrap.py && git diff --exit-code dist/bootstrap.py` →
  byte-pin green
- `python3 -m ruff check src/engine/` (CI's exact scope) → all checks passed

## Run report

### ⚑ Flags

1. **⚑ Self-initiated: CHANGELOG entry** — #90 (the posture precedent) shipped its
   checker without a CHANGELOG line, but the file's own header says MINOR = "new
   checker", so this one carries an [Unreleased] ### Added entry; flagged because
   it goes one step beyond mirroring #90.
2. **⚑ Coarseness disclosed:** the cross-check is distinctive-token overlap, not
   semantics — false nudges are possible by design and the docstring says so; the
   advisory posture is the containment.

### 💡 Session idea (dedup-checked against docs/ideas/ + roadmap)

**CAPABILITIES.md append-log format advisory.** The append-log tag vocabulary
(`wall` / `capability` / `wall+recipe`) just became load-bearing: `check_capability_xref`
routes each entry to the wall or working side BY its tag, but nothing validates the
entry grammar (`- YYYY-MM-DD · tag · finding · evidence · workaround`) — a malformed
or missing tag silently lands evidence on the wrong side of the cross-reference. A
tiny advisory (same posture family) that flags unparseable append-log entries keeps
the ledger machine-readable now that a checker consumes it. No existing
`docs/ideas/` file covers the ledger's format.

### ⟲ Previous-session review (`.sessions/2026-07-10-run2-ordinary-followups.md`)

Genuinely strong: the `handoff.py` `_marker_miss` ripple was fixed at the root (the
string-shaped seam), its 💡 idea named that exact seam class, and its status-close
handoff (`next:` naming #92 as behind-main with the precise remedy "merge origin/main
into the branch + push") is what let this session adopt #92 without any re-derivation
— the conveyor working twice in a row. What it could have done better: it *described*
the orphaned-#92 remedy but left ownership at "whichever session owns that lane",
when that lane's session was already closed — a READY+green+claimless PR has no
owner by definition. **Workflow improvement:** add one line to the control/README
claim ritual: an orphaned PR (READY, green, no live claim, behind main) is itself a
claimable work item — claim `prNN-adopt` before touching the branch, exactly the
shape this session used via #97; that turns tonight's ad-hoc pattern into the
convention.

### Docs audit

Everything in a durable home: checker + tests + cli wiring + MODULE_ORDER in
engine/dist (byte-pinned); release note → CHANGELOG [Unreleased] ### Added;
provenance → this card + the checker docstring (the idea's origin, the #68 card, is
quoted there); #92's ideas-README flip landed with #92 itself; telemetry —
`.substrate/guard-fires.jsonl` untouched this session (no strict-gate fire in the
worktree; CI's own runs write theirs). `docs/current-state.md` deliberately
untouched — #90 (the checker precedent) did not ledger itself there either; the
status close records both ships on the bus. `docs/gen2/queue-state.md` untouched
per the gen-2 convention (#95 card documents why).
