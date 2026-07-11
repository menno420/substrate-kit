# 2026-07-11 — adopter outcomes measurement (before/after report)

> **Status:** `complete`

- **📊 Model:** fable-5 · high · measurement/report

## Scope (what is about to happen)

Measure adopter outcomes before/after kit adoption — owner-steering load,
false-claim rate, and time-to-ship across the adopter fleet; honest nulls
expected and reported as nulls. Findings land in
`docs/reports/2026-07-11-adopter-outcomes-measurement.md`; close-out records
in `control/status.md` + this card. Claim:
`control/claims/measure-adopter-outcomes.md` (fast-lane PR #245, on main at
69c6a0c).

## What was done

Four read-only measurement passes (kit recon; 10-adopter classification +
7-row drift verification + 16-claim sweep across superbot-games /
venture-lab / fleet-manager; superbot before/after over a ~332-day
pre-period; websites + superbot-next deep dive incl. two incident
reconstructions and one force-push null check) synthesized into
`docs/reports/2026-07-11-adopter-outcomes-measurement.md`. Headline: the
before/after question is unanswerable today — 9/10 adopters were born 13
minutes–20 hours before their kit-install PR, and superbot (the only real
pre-period) is pin-only, with the kit extracted *from* its native machinery.
False-claim audit near-clean: ~130 superbot merged-claims + 16 mid-tier
claims verified with 0 contradictions; the one confirmed false-"shipped"
(superbot-next #44) was caused by the pre-v1.0.0 kit's own too-weak gate and
self-corrected in ~6 minutes (#46). Registry drift (7 rows) confirmed as
structural stale heartbeat self-reporting (Q-0261.3), not deception.
Post-adoption time-to-ship baselines recorded for future measurement
(websites 2.4 min median / n=151; superbot-next 1.9 min / n=211).

## 💡 Session idea

Adopter-outcomes measurement needs a **pre-registered baseline**: extend the
currency checker (or a sibling `scripts/` pass run with each registry regen)
to snapshot per-adopter PR-latency median/p90 and claim-audit counts into a
dated, append-only baseline file. This session had to reconstruct baselines
forensically after the fact and still couldn't answer the causal question;
the next adoption wave — and especially the first adopter with genuine
pre-kit history — should find its "before" already on disk. Today's report
§2 baselines are the natural first entries.

## ⟲ Previous-session review

The archive-prep close-out (#241/#242) left exactly the durable trail this
measurement session needed — the continuous-run retro and archive one-pager
made the coordinator-era state citable without chat archaeology. The genuine
wrinkle it surfaces: #242 exists only because the squash order of #240/#241
dropped the claim-file deletion, i.e. the two-PR close-out pattern silently
splits when the work PR and claim-clear race. This session's own close-out
uses the same fast-lane pattern deliberately (claim clear + status in ONE
commit, after the work PR is terminal) — worth encoding that ordering as the
stated convention in `control/claims/README.md` rather than leaving it to
each session's judgment.
