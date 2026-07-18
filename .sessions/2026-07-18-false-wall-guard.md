# 2026-07-18 · false-wall-guard

> **Status:** `complete`

- **📊 Model:** Claude Opus 4.8 · high · feature build
- Scope: mechanize the prevention of the recurring FALSE "agents cannot merge /
  owner is the merge authority / classifier-denied" regression. Three sessions
  have now hand-removed the same false wall from three layers (templates →
  rendered docs → skills); this ships an ENFORCING CI checker so it can never be
  re-seeded onto a forward-binding surface. A checker/test guard is free-to-ship
  doctrine (friction → guard: checker/CI/test rung).
- ⚑ Self-initiated: no — owner-directed task (the prompt IS the order). Merge is
  the review; PR opened READY, lands on green `kit-quality`.

## Record

- New checker `tools/check_no_false_walls.py` (stdlib-only, Python 3.10, uses
  print, never vendored into dist). Scans ONLY forward-binding surfaces —
  `src/engine/templates/**/*.tmpl`, `src/engine/skills/skills.py`,
  `docs/**/*.md` (minus historical dirs `docs/retro|planning|audits`, the gen2
  queue/proposal records, `CHANGELOG*`, and any ISO-dated report basename),
  root `CONSTITUTION.md`, and `docs/CAPABILITIES.md`. Fails (exit 1, file:line +
  matched phrase) on a curated blocklist of SPECIFIC false standing
  prohibitions; the corrected/dated/repudiated phrasings PASS.
- Two-layer design (owner bias: a false positive that reds CI is worse than a
  rare miss). Layer A = the blocklist (matches the PROHIBITION, never bare
  "merge"/"wall"/"owner"). Layer B = clearing: a candidate passes if the line is
  a dated ledger record (`- YYYY-MM-DD · …`, `LAST-VERIFIED`, `SUPERSEDED`, or
  a bullet-block continuation), carries a repudiation cue ("no standing", "NOT a
  wall", "do not invent one", "never route a mergeable green PR to the owner",
  "normal agent action", "works agent-side", "land your own", "the old …", a
  `FALSE "…"` quote), or sits under an `## Append log` / `## Historical` heading.
  `owner-gated PR` and the `Merge Without Review`/`Self-Approval` refusal-labels
  only fire when a same-line standing-directive/prohibition frame is present, so
  their adjective/quotation uses don't trip.
- Verified on current `main`: exit 0, ZERO false positives (the corrected merge
  doctrine in CONSTITUTION.md.tmpl / CAPABILITIES.md.tmpl / current-state.md,
  the dated CAPABILITIES.md wall ledger, and the NEXT-TASKS.md `FALSE "…"` flag
  all pass). Catches the synthetic re-seed
  `agents do NOT arm auto-merge — classifier-denied since 2026-07-15` (exit 1).
- Test `tests/test_no_false_walls.py` (12 cases): current-tree exit-0, synthetic
  bad-string caught (+ four more blocklist spreads), all corrected variants
  pass, and the exclusion paths (dated ledger, dated filename, historical
  heading, `FALSE "…"` quote, historical dir) verified.
- Wired into CI as a real gate: a lane-conditioned step in the `kit-quality`
  job (`.github/workflows/ci.yml`), registered in the `test_ci_control_lane`
  heavy-step pin so the control fast-lane invariant stays honest.
- No template touched → no dist regen needed; `python3 src/build_bootstrap.py`
  leaves `dist/bootstrap.py` byte-identical (verified).
- Verify: `python3 -m pytest tests/ -q` → 1738 passed, 1 skipped;
  `python3 tools/check_no_false_walls.py` → exit 0.

## 💡 Session idea

**Generalize `check_no_false_walls` into a config-driven "stale-doctrine
guard".** The recurring failure class isn't unique to the merge wall — any
doctrine the owner corrects (a retired gate, a superseded autonomy rail) risks
being re-seeded onto a forward-binding surface by a session reading an older
layer. The blocklist + repudiation-cue + dated-record-clearing engine here is
reusable: lift the patterns into a `substrate.config.json` `stale_doctrine`
list ({name, blocklist_regex[], clear_cue[]}) so a new correction ships its own
one-line guard entry instead of a new script. Dedup: grepped `docs/ideas/` —
the closest entries are the taxonomy-sync and template-pointer guards (both
consistency checks between surfaces), none covers repudiation-aware
false-assertion detection. Worth having: it converts "hand-remove the same
regression N times" into "add one config row once."

## ⟲ Previous-session review

Reviewing `2026-07-15-adopter-currency-websites-v1170` (PR #389): a clean,
well-scoped self-initiated currency slice — ladder discipline was explicit,
the claim-format advisory was fixed in-band, and its 💡 (`currency --check`)
correctly identified that a hand-eyeballed registry-delta scan goes stale
within the hour. What it could have done better is exactly what this session
acts on at the doctrine layer: that card noted a recurring manual re-derivation
(the adopter self-report spot-check) but left it as a *proposed* idea rather
than a shipped guard. The system-level improvement this surfaces:
**"recurring manual re-derivation" is itself a friction→guard trigger** — when
two consecutive sessions re-do the same by-hand check (currency staleness
there, false-wall removal here), the second occurrence should mechanize it, not
re-note it. This session applies that to the merge-wall regression; the currency
idea is still owed its checker.
