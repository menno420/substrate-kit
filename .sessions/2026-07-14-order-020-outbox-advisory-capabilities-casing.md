# 2026-07-14 · ORDER 020 (d)+(e) — check-time outbox advisory + fleet-master pointer casing

> **Status:** `complete`

About to happen (opening declaration): close the two open BUILD sub-items of
ORDER 020 (fm lane-write relay, 2026-07-14T04:12Z; a/b/c were premise-checked
SATISFIED at HEAD and need no action):

- **(d) — A10 outbox-size advisory in `check --strict`.** The friction-outbox
  drain reminder (`list_outbox` → "N report(s) pending, file them then delete")
  lives ONLY in `cmd_session_close` today, so a stranded envelope — a §9.1
  friction report the engine could not file (no GitHub reach) — is invisible to
  every plain `check` / `check --strict` between session-close seams. Lift the
  same pending-count reminder into the `check` advisory lane.
- **(e) — INC-29 / fm plan B2: dead lowercase `docs/capabilities.md` → uppercase
  `docs/CAPABILITIES.md`** at the three seat-digest/CAPABILITIES surfaces. fm
  (authority on its own repo) states its fleet-master ledger is uppercase; the
  lowercase pointer is a dead link. One template fix heals ~14 adopters.

- **📊 Model:** Opus 4.8 · high · feature build

Run type: routine · lab

## What shipped (PR #363)

- **(d)** `src/engine/checks/check_outbox.py` (new, stdlib-only):
  `check_outbox_pending(target, state_dir)` returns one advisory `Finding`
  (`outbox-pending`) when `list_outbox` finds ≥1 envelope, naming the head
  envelopes (elides past 3) and the drain verbs (`friction show` /
  `friction export`) + the `friction` label; empty outbox → no finding. Wired
  into `cmd_check`'s full lane (`src/engine/cli.py`) with the identical
  warn-only emit + `record_guard_fires` block as every other advisory —
  **advisory-only, never exit-affecting** (the envelope may be un-drainable
  precisely because CI has no GitHub auth, so a required-check red would be a
  bomb); `not status_only` (the outbox is not control-lane traffic).
  Registered in `MODULE_ORDER` (`src/build_bootstrap.py`) right after
  `loop/friction.py` — it consumes `list_outbox`/`FRICTION_LABEL` defined
  there; dist regenerated, byte-stable.
