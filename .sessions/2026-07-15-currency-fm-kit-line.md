# 2026-07-15 · currency-fm-kit-line

> **Status:** `complete`

- **📊 Model:** Fable 5 · medium · docs-only
- Scope: currency regen — fleet-manager's control/status.md grew a
  `kit: v1.17.0` self-report line (delegated-pen PR fm#232, 12:58:30Z) that
  the 12:09:23Z registry didn't record; re-ran
  `python3 dist/bootstrap.py currency` to regenerate docs/adopters.md. Plus:
  captured the dangling `currency --check` preflight idea (baton pointed at
  docs/ideas/README.md § Backlog, but it existed only as a 💡 in the #389
  session card) into a proper idea file + Backlog row.
- ⚑ Self-initiated: the idea capture (part B) —
  docs/ideas/currency-check-registry-delta-preflight-2026-07-15.md + README
  § Backlog row, crediting the originating #389 card; fixes the dangling
  baton pointer. (Part A, the currency regen, was baton/coordinator-routed.)

About to (opening declaration, retained): re-run the currency discovery so
the registry records fleet-manager's new `kit:` line (4 known-DRIFT rows
expected unchanged); capture the `currency --check` registry-delta preflight
idea into docs/ideas/ + README § Backlog; heartbeat + flip.

## Record

- Boot: hard-synced to origin/main 4e29182 (#390); inbox tops at ORDER 024
  (all acked+done per the heartbeat orders line); control/claims/ held
  README only; zero open PRs at the ~13:07Z scan. Born-red card + claim
  (`bootstrap claim` rendered, round-trip verified) = first commit c480630;
  PR #391 opened READY immediately after.
- Shipped (e79695c): `python3 dist/bootstrap.py currency` at
  2026-07-15T13:14:20Z — 12 repos scanned read-only, exit 0 first try.
  docs/adopters.md regenerated: fleet-manager row flipped
  `no kit: line` → self-report `v1.17.0` (verdict stays `current`); the only
  other delta is the `Generated:` stamp. All 4 known-DRIFT rows
  byte-unchanged (superbot-next v1.16.0, superbot-games v1.15.0 + lanes
  v1.7.1, superbot-mineverse v1.16.0, kit tree-internal v1.0.0 pin).
  Kit-side registry regen only — no adopter repo touched (Q-0261.3). Same
  commit: idea file + README § Backlog row (part B above). Guard-fires
  telemetry delta committed per checker instruction (999f81e).
- Verify (at e79695c): `python3 scripts/preflight.py` → 8/8 legs green —
  `1594 passed, 1 skipped in 44.80s` (pytest); ruff `All checks passed!`;
  dist-byte-pin; idea-index (`check_idea_index: OK` — new idea file
  indexed); retro-index; changelog-structure; program-law; bench-integrity.
  `dist/bootstrap.py check --strict` → designed born-red HOLD only (this
  card, pre-flip), plus known advisories: staged-regen-lag ×3 and the
  honest `unrecorded` model-line-effort nags — now ×2, the third
  (2026-07-14-seat-digest-adaptive-clip) aged out of the newest-10 lint
  window; terminal disposition unchanged, no tiers invented. Nothing new
  red.
- Heartbeat (ee46155): control/status.md overwritten wholesale — this wake
  recorded; ⚑ blocks carried byte-identical (diff-verified: no ⚑ header
  lines in the diff); `kit:` line plain; orders line unchanged
  (acked=001–024 · done=001–024); next-2 baton refreshed (1: grounded-skills
  window ~07-19..26 · 2: build the `currency --check` verb, now captured;
  conditional currency re-run if another adopter `kit:` line bumps).
- This flip commit also deletes the claim
  (control/claims/claude-currency-fm-kit-line.md), per the #390 convention.

## Enders

- 💡 Session idea: **baton pointer resolution — verify heartbeat file
  references resolve.** This session existed in part because the previous
  baton asserted the `currency --check` idea was "in docs/ideas/README.md
  § Backlog" when it never was — a dangling prose pointer no checker
  catches. The retro-index checker (#388) proved the pattern for
  docs/retro/; extend it (or add a sibling advisory) that scans
  control/status.md for repo-relative path references (`docs/...`,
  `.sessions/...`, `scripts/...`) and warns when one doesn't exist on disk —
  advisory-only, path-existence only (never prose-claim adjudication).
  Dedup: grepped docs/ideas/ — retro-docs-reachability covers docs/retro
  README links, idea-index covers idea-file linkage, heartbeat-verb is a
  mechanical writer; nothing checks heartbeat path pointers.
- ⟲ Previous-session review (2026-07-15-model-line-payload-sweep, PR #390):
  disciplined honesty under pressure — it refused to invent effort tiers,
  chose `unrecorded` + a terminal disposition, and captured the sanctioning
  idea instead of silently eating the nags. Its adopter-bump precheck also
  correctly concluded "no currency re-run warranted" at 12:3xZ — and was
  stale by 12:58Z when fm#232 landed, which is exactly the staleness class
  its own baton's `currency --check` idea addresses. Concrete improvement:
  its baton item 2 pointed at a Backlog entry that didn't exist (the 💡 was
  card-only) — batons that cite a docs/ location should be written only
  after the pointer is verified on disk, or the capture should ride the
  same PR that writes the baton; this session's 💡 above proposes the
  enforcing check.
