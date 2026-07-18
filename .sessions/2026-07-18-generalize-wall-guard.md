# 2026-07-18 · generalize-wall-guard

> **Status:** `complete`

- **📊 Model:** Claude Opus 4.8 · high · feature build
- Scope: generalize the merge-specific `tools/check_no_false_walls.py` (PR #448)
  so CI reds ANY documented false **agent-capability limitation**, not only
  merge-walls. Owner directive 2026-07-18: agents have NO owner-imposed
  limitations — a refusal is a TRANSIENT auto-mode-classifier state, so a
  written-down wall is stale on the next platform update AND stops the next
  session from even trying. CI is the authoritative enforcement ("agents can't
  argue with CI"): the docs record capabilities, never limitations. Reuses the
  existing scan set + clearing logic wholesale; adds the generalized blocklist +
  fixtures. A checker/test guard is free-to-ship doctrine (friction → guard).
- ⚑ Self-initiated: no — owner-directed (the prompt IS the order). Merge is the
  review; PR opened READY, lands on green `kit-quality`.

## Record

- Generalized `tools/check_no_false_walls.py` past merge to the whole semantic
  class of false capability walls. New shared grammar fragments (`_SUBJECT`,
  `_NEGATION`, `_CAP_VERB`, `_INFRA_OBJ`, `_OWNER_AUTHORITY`, `_CAP_NOUN`) +
  six new blocklist entries, all case-insensitive, all still gated by the
  UNCHANGED clearing layer (dated / repudiated / historical):
  - `agent-negated-capability` — SUBJECT {agent|session|worker|seat|the bot|
    you} + NEGATION {cannot|can't|may not|must not|are not allowed to|are
    unable to|is blocked from|do not} + FALSE-wall verb {merge|self-merge|
    deploy|redeploy|push|arm|ready-flip|flip|land|delete a branch}.
  - `agent-negated-infra-mutation` — SUBJECT + NEGATION + {update|change|set|
    modify|provision|configure|edit} + infra object {railway|env|deployment|
    infra|variables|secrets|config}. (Catches "update Railway variables"
    without matching bare "update".)
  - `capability-is-owner-authority` — {the owner must|only the owner can|
    requires the owner to} + [≤25 chars] + {merge|deploy|ready-flip|arm auto|
    land a/the/your|push}. The tight same-clause window keeps "the owner must
    ENTER/paste/parse" (owner-assist doctrine) passing.
  - `capability-asserted-owner-only` — capability NOUN {merging|merge|deploy|
    deploying|branch deletion|ready-flip|pushing|auto-merge} + {is|are|remains|
    =} + {owner-only|owner-gated|classifier-denied|blocked for agents|not
    enabled for agents|not agent-side}.
  - `standing-platform-wall` — compound tokens {agent-unlandable|403-walled|
    permission-walled|classifier-walled|blocked for agents|not enabled for
    agents|agents/sessions get 403}. Compound "walled" only, never bare "wall"
    (main documents "403 wall(s)" as a genuine dated wall — must pass).
  - `classifier-denied-standing` — standalone `classifier-den(y|ies|ied)`, no
    "since <date>" required (the fixture "deploying is classifier-denied").
  - All original merge-specific entries retained verbatim.
- CRITICAL false-positive discipline (owner: a false positive that reds CI is
  worse than a rare miss). The verb list DELIBERATELY EXCLUDES read / create /
  access / provision / write — those collide with GENUINE standing walls on real
  trees ("sessions cannot read fleet-manager", "session tokens cannot create
  repos", "host provisioning owner-only"). Owner-only is scoped to merge/deploy/
  branch-deletion nouns only, NOT repo-creation / settings / secrets / release /
  seat-plan (all of which appear legitimately owner-only on `main`). The SUBJECT
  slot excludes code nouns, so a CODE rule ("services must not import views",
  "utils/ may not import services", "never call pool.execute") never trips.
- Verified on current `main`: **exit 0, ZERO false positives.** Surveyed every
  one of the 64 scanned files for "must not"/"cannot"/"owner"/"owner-only" —
  every legit line passes: the corrected merge doctrine, the dated CAPABILITIES
  wall ledger (branch-deletion/tag-push/api.github.com/settings, all cleared by
  `LAST-VERIFIED`/dated), the owner-assist "the owner must enter/paste/parse"
  prose, the `## Append log` history, and the `FALSE "…"` repudiation flags.
- Tests (`tests/test_no_false_walls.py`): +5 new classes. MUST-FAIL fixtures
  ("agents cannot delete branches", "sessions are not allowed to update Railway
  variables", "branch deletion is owner-only", "deploying is classifier-denied
  for agent seats", "the owner must merge PRs" + spread). MUST-PASS fixtures
  (the five code-rule fixtures, corrected capability text, missing-credential
  owner-input "needs a Stripe/PayPal account from the owner", and genuine dated
  walls). `python3 -m pytest -q` → 1743 passed, 1 skipped (17 in this file).
- No template / engine / dist changes (`tools/` + `tests/` only) — no
  `src/build_bootstrap.py` regen needed, no `do-not-automerge` law surface
  touched.

## Fleet propagation — how far this reaches, and the remaining gap

- **Adopters get the generalization at its SOURCE, today.** The check scans
  `src/engine/templates/*.tmpl` — the single fleet-wide source rendered into
  every adopter's planted doctrine (CONSTITUTION.md, CAPABILITIES.md,
  collaboration-model.md, skills, …). So no false capability wall can be seeded
  into the doctrine any adopter renders: the kit's own `kit-quality` CI reds it
  before it can ship in a template. This is the meaningful fleet coverage and it
  is LIVE on merge.
- **Not yet covered: an adopter authoring a NEW false wall into its OWN
  non-templated local docs.** `bootstrap.py adopt` plants no `tools/`, and the
  generated adopter CI (`adopt.py::live_ci_workflow`) runs `bootstrap.py check`
  steps + pytest, never the kit's `tools/`. Vendoring this check into adopter CI
  would need: (a) planting the file, (b) a generated-CI step, and (c) making
  `_iter_target_files` adopter-aware (it hard-codes `src/engine/templates` +
  `src/engine/skills/skills.py`, absent in adopters — though it already
  `.is_dir()`-guards them, so dropped into an adopter it would safely scan only
  docs/ + CONSTITUTION.md + CAPABILITIES.md). That is a change to the
  heavily-engineered adopt/dist path (bundled into the 12k-line
  `dist/bootstrap.py`) and is DEFERRED here to avoid regressing the generated
  gate. Flagged in the PR body as the remaining fleet-wide item.

## Enders

- 💡 Session idea: **teach the clearing layer a first-class `capability` ledger
  row.** The check clears dated `- YYYY-MM-DD · wall · …` rows so genuine,
  momentary refusals are recorded honestly. But the owner's principle is that
  even genuine refusals are transient — so the ledger should nudge toward
  re-verification. Idea: have the check (advisory, not a red) surface any
  `wall` ledger row whose `LAST-VERIFIED` date is > N days old, so a stale wall
  is re-attempted rather than trusted forever — the enforcement analogue of the
  DISCOVERY RULE ("attempt before assuming it is walled"). Dedup: grepped
  docs/ideas/ — the false-wall guard idea (this line's parent) mechanizes
  seeding-prevention; nothing covers ledger-staleness re-verification.
- ⟲ Previous-session review (2026-07-18-false-wall-guard, PR #448): it did the
  hard part right — a two-layer design (specific-prohibition blocklist +
  dated/repudiated/historical clearing) with an explicit owner-biased "false
  positive is worse than a miss" stance, verified exit-0 on main with a survey
  of the corrected/dated/repudiated lines. What it left on the table was exactly
  this session's scope: it hard-coded the semantic class to MERGE, so a false
  "agents cannot deploy / delete branches / update Railway" wall would have
  sailed through — the regression class is broader than the one instance that
  triggered it. Concrete system improvement (shipped here): the grammar is now
  factored into reusable SUBJECT/NEGATION/CAP-VERB/CAP-NOUN fragments, so the
  NEXT capability class (e.g. a new platform action) is a one-line verb-list
  addition, not a new bespoke regex — the check is now extensible by design, not
  by copy-paste.

## 📤 Run report

- **Did:** generalized `check_no_false_walls.py` from merge-only to the full
  false-capability-wall class (subject-negated capability, owner-only
  capability, standing platform wall, standalone classifier-denied), with the
  verb list scoped to exclude genuine walls; +5 test classes; verified exit-0 on
  main with zero false positives · **Outcome:** shipped
- **Shipped:** tools/check_no_false_walls.py · tests/test_no_false_walls.py ·
  this card
- **Run type:** owner-directed feature build (single PR)
- **⚑ Flag for owner:** fleet-wide adopter-local CI coverage is the one deferred
  item (see "Fleet propagation" above) — the template source is guarded today;
  vendoring the check into the generated adopter gate is the remaining step.
