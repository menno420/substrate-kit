# 2026-07-14 · model-line payload lint (advisory)

> **Status:** `complete`

About to happen (opening declaration): build the `📊 Model:` payload lint from
`docs/ideas/model-line-payload-lint-advisory-2026-07-11.md` (Night-8 triage #3,
measured 4-of-5-card drift) — an advisory-only, never exit-affecting `check`
finding when a completed card's Model line breaks the three-field `·` shape,
carries an exact model-ID token instead of a family-level name, or files an
off-taxonomy effort / task-class segment; shared writer/enforcer constants land
in `engine.grammar` (EAP §6.8 pattern), telemetry consumes the same constants,
dist regenerated.

- **📊 Model:** fable-5 · high · feature build

Run type: worker session (coordinator-dispatched build).

## What shipped (PR #352)

- `src/engine/grammar.py` — new "📊 Model run-report line" section: needle,
  taught byte-form (`MODEL_LINE_TAUGHT_FORMAT`), `MODEL_EFFORT_VALUES`
  (low/medium/high, declared from the measured dataset), the 9 PL-004
  `MODEL_TASK_CLASSES`, the exact-ID detector, the payload parser
  (byte-identical move of `telemetry._parse_model_payload`), and
  `model_line_example()` — ONE grammar home (EAP §6.8).
- `src/engine/loop/telemetry.py` — consumes the grammar objects; body-level
  aliases (never import-as: the dist builder drops intra-package imports)
  keep `TASK_CLASSES` / `_EXACT_MODEL_ID_RE` / `_parse_model_payload` /
  `MODEL_LINE_NEEDLE` stable for existing consumers. Behavior unchanged,
  pinned by the pre-existing telemetry suite + new identity tests.
- `src/engine/checks/check_model_line.py` — the lint: completed cards only
  (`status_in_progress`/`unresolved_fill_count` gate, same machinery as
  `reconcile_model_usage`), code spans/fences stripped, `[[fill:]]` stand-ins
  skipped, last-valid-wins mirroring the harvest exactly; finding kinds
  `model-line-shape` / `model-line-exact-id` / `model-line-effort` /
  `model-line-class`, every message quoting the taught form verbatim.
  Scan bounded to the newest-10 completed cards (`MODEL_LINE_LINT_WINDOW`;
  `window=0` = unbounded measurement lane) — decide-and-flag, rationale
  below. PL-008 header: UNVERIFIED, advisory-only, delete-if-unreliable.
- `src/engine/cli.py` — wired into `cmd_check`'s full lane with the same
  warn-only emit + guard-fire telemetry block as every advisory
  (never exit-affecting, by contract and by test).
- `src/build_bootstrap.py` — module registered after `check_session_log.py`;
  dist regenerated, byte-stable
  (sha256 `096da6ad962b8314db34a59064092233e6b8b4ab98dd446b43d5c9fec1702cc6`
  across a double build).
