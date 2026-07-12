# 2026-07-12 — kit v1.14.0 distribution wave B close-out

> **Status:** `complete`

- **📊 Model:** fable-5 · distribution-wave close-out

## Scope (what is about to happen)

wave B close-out: adopters regen + status record + claim delete.

## What happened

- **Adopters regen** (runbook §6): `python3 dist/bootstrap.py currency` ran
  clean first try (no SSL retry needed), committed AS GENERATED. All four
  wave-B rows read **tree v1.14.0**: gba-homebrew (current, no drift),
  pokemon-mod-lab (current, no drift; private repo handled by currency as
  in prior waves), venture-lab (current · self-report DRIFT v1.12.1 — the
  chronic heartbeat-lag class), fleet-manager (current · self-report DRIFT
  v1.7.0 — same class). Kit's own row: the deliberate tree-internal pin
  DRIFT (§7 ⚑), not chased. Wave-A repos as expected mid-flight:
  superbot-next tree 1.13.0 (its v1.14.0 hop not yet merged); websites /
  superbot-games / trading-strategy trees already 1.14.0 with self-report
  lag DRIFT (wave A's lane owns their rows).
- **control/status.md**: wave-B v1.14.0 distribution record added to phase
  (per-repo: PR · merge SHA · landing path · seed outcome · docs applied),
  lane-owed follow-ups condensed (venture-lab capability-seed
  hand-adopt-once; control/README.md diverged manual-merge on all four;
  Q-0270 collapse notes; pokemon-mod-lab + venture-lab docs/CAPABILITIES.md
  diverged), blockers claim note + next-queue parenthetical + notes line.
  Wave A's rows/claim untouched. `check --strict --status-only` green.
- **control/claims/wave-b-v1140.md deleted** (lane terminal);
  `control/claims/wave-a-v1.14.0.md` left alone (parallel lane, open by
  design).
- Gate: `python3 dist/bootstrap.py check --strict` — only red was this
  card's designed born-red hold. Full 1147-test suite left to CI per
  coordinator instruction.
- Wave A's close-out had NOT landed before this one (origin/main tip
  47bf43c at flip time).

## 💡 Session idea

The wave close-out runbook (§6) could have `currency` emit a one-line
machine-readable summary (repo → tree version → drift class) that the
close-out session pastes verbatim into the status record — the per-repo
tree/DRIFT prose in phase records is currently hand-transcribed from the
currency stdout each wave, a small recurring transcription-error surface.

## ⟲ Previous-session review

The wave-B distribution session (this lane's prior leg) recorded merge
SHAs, landing paths, and seed outcomes per repo in a paste-ready form,
which made this close-out purely mechanical — good practice worth keeping.
Improvement: it left the close-out to a separate session without noting in
the claim file that the close-out was still owed; a `· close-out pending`
suffix on the claim bullet would make the lane's remaining debt visible to
parallel sessions scanning control/claims/.
