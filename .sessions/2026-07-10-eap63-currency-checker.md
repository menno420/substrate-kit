# Session 2026-07-10 — EAP §6.3: kit-upgrade currency checker + generated docs/adopters.md

> **Status:** `in-progress`

- **📊 Model:** claude-fable-5 · medium · engine+tests+live-fleet-scan

**Scope (as declared, born-red):** the coordinator's program-review §6.3 slice
(spec: menno420/superbot `docs/eap/eap-program-review-2026-07-10.md` §6 item 3;
claim `claimed-by: eap-review-6.3 kit-eap63-lane 2026-07-10T18:22Z`, fast-lane
PR #132 → squash 2c77011, landed before this build work per the ORDER 007
ritual). Nothing owns the fleet's kit-version spread today; this slice makes
`docs/adopters.md` a GENERATED artifact fed by tree truth.

Plan:

1. **`src/engine/currency.py`** — fleet kit-currency scanner: per repo, read
   the ACTUAL committed tree (vendored `bootstrap.py` header = primary truth,
   `substrate.config.json` `kit_version` pin = secondary) AND the `kit:`
   self-report line from the configured heartbeat file(s). Tree vs self-report
   disagreement = a DRIFT row, surfaced loudly, never silently resolved. Fetch
   behind an injectable-fetcher seam (default: stdlib urllib →
   raw.githubusercontent.com); all parse/drift/render logic unit-testable with
   no network.
2. **`bootstrap currency` subcommand** — agent-side runnable: fetches live,
   regenerates `docs/adopters.md` (GENERATED marker + provenance preamble
   kept), prints the drift report. **Execution-home split (flagged):** kit CI
   cannot auth to sibling repos, so generation is agent-side only; the CI-side
   check validates ONLY format + staleness of the committed file, no network.
3. **`src/engine/checks/check_adopters_current.py`** — the CI-side gate,
   wired into `_extra_check_findings` like the existing checkers; engages only
   when `docs/adopters.md` exists; static format findings ride the strict
   loop, wall-clock staleness stays advisory-only (the check_status_current
   doctrine: a required check never reds on time alone).
4. Fleet roster as data: `docs/fleet-repos.txt` (one `owner/repo` per line).
5. Tests (version parsing · drift detection · table generation ·
   not-adopted/unknown handling · format check), CHANGELOG, dist rebuild
   (byte-pin), live fleet scan committed in this PR.

NOT in this slice: any write outside this repo; resolving the drifts found
(they are surfaced for the manager/owner); the §7 version-truth layering
ruling (deference note goes in the close-out heartbeat).
