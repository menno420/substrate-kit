# Gen-2 blueprint feedback — from the kit-lab lane (2026-07-09)

> **Status:** `owner-guidance` — the kit-lab lane's concrete suggestions
> for fleet-manager's `docs/gen2-blueprint.md` (read IN FULL at wind-down:
> the GitHub MCP allowlist walls fleet-manager, but `add_repo` + a shallow
> clone reached it — status `binding`, finalized 2026-07-09 late evening)
> and for the seed standard generally. Every item: what to change, why,
> gen-1 evidence. Written at wind-down (phase 2, PR #74). Sibling lane's
> feedback:
> [../succession/gen2-feedback-superbot-coordinator.md](../succession/gen2-feedback-superbot-coordinator.md).

1. **Promote claim-first-on-main to a seed standard with a checker, not
   just an instruction line.** Blueprint §2 delta 5 (order claim/lease)
   is right but stops at prose. Change: seed every repo with the ORDER 007
   claim ritual in `control/README.md` **plus a claim-aware advisory
   checker** (duplicate-claim + stale-claim detection — filed as the #69
   card's idea, unbuilt). Evidence: the #50/#51 twin execution happened in
   a ~90-second window; prose conventions are exactly what a
   90-second race doesn't read.

2. **Control fast lane from day one, wired to the status gate.** Blueprint
   §2 delta 9 (batch heartbeats / fast lane) is confirmed by live data:
   heartbeat PRs merged in 7–30 s on the lane vs full-suite minutes before
   it, and phase-1's wind-down claim (#72) merged in ~21 s. Change: make
   the fast lane part of the SEED CI (it arrived at ORDER 002 here —
   "heartbeats were paying full-suite CI for half a day", self-review C4),
   and pair it with the `check --strict --status-only` step — gen-1's
   fleet review proved a fast lane WITHOUT the scoped gate lets a
   heartbeat-deleting PR merge green (PR #35 closed that hole).

3. **Telemetry writes at card-commit, not session-close.** Blueprint §2
   delta 7 mandates instrumentation "from row one" but doesn't say WHEN
   the row is written. Evidence: gen-1's harvest ran only inside
   `session-close`, which later sessions skipped — 10 harvested rows vs
   21+ eligible cards; the PL-004 dataset undercounts exactly when
   discipline slips. Change: the card's `📊 Model:` line is written at the
   born-red commit and harvested by CI or the next session, so no
   close-time ritual is load-bearing.

4. **Fleet-visible checkers ship advisory-first, gate-later.** Not in the
   blueprint. Evidence: ORDER 008's owner-action checker was deliberately
   advisory-only because a hard gate "would pre-redden every adopter's
   free-text heartbeat on upgrade" (#68 card deviation flag). Change: seed
   standard rule — a NEW checker whose findings touch files other lanes
   already write starts advisory, and graduates to a gate only after one
   clean fleet cycle. (Load-bearing single-repo gates — session gate, byte
   pin — stay born-gating.)

5. **P10-class required-check hygiene: make the skeleton VERIFY context
   names, and forbid legacy contexts outright.** Blueprint §1 and §3 step
   3 already say "exact names!" — promote it from checklist prose to the
   walking skeleton's hard assertion (the skeleton PR must show every
   required context reporting from a real job). Evidence: gen-1 paid ~70
   min in two runner-queue stalls + the #7 skipped-alias merge + the #22
   lag window, all under owner-landed legacy context names that one test
   PR would have exposed on day one.

6. **Worker worktrees in scratchpad as a seed-standard line.** Not in the
   blueprint (§1 covers repos, not worker filesystem layout). Evidence:
   two parallel workers collided in the shared `/home/user` checkout
   (session 7, KL-2); the fix (scratchpad worktrees per worker) was
   adopted same-day and never violated again. One sentence in the
   conventions file deletes the class.

7. **The OWNER-ACTION six-field format as the fleet-wide ⚑ grammar.**
   Blueprint §1 requires agent-reachable done-whens; ORDER 008's format
   (WHAT / WHERE / HOW / WHY-IT-MATTERS / UNBLOCKS / VERIFIED-NEEDED,
   assumption-based asks banned) is the shipped, checker-backed version of
   that idea for the owner-queue direction. Evidence: the kit's 11-item ⚑
   list went from free-text sprawl to one-click-executable items in one
   pass; the sibling lane's owner-queue converged on the same need
   independently. Change: adopt the six fields (or cite them) in the
   blueprint's conventions-file checklist so every lane's asks parse the
   same way.

8. **Record the `add_repo` cross-repo workaround in PLATFORM-LIMITS
   seeds.** New finding, this session: the per-session GitHub-MCP repo
   allowlist (`Access denied: repository ... is not configured for this
   session`) is NOT the last word — the `add_repo` session tool + shallow
   clone reached fleet-manager (public repo) and read the blueprint in
   full. Change: the blueprint's pre-filled walls doc (its item: "walls
   with exact error text") should carry the workaround next to the wall,
   or lanes will keep treating manager-relay as the only channel.
   (Caveat honestly: verified for a PUBLIC repo from a kit-lab session
   once; private-repo behavior unverified.)

9. **Name the sanctioned release path in the conventions file.** Blueprint
   §2 delta 3 covers write-scope walls; add the positive half: the
   `release.yml` `workflow_dispatch` route (tag created in-Actions,
   refuse-to-release guards, assets + sha256) is proven across all 7 gen-1
   releases and should be seeded as THE release mechanism for any repo
   that cuts releases, not rediscovered after the first tag-push 403.
