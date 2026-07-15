# 2026-07-15 · adopters-currency-refresh

> **Status:** `complete`

- **📊 Model:** Fable-class
- Scope: ORDER 024 first-rebooted-wake ack + docs/adopters.md currency regen (PR #382, branch claude/adopters-currency-2026-07-15).

## Record

- Boot: hard-synced to origin/main 58b3f80; preflight 7/7 legs green (pytest 1568 passed, 1 skipped). Tree clean, no rescue branch needed.
- ORDER 024 (EAP extended through 2026-07-21): acknowledged + done on this first rebooted wake per its done-when; this session armed no triggers itself — routines coordinator-managed this wake; a read-only trigger inventory observed a coordinator-bound failsafe post-dating ORDER 024's do-not-re-arm line, recorded neutrally in the heartbeat Routine state block and flagged for owner review; heartbeat orders line now `acked=001–024 · done=001–024`.
- Registry regen: `python3 dist/bootstrap.py currency` at 2026-07-15T04:37:23Z, 12 repos scanned read-only, exit 0 first try. DRIFT 7 repos → 5: idea-engine + trading-strategy drift cleared, venture-lab now self-reports v1.17.0, superbot-next self-report advanced v1.15.0 → v1.16.0. Remaining DRIFT = chronic lane-owed heartbeat `kit:`-lag (superbot-next, websites, superbot-games ×3 lanes, superbot-mineverse) + kit's known tree-internal config-pin v1.0.0 row.
- Friction (converted to idea below, no new owner ask): first push rejected — the branch name `claude/adopters-currency-refresh` still exists on origin as a SPENT survivor of its 2026-07-13 merged PR (the ORDER 022/023 branch-litter class, live-hit at session open). Resolved by renaming to the dated branch; no force-push over evidence.

## Session enders

- 💡 **Session idea:** session-OPEN branch-collision preflight — before the first push, run `git ls-remote origin refs/heads/<branch>`; if the ref exists and its tip is an ancestor of origin/main (a spent merged-PR survivor), auto-suffix the branch with the date instead of colliding. The litter class now has guards at session END (v1.16.0 stop-hook merged-push guard) and cleanup (staged branch-sweep.yml), but session OPEN is unguarded — this wake hit it live (push rejected, HTTP 403 + non-fast-forward, on a name whose PR merged two days ago). Cheapest home: the session-open ritual doc + optionally a `bootstrap claim`/open helper check. Dedup: grepped docs/ideas/ + .sessions/ — order-claim-cross-branch-collision-2026-07-14.md covers claim-file collisions, not branch refs; no existing idea covers open-time ref collisions.
- ⟲ **Previous-session review:** the v1.17.0-wave closeout card (2026-07-14-v1.17.0-wave.md) is a model wave record — per-adopter merge table, three-way sha256 pin, and an honest "legitimate no-op" call on the zero-delta apply-docs pass. Gap this wake's rescan exposed: its drift report named six lagging self-report rows but the baton assigned the `kit:` bump to no concrete lane, and only 2 of 6 healed overnight — which validates its own 💡 (paste-ready per-repo fix lines / one canonical bump owner). Concrete improvement carried forward: this wake's baton item 2 makes the currency re-run explicitly conditional on the lane bumps, so the next regen is a check, not a hope.
