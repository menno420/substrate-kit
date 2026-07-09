# Session 2026-07-09 — enabler label-race hotfix (the #22 incident guard)

> **Status:** `complete`

**Scope (incident-driven hotfix):** deploy PR #17's fresh-label re-read
guard into `.github/workflows/auto-merge-enabler.yml` on main NOW — the
`do-not-automerge` gate was defeated live today when PR #22 (PL-010,
discuss-first program law) auto-merged mechanically: main's enabler checks
the label only via its job-level `if:` on the **stale PR-open event
payload**, the label landed +7 s after open, and a ~12-min runner-queue lag
armed auto-merge long after the label existed (incident comment on #22).
The guard exists but only inside unmerged, owner-gated PR #17 — this PR
extracts exactly that hunk (byte-identical) so it is live for the very next
labelled PR, and #17's eventual merge conflict on this file resolves
trivially/identically. Also fixes the post-#22 prose staleness on main
(`docs/current-state.md` owner gate 2 + the idea file's B4 frontmatter
still describe #22 as open/awaiting blessing).

## What shipped

- **`.github/workflows/auto-merge-enabler.yml`** — PR #17's KL-5 race
  guard, extracted **byte-identical** (verified: `diff` of the full file
  vs `claude/kl5-bench-tree`'s head is empty): a new
  `Re-check the do-not-automerge label FRESH` step (15 s grace beat →
  `gh api .../issues/$PR/labels` re-read → `skip=1` on the label) + the
  arm step's `if:` gaining `steps.label.outputs.skip == '0'`. **Queue-lag
  coverage verified, no extra change needed:** the re-read runs at job
  *execution* time — after any runner-queue wait — so it defeats both the
  seconds-level label-after-open race AND the ~12-min queue lag that
  actually merged #22.
- **`docs/current-state.md`** — owner gate 2 reworded to **ratify or veto
  PL-010 (#22)** (merged mechanically; reaction replaces the
  merge-as-ratification gate; veto = revert PR); a #22 row added to
  Recently shipped with the incident flag.
- **`docs/ideas/feature-build-task-class-2026-07-09.md`** — B4 frontmatter
  flipped `shipped` (shipped_pr: 22, shipped_repo: menno420/substrate-kit,
  merged_date: 2026-07-09) — it did ship, however irregularly; Status
  prose records the mechanical merge + pending ratify-or-veto; README
  entry moved to the Shipped (survive window open) section.

## Run report

- **📊 Model:** fable-5 · high · runtime bugfix
  *(judgment: the natural label "guard/checker work" is not one of
  PL-004's nine classes — filing it would be the exact off-taxonomy drift
  PL-010 exists to end. Nearest true class: a live defect in running
  automation, root-caused and fixed — `runtime bugfix`, not
  `feature build` (no new capability; a hunk of #17 deployed early).)*

### ⚑ Self-initiated / flags (decide-and-flag, PL-001)

1. **This PR duplicates one hunk of owner-gated #17 BY DESIGN** — the
   guard could not wait for #17's blessing after defeating a program-law
   gate live. Byte-identical extraction so #17's conflict on this file
   resolves trivially/identically; comment posted on #17 after merge.
2. **#22 row added to Recently shipped** (slightly beyond the named
   staleness fixes) — reality is it merged; a ledger that lists it only
   as an owner gate would misreport what is on main.
3. **💡 filed as a full idea file** (below) rather than a card-only note —
   it names a real residual attack window on a governance gate.

### 💡 Session idea (dedup-checked against docs/ideas/ + roadmap)

**Label-added disarm guard** — filed with B4 frontmatter at
`docs/ideas/label-added-disarm-guard-2026-07-09.md` + README entry. The
deployed re-read is point-in-time: a `do-not-automerge` label applied
*after* the enabler has armed (owner labels five minutes — or a day —
later) still does nothing, and #22 proved manual disarm loses timing
races. Guard recipe: `on: pull_request: types: [labeled]` →
`gh pr merge --disable-auto` — the label itself becomes the disarm switch
at any moment in the PR's life (enforce, don't verify — PL-002).

### ⟲ Previous-session review — pl004-feature-build (PR #22)

The work itself was exemplary (amend-don't-supersede register shape,
count derived from `len(TASK_CLASSES)`, conflict-hygienic CHANGELOG
placement). The incident exposes the one real flaw, and it's
instructive: the card's governance line — "auto-merge verified **not
armed** (and disarmed if ever found armed)" — was true when written and
false 12 minutes later, because the adversary was a *queued* workflow
run, not a state. **A point-in-time verification of an asynchronous
adversary is not a verification.** Concrete system improvement, two
halves: (a) when verifying "workflow X did not / will not act", check
the Actions *queue* for a pending run of X on your PR, not just current
state — a queued enabler run is a loaded gun the state read can't see;
(b) better, stop verifying and enforce — the 💡 above makes the label
itself disarm at any time. Half (b) is filed; half (a) is this sentence,
grep-able for the next session that writes a "verified not armed" line.

## KPIs / verification (this worktree)

- `python3 -m pytest tests/ -q` → **618 passed** (no engine changes; dist
  untouched, byte-pin unexercised by this diff — `git status` confirms
  only workflow + docs + card + idea files).
- Workflow hunk: `diff <(git show FETCH_HEAD:.github/workflows/auto-merge-enabler.yml) …`
  vs `claude/kl5-bench-tree` → **byte-identical**.
- `python3 scripts/check_program_law.py` → OK.
- `python3 scripts/check_idea_index.py` → OK (shipped frontmatter + the
  new captured idea + README moves).
- `python3 dist/bootstrap.py check --strict --require-session-log
  --session-log .sessions/2026-07-09-enabler-race-hotfix.md` → green at
  this flip (held red while `in-progress`, as designed).
- PR #23: opened born-red READY via MCP, auto-merge armed at open
  (enable_pr_auto_merge — the Q-0127 MCP carve-out), **no**
  `do-not-automerge` label: this PR is meant to auto-merge, and its own
  enabler run exercises the new guard's happy path.
