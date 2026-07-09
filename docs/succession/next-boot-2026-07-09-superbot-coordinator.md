# Next boot — first 10 minutes for the gen-2 SuperBot coordinator (2026-07-09)

> **Status:** `owner-guidance` — succession handoff from the gen-1
> SuperBot-rebuild COORDINATOR lane (wind-down 2026-07-09T19:55Z), written
> for the FIRST 10 MINUTES of the fresh gen-2 coordinator. Filename suffixed
> `-superbot-coordinator` per the multi-lane rule; this lane never writes
> unsuffixed control/docs files. Companions:
> [custom-instructions-proposal](custom-instructions-proposal-superbot-coordinator.md) ·
> [environment-spec](environment-spec-superbot-coordinator.md) ·
> [gen2-feedback](gen2-feedback-superbot-coordinator.md) ·
> [wind-down review](../retro/wind-down-review-2026-07-09-superbot-coordinator.md).

## 1. Read order (10 minutes, in this exact sequence)

1. **This file** — it is the map; everything below is one hop from here.
2. **superbot-next `control/README.md` + `control/inbox.md` +
   `control/status.md`** — the fleet protocol you operate under: inbox
   first, status last, one writer per file, order claiming before
   execution.
3. **superbot-next `docs/status/testing-report-2026-07-09.md`** — the live
   testing-ladder state, band by band, including flag 13 (the
   kernel-surface-drift ruling every parity flip waits on).
4. **substrate-kit
   [`docs/retro/project-review-2026-07-09-superbot-coordinator.md`](../retro/project-review-2026-07-09-superbot-coordinator.md)**
   — who did what, which models ran, and every stall class of gen-1,
   already classified (a) instructions / (b) platform / (c) work.
5. **superbot-next `docs/status/rebuild-completion-report-2026-07-09.md`**
   — the consolidated owner-flag list; do not re-derive it.
6. **substrate-kit
   [`docs/environment-setup-script.md`](../environment-setup-script.md)** —
   why gen-1 sessions died at provisioning, and the exit-0-safe script that
   fixes it (re-verified exit 0 at wind-down, both no-repo and with-repo
   cases).

## 2. Queue state at handoff (commit this as truth — do not re-audit)

- **Bands 0–4 are live-tested**: composition root/boot smoke, band 1
  (dispatch), app-commands + message feed, moderation + logging, operator
  spine, economy, XP/karma/community — **20+ real bugs found and fixed by
  live testing** that the unit suite never caught.
- **Band 5 is PAUSED mid-flight at the owner's stop**: superbot-next
  **PR #95 is open and READY** with only the born-red report job red (red
  by design until evidence lands). Band-5 findings — the **silent
  compensators** and the **temp-role repr leak** — are **partially
  landed**; the rest rides PR #95.
- **Bands 6 (games) and 7 (knowledge/AI) are NOT started.**
- **Every parity flip is gated on the owner's kernel-surface-drift ruling
  (flag 13)** — "relax-compare" vs "re-baseline". Nothing flips before
  that ruling; do not burn time trying.
- **Presentation follow-ups queued**: settings edit hub (D-0025), setup
  wizard (D-0027), hub-topology ratification, nav-edit-in-place polish.

## 3. Walking-skeleton check (BEFORE any real work)

In **BOTH** repos (superbot-next and substrate-kit): make a trivial docs
branch → open a PR → verify the required checks actually run and report →
arm auto-merge (squash) → watch it merge on green. If any step fails,
stop and fix the merge path first — gen-1's PR #35 froze at "Expected"
for ~35 minutes because a required-check name matched no real job, and
the born-right blueprint made this its flagship seed rule.

## 4. KNOWN WALLS — exact error text (probing a documented wall twice is a bug)

- **Environment setup script death** (fixed script in read-order item 6;
  if you see this, the owner has not pasted it yet):

  ```
  Setup script failed with exit code 1 ... fatal: not a git repository (or any of the parent directories): .git ... ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'
  ```

- **GitHub MCP rate limit** (back off, batch reads, fall back to the local
  clone):

  ```
  rate limit already exceeded for user ID 225413533
  ```

- **Agents cannot delete remote branches** (403) **nor create repos** —
  both are owner clicks. Direct REST fallback also walls:

  ```
  GitHub access is not enabled... An org admin must connect the Claude GitHub App
  ```

- **Child-session brief cap** — briefs over 4096 bytes are rejected:

  ```
  instructions must be at most 4096 bytes (got 4132)
  ```

  Compress; put detail in a committed doc and point the brief at it.

- **Agent tool from a worker context**:

  ```
  Agent type 'general-purpose' not found. Available agents: worker
  ```

- **`send_later` binds to the arming session** — there is no
  session-target parameter; timers route through whoever armed them.
  Arm watchdog timers from the session that should receive the wake.
- **Required-check names must match real job names** — or PRs freeze at
  "Expected" forever (the #35 incident). Verify against the walking
  skeleton before relying on auto-merge.
- **The coordinator has no direct child-messaging tool** — steer children
  via a relay worker calling `claude-code-remote` `send_message`. It works
  and never lost a message; it just costs a worker per steer.
- **Webhook subscribe / auto-merge / merge notices generate ~100+ no-op
  coordinator wakes** — NEVER act on them; triage rule: subscribe/merge
  notices are not actionable, ever.

## 5. Standing facts (owner-confirmed, do not re-litigate)

- **`DISCORD_BOT_TOKEN_PRODUCTION` is a SEPARATE TEST-BOT token.** The
  name is misleading; owner confirmed 2026-07-09. Gen-2 should rename it
  `DISCORD_BOT_TOKEN_TEST` (see the environment spec).
- **The test guild is MineSnakeBotTest.**
- **The old SuperBot still answers `!` in that guild** — the owner asked
  to remove it; until that click lands, expect double-answer noise in
  prefix-command evidence.
