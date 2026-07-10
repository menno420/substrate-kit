# 2026-07-10 — gen-2 wave-2 session close: release-readiness note + full session ledger

> **Status:** `in-progress`

- **📊 Model:** claude-opus-4-8 · high · gen-2 wave-2 close — status-ledger
  overwrite + release-readiness assessment (no release cut)

## Scope

One PR, touching ONLY `control/status.md` and this card in `.sessions/`. NEVER
`control/inbox.md`, NEVER anything under `bench/`. No src/ change → no dist
regen.

- **Assess release-readiness (ITEM 3 — assess, do NOT cut).** Read the release
  path (`.github/workflows/release.yml`), the version source (`KIT_VERSION` in
  `src/engine/lib/config.py` = 1.6.0; dist header = 1.6.0; pyproject = 1.6.0),
  and the CHANGELOG. Last released = v1.6.0 (2026-07-09). The [Unreleased]
  section has accumulated ~12 entries (new checkers + `adopt --lane` +
  upgrade/engagement/telemetry/adopter fixes + the B1 run-3 record) — a
  MINOR-worthy v1.7.0 IS warranted, but NO bump is prepared (KIT_VERSION still
  1.6.0, no [1.7.0] section, no tag), so a dispatch would fail its own guard.
  Queued as a ⚑ needs-owner one-click (release NOT triggered — a publishing
  action adopters consume, deliberately owner-fired overnight) + an
  agent-available prep-bump PR under `next`.
- **Overwrite `control/status.md` wholesale** with the full wave-1+wave-2
  ledger: THIS lane's 12 merged PRs (#84, #86–#92, #99, #100, #106, #111 —
  each verified against main by its own squash-merge commit), orders 001–009
  done, no new order ≥010, the twelve six-field ⚑ OWNER-ACTIONs (the ten
  carried from the #109 night-cap status + new item 11 "automatically update
  branches" + new item 12 release-readiness), and the agent-available `next`
  list. Sibling facts carried, not clobbered; sibling heartbeat
  `control/status-gba-homebrew-trackb.md` untouched (one-writer rule).

## 💡 Session idea

A release is the one queued action this close identifies as *warranted but not
prepared* — the interesting gap. The workflow is agent-reachable
(`workflow_dispatch`), so the naive move is to fire it; but two things stop
that being right overnight. First, honesty: a versioned release is consumed by
downstream adopters, so it wants an explicit owner action, not an autonomous
one — the same "publishing is owner-gated even when technically reachable"
doctrine that governs tag pushes. Second, mechanics: the refuse-to-release
guard would reject a dispatch today because no bump is staged. The
generalizable shape: when you find accumulated-but-unreleased work, split it
into the *prep* half (bump version + roll CHANGELOG + regen pin — agent-ownable,
queue it as ready work) and the *publish* half (the dispatch — owner-ownable,
queue it as a one-click). That keeps the agent lane productive right up to the
last click without ever taking the publishing action itself.

## ⟲ Previous-session review

The prior card (`2026-07-10-queue-reconcile-enabler-sync.md`, shipped #111)
closed `complete`, `check --strict` green, suite 819. It reconciled
`queue-state.md`, recorded the auto-merge stall class in CAPABILITIES, and
added `synchronize` to the enabler so it re-arms on fix-pushes — but it
explicitly left the *staleness* half of the behind-stall open, flagging that
the full cure is the repo setting "automatically update branches". This close
promotes that residual into a first-class six-field ⚑ (OWNER-ACTION 11) so it
sits in the owner's ledger rather than only in a workflow comment, and folds
the #111/#106 facts into the wave-2 status ledger. No code defect inherited;
the learned CI lesson (from #106's first-CI failure — the session-gate requires
`💡 Session idea` + `⟲ Previous-session review` + a completed Status at merge)
is applied to this card's structure up front.

## Outcome

_(to be completed at the closing commit — check --strict output pasted below)_
