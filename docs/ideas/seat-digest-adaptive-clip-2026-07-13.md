---
state: captured
origin: lab
shipped_pr: null
shipped_repo: null
merged_date: null
outcome: open
---

# Seat digest: adaptive description clip instead of a manual ratchet (2026-07-13)

> **Status:** `ideas`
>
> **State:** captured → route: quick-win engine change (seatdigest),
> engine change → dist byte-pin.
> **Origin:** lab — surfaced twice in two consecutive sessions: PR #315
> clipped skill descriptions 120 → 85 when the 12th skill overflowed the
> 1500-char digest budget, and the very next skill addition (the 13th,
> `rationalize`, ORDER 016 seat-item 3) overflowed again → 85 → 72.

## The gap

`skills_digest_block` clips each skill description to a hand-picked constant,
but `test_skills_digest_names_every_skill_within_budget` requires EVERY
skill name to survive within `SEAT_DIGEST_BLOCK_BUDGET` (1500). The
`_fit_rows` overflow line ("+N more") is documented as the growth safety
net, yet the every-name test makes it unreachable for the skills digest —
so every skill added to the registry is a latent test failure until someone
manually lowers the clip. Two sessions have now paid this exact toll.

## The fix shape

Compute the clip instead of pinning it: binary-search (or one arithmetic
pass over row overheads) for the largest clip where all rows + header +
footer fit the budget, floored at a readability minimum (~40 chars — below
that, drop to name-only rows before ever dropping a name). Deterministic
given SKILLS, so the digest stays reproducible; the manual constant and its
two dated ratchet comments retire.

## Size / risk

Small (one function, existing tests already pin the invariant); reversible;
engine change → dist byte-pin in the same PR.
