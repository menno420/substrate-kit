# 2026-07-14 — `bootstrap heartbeat` mechanical status.md restamp verb (ORDER 019 item 7)

> **Status:** `in-progress`

About to (opening declaration): build the `bootstrap heartbeat` CLI verb — a
mechanical, grammar-exact writer/refresher for the seat's `control/status.md`
heartbeat fields per `docs/ideas/heartbeat-verb-2026-07-09.md` (ORDER 019
item 7): non-destructive preserve-and-restamp, `--dry-run`, grammar reuse
from `engine.grammar`, tests + dist regen.

## What shipped (PR #346)

- `src/engine/heartbeat.py` (new): two lanes. **Restamp lane (default)** —
  non-destructive preserve-and-restamp: only the `updated:` line's timestamp
  token (fresh UTC now, seconds precision, the `updated_line_example` shape)
  plus explicitly passed field lines (`phase:`/`health:`/`orders:`/
  `last-shipped:`/`blockers:`/`⚑ needs-owner:`/`notes:`) are rewritten;
  `--kit-version` swaps only the `kit:` line's `v<X.Y.Z>` token. ⚑ blocks,
  ORDER ledger lines, `claimed-by` annotations, decorated `updated:` tails
  all survive byte-identical (test-pinned by reconstructing the input from
  the output). **Full-write lane (`--full`)** — the idea file's
  contract-shape whole-file writer for the first real heartbeat over the
  adopt seed; missing flags default honestly (`blockers: none`,
  `⚑ needs-owner: none`); `--phase` required (no honest default exists).
- Grammar reuse, zero duplicated regexes: `UPDATED_LINE_RE` (already
  case-insensitive), `KIT_LINE_RE`, `KIT_VERSION_TOKEN_RE` from
  `engine.grammar`; every write round-trips through
  `check_status_current.parse_heartbeat` before it leaves the module (the
  idea file's write → parse → equal recipe, run at runtime, not just in
  tests).
- `cmd_heartbeat` in `cli.py`: `--dry-run` prints a unified diff (or the
  full text for a new file) and writes nothing; `--status-file` targets a
  lane heartbeat (default: first `heartbeat_files` entry); refuses outside a
  control-carrying host (the idea file's named test); missing/seed/
  unparseable status.md errors name the fix (`--full`), never a silent
  clobber. Writes via `atomic_write_text`.
- Advisory pointers wired (the idea file's "session-close advisory pointer"
  recipe): `status-stale` message now names `python3 bootstrap.py
  heartbeat` as the mechanical restamp; `status-no-heartbeat` names
  `heartbeat --full --phase "…"`.
- Decide-and-flag — **restamp is the default lane, contract overwrite is
  opt-in (`--full`)**: the idea file predates the fleet's rich seat
  heartbeats (⚑ sets, shipped ledgers); a default whole-file overwrite would
  destroy them, and ORDER 019 item 7 names the verb as the fix for the
  heartbeat-staleness class, which is a restamp. The idea file's whole-file
  contract lane is preserved verbatim behind the explicit flag.
- Decide-and-flag — the restamp lane refuses `--kit-check`/`--kit-engaged`
  (they shape the `--full` render only) instead of silently ignoring them.
- `src/build_bootstrap.py`: `heartbeat.py` registered after
  `check_status_current.py`; dist regenerated.
- `tests/test_heartbeat.py`: 17 tests — byte-identical round-trip on a
  realistic seat heartbeat, enforcer-grammar assertions on the restamped
  output, field/kit-token surgery, dry-run-writes-nothing (incl. no `.tmp`
  residue), refusals (no control bus, missing file, adopt seed, missing
  field line, kit line absent, full-only flags), full-lane honest defaults,
  lane `--status-file`.

## Verify

- `python3 -m pytest -q` → 1322 passed at session-start HEAD (4e09862) →
  **1339 passed** after the change + the origin/main merge (#340 landed
  mid-session; sole conflict `.substrate/guard-fires.jsonl` resolved as
  append-only union).
- `python3 src/build_bootstrap.py` run twice, pre- and post-merge →
  byte-identical (sha256 2627df64… all runs, 911787 bytes).
- `python3 -m ruff check src/engine/` → All checks passed.
- `python3 dist/bootstrap.py check --strict` → red only on this card's own
  designed born-red hold pre-flip (plus the standing preflight-script NOTE);
  green expected on the flip.
- Dogfooded: this close-out's `control/status.md` restamp was performed by
  the new verb itself (`python3 dist/bootstrap.py heartbeat --target .`)
  after the hand-edited outcome line — the hand edits survived the restamp
  byte-identical, live proof of the preserve contract.

## Enders

💡 **Session idea:** `bootstrap heartbeat --done <order-id>` — a mechanical
`orders:` line mutator that moves an id from `claimed-by:` into `done=`
using `ORDERS_LINE_RE`/`ORDERS_DONE_RE`/`ORDERS_CLAIMED_BY_RE` (already in
`engine.grammar`, currently enforcer-only). The orders ack/done line is the
second hand-assembled grammar surface after the timestamp — the claim ritual
(claim → build → move to done=) is exactly the kind of fiddly token surgery
sessions get subtly wrong, and the grammar constants for it already exist
with no writer half. Dedup-grepped `docs/ideas/` — the heartbeat-verb idea
covers fields, not orders-line mutation; no other file touches it.

- **📊 Model:** Fable (Claude 5 family)

⟲ **Previous-session review** (2026-07-14-enabler-install-preflight.md,
ORDER 019 item 4): strong session — the fail-open contract was enumerated
per degradation path and each path got a test, which is why 28 tests landed
without a red round-trip; and its card's "Q-0200 exact-name class — caught
by pre-commit grep, not by CI" note is a genuinely useful trailhead this
session reused when naming new module-level helpers. Improvement it
surfaces: its session idea (PR-time required-context name drift) was left as
a card ender only — it never got a `docs/ideas/` file, so the idea index
can't route it and the next groom pass won't see it. The workflow gap is
real: card-ender ideas substantial enough to name a drift window should get
the idea file in the same session (the Q-0089 capture discipline), not just
the card line.

Run type: ORDER-dispatched worker session (ORDER 019 item 7).
