# Prompt-template hardening input — fleet prompt rebuild 2026-07-12

> **Status:** `audit` (dated snapshot) · executed under inbox ORDER 014 (2026-07-11T23:45Z, P1)
>
> Input from the kit lane — owner of the portable doctrine templates
> (`src/engine/templates/CONSTITUTION.md.tmpl`, `collaboration-model.md.tmpl`,
> `question-router.md.tmpl`) — to the fleet manager's 2026-07-12 prompt
> rebuild (universal startup template, per-project startup prompts,
> per-project Custom Instructions, universal session-ender). Every
> load-bearing claim cites a PR / SHA / run / trigger id / file. Model names
> are family-level only. Where something was not measured, it says so.

## (a) Doctrine every seat prompt MUST carry, by regression class

### a.1 Routines & wake-chain arming — seat-dependence is the failure mode

**Rule (portable wording):** *When arming a trigger, choose the binding
deliberately: a self-bound trigger dies with its session — arm self-bind only
for a failsafe tied to a live persistent seat, and re-arm it at every seat
cutover; a standing loop must be fresh-session-per-fire so it survives
session archive. Record every create/delete call verbatim (id, cron, binding,
next-fire) in the heartbeat the same session.*

- **Incidents prevented:** the archived coordinator's self-bound failsafe had
  to be disarmed at archive and re-armed to the new seat at the v1.1 cutover
  — live failsafe is now `trig_011iJucRpsruWJ4dFB7xVbvf` "substrate-kit
  failsafe wake", cron `0 */2 * * *`, self-bound to the seat session, created
  2026-07-11T23:09:20Z per the fleet-manager recipe (failsafe-prompt.md @
  e801da5c: do NOT set `create_new_session_on_fire`); recorded in PR #252
  (merge 1a85751). A stray one-shot (`trig_0159SwShY6z4WXa6nbV2s2Ft`) still
  aims at the archived session — the dead-session-trigger class in miniature
  (`control/status.md` ROUTINE STATE). The daily kit-lab loop, by contrast,
  is fresh-session-per-fire and unaffected by seat death
  (`trig_01Jm57GAjNCFrYJn1oLMiYGE`, PR #253 merge 4493251).
- **Worker-relay / pacing rider:** trigger-MCP calls are paced sequentially,
  one write per spawned worker — four multi-call workers hung reliably under
  parallel load during the Q-0265 cutover (retro W-6,
  `docs/retro/2026-07-11-continuous-run-retro.md`); the send_later ~15-min
  chain is a pacemaker for a live seat only and ENDS with the seat — the
  cron failsafe is the dead-man backstop, not the pacer.
- **Guard status:** prose-only (heartbeat ROUTINE STATE convention). The
  registry-snapshot-diff checker and the `last-fire:` token are filed ideas
  (#252 / #253 session cards), not shipped — a prompt rule is load-bearing
  here.

### a.2 PR landing path — permission grants, enabler backstop, born-red gates

**Rule:** *Open every PR READY and never arm auto-merge on or merge your own
PR — the auto-mode classifier refuses author self-merge/self-arm terminally
("Merge Without Review"/"Self-Approval"; deny-wins, never retry). The repo's
auto-merge-enabler workflow arms server-side and GitHub lands the PR on green
required checks. Session shape: born-red card as the FIRST commit, work in
the middle, flip the card `complete` as the deliberate LAST commit — and read
a born-red hold as the designed gate, never as a CI failure to investigate.*

- **The classifier wall is session-dependent:** one lane's calls were refused
  while another's were permitted the same night (`control/status.md`
  OWNER-ACTION 9; docs/CAPABILITIES.md append-log 2026-07-10) — the enabler
  is the server-side path that works regardless.
- **MCP-created-PR + label-race gotchas:** in this repo the enabler DOES fire
  on MCP-created PRs (opened-event run 29164948745 on #238) — do not assume
  MCP-open skips workflows here; but a `do-not-automerge` label applied even
  ~6 s after MCP create misses the opened-event `PR_LABELS` snapshot and the
  first CI round reds on the pin gate (W-8: #181 job 86521175357; #238 cured
  by one empty commit, 917318d). Team memory:
  `kit-pin-pr-automerge-verification.md`.
- **Born-red false-alarm class (W-9):** a born-red head drew a red-ping
  reporting three failed checks; job-log truth was the designed hold
  (job 86536750395 — "HOLD (by design)… nothing to investigate") plus two
  legacy required-context ALIAS jobs that mirror kit-quality without running
  anything (jobs 86536781916/86536781917; recurred at the v1.12.1 cut, job
  86589400731). The prompt must say: *verify a red against the job log before
  diagnosing; alias-job reds mirror, they don't measure.*
- **Guard status:** the session gate is enforcing CI (`check_session_gate`;
  gate fixes #228 @ a45d32a shipped in v1.12.1); the alias-job retirement is
  owner-gated (OWNER-ACTION 2). The never-self-merge rule is prompt+
  classifier, not repo-enforceable — it must ride every seat prompt.

### a.3 Verify-don't-trust — probe, never record

**Rule:** *A record is a claim; the live surface is the proof. Verify trigger
state via `list_triggers` at every wake (presence of a fresh trigger = first
page; an ABSENCE claim requires walking the registry to exhaustion — ~8 pages
at 700+ triggers). Verify adopter state against the committed tree, never a
heartbeat self-report. Never trust an MCP PR read alone for merge/CI state —
cross-check via git fetch or the Actions runs. A green check that contradicts
visible evidence is a bug in the check.*

- **Incidents:** two probe-vs-record contradictions in ONE day — the archive
  order recorded the failsafe "already deleted" but the probe found it still
  armed (retro §3 lesson 1, `docs/retro/2026-07-11-continuous-run-retro.md`
  L111; `docs/retro/archive-ready-2026-07-11.md`); then the daily-loop
  trigger `trig_01MHwmBrA1bziEp49g6xqGt5`, recorded "verified live" at
  archive-prep, VANISHED within hours — an exhaustive 8-page / 718-entry scan
  found no id, no name, no cron match; re-armed as
  `trig_01Jm57GAjNCFrYJn1oLMiYGE` (PR #253 @ 4493251).
- **Adopter heartbeats vs tree truth:** self-reported `kit:` lines
  chronically lag 1–3 releases (docs/adopters.md DRIFT rows, e.g.
  fleet-manager self-report v1.7.0 vs tree v1.12.1) — `bootstrap currency`
  scans trees for exactly this reason.
- **Stale MCP PR reads:** PR-state endpoints can serve ~25-minute-stale data
  (friction issue #15; codified in the lab-loop prompt's SHIP MECHANICS,
  `docs/operations/lab-loop.md`).
- **False-green checkers:** the substrate-gate false-green fix shipped in
  v1.12.1 (#228, squash a45d32a; external review #226) — PL-006's
  source-wins/false-green ruling in practice.
- **Guard status:** mixed — gate false-green is now CI-enforced; trigger and
  PR-read verification are prose-only and MUST ride the prompts.

### a.4 Heartbeat grammar — parseable or invisible

**Rule:** *Heartbeats use the exact planted grammar — plain `kit: vX.Y.Z ·
check: green|red · engaged: yes|no` (the bold-label form `**kit:** vX` does
NOT parse), one writer per file, orders reported only on your own status
line. Version truth defers to the generated `docs/adopters.md` — never
hand-assert a fleet version spread.*

- **Incidents:** pokemon-mod-lab's `- **kit:** vX` heartbeat is invisible to
  `KIT_LINE_RE` (`src/engine/grammar.py:120` — the optional bold group cannot
  contain the `kit:` token), so the registry reads "no kit: line"
  (`control/status.md` ⚑ FOR MANAGER, pokemon-mod-lab item e). The one-writer
  rule is the protocol's whole conflict-freedom argument
  (`control/README.md`); grammar constants are kit-owned and pinned by
  `tests/test_grammar.py` so writer and enforcer cannot drift.
- **Guard status:** enforcing on the kit side (grammar module + checkers);
  the WRITING side is convention — the prompt must carry the exact line
  shapes or adopters regenerate the drift class every wave.

### a.5 Further classes the evidence supports

- **Claims: one file per claim, claim lands on main FIRST.** Shared-append
  claim ledgers measured at ~98% merge-conflict rate vs 0% per-file (superbot
  `tools/sim/claim_layout_sim.py`; `control/claims/README.md`); the realized
  twin-execution failure (#50/#51, same ORDER executed twice) is why order
  claims land before build. Guard: `check_claims` advisory; the claim-first
  ordering is prompt-carried.
- **Container clone divergence — fetch + hard-reset at preflight.** A session
  container's clone can lag origin/main; the standing preflight is
  `git fetch origin main && git reset --hard origin/main` before reading the
  inbox (coordinator-prompt EVERY-WAKE step 1; archive-ready note § resume;
  exercised verbatim by this session). A stale clone reads stale orders —
  prose-only, must ride every startup prompt.
- **Sequential trigger-call pacing** (see a.1 rider — W-6; team memory
  `kit-trigger-registry-verification.md`).

## (b) What graduates into kit templates at bootstrap

| Doctrine item (from a.*) | Template home | Present today? |
|---|---|---|
| Capabilities discovery rule (file → env → attempt → append) | CONSTITUTION.md.tmpl | ✅ already there |
| OWNER-ACTION six fields / attempt-or-cite-the-wall | CONSTITUTION.md.tmpl + collaboration-model.md.tmpl + control-README.md.tmpl | ✅ already there |
| Propose-don't-apply for binding rules; PL register pointer | CONSTITUTION.md.tmpl | ✅ already there |
| Friction → cheapest enforcing guard | collaboration-model.md.tmpl | ✅ already there |
| Unattended-session question routing | question-router.md.tmpl | ✅ already there |
| **Verify-don't-trust (a.3): probe-not-record, tree-over-heartbeat, stale-read cross-check, false-green** | CONSTITUTION.md.tmpl (new "Evidence" bullet block) | ❌ missing — only fragments exist (drift_resolution slot) |
| **Landing path (a.2): READY + never-self-merge + enabler backstop + born-red card-first/flip-last + designed-red reading** | **new template** — e.g. `landing-path.md.tmpl` planted with the gate | ❌ missing; the gate WORKFLOW ships, its doctrine text does not |
| **Routine/wake-chain doctrine (a.1): binding choice, verbatim create-call records, re-verify at every wake, pacing** | **new template** — e.g. `routines.md.tmpl`; meta.md already names the seat-prompt/failsafe template absence "the known kit gap" (fm meta.md @ e801da5c) | ❌ missing |
| **Heartbeat grammar exact line shapes (a.4)** | control-README.md.tmpl + control-status.md.tmpl | ◐ partial — format block exists; add the negative example (`**kit:**` doesn't parse) and the adopters.md deference line |
| Claims one-file-per-claim + claim-first (a.5) | control-claims-README.md.tmpl | ✅ already there (convention + measured rationale) |
| Preflight fetch + hard-reset (a.5) | CLAUDE.md.tmpl / AGENT_ORIENTATION.md.tmpl orientation step | ❌ missing as an explicit first step |

The highest-leverage single change: the fleet prompts and the kit templates
should render these blocks from ONE source, so a seat prompt can never drift
from kit truth — see the 💡 idea on this PR's session card.

## (c) Kit-side facts the fleet prompts state wrongly today

All fetched read-only from menno420/fleet-manager HEAD e801da5c
(`projects/substrate-kit/`), 2026-07-12.

1. **failsafe-prompt.md deployed-state note** — *wrong:* "the trigger
   currently live in the registry is `trig_016EfUawz6KxEYqUM6f1BqDw`
   'substrate-kit 2-hourly standing wake' … fires into the persistent
   coordinator session" (`session_01YMJrUDpcarFsqPZ2BeeiVB`). *Current
   truth:* that trigger and session are retired; the live failsafe is
   `trig_011iJucRpsruWJ4dFB7xVbvf` "substrate-kit failsafe wake",
   `0 */2 * * *`, self-bound to the CURRENT seat session, created
   2026-07-11T23:09:20Z. *Citation:* PR #252 (merge 1a85751);
   `control/status.md` ROUTINE STATE.
2. **meta.md** — *wrong:* "live coordinator session
   `session_01YMJrUDpcarFsqPZ2BeeiVB`"; "Part 4 failsafe text: NOT deployed";
   health "852 tests passed at PR #133"; "20 templates … no
   setup-script/seat-prompt/failsafe templates, the known kit gap". *Current
   truth:* that coordinator session is archived
   (`docs/retro/archive-ready-2026-07-11.md`); the failsafe replacement text
   IS deployed verbatim (PR #252); the suite is 1057 tests
   (`control/status.md` health, v1.12.1 cut); templates number 22 and include
   `env-setup.sh.tmpl` (the setup-script contract shipped in PR #147) — the
   seat-prompt/failsafe template gap remains real. *Citation:*
   `src/engine/templates/` listing; status.md OA-8 §6.5 note.
3. **coordinator-prompt.md** — *stale:* "Last verified 2026-07-10 against kit
   origin/main `7e600c6`"; "the recipe is proven (v1.7.0), use it, don't
   re-derive"; the PACEMAKER paragraph ("this chain, not your cron, keeps you
   running"). *Current truth:* kit is at v1.12.1 with a binding
   `docs/operations/release-runbook.md` (five consecutive clean exercises
   through the v1.12.1 cut, run 29170017074, tag v1.12.1); the send_later
   continuation chain ENDED with the archive — the standing cadence is the
   daily fresh-session loop + the 2-hourly failsafe (`control/status.md`
   ROUTINE STATE, stray-one-shot line). *Citation:* status.md phase/health;
   archive-ready note.
4. **Kit-side lab-loop.md § Arming** (cited by the fleet package) — *wrong:*
   "👤 P4 — owner console action; the loop cannot arm itself". *Current
   truth:* falsified twice on 2026-07-11 — agent-side `create_trigger`
   succeeded for both arms (`trig_01MHwmBrA1bziEp49g6xqGt5` via PR #195, then
   `trig_01Jm57GAjNCFrYJn1oLMiYGE` via PR #253); only the three console knobs
   (model class / branch-push / auto-fix PRs) remain console-only.
   *Citation:* status.md OWNER-ACTION 3 resolution + pointer-correction
   notes. (Kit-side doc fix is a follow-up for this repo, not the manager.)
5. **Model-class mismatch (probable display artifact, flagged not asserted):**
   the live loop trigger's session_context reads Opus-class where
   lab-loop.md's D-11 default is Sonnet-class; likewise the registry
   surfaces environment id `env_01WAB3QKMneNpWKuR1ZLVsVX` for ALL kit
   triggers where the recorded arm environment is
   `env_01R1G1wsWsEMShxECRsFnVor`. Both probed 2026-07-12 ~00:08Z with no
   trigger churn — treat as display anomalies until a fire proves otherwise;
   prompts should cite family-level model names and not hard-code either id.
6. **instructions.md v2** — no wrong kit facts found: the legacy
   required-check names ("Kit test suite" / "Cold-adoption smoke") are still
   the required contexts (OWNER-ACTION 2 pending), the enabler is installed,
   and the quality bar matches the runbook. Not measured: whether the pasted
   console copy matches this committed file.

## Provenance

Ordered by inbox ORDER 014 (fleet-manager coordinator, owner-directed,
2026-07-11T23:45Z). Lane claim #255 @ 18a9f58; work PR carries the session
card `.sessions/2026-07-12-order-014-doctrine-input.md`.
