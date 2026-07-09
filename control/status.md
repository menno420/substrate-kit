# substrate-kit · status
updated: 2026-07-09T12:29:00Z
phase: founding bands + KL-7 done; B1 PASS recorded (#28); v1.1.0 cut in flight (PR #29 open + release.yml dispatch to follow); control protocol adopted this session (PR #27 landed + this first heartbeat, PR #30)
health: green
last-shipped: #28 — B1 first cold-start row recorded (run 2026-07-09-run01, VERDICT PASS, judge claude-opus-4-8; raw run dir committed)
blockers: none session-side (v1.1.0 completion rides the parallel release session's PR #29 + post-merge dispatch)
orders: acked=001,002 done=
⚑ needs-owner: ratify PL-011 (PR #26, open + CI-green, merge = ratification); ratify/veto PL-010 (PR #22 — merged mechanically, reaction replaces the gate); P4 arm the kit-lab loop schedule; P10 required-check swap to kit-quality; P5 create Railway `kit-lab` → unblocks P6 console move; P11 public flip or P13 read-only PAT; P8 confirm MIT license; delete 8 merged claude/* branches (branch DELETE is proxy-blocked session-side — or flip "Automatically delete head branches")
notes: ORDER 001 — B1 firing DONE (#28) and the CHANGELOG `[Unreleased]` heading-order fix already landed; v1.1.0 cut IN FLIGHT (not yet live at status-writing time: tag list shows v1.0.0 only, PR #29 open) — 001 flips to done when the release is live. ORDER 002 — acked; execution queued as the next band session (substantial: ADOPT_PLAN control/ scaffold + README tmpl + check_status_current.py + CI paths-ignore + fresh release), deliberately not built in this session. #27 landing: the manager PR sat behind main with no CI runs; this session merged origin/main into it, pushed forward-only to the manager branch (⚑ flagged), verified CI green, squash-merged (11744d8).
