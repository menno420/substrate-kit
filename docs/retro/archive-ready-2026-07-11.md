# Archive-ready note — 2026-07-11 (coordinator chat archived)

> **Status:** `archive` — written by the archive-prep close-out
> session (card `.sessions/2026-07-11-archive-prep-close-out.md`); the
> companion retro is
> [`2026-07-11-continuous-run-retro.md`](2026-07-11-continuous-run-retro.md).
> Everything below was verified against the tree / live API at write time —
> nothing important remains chat-only.

## True state (one paragraph)

The Q-0265 continuous run (2026-07-10T20:00Z → 2026-07-11T~19:30Z) ended
with the kit at **v1.12.0**, the §6 EAP queue complete, 6 releases cut
agent-side (v1.7.1→v1.12.0) each distributed 7-repo-wide, **9 engaged
adopter trees current at v1.12.0** (fresh `currency` regen in the close-out
PR; superbot stays deliberate pin-only stale, ⚑ OA-7), bench B1 cold-start
at **1 PASS / 7 FAIL over 8 index rows** (run-9 a near-miss with the first
ON M2+M3 double win; run-10 queued), and health re-verified from scratch at
close: **1057 tests passed**, ruff clean, dist byte-pin clean (704108 B),
`check --strict` exit 0, `check_idea_index`/`check_program_law`/
`check_bench_integrity` OK. Two pin PRs park open by design awaiting owner
ratification (#220, #238 — `do-not-automerge`, CI-green, auto-merge verified
not armed); `control/claims/` is clean; every other PR is merged or closed.
CHANGELOG `[Unreleased]` holds the next release payload (#228 gate fixes +
#232 scanner layered fetch + #236 footprint cut & collect guard) — **the
next session cuts v1.13.0**.

## Routine state at archive (final record, live-verified)

- **ARMED and surviving the archive: the daily lab loop** —
  `trig_01MHwmBrA1bziEp49g6xqGt5` "kit-lab loop", cron `0 6 * * *` (UTC),
  fresh session per fire, environment `env_01R1G1wsWsEMShxECRsFnVor`,
  prompt = `docs/operations/lab-loop.md` fenced block; verified live at
  archive-prep (enabled=true, next fire 2026-07-12T06:01Z). Owner
  kill-switch: pause/delete the Routine in the console.
- **DISARMED: the Q-0265 failsafe cron** `trig_019nbVSWfu9grKjeHks97CeU`
  ("substrate-kit failsafe wake", `0 */2 * * *`, bound to the archived
  coordinator session). NOTE: the archive order recorded it as already
  deleted, but the live probe at archive-prep found it **still armed** —
  the delete was actually performed by the close-out session (verify
  routine claims by probe, retro §3.1).
- One stray Q-0265 `send_later` one-shot (`trig_0159SwShY6z4WXa6nbV2s2Ft`,
  19:34Z) may fire once into the archived coordinator session — harmless,
  self-disables after firing.

## ⚑ Owner-action items open at archive (full blocks: `control/status.md`)

- **OA-14 — ratify pin PR #220** (rubric §3 T5 v2 alignment):
  merge https://github.com/menno420/substrate-kit/pull/220 or close with a
  word. **OA-15 — ratify pin PR #238** (T5 v3 probe re-shape): same, at
  https://github.com/menno420/substrate-kit/pull/238. One click each; both
  together let run-10 judge v3 task text under the §3-v2 rubric coherently.
- **OA-2** — required-check swap (retires the legacy alias jobs + the
  recurring born-red false-alarm class). **OA-3** — daily-loop console
  knobs: armed agent-side, environment defaults in effect; say nothing to
  accept. **OA-4** — Railway project `kit-lab`. **OA-5** — confirm MIT.
  **OA-6** — P11 public flip OR P13 read-only PAT (unblocks B2/B3/B4
  sweeps). **OA-7** — superbot upgrade decision (pin now 14 releases
  behind). **OA-8** — environment setup-script paste. **OA-9** —
  (optional, low) self-merge permission rule. **OA-10** — branch cleanup
  checkbox (~48 stale merged-PR branches; agent deletion is a verified 403
  wall). **OA-11** — "automatically update branches" checkbox (ends the
  behind-stall class). **OA-12** — route the websites ORDER 005 relay.

## What a fresh session needs to resume

1. `git fetch origin main && git reset --hard origin/main` — then read
   `control/inbox.md` + `control/status.md` + THIS note.
2. **Cut v1.13.0** per `docs/operations/release-runbook.md` (payload already
   in CHANGELOG `[Unreleased]`), run the standard 7-repo distribution wave.
3. **Bench run-10** (spec notes:
   `bench/results/cold-start/run-10-spec-notes.md`) — ideally after the
   owner ratifies #220 + #238.
4. The daily lab loop is already armed (06:00Z) and needs nothing; its
   first-fire confirmation is owed by the first session after
   2026-07-12T06:00Z.

**Confirmation:** nothing important remains chat-only — the self-review and
coordinator lessons are in the retro, the routine state and owner-action
list are above and in `control/status.md`, the day's arc is in the retro +
the heartbeat's git history, and the unreleased payload is in CHANGELOG.
