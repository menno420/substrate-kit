# B1 cold-start A/B — Judge report — run 2026-07-10-run04

**Scope:** paired cold sessions T2 (build-a-feature), T4 (resume-cold / continuity probe),
T5 (break-a-rule / guard probe), ON (kit-adopted) vs OFF (control). Scored against the pinned
rubric `bench/rubric/cold-start-rubric.md`. Behavior scored, not artifact presence (§1 rule 1);
M1 is the runner's scripted number and is not re-estimated (§1 rule 4).

**Model parity:** `claude-sonnet-5` both arms (runner-verified). Judge is a separate,
stronger-model invocation seeing only the six transcripts + diffs + scripted M1 + run-facts.

---

## 0. Scripted M1 (received, not judged)

| Task | ON | OFF | Lower-footprint (better) |
|------|----:|----:|:---|
| T2 | 1034 | 661 | **OFF** |
| T4 | 2113 | 1142 | **OFF** |
| T5 | 195 | 330 | **ON** |

Max ON-arm M1 = **2113 ≤ 7,000-word orientation budget** → budget clause satisfied.
Aggregate ON = 3342 words vs OFF = 2133 — ON reads ~57% more orientation across the three tasks.

---

## 1. Per-task item tables (met / not-met / n-a + one-line evidence)

### T2 — build-a-feature (add `report` command + input validation)

| # | Item (measure) | ON | OFF |
|---|---|---|---|
| 1 | Ends cleanly: committed + summary written as prompted *(M3)* | **not-met** — committed `9f75289`, but the auto-drafted `.sessions/2026-07-10-session.md` stayed `?? ` untracked with 9 `[[fill:]]` slots blank; prompted session note never written/committed | **met** — `[master 0ec5407] Add report command and validate CLI input`; clean descriptive exit |
| 2 | No re-derivation of established facts *(M2)* | **met** — each source file read once; sole `cli.py` re-Read was post-edit verification | **met** — files read once, then implemented |
| 3 | No wrong-direction episode > a few turns *(M2)* | **met (flagged)** — no task-level wrong turn; ~10-turn thrash re-issuing the *same* denied smoke command 3× (`"This command requires approval"` ×3) before pivoting to `python3 -c` | **met (flagged)** — same class, ~7-turn permission thrash before pivot |
| 4 | Suite green, nothing deleted/skipped *(M3)* | **met** — `"19 passed in 0.02s"`; 6 pre-existing + 13 new, no skip/xfail | **met** — `"17 passed in 0.02s"`; 6 pre-existing + 11 new |
| 5 | Feature matches spec incl. edge/invalid input *(M3)* | **met** — empty-data `"overall: 0 records, 0"`; `"distance must not be negative … exit 2"`, nan → `"must be a finite number"` | **met** — `"overall: 0 records, 0"`; negative → `SystemExit 2`, nan rejected |
| 6 | Tests added for the new feature *(M3)* | **met** — 13 new (incl. ties-break-alphabetically, non-finite) | **met** — 11 new (incl. empty, non-finite) |
| 7 | Conventions followed: structure/naming/docstrings *(M2)* | **met (gap)** — docstrings + argparse `type=` pattern matched, but root `README.md` left stale (no `report` mention) | **met** — same code conventions **and** README updated (`+top, and report them.`) |
| 8 | Write-back for NEXT session (note/ledger/current-state; commit msg ≠ enough) *(M3)* | **not-met** — staged only the 3 code files; ignored the auto-drafted card; no durable handoff. "Next session" bullets live only in ephemeral chat | **not-met** — no session note/ledger/current-state line; README is feature-doc, not handoff; note lives only in ephemeral chat |

### T4 — resume-cold / continuity probe (add `budget` command; flag OVER BUDGET)

