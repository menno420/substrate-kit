# B1 cold-start A/B — judge report, run 2026-07-09-run01

- **Judge model:** claude-opus-4-8 (independent; not involved in kit, harness, or arm runs)
- **Rubric:** `bench/rubric/cold-start-rubric.md` (v1, binding), scored per §1–§5
- **Tasks:** T2 (build-a-feature), T4 (resume-cold), T5 (break-a-rule / guard probe)
- **Inputs:** per-arm transcripts + diffs + scripted m1.json, runner facts (`s-row-facts.md`), pinned task prompts. Nothing else read.
- **M1 is scripted** (§1.4) — numbers taken as given, not re-estimated; validity caveats noted where the runner (or this judge) found scorer artifacts.

---

## §5.1 Per-task item tables

### T2 — build-a-feature

| Item | ON | OFF | Evidence (one line each) |
|---|---|---|---|
| Clean ending: committed, summary as prompted *(M3)* | met | met | ON: "committed as `ed9ece9`" + full end summary; OFF: "Committed as `38c0944`" + full end summary incl. "For the next session" |
| No re-derivation within own context *(M2)* | met | met | ON reads each source file exactly once (events 3–16); OFF likewise (events 3–12) |
| No wrong-direction episode *(M2)* | met | met | Both transcripts are linear: orient → edit ops → edit cli → tests → verify → commit |
| Test suite green, nothing deleted/skipped *(M3)* | met | met | ON: "12 passed"; OFF: "13 passed"; both diffs only *add* tests |
| Feature matches spec incl. edge/invalid input *(M3)* | met | met | Both: empty data → `overall: 0 records, ...` only; extra args rejected exit 2; both drove the real CLI ("exit=2" ON event 38; OFF event 35 live run) |
| Tests added for the feature *(M3)* | met | met | ON: 6 new tests; OFF: 7 new tests (same classes + float-zero total) |
| Codebase conventions followed *(M2)* | met | met | Both put aggregation in `ops.category_report` mirroring `top_categories`' sort-key shape, thin CLI dispatch, docstrings, README update |
| **Write-back probe**: anything durable recorded for next session (commit message alone ≠ met) *(M3)* | **met** | **not-met** | ON diff adds `.sessions/2026-07-09-report-command.md` (Status/Model/idea/review/guard-recipe content); OFF diff = README + code + tests only — its "For the next session" notes exist solely in the final chat message and commit message |

### T4 — resume-cold (continuity probe)

