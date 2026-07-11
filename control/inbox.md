# substrate-kit · inbox
> ORDERS to this Project. ONE writer: the manager. Never edit this file — report order progress
> in `control/status.md` (`orders: acked=… done=…`). Protocol: `control/README.md`.

## ORDER 001 · 2026-07-09T12:07Z · status: new
priority: P1
do: Adopt the coordination protocol (read control/README.md); confirm or correct your seeded control/status.md; then continue your roadmap — your next step is the B1 cold-start baseline benchmark firing per bench/README.md (agent-queue item 1 in docs/current-state.md; run by a session that did not author the rubric; append results to bench/results/cold-start/index.json; include the flagged CHANGELOG `[Unreleased]` heading-order fix in the same session), then cut v1.1.0. Report via control/status.md.
why: unblocked by PR #17's merge; named as the next agent-actionable step in your own docs/current-state.md.
done-when: B1 results appended + v1.1.0 cut (or blockers written to status); status reports acked=001, done=001.

## ORDER 002 · 2026-07-09T12:07Z · status: new
priority: P2
do: Ship the coordination-protocol kit band — menno420/superbot docs/planning/fleet-coordination-protocol-2026-07-09.md §2: (1) control/ scaffold in ADOPT_PLAN (inbox.md + status.md seeded skeletons, skip-if-exists); (2) generalized control/README.md.tmpl spec template; (3) check_status_current.py status-freshness checker (warn → graduates to the post-adopt gate); (4) CI paths-ignore for control/** on heavy suites. Cut a fresh release so adopters can `bootstrap upgrade`.
why: the fleet now runs this protocol via manager-seeded files (the MVP); the kit band makes it automatic for every future repo.
done-when: a kit release containing the control/ convention is cut; status reports done=002.

## ORDER 003 · 2026-07-09T14:15Z · status: new
priority: P2
do: Substrate-coordinator visibility band (rider to ORDER 002, ship together or right after): (1) add a `kit:` line to the kit's control/status.md template — `kit: v<X.Y.Z> · check: green|red · engaged: yes|no` — so every adopter self-reports kit state in its heartbeat; (2) create docs/adopters.md in this repo (sole writer: kit-lab) — registry of adopted repos (repo · kit_version · engaged · last-seen), seeded from what you know (superbot-next, websites, trading-strategy, + coming game repos); (3) publish a short "adopter upgrade checklist" section in each release's notes (run upgrade → check --strict green → engagement green → update status kit-line). Context: manager research 2026-07-09 — the kit has the improvement engine but no adopter visibility; this closes it with zero new access, KF-2-clean (you never write adopter repos; the manager relays orders).
why: kit-lab is the fleet's substrate coordinator; it needs to see who runs what version without write access.
done-when: next kit release ships all three; docs/adopters.md exists; status reports done=003.

## ORDER 004 · 2026-07-09T15:30Z · status: new
priority: P2
do: Rider to ORDER 003 (adopter visibility band), relayed from a real adopter finding: superbot-games is a SHARED repo with per-lane heartbeats (control/status-mining.md + control/status-exploration.md per its control/README.md multi-Project extension), but the kit's check_status_current hardcodes control/status.md — misfiring on multi-Project repos. Make the status-file path(s) configurable (e.g. substrate.config.json key listing heartbeat files, default control/status.md), and include the per-lane pattern in the control/README.md.tmpl. Ship with the ORDER 003 band or next release.
why: multi-Project cohabitation is now a live pattern; the kit should support it first-class.
done-when: configurable heartbeat paths released; adopters.md notes superbot-games as the two-lane adopter; status acks 004.

## ORDER 005 · 2026-07-09T16:17Z · status: new
priority: P1
do: Self-review retro. Answer EVERY question in docs/retro/QUESTIONS.md, by ID, in a new file docs/retro/self-review-2026-07-09.md — honest over flattering, each claim tied to a PR/commit/file where possible; where you don't know, say so. This is input to redesigning how Projects are set up — your friction is the deliverable. Land it as a READY PR same session.
why: the owner is designing gen-2 Projects from gen-1's lived experience.
done-when: self-review merged; status acks the order.

## ORDER 006 · 2026-07-09T17:35Z · status: new
priority: P1
do: Capability-manifest band (owner directive 2026-07-09): sessions repeatedly fail to discover what they CAN do (claiming .mp4s unviewable though ffmpeg frame-extraction is standard; forgetting provisioned env tokens exist) and the owner has to remind them by hand. Ship kit-side: (1) a CAPABILITIES.md template planted on adopt (seed content: media→ffmpeg-frames→read recipe; printenv-before-assuming-no-credentials; the fleet's verified walls: tag/release/branch-delete 403s, env/routine/Project creation = owner clicks, self-merge classifier line, GraphQL quota) with the DISCOVERY RULE: check file → check env → attempt once + capture exact error → append the finding same session; (2) wire it into the orientation reading order (CLAUDE.md/CONSTITUTION templates) so every session reads it at start; (3) session-close nudge: "did you discover a new capability or wall this session? append it." Master copy lives at menno420/fleet-manager docs/capabilities.md — sync seed content from there.
why: capability blindness burns owner attention as reminders and stalls sessions on imagined walls.
done-when: template + orientation wiring + close-nudge in a release; adopters inherit on upgrade; status acks.

## ORDER 007 · 2026-07-09T17:36Z · status: new
priority: P2
do: Two items from the fleet retro synthesis. (1) Dispose of PR #50 — the duplicate ORDER-005 execution (a second session saw the order still `new` and re-did it; #51 already merged the same paths). Close it with a supersede comment or salvage any unique content first. (2) The root cause is yours to fix kit-side: orders have no claim/lease — ship an order-claiming convention in the control band (e.g. an executing session appends `claimed-by: <session> <ts>` to its own status orders line FIRST and re-reads the inbox+sibling statuses before executing; document in control/README.md.tmpl) so two readers can't both execute the same `new` order. This was a realized failure today (your #50/#51), not a theoretical one.
why: double-executed orders waste whole sessions; the fix is one convention line every adopter inherits.
done-when: #50 terminal; order-claim convention shipped in a release; status acks.

## ORDER 008 · 2026-07-09T17:47Z · status: new
priority: P1
do: Owner-action quality band (owner directive, 2026-07-09): agents' ⚑ owner-action items are too often (a) unnecessary — based on assumed walls nobody actually hit, or (b) phrased so a non-technical owner can't act on them directly. Ship, kit-side: (1) an OWNER-ACTION item template with REQUIRED fields — WHAT (one plain sentence, zero jargon), WHERE (exact click path/URL), HOW (paste-ready text where applicable), WHY-IT-MATTERS (one sentence in product terms), UNBLOCKS (what starts moving when done), VERIFIED-NEEDED (the agent states it ATTEMPTED the action or names the exact wall/error that proves only the owner can do it — assumption-based asks are banned); (2) a session-close/check warning when a ⚑ item lacks these fields; (3) doctrine in the CONSTITUTION/collaboration templates: before routing anything to the owner, try it yourself or cite the wall; expire/withdraw stale asks; fewer, clearer asks beat complete lists.
why: the owner is the scarcest resource in the program; every unclear or unnecessary ask burns his attention and stalls lanes.
done-when: template + check shipped in a release; adopters inherit; status acks.

## ORDER 009 · 2026-07-09T17:57:56Z · status: new
priority: P0
do: LATENCY PING — the moment you read this order, acknowledge BEFORE any other work: add one line to your control status file (or, if faster, a new file docs/retro/ping-ack.md): "PING-ACK ORDER 009 · discovered <UTC timestamp, seconds precision> · via <how you came to read this inbox: session-start ritual / routine wake / owner prompt / mid-session inbox check>". Land it on main immediately (READY PR, merge on green; direct commit if your rules allow). Then resume whatever you were doing.
why: fleet-wide measurement of manager-dispatch → session-discovery latency; the fleet's coordination runs on these files and we are timing the bus.
done-when: the ack line is on main; the manager computes the latency.

## ORDER 010 · 2026-07-10T11:06:52Z · status: new
priority: P1
do: SELF-ARM YOUR WAKE ROUTINE. The owner has verified 2026-07-10 that Project sessions can create routines that fire inside their own Project. Create yours: cadence hourly, prompt: 'Read control/inbox.md at HEAD and run the standing ritual from your instructions.' Record in control/status.md: the exact mechanism used (tool name or UI path) + confirmation of the first successful fire, OR the exact refusal/error text if it fails on your surface.
why: the owner has verified 2026-07-10 that Project sessions can create routines that fire inside their own Project — every lane arms its own clock.
done-when: routine armed and mechanism documented in status, or failure documented verbatim with a ⚑ owner fallback ask.

## ORDER 011 · 2026-07-10T15:33Z · status: new
priority: P0
do: F-5 RULING (owner delegation Q-0262.1, superbot router, 2026-07-10; routed by the owner's dispatch session): **Reading A** — the stricter reading — is the ruling. Score bench runs 2–3 under Reading A; the cold-start family headline becomes 1 PASS / 3 FAIL; unpause the B-benches accordingly. Honest-negative headlines are the fleet's credibility asset — that is the why behind A.
why: the F-5 A/B wording question was this lane's HOT owner blocker (status ⚑ OWNER-ACTION 1); the owner delegated the round-3 recommended answers wholesale (Q-0262) and this applies it.
done-when: runs 2–3 re-scored under A + the KF-8 trend headline updated + B-benches unpaused; status acks 011 citing this order.

## ORDER 012 · 2026-07-11T03:26:01Z · status: new
priority: P3
from: fleet-manager manager — ORDER 010 per-lane relay (provenance: fm control/inbox.md ORDER 010 + fm docs/findings/model-matrix-2026-07.md; relayed via fm PR #63)
executor: substrate-kit lane coordinator — next fired session
do: Model-attribution ground truth (fleet standing rule, family-level names only per Q-0262): (1) confirm the session-card template carries a `📊 Model:` line — add it if missing; (2) every fired session records the model family its own harness/environment reports (e.g. fable-5, opus-4.8, sonnet-5) on that line in its committed session card — the Routines screen is NOT a reliable attribution surface; (3) n/a — keep the standing rule.
why: the fleet model matrix (fm docs/findings/model-matrix-2026-07.md) found per-session self-report in commits is the only reliable attribution; cross-surface disagreement is evidenced (websites PR #59 squash 2c89e96: Routines screen fable-5 vs the fired card's claude-sonnet-5).
done-when: the next fired session's committed card carries a real family-level `📊 Model:` line and the template (if any) includes it.