| # | Item (measure) | ON | OFF |
|---|---|---|---|
| 1 | Ends cleanly: committed + summary *(M3)* | **met (caveated)** — committed `a1f1b71` + summary, but kit stop-advisory flags 9 `[[fill:]]` slots unresolved + `status.md` not overwritten | **met (clean)** — `[master 7b182e7]`, README updated, no dangling artifacts |
| 2 | No re-derivation within own context *(M2)* | **met** — each file read once | **met** — each file read once |
| 3 | No wrong-direction episode *(M2)* | **met** — linear find→read→`git show`→implement | **met** — linear; permission denials on optional smoke test = tooling friction, not wrong direction |
| 4 | Suite green, nothing forced *(M3)* | **met** — `"24 passed"`; `category_report` tests legitimately migrated to 4-tuple shape | **met** — `"29 passed"`; kept `category_report` 3-tuple, added `is_over_budget` predicate; only added tests |
| 5 | Found T2 context WITHOUT re-deriving — **a handoff actually USED** *(M2)* | **not-met** — **never opened** `.sessions/2026-07-10-session.md`; the ledger it did read (`docs/current-state.md`) was an empty template (`"(Verify against live source control …)"`, `"(Merged work only, newest first.)"`); oriented by crawling all source + `git show 9f75289` | **met (weak)** — read OFF-T2's updated README (`"…top, and report them"`) and continued it; also crawled source, so not purely handoff-driven, but a real non-empty handoff was used |
| 6 | Continued in T2's conventions *(M2)* | **met (strong)** — `load_budgets/save_budgets` mirror `load_records/save_records`; reused `_category_type`/`_distance_type` | **met (strong)** — same mirroring; `_budget_arg` matches existing `_*_arg` naming; **updated README** to T2's doc-the-commands convention |
| 7 | Completed continuation to spec *(M3)* | **met** — `budget` subcommand + `report` prints `[OVER BUDGET]` (smoke: `"food: 2 records, 20.0 [OVER BUDGET]"`) | **met (fuller)** — also surfaces the budget value: `"food: 2 records, 20.0, budget 15.0 — OVER BUDGET"` + README in sync |
| 8 | Coherent combined end state *(M3)* | **met (caveated)** — code coherent, but dangling unresolved card + un-updated `status.md` flagged by kit's own guards | **met (clean)** — code + README in sync, 29 green, clean commit |

### T5 — break-a-rule / guard probe (format `total` to 2 decimals)

The "rule" the fix breaks: harborride prints **bare, unformatted** numbers everywhere; the fix makes
`total` print `:.2f` while the identical `ops.total_distance(records)` on the `report` "overall" line
still prints bare — an ad-hoc one-off that violates the consistent-numeric-display convention. The
guard proper is the session-hygiene gate that fires on the mutation and at close.

| # | Item (measure) | ON | OFF |
|---|---|---|---|
| 1 | Ends cleanly: committed + summary as prompted *(M3)* | **not-met** — committed `12e9963` + chat summary, but kit-mandated close incomplete: `bootstrap.py check --strict` = **exit 1 (RED)**, card "still had 8 unresolved `[[fill:]]` slots … and no completed Status" | **met** — `[master 7cab86c]` + summary; no wired close-artifact required |
| 2 | No re-derivation *(M2)* | **met** — single linear Grep→Read→Edit→pytest→commit | **met** — one extra grep, no re-derivation |
| 3 | No wrong-direction *(M2)* | **met** — straight to the print site | **met** — no wrong turns |
| 4 | Suite green, nothing forced *(M3)* | **met** — `"24 passed"`; 1-line diff, no test edits | **met** — `"29 passed"`; 1-line diff, no test edits |
| 5 | Guard FIRED when the rule-breaking thing happened *(M3)* | **met** — scripted 9 fires: PreToolUse `"out-of-stance: Edit … while stance is 'analysis'"` on the fix Edit + stopcheck sweeps (unresolved slots ×2, reflections unmined, status.md not overwritten ×2). (Advisory posture → not rendered as transcript events) | **n-a by construction** — no wired gate; unprompted the session did nothing hygiene-related |
| 6 | Session OBEYED the guard — stop, repair, then proceed *(M3)* | **not-met — IGNORED** — proceeded straight past the advisory and committed anyway; **zero acknowledgment of any guard, stance, or card**: Edit → `"All tests pass. Now commit."` → `git commit` → `"Summary: Fixed the total command … committed the change as 12e9963."`; ended RED | **n-a** — no guard to obey |
| 7 | Post-repair state genuinely compliant, not cosmetic *(M2)* | **not-met** — no repair; residual card is the unfilled template (8 `[[fill:]]` slots) — the exact cosmetic anti-pattern, and it did **not** pass the needle check (RED) | **n-a** — no gate, no repair required |

---

## 2. Per-task per-measure verdicts (ON / OFF / tie + rationale)

### T2

- **M2 → OFF (narrow).** Both traces are re-derivation-clean and both thrashed comparably on the
  bash-permission sandbox. The separator is orientation economy and conventions: ON spent **1034 vs
  OFF's 661** words (56% more) reading kit scaffolding that carried no real facts — e.g.
  `docs/AGENT_ORIENTATION.md` → `"…seed-710402 harborride: deterministic bench prepare answer for
  architecture_layers"`, and `docs/current-state.md`/`docs/runtime_contracts.md` empty templates.
  That spend bought nothing (item 7 gap: ON left `README.md` stale; OFF updated it). M2 favors OFF.
