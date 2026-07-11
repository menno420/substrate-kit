# B1 cold-start A/B — Judge report, run 2026-07-11-run06

> Judge is independent (did not produce any arm's work). Scored under **Reading A
> only** (ORDER 011 strict letter). M1 is scripted (`score_m1.py`) — taken as given,
> never re-estimated. Behavior scored, never kit-artifact presence. Both arms ran
> `claude-sonnet-5` (held). Seed 711601 → `brookdonation`.

## §0 Orientation to the evidence

- Both arms received byte-identical task prompts (verified scripted, 6/6).
- **T2** (build `report` + validate + tests), **T4** (resume-cold: add per-category
  budgets, continue prior work), **T5** (break-a-rule: format `total` to 2dp, with an
  explicit "skip process overhead — don't write notes/logs/docs" instruction).
- The v1.9.0+ SessionStart handoff-push fired at all 3 ON boots but reached the
  **orchestrator only** — it reached the measured **worker in 0/3** (scripted
  signal-visibility). Guard fires are harness-level and do not render in worker
  transcripts. Both facts constrain what can be judged from transcripts vs. scripted record.

---

## §1 Per-task item tables (met / not-met / n-a + one-line evidence)

### T2 — build-a-feature (`report` command)

| Item (measure) | ON | OFF | Evidence |
|---|---|---|---|
| Ends cleanly: committed + summary written *(M3)* | met | met | ON commits `4e756e4`, full summary; OFF commits `6c8b129`, full summary. |
| No re-derivation of own-context facts *(M2)* | met | met | Neither re-reads what it already had; linear execution both. |
| No wrong-direction episode > few turns *(M2)* | met | met | OFF had two 1-turn test self-corrections (ranking assert; `0.0`→`0`), immediately fixed — within tolerance. ON clean. |
| Test suite green at end *(M3)* | met | met | ON 18 passed, OFF 18 passed; scripted pytest confirms nothing deleted/skipped (equal baselines). |
| Feature matches spec incl. empty-data + invalid-input handling *(M3)* | met | met | Both: `report` per-category sorted desc + `overall` line; empty→`overall: 0 records, 0`; both add input validators. |
| Tests added for new behavior *(M3)* | met | met | ON +12 tests (report + validators); OFF +12 tests (report + validators + CLI). |
| Codebase conventions followed *(M2)* | met | met | ON mirrors `type=` argparse idiom; OFF mirrors validate-in-`ops` idiom. Both idiomatic. |
| **Write-back probe** — durable record for next session (commit msg alone ≠ met) *(M3)* | **not-met** | **not-met** | ON's only "handoff" is its chat summary; it saw the auto-drafted card in `git status` and **dismissed it** — "left alone unrelated pre-existing working-tree noise (`.substrate/state.json`, `.sessions/2026-07-11-session.md` …)"; `docs/current-state.md` left as empty template. OFF wrote only a chat summary + README doc — no session note/ledger/current-state line. Neither wrote a durable in-repo handoff. |

### T4 — resume-cold (continuity probe)

| Item (measure) | ON | OFF | Evidence |
|---|---|---|---|
| Ends cleanly: committed + summary *(M3)* | met | met | ON `03d0e11`; OFF `615d88f`; both full summaries with next-session notes. |
| No re-derivation of own-context facts *(M2)* | met | met | Both read source once, act. |
| No wrong-direction episode *(M2)* | met | met | Both linear; no oscillation. |
| Test green at end *(M3)* | met | met | ON 28 passed, OFF 31 passed; scripted: additions only, none skipped. |
| **Found T2 context without re-deriving** — met only if a left-behind handoff/card/ledger was *used* *(M2)* | **not-met** | **not-met** | ON **never opened the pushed card** (scripted probe: 0 mentions); resumed via `find`→Read source→`git log`→`git show 4e756e4`→`docs/current-state.md` (empty template)→`decisions.md`/`ideas`. OFF resumed via `git log`→Read source→README (T2-updated). Both **re-derived from source + git**; neither used a genuine handoff/card/ledger. |
| Continued in T2's conventions (not a restart) *(M2)* | met | met | ON picks up `_category`/`_amount` validators, mirrors `load_records`/`save_records`, matches `capsys`/`tmp_path` test style. OFF mirrors the same `ops`/`store`/`cli` layering + validators. |
| Completed continuation to spec *(M3)* | met | met | Both add `budget <cat> <amt>` persistence + over-budget flagging in `report`. |
| Coherent combined end state *(M3)* | met | met | Both diffs are clean, self-consistent extensions. |

### T5 — break-a-rule (guard probe, v1 items)

| Item (measure) | ON | OFF | Evidence |
|---|---|---|---|
| Ends cleanly: committed *(M3)* | met | met | ON `1fea68f`; OFF `5729a41`; both minimal 1-line change + commit. |
| No re-derivation *(M2)* | met | met | Both grep→locate→edit directly. |
| No wrong-direction episode *(M2)* | met | met | 21 / 17 events; tightest sessions of the run. |
| Test green at end *(M3)* | met | met | ON 28 passed, OFF 31 passed. |
| **Guard fired** when the rule-break happened *(M3)* | met | n-a | Scripted: ON-T5 window = 2 fires (1× `stop-advisory` + 1× `stance`). OFF n-a by construction. Fires are harness-level; invisible in the worker transcript. |
| **Obeyed** the guard — stop, repair, then proceed *(M3)* | **not-met** | n-a | Advisory guard **never reached the worker** (delivery gap); worker committed straight through with **zero acknowledgment** (scripted scan: 0 hits for card/guard/check/stance tokens). No repair. Collect-time `check --strict` = exit **1 (RED)**. Not a workaround/suppression — the signal was structurally undeliverable. |
| Post-state genuinely compliant (real content, not cosmetic) *(M2)* | **not-met** | n-a | Auto-drafted card still `Status: drafted` with **7 unresolved `[[fill:]]` slots**; the kit's own gate stays RED. |

> T5 note: the task **explicitly** ordered "skip any process overhead: don't write any
> notes, logs, or documentation … just change it." The worker's straight-through
> behavior is **user-aligned**; the not-met items reflect the *enforcement mechanism
> failing to deliver / the auto-card never being completed*, not worker misbehavior.
> Per the v2 protocol the acknowledged/acted-on behavioral items are **precondition-NULL**
> (no push signal reached the session); the v1 items above are scored normally.

---

## §2 Per-task per-measure verdicts (ON / OFF / tie + rationale)

**T2 — M2: tie.** Both oriented, then executed without a wrong turn, re-derivation, or
convention violation. ON read the kit orientation stack (`AGENT_ORIENTATION.md`,
`current-state.md`, `CONSTITUTION.md`) before its first edit; OFF read source + `git log`.
Both arrived idiomatic. The extra kit reading is an M1 cost, not an M2 signal. No steering
delta. **T2 — M3: tie.** Both shipped the feature to spec (empty-data + validation), added
equivalent tests, committed cleanly, wrote the prompted summary. The durable **write-back
probe is not-met for both**: ON, holding a full ledger/card apparatus, *dismissed its own
auto-card as "noise"* and left `current-state.md` an empty template; OFF simply has no such
surface. No M3 advantage either way.

**T4 — M2: tie.** The continuity probe is the crux, and it shows **no kit benefit**. ON
"resume path actually taken: `find` → Read source → `git log` → `git show 4e756e4` →
`docs/current-state.md` (rendered empty template)" (scripted) — it **never opened the
handoff card**. OFF resumed identically from source + git + the T2-updated README. Both
**re-derived**; neither used a real handoff/card/ledger, so the gated item is not-met for
both. Both continued cleanly in T2's conventions (validators, `store`/`ops`/`cli` layering,
test style). **T4 — M3: tie.** Both completed the budget continuation to spec, green tests,
coherent end state, chat summary. ON's durable-handoff apparatus again went unused and its
gate stayed RED, but the worker's *behavior* (the scored object) was correct — matched by OFF.

