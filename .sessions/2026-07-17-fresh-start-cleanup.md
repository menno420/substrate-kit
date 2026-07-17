# Session · 2026-07-17 · fresh-start-cleanup

> **Status:** `complete`

Owner-authorized fresh-start cleanup ahead of the 2026-07-21 EAP read-only
cutover and the Projects recreation. Surgical docs + template pass; no
runtime/engine code deleted; workflow files, `dist/` payload logic and
`src/engine/` code left intact.

- **📊 Model:** opus-4.8 · high · docs-only
- ⚑ Self-initiated: no — owner-authorized cleanup task.

## What shipped (PR #TBD)

1. **Merge-doctrine template fix (highest leverage — propagates fleet-wide).**
   `src/engine/templates/CONSTITUTION.md.tmpl` autonomy-rail item 3 no longer
   tells agents to "arm auto-merge while checks pend → it lands itself → re-arm".
   New doctrine: *open PRs READY and let the server-side merge-on-green workflow
   land them; agents do NOT ready-flip, arm auto-merge, or REST/MCP-merge their
   own OR a sibling's PR (classifier-denied since 2026-07-15)*. All PL-012 rider
   pins preserved (`tests/test_rider_graduation.py` green, 36 tests). Regenerated
   `dist/bootstrap.py` (byte-pin holds; only the doctrine line changed).
2. **`docs/current-state.md`** — added a top "Fresh-start reconciliation
   (2026-07-17)" block (EAP cutover 2026-07-21 · classifier freeze · v1.18.0
   released+verified but NOT distributed · autonomy wind-down · recreation);
   corrected the false "distribution COMPLETE — all 9 adopters current" line;
   corrected § Review rhythm to the classifier-aware merge doctrine.
3. **`docs/NEXT-TASKS.md`** (new) — #1 distribute v1.18.0 to the ~15 adopters
   (per-adopter `bootstrap.py upgrade` + pin bump, one PR per adopter in its own
   session); #2 merge-doctrine template propagation; + self-pin drift, ledger
   reconcile, veto-menu curation, grounded-skills.
4. **`docs/CAPABILITIES.md`** — folded #433's sibling-PR-merge wall append
   verbatim + a 2026-07-17 classifier-freeze entry. #433 is superseded by this
   PR (its card / claim / status-heartbeat edits were session-local; only the
   CAPABILITIES append had durable value).

Claims dir on `main` was clean (README only); no stale claims to prune.

## 💡 Session idea

An `adopters-staleness self-signal` check: `currency` already knows the kit
release and each adopter's pinned version — have it emit an explicit
`⚠️ N adopters below current release, wave NOT run` line whenever any tree
lags the registry, so a "registry says v1.18.0" reading can never again be
mistaken for "distribution complete" (the exact drift this cleanup corrected).
Routed to NEXT-TASKS §5 / the veto menu.

## ⟲ Previous-session review

The 2026-07-16 sessions (#431/#433 + the release-v1.18.0 close-outs) did the
release + registry regen correctly but left two PRs frozen by the classifier
(a draft that never got readied, a born-red card never flipped) and never
propagated the true distribution gap into `current-state.md` — which kept
asserting "distribution COMPLETE" nine days stale. **System improvement:**
the frozen-PR class is a doctrine bug, not a per-session slip — sessions were
still following templates that told them to self-arm/flip. Fixing the source
template (done this session) is the durable guard; the follow-on is the
staleness self-signal above so the ledger can't silently lie about the wave.
