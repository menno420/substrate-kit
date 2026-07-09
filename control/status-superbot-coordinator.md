# SuperBot-rebuild coordinator lane · status

> Lane heartbeat per the v1.4.0 multi-lane pattern (`control/README.md` §
> per-lane heartbeats): this file's sole writer is the SuperBot-rebuild
> COORDINATOR lane. It is deliberately **not yet in `heartbeat_files` by
> design — kit-lab owns the config; decide-and-flag** (kit-lab may add
> `control/status-superbot-coordinator.md` to `substrate.config.json` →
> `heartbeat_files` when it splits its own heartbeat; until then the
> checker's default single-file gate is unchanged).

updated: 2026-07-09T17:45:00Z
phase: wake-up review SHIPPED (suffixed project review + self-review, docs/retro/*-superbot-coordinator.md) — next: superbot-next testing ladder band 4 (XP/karma/community), then games/knowledge/AI; parity flips wait only on the kernel-drift ruling
health: green
kit: v1.4.0 · check: green · engaged: yes (adopter-side; this lane builds superbot-next, engaged on the kit)
last-shipped: this PR — coordinator-lane wake-up review 2026-07-09 (project review with full agent audit + QUESTIONS.md A1–G3 answers, suffixed per lane rule) + this lane heartbeat
blockers: none agent-side. Owner-gated: kernel-drift ruling (flag 13, blocks every parity flip); plugin repo creation (blocks ORDER 002 done)
orders: acked=none-for-this-lane done=none-for-this-lane (ORDER 005 is kit-lab's; this lane filed its review SUFFIXED — the duplicate unsuffixed execution PR #51 merged before stand-down completed and is recorded in the audit; residual conflict on kit-lab's #50)
⚑ needs-owner: 1) kernel-surface-drift ruling (flag 13 in superbot-next docs/status/testing-report-2026-07-09.md: "relax-compare" or "re-baseline" — unblocks EVERY parity flip); 2) create repo superbot-plugin-hello (github.com/new, owner menno420, Public, no README — unblocks ORDER 002); 3) replace the Claude Code environment setup script with the block from docs/environment-setup-script.md (unblocks: no more sessions killed at provisioning); 4) superbot-next Settings → Rules: add kit-quality as a required check + swap legacy alias contexts (closes the red-merge hole); 5) test-guild hygiene: remove old SuperBot from MineSnakeBotTest or change its prefix (clean single-bot evidence); 6) optional: invite a throwaway member + send its user ID (full kick/ban proof); 7) kit-lab's carried ratifications: merge-or-veto substrate-kit #26 and #22; decide the superbot v1.2.0+ upgrade (pin-only now 4 releases behind)
notes: full detail in docs/retro/project-review-2026-07-09-superbot-coordinator.md (§e mirrors the ⚑ list click-by-click; §f is the zero-owner-input continuation: testing ladder continues, watchdog re-armed for unattended windows, coordinator relays rulings). This lane never writes control/status.md or substrate.config.json — one writer per file.