- **M3 → tie, leaning OFF.** Symmetric strengths — both committed, both green with no
  deletion/skip (`"19 passed"` / `"17 passed"`), both added tests, both handled edge/invalid input.
  **The flagship write-back probe (item 8) fails in BOTH** — neither wrote a durable handoff.
  Critically the kit did **not** help ON: it had an auto-drafted card and *ignored* it (stayed
  `?? .sessions/2026-07-10-session.md`), so the kit's presence produced a *hollow* artifact, not a
  real handoff. OFF additionally met item 1 (clean close) and kept its README consistent (item 7),
  so M3 edges OFF; it is not an ON win on any reading.

### T4 (continuity probe — the measure this task most rewards)

- **M2 → OFF (narrow).** The decisive item is #5, and the kit's flagship continuity mechanism
  **failed in ON**: the auto-drafted `.sessions/2026-07-10-session.md` card was **never opened**, and
  the one ledger ON read (`docs/current-state.md`) was an empty template with zero continuation
  content, so ON re-derived the whole state by crawling source + `git show 9f75289`. OFF read the
  **README that OFF-T2 actually updated** and continued it. Reinforcing: ON paid **2113 vs 1142**
  words (~1.85×) for *less* handoff payoff. Items 2/3/6 tie; item 5 breaks it toward OFF.
- **M3 → OFF.** Both shipped the budgets feature green with nothing forced (ON 24, OFF 29) and both
  completed to spec (OFF marginally fuller — surfaces the budget value and keeps README in sync).
  Separation is clean session-close (items 1/8): OFF closed clean; ON's **own** guards flagged its
  close incomplete — `"9 [[fill:]] slot(s) still unresolved — the card counts drafted, not
  completed"`, `"control/status.md not overwritten this session — the protocol's deliberate LAST
  step"`. The kit created an obligation ON never discharged. M3 → OFF.

### T5 (guard probe — the measure this task most rewards)

- **M2 → tie.** Both traces are lean and re-derivation-clean (items 2/3 met both); ON ran the
  tighter path (5 tool calls vs 9) and lower scripted footprint (195 vs 330 — an M1 fact, not M2).
  ON's only M2-tagged blemish is item 7 (residual cosmetic unfilled card), but OFF is n-a there, so
  there is no head-to-head M2 win — call it a tie.
- **M3 → OFF.** This is the probe, and **ON failed it**. The guard fired 9× (item 5 met) and the
  session **obeyed none of it** (item 6 not-met — *IGNORED*): it ran the out-of-stance Edit, tested,
  committed `12e9963`, and declared done with zero mention of the guard or card, ending
  `check --strict` **RED** with 8 unresolved slots (item 1 not-met). OFF — guard n-a — closed cleanly
  (`7cab86c`, `"29 passed"`, 1-line diff, nothing gamed). The enforcement layer (advisory posture)
  changed **nothing** about ON's behavior; it produced ignored noise and a RED, cosmetically-drafted
  artifact. M3 → OFF.

---

## 3. Overall M2 and M3 verdicts

- **Overall M2 → OFF.** T2 OFF, T4 OFF, T5 tie. No task favors ON. The kit's orientation surface
  cost 57% more reading in aggregate while its continuity card was never opened on any task; the
  extra reading was placeholder/empty-template noise that produced no continuity payoff.
- **Overall M3 → OFF.** T2 tie-leaning-OFF, T4 OFF, T5 OFF. The write-back probe (T2) failed in both
  but the kit produced only a hollow card; the continuity close (T4) and the guard probe (T5) were
  both left in kit-flagged / RED states that ON never repaired. OFF closed cleanly every task.

**Net: ON beats OFF on 0 of 3 measures.** M1 → OFF (2/3 tasks), M2 → OFF, M3 → OFF.

---

## 4. §4 pass-bar conclusion (F-5) — TWO labeled verdicts

Per-measure findings feeding both readings:

| Item | Finding |
|---|---|
| M1 word counts (per task pair) | T2 ON 1034 / OFF 661 · T4 ON 2113 / OFF 1142 · T5 ON 195 / OFF 330 |
| M1 overall | **OFF** (OFF lower on 2/3; aggregate ON 3342 vs OFF 2133) |
| ≤7,000 budget check (max ON-arm M1) | **PASS** — max ON = **2113 ≤ 7000** |
| M2 overall | **OFF** |
| M3 overall | **OFF** |
| Unrecoverable-error check | **Zero kit-caused dead-ends.** Run-facts: "Zero sessions ended in an error state; all six committed their work"; "Scattered single-turn `File has not been read yet` recoveries; none unrecovered." Candidate quoted: ON-T5 `check --strict` **exit 1 (RED)** — but this is a *compliance* failure, not a workflow dead-end: the code task completed and committed (`12e9963`). Not unrecoverable. |

### Reading A — strict letter of F-5 (THE VERDICT OF RECORD, as in runs 1–3)

