# Session 2026-07-11 — adopter-registry regen after the v1.8.0 upgrade wave (kit seat)

> **Status:** `complete`

- **📊 Model:** claude-fable-5 · medium · docs-regen (fleet registry currency)

**Scope (as declared, born-red):** v1.8.0 distribution-wave close-out, kit-seat
slice — regenerate the GENERATED `docs/adopters.md` via `python3.10
dist/bootstrap.py currency` now that this seat's four adopters merged their
v1.7.1 → v1.8.0 upgrades on green (superbot-next #135 @ 3dfc194 · websites #85
@ 8abfe0a · gba-homebrew #28 @ 0a7689f · venture-lab #17 @ fb5ef4b). A PARALLEL
worker is mid-flight on fleet-manager / superbot-games / trading-strategy —
their rows read whatever the tree says at snapshot time (the `Generated:`
stamp is the snapshot time); their rows are NEVER hand-fixed. Registry-only +
this card; NEVER touched: `control/inbox.md`, `control/status.md` (no claim
file accompanies this session per the #135/#142 precedent — this born-red card
+ the immediately-opened PR is the in-flight signal). Verified pre-flight at
origin/main HEAD e88af57: no open PRs, `control/claims/` empty (README only),
no new inbox ORDER touching the registry.

## Close-out

**Shipped (session PR #161):** `docs/adopters.md` regenerated from live tree
truth (10 repos scanned, `Generated: 2026-07-11T01:28:27Z` — the snapshot
time). All four kit-seat wave repos read **tree=v1.8.0 · pin=v1.8.0 ·
current**: superbot-next, websites, gba-homebrew, venture-lab. Parallel-worker
lane at snapshot time: fleet-manager, superbot-games, and trading-strategy
ALREADY tree=v1.8.0 · pin=v1.8.0 (their upgrades merged before the scan) —
only their self-reports lag (DRIFT rows below), the expected mid-wave state,
deliberately NOT hand-fixed. superbot stays pin-only stale v1.0.0;
pokemon-mod-lab not adopted. Verified locally: `python3.10 -m pytest tests/
-q` → **938 passed**; `python3.10 src/build_bootstrap.py` rebuild
byte-identical (dist byte-pin clean); ruff clean; `check_program_law` OK;
`check_idea_index` OK; `check --strict` red only on this card's own born-red
hold (this flip clears it). One guard-fires.jsonl append (the check run's
session-log fire) rides this flip commit, matching prior sessions.

**Surfaced, not resolved (registry protocol — reconcile at the SOURCE):**
5 DRIFT repos, 4 self-report lag + 1 tree-internal: superbot-games (both lane
heartbeats v1.7.1), trading-strategy (v1.7.1), gba-homebrew (v1.6.0 — now
chronic, surviving its third regen), fleet-manager (v1.7.0) — all tree=v1.8.0,
the same upgrade-doesn't-touch-the-heartbeat cause the v1.7.0-wave card's 💡
already named (superbot-next is the counterexample: its wave PR updated the
`kit:` line, and its row is the only fully-clean one); plus the kit's own
config-pin v1.0.0 vs dist v1.8.0 (deliberately untouched pending the §7
version-truth ruling). Also re-confirmed #160's 💡: build printed
"622084 bytes" while `wc -c dist/bootstrap.py` = 625066 — byte-pin was
git-diff clean so harmless, but the false-mismatch print is still live.

**💡 Session idea:** currency rows carry no per-repo evidence anchor — only
the global `Generated:` stamp. This session's brief called the trio "mid-wave"
yet the tree already read v1.8.0; nothing in the registry lets a reader
resolve that dispute without rerunning the scan. Have the currency verb
record, per row, the scanned tree ref (the fetched HEAD commit SHA of each
adopter at scan time, which the fetcher already resolves) — every row becomes
independently citable/reproducible ("scanned at <sha>"), snapshot-timing
questions become evidence lookups, and diffing two committed registries shows
exactly which repo moved between scans.

**⟲ Previous-session review:** the release-v1.8.0 close-out (#160) was
rigorous where it counts — machine-checked status.md block preservation,
three-way sha256 verification of the release asset, and an honest regen that
showed all 7 adopter rows stale minutes before the wave (correct, not
alarming). One improvement it surfaces: its close-out set next-slice = the
distribution wave but did not remind wave workers that the upgrade checklist's
last step (update the heartbeat `kit:` line) is what keeps the NEXT regen
drift-free — 4 of 7 wave upgrades skipped it and this session's registry
manufactured 5 DRIFT rows by construction. Until the upgrade verb self-heals
the heartbeat (the v1.7.0-wave card's captured idea — promoting it is now
clearly worth it, three waves of evidence), the wave-dispatch order text
should carry that one-line reminder.
