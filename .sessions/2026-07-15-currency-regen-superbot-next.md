# Session · 2026-07-15 · currency-regen-superbot-next

> **Status:** `complete`

Intent: currency slice — `python3 dist/bootstrap.py currency --check` exited 1 at sync HEAD c30f714 (superbot-next roster row stale: recorded v1.16.0, live kit v1.17.0); regenerate docs/adopters.md via the discovery tooling (generated file, never hand-edited).

- **📊 Model:** Claude Fable 5 · small · registry regen (drift-probe-fired)
- ⚑ Self-initiated: no — slice mandated by the drift probe (`currency --check` exit 1 is the standing regen trigger, #392 turnkey convention).

## What shipped (PR #406)

- `docs/adopters.md` regenerated via `python3 dist/bootstrap.py currency` (commit efb4ee5): superbot-next row flipped `⚠️ DRIFT · current` → `current` (self-report caught up to v1.17.0), its DRIFT-detail bullet removed, `Generated:` stamp 13:14:20Z → 20:38:20Z. Net change: 2 insertions, 3 deletions — one row plus one drift bullet; remaining DRIFT set unchanged at 3 repos (substrate-kit pin-internal v1.0.0 · superbot-games 3-lane self-report lag · superbot-mineverse self-report lag), all owned at the adopter source.
- Post-regen `python3 dist/bootstrap.py currency --check` → exit 0 (12 repos, rows-only compare).
- Operational note: the first regen attempt died with `urllib.error.URLError: <urlopen error [Errno 104] Connection reset by peer>` mid-fleet-scan; a single retry succeeded end-to-end. Transient proxy/network blip, not a wall — recorded per the attempt-once-capture-exact-error discipline.
- Verify (at efb4ee5): `python3 scripts/preflight.py` → 9/9 legs green (pytest 1650 passed, 1 skipped; dist-byte-pin; ruff; idea-index; retro-index; changelog-structure; taxonomy-sync; program-law; bench-integrity). `dist/bootstrap.py check --strict` → exit 0; only the designed born-red HOLD (this card, pre-flip), the known staged-regen-lag ×3, and the required-unverified NOTE; guard-fires telemetry delta committed with the heartbeat (776fa68).

## 💡 Session idea

Currency regen retry-once resilience: this slice's first `currency` run crashed with a raw urllib traceback on one transient `ConnectionResetError` mid-scan — 11 of 12 repo fetches wasted because the 12th reset. The fetch path (`dist/bootstrap.py` `_urllib_get` → `scan_fleet`) could wrap each raw-content GET in a single bounded retry (one re-attempt, short backoff, then surface the error with the repo/path named instead of a traceback), so a routine-fired wake doesn't burn its slice on a network blip. Dedup: `grep -ril "retry" docs/ideas/` finds no currency/fetch-retry idea at HEAD.

## ⟲ Previous-session review

The #405 session (gate-verify-command) left an exemplary trail: its heartbeat named the exact probe discipline ("run the probe FROM THE REPO ROOT — from elsewhere it exits 1 with 'no roster', a cwd artifact") which this session used verbatim to trust its own exit-1 as a real regen signal rather than a cwd artifact — a one-line wake note that pre-empted a misdiagnosis class. Miss, small: its "This wake" line recorded "`currency --check` exit 0 ... no regen slice due" as a point-in-time fact without a timestamp on the probe itself; superbot-next's self-report flipped between that probe and this one, which is fine (the registry lags by design), but a probe timestamp would have let this session say precisely when the drift window opened. Improvement worth keeping: heartbeat probe claims should carry their own UTC stamp, not just the header's `updated:` stamp — one token of precision per claim makes cross-wake drift windows measurable.