- `tests/test_check_model_line.py` — 25 tests: the mutation arc
  (malformed→fires / fixed→clean / exact-ID→flagged), grammar identity pins
  (telemetry consumes THE SAME objects), taught-form-in-README writer pin,
  scope discipline (in-progress/drafted/fill/README/code-span/fence never
  fire; last-valid-wins; needle absence is the marker gate's job), window
  bound, input-gating, and the advisory-never-reds-strict end-to-end pin.
- `CHANGELOG.md` entry under `[Unreleased]` ### Added; idea frontmatter
  flipped promoted/shipped (#352, the #349/#351 in-PR flip convention;
  merged_date is the anticipated date).
- Park state: NO auto-merge armed by this session (mechanism note: the
  server-side enabler arms non-draft `claude/*` PRs at open on its own —
  landing on green would be the enabler's doing, as with #349/#351).

## Decide-and-flag

- **Newest-10 window on the check-time scan.** The unbounded measure over
  the kit's own tree found **124 of 178 completed cards drifted (174
  findings)** — surfacing all of it on every `check` run would bury the
  actionable signal in archaeology and burst the guard-fires dedupe scan
  (200-record tail) on every run. The lint's job is friction→guard at
  session velocity (W-10a's evidence was the 5 NEWEST cards), so the shipped
  default judges the newest 10; `window=0` keeps the full measure one call
  away. Reversible: one constant.
- **Effort taxonomy declared as low/medium/high** — no PL-004 surface
  enumerates effort tiers; declared from the measured dataset
  (`telemetry/model-usage.jsonl`: low/medium/high are the only recurring
  values) + the harness's own effort levels. Off-list values nag, never red.
- **Task-class judged by prefix-match** (per the idea file), so decorated
  classes like `docs-only — oracle pin edit` pass; the harvest's own
  exact-membership advisory at close is unchanged.

## Verify

- Baseline at HEAD 727f5db: `python3 -m pytest -q` → `1366 passed in 50.47s`.
- Final: `python3 -m pytest -q` → `1391 passed in 29.06s` (+25, zero failures).
- Mutation arc run END-TO-END via `python3 dist/bootstrap.py check --strict`
  on a scratch tree: (a) `fable-5 · high` (missing field) →
  `[model-line-shape]` naming the line + the taught form, exit 0;
  (b) fixed line → `all checks passed`, zero model-line warnings, exit 0;
  (c) `claude-fable-5-20260714 · high · feature build` →
  `[model-line-exact-id]`, exit 0. Advisory posture proven: exit 0 all three.
- Drift re-measured on this repo: **unbounded 124/178 completed cards fail**
  (98 class / 36 exact-id / 23 shape / 17 effort findings); **shipping
  window: 10 of the newest 10 fail (11 findings)** — spot-checked true
  positives (`Claude 5 family` single-field, `default` effort, `engine-fix`
  class), so the nudge is live from this PR's first run.
- `python3 -m ruff check src/engine/` → All checks passed.
- `python3 dist/bootstrap.py check --strict` on this repo → all checks
  passed + the DESIGNED born-red hold on this very card pre-flip; the 11
  model-line advisories surfaced (never exit-affecting, working as built);
  guard-fires delta (13 records) committed per the ledger convention.
- `python3 scripts/check_idea_index.py` / `check_changelog_structure.py` /
  `check_program_law.py` → all OK.

## Friction → guard candidates

- **`claims-stale` false positive, found live:** `check_claims` dates a work
  claim by the FIRST `YYYY-MM-DD` match in the file
  (`WORK_CLAIM_DATE_RE.search`), so a dated idea-filename in the scope text
  (`…-2026-07-11.md`) shadowed this session's real `· 2026-07-14` date and
  the fresh claim nagged as 3-days-stale. Guard recipe: take the LAST date
  match on the bullet line (or the first date AFTER the backticked token) —
  `src/engine/checks/check_claims.py` line ~251 + a fixture in
  `tests/test_check_claims.py` with a dated filename in the scope text.
  Worked around this session by rewording the claim.

## Enders

💡 **Session idea:** put the taxonomy INSIDE the auto-draft stand-in — the
measured 10-of-10 newest-card drift says the taught form never reaches
writers at write time (they free-text the payload from memory). The KL-5
auto-draft currently writes `[[fill: model]]` stand-ins; make it write the
choices inline instead — `[[fill: model family, e.g. fable-5]]` ·
`[[fill: effort: low|medium|high]]` ·
`[[fill: task-class: docs-only|…|feature build]]` —
rendered from the same `engine.grammar` constants as the lint, so the
writer picks from the taxonomy instead of inventing values and the
writer/enforcer loop closes at the moment of authorship, not at check time.
Dedup-grepped `docs/ideas/` (41 files): `taxonomy-surface-sync-checker` is
TASK_CLASSES⇄ladder⇄README sync, `substrate-kit-auto-drafted-handoff` is
the handoff draft — no overlap with taxonomy-in-the-stand-in.

⟲ **Previous-session review** (Night 9, CHANGELOG `[Unreleased]` structure
checker, PR #351): a model build — design-authority rules (a)–(d) executed
verbatim, the 22-test suite pinned the real CHANGELOG born-green, and the
`HEAVY_STEP_NAMES` pin catching the unlisted CI step was the guard system
working mid-build. Its card even applied MY predecessor's review (the
mechanism-cited park-state line — the self-auditing loop compounding). What
it missed, with irony: its own card's Model line reads `- **📊 Model:**
Claude 5 family` — a single-field payload the telemetry harvest silently
records NOTHING from, on the very session whose sibling backlog item was
this payload lint. Concrete improvement: shipped today — that exact card is
one of the 10/10 the new lint flags, and the shape finding says loudly that
the harvest lost the row. Root-cause follow-up filed as this session's 💡
(taxonomy inside the stand-in).

**Documentation audit:** CHANGELOG entry rides the PR; idea frontmatter
flipped in-PR; grammar/checker/cli all carry provenance headers; the
claims-date false positive is recorded above with a guard recipe; nothing
chat-only remains.