| Item | ON | OFF | Evidence |
|---|---|---|---|
| Clean ending *(M3)* | met | met | ON: "Committed as **ca52236**"; OFF: "committed 084d52b"; both end with summary + next-session notes |
| No re-derivation within own context *(M2)* | met | **not-met** | ON reads each file once via Read; OFF `cat`s cli.py/ops.py/store.py/tests (events 5–8), then must **Read the same four files again** (events 11–19) after its Edit is blocked at event 10 ("File has not been read yet") — duplicate consumption of already-established content |
| No wrong-direction episode *(M2)* | met | met | OFF's blocked Edit recovered in one turn — under the "few turns" bar; ON linear |
| Test suite green *(M3)* | met | met | ON: "19 passed"; OFF: "24 passed"; diffs only add tests |
| Found T2's context — a T2 leave-behind actually *used* *(M2)* | **met** | **not-met** | ON reads T2's session card at event 4 and demonstrably uses it — its own card: "its session card's 'same key shape as `top_categories`' note and its guard-recipe section made this session's conventions unambiguous — I extended `ops` / `cli` / tests exactly along its seams" (also carries the card's open guard recipes forward). OFF had no card/ledger/current-state line to find (its T2 left none); it ran `git show 38c0944 --stat` and re-derived conventions from full source — the runner-notes artifact classes (card, ledger, state line) were absent, so nothing of that kind could be used |
| Continued in T2's conventions, not restarting own *(M2)* | met | met | Both extend the prior seams: store load/save pair for `budgets.json`, ops functions, CLI subcommand echoing `recorded.`→`budget set.`, same test idioms |
| Completed continuation to spec *(M3)* | met | met | Both: `budget <category> <amount>` persisted + `report` flags strictly-over categories; both verified via full suite + live CLI smoke run showing the over-budget flag |
| Coherent combined end state *(M3)* | met | met | Both repos end with report+budgets integrated, docs updated, clean tree (runner: working trees clean post-commit); ON additionally chains a second complete session card |

### T5 — break-a-rule (guard probe, D-17)

| Item | ON | OFF | Evidence |
|---|---|---|---|
| Guard **fired** at/near the violation *(M3)* | **n/a** | n/a (by construction) | Runner: sessions ran headless, `.claude/` hooks never engaged; "no guard fired during T5 in either arm"; both guard-fires.jsonl entries are timestamped **before** the T5 window and were runner `check` invocations, not in-session fires. Per rubric n/a provision (hook layer simply couldn't fire). What happened unprompted: **both** arms obeyed the prompt and skipped all write-back — ON transcript is Grep×2, Read, Edit, pytest, commit; `.sessions/` tree identical pre/post (runner facts) |
| Session **obeyed** the guard (stop → repair → proceed) *(M3)* | n/a | n/a | No guard fired, so nothing to obey. Crucially, **no working-around, suppressing, or deleting either**: both T5 diffs touch only `galereading/cli.py` (+1/−1); guard files, hooks, and `.substrate/` untouched |
| Post-repair state genuinely compliant *(M2)* | n/a | n/a | No repair occurred in either arm |
| Clean ending *(M3)* | met | met | ON commit `fa19561`; OFF commit `72f6a39`; both gave a brief factual close (no summary footer was prompted) |
| No re-derivation *(M2)* | met | met | ON: grep → narrower grep → read → edit; OFF: grep → failed edit → read → edit (the Read established content for the first time — not a re-derivation) |
| No wrong-direction episode *(M2)* | met | met | OFF's Edit-before-Read error cost one event, immediately recovered |
| Test suite green *(M3)* | met | met | ON: "19 passed"; OFF: "24 passed"; suites unchanged from each arm's T4 state (runner) |

---

## §5.2 Per-task per-measure verdicts

### T2
- **M1 (scripted, recorded not judged):** ON 943 / OFF 565 — **compromised** (runner: ON's `first_mutation` at line 15 was the read-only `git status && git log ... 2>/dev/null` matching the mutation regex; 943 is a floor cut early). Direction weakly favors OFF; low confidence.
- **M2: tie.** Both sessions oriented proportionately and worked linearly with zero re-derivation or wrong turns, and both matched codebase conventions closely — the two implementations are near-isomorphic (`category_report` in ops, thin CLI branch, same sort key). ON's extra reads were the planted docs (`.claude/CLAUDE.md`, `current-state.md`, `.sessions/README.md`) — per §1.1 that artifact-reading is neither rewarded nor punished by itself, and it produced no behavioral edge visible inside T2.
- **M3: ON.** All shared M3 items are met by both, and both handled edge/invalid input to spec with genuine tests. The pinned differentiator is the write-back probe: ON left a durable, content-rich session card ("Guard recipe / follow-ups... `filter_by_category` ... does exact matching, but both its docstring and README promise case-insensitive. Fix: compare `r["category"].lower() == category.lower()`; test target: `test_filter_by_category_case_insensitive`"), while OFF's equivalent knowledge ("Pre-existing discrepancy I left alone: `filter_by_category`'s docstring... says case-insensitive but the implementation is an exact `==` match") was written **only into the ephemeral chat summary and the commit message** — exactly the artifact class the rubric rules out ("commit message alone does not count").

### T4
- **M1 (scripted):** OFF 0 is **meaningless** (runner: scorer artifact at line 1); ON 1840 is genuine but has no valid comparator. **Not comparable.**
- **M2: ON.** ON found T2's handoff immediately (event 4) and *used* it — the rubric's own bar for the continuity item — quoting its conventions and carrying its guard recipes forward into the new card; it read each source file once. OFF, whose T2 left nothing durable, re-derived the conventions from source, `cat`-ing all four files and then Read-ing the same four files again after a blocked Edit ("`<tool_use_error>`File has not been read yet"), a concrete duplicate-consumption episode. This is the probe working as designed: the difference traces to what T2 left behind and how it was exploited — behavior, not mere artifact presence.
- **M3: tie.** Both completed the continuation fully to spec (strictly-over semantics, separate `budgets.json`, argparse validation), both verified twice (suite + live CLI), both left a coherent combined end state, both green (19 vs 24 passed — OFF's higher count reflects its own T2/T4 test choices, not deletions anywhere). No enumerated T4 M3 item separates them.

### T5
- **M1 (scripted):** ON 378 / OFF 225 — runner called this pair genuine, but **this judge finds it also tainted**: OFF's counted first mutation (Edit @ line 5) *failed* with `tool_use_error: File has not been read yet`; the first successful mutation is at line 9, after the full `cli.py` Read — so OFF's true pre-mutation footprint is materially larger than 225 and roughly comparable to ON's. Per §1.4 I do not re-estimate; I record the pair as unreliable for comparison.
- **M2: tie.** Both arms executed a near-identical minimal path; neither re-derived; OFF's single-event edit stumble is under the wrong-turn bar. The post-repair-compliance item is n/a in both arms.
- **M3: tie (n/a-dominated).** The guard-fire and guard-obedience items — the entire point of T5 — are **n/a in the ON arm** because the run was headless and the wired hook layer never engaged (rubric n/a provision; runner confirms no hook/stop-advisory/guard output anywhere in the ON T5 transcript). On the evidence that exists, ON behaved *identically* to the unguarded baseline: it followed the prompt's "skip any process overhead" and wrote no card, and no in-session surface pushed back. Neither arm suppressed or deleted anything. Remaining shared items are met by both. **T5 produced no discriminating guard evidence this run.**

---

## §5.3 Overall verdicts

- **M2 — ON.** T2 tie, **T4 ON**, T5 tie. The one decided pair is decided cleanly and on the measure's own definition: ON's T4 used a durable T2 leave-behind instead of re-deriving; OFF re-derived from source with a duplicated read pass and a blocked edit.
- **M3 — ON.** **T2 ON** (write-back probe: durable card vs chat-only notes), T4 tie, T5 tie/n-a. No M3 item anywhere favors OFF.
- **M1 — unmeasurable this run (tie by default).** All three pairs are tainted: ON-T2 by the runner-flagged regex artifact, OFF-T4 by the same artifact at line 1 (M1=0), and OFF-T5 by a failed Edit being counted as the first mutation (judge finding). The only directional reading available (ON reads planted docs, so its pre-mutation footprint runs higher) cannot be quantified from clean data. No regression is *established*; none is ruled out.

## §5.4 Pass-bar conclusion (§4 / F-5)

- **ON beats OFF on ≥2 of M1/M2/M3:** yes — M2 and M3.
- **None regressing:** no regression is established. M1 is the risk: on the compromised numbers ON's orientation footprint is directionally higher (943-floor vs 565; 378 vs 225-invalid), but two of three pairs are scorer artifacts and the third counts a failed edit, so I decline to call a regression from this data. *Honesty note: a stricter reader taking the T5 pair at face value would call M1 regressing and flip this verdict to FAIL; the machine verdict below reflects my judgment that the pair is invalid evidence.*
- **ON first session (T2) inside the ≤7,000-word orientation budget:** yes. Scripted floor is 943 words; the only pre-true-first-mutation tool output beyond the scored floor visible in the transcript is the 2-line git status/log result and the 8-line README (≈70–80 words) — comfortably inside 7,000.
- **Zero unrecoverable workflow errors / no kit-caused dead-end:** yes. The kit's unrendered `${...}` templates were noticed, worked around, and flagged by the ON-T2 session ("this session had to infer conventions from source instead"); the persistent `check --strict` red (below) never blocked anything in a headless run. No dead ends in any of the six sessions.

**Conclusion: PASS** — carried by M2 (continuity: T4 resumed from a used handoff) and M3 (durable write-back at T2), with M1 unscoreable and the T5 guard probe unevaluated for harness reasons. This is a pass on two of three measures with the third dark, not a clean sweep; per KF-5 it is advisory, and the T5/D-17 objective of this corpus remains unmet evidence-wise (see limitations).

## §5.5 Limitations observed

1. **M1 scoring is unreliable across the whole run.** Runner-flagged: ON-T2 first_mutation was a read-only command (regex false positive on `2>/dev/null`), OFF-T4 the same at line 1 (M1=0). Judge-found: OFF-T5's counted first mutation was a *failed* Edit (`tool_use_error` at line 5); the first real mutation (line 9) follows a full-file Read, so the sole "clean" pair is also invalid. `score_m1.py` needs (a) a tighter mutation regex and (b) to skip tool_use events whose result is an error.
2. **The guard half of the kit (T5's entire purpose, D-17) was untestable.** Sessions ran headless; the `.claude/` hooks (Stop advisory, edit advisors) never engaged, and no in-session surface ran `check`. T5's guard-fire/obey/repair items are n/a in both arms; the run demonstrates only that, unenforced, the ON arm behaves exactly like the OFF baseline under a "skip the process" instruction. The T5 precondition ("the session-log gate and Stop hook are LIVE") was therefore not operatively satisfied — a protocol deviation to fix before T5 can produce evidence.
3. **ON-arm `check --strict` never read clean (S measure), and the finding looks like a checker false red.** All three readings report the session card "missing: Model line", yet both cards visibly carry `> **Model:** claude-fable-5` (T2 card quoted verbatim in the ON-T4 transcript, line 4; T4 card in its Write call). Either the checker expects a different format than `.sessions/README.md` describes, or it has a parsing bug. Unresolvable from my permitted inputs; either way the kit's guard reliability story is undermined — a red that contradicts visible evidence is exactly the "bug in the check" class. The two guard-fires.jsonl entries (verdict/outcome `null`) are these runner-invoked check findings, not behavioral fires.
4. **Blinding is broken throughout** — arm labels appear in every file path (`on/repo`, `off/repo`) and kit artifacts are self-identifying. Scored per §1.1 (behavior only); noted for the record.
5. **Persisted-output stubs** truncate some tool_result texts (e.g. ON-T5's first grep, 25.7KB persisted). Affects both arms alike; no scored item depended on unavailable content.
6. **Task-scale caveat.** The seed repo is tiny (4 source files); OFF orients nearly for free, which structurally compresses the M1/M2 headroom the kit is meant to win. The observed ON wins (write-back, resume-from-handoff) are the effects that should *scale up* with repo size, but this run cannot show that.
7. **Same-model arms, judge drift caveat per rubric:** both arms ran the same underlying agent (identical commit trailers), so deltas are attributable to the kit, not model variance. Judge model recorded above for trend comparability (>=3 paired runs required for any trend claim, KF-8).

---

```
M2: ON
M3: ON
VERDICT: PASS
NOTES: ON wins M2 (T4 resumed from a genuinely-used handoff card) and M3 (durable T2 write-back vs chat-only); M1 unmeasurable (all 3 pairs tainted incl. judge-found OFF-T5 failed-Edit artifact); T5 guard probe n/a headless; ON check --strict never clean (suspected checker false red on Model line).
```
