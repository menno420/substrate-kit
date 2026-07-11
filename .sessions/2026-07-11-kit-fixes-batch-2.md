# 2026-07-11 — Queued kit fixes batch 2 (items 1–5)

> **Status:** `complete`

## What is about to happen

Coordinator-assigned dev slice (not an inbox order): five fixes from the
QUEUED KIT FIXES list in control/status.md (2026-07-11 list, items 1–5),
each with a regression test where testable + CHANGELOG `[Unreleased]`
entries. NO release cut this session.

1. **Gate added-card grammar lint** (venture-lab #15 false-green class) — the
   advisory sentinel path stops exempting an ADDED card's grammar entirely;
   design per the idea on venture-lab #17's session card.
2. **build_bootstrap.py byte-count print** — prints the char count, file is
   UTF-8; report the real written byte count.
3. **automerge.required_context validation at plant time** (websites
   "quality" class) — decide-and-flag.
4. **Born-red designed-hold signal** (PL-006 observer-noise class) —
   decide-and-flag.
5. **Grep-pollution mechanical plant** (run-5 judge limitation 5; the
   mechanical half queued by #165) — decide-and-flag on the exact mechanism;
   merge-not-clobber into existing adopter files.

Claim: `control/claims/kit-fixes-batch-2.md` (PR #167, fast lane, armed).

## What happened (close-out)

All five shipped whole, none re-queued. Build commit b5a8802 on PR #168
(claim #167 squash bd6684a on main before build; branch rebased onto it
before the PR opened). Tests 947 → 971 (24 new). Dist regenerated —
644453 bytes, and from this slice the printed count IS the byte count.

1. **Added-card grammar lint** — new `check --added-card <card>` flag +
   `check_added_card()` (src/engine/checks/check_session_log.py); the
   generated gate's advisory lane (src/engine/adopt.py `live_ci_workflow`)
   now passes the added card alongside the absent sentinel. Tiering by the
   card's DECLARED status: no Status badge at all → grammar red (born-red
   exempts the badge's VALUE, never its presence); in-progress/drafted →
   fully exempt (born-red flow untouched); complete & co. → the full
   `check_log` completeness check. Findings are `session-card-grammar`,
   strict-loop, never allowlistable. The exact venture-lab #15 shape
   (complete-declaring card with `## Session idea`/`## Model` headings but
   no 💡/📊 needles) now exits 1 at the door — verified live in a scratch
   adopter.
2. **Byte-count print** — `src/build_bootstrap.py main()` writes the UTF-8
   encoding and prints `len(data)`. Ground truth re-measured: origin/main
   dist was 628829 bytes / 625817 chars — the old print (and status prose
   quoting it, incl. #165's "625817 B") reported chars. Regression test pins
   printed count == `stat().st_size` and pins the artifact as genuinely
   multi-byte.
3. **required_context validation** — `_workflow_context_names()` +
   `_required_context_advisory()` (src/engine/adopt.py): at adopt/upgrade,
   the configured context is checked against the job ids + display names
   the repo's own workflows produce; mismatch → one advisory report line
   naming the `substrate.config.json → automerge."required_context"`
   override; the repo-settings checklist documents the same override.
4. **Designed-hold signal** — cmd_check (src/engine/cli.py): when the ONLY
   strict red is a card that itself declares in-progress, emit
   `check: HOLD (by design) … not a defect; nothing to investigate` plus a
   `::notice title=HOLD: session card in-progress (by design)` annotation
   under GITHUB_ACTIONS. Fired live on this PR's own born-red run.
5. **Search-hygiene plant** — `_plant_search_hygiene()` (src/engine/adopt.py)
   plants root-anchored `.ignore` (`/bootstrap.py`, `/.substrate/backup/`)
   and `.gitattributes` (`linguist-generated=true` for both) on every
   adopt/upgrade pass: append-only merge under one provenance marker,
   idempotent, host content byte-for-byte preserved; unreadable file →
   skip + report. Verified live: rg stops seeing bootstrap.py by default,
   `rg --no-ignore` still reaches it.

Preflight deviation record: ORDER 012 (P3, model-attribution, fm relay via
kit #166 @ b58e740) landed mid-preflight — observed and deliberately NOT
executed by this slice (its `executor:` field names the lane coordinator's
next fired session); routed on the status orders line with a CHECK-first
note (the 📊 Model card convention likely already satisfies its item 1).

## ⚑ Flags (decide-and-flag calls)

- Fix 1 design: declared-status tiering instead of the idea's
  "present-section" heuristic — a heading-matching lint would be fuzzy and
  false-positive-prone; the #15 card declared `complete`, so judging
  declared-complete cards as complete catches the class mechanically while
  leaving born-red truly exempt. The one new birth requirement: a Status
  badge must exist from the first commit (already the convention).
- Fix 3 design: VALIDATE, don't derive — the required check lives in the
  branch ruleset (owner-UI, invisible in-tree), so deriving it would be a
  guess; the advisory names the exact config override instead. Knob stays
  informational-only. websites repo itself untouched (their lane applies
  the one-line config edit; the advisory will name it on their next
  upgrade).
- Fix 4 design: banner only when the in-progress hold is the SOLE finding —
  a partially-real failure must never be labelled "by design". `::notice`
  (not `::error`) because the annotation is information, not a new failure.
- Fix 5 design: `.ignore` includes the vendored bootstrap.py itself —
  sessions search for their repo's code, not the ~12k-line vendored dist;
  `rg --no-ignore`/`-u` and direct reads still reach it, and the planted
  CLAUDE.md note (shipped #165) teaches that. Plain `grep -r` has no ignore
  protocol — guidance-only there, stated honestly in the CHANGELOG.
- Self-initiated correction: status prose had been quoting the builder's
  chars-as-bytes print as real byte sizes; the close-out heartbeat states
  the re-measured ground truth.

## 💡 Session idea

💡 A `check` **merged-card drift advisory**: scan the N newest COMMITTED
session cards for grammar misses (advisory-only, like the claims nags).
The venture-lab #15 card sat red-ing bare `check --strict` for a full
upgrade cycle because every gate judges only the PR in flight — nothing
ever re-scans merged history. Fix 1 closes the door for NEW cards; the
advisory would surface any already-merged drift the day it lands instead
of at the next upgrade wave (dedup: distinct from the newest-by-mtime
fallback, which only ever reads one card).

## ⟲ Previous-session review

⟲ previous-session review: the SessionStart handoff-push session
(#164/#165) was exemplary in mechanism-vs-claim honesty (shipped the push,
refused to claim it works before run-6), and its status close-out queued
this slice cleanly enough that zero re-derivation was needed — the QUEUED
KIT FIXES list with per-item provenance is what made a five-fix slice
startable in minutes. One genuine improvement it surfaces: it recorded
"dist regenerated (625817 B)" by quoting the builder's print — which fix 2
now proves was a CHARS count. The lesson, root-caused: numbers quoted into
durable records should come from the measuring tool (`wc -c`), not a
convenience print; fix 2 makes the print itself trustworthy.

- **📊 Model:** claude-fable-5 · kit-dev lane · queued-fixes batch slice
