# Session card — 2026-07-15 · archive-ready close-out surface PLAN

> **Status:** `complete`

## What happened

Baton item 1 (control/status.md § Next-2 at sync HEAD 0984d95): the
archive-ready close-out surface idea self-routes to the structured-plan lane,
so this session shipped the PLAN, not the build — PR #410.

- Wake probe: `python3 dist/bootstrap.py currency --check` → exit 0 (registry
  current, no drift slice due); no inbox ORDER above 024; claims README-only;
  zero open PRs at scan.
- Shipped: `docs/planning/2026-07-15-archive-ready-close-out-plan.md` —
  surface contract (`archive-prep` draft verb reusing the KL-5
  `ensure_draft` pattern; REQUIRES-PROBE slot semantics grounded in the
  2026-07-11 stale-routine-record failure; advisory-red `check --strict`
  first per PL-008), evidence-source split (tree-local fills vs
  session-resolved slots — engine stays stdlib-only/offline), 3
  decide-and-flag design decisions, slices S1–S5 each a follow-up PR.
- Idea lifecycle flipped: `docs/ideas/archive-ready-close-out-surface-2026-07-11.md`
  state captured → routed (outcome stays `open` until a build slice merges);
  `docs/ideas/README.md` backlog line refreshed with the plan link.
- Heartbeat refreshed wholesale (⚑ blocks carried byte-identical; baton now
  names S1 as next).

## Verify

At commit 4a98a34:

- `python3 scripts/preflight.py` → `preflight: OK — 9 leg(s) green`
  (pytest 1652 passed 1 skipped; dist-byte-pin; ruff; idea-index;
  retro-index; changelog-structure; taxonomy-sync; program-law;
  bench-integrity).
- `python3 dist/bootstrap.py check --strict` → exit 0; only hold is this
  card's own designed born-red gate ("HOLD (by design)"); the 3
  staged-regen-lag advisories are pre-existing and never exit-affecting.

## Enders

💡 Session idea: root-anchor the `currency` roster path — `currency --check`
run from any cwd other than the repo root exits 1 with "no roster at …", a
pure cwd artifact that two heartbeats now carry a prose warning about.
Resolve `docs/adopters.md` relative to the bootstrap entrypoint's repo root
(or `git rev-parse --show-toplevel` fallback) so the probe is
location-independent and the warning prose can be deleted. Dedup-checked:
`currency-check-registry-delta-preflight-2026-07-15.md` is a different idea
(registry-delta preflight), no cwd/roster-resolution idea exists.

📊 Model: Claude Fable

⟲ Previous-session review: the #409 currency-regen session was clean — it
correctly read the mid-scan `Connection reset by peer` as a network blip,
retried once, and wrote the retry guidance into the heartbeat State section
so the next wake doesn't misread it. Workflow improvement: its heartbeat
"Registry current" line hard-coded the regen commit/PR, which the very next
wake (this one) had to rewrite while carrying the same standing prose — the
State section would drift less if per-wake facts lived only in "This wake"
and State kept only standing invariants; adopted that split in this wake's
heartbeat.

⚑ Self-initiated: none — the slice was baton-named (control/status.md
Next-2 item 1); the only self-chosen elements are the plan's three
decide-and-flag design decisions, flagged in the plan §4.
