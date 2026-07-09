# Session 2026-07-09 — KL-2: the program governance home

> **Status:** `complete` *(kit-side KL-2 in one PR — #12. The superbot
> companion PR — provenance riders on the origin Q-blocks — is deliberately a
> separate increment, recorded in current-state ▶ Next action.)*

**What happened (founding plan §8 + §10 KL-2 row, kit-side):**

- **`docs/program/`** — the canonical program-governance home (KF-6):
  - `rulings.md` — the [PL-NNN] register, D-ledger grammar, all nine blocks:
    PL-001←Q-0240 (decide-and-flag) · PL-002←Q-0241 (never-wait rebuild
    autonomy, **verbatim to its provenance** — scope stays the rebuild, the
    lab's rails are not smuggled in) · PL-003←Q-0247 (rail before scale) ·
    PL-004←Q-0248 (empirical model allocation, both planes) · PL-005←Q-0249
    (observe-first budgets) · PL-006←Q-0120 (source-wins / false-green) ·
    PL-007←Q-0132 (enforce, don't exhort) · PL-008←Q-0105 (adopt freely +
    kill-switch) · PL-009 (the lab's own Q-0241-*shaped* ruling on its own
    provenance chain: capture row 5 + Q-0247 + plan §6.3/D-12). Q-blocks read
    verbatim from superbot origin/main (9e35130) and imported faithfully.
  - `README.md` — what the directory is + the §8.3 cite-never-copy /
    one-home / origin-pointer / checker sync rule.
  - `collaboration-model.md` + `agent-decision-authority.md` — canonical
    program copies, generalized from superbot's (repo-specifics stripped,
    program mechanisms kept; origin files stay as that repo's local docs).
- **`scripts/check_program_law.py`** (repo-level tooling, not engine — it
  inspects `src/engine/templates/`, which consumers never have on disk):
  PL-heading grammar + malformed-heading detection · required fields
  (status/date/**provenance**/verdict; superseded needs superseded-by) ·
  monotonic sequential IDs (no gaps, no dups, ascending) · pointer sections:
  the two designated templates MUST carry a "Program law" section citing
  `docs/program/rulings.md` + ≥1 PL-ID, and **no pointer section** (any
  template or the kit's own planted copies) may contain a ruling body — any
  8-word normalized run from a PL verdict inside a pointer section is a
  `body-copy` finding. Wired as a `kit-quality` step; PL-008 provenance +
  delete-if-unreliable header carried. 18 tests (fixtures + the real repo as
  ground truth), suite 483 → 501, all green in 2 s.
- **Template pointer sections** — `CONSTITUTION.md.tmpl` +
  `collaboration-model.md.tmpl` gain the "Program law" pointer (kit-repo URL
  + PL-IDs, no bodies); dist regenerated (`src/build_bootstrap.py`), byte-pin
  green. The kit's own planted `CONSTITUTION.md` + `docs/collaboration-model.md`
  got the same sections — consumer #0 cites the home, which is D7's
  "≥1 consumer citing it by pointer" until a real consumer upgrades.
- **`docs/house-style.md`** (§3.4/D-7): the 💡⚑⟲📊👤 marker grammar, born-red
  / PR-early doctrine, badge taxonomy, ADR path, GUIDED_ROLLOUT order —
  declared opinionated house style with fork-points named, never config.
- **Ledgers:** D-0002 (the convention + its checker); CHANGELOG
  `[Unreleased]` (MINOR — new checker + new template content); orientation
  router reaches the new docs; `ruff` excludes `scripts/` (CI-scope parity).
- **Drift fixed on sight:** KL-1's card + current-state said tag `v1.0.0`
  rides PR C's merge commit — it actually rides **PR D #11's** `daaf29c` (cut
  via the `workflow_dispatch` path). Both corrected.
- **Verified locally:** 501/501 pytest · fresh-dist byte-compare clean ·
  `dist/bootstrap.py check --strict` green (D7's done-condition) · ruff
  engine bans green · `check_program_law` OK on the real tree.

## ⚑ Flags

1. ⚑ Self-initiated: the no-body scan also covers the kit's **own** planted
   pointer copies (plan letter says template-side only) — same code path,
   and consumer #0 should obey the covenant it ships.
2. ⚑ Decide-and-flag: `check_program_law.py` lives at **`scripts/`** (repo
   tooling), not in the engine — it checks kit-repo-only surfaces
   (`docs/program/`, `src/engine/templates/`); engine placement would ship
   dead weight to every consumer. Revisit only if program law ever needs
   consumer-side enforcement.
3. ⚑ Decide-and-flag: body-copy heuristic = normalized 8-word n-gram overlap
   between PL verdicts and pointer sections, scoped to the *pointer section*
   (not whole templates — the collaboration-model template legitimately
   states the friction→guard doctrine in its own words; whole-file scanning
   would false-positive on PL-007).
4. ⚑ PL-007's provenance names Q-0132 (the census assignment) with the
   Q-0194 hardening noted inline — Q-0132's block is a capture index; the
   enforce-don't-exhort doctrine is its named durable item.

## 💡 Session idea

`check_program_law` gains a `--consumer` mode the *consumer's* substrate-gate
can run: verify the repo's local ledgers/router contain no PL-ID heading
collisions and no copied PL bodies anywhere in `docs/` (not just pointer
sections) — the cite-never-copy covenant enforced where the drift would
actually happen, at near-zero cost since the verdict n-grams can ship in the
kit's staged CI example. Natural KL-3/KL-4 rider once consumers upgrade.

## ⟲ Previous-session review (kl1-release-train)

Genuinely strong session: it turned two live merge-gate failures (#7
instant-merge on skipped aliases, #9 pre-close-out merge) into *engine-level*
guards the same day — exactly the PL-007 pattern — and the workflow_dispatch
release path converted a hard environment limit (403 on tag push) into a
mechanism that makes releasing agent-runnable at all. Miss: its own close-out
drifted — the card's Status line said the tag rides PR C's merge commit while
its own "PR D" section documented the dispatch path; nobody reconciled the
two before the flip (fixed this session). **Workflow improvement:** the
session gate checks badge *value* but nothing cross-checks a card's factual
claims against git at flip time; cheapest guard = the flip step of a future
`session-close` skill re-reading the Status line for commit/tag refs and
verifying them against `git tag --points-at` / merged-PR data before
flipping. Until then it stays a checklist instinct: re-read your Status line
last, not first.

## Docs audit

`check --strict` green (badges/links/reachability incl. the 5 new docs);
current-state updated (KL-2 kit-side DONE; Next action = superbot companion
riders → consumer pin PRs → KL-3); decisions/CHANGELOG/orientation updated;
nothing left chat-only.

- **📊 Model:** fable-5 · high · docs-only + test writing
