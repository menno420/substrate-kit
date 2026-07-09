# Project review — SuperBot-rebuild coordinator lane (2026-07-09)

> **Status:** `audit` (dated snapshot — written by the SuperBot-rebuild
> COORDINATOR lane, filename suffixed `-superbot-coordinator` per the
> owner's multi-lane rule so it never collides with kit-lab's unsuffixed
> ORDER 005 deliverables; ground truth is the coordinator's own session
> ledger plus repo-checkable facts verified live at 2026-07-09 ~17:3xZ;
> where the coordinator's vantage cannot verify a claim, the doc says so)

This is the companion doc to
[self-review-2026-07-09-superbot-coordinator.md](self-review-2026-07-09-superbot-coordinator.md).
It reviews a DIFFERENT Project than kit-lab's
[project-review-2026-07-09.md](project-review-2026-07-09.md): the
**SuperBot-rebuild Project** — the coordinator and its child sessions that
rebuilt superbot into superbot-next and are now live-testing it. It is filed
in this repo because substrate-kit's `docs/retro/` is where the gen-1 retro
protocol lives, and because the fleet's lane collision of today (see §b) is
itself part of the record.

## (a) What this Project is, and its true current state

**The SuperBot-rebuild Project** is a coordinator session plus a fleet of
child sessions that executed steps 7–13 of the canonical plan
(superbot → substrate-kit → superbot-next), then moved into the live-testing
phase. The coordinator steers; children build, document, and test; committed
git files are the only shared medium between them.

True state, verified where the coordinator can check:

- **substrate-kit is populated and at v1.4.0** — verified live in this
  clone: `CHANGELOG.md` carries `## [1.4.0] - 2026-07-09` and the v1.4.0
  release tag exists. That work is the kit-lab lane's (a different
  Project); it is cited here as fleet context, not audited (see the
  out-of-scope note in §b).
