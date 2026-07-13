# 2026-07-14 — Seat digest: adaptive description clip (retire the manual ratchet)

> **Status:** `in-progress`

About to (opening declaration): build
`docs/ideas/seat-digest-adaptive-clip-2026-07-13.md` — compute the
skills-digest description clip in `src/engine/seatdigest.py` from the SKILLS
list + block budget instead of hand-ratcheting a constant (ratcheted
120 → 85 → 72 in two consecutive sessions), floored at a readability minimum
with a name-only fallback; tests + dist byte-pin regen in the same PR.

- **📊 Model:** Fable

Run type: worker session (BUILD phase, coordinator-dispatched).
