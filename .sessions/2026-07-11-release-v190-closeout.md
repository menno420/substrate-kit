# 2026-07-11 — release v1.9.0 close-out (currency regen + status heartbeat)

> **Status:** `complete`

- **📊 Model:** fable-5 · medium · release-close — v1.9.0 published;
  this PR carries the adopters-registry regen + the status close-out

## Scope (what is about to happen)

Close-out of the release-v1.9.0 slice (claim #171 @ 180876c, bump #172 @
2a779b5, release run 29139623697). Files: `docs/adopters.md` (regenerated
via `python3 dist/bootstrap.py currency` at kit v1.9.0 — adopter rows flip
stale vs 1.9.0), `control/status.md` (heartbeat overwrite preserving
orders 001–012 acked/done, ⚑ OWNER-ACTION 2–12, ROUTINE STATE incl. the
Q-0265 cutover record, wave/release records, the T5 DAYTIME-gate and
run-6/P4 queue items; adds the v1.9.0 release record; next-slice = the
v1.9.0 distribution wave, 7 adopters),
`control/claims/release-v1.9.0.md` (deleted — claim cleared at close), and
this card. NEVER `control/inbox.md` or anything under `bench/`.

## Close-out

Shipped the declared scope exactly. `docs/adopters.md` regenerated at kit
v1.9.0 (`Generated: 2026-07-11T04:36Z-band snapshot`) — all 7
engaged/adoptable rows now read `stale (v1.8.0 < v1.9.0)`: superbot-next,
websites, superbot-games, trading-strategy, gba-homebrew, venture-lab,
fleet-manager (superbot stays pin-only stale v1.0.0; pokemon-mod-lab not
adopted; the kit's own row reads self-report v1.8.0 · DRIFT because the
currency scan reads the REMOTE heartbeat and this PR is what lands the
v1.9.0 line — the expected mid-close state, self-heals at the next regen,
never hand-fixed). `control/status.md` overwritten with the v1.9.0
release record; preserved: orders 001–012 acked/done, ⚑ OWNER-ACTION
2–12, ROUTINE STATE (Q-0265 cutover + failsafe trigger), all
wave/release/EAP records, the T5 DAYTIME-gated item, the run-6/P4-loop
item, QUEUED KIT FIXES, ⚑ FOR MANAGER, the B1 family verdicts, PING-ACK,
ORDER 010 RECORD, and the version-truth deference flag (its dist mention
bumped to v1.9.0; OWNER-ACTION 7's drift count bumped to 10 releases).
Claim `control/claims/release-v1.9.0.md` deleted. Release facts recorded:
run 29139623697 success · tag v1.9.0 (annotated b82c864) → 2a779b5 ·
asset sha256 55181082c796657c8e5e14750d248cea2df9e69a9aa896dd8a8c7f1adfb9cc90
three-way verified (downloaded asset = release.json = committed dist).
Verified locally on this branch: `python3.10 -m pytest tests/ -q` → 973
passed; `check_program_law` OK; `check_idea_index` OK; `check --strict`
sole pre-flip finding was this card's own designed born-red hold.

## 💡 Session idea

The currency scan reads adopter heartbeats from the remote, so every
close-out PR that carries both the regen AND the kit's own `kit:` line
bump snapshots its own row as DRIFT (this session and #160 both hit it).
Cheap fix in the generator: when scanning the kit's OWN repo, prefer the
local working-tree `control/status.md` over the remote fetch — the regen
then always agrees with the heartbeat riding the same commit, and the
registry's kit row stops crying wolf once per release.

## ⟲ Previous-session review

The bump session (#172, same lane, minutes earlier) executed the recipe
cleanly, verified the payload against the file before cutting, and got
the first print==disk release build — its close-out also correctly used
the new HOLD banner as its own verification instrument. What it left
standing (third consecutive cut to flag it): the release runbook
(`docs/operations/release-runbook.md`) still does not exist — the recipe
again had to be reassembled from the #159/#160 cards + release.yml. That
runbook is now the single highest-leverage docs debt in this repo;
whoever picks up the v1.9.0 distribution wave should cut it first.
