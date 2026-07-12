# 2026-07-12 — grounded-skills program, slice 1: skill index + boot-set wiring

> **Status:** `complete`

- **📊 Model:** fable-5 · seat-worker · grounded-skills slice 1

## Scope (what is about to happen)

Implementing §7 slice 1 of the grounded-skills program plan
(`docs/planning/2026-07-12-grounded-skills-program.md`, merged PR #263,
squash b820b0f — owner directive 2026-07-12): a generated `docs/SKILLS.md`
skill index rendered FROM the kit's `SKILLS` list (engine-computed table,
one source — plan §2 artifact classification), planted via one `ADOPT_PLAN`
tuple, wired into the boot/orientation set (pointer lines in
`AGENT_ORIENTATION.md.tmpl`, `CONSTITUTION.md.tmpl`, `CLAUDE.md.tmpl` —
the CAPABILITIES.md wiring pattern), with tests for index generation and
adopt-time planting, plus a dist rebuild. Advisory only — no CI enforcement
in this slice. No slice-2 (playbook bodies) or slice-5 (capability refresh)
content.

**Provenance flag:** the coordinator is proceeding on the plan's §8
recommended defaults — Q2=B (advisory-first, grammar checks graduate later)
and Q4=A (the program supersession covers its slices under the 2026-07-11
freeze). Vetoable at the owner's normal window.

Lane claim: `control/claims/claude-grounded-skills-slice1-index.md`
(deleted at close).

## Close-out

Shipped (PR #264, implementation commit 298573b):

- **`skills_index_table()`** (`src/engine/skills/skills.py`) — renders the
  index table FROM `SKILLS` + `skill_capabilities()`, so the planted index
  can never hand-drift from what the kit emits (§2 "render from ONE source").
- **`skills_index` engine context key** — added to `ENGINE_CONTEXT_KEYS`
  and injected unconditionally in `build_context` (`src/engine/render.py`),
  so every render path (adopt / upgrade / `render --live`) fills it; a
  same-named slot would win, per the `kit_version` precedent. Top-level
  import is MODULE_ORDER-safe (`skills/skills.py` precedes `render.py`).
- **`SKILLS-index.md.tmpl`** planted at `docs/SKILLS.md` via one
  `ADOPT_PLAN` tuple (`src/engine/adopt.py`) — hash-recorded like every
  planted doc; upgrade classifies a pre-slice-1 adopter's absent index
  `missing → replanted` (test-proven).
- **Boot-set wiring:** `AGENT_ORIENTATION.md.tmpl` (planted-doc list + a
  "Recurring action?" router line), `CONSTITUTION.md.tmpl` ("Recurring
  actions run through the skill index" working-agreement bullet),
  `CLAUDE.md.tmpl` (orientation routing line, reaching both the staged and
  the opt-in live copy).
- **Tests:** suite 1060 → 1065 (2 index-generation, 1 engine-context
  injection, 1 adopt planting+wiring, 1 upgrade missing→replant; plus the
  ADOPT_PLAN-driven generics now cover the new tuple automatically).
  `dist/bootstrap.py` rebuilt; byte-pin green; `check --strict` green
  except this card's designed born-red hold; `ruff check src/engine/`
  clean.

Accept criteria (§7.1): fresh adopt plants the index ✔ (test); index names
all 7 skills with when-to-use lines ✔ (engine-computed, test); `check
--strict` green ✔; existing adopters receive it at next upgrade as
`missing → replanted` ✔ (test).

**Decide-and-flag calls (plan silent on the detail):**

1. **Index columns = Skill · When to reach for it · Capabilities** — the
   plan's "what it grounds (exact commands/tools)" column is deferred to
   slice 2: today's bodies are short checklists, and a grounds column
   scraped from them would be noise; the description IS the honest
   when-to-use line. Single-source beats a hand-written grounds column.
2. **Injection point = `build_context`** (the single funnel), not
   per-caller `setdefault` like `agreement_home` — `skills_index` needs no
   per-run filesystem knowledge, so the funnel is the drift-proof home.
3. **The kit's own repo gets no hand-written `docs/SKILLS.md`** — the
   guardrail refuses self-adopt, and a hand copy would be exactly the
   hand-drift the index exists to kill; the kit's skill truth stays
   `skills.py`.
4. **Wiring = 3 template pointer lines** — CAPABILITIES' fourth wiring
   place (the session-close skill body) is a skill-body edit = slice 2
   territory, not touched here.
5. **control/status.md untouched** — one-writer rule read conservatively;
   this session's visibility artifacts are the claim, the born-red PR, and
   this card.

## Session enders

💡 **Session idea:** slice 2's accept criterion "each body names only
commands that exist" should ship as a checker, not a review habit: a
grammar-level advisory check that extracts backticked command spans from
rendered skill bodies (and from the future grounds column) and verifies
each names an existing file/subcommand in the target tree — the same
enforce-don't-exhort move as check_setup_script, and it graduates under
Q2=B once proven. Dedup-checked against docs/ideas/ (nearest neighbor is
the adopt-time dead-pointer linter idea from the ORDER 015 card — that one
covers planted-doc path references; this covers skill-body command
groundings).

⟲ **Previous-session review:** the plan session (PR #263) made this slice
near-mechanical — §2's artifact-classification table pre-decided
template-vs-generated-vs-engine-computed with cited precedents
(`agreement_home`, PR #261), so implementation needed zero design churn;
that is what a good plan buys. One improvement: the plan's §7.1 accept
criteria and §2 table disagree slightly on the index's third column ("what
it grounds" vs what slice-1 bodies can honestly ground) — a one-line
"columns are name/when/capabilities until slice 2 upgrades the bodies"
would have removed the only decide-and-flag this slice needed. Workflow
improvement: slice-ordered programs should state per-slice column/format
expectations in the slice row itself, not only in the architecture table.

Documentation audit: `check --strict` green at flip (this card's hold
excepted, by design); durable homes are this card, the engine/template/test
diff, and PR #264's description; no chat-only decisions left unrecorded —
the decide-and-flag list above is the complete set. Claim file deleted this
commit.