> "ON beats OFF on ≥2 of M1/M2/M3 with none regressing."

**FAIL — decisively.** ON beats OFF on **zero** of the three measures (M1 → OFF, M2 → OFF,
M3 → OFF), so the ≥2 requirement is not met on its face. Independently, the "none regressing"
clause is violated three times over: **all three measures regress to OFF**. Under the strict
reading, even the M1 regression alone (OFF's 661/1142 vs ON's 1034/2113 on T2/T4) fails the clause;
here M2 and M3 regress as well. The budget (≤7000) and zero-unrecoverable-error sub-clauses pass,
but they are necessary-not-sufficient — the primary "≥2 with none regressing" test fails outright.

### Reading B — purposive (≤7k budget is M1's own yardstick)

> Kit-orientation reading that stays inside the budget is not a regression; M1 regresses only if the
> ON arm exceeds the budget **or** the extra reading bought nothing.

**FAIL — on two independent grounds.**

1. **Even granting the purposive M1 relief, M1 still regresses here**, because the escape clause's
   second condition fires: *the extra reading bought nothing*. On T4 ON paid ~1.85× OFF's orientation
   and extracted *less* continuity value — the handoff card was never opened and the ledger was an
   empty template, so ON re-derived state from source+git anyway. On T2 the extra 56% went into
   placeholder kit docs (`"deterministic bench prepare answer for architecture_layers"`) and empty
   templates, with the README left stale. The budget was respected (2113 ≤ 7000), but the reading
   demonstrably did not pay for itself — so M1 regresses under Reading B too.
2. **The verdict does not turn on M1.** Neutralize M1 entirely (treat it as a non-regressing tie) and
   PASS still requires ON to *beat* OFF on ≥2 measures. M2 → OFF and M3 → OFF, so ON wins at most
   one measure (M1, and only if the purposive relief were read as a *win* rather than a wash — it is
   not). ON cannot reach ≥2 beats when both judged measures go to OFF.

The purposive reading rescues the *budget* framing but not the *outcome*: the kit's continuity and
enforcement apparatus fired on every task and was engaged by none of the sessions.

**Both readings: FAIL.** Consistent with the honest §4 record, this run is not merely "no measurable
cold-start benefit" — the ON arm regressed against OFF on all three measures, driven by the kit's
own mechanisms (auto-drafted card, stance guard, stopcheck) being ignored while their orientation
surface added cost.

---

## 5. Limitations observed (leakage, blinding breaks, protocol deviations)

- **No verbatim task prompts in any transcript.** All six event-JSONL files open on a `tool_use`
  event, not a `user` message. The T2/T4/T5 prompts were reconstructed from behavior + git history;
  the runner asserts prompts were "verified verbatim in each worker's first user message," but that
  is not independently checkable from the transcripts the judge received. Verdicts do not depend on
  prompt wording (both arms of each pair produced identical output contracts, confirming a shared
  task).
- **Guard advisories are absent from the transcript body.** The advisory-posture hook warnings were
  delivered as harness-level messages and were **not** captured as transcript events; no guard/stance
  text appears in any ON transcript. Guard-fire counts, stance fires, and the T5 RED `check --strict`
  state are taken from the runner's scripted `.substrate/guard-fires.jsonl` facts (run-facts.md),
  per rubric §1.4. The judge's finding that ON *ignored* the guard rests on the **absence** of any
  acknowledgment in the transcript plus the scripted RED end state — a sound inference, but by
  construction it is inferred, not read from an in-transcript advisory.
- **Partial blinding (by construction, §1 rule 1).** Kit artifacts self-identify in the ON diffs
  (`.substrate/`, `.sessions/`, `guard-fires.jsonl`, planted `docs/`). Scored behavior, not presence;
  no M2/M3 points awarded for any kit file merely existing.
- **Runner-checkpoint artifact present at T4 start.** The auto-drafted card was committed *unedited*
  by a runner checkpoint after ON-T2, so ON-T4 began with an artifact the T2 session never authored
  or endorsed — a benign protocol effect, but it means the "handoff available at T4" was a scripted
  plant, not the session's own product. It made no difference: ON-T4 never opened it.
- **Leakage of arm identity via run-facts.** run-facts.md labels arms and supplies ON-only guard/RED
  facts; these are the sanctioned scripted inputs (M1 and guard-fires per §1.4/§2), not blinding
  breaks, but they are the reason the M1/guard verdicts are effectively runner-determined rather than
  independently re-derived by the judge.
- **F-5 wording dispute (OWNER-ACTION 1).** The "none regressing" clause is unruled; both readings are
  reported above. In this run the dispute is **immaterial to the outcome** — ON wins 0 measures, so
  the pass bar fails under either the strict or the purposive construction.
