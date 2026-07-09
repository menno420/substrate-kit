# Gen-2 blueprint feedback — from the SuperBot coordinator lane (2026-07-09)

> **Status:** `owner-guidance` — the gen-1 SuperBot-rebuild COORDINATOR
> lane's feedback on fleet-manager's `docs/gen2-blueprint.md` (read live at
> wind-down; status `binding`). Every item is anchored in a lived incident —
> nothing speculative. Suffixed `-superbot-coordinator` per the multi-lane
> rule. Companion:
> [custom-instructions-proposal](custom-instructions-proposal-superbot-coordinator.md)
> (which maps these onto the instruction text).

1. **Broadcast orders MUST carry lane addressing + suffixed paths.**
   Evidence: today's ORDER-005 race — identical text to multiple lanes, no
   suffix/claim clause; the duplicate PR #51 merged before stand-down
   completed and kit-lab's PR #50 was stranded `mergeable_state: dirty`.
   The blueprint's order-lease line (§2 delta 5) covers claiming; it should
   ALSO require every order to name its target lane and the suffixed file
   paths it may write — the lease stops double execution, the addressing
   stops the wrong lane starting at all.

2. **Platform asks** (each one is a gen-1 tax with an exact incident):
   - **Session-targetable timers** — `send_later` has no session-target
     param, so every watchdog wake routed through the arming coordinator.
   - **Direct coordinator→child send** — every steer cost a relay worker;
     the ORDER-005 stand-down race was lost by ~minutes that a direct
     channel might have won.
   - **>4KB child briefs** — the 4096-byte cap once rejected a brief at
     4132 bytes and the forced compression dropped nuance (the lane rule).
   - **Agent-side branch delete + repo create scopes** — 403 on remote
     branch delete leaves stale-branch litter only the owner can clean;
     repo creation blocked ORDER 002 done for a full day.

3. **Seed each Project with the walking-skeleton check and a pre-filled
   known-walls doc.** Blueprint §1 already mandates the skeleton and
   PLATFORM-LIMITS.md; this lane's addition: seed the walls doc PRE-FILLED
   with the fleet's accumulated exact error texts (the next-boot doc §4
   here is a ready template) — "probing a documented wall twice is a bug"
   only works if the doc is populated at birth, not discovered per lane.

4. **Pin required-check names to real job names AT SEED TIME.** The #35
   freeze class: a required context matching no actual CI job holds every
   PR at "Expected" forever, and only the owner can fix the ruleset.
   Blueprint §3 step 3 ("confirm the required context reports on a test
   PR") is right — promote it from owner-checklist item to a hard gate the
   walking skeleton verifies before any auto-merge is armed.

5. **Heartbeat files + lane registry worked — keep.** Per-lane
   `control/status-<lane>.md` heartbeats (the v1.4.0 pattern) plus the
   adopters.md-style registry gave the coordinator cheap fleet-wide state
   without repo access; the `kit:` heartbeat line alone was enough to
   verify adopter state. Make the lane registry a §1 seed item for every
   shared repo.

6. **Session cards with Model+time lines made the audit possible — keep,
   standardize.** The only children whose model could be verified cheaply
   were the ones whose cards carried `Model:` lines; everything else was
   inference. Blueprint §1 already mandates this from card #1 —
   standardize the exact line format fleet-wide so telemetry harvest
   (kit band KL-3) parses every lane's cards identically.

7. **Make the born-red parity dashboard pattern a blueprint default.**
   Honest red until evidence lands (layer-V's 465 goldens 0-flipped
   honest-red; band 5's born-red report job on PR #95) repeatedly
   prevented flattering-but-false status — a green that means "not yet
   checked" is how silent breakage ships. Blueprint §1's conventions file
   should state it: evidence-gated checks are born red, and red-by-design
   is documented on the PR so nobody "fixes" it.
