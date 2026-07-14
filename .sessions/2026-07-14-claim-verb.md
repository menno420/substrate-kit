# 2026-07-14 — `bootstrap claim` verb (mechanical grammar-valid claim writer)

> **Status:** `in-progress`

About to (opening declaration): build the #358 card's 💡 ender — a
`bootstrap claim` verb that writes/deletes one-file-per-claim work claims
mechanically from the SAME grammar constants `check_claims` consumes
(`engine.grammar` WORK_CLAIM_BULLET_RE / WORK_CLAIM_DATE_RE), mirroring the
heartbeat verb's structure (write-by-default + `--dry-run`, refuse-and-name
errors, write → parse round-trip); plus two ride-alongs: restamp
control/status.md (#358 is MERGED, not parked) and a drift-pin test tying
cut_release.py's FOLLOWUP_CHECKLIST keywords to the release runbook.

- **📊 Model:** fable-5 · high · feature build

Run type: worker session (coordinator-dispatched).

## What shipped (PR #359)

- `src/engine/claim.py` — the writer's pure logic: `branch_for(slug)` →
  `claude/<slug>`, `claim_filename(slug)` → `claude-<slug>.md`,
  `render_claim(slug, scope, area=None)` (backticked branch token · bold
  scope · optional area · current-UTC date LAST on the bullet — the
  post-#353 rule mechanized), `owner_token(text)` (the ownership probe),
  every render round-trip verified against WORK_CLAIM_BULLET_RE /
  WORK_CLAIM_DATE_RE before it leaves (the heartbeat verb's
  write → parse → equal recipe). Grammar-breaking inputs refuse loudly:
  backticks in scope/area (the enforcer regex keys the duplicate scan on
  the LAST backticked token, so a scope backtick would shadow the branch),
  newlines, non-filename-safe slugs.
- `cli.py` — the verb: `bootstrap claim <slug> --scope "<scope>"
  [--area "<files/area>"] [--dry-run | --delete]`. Honors the existing
  `substrate.config.json` → `claims_dir` pin; control-bus gate like the
  heartbeat verb; rc 2 refusals name the fix.
- **Decide-and-flag (dry-run convention):** write-by-default + `--dry-run`,
  exactly the #346 heartbeat verb's convention — not a `--write` opt-in
  (cut_release's convention); the sibling status-file writer is the closer
  precedent.
- **Decide-and-flag (claims_dir):** reused the existing config key
  (`engine.lib.config.DEFAULT_CLAIMS_DIR` / `config.claims_dir`, already
  consumed by check_claims) — no new config surface needed.
- **Decide-and-flag (foreign-claim ownership):** ownership = the existing
  file's bullet token equals this invocation's derived branch
  (`claude/<slug>`) — the SAME token the duplicate scan keys on, so "who
  owns the file" and "who holds the claim" can never disagree. Mismatch OR
  an unparseable existing file (ownership unprovable) → both `--delete` and
  write-over refuse, file left intact. Same-token overwrite is allowed as a
  refresh (the token is the identity, not the writing process).
- `tests/test_claim.py` — 18 tests: round-trip (verb-written claim passes
  check_claims with ZERO findings, including the #353 case of a dated
  filename `2026-07-01-foo.md` in the scope), delete path, foreign-claim
  refusals (delete + write-over, file intact byte-for-byte), dry-run
  touches nothing, grammar-breaker refusals, control-bus gate.
- **Ride-along (drift pin):** `tests/test_cut_release.py`
  `TestFollowupChecklistRunbookPin::test_followup_checklist_keywords_pinned_to_runbook`
  — cut_release.py's FOLLOWUP_CHECKLIST embeds runbook prose with no drift
  protection; the pin asserts each checklist step's key noun/verb phrases
  appear in BOTH the checklist and docs/operations/release-runbook.md
  (loose case-insensitive presence, NOT byte equality — wording tweaks stay
  free, concept removals/renames fail loudly and name both homes).
- **Ride-along (heartbeat):** control/status.md restamped — #358 was
  MERGED 2026-07-14T03:18Z (squash e564b2d), not "open, parked green";
  moved to Recently merged, this session's outcome line added.
- README discoverability: `control-claims-README.md.tmpl` + the planted
  copy now name the verb in steps 2/4 (write + delete) instead of teaching
  hand-writing only.
- Dist regenerated via `src/build_bootstrap.py` (engine + template payload
  changed), byte-stable across two consecutive builds; `claim.py` added to
  MODULE_ORDER beside its sibling writer heartbeat.py;
  `_verify_claim_roundtrip` named to clear the cross-module top-level
  collision guard (heartbeat.py owns `_verify_roundtrip`).

## Verify

- Baseline at HEAD e564b2d (#358): `1476 passed, 1 skipped`. Final:
  `python3 -m pytest tests/ -q` → `1495 passed, 1 skipped` (+19: 18 claim
  tests + 1 drift pin; zero failures).
- `python3 scripts/preflight.py` → `preflight: OK — 7 leg(s) green`.
- `python3 dist/bootstrap.py check --strict` → the only hold is the
  DESIGNED born-red gate on this card (pre-existing model-line advisories
  on earlier July-14 cards unchanged); claims scan: zero findings.
- DOGFOOD: this session's own claim was deleted and recreated by the verb
  itself (`bootstrap claim claim-verb --delete` on the hand-written one,
  then `bootstrap claim claim-verb --scope "..." --area "..."`) —
  check_claims zero findings on the verb-written file.

## Enders

💡 **Session idea:** a `bootstrap card` verb — mechanical born-red
session-card OPENER (`bootstrap card <slug> --about "..." --model
"fable-5 · high · feature build"`) that renders the card skeleton with a
grammar-valid `📊 Model:` payload validated against check_model_line's
taxonomy at write time. Evidence from this session: `check --strict`
surfaced FIVE model-line advisories on 2026-07-14 cards alone (bad effort
segment, free-text task classes, one- and zero-separator payloads) — every
one a hand-written opening card, every one silently dropped from the PL-004
telemetry harvest. Distinct from the existing `draft` verb (KL-5), which
drafts the CLOSE-OUT from evidence at session end; nothing mechanizes the
opening card, which is where the payload goes wrong. Third rung of the
mechanical-writer ladder: heartbeat (#346) → claim (this PR) → card.
Dedup: grepped `docs/ideas/` — no card-writer/opener idea exists.

⟲ **Previous-session review** (Night 16 / PR #358, git-truth helper): the
decide-and-flag discipline was the standout — the rc-1/rc-128 × shallow
verdict table was stated precisely enough to re-check without rerunning it,
and the 💡 ender again named exact regexes, the evidence (its own live
claims-format fire), and the sibling precedent (heartbeat verb), letting
this session start near-mechanically; the self-audit that demoted the
"three claimed sites" to two real ones is the verify-don't-trust posture
working. The miss: after hand-fixing its own claims-format finding, it left
`control/claims/README.md` still teaching hand-writing as the only path —
the friction was filed as an idea but the point-of-need doc kept
manufacturing the same friction for the interim window. Concrete workflow
improvement: when friction produces a "mechanical writer" idea, the same
session leaves a one-line pointer at the point-of-need doc (even just
"writer coming — grammar lives in grammar.py") so the gap between idea and
build stops reproducing the failure; this session closed that specific gap
in both the template and the planted copy.
