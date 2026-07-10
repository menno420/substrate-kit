# Session 2026-07-10 — adopter-registry regen after the v1.7.1 upgrade wave (kit seat)

> **Status:** `complete`

- **📊 Model:** claude-fable-5 · medium · docs-regen (fleet registry currency)

**Scope (as declared, born-red):** v1.7.1 distribution-wave close-out, kit-seat
slice — regenerate the GENERATED `docs/adopters.md` via `python3
dist/bootstrap.py currency` now that this seat's four adopters merged their
v1.7.0 → v1.7.1 upgrades on green (superbot-next #122 @ 1ba8607 · websites #74
@ a057140 · gba-homebrew #27 @ 16e64d7 · venture-lab #14 @ 7558cb2). A PARALLEL
worker is mid-flight on fleet-manager / superbot-games / trading-strategy —
their rows are expected possibly-stale in this snapshot (the `Generated:`
stamp is the snapshot time); their rows are NEVER hand-fixed. Registry-only +
this card; NEVER touched: `control/inbox.md`, `control/status.md` (the
coordinator owns the seat heartbeat — no `claimed-by:` line accompanies this
session per the #135 precedent; this born-red card + the immediately-opened PR
is the in-flight signal). Verified pre-flight at origin/main HEAD 415c37e: no
open PRs, no live claim in any `control/status*.md` touching
`docs/adopters.md` or the currency checker, no ORDER 012+ in the inbox.

## Close-out

**Shipped (session PR #142):** `docs/adopters.md` regenerated from live tree
truth (10 repos scanned, `Generated: 2026-07-10T22:11:08Z` — the snapshot
time). All four kit-seat wave repos read **tree=v1.7.1 · pin=v1.7.1**:
superbot-next, websites, gba-homebrew, venture-lab. Parallel-worker lane at
snapshot time: fleet-manager and superbot-games ALREADY tree=v1.7.1 (their
upgrades merged before the scan), trading-strategy still tree=v1.7.0 →
`stale (v1.7.0 < v1.7.1)` — the expected mid-wave state, deliberately NOT
hand-fixed; the next regen picks it up. Verified locally: `python3 -m pytest
tests/ -q` → **858 passed**; `python3 src/build_bootstrap.py` rebuild
byte-identical (dist byte-pin clean, `git status` empty); `check --strict`
red only on this card's own born-red hold (this flip clears it). One
guard-fires.jsonl append (the check run's session-log fire) rides the regen
commit, matching prior sessions.

**Surfaced, not resolved (registry protocol — reconcile at the SOURCE):**
5 DRIFT rows, 4 self-report lag + 1 tree-internal: superbot-next (status
claims v1.6.0), gba-homebrew (v1.6.0), superbot-games (both lane heartbeats
v1.2.0), fleet-manager (v1.7.0) — all tree=v1.7.1, same upgrade-doesn't-touch-
the-heartbeat cause the #135 card's 💡 already named; plus the kit's own
config-pin v1.0.0 vs dist v1.7.1 (deliberately untouched pending the §7
version-truth ruling).

**💡 Session idea:** the currency run report (and the file's drift section)
could tag each DRIFT row with `seen-since: <first Generated stamp that showed
it>` by diffing against the previous committed adopters.md at regen time —
persistent drift (superbot-games' v1.2.0 lane heartbeats, now surviving three
regens) would then be visibly chronic rather than indistinguishable from
fresh wave-lag, giving the coordinator a triage signal for when
reconcile-at-source needs an actual dispatched order instead of patience.

**⟲ Previous-session review:** the release-v1.7.1 session (#139/#140 + run
29124338479) was exemplary on the ritual (claim-first on main, born-red bump,
independent sha256 verification of the published asset) and its
"suite is 858 tests, brief said 819 — repo wins" note directly saved this
session from chasing a phantom count mismatch. One improvement it surfaces:
its close-out heartbeat is a single ~3000-word status.md overwrite in which
load-bearing facts (the alias-job false-alarm, the semver flag) sit inside
one giant `notes:` paragraph — a keyed sub-line convention (e.g.
`notes.false-alarm:`, `notes.flagged:`) would let the next session grep one
fact without parsing the whole block.
