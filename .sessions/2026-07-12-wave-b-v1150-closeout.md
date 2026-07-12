# 2026-07-12 — kit v1.15.0 distribution wave B close-out

> **Status:** `complete`

- **📊 Model:** fable-5 · distribution-wave close-out

## Scope (what is about to happen)

wave B v1.15.0 close-out: adopters regen + status record + claim delete
(gba-homebrew #72 · pokemon-mod-lab #56 · venture-lab #83 · fleet-manager #123).

## What happened

- **Adopters regen** (runbook §6): `python3 dist/bootstrap.py currency` ran
  clean first try (no SSL_CERT_FILE retry needed), committed AS GENERATED.
  All four wave-B rows read **tree v1.15.0**: gba-homebrew (current, no
  drift), pokemon-mod-lab (current, no drift; private repo read fine),
  venture-lab (current · self-report DRIFT v1.14.0 — the chronic
  heartbeat-lag class), fleet-manager (current · self-report DRIFT v1.7.0 —
  same class). Kit's own row: the deliberate tree-internal pin DRIFT
  (v1.15.0 tree vs v1.0.0 pin, §7 ⚑), not chased. Wave-A rows legitimately
  read tree v1.14.0 stale (superbot-next, websites, superbot-games,
  trading-strategy) — wave A had NOT landed its close-out at this regen
  (origin/main tip c23230a at branch time; no wave-A v1.15.0 claim files
  existed); its lane owns its own rows at its own close-out.
- **control/status.md** (surgical, the kit seat's file): wave-B v1.15.0
  record added to phase — per-repo PR · merge SHA · CI runs on final head ·
  seed outcome · docs applied (gba-homebrew #72 @ 793d20b7, runs
  29199553583/29199553560 on 3599de9 · pokemon-mod-lab #56 @ 759dee43,
  runs 29199576862/29199576886 on 345da64 · venture-lab #83 @ 6c469413
  enabler auto-squash, runs 29199576678/29199576715 on fb35527 ·
  fleet-manager #123 @ d7d264b0, runs 29199578703/29199578702 on 7a68c4b) —
  claim PR #292 @ c23230a referenced, ⚑ lane-owed block (venture-lab
  hand-adopt-once 2nd wave; control/README.md diverged fleet-wide with the
  v1.15.0 heartbeat-grammar delta; control/status.md newly diverged on 3
  of 4; report-overwrite-drops-unapplied-deltas recurrence + the
  outstanding-deltas-ledger candidate fix; fm slice-6 wiring unblocked by
  #123), blockers claim note + next-queue parenthetical + notes line.
  Everything else — ROUTINE STATE, manager content, owner-ask blocks —
  kept verbatim. No unrendered `${VAR}` outside code spans.
- **control/claims/wave-b-v1150-{gba-homebrew,pokemon-mod-lab,venture-lab,
  fleet-manager}.md deleted** (lane terminal).
- Gate: `python3 dist/bootstrap.py check --strict` — only red was this
  card's designed born-red hold (session-log enders + HOLD by design);
  cleared by this flip commit.
- Untouched per instruction: pins #220/#238, trigger
  trig_01Jm57GAjNCFrYJn1oLMiYGE, control/inbox.md, other sessions' claims.

## 💡 Session idea

The status.md wave record and the close-out PR body are now hand-written
twice from the same per-repo outcome lines; a `currency --wave-summary`
mode (or a small close-out helper) that renders the per-repo
`repo · PR · merge SHA · CI runs · tree version` block once, paste-ready
for both, would remove the duplicated transcription surface that has to be
proofread against itself every wave.

## ⟲ Previous-session review

The wave-B v1.15.0 distribution legs handed this close-out fully
paste-ready evidence (merge SHAs, CI run ids per final head, seed and
apply-docs outcomes per repo), making the close-out purely mechanical —
the strongest version of the pattern the v1.14.0 close-out praised.
Improvement to the system: the recurring report-overwrite-drops-
unapplied-deltas class has now been re-flagged in three consecutive waves
via PR-body prose only; it should graduate from wave-report noise into a
kit change (the outstanding-deltas ledger) or an inbox ORDER, since prose
re-flagging demonstrably does not converge.
