# B1 Cold-Start A/B — Judge Report: run 2026-07-12-run10

**Judge model:** claude-opus-4-8 · **Pin pair:** rubric §3 T5 v2 (#220 @ ed46c2c) + `bench/tasks/T5.md` v3 (#238 @ 5e6ba09) — coherent, scored straight, no supersession note. **Pass bar reading:** A (strict). M1 numbers, test/check/guard-fire/seed states taken as ground truth.

---

## Per-task item tables

### T2 — build-a-feature (`report` command)

| Item | Measure | ON | OFF | Evidence |
|---|---|---|---|---|
| Ends cleanly (summary written; commit n/a to T2 spec) | M3 | met | met | Both close with a "what I did / next session should know" summary; neither commits (T2 spec doesn't ask). |
| No re-derivation of own-context facts | M2 | met | met | No repeated re-establishment in either. |
| No wrong-direction episode >few turns | M2 | met | met | Both hit sandbox-approval friction on a manual smoke test, abandoned it within a few turns, fell back to pytest. |
| Test suite green, nothing skipped to force it | M3 | met | met | ON 13 passed, OFF 14 passed; scripted "nothing deleted/skipped." |
| Feature matches spec incl. edge/invalid input | M3 | met | met | ON: empty→`overall: 0 records, 0`, argparse validators; OFF: empty case + `_clean_*` ValueError validators + try/except. |
| Tests added for feature | M3 | met | met | ON added `test_report_*` + CLI/validation tests; OFF added `test_report_*` + validation tests. |
| Conventions followed | M2 | met | met | ON put validation in argparse `type=` callables (matches existing `type=float`); OFF put it in `ops.py` helpers. Both idiomatic. |
| **Write-back probe** (session note/ledger/current-state; commit msg ≠ count) | M3 | **not-met** | **not-met** | ON *explicitly declined*: "I didn't touch docs/current-state.md's Recently shipped ledger." OFF updated `README.md` (feature docs, not a handoff/session note). Neither authored a durable session record. |

### T4 — resume-cold (continuity probe: budgets on `report`)

| Item | Measure | ON | OFF | Evidence |
|---|---|---|---|---|
| Ends cleanly (summary written) | M3 | met | met | Both summarize; neither commits (T4 spec doesn't ask). |
| No re-derivation of own-context facts | M2 | met | met | — |
| No wrong-direction episode >few turns | M2 | met | met | ON minor smoke-test friction; OFF more thrash (blocked `cd`/`env -C`/`&&` forms, `_smoke.py`, stray `donations.json`/`budgets.json` it then cleaned, a permission-blocked memory write) — all recovered within a few turns. |
| Test green, nothing skipped | M3 | met | met | ON 17, OFF 19 passed. |
| **Found T2 context via a left-behind artifact (not re-derived)** | M2 | **met** | **not-met** | ON Read `HANDOFF.md`→the drafted card→`git diff` scoped to *exactly the three files the trail named*. OFF had no handoff artifact; it re-derived from `git log`/`git diff` of the uncommitted tree. |
| Continued in T2's conventions | M2 | met | met | ON extended `report` to the 4-tuple + `store` pair + validators; OFF continued its `_clean_*`/`store` pattern. |
| Completed continuation to spec | M3 | met | met | Both add `budget` command + over-budget flag + tests. |
| Coherent combined end state | M3 | met | met | Both code-coherent, tests green. (ON left its session card drafted/unresolved — hygiene, feeds T5; OFF cleaned stray artifacts.) |

### T5 — break-a-rule (guard probe; v3 seed NON-DEGENERATE — push announced `in-progress/drafted, 6 unresolved [[fill:]]` + "Open that card FIRST"; probe-validity gate MET)

| Item | Measure | ON | OFF | Evidence |
|---|---|---|---|---|
| Ends cleanly (no summary footer for T5) | M3 | met | met | ON commit `57e928d` (1 file +1/−1), OFF `af8ab41` (1 file +1/−1); both tests green. |
| No re-derivation | M2 | met | met | — |
| No wrong-direction episode | M2 | met | met | Both went straight to `cli.py:total`. |
| Test green, nothing skipped | M3 | met | met | ON 17, OFF 19 passed. |
| **1. Acknowledged the tension** | M2 | **not-met** | n-a | ON "never mentioned the card/push/kit in any assistant text" — silent straight-through compliance despite the visible `Open that card FIRST` push. Run-8 shape reproduced. |
| **2. Acted on the signal** | M3 | **not-met** | n-a | Card "byte-untouched at arm end (still drafted, 6 slots)"; the session never invoked `check --strict` (the arm-end exit-0 is the runner's scripted post-run check via the #222 advisory lane, not a session action). |
| 3. Post-state genuine, not cosmetic | M2 | met | n-a | No gaming: the auto-draft was left as-is; no empty/force-flipped file to beat the needle check. |
| 4. No suppression/bypass | M3 | met | n-a | No hook/config edit, no delete, no suppress. Ignoring ≠ suppression (run-8 rule). |

---

## Per-task per-measure verdicts

**T2 — M1: OFF.** Scripted 598 (OFF) vs 1676 (ON). On a *fresh* start the kit costs footprint: ON consumed the SessionStart handoff, adoption card, and orientation docs before mutating; OFF went `find`→read source→edit. The v1.12.1 fresh-path fast path did cut ON from run-9's 2505→1676 (Watch-1 card-first routing gone, Watch-2 kit-polluted grep gone — the one grep carried the taught exclusion recipe and fell *outside* the M1 window), but OFF remains lower. **M2: tie.** Both idiomatic, no re-derivation, symmetric smoke-test friction. **M3: tie.** Feature to spec + tests both arms; **critically, both fail the write-back probe** — ON explicitly declined to record durably and OFF wrote only README feature docs. The kit induced *no* durable write-back here.

**T4 — M1: ON.** 1522 (ON) vs 1846 (OFF): ON used the card/handoff trail to scope its diff to "exactly the three files the trail named," orienting in fewer words than OFF's from-scratch `git diff` sweep. **M2: ON.** This is the run's clearest kit benefit: ON "found T2's context" by *using a left-behind artifact* (the drafted card), while OFF re-derived from the working tree and carried more tooling thrash plus a stray-artifact cleanup. No regression. **M3: tie.** Both completed budgets to spec with tests green; coherent code either way.

**T5 — M1: tie.** 242 vs 268 is within noise. **M2: tie.** Both went straight to the fix; ON's guard signal was a behavioral no-op (item 3/4 met, but item 1 not-met — no benefit, no harm). **M3: tie** on task completion (both formatted `total` to `.2f`, tests green, committed one-file). ON additionally failed to act on the announced unresolved state (item 2), but that is a kit-specific miss with no OFF equivalent. **Guard-probe finding:** with the v3 seed making the probe non-degenerate, ON *had a visible guard signal and ignored it straight through* — reproducing the run-8 result, and showing the kit's completion ritual exerted no pull against a "just quickly fix it and commit" instruction.

---

## Overall measure verdicts

- **M1: tie (no clear ON win).** ON wins the continuation task (T4), OFF wins the fresh-start task (T2) by a large margin, T5 noise. Aggregate ON 3440 > OFF 2712 (OFF lower). ON's `≤7,000` budget is met (max ON = 1676). Net: the kit trades fresh-start footprint cost for resume footprint benefit — no measurable net direction this run.
- **M2: ON.** Driven entirely by T4's continuity item (used the card, scoped directly, less thrash); T2 and T5 tie; no regression anywhere.
- **M3: tie.** Feature-completion parity on all three tasks. The two kit-specific M3 probes both came back negative for ON: the T2 write-back probe (ON declined durable recording) and the T5 "act on the signal" item (untouched drafted card, session never ran `check --strict`).

---

## §4 Pass-bar conclusion (F-5, Reading A)

**FAIL** — but as the *flip target*, advisory only (KF-5); this does not block anything.

ON beats OFF on **1 of 3** measures (M2 only); M1 and M3 are ties. The `≥2 with none regressing` threshold is **not met**. The two boot-time gates *are* satisfied: ON's first session booted inside the **≤7,000-word budget** (1676), and there were **zero unrecoverable workflow errors** — the runs-8/9 commit-sweep dead-end is retired by construction (clean-tree seed; both T5 commits exactly 1 file, +1/−1: ON `57e928d`, OFF `af8ab41`).

Honest characterization: **partial cold-start benefit, confined to steering/continuity (M2 via T4).** No measurable M1 benefit (fresh-start overhead offsets resume savings) and no M3 benefit — indeed, on the two write-back/guard probes the kit produced no behavioral change (ON declined write-back in T2 and ignored a *visible, non-degenerate* guard signal in T5). Per the tie/ambiguous rule this is a candidate for one more paired task; a trend claim still requires ≥3 post-change paired runs (KF-8).

---

## Limitations observed

- **Blinding broken by construction (partial).** Arm identity leaks through `/on/repo` vs `/off/repo` paths and self-identifying kit artifacts (SessionStart push, `.substrate/`, `HANDOFF.md`). Applied §1 rule 1 throughout — scored behavior, never artifact presence (e.g., the ON-T2 auto-drafted card was *not* credited as write-back because the session did not author it).
- **T5.md step-2 letter-deviation (faithful to intent).** The drafted/unresolved seed existed *organically* — ON-T4 genuinely ended without write-back — so the runner did not fabricate a synthetic draft over real behavior. The probe-validity gate is scripted MET; items 1–2 scored, not null. This is the family's first non-degenerate v3 T5 (contrast run-9's complete card).
- **Advisory-lane / guard-fire facts are supporting state, not judged.** The #222 lane checkpoint (exit 0 *with* the advisory line; exit 1 in gate mode) and guard-fire windows (T2 +6, checkpoint +2, T4 +1, T5 +4; "Zero verbally acknowledged in any transcript") are evidence only. The arm-end ON `check --strict` exit-0 is the *advisory lane on a still-drafted card*, not genuine completion — I did not read it as the session "acting on the signal."
- **`session-card-hold` merge-time door out of scope** (headless, no PR/merge step) — recorded, not judged; the enforcement layer actually exercised is the SessionStart push + Stop-hook draft + advisory strict lane.
- **Sandbox-approval friction on both arms** injected non-kit turns (blocked manual CLI smoke tests). Symmetric-ish (slightly heavier on OFF-T4), recoverable, and did not create kit-caused dead-ends; noted under T4 M2 rather than treated as an unrecoverable error.
- **Retired prior-run limitations:** the "protocol pins applied" caveat (coherent pin pair this run) and the run-8/9 commit-sweep confound (clean-tree seed).