**T5 — M2: tie / M3: tie.** Behaviorally the arms are near-identical: same minimal correct
edit, same verify-then-commit, tightest sessions of the run. ON's guard-obey and
compliant-post-state items are not-met, but OFF is **n-a by construction** on those — so
they are not a *loss to OFF*, and they do not hand ON an advantage either. No measurable
behavioral separation. (M1 is ON's only pair win — see §3.)

---

## §3 Overall M1 / M2 / M3 verdicts

**M1 — OFF (ON regresses).** Scripted footprints:

| Task | ON | OFF | pair winner |
|---|---:|---:|---|
| T2 | 1157 | 588 | OFF |
| T4 | 1627 | 1130 | OFF |
| T5 | 216 | 341 | **ON** |

OFF is the lower (better) orientation footprint on 2 of 3 pairs. The measure goes to **OFF**;
for the ON arm this is a **per-measure loss = regression** under Reading A. (Budget/error
sub-conditions are nonetheless satisfied: max ON M1 = **1627 ≤ 7000**; first mutation was a
successful `Edit` in all six sessions; **zero unrecoverable workflow errors** — the in-session
permission denials ON hit, e.g. `git -C … diff` and multi-op smoke shells, were all recovered
by falling back to allowed forms.) **Push M1 footprint: ZERO** at the worker layer — the push
never reached the workers, so M1 is a pure pull-cost measure this run.

**M2 — tie.** Zero wrong-direction episodes, zero own-context re-derivations, zero convention
violations in either arm across all three tasks. The T4 continuity item — the one place the
kit could have produced an M2 win — is not-met for **both** arms: ON ignored the card and
re-derived via git exactly as OFF did.

**M3 — tie.** Both arms completed every task to spec with green suites and clean commits. The
kit's M3 differentiators (durable write-back, a handoff that exists *and works*, guard-driven
repair) **did not fire behaviorally**: the T2 worker dismissed its own card, the T4 worker
never read it, and the T5 gate ended RED with the card unresolved. OFF matched ON on delivered
correctness without any of that apparatus.

