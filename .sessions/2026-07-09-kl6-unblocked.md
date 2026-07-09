# Session 2026-07-09 — KL-6 (unblocked half): B4 ideas-frontmatter + console-feed groundwork

> **Status:** `complete` *(PR #18 — the KL-6 pieces not blocked on PR #17's
> owner blessing or on 👤 P5/P11/P13; the blocked remainder is ledgered in
> current-state ▶ Next action.)*

**What happened (founding plan §10 KL-6 row, the unblocked subset; §5.4/§7.2/§7.3):**

- **The B4 ideas-frontmatter convention + `scripts/check_idea_index.py`**
  (same PR per §5.4 — a convention ships with its checker): every
  `docs/ideas/` entry opens with the flat YAML-subset block `{state, origin,
  shipped_pr, shipped_repo, merged_date, outcome}`. The checker (stdlib,
  `check_program_law` house pattern, 23 tests) enforces the grammar, the
  outcome-consistency rules (ship outcomes require all three ship fields;
  `open`/`rejected` require them null; `survived` needs the 30-day D-15
  window), the `-YYYY-MM-DD.md` cohort-key filename (B4 scores by
  generation-month cohort), and README index consistency (every file linked,
  every relative link resolving). Wired into kit-quality — the CI step is
  placed *before* the Program-law step so it merges cleanly around PR #17's
  bench-integrity step (inserted *after* it).
- **Migration**: the three existing entries carry frontmatter — and the
  auto-drafted-handoff stub records the register's **first real B4 `shipped`
  outcome** (kit PR #16, merged 2026-07-09; survive window closes
  2026-08-08). The README gains the convention section + a
  "Historical / pointer stubs" index so the two stubs are indexed.
- **Planted template**: `ideas-README.md.tmpl` documents the convention for
  consumers (stdlib-friendly flat subset by design — no YAML dep, engine
  untouched); dist regenerated + byte-pinned.
- **`telemetry/*.jsonl merge=union` gitattribute** (friction → guard): this
  session and PR #17 both append one row after the same EOF line — a
  guaranteed textual conflict on an append-only feed. Union merge keeps both
  rows; applied only to the append-only JSONL, never to prose.
- **👤 P5/P6 documented in current-state**: exact owner steps for the
  Railway project `kit-lab` (P5) and the console-move picture (P6) —
  including the reality update that the **websites repo** (menno420/websites
  PRs #7/#8) now serves botsite/dashboard/console rendering from superbot's
  committed feeds, which postdates the plan's console picture. No Railway
  touched (ambient IDs may point at production).
- **Companion superbot PR #1883**: exporter `telemetry` family (reads
  `telemetry/model-usage.jsonl`, field-whitelisted; superbot's feed seeded
  hand-authored per §4.2) rendered real on the console's telemetry lane, plus
  the new declared lane **"Kit lab — benchmarks & guards"** carrying the
  §7.3 contract `bench/results/*/index.json → [{date, kit_version, family,
  verdict, headline}]` — declared, not faked (the kit's results indexes ride
  the open #17).
- **Verified:** 611/611 pytest (588 → 611) · ruff engine bans green ·
  fresh-dist byte-equal · `check_idea_index` OK · `check_program_law` OK ·
  `check --strict --require-session-log` green at flip.

## ⚑ Flags

1. ⚑ Decide-and-flag: the KL-6 remainder is **built-around, not waited-on**
   (PL-002 never-wait): kit-lab lane real data blocked on #17's blessing +
   👤 P11/P13; B2/B3/B4 sweeps blocked on 👤 P13; console move blocked on
   👤 P5 — each ledgered in current-state ▶ Next action with its unblocker.
2. ⚑ Decide-and-flag: **pointer stubs carry frontmatter too** (state
   `historical`) rather than a checker exemption — an exemption class would
   be a hole B4 rows could silently fall through. The multi-repo capture
   stays `open` (it spans the unbuilt trading repo; not one shippable unit).
3. ⚑ Conflict-avoidance vs the blessing-gated #17: this card's PR does NOT
   edit current-state's "In flight" bullets or the Stability-baseline KL-5
   tail (#17 rewrites both); KL-6 status lives in ▶ Next action instead. The
   CHANGELOG entry is inserted below the auto-draft entry, clear of #17's
   top-of-section insertion. Remaining known overlap: none textual; the
   telemetry JSONL append is covered by the new union attribute.
4. ⚑ The `📊 Model:` task_class files as `kernel/architecture design` —
   band precedent (KL-3/4/5 filed the same); the mislabel is the known
   `feature build` taxonomy gap, routed discuss-first
   (`docs/ideas/feature-build-task-class-2026-07-09.md`).

## 💡 Session idea

**Auto-backfill idea outcomes at merge (B4's write half, mechanized):**
extend the kit's session-close/loop sweep to detect an idea reference in a
merged PR (the §9.3 `kit-idea:` marker, or a `docs/ideas/<file>` link in the
PR body) and flip that idea's frontmatter `outcome → shipped` with
`shipped_pr`/`shipped_repo`/`merged_date` filled — then flip
`shipped → survived` automatically when the 30-day revert-scan comes back
clean. Exactly the auto-draft lesson applied to B4: the convention now
exists, but its upkeep is exhortation until the write half is mechanized.
Dedup-checked against `docs/ideas/` (nothing covers outcome write-back);
lands with: the B2/B3/B4 sweep build (post-P13).

## ⟲ Previous-session review (kl5-auto-draft, PR #16)

Strong: it shipped the full mechanization *and* verified it live end-to-end
on a scratch adopt (sessionstart → draft → gate red → flip → harvest) — the
Phase-2.5 lesson executed, not just cited; and its flag-3 friction→guard fix
(code-span stripping in the slot counter, with a regression test) is the
doctrine working mid-session. Miss: it left the two pointer-stub idea files
unindexed (the README backlog listed only one of three entries) — exactly
the drift class this session's `check_idea_index` now reds, which is also
the honest answer to "what one change would have helped": a convention
without its checker decays silently (§5.4 was right to demand same-PR).
**Workflow improvement adopted:** its "a 💡 names its landing band" rule is
followed above (`lands with:` line).

## Docs audit

`check --strict --require-session-log` green at flip; CHANGELOG
`[Unreleased]` gained the Added entry; current-state carries the 👤 P5/P6
section, the KL-6 done/blocked ledger in ▶ Next action, and the #18
recently-shipped entry; ideas README + planted template carry the
convention; telemetry row appended (union-merged from now on); nothing left
chat-only. Superbot side: PR #1883 carries its own card/claim per that
repo's conventions.

- **📊 Model:** fable-5 · high · kernel/architecture design
