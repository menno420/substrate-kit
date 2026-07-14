---
state: promoted
origin: lab
shipped_pr: 355
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-14
outcome: shipped
---

# `check_idea_index` merged-reality leg — grace-windowed git-truth verification (2026-07-14)

> **Status:** `ideas`
>
> **State:** captured (💡 ender on the PR #349 session card, ranked #2 in
> the Night-12 triage) → **shipped** same file's creation session (kit PR
> #355: the leg + the four-case mutation arc; merged_date is the
> anticipated date per the #349/#351/#352/#354 in-PR flip convention — and
> this very file is the leg's first live grace-window dogfood).

## The idea

`scripts/check_idea_index.py` validates frontmatter **shape** only: an idea
file can claim `outcome: shipped` with a `shipped_pr` that never merged, a
`merged_date` that was only ever the in-PR flip's ANTICIPATED date, or a
`merged_sha` (optional key) that isn't on main — and nothing catches it.
The merged-reality leg verifies shipped claims against **actual local git
history** (no GitHub API — the repo is the ground truth): `shipped_pr` must
have a merge marker on main (`(#N)` squash tail / `Merge pull request #N`),
the real merge date reconciles `merged_date` (drift > 1 day flagged with
the real date), and a well-formed `merged_sha` must be an ancestor of main.

## The design that makes it safe

- **Grace window (7 days from `merged_date`, cohort-date fallback):** the
  in-PR flip convention marks an idea shipped while its PR is still open,
  and kit PRs park for days on owner-gated review — an unreachable claim
  younger than the window is clean, never a finding.
- **Advisory-first:** reachability/date findings print `[advisory]` and
  never affect the exit code; only malformed `merged_sha` syntax (a typo,
  never a timing issue) fails hard.
- **Graceful degradation:** gitless tree / shallow clone (proven live —
  the building session's own container clone was shallow, 51 of 441
  commits) / unresolvable ref → self-skip with a note, zero findings.
  Claims about other repos (`shipped_repo` ≠ the local origin) are
  skipped: unverifiable here by design.

## Why it is worth having

The in-PR flip necessarily writes anticipated ship facts; mechanical
post-merge reconciliation beats trusting them forever (the #344/#346
`state: captured` drift found and fixed by hand in the #349 session is the
same class from the other end). With this leg, a stale or fabricated ship
claim surfaces on the next checker run instead of misdirecting a future
dispatch session.
