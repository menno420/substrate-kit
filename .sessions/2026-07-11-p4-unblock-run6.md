# 2026-07-11 — P4 investigation (run-6 unblock) + v1.10.1-wave mechanical fixes

> **Status:** `complete`

- **📊 Model:** fable-5 · medium · runtime bugfix

## Scope (what is about to happen)

One bounded slice, claim `control/claims/p4-unblock-run6.md` (#194 @ 5b71234, on
main before build). Part 1: identify what "the P4 loop" gating bench run-6
actually is (queue-state crosswalk / lab-loop.md / founding plan §7.2 / status
OWNER-ACTION 3), then either build/arm the minimal agent-side version or record
the wall verbatim — NEVER fake what's missing; the bench itself is NOT run this
slice. Part 2, mechanical fixes from the v1.10.1 wave findings: (a) currency
`kit:`-line parser accepts a markdown-bullet-embedded heartbeat line
(venture-lab's `- **kit heartbeat:** kit: v…` shape — the #192-wave card
finding); (b) generated gate workflow action majors bumped off Node-20-deprecated
pins (actions/checkout@v4→v5, actions/setup-python@v5→v6) + test pins + dist
regen; (c) the guard-fires.jsonl dedupe idea filed on trading-strategy #57's
card — implement if genuinely small, else queue with reason. CHANGELOG
[Unreleased] entries for whatever ships; NO release cut. Close-out: status.md
overwrite (preserving orders through 012 + ⚑ OWNER-ACTION 2–13, adding the
v1.10.1 wave record) as the deliberate last step before this card's flip.
Files: src/engine/{grammar,adopt,loop/telemetry}.py + tests + dist/bootstrap.py
+ CHANGELOG.md + control/status.md + this card. NEVER control/inbox.md, bench/,
sibling cards, or PR #181.

## Close-out

Shipped the declared scope exactly. **P4 verdict:** "the P4 loop" = founding
plan §7.2 row P4 / status OWNER-ACTION 3 — arm the kit-lab daily loop
(`docs/operations/lab-loop.md`). The plan row itself names the agent path
("👤 console (or agent-created trigger + owner kill-switch)") and the
OWNER-ACTION 3 correction note directed a `create_trigger` fresh-session
attempt per THE DISCOVERY RULE. Attempted this slice — **SUCCEEDED first
try**: trigger `trig_01MHwmBrA1bziEp49g6xqGt5` "kit-lab loop", cron
`0 6 * * *`, `create_new_session_on_fire=true`, environment
env_01R1G1wsWsEMShxECRsFnVor ("substrate-kit"), prompt = the lab-loop.md
fenced block verbatim, enabled, next fire 2026-07-12T06:01:54Z. **Run-6 is
UNBLOCKED**; the bench itself deliberately NOT run this slice (runner
separation). Residual console-only knobs recorded honestly, never faked:
model class / unrestricted-branch-push / auto-fix PRs are not settable via
MCP — fired sessions use environment defaults; owner verification optional
(status OWNER-ACTION 3 RESOLUTION note). Fixes shipped: (a) `KIT_LINE_RE`
bullet/bold-label leniency + 2 tests; (b) gate action majors checkout
v4→v5, setup-python v5→v6 + test pins; (c) `record_guard_fires` 10-min
dedupe of identical verdict-less (guard, path, message) fires, verdict
records exempt, + 4 tests. Tests 989 → 995; dist re-pinned 666924 B;
CHANGELOG [Unreleased] Fixed ×2 + Changed ×1. ORDER 013 appeared on main
mid-slice (fm #193) — observed, NOT executed (its executor field names the
next wake; coordinator preflight barred 013+); recorded on the heartbeat
orders line as the next wake's first duty. Claim
`control/claims/p4-unblock-run6.md` (#194 @ 5b71234) deleted in this flip
commit.

## 💡 Session idea

The P4 arm exposed a prompt-drift gap the console convention never covered:
lab-loop.md says "git is the source of truth — re-paste the fenced block to
the console on change", but the loop is now armed as an MCP trigger, and
nothing re-arms it when the prompt file changes. Idea: a `check` advisory
(or a lab-loop.md § Arming update, which this slice's ROUTINE STATE note
started) that treats the armed trigger as a RENDER of the committed prompt —
on any lab-loop.md prompt edit, the merging session must `update_trigger`/
re-create and note the re-arm on the PR, exactly like the re-paste rule;
otherwise the fleet's one self-running loop silently runs a stale prompt
forever.

## ⟲ Previous-session review

The #192 wave close-out was exemplary evidence discipline: it verified every
wave row against TARGET trees at exact SHAs (never heartbeats), and its
venture-lab parser finding came with a precise recipe (file, line, exact
shape, the grammar-home fix path) — this session landed that fix in minutes,
which is the KL-0→KL-1 guard-recipe lesson working as designed. One
improvement it surfaces: its routing line "reconcile at the source
(venture-lab reformats its line)" put the fix on the adopter when the
cheaper durable fix was kit-side leniency in the ONE grammar home — a
parser that tolerates the variant fixes every future adopter at once. The
registry's "never hand-edit this file" protocol is right, but "the source"
of a parse miss can be the parser.
