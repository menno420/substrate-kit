# 2026-07-11 — ORDER 013: lane self-review (last ~24h)

> **Status:** `complete`

- **📊 Model:** fable-5 · medium · review/verify

## Scope (what is about to happen)

Execute inbox ORDER 013 (fm PR #193 @ 059b5f3, priority P1, executor
"substrate-kit seat (next wake)" — this wake; claimed FIRST on main per
control/README § Claiming an order, fast-lane PR #196 @ f9717f4,
`claimed-by: 013 kit-order-013 2026-07-11T10:30Z`). Deliverable per the
order's done-when: a dated **"Self-review 2026-07-11"** section committed in
`control/status.md`, covering the last ~24h (2026-07-10 ~20:00Z → now):
(1) what WENT WRONG — each with a PR/run/commit citation; (2) what REQUIRES
OWNER ATTENTION — click-level, plain language, mirrored as ⚑ items on the
heartbeat; (3) one-line current health. Honest-negative findings are the
deliverable — nothing softened; where the record already exists in
status/docs, cite it rather than duplicate it. Close-out: status overwrite
(self-review section + orders line moves 013 into done=, claimed-by dropped;
ALL standing content preserved — ⚑ OWNER-ACTION 2–13, ROUTINE STATE, release
+ wave records, next-queue) as the deliberate last content step before this
card's flip. Files: `control/status.md` + this card ONLY. NEVER
control/inbox.md, bench/, sibling cards, or PR #181.

## Close-out

Shipped the declared scope exactly. The **"Self-review 2026-07-11"** section
is in `control/status.md` (findings W-1…W-10, owner-attention block, health
line — every load-bearing claim cited to a PR/run/commit; window-start
baseline verified from git history: 852 tests at heartbeat fa94f6c 18:37Z →
995 now). Negative findings led: B1 headline stays 1 PASS / 4 FAIL (run-5
FAIL, PR #163); the run-5 fabricated-approval incident (worker correctly
refused); two gate loopholes realized live before being closed same-day
(tail-1 shadowing → #187/v1.10.1; card-only born-red exemption →
superbot-games #40 → #176); drift found and NOT hidden (off-taxonomy model
lines; kit's own ci.yml/release.yml still on checkout@v4/setup-python@v5 —
new queue item from W-10b). Orders line: 013 → done=, claim dropped; inbox
re-read at claim + post-claim — **ends at 013, NO ORDER 014+**; sibling
statuses carry no 013 claim. Mid-slice: a coordinator red-ping on this PR's
born-red head (9a7ce06, run 29149561718) was job-log-verified per PL-006 as
the designed session-gate hold (job 86536750395: "HOLD (by design)…
nothing to investigate") mirrored by the two legacy alias jobs
(86536781916/86536781917, body = `if [ "failure" != "success" ]; then exit
1`) — the exact false-alarm class the review's W-9 documents, firing during
the review itself; no defect, cure = this flip. Verify: `python3 -m pytest
tests/ -q` → **995 passed**; `python3 src/build_bootstrap.py` → 666924 B,
`git diff dist/bootstrap.py` empty (byte-pin clean); `python3
dist/bootstrap.py check --strict` red ONLY by this card's own pre-flip hold.
Diff = control/status.md + this card, nothing else.

## 💡 Session idea

**Teach the red-ping triage to cite the alias topology:** the coordinator
red-ping class (W-9 — born-red hold + legacy-alias mirrors read as "three
real failures") has now cost a diagnosis round in at least five sessions
(#140/#144/#147/#153/#197). Until OWNER-ACTION 2 retires the aliases, ship a
one-line kit `check` advisory (or a note in the generated gate's HOLD
banner): "N other failing contexts on this head are required-context
aliases that mirror kit-quality — check kit-quality's log only." Cheap,
advisory-only, and it converts the recurring human/coordinator
misdiagnosis into a self-explaining CI surface — enforce-don't-exhort
applied to the false-alarm class itself.

## ⟲ Previous-session review

The P4/wave-fixes slice (#194/#195) was exemplary on the lane's hardest
discipline: it ATTEMPTED the assumed-owner-only trigger arm per THE
DISCOVERY RULE and succeeded, converting OWNER-ACTION 3 from an ask into a
record — and it recorded the three console-only knobs honestly instead of
faking coverage. One genuine improvement it surfaced: it bumped the
Node-20-deprecated action majors in the GENERATED gate but not in the kit's
OWN ci.yml/release.yml (verified in-tree this session, W-10b) — a
half-applied fix pattern worth a checklist line in the release runbook:
"when bumping generated-workflow pins, grep .github/workflows/ for the same
pins." Queued as a next-slice item rather than fixed here (out of this
order's declared scope; diff stays heartbeat + card only).
