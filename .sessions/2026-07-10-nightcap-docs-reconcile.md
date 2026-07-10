# 2026-07-10 — gen-2 night-cap: docs reconcile + groom (post-overnight-run)

> **Status:** `complete`

- **📊 Model:** Claude (ID withheld) · high · docs-reconcile night-cap
  (single docs-only PR: queue-state/next-boot reconcile + CHANGELOG backfill
  + one groom + ledger drift fixes)

## Scope (as declared)

Reconcile `docs/gen2/queue-state.md` against what the overnight run actually
landed (every PR number verified on main), fix stale bits of
`docs/gen2/next-boot.md`, one backlog groom, and a docs-drift audit —
claimed via #107 (`nightcap-docs-reconcile-groom`).

## What shipped

1. **`docs/gen2/queue-state.md` reconciled** (header banner + per-item
   annotations, all verified against `git log` at HEAD 704a537): IN FLIGHT
   fully resolved (#74 merged; #26 = `706190f`, #49 = `6d6046b`, both
   owner-clicked ~00:10Z); owner one-click crosswalk to the renumbered
   OWNER-ACTION 1–10; agent queue 9/12 DONE with PRs (#84 boot · #85 run-3 ·
   #95 item 3 · #86+#87+#89 item 5 · #91 item 6 · #90 item 7 · #98 item 8 ·
   #92 item 10 · #103 item 11); the 3 remaining each carry their exact gate
   (item 4 T5 = pin path → daytime `do-not-automerge` PR; item 9 = P10;
   item 12 = P5 + P11-or-P13). Same-night out-of-queue ships noted
   (#99, closes, visiting #105/#108 lane).
2. **`docs/gen2/next-boot.md` de-staled**: OWNER-ACTION count/renumber
   (11 → 1–10, refs at items 4/§3 branch-cleanup/§3 setup-script), KF-8
   threshold marked MET (run-3, PR #85, first trend on record), queue-state
   pointer notes the reconcile. (The #26/#49 "do not touch" §4 bullet was
   already fixed by the run-3 session — verified, left as-is.)
3. **CHANGELOG `[Unreleased]` backfilled** — six overnight PRs had shipped
   with no entry: #87 (+#89) and #90 added under `### Added` (new
   checkers); #86, #91, #92, #99 under `### Fixed`. Each entry written
   from the PR's actual diff/card, not the coordinator brief (#99's brief
   description was corrected against its real commit message).
4. **`docs/current-state.md` drift fixed on sight**: stale owner gate 1
   ("bless rubric → merge #17" — owner-merged 2026-07-09 per D-0005, the
   ledger's own baseline section already said so) removed; F-5 ruling
   promoted to gate 1 (HOT); Next action = post-overnight queue-dry state;
   agent-queue item 1 (#92) closed; overnight nine-PR block added to
   Recently shipped; older #75/PL-010 entries compressed (see budget note).
5. **`docs/CAPABILITIES.md` append** (THE DISCOVERY RULE, live-hit this
   session): armed auto-merge does not fire on a `behind` PR — #107 sat
   10+ min with all checks green; recipe = check `mergeable_state` first,
   merge origin/main, push.
6. **Groom**: filed the #103 card-only 💡 into
   `docs/ideas/plain-adopt-lane-drift-advisory-2026-07-10.md` + README
   backlog entry (state: captured → reachable by the grooming surface).

## Gates (final head)

- `python3 -m pytest tests/ -q` → **814 passed**
- `python3 dist/bootstrap.py check --strict` → orientation-budget finding
  cleared at 7000-word boundary after trims; remaining finding pre-flip was
  only the born-red session gate itself (this flip clears it)
- `python3 src/build_bootstrap.py && git diff --exit-code dist/bootstrap.py`
  → byte-pin green

## Run report

### ⚑ Flags

1. **⚑ Self-initiated:** the groom choice (filing the #103 card-only idea),
   the CAPABILITIES `behind`-stall append, and the current-state
   compressions (#75, PL-010 gate) — the last were forced by the
   [orientation-budget] gate: this session's additions pushed the boot-read
   set (AGENT_ORIENTATION + current-state) from ~6.9k to 7,250 words, over
   the 7,000 budget; trimmed back under by compressing entries whose detail
   lives elsewhere (registry, #22 comment, CHANGELOG). Nothing was deleted
   that isn't reachable in a durable home.
2. **⚑ Discrepancy vs the coordinator brief: none material** — every
   claimed PR verified on main. One nuance the brief missed: #92 was
   authored overnight but landed via the #98 lane's adoption (its own
   session lost the auto-merge arm race), and #99's content differed from
   its one-line description (token *shorthand acceptance*, not re-sync).

### 💡 Session idea (dedup-checked against docs/ideas/ + roadmap)

**Orientation-budget headroom advisory.** The budget gate bites silently:
this session took the boot-read set 6.9k → 7,250 words with no signal until
`check --strict` went red, then paid an iterative trim loop (7250 → 7136 →
7065 → 7004 → green) with a full check run per guess. A `check` advisory at
≥95% of `budget_words` ("boot-read set at 6,950/7,000 — 50 words of
headroom") plus the per-doc word split in the finding message would turn
the cliff into a gauge — and a docs session would see the pressure BEFORE
committing. No existing `docs/ideas/` file covers orientation/budget.

### ⟲ Previous-session review (`.sessions/2026-07-10-adopt-lane.md`, PR #103)

Genuinely strong: the claim ritual run end-to-end for the fourth time that
night, field verification through the real dist CLI in a scratch repo
(fresh lane / join / refusal all exercised live), and the replace-vs-append
rule disclosed as a flag rather than buried in code. The irony worth
naming: its ⟲ review correctly flagged the #98 session for leaving its 💡
idea card-only — then its own 💡 (plain-adopt lane-drift advisory) was
ALSO left card-only. The pattern held for two consecutive sessions, which
means it's structural, not a lapse. **Workflow improvement:** make the
close ritual mechanical about it — a one-line advisory in the session-log
checker (or the close skill) when a `complete` card contains a `💡` block
but the same session's diff adds no `docs/ideas/` file and the card lacks
an explicit "deliberately card-only" note. This night-cap filed the
orphan; the checker would make that filing self-serve.

### Docs audit

Is anything from this session not in its durable home? Queue truth →
queue-state.md (reconciled); boot guidance → next-boot.md; release notes →
CHANGELOG [Unreleased] (backfilled); living ledger → current-state.md;
capability finding → CAPABILITIES.md append log; groomed idea →
docs/ideas/ + README index; the `behind`-stall recipe doubles in the
status-close notes. `control/inbox.md` and all pin paths untouched. Status
close (the sole remaining step after this flip) overwrites
`control/status.md` as the deliberate LAST act and clears the #107 claim.
