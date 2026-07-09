# Session 2026-07-09 — band KL-8: the coordination-protocol kit band (ORDER 002)

> **Status:** `complete` *(PR #31 — auto-merge armed at open)*

**Scope (about to do):** execute inbox ORDER 002 — make the `control/` fleet
coordination protocol a first-class kit capability per the canonical spec
(superbot `docs/planning/fleet-coordination-protocol-2026-07-09.md` §2):
(1) `control/` scaffold in `ADOPT_PLAN` — plant a generalized
`control/README.md` (new `control-README.md.tmpl`) + seeded-skeleton
`control/inbox.md` / `control/status.md`, skip-if-exists like every plant;
(2) the status-freshness checker (`engine/checks/check_status_current.py` —
engine-side so it ships in the dist to every adopter): missing/heartbeat-less
status gates strict RED (the born-red graduation the spec names), wall-clock
staleness warns advisory-only, and the Stop hook advises when `status.md`
wasn't overwritten this session; (3) the CI control fast lane — control-only
diffs short-circuit the heavy suite GREEN inside the required job (never
`paths-ignore`, which would leave required contexts pending and jam
auto-merge — today's heartbeat-lane lesson), in both the kit's own `ci.yml`
and the planted `substrate-gate.yml`; (4) tests for all of it, dist
regenerated + byte-pinned, CHANGELOG `[Unreleased]`, ledger KL-8 entry,
D-0007. Release v1.2.0 rides a separate follow-up PR per the #29 pattern;
the status overwrite is the deliberate LAST act of the whole order (its own
control-only PR, exercising the new lane live).

## What shipped (PR #31)

- **`control/` scaffold**: 3 new templates (`control-README.md.tmpl` —
  the generalized contract incl. both 2026-07-09 CI lessons;
  `control-inbox.md.tmpl` / `control-status.md.tmpl` seeded skeletons, the
  status seed honestly heartbeat-less) appended to `ADOPT_PLAN` with a
  root-level rationale comment; planted skip-if-exists + hash-recorded like
  every plant, `${project_name}` rendered from the derived slot.
- **`engine/checks/check_status_current.py`** (in `MODULE_ORDER` → ships in
  the dist): `parse_heartbeat` (ISO-8601, Z-tolerant, naive=UTC);
  `(gate, advisory)` split — `status-missing` / `status-no-heartbeat` ride
  the strict finding loop (wired in `cmd_check` + printed on `cmd_adopt`'s
  NOT-ENGAGED checklist), `status-stale` (>72h) is emitted + guard-fire
  recorded with posture `advisory` and never touches the exit code;
  `hooks/stop_check.py` gains `_stop_status` (mtime vs KL-5 session
  anchor, fail-open).
- **CI control fast lane**: `ci.yml` lane-detect step + every heavy step
  (incl. session gate + setup-python) conditioned, an explicit
  green-by-design step reports on the lane; `live_ci_workflow()` (planted
  `substrate-gate.yml`) carries the same in-job short-circuit; `ci_snippet`
  warns against `paths-ignore` on required checks; cold-adopt smoke
  extended with the KL-8 leg (RED on seed status → GREEN after the first
  real heartbeat) — walked locally end-to-end before push.
- **Friction→guard, caught live**: the first dist regen omitted the new
  module (`MODULE_ORDER` is a hand list) — the dist byte-pin stayed green
  while dist `cmd_check` NameError'd. Guard shipped same commit:
  `test_module_order_covers_every_engine_module` pins MODULE_ORDER == the
  on-disk `src/engine/` module set.
- **Docs**: CHANGELOG `[Unreleased]` (3 Added + 1 Fixed), ledger KL-8
  baseline bullet + In-flight #31 + recently-shipped row, D-0007
  (static-states-gate / time-only-warns / in-job-lane-not-paths-ignore),
  idea filed + indexed.
- **Verification**: suite 658 → **683** (py3.11 + py3.10 both green); ruff
  clean; dist rebuilt deterministically; `check_idea_index` /
  `check_program_law` / `check_bench_integrity` OK; dist `check --strict
  --require-session-log --session-log <this card>` held RED on the
  born-red badge exactly as designed (green at this flip); adopt smoke arc
  verified in scratch dirs with the new dist.

## Run report

- **📊 Model:** fable-5 · high · feature build

### ⚑ Self-initiated / decide-and-flag (PL-001)

1. **⚑ Engine check, not `scripts/`**: the spec names
   `check_status_current.py` and its graduation to the born-red post-adopt
   gate — that gate is the engine's `check --strict`, and adopters only
   receive engine code via the dist, so the checker is
   `src/engine/checks/`, not repo-local `scripts/` (which never ships).
2. **⚑ "warns → graduates" resolved by determinism, not by phase**: static
   protocol states (missing / heartbeat-less status) gate strict RED *now*;
   wall-clock staleness stays advisory *permanently* — a REQUIRED CI
   context that reds purely on elapsed time is a pre-reddened-PR time bomb.
   D-0007 records the split.
3. **⚑ `paths-ignore` (spec §2 item 4) replaced by the in-job short-circuit**
   — the order's own lesson (a): with `paths-ignore` on a required suite,
   the context never reports, GitHub holds it "pending", and heartbeat PRs
   jam. The lane skips every heavy step (same cost saving) while the
   required context always reports.
4. **⚑ Lesson (b) closed by documentation + write-path doctrine**: the
   planted `control/README.md` documents that API-authored PRs may carry
   zero check runs (#27) and sets the manager's canonical inbox write as a
   direct Contents-API commit to the default branch (sole-writer ⇒ no PR
   needed); `check_status_current` itself is CI-agnostic (file-shape only),
   so nothing in the checker can strand on a checks-less PR.
5. **⚑ Session gate skipped on the control lane**: heartbeat PRs carry no
   session card by design — coordination writes are exempt from the card
   ritual (pinned by `test_ci_control_lane.py`).

### 💡 Session idea (dedup-checked against docs/ideas/ + roadmap)

**`bootstrap heartbeat` — a mechanical status.md writer** — filed with B4
frontmatter at `docs/ideas/heartbeat-verb-2026-07-09.md` (+ README index):
the moment the heartbeat became *enforced* (this band), its hand-formatted
`updated:` timestamp became the weakest link — one verb writes the
contract-shaped file with an always-parseable UTC stamp, giving sessions
and routine wakes a mechanical LAST step (the KL-5 auto-draft motion
applied to the protocol).

### ⟲ Previous-session review — control-protocol adoption (PR #30)

Strong: landing the stranded manager PR #27 forward-only (merge main in,
never force), and the acked-NOT-done honesty on ORDER 001 while v1.1.0 rode
a parallel PR, are exactly the one-writer/forward-only discipline the
protocol needs — and its 💡 (manager PRs strand with zero check runs) fed
directly into this band's README-template lesson. What it missed: it opened
against a stale base (11744d8) while #29 was rewriting the same
`docs/current-state.md` "In flight" section — at this session's start #30
still sat open on that base, a likely textual conflict nobody owns.
**Workflow improvement:** a session opening a PR that touches
`docs/current-state.md` should re-merge main (or rebase via merge) into its
branch *at open time* if `origin/main` moved past its base — cheap to state
in the session-shape journal rule, and it would have let #30 merge clean.
(This band deliberately edited around #30's hunks; `status.md` conflicts
are structurally impossible — overwrite-own, newest wins.)

## KPIs / verification (this worktree)

- `python3 -m pytest tests/ -q` → **683 passed** (also green under
  `python3.10`); baseline was 658.
- `python3 -m ruff check src/engine/` → clean; dist regenerated twice,
  byte-identical; `check_idea_index` / `check_program_law` /
  `check_bench_integrity` all OK.
- Dist smoke: bare adopt prints the 4-condition checklist incl.
  `[status-no-heartbeat]`; full arc render → gate → card → **still RED on
  seed status** → heartbeat → `check --strict` green; planted
  `substrate-gate.yml` YAML-parses with the lane step.
- Born-red gate: dist `check --strict --require-session-log --session-log
  <this card>` rc=1 while `in-progress`; flips green with this commit.