- **(e)** dead lowercase `docs/capabilities.md` → uppercase
  `docs/CAPABILITIES.md` at all three surfaces the order named:
  `src/engine/templates/CAPABILITIES.md.tmpl:8` (the "Fleet master copy" line
  planted into every adopter's ledger), `src/engine/seatdigest.py` docstring
  (:31) and the rendered "No third copy" block (:442). The template-pointer
  guard's `_EXTERNAL_REPO_REFS["docs/capabilities.md"]` entry went stale on the
  fix (no template emits lowercase anymore — `test_no_stale_accounting_entries`
  would flag it) and was removed with a comment recording INC-29; the corrected
  uppercase pointer resolves via `_PLAN_DESTS` (it is an ADOPT_PLAN dest), and
  `CAPABILITIES.md.tmpl` still names `menno420/fleet-manager` next to it.
- `tests/test_check_outbox.py` (6 tests): empty-silent (no dir + empty dir),
  fires-one-advisory (singular grammar, names the envelope, drain verbs +
  label), plural grammar + name-preview elision (>3), two-envelopes no-elision,
  and a **differential** end-to-end proof — adding a pending envelope to a tree
  never changes what `check --strict` decides, only adds the surfaced line.
- `CHANGELOG.md` `[Unreleased]` — `### Added` (d) + `### Fixed` (e).
- ORDER 020 ack appended to `control/inbox.md` (pure-append, grammar-clean);
  `docs/current-state.md` ▶ Next action sharpened (DONE/REMAINS/where-stopped).
- `.substrate/guard-fires.jsonl` delta committed per the ledger convention.
- Park state: PR opened READY early; the born-red card holds the merge until
  this flip. Routine lab loop — the server-side enabler arms auto-merge on
  non-draft `claude/*` PRs on its own; the card gate is the real door.

## Decide-and-flag

- **Both sub-items in ONE PR under one ORDER-020 card.** (d) is a small
  feature and (e) a three-site casing fix; they share provenance (ORDER 020),
  both regen dist, and the order's done-when closes on both — one PR closes the
  order cleanly and halves CI/dist churn. Reversible: two independent commits.
- **`_NAME_PREVIEW = 3` on the envelope name list.** The finding is one line;
  a long outbox names its head and points at the directory for the rest.
  Reversible: one constant.
- **Removed rather than re-cased the `_EXTERNAL_REPO_REFS` guard entry.** With
  the template pointer now uppercase (an ADOPT_PLAN dest), no template emits a
  cross-repo lowercase pointer, so a re-cased entry would itself be stale by
  the same test. The uppercase resolves via `_PLAN_DESTS`; the sentence still
  attributes fleet-manager, so the cross-repo intent survives in prose.

## Verify

- Baseline (morning consolidation, main @ c0297d8): 1495 tests. Final:
  `python3 -m pytest tests/ -q` → **1501 passed, 1 skipped** (+6 from
  `test_check_outbox.py`, zero failures).
- `python3 scripts/preflight.py` → `preflight: OK — 7 leg(s) green` (pytest ·
  dist byte-pin · ruff · idea-index · changelog-structure · program-law ·
  bench-integrity).
- `python3 dist/bootstrap.py check --strict` → green except the DESIGNED
  born-red HOLD naming this card (pre-flip); the outbox advisory is correctly
  SILENT on this repo (no pending envelopes); pre-existing model-line
  advisories on earlier July-14 cards unchanged, never exit-affecting.
- dist byte-stability: `python3 src/build_bootstrap.py` twice → identical
  sha256 `b1b515cad460f74f9c59e0773b402973fdb2360a0ae996dea367113a3f93477e`.
- `python3 -m ruff check src/engine/checks/check_outbox.py src/engine/cli.py
  src/engine/seatdigest.py` → All checks passed.
- Inbox append proven pure-append + grammar-clean against `origin/main`'s blob
  (`check_inbox_append` → CLEAN) — the ORDER 020 ack does not red the CI inbox
  leg.

## 💡 Session idea

Give the `check` advisory lane a **one-line roll-up header** when several
advisory families fire at once. Today each family (`setup-script`,
`model-line`, `adopter-registry`, `auto-merge-enabler`, and now
`friction-outbox`) prints its own `check: N … advisory warning(s) (never
exit-affecting):` banner followed by its findings — a check run with four live
families emits four near-identical banners, and the "never exit-affecting"
reassurance is repeated verbatim each time. A single leading
`check: M advisory warning(s) across K families (never exit-affecting) —` line,
with each family then printing just its findings under a short `[family]`
sub-label, would cut the boilerplate and make the advisory block scan as one
section instead of five. Purely presentational (no posture change), and the
per-family guard-fire records stay exactly as they are. Dedup-grepped
`docs/ideas/` (44 files): the advisory checkers each have their own idea file
but none proposes consolidating the *emit* surface — this is about the shared
presentation seam in `cmd_check`, not any single checker.

## ⟲ Previous-session review

Previous run (the ORDER 019 EAP-final-night arc through the backlog-dry phase,
#342–#361): a genuinely strong sweep — the seat consumed inbox 001–019 + fm
ORDER 025 top-down, one card per item, every engine item landing with tests +
a dist byte-pin in the same PR, and it converged the local/CI check surfaces
(#342/#343) that this very ORDER 020 then premise-checked as SATISFIED — the
loop's own convergence work made three of my five sub-items no-ops, which is
the system working. What it left for me: ORDER 020 landed at 04:12Z, ten
minutes *after* the 04:02Z status.md consolidation declared "backlog DRY", so
the order sat unconsumed with no status/current-state pointer — I nearly
treated the tree as idle. Concrete workflow improvement: an order appended to
`control/inbox.md` after the last heartbeat should trip a check-time "unacked
ORDER newer than the status heartbeat" advisory (the data is already there —
the inbox's newest `## ORDER` timestamp vs `status.md`'s `updated:` stamp), so
a fresh routine fire sees the unconsumed order mechanically instead of by
reading the whole inbox tail. Filed as a follow-up candidate here; it pairs
naturally with the existing `check_status_current` heartbeat gate.

## Documentation audit

CHANGELOG `### Added`/`### Fixed` entries ride this PR; ORDER 020 ack appended
to `control/inbox.md`; `docs/current-state.md` ▶ Next action carries the
DONE/REMAINS/where-stopped handoff; the decide-and-flag calls are recorded
above and in the PR body; guard-fires delta committed; `check --strict` green
but for the designed hold. Nothing chat-only remains.