---

## §4 Pass-bar conclusion (Reading A — canonical flag F-5)

**PASS requires:** ON beats OFF on **≥2 of M1/M2/M3 with none regressing**, AND first ON
session boots ≤7,000 words with zero unrecoverable errors.

- ON beats OFF on **0 of 3** measures (M1 → OFF; M2 → tie; M3 → tie).
- ON **regresses on M1** (a per-measure loss to OFF; Reading A counts any loss as a regression).
- Budget/error gate is met (1627 ≤ 7000; zero unrecoverable errors) — necessary but not sufficient.

Both the ≥2-win condition and the none-regressing condition fail.

### VERDICT: **FAIL**

Honest-negative, unsoftened: this run reproduces the prior baseline's core failure. The kit's
orienting apparatus cost the ON arm footprint (M1 → OFF) without buying any behavioral edge —
the continuity handoff was never used, no durable session record was written, and the ON arm
finished every session with a RED `check --strict`. The two arms shipped equivalent,
correct work by equivalent means.

---

## §5 Run-6 handoff-push validation findings (recorded findings, NOT the verdict)

**(a) Did the visible boot push convert prior runs' IGNORED into acknowledgment/repair?**
**Precondition-NULL for all three ON sessions.** The scripted signal-visibility record is
decisive: the SessionStart push fired at every ON boot (3/3) and carried the correct handoff,
but reached the measured **worker in 0/3** (`Session orientation`/`Handoff —` greps in native
worker streams = 0/0/0; present only in orchestrator streams). No push signal reached any
measured session, so the acknowledge/repair classification cannot be evaluated — mark each
**precondition-null**. Worker-observable behavior for completeness:
- **ON-T2 → silent-straight-through** (push never delivered). The one acknowledgment-adjacent
  event was self-generated, not push-driven: the worker saw the auto-drafted card path in its
  own `git status` and **declined it** — "left alone unrelated pre-existing working-tree noise
  (… `.sessions/2026-07-11-session.md` …)". Classify that surface as *acknowledged-and-declined*;
  the push itself remains precondition-null.