- **superbot-next holds 86 merged PRs** (verified live via the GitHub
  search API at review time; the coordinator's ledger said "~87" — the
  86th-merged was #87, the superbot-next lane's own ORDER 005 self-review).
  Content per the coordinator's ledger and superbot-next `docs/status/*.md`:
  the full kernel S0–S15; layer-V (465 goldens replayable, 0 flipped,
  honest-red); K10; port bands 1–7; the presentation rework; the game-plugin
  contract (superbot-next ledger decision 56); and a live bot (Galaxy Bot)
  that boots and serves commands in the test guild.
- **The testing ladder is done through the economy band**, and roughly 15
  real bugs have been found and fixed by live testing — bugs the unit suite
  did not catch (PR anchors in §b, testing session).
- Cross-check pointers: `docs/status/*.md` in superbot-next, and
  `control/status.md` in both repos.

## (b) Agent audit — every session in this lane, classified

Classification legend, per the retro protocol: **(a)** instructions/setup,
**(b)** platform, **(c)** the work itself.

### Coordinator session (this lane's brain)
- **Model:** claude-fable-5[1m] (stated in its environment config; fallback
  claude-opus-4-8[1m]).
- Spawned **~20 short-lived workers** (recon, relays, watchdog, video
  analysis). Workers inherit the session model → claude-fable-5, confirmed
  via transcript events showing model claude-fable-5.
- **Friction (all class (b), platform):** no direct coordinator→child
  messaging tool — every steer needs a relay worker; `send_later` timers
  bind to the arming session, so watchdog wakes route through the
  coordinator; a 4096-byte cap on child-session briefs; ~100+ no-op webhook
  wakes (subscribe/auto-merge/merge notices) costing tokens; sessions run
  in isolated containers, so file exchange happens only via repos/memory.

### Builder session — "SuperBot rebuild: steps 7–13" (created 07-08 15:39Z)
- Delivered **the entire rebuild**: the superbot-next PR #1–#50 era, 49
  rebuild PRs, **~13.6h** wall time (PR #1 opened 16:17Z → PR #50 merged
  05:56Z, by merge stamps). Ran 18 sequential workers plus 1 mid-task
  resume (S12), with shared progress-log handoffs.
- **Incidents:** the band-3 worker was externally killed mid-run —
  recovered via a read-only scout plus a continuation worker, zero loss
  (external stop; class (b)/owner action). PR #35 froze at "Expected" on
  misconfigured required checks — owner fixed the ruleset (class (a),
  setup).
- **Model:** cannot be determined directly from the coordinator's vantage;
  the one child transcript inspected ran claude-fable-5 and a sibling
  session card states "Model: fable-5" — very likely claude-fable-5
  throughout, but directly verified only for those two.

### Retrospective session #1 (created 07-09 10:27Z)
- **DIED at provisioning**: the environment setup script exited 1
  (`pip install -r requirements.txt` with the wrong cwd/no file present).
  Zero work done. Class (a), setup — the failure mode is now documented in
  `docs/environment-setup-script.md`, merged as #47 in this repo.
- **Anomaly:** the dead session **self-revived ~6h later** and began
  re-doing the already-merged task; it was stood down by a coordinator
  message; verified no repo changes. Class (b), platform oddity.

### Retrospective retry session
- Delivered `docs/status/rebuild-orchestration-retrospective-2026-07-09.md`
  (superbot-next #51 + #53, including fixing 4 kit-checker findings on its
  own doc). Clean. Class (c).

### Diff-overview session
- Delivered `docs/status/old-vs-new-diff-overview-2026-07-09.md`
  (superbot-next #52): 58 old cogs mapped, a 276-vs-479 command-surface
  comparison, and the unported list. Clean. Class (c).

### Testing session (created 10:34Z, ongoing)
- Composition root + boot smoke (#54); band-1 live (#56, #58 — two
  live-blocking bugs); app-commands + message feed (#61); moderation +
  logging (5 bugs: #62, #63); triage of the owner's 9 recording defects
  (#65, #66); presentation rework (#67, #70, #71); plugin contract ORDER
  002 (#75–#77); operator-spine band (3 bugs: #79, #80); economy band
  (4 fixes: #85, #83). All PR numbers are superbot-next.
- **Pattern:** every band finds real bugs the unit tests missed — live
  testing is this Project's highest-value activity. Class (c) — the work,
  done well.
- **Stall points were all owner-gated platform clicks**: privileged intents
  (fixed by owner), plugin repo creation (session tokens cannot create
  repos — class (b)), and the kernel-drift corpus ruling (product taste,
  owner-only).

### Setup-script-fix session (created 11:02Z)
- Delivered substrate-kit #47 (the environment-setup-script doc).
- **Anomaly:** a ~5.5h gap between creation and first visible activity —
  cause not determinable from the coordinator's vantage (possibly a
  provision retry or queueing). Flagged as class (b), "cannot determine".

### Wake-up session (created by the owner 16:49Z)
- Opened substrate-kit **PR #51**, duplicating kit-lab's in-flight ORDER
  005 (their PR #50, branch `claude/order005-retro-2026-07-09`, opened
  17:10Z — before #51's open at 17:11Z, and acked as kit-lab's own next
  session in `control/status.md`).
- **Collision class (a):** the same order was broadcast to multiple lanes
  without the lane-suffix rule reaching all executors. **How it resolved,
  live:** the duplicate **PR #51 MERGED at ~17:24Z** — auto-merge fired
  before coordination completed, so the stand-down became an FYI rather
  than a close. This is a live example of the broadcast-order collision
  class: the residual conflict now sits on kit-lab's #50 (verified
  `mergeable_state: dirty` at review time), which kit-lab must reconcile.
  The coordinator messaged the wake-up session to make no further changes
  to the unsuffixed `docs/retro/` files.

### Overnight watchdog (worker under the coordinator)
- 5 hourly cycles, zero stalls detected, stood itself down on completion.
- Quirk: its timers fired into the coordinator session — class (b),
  `send_later` has no session-target parameter.

### Out-of-scope note
substrate-kit's **kit-lab lane is a different Project**: it executed ORDERS
001–004 and cut releases v1.1.0–v1.4.0 today. It is not audited here beyond
the collision above; its own retro is the unsuffixed pair in this directory.

## (c) Retro answers

The full QUESTIONS.md answers (A1–G3), from this lane's perspective, live in
the companion file:
[self-review-2026-07-09-superbot-coordinator.md](self-review-2026-07-09-superbot-coordinator.md).

## (d) Efficiency verdict

**The build took ~13.6h against prior human estimates of weeks** — possible
because the specs were front-loaded and frozen before the builder started.
**Testing has taken ~6h so far** across 5 bands plus the presentation
rework, and every band paid for itself in real bugs.

Biggest sinks:
1. **The required-checks freeze** (~35 min; PR #35 stuck at "Expected";
   owner-fix).
2. **The provisioning death + zombie duplicate** (~30 min plus the risk of
   duplicate work landing).
3. **The ORDER-005 triple-collision risk today** — a third copy was averted
   only because recon caught it; the second copy (PR #51) merged anyway.
4. **Webhook noise** — ~100+ no-op wakes; token cost, no wall-time cost.

Redo ordering, with what the lane knows now:
1. **Fix the environment setup script BEFORE spawning any doc sessions**
   (one dead session and one zombie trace to it).
2. **Build the replay adapter in layer-V, before the port bands** — parity
   could have tracked band progress instead of trailing it.
3. **Run the first live boot right after K10, not after all 7 bands** —
   the two dispatch-blocking bugs (superbot-next #56, #58) would have
   surfaced a day earlier.
4. **State the lane-suffix rule in every broadcast order** — today's
   collision was exactly this omission.

## (e) ⚑ Owner actions (exact steps, and what each unblocks)

1. **Kernel-surface-drift ruling (flag 13):** open superbot-next
   `docs/status/testing-report-2026-07-09.md`, find flag 13; reply in the
   manager inbox or chat with either "relax-compare" (ignore the new
   kernel's extra audit fields) or "re-baseline" (re-record goldens against
   the richer surface). **Unblocks: EVERY parity flip.**
2. **Create the plugin repo:** github.com/new → owner menno420 → name
   `superbot-plugin-hello` → Public → Create repository (no README). Then
   tell any session "move examples/superbot-plugin-hello into it".
   **Unblocks: ORDER 002 done.**
3. **Env setup script:** claude.ai/code → your project → Environment
   settings → Setup script → replace contents with the block from
   substrate-kit `docs/environment-setup-script.md` → Save. **Unblocks: no
   more sessions killed at provisioning.**
4. **superbot-next required checks:** repo Settings → Rules → edit the main
   ruleset → required status checks: add the kit gate (kit-quality) — and
   per kit-lab: swap the legacy alias contexts for kit-quality. **Unblocks:
   the red-merge hole is closed.**
5. **Test-guild hygiene:** remove the old SuperBot from MineSnakeBotTest
   (or change its prefix). **Unblocks: clean single-bot evidence.**
6. **Optional:** invite a throwaway member, send its user ID in chat.
   **Unblocks: full kick/ban effect proof.**
7. **substrate-kit ratifications (kit-lab's list, cited):** merge-or-veto
   PRs #26 and #22 (the two pending program-law ratifications); decide the
   superbot v1.2.0+ upgrade (the pin-only stance is now 4 releases behind).

## (f) Continuation — what happens next with zero owner input

The testing ladder continues: band 4 (XP/karma/community), then games,
knowledge, AI. Parity flips wait ONLY on ruling (e)1. The coordinator keeps
relaying owner rulings as they arrive, re-arms the overnight watchdog for
unattended windows, and steers new sessions per the fleet protocol
(`control/` bus, one writer per file, suffixed lane files in shared repos).
