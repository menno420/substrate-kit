# SuperBot-rebuild coordinator lane · status

> Lane heartbeat per the v1.4.0 multi-lane pattern (`control/README.md` §
> per-lane heartbeats): this file's sole writer is the SuperBot-rebuild
> COORDINATOR lane. It remains deliberately **not in `heartbeat_files` —
> kit-lab owns the config; decide-and-flag** (unchanged from the wake-up
> review).

status: wind-down complete — ready for archive + fresh session
updated: 2026-07-09T19:58:00Z
phase: gen-1 lane CLOSED. Succession pack shipped in docs/succession/ (next-boot guide, custom-instructions proposal, environment spec with re-verified setup script, gen-2 blueprint feedback) + wind-down retro addendum docs/retro/wind-down-review-2026-07-09-superbot-coordinator.md. The gen-2 coordinator boots from docs/succession/next-boot-2026-07-09-superbot-coordinator.md
health: green (nothing in flight agent-side; band 5 paused at the owner's stop with superbot-next PR #95 open/READY, only the born-red report job red; bands 6–7 not started; parity flips gated on the kernel-drift ruling)
kit: v1.6.0 · check: green (strict + session log) · engaged: yes (adopter-side)
last-shipped: this PR — coordinator-lane wind-down succession pack (gen-1 → gen-2), suffixed per lane rule
blockers: none agent-side — the lane is closed; everything remaining is an owner click (see ⚑)
orders: the owner's wind-down guidance is EXECUTED (succession deliverables 1–5 shipped, heartbeat flipped as the deliberate last commit); no orders remain for this lane — successor lane claims its own
⚑ needs-owner: 1) kernel-surface-drift ruling (flag 13 in superbot-next docs/status/testing-report-2026-07-09.md: "relax-compare" or "re-baseline" — unblocks EVERY parity flip); 2) create repo superbot-plugin-hello (github.com/new, owner menno420, Public, no README — unblocks ORDER 002 done); 3) paste the setup script from docs/environment-setup-script.md into the project Environment settings (re-verified exit-0 at wind-down — unblocks: no more sessions killed at provisioning); 4) superbot-next Settings → Rules: required-check swap — add kit-quality and drop the legacy alias contexts (closes the red-merge hole / the #35 "Expected"-freeze class); 5) remove the old SuperBot from MineSnakeBotTest or change its prefix (clean single-bot evidence); 6) optional: invite a throwaway/sacrificial member + send its user ID (full kick/ban effect proof); 7) kit-lab loose ends: PR #50 disposition + done=005 reconciliation (kit-lab's ORDER 007 convention carries it); 8) stale-branch cleanup in both repos (agents get 403 on remote branch delete — owner or a repo setting must sweep the merged claude/* branches)
notes: whole-life record in docs/retro/wind-down-review-2026-07-09-superbot-coordinator.md (whole-life summary, exact-error friction ledger, first-person close), linking the merged review pair rather than repeating it. This lane never writes control/status.md, control/inbox.md, or substrate.config.json — one writer per file. Archive this heartbeat with the lane; the gen-2 lane opens its own suffixed file.
