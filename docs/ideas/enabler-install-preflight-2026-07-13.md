---
state: captured
origin: consumer:menno420/idea-engine
shipped_pr: null
shipped_repo: null
merged_date: null
outcome: open
---

# Auto-merge-enabler: install-time preflight for required checks + branch allowlist (2026-07-13)

> **Status:** `ideas`
>
> **State:** captured → route: quick-win (install-step verification in the
> enabler distribution path / install docs).
> **Origin:** consumer — three independent hits on the 2026-07-12→13 night
> run: superbot-idle's enabler sat INERT ("zero required checks — safely
> refuses to arm", fm OQ B#50), gba-homebrew #76 merged with the enabler
> INERT pending OQ-GBA-ROM-RULESET (fm OQ B#51), and idea-engine had to
> patch the allowlist post-install (PR #272 "fix: add claude/ to
> auto-merge-enabler branch allowlist") with its outbox ASK 001 flagging
> that a kit upgrade will clobber the local fix. Cross-cited by
> `docs/reports/2026-07-13-night-run-adopter-outcomes.md` §a.

## The gap

The enabler installs cleanly into repos where it cannot function: no
required checks configured (refuses to arm — correct, but silent until a
PR parks) or the target branch pattern missing from its allowlist. The
refusal-to-arm is designed behavior; the missing piece is an install-time
preflight that verifies both preconditions and reports what the owner must
configure — so the INERT state surfaces at install, not at the first
parked PR. Related: `engagement-wiring-strength-verification-2026-07-12.md`
(required-check status unverifiable by agents — the preflight output may
need to route to the owner queue rather than assert).

## Size / risk

Small (install-step check + report line); no change to the enabler's
runtime behavior; reversible.

## Progress

- **Branch-allowlist half — in flight, PR #321** (`claude/clever-sagan-bro9uh`):
  `src/engine/checks/check_automerge_preflight.py`, a self-silencing
  `check`-time advisory that flags when the installed
  `auto-merge-enabler.yml`'s branch allowlist drifts from
  `automerge.branch_patterns` (the idea-engine hand-patch/stale-allowlist
  class). Advisory-only, compares the branch expr (version-skew-robust).
- **Install-time half — SHIPPED, PR #344** (`claude/enabler-install-preflight`,
  ORDER 019 item 4): `src/engine/enabler_preflight.py`, called by `adopt`
  (and so by `upgrade`) whenever the live enabler is planted/regenerated,
  right after the repo-settings checklist. Best-effort ONLINE verification
  of the two owner-UI preconditions via the GitHub API (stdlib urllib,
  `GITHUB_TOKEN`/`GH_TOKEN` honoured, origin slug read from `.git/config` —
  no subprocess): `"Allow auto-merge"` OFF → loud line naming the toggle;
  ZERO required status-check contexts on the default branch → loud INERT
  line (same rules endpoint the enabler's refuse-to-arm guard counts);
  required-context name mismatch → line naming the actual required contexts
  to pin in config. Advisory + fail-open: no git / non-github origin /
  offline / tokenless visibility / HTTP or JSON errors each collapse to one
  honest UNVERIFIED line pointing at the manual checklist — an offline
  install never fails or slows on this. The branch-allowlist condition is
  deliberately NOT re-checked here (install-time regen forces workflow ==
  config; later drift is #321's check-time advisory).
- **Remaining owner-UI residue**: the preflight *reports* what is
  misconfigured; it cannot *set* repo settings (no workflow/API-write path)
  — flipping "Allow auto-merge" and requiring the context stay owner
  clicks, now prompted at install time instead of at the first parked PR.
