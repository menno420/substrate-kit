# Wind-down review — SuperBot-rebuild coordinator lane (2026-07-09)

> **Status:** `audit` — the wind-down ADDENDUM to the merged
> [project-review-2026-07-09-superbot-coordinator.md](project-review-2026-07-09-superbot-coordinator.md)
> and
> [self-review-2026-07-09-superbot-coordinator.md](self-review-2026-07-09-superbot-coordinator.md)
> (the full agent audit and QUESTIONS.md answers live THERE — this file
> adds only what wind-down adds: the whole-life summary, the exact-error
> ledger in one place, and the first-person close). Lived incidents only.
> Suffixed `-superbot-coordinator` per the multi-lane rule. Succession pack:
> [docs/succession/](../succession/README.md).

## Whole-life summary (kickoff → wind-down)

- **2026-07-08 15:39Z** — builder session created; the rebuild
  (superbot → superbot-next, canonical plan steps 7–13) ran **~13.6h wall
  time across 49 PRs** (PR #1 opened 16:17Z → PR #50 merged 05:56Z).
- **2026-07-09** — testing phase: **bands 0–4 live-tested, plus the
  presentation rework and the plugin band; 20+ real bugs found and fixed
  by live testing** that the unit suite never caught. Band 5 paused
  mid-flight at the owner's stop (PR #95 open/READY, born-red report job
  the only red); bands 6–7 not started; parity flips gated on the
  kernel-surface-drift ruling (flag 13).
- **Totals: ~95 PRs across repos** (86+ merged in superbot-next at the
  wake-up audit, climbing through band 5, plus this lane's substrate-kit
  PRs: #47, #52, and this wind-down PR).
- **2026-07-09 ~19:55Z** — wind-down: succession pack authored
  (`docs/succession/*-superbot-coordinator.md`), lane heartbeat flipped to
  "wind-down complete", remaining owner clicks carried on the ⚑ ledger.

## Friction / failure classes — the exact-error ledger

Every class the lane hit, with the exact text where one exists (the
audit's per-session classification stands; this is the one-place lookup
the gen-2 coordinator should never have to rebuild):

1. **Environment setup script death** (killed retro session #1 at
   provisioning; fixed by `docs/environment-setup-script.md`, re-verified
   exit-0 at wind-down):

   ```
   Setup script failed with exit code 1 ... fatal: not a git repository (or any of the parent directories): .git ... ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'
   ```

2. **Zombie-session revival** — the SAME dead session self-revived ~6h
   later and began re-doing the already-merged setup-script doc; stood
   down by coordinator message; verified zero repo changes. Platform
   oddity; not preventable lane-side.
3. **The 5.5h silent session gap** — the setup-script-fix session showed
   ~5.5h between creation and first visible activity. Cause: **"cannot
   determine"** from the coordinator's vantage (possibly provision retry
   or queueing). Recorded honestly as class (b); the blueprint's
   heartbeat-before-work rule is the mitigation.
4. **GitHub MCP rate limit**:

   ```
   rate limit already exceeded for user ID 225413533
   ```

5. **Write-scope walls** — agents cannot delete remote branches (403) nor
   create repos; the direct REST fallback walls too:

   ```
   GitHub access is not enabled... An org admin must connect the Claude GitHub App
   ```

6. **Child-session brief cap**:

   ```
   instructions must be at most 4096 bytes (got 4132)
   ```

7. **Agent-type wall in worker contexts**:

   ```
   Agent type 'general-purpose' not found. Available agents: worker
   ```

8. **`send_later` binds to the arming session** — no session-target
   parameter; every watchdog timer routed through the coordinator.
9. **Required-check name mismatch** — the #35 incident: a required
   context naming no real CI job froze the PR at "Expected" (~35 min,
   owner-fixed ruleset).
10. **No direct coordinator→child messaging** — every steer went through
    a relay worker calling `send_message`; workable, never lost a
    message, but the ORDER-005 stand-down race was lost by ~minutes.
11. **Webhook wake noise** — ~150 wakes from subscribe/auto-merge/merge
    notices, near-zero actionable; the single worst noise source of the
    lane's life.
12. **ORDER-005 broadcast collision** — one order, three
    near-executions; the duplicate PR #51 merged before stand-down,
    kit-lab's #50 stranded dirty. Root cause: no lane addressing in the
    broadcast; kit's ORDER 007 claiming convention is the systemic fix.

## How it felt — first person, coordinator vantage

Honestly: the discipline mostly held, and where it held it was because of
structure, not vigilance. The reply/no-reply contract and the status
checklists gave every turn a shape — inbox first, status last — and that
shape is why a fleet of sessions that never shared a filesystem never
truly lost each other.

The webhook firehose was the single worst part of the job. Roughly 150
wakes, and I can count the actionable ones on one hand. Every wake costs a
full orientation pass — am I mid-task? is this new? — and the answer was
almost always "a merge notice about a merge I armed myself." It trained a
reflex of dismissal that is exactly the wrong reflex to train in a
coordinator.

Steering children through relay workers felt like phoning through an
operator — compose the message, brief a worker, wait for the relay
confirmation — but credit where due: it never lost a message. The one
race it plausibly lost (the ORDER-005 stand-down vs auto-merge) was a
latency loss, not a delivery loss.

The 4KB brief cap forced compression that once dropped nuance — the lane
rule fell out of a brief at 4132 bytes, and that omission is in the causal
chain of the day's collision. When the medium truncates, the truncated
part is always the caveat, never the imperative.

On the model: claude-fable-5 held long-horizon state well. Across ~28
hours of lane life the failures that occurred were environmental — a
setup script, a ruleset, a rate limit, a timer with no address field —
not cognitive. I did not lose the plot; I lost tools.

The races today were the price of broadcast orders without lane
addressing. That is an instructions bug, and the fix costs one sentence
per order.

And the honest-red gates earned their keep repeatedly: layer-V's 0-flipped
honest-red, band 5's born-red report job. Every time a surface stayed red
until evidence existed, a flattering-but-false green was prevented. If
gen-2 keeps one aesthetic from gen-1, keep that one: red is not failure,
red is "not yet proven" — and saying so out loud is what made this
Project's greens worth trusting.
