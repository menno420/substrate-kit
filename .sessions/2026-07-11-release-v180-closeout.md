# 2026-07-11 — release v1.8.0 close-out (currency regen + status heartbeat)

> **Status:** `complete`

- **📊 Model:** claude-fable-5 · medium · release-close — v1.8.0 published;
  this PR carries the adopters-registry regen + the status close-out

## Scope (what is about to happen)

Close-out of the release-v1.8.0 slice (claim #158 @ c7c430f, bump #159 @
63c6b39, release run 29133041799). Files: `docs/adopters.md` (regenerated
via `python3 dist/bootstrap.py currency` at kit v1.8.0 — adopter rows flip
stale vs 1.8.0), `control/status.md` (heartbeat overwrite preserving
orders 001–011, ⚑ OWNER-ACTION 2–12, ROUTINE STATE incl. the Q-0265
cutover record, wave records, the §6-COMPLETE note; adds the v1.8.0
release record; next-slice = the v1.8.0 distribution wave),
`control/claims/release-v1.8.0.md` (deleted — claim cleared at close), and
this card. NEVER `control/inbox.md` or anything under `bench/`.

## Close-out

Shipped the declared scope exactly. `docs/adopters.md` regenerated at kit
v1.8.0 (Generated: 2026-07-11T00:41:38Z) — all 7 engaged/adoptable rows
now read `stale (v1.7.1 < v1.8.0)`: superbot-next, websites,
superbot-games, trading-strategy, gba-homebrew, venture-lab,
fleet-manager (superbot stays pin-only stale v1.0.0; pokemon-mod-lab not
adopted). `control/status.md` overwritten with the v1.8.0 release record;
preservation of orders 001–011, ⚑ OWNER-ACTION 2–12, ROUTINE STATE
(Q-0265 cutover), wave records and the §6-COMPLETE note was
machine-checked (a required-blocks scan ran before commit: NONE missing).
Claim `control/claims/release-v1.8.0.md` deleted. Release facts recorded:
run 29133041799 success · tag v1.8.0 (annotated 13d40f5) → 63c6b39 ·
asset sha256 28c5dcb64b713dde8d64a513a9a1aa860b4a07bf17d832686f0009932dc89b9b
three-way verified.

## 💡 Session idea

`build_bootstrap.py` prints "wrote … (622084 bytes)" while the file it
wrote is 625066 bytes — the print measures something other than the final
artifact. Harmless today (the byte-pin compares real bytes), but a
human/agent eyeballing the log against `wc -c` or the release-asset size
gets a false mismatch signal — exactly the kind of noise that costs a
PL-006 verification pass. Idea: make the build print
`len(final_bytes)` of the artifact it actually wrote (one line), and have
a test pin print == stat size.

## ⟲ Previous-session review

The bump session (#159, same lane, minutes earlier) executed the recipe
cleanly and its card's MINOR-class justification pre-answered the v1.7.1
card's class-mismatch flag — good closure of an open thread. Improvement
it surfaced for the system: the born-red hold again triggered a
coordinator red-alert round-trip mid-build (third occurrence across
#153/#156/#159); the gate should self-describe its designed hold in the
check output (the #159 card's idea) — promoting that from idea to build
is worth prioritizing before the distribution wave multiplies observers.
