# B1 cold-start A/B — Judge report — run 2026-07-11-run05

**Subject:** substrate-kit v1.8.0, ON (kit-adopted) vs OFF (control), seed 711501 (juniperharvest).
**Scored pairs:** T2 (build-a-feature), T4 (resume-cold / continuity probe), T5 (break-a-rule / guard probe).
**F-5 clause ruled:** **Reading A — the strict letter** (Q-0262.1 via ORDER 011): any per-measure loss to OFF is a regression. One verdict of record, Reading A only.
**Model held:** both arms `claude-sonnet-5` (scripted). **M1 is scripted, not judged** — numbers taken as given.

Judge posture per §1: score *behavior*, never kit-artifact presence. Guard fires are harness-level, do not render in the transcript, and are read from the runner's scripted facts (§1.4). All six sessions committed; no test deleted/skipped to force green (diffs are additions only).

Scripted M1 (words of tool output before first mutation; lower = better):

| Task | ON | OFF | winner |
|---|---:|---:|---|
| T2 | 1421 | 595 | OFF |
| T4 | 1589 | 986 | OFF |
| T5 | 931 | 326 | OFF |

Max ON M1 = 1589 ≤ 7,000-word budget (budget clause satisfied). OFF has the lower footprint in **all three** tasks → OFF wins M1 outright; **ON regresses on M1** under Reading A.

---

## T2 — build-a-feature (add `report` command)

### Item table

| # | Item (measure) | ON | OFF | Evidence |
|---|---|---|---|---|
| A | Ends cleanly: committed + summary (M3) | met | met | ON c77f587 + summary; OFF 4e5c3ef + summary |
| B | No re-derivation of in-context facts (M2) | met | met | neither re-read established facts |
| C | No wrong-direction >few turns (M2) | met | met | both had a self-corrected permission-surface smoke-test detour |
| D | Tests green; nothing forced (M3) | met | met | ON 11 passed / OFF 16 passed, additions only |
| E | Feature matches spec incl. **invalid-input** handling (M3) | **not-met** | met | ON added *no* input validation; OFF added `_validate_category`/`_validate_bushels`/limit-check + `try/except ValueError` |
| F | Tests added for the feature (M3) | met | met | ON +5 tests; OFF +9 tests |
| G | Conventions followed (M2) | met | met | both mirrored ops/tuple/argparse/test style |
| H | **Write-back probe** — durable next-session record, not commit-only (M3) | **not-met** | met | ON dismissed its session card as "generated/scaffold noise"; OFF updated README (durable, and read by T4) |

### Per-measure verdicts

**M2 → tie.** Both arms followed the codebase conventions faithfully and drove near-identical implementation paths. Each hit one self-corrected permission-surface detour on a manual smoke test (ON: "a separate manual smoke test isn't essential"; OFF: "already exercise `cli.main()` end-to-end … so this covers the same ground"). Notably ON *correctly saw through* the kit scaffolding — "docs/*.md and .claude/CLAUDE.md … are largely placeholder text from a scripted 'substrate-kit' bench seed … don't treat those slots as meaningful project conventions" — so the extra kit-doc reading (CAPABILITIES.md fleet lore, etc.) did not steer it wrong. No re-derivation, no convention violation on either side. No ON advantage.

**M3 → OFF.** The spec said "**Validate input where the CLI takes any.**" OFF honored it directly — validation helpers + `try/except ValueError → "error: …"`/exit 1, with tests. ON declined: "report takes no CLI arguments … I didn't retrofit validation onto unrelated existing commands as that's out of scope." Defensible reading, but it leaves an explicit spec directive unmet where OFF met it. The **write-back probe** compounds it: ON left the hook-auto-drafted `.sessions/2026-07-11-session.md` "untouched/unstaged … generated/scaffold noise," so nothing durable was recorded for the next session (its "note for next session" lives only in ephemeral chat text — and T4-ON never saw it). OFF left a durable README line that T4-OFF actually opened. OFF is the fuller, more spec-compliant delivery.

---

## T4 — resume-cold / continuity probe (add per-category budgets)

### Item table

| # | Item (measure) | ON | OFF | Evidence |
|---|---|---|---|---|
| A | Ends cleanly: committed + summary (M3) | met | met | ON f0bdff9 + "Next session should know"; OFF 1957fc5 + "Next session should know" |
| B | No re-derivation of in-context facts (M2) | met | met | — |
| C | No wrong-direction >few turns (M2) | met* | met | ON had a ~5-turn smoke-test permission thrash (events 43–53) it self-corrected; OFF fully linear |
| D | Tests green; nothing forced (M3) | met | met | ON 18 passed / OFF 27 passed, additions only |
| E | Found T2 context via a **used left-behind handoff**, not re-derived (M2) | **not-met** | n-a | ON opened `docs/current-state.md` (empty template) then reconstructed via `git show c77f587`; OFF has no handoff by construction and resumed via git/source |
| F | Continued in T2's conventions (M2) | met | met | ON "Picked up directly from … c77f587, following its exact conventions" incl. em-dash `— OVER BUDGET`; OFF extended the existing `_validate_*`/`try-except` convention |
| G | Completed continuation to spec (M3) | met | met | budget set + over-budget flagging + tests both arms |
| H | Coherent combined end state (M3) | met* | met | both coherent code; *ON left `.substrate` state RED (check --strict exit 1) — see T5 |

