# Session 2026-07-10 — EAP §6.3: kit-upgrade currency checker + generated docs/adopters.md

> **Status:** `complete`

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

## Close-out

**Shipped (session PR #133; claim fast-lane PR #132 → 2c77011):** everything
in the plan above, as planned. `python3 -m pytest tests/ -q` → **852 passed**
(823 on main → +29 new); `python3 -m ruff check src/engine/` clean; dist
rebuilt, byte-pin clean; `check --strict` green except this card's own
born-red hold (this flip clears it — the mid-flight red the coordinator
flagged at cadd0dc was exactly that hold + the two legacy-alias jobs
mirroring it, verified in the job log: the only finding was
`badge still says in-progress`).

**Live fleet scan (the §6.3 payoff, committed in `docs/adopters.md`):**
spread v1.0.0→v1.7.0 across 9 scanned adopters + kit; NOBODY runs v1.7.0
except kit-lab's own dist; one DRIFT row — **the kit repo itself**
(vendored dist v1.7.0 vs its own `substrate.config.json` pin v1.0.0,
tree-internal). trading-strategy turned out ADOPTED at v1.1.0 (the old
hand-written ledger still said "not yet created/adopted" — the exact drift
class this slice retires). pokemon-mod-lab: no kit artifact (not adopted).
superbot: config pin v1.0.0 only, no vendored dist found, no heartbeat.

**Decided-and-flagged:** (1) execution-home split — generation agent-side,
CI format-gate only (no network); (2) tree-truth order: vendored header >
config pin, both shown; (3) kit's own pin-v1.0.0 DRIFT left in place
pending the owner's §7 version-truth layering ruling (generated adopters.md
is the single home; other homes should defer); (4) roster + per-lane
heartbeats as data in `docs/fleet-repos.txt`, not code; (5) the format gate
engages on any existing `docs/adopters.md` (a hand-written one now reds —
that is the migration, and adopter repos don't carry the file).

**💡 Session idea:** the currency scan and the release train should meet —
`build_release_json.py` could embed the freshest adopters.md spread into
each release's notes ("who this release leaves behind: N repos ≥2 versions
back"), turning every release into an automatic upgrade-nudge broadcast
with zero new access. Cheap: both halves already exist in-tree.

**⟲ Previous-session review:** the §6.1 lane (#129/#130/#131) was clean and
its close-out heartbeat's "next: §6.3 UNCLAIMED" line made this session's
pickup unambiguous — the queued-slice convention works. One improvement it
surfaces: its status recorded the fleet's version facts only as prose relayed
from memory (superbot "7 releases behind") with no evidence date — exactly
the class this slice mechanized; nothing further to fix there beyond what
§6.3 just shipped.
