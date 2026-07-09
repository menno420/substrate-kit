# Session 2026-07-09 — groomed-ideas-1: post-band idea increment

> **Status:** `complete` *(PR #19 — three groomed ideas from recent session
> cards, shipped in one coherent PR; touches none of the open PR #17's files.)*

**What happened (post-band groomed-ideas work, best value/size first):**

1. **PR-diff-aware session-card selection** (💡 from the kl1-ci-delta card,
   shipped): `check --session-log <file>` (`cmd_check`, `src/engine/cli.py`) —
   gate on the named card explicitly; a missing named file counts as an
   *absent* log (advisory by default, hard failure under
   `--require-session-log`), **never a silent fallback** to a different card;
   no argument → newest-by-mtime unchanged (fail-open, backward-compatible).
   The kit's own `ci.yml` session-gate step now derives the card from
   `git diff --name-only <range> -- '.sessions/*.md' ':!.sessions/README.md'`
   (PR base range on pull_request, `event.before..sha` on push) and passes it
   via `--session-log` — **the git-mtime-restore shim is deleted**. The
   planted `substrate-gate.yml` (`live_ci_workflow`, `src/engine/adopt.py`)
   carries the same diff-aware step to every `adopt --wire-enforcement`
   consumer, `sessions_dir`-parameterized — the shim class never travels.
2. **Reflection-miner line-start markers** (KL-5-era observation, shipped):
   `_ref_marker_tags` (`src/engine/loop/reflections.py`) requires 💡/⚑ to
   *lead* the line after list/number/blockquote prefixes
   (`_REF_LEAD_PREFIX_RE`); mid-prose cross-references ("see 💡 below…", "its
   friction-index 💡 … was left floating") stop becoming junk lesson
   candidates; `_ref_clean_line` shares the prefix regex so numbered-list
   prefixes no longer leak into lesson text. Regression:
   `tests/test_reflections.py::test_mine_skips_mid_prose_marker_fragments`.
3. **Guard-recipe convention** (⟲ improvement from the kl1-ci-delta review,
   shipped): friction→guard entries deferred to a later session carry a
   one-line **guard recipe** — function + file + test anchors, not just the
   symptom (KL-1 re-derived `_vendor_bootstrap` / `_ref_mine_log` by grep from
   KL-0's symptom-only notes). Convention text in the kit's
   `.sessions/README.md` **and** the planted `_adopt_sessions_readme` so it
   travels. Deliberately a convention, not a checker (see flag 2).

**B4 ledger exercised for real:** three new `docs/ideas/` entries with
outcome frontmatter (`state: promoted`, `outcome: shipped`, `shipped_pr: 19`,
`shipped_repo: menno420/substrate-kit`, `merged_date: 2026-07-09`; survive
windows close 2026-08-08) + a "Shipped (survive window open)" README section:
`session-gate-diff-aware-selection-2026-07-09.md`,
`reflection-miner-line-start-markers-2026-07-09.md`,
`session-card-guard-recipes-2026-07-09.md`. `check_idea_index` green.

## ⚑ Flags

1. ⚑ Decide-and-flag: the B4 rows are written `shipped` with
   `merged_date: 2026-07-09` **before** the merge lands (the session merges
   its own PR the same day per house rhythm); had the merge slipped a day the
   date would need a one-line fix. Chosen over a post-merge second PR.
2. ⚑ Decide-and-flag: guard recipes ship as **convention only** — a checker
   needle on prose shape would be ceremony (the Q-0089 forced-filler bar);
   revisit only if cards keep shipping symptom-only friction entries.
3. ⚑ Decide-and-flag: diff-awareness lives **workflow-side** (shell `git
   diff`) + an explicit engine flag — NOT in-engine git-tree diffing, which
   would need packfile/delta parsing in stdlib for a merge-base walk; the
   engine keeps its no-subprocess purity, CI shell owns the diff. Fail-open:
   no card in the diff → the argument is omitted → the engine's mtime
   fallback (on main every merged card is complete, so the push leg is safe).
4. ⚑ Precision-over-recall in the miner: `## 💡 Session idea` *headings*
   stay excluded and idea bodies are prose, so pass-1 now fires mostly on
   explicitly marker-led bullet lines — intentional; deliberate `reflect
   --add` remains the high-signal path.

## 💡 Session idea

**Anchor-aware card selection for local `check`:** CI now knows the session's
card from the PR diff, but a *local* `check` still guesses by mtime — while
the engine already records a session-start anchor + a files-touched-since
scan (`src/engine/loop/handoff.py`). Derive the card locally from the
anchor's own `.sessions/` touches (the same evidence the auto-draft uses) so
local and CI selection agree, and the Stop hook's advisories name the right
card in multi-card checkouts. Dedup-checked against `docs/ideas/` (the
diff-aware entry covers CI only). Lands with: a future handoff/loop
increment.

## ⟲ Previous-session review (kl6-unblocked, PR #18)

Strong: built-around-not-waited executed exactly as PL-002 intends — the
blocked KL-6 remainder became a ledger with named unblockers instead of a
stall; the pointer-stubs-carry-frontmatter call (flag 2) closed an exemption
hole rather than opening one; and the `merge=union` gitattribute turned a
guaranteed parallel-session conflict into a non-event. Miss: it shipped B4's
*read* half (checker) while the *write* half stayed an idea — right
sequencing, but its own session idea admits upkeep-by-exhortation is the
known failure mode, so the backfill idea should carry higher priority than
its `lands with: post-P13` suggests. **Workflow improvement:** current-state
▶ Next action is accreting DONE paragraphs (KL-6's, now this session's — the
precedent compounds); adopt the rule that ▶ Next action carries only
*pending* items and a DONE line moves to Recently shipped on the next touch.

## Docs audit

CHANGELOG `[Unreleased]` gained the Added entry (below KL-6's, clear of PR
#17's top-of-section insertion); current-state carries the PR #19 paragraph
in ▶ Next action + the Recently-shipped entry (no touch of the In-flight
bullets or the Stability KL-5 tail — PR #17 rewrites both); ideas README +
three frontmatter entries; both `.sessions/README`s carry the guard-recipe
convention; dist regenerated + byte-pinned; nothing left chat-only.

## KPIs / verification

- `python3.10 -m pytest tests/ -q` → **618 passed** (611 → 618: 4 gate
  selector + 1 miner + 2 adopt tests).
- `python3.10 src/build_bootstrap.py` → fresh build byte-equal to committed
  dist (pin test green in the suite).
- `python3.10 -m ruff check src/engine/` → clean (no print/assert/subprocess).
- `python3.10 dist/bootstrap.py check --strict --require-session-log` → red
  on this born-red card exactly as designed; `--session-log` exercised live
  against a complete card (exit 0) and a missing path (MERGE HELD).
- `python3.10 scripts/check_idea_index.py` → OK ·
  `python3.10 scripts/check_program_law.py` → OK.
- CI diff-selection dry-run: `git diff origin/main...HEAD` picks
  `.sessions/2026-07-09-groomed-ideas-1.md` (README correctly excluded even
  though this PR modifies it).

- **📊 Model:** fable-5 · high · kernel/architecture design
