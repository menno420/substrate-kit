# 2026-07-15 · adopter-currency-websites-v1170

> **Status:** `complete`

- **📊 Model:** Claude 5 · medium · docs-only
- Scope: adopter-currency refresh — websites now self-reports `kit: v1.17.0`;
  re-run `python3 dist/bootstrap.py currency` to regenerate docs/adopters.md
  and retire the DRIFT rows the bump clears (5 repos at the 04:37Z scan), per
  the heartbeat next-2 baton item 2.
- ⚑ Self-initiated: coordinator-routed adopter-currency slice (baton item 2;
  no inbox ORDER above 024; claims dir held README only; zero open PRs at the
  12:0xZ scan).

## Record

- Boot: hard-synced to origin/main 7473869 (#388). Born-red card + claim =
  first commit 80b9ca3; PR #389 opened READY immediately after.
- Shipped (da6584f): `python3 dist/bootstrap.py currency` at
  2026-07-15T12:09:23Z — 12 repos scanned read-only, exit 0 first try.
  docs/adopters.md regenerated: websites row flipped DRIFT → `current`
  (self-report v1.17.0 = tree v1.17.0); DRIFT 5 repos → 4. Remaining rows
  preserved per the benign-red doctrine (chronic lane-owed self-report lag:
  superbot-next v1.16.0, superbot-games status.md v1.15.0 +
  mining/exploration v1.7.1, superbot-mineverse v1.16.0; plus kit's known
  tree-internal config-pin v1.0.0 row). Docs-only: no engine change, dist
  byte-pin untouched.
- Claim hygiene (same commit): the hand-written claim bullet was unparseable
  (`claims-format` advisory) — re-rendered via `bootstrap claim` (round-trip
  verified). Guard-fires telemetry delta committed per checker instruction.
- Heartbeat (f8372e5): control/status.md records this wake; next-2 baton
  item 2 → model-line payload sweep (the 4 advisory-named older cards);
  owner-ask blocks carried byte-identical; orders line unchanged
  (acked=001–024 · done=001–024).
- Verify: `python3 scripts/preflight.py` → 8/8 legs green (pytest 1594
  passed, 1 skipped; ruff; dist-byte-pin; idea-index; retro-index;
  changelog-structure; program-law; bench-integrity);
  `dist/bootstrap.py check --strict` → designed born-red HOLD only, plus
  known advisories (staged-regen-lag ×3, model-line ×4 older cards).

## Enders

- 💡 Session idea: **`currency --check` — a cheap registry-delta preflight.**
  Every wake currently decides "is a currency slice due?" by hand-fetching
  adopter self-report lines and eyeballing them against the registry (the
  #388 heartbeat did exactly this in prose), or by running the full regen
  and diffing. A `bootstrap.py currency --check` verb that fetches only the
  self-report/tree evidence and exits 0 (registry current) / 1 (regen would
  change rows) would make the wake-scan turnkey, and this very slice would
  have been detectable by any session instead of needing a coordinator
  route. Dedup: grepped docs/ideas/README.md — no entry covers a currency
  delta precheck (order-claim/heartbeat-tally ideas are adjacent but about
  claims and delegated writes, not registry staleness detection).
- ⟲ Previous-session review (2026-07-15-retro-index-checker, PR #388): a
  model self-initiated slice — ladder discipline explicit (adopter-bump
  check before choosing the rung), parity pins updated in the same PR, and
  the 💡 was properly deduped and scoped. Improvement it surfaces: its
  ~11:3xZ adopter spot-check result ("websites v1.15.0 — no currency slice
  due") lived only as heartbeat prose and was stale within the hour when
  websites bumped; a machine-checkable currency-due signal (this session's
  💡) would let the next wake detect the flip itself rather than relying on
  coordinator recon to re-derive it.