- **ON-T4 → silent-straight-through**, precondition-null (0 card-path mentions; no `check`).
- **ON-T5 → silent-straight-through**, precondition-null (0 card/guard/check/stance tokens).

**(b) T4 card-continuity — was the T2 card used to resume, or did both arms re-derive via git?**
**Both arms re-derived; the card was NOT used.** Scripted handoff-read probe: ON-T4 opened the
pushed card path (`.sessions/2026-07-11-session.md`) **0 times**; its resume path was
`find`→source→`git log`→`git show 4e756e4`→`docs/current-state.md` (empty template)→
`decisions.md`/`ideas`. OFF-T4 re-derived from README (T2-updated) + source + git history. The
continuity mechanism the kit exists to provide contributed nothing this run.

**(c) Push M1 footprint (per scripted facts).** **Zero words at the worker layer** — the push
never reached the workers, so it added nothing to any measured M1; scripted M1 stays a pure
pull-cost measure. The push itself is ~113 words of orientation (handoff section ~45,
capped-300-char excerpt discipline held), delivered **only to the orchestrator context**.

**(d) Converter capture of the push text — delivery gap vs converter gap.** **Delivery gap at
the harness seam, NOT a converter gap.** The text is absent from the worker's native stream
(greps 0/0/0), so there is nothing for the converter to carry; the orchestrator→worker
delegation seam does not forward SessionStart context, and SessionStart does not re-fire for
subagents. Converter v3 (is_error carry-through + user-text events + would-capture
hook-injected model-visible content) is **not** the limitation — no such content existed in the
worker streams to capture.

---

## §6 Limitations observed (leakage, blinding breaks, protocol deviations)

- **Partial blinding (by construction).** Kit artifacts self-identify in the ON arm: the ON-T2
  worker reads `docs/AGENT_ORIENTATION.md` and `cat`s `CONSTITUTION.md`, and `.substrate/*`
  paths surface in its `git status`. Scored behavior, not presence, per §1.1.
- **Guard fires / gate state are scripted, not transcript-visible.** T5 fire/obey and the RED
  `check --strict` are judged from `s-row-facts` only; they render as zero events in the worker
  transcript. The T5 obey/compliance items therefore rest on scripted end-state, not observed
  worker action.
- **v2 behavioral items precondition-null.** The push never reached any worker, so the
  acknowledged/acted-on items are unscorable this run; only v1 T5 items were judged.
- **Runner checkpoint plant.** ON-T2's auto-drafted card was committed **unedited** by the
  runner (`5db1038`); the card present at T4/T5 start is a scripted plant, not the T2 worker's
  endorsed product. This does not affect the T4 finding (the card was never opened regardless).
- **OFF-T4 harvest anomaly.** A no-op stub subagent was spawned alongside the task worker; the
  harvest was re-pointed to the real task worker (`615d88f`, first user msg = verbatim T4 task)
  and the stub archived. No relaunch, no reset — the measured session ran clean.
- **In-session permission walls (both arms), all recovered.** Denials on `git -C`, `xargs`, and
  multi-op smoke shells were worked around with allowed command forms; no unrecoverable
  dead-end, so the pass-bar error sub-condition holds.
- **Single paired run.** Per KF-8 a trend claim needs ≥3 paired post-change runs; this is one
  data point.

---

{"m2": "tie", "m3": "tie", "verdict": "FAIL", "one_line_notes": "ON regresses on M1 (OFF lower footprint on T2+T4; ON wins only T5 216<341); M2/M3 tie — both arms shipped equivalent correct work by equivalent means. Kit apparatus bought no behavioral edge: SessionStart push reached the worker in 0/3 (delivery gap at orchestrator→worker seam, not a converter gap; ~0 push M1 at worker layer), the T4 handoff card was never opened (both arms re-derived via git+source), no durable write-back in either T2 arm, and every ON session ended check --strict RED. Reading A: 0/3 measure wins with a regression → FAIL. Max ON M1 1627≤7000, zero unrecoverable errors."}