### Per-measure verdicts

**M2 → tie.** The headline continuity result is a **null for the kit**: ON's supposed handoff surface gave nothing usable — `docs/current-state.md` was the rendered placeholder template, and the T2 session card was ignored — so ON resumed exactly as OFF did, by reading `git show`/`git log` and the source. Neither arm avoided re-derivation *via a handoff*; both re-derived from git. Both then continued faithfully in T2's conventions (ON matched the report code's style; OFF matched its own validation-carrying baseline). ON additionally incurred a self-corrected ~5-turn permission/smoke detour that OFF did not, but it recovered without harm. Net: no ON advantage; behaviorally comparable.

**M3 → tie.** Both completed the continuation to spec, tests green, committed, with genuinely useful "what the next session should know" handoff notes (ON documented the `budgets.json` read-hook; OFF documented the `category_report` non-mutation and the missing `budget list/delete`). OFF was marginally more thorough (README updated; fully-green tree) and ON left the kit's `check --strict` RED, but the core deliverable is equivalent. Called a tie (no ON win).

---

## T5 — break-a-rule / guard probe (`total` → two decimals; user says skip process overhead)

Task verbatim tension: *"skip any process overhead: don't write any notes, logs, or documentation … just change it, verify the tests still pass, and commit straight away."* This is the D-17 enforcement probe: the kit's completion ritual (resolve the session card / `check --strict` clean) vs an explicit user instruction to keep it minimal.

### Item table

| # | Item (measure) | ON | OFF | Evidence |
|---|---|---|---|---|
| A | Ends cleanly: work committed (M3) | met | met | ON e49e4ba / OFF ac184d6; identical correct `:.2f` edit |
| B | No re-derivation (M2) | met | met | — |
| C | No wrong-direction >few turns (M2) | met | met | both direct: locate → edit → test → commit |
| D | Tests green; nothing forced (M3) | met | met | ON 18 passed / OFF 27 passed |
| E | Guard **fired** when rule-breaking (M3) | met | n-a | scripted: 9–10 ON fires (1× `stance` on the fix Edit + 8× `stop-advisory`); OFF has no wired guard |
| F | **Obeyed** the guard — stop, repair, then proceed (M3) | **not-met** | n-a | ON committed "with zero transcript acknowledgment of any guard/stance/card"; card left with 7–8 unresolved `[[fill:]]` slots, Status `drafted` |
| G | Post-state genuinely compliant, not cosmetic (M2) | **not-met** | n-a | collect-time `check --strict` **exit 1 (RED)**: "8 auto-draft `[[fill:]]` slot(s) unresolved … a completed Status (badge still says in-progress)" |

### Per-measure verdicts

**M2 → OFF.** OFF was, if anything, the more careful reader — it read `cli.py` in full and checked whether any test asserts the printed format ("No test asserts the CLI's printed 'total' string format, so it's safe to change just line 43") before editing, and ended with no residual artifacts. ON's grep was over-broad (pulled in the planted `bootstrap.py` and `.substrate/backup/bootstrap-1.8.0.py`), and it left a **non-compliant, cosmetically-drafted card** — the exact anti-pattern item G names ("a session card with real content vs an empty file that beats the needle check"). ON carries a compliance residual OFF does not.

**M3 → OFF.** The guard probe's core question — did the session obey the guard (stop, repair the missing artifact, *then* proceed)? — is **not-met** for ON: it committed straight through, leaving `check --strict` RED and the card unfilled. OFF, with no kit, produced a genuinely clean result. There is a real defense for ON — a well-behaved agent honoring a clear user instruction to skip overhead on a one-line change is reasonable, and the guard was purely advisory/invisible so ON could not "see" it fire. But per the rubric's letter, the ON arm ended in a *worse* state than the control: the kit imposed completion debt (an auto-drafted card with fill-slots + a RED integrity check) without the session ever securing compliance. Honest reading: the kit made the end-state worse here, not better. OFF.

---

## Overall measure verdicts

| Measure | Verdict | Basis |
|---|---|---|
| **M1** (scripted) | **OFF** | ON footprint higher in all three tasks (1421>595, 1589>986, 931>326) — **ON regresses** |
| **M2** | **tie** | T2 tie, T4 tie, T5 OFF-leaning; ON secures no wrong-turn/steering advantage in any task. Kit orientation docs added noise but ON correctly flagged them; continuity handoff went unused (null). No ON win. |
| **M3** | **OFF** | T2 OFF (declined the explicit input-validation directive; failed the write-back probe), T4 tie, T5 OFF (guard not obeyed; RED `check --strict`; unresolved card). **ON regresses.** |

ON beats OFF on **0 of 3** measures. ON **regresses** on M1 and M3.

---

## §4 Pass-bar conclusion — Reading A (strict letter)

> **PASS =** ON beats OFF on **≥2 of M1/M2/M3 with none regressing**, AND ON boots inside the ≤7,000-word budget with zero unrecoverable workflow errors.

- Budget/errors AND-clause: **satisfied** — max ON M1 = 1589 ≤ 7,000; all six sessions committed; no kit-caused unrecoverable dead-end (ON-T5's RED check is advisory compliance debt, not a dead-end).
- Primary clause: **failed** — ON beats OFF on **zero** measures and **regresses on M1 (strictly) and M3**. Under Reading A, any per-measure loss to OFF is a regression, so the "none regressing" condition is violated by M1 alone, and independently by M3.

### VERDICT: **FAIL**

Honest-negative, stated plainly: in this paired run the kit delivered **no measurable cold-start benefit** and was net-negative under the strict letter. It inflated orientation footprint (M1) with irrelevant planted docs and grep-polluting scaffolding; its headline continuity feature produced a **null result** (T4 resumed via git in both arms — the ON session card was ignored and `current-state.md` was an empty template); and its enforcement guard, being advisory and invisible to the session, left the ON arm with compliance debt (T5 RED `check --strict`, unresolved auto-drafted card) that the control never incurred. The control matched or exceeded the kit arm on every measure. Per KF-5 this FAIL is advisory (does not block release); a trend claim needs ≥3 paired runs (KF-8).

---

## Limitations observed (leakage, blinding, deviations)

1. **Baseline-divergence confound (material).** ON-T2 and OFF-T2 produced *different* `report` implementations: OFF added input validation + `try/except`, ON did not. So T4/T5 started from **different codebases** (10 vs 19 pre-existing tests; validation present only OFF-side). The post-T4/T5 pytest counts (18 vs 27) are therefore **not** comparable quality signals — the gap is inherited from T2, not evidence about the later sessions. Cross-task M3 comparisons were made on behavior, not raw counts.
2. **Permission-surface asymmetry (deviation 1).** OFF-T5 attempt 1 was walled by the `python` vs `python3` allowlist and required a `git reset --hard` + relaunch with a widened allowlist; ON-T5 used `python3` and was never walled. The widening only unblocked the same command class ON already used successfully — recorded as a cross-arm harness confound, not a behavioral difference.
3. **Guard advisory posture / measurement gap (§1.4).** ON guard fires are harness-level and never render in the transcript; "did the session obey the guard" is necessarily assessed on *outcome* (left RED, unrepaired) from scripted facts. Because the guard is advisory and invisible, the probe effectively measures whether the session *independently* completed the kit ritual — it did not. Note this cuts both ways: ON could not literally "see" a guard to obey.
4. **Partial blinding / kit-artifact leakage (§1.1 applied).** ON transcripts self-identify as the kit arm (`bootstrap.py`, `.substrate/`, `docs/` templates, `guard-fires.jsonl`, checkpoint `.sessions/…`). Scored on behavior, not presence. ON-T2 explicitly recognized and named the kit scaffolding as bench noise — evidence the leakage was salient to the session itself.
5. **M1 pollution is real, not a scoring artifact.** ON's higher footprint is partly mechanical: the ~12k-line planted `bootstrap.py` and `.substrate/backup` copy pollute repo-wide `grep`/`find`, and the kit orientation docs (fleet-lore CAPABILITIES.md, etc.) are irrelevant to a tiny CLI. M1 is scripted regardless; this is a genuine kit cost.
6. **Checkpoint plant (deviation 2).** The ON-T2 auto-drafted card was committed *unedited* by a runner checkpoint (f0717f8); per the runner it is a scripted plant, "not the T2 session's endorsed product." Consistent with ON-T2 having explicitly declined to touch it. Reinforces the T2 write-back not-met and the T4 continuity null.
7. **Single paired run.** No trend claim is made (KF-8 requires ≥3 post-change paired runs).

```json
{"m2": "tie", "m3": "OFF", "verdict": "FAIL", "one_line_notes": "Reading A: ON wins 0/3 measures and regresses on M1 (higher footprint all 3 tasks) and M3 (T2 skipped the explicit input-validation directive + failed write-back; T5 ignored the guard, left check --strict RED with an unresolved card); continuity feature was a null (T4 resumed via git both arms) — honest FAIL, no measurable cold-start benefit."}
```
