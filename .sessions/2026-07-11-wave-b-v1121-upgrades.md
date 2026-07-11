# 2026-07-11 — Wave B: v1.12.1 distribution to the last four adopters

> **Status:** `complete`

- **📊 Model:** fable-5 · medium · distribution-wave

## Scope (what is about to happen)

Wave B: distribute kit v1.12.1 to the last four adopters in registry order.

Registry order (docs/adopters.md, 9 adopters at v1.12.0; superbot excluded —
owner-held pin-only row): Wave A = first five, Wave B = LAST FOUR:
**gba-homebrew · pokemon-mod-lab · venture-lab · fleet-manager**.
Recipe per docs/operations/release-runbook.md §6 + the wave records' shape
(kit-upgrade-distribution-gotchas): stage the three-way-verified v1.12.1
asset (sha256 1055ca2cfd32a83e3dab7a978b05fbec2a82932a3375de0b1034f2519c16e4aa,
704108 B, tag v1.12.1 → 203bb09, run 29170017074) as `bootstrap.py.new` +
`release.json` in each adopter root → `python3 bootstrap.py.new upgrade` →
`check --strict` → born-red card PR per adopter, merged on green.

Kit-side this PR touches ONLY this card + the wave-B claim file
(`control/claims/claude-wave-b-v1121.md`). NO engine/dist/src changes; NEVER
`control/inbox.md` or `bench/`; adopters regen (currency) belongs to the
wave close-out slice, not this card's first commit.

## Close-out

All four wave-B adopters upgraded to v1.12.1 and MERGED. Per-repo outcomes:

- **gba-homebrew** — PR #59, MERGE-COMMIT `d1ec24f083fdb6758be16e504aab570680db9412`; designed-red gate run 29170478652; final-head green runs 29170527349 (substrate-gate) + 29170527350 (ROM builds); banked bootstrap-1.12.0.py (sha256 77c00b81…e1f8); carve-out scan 0 found; `check --strict` exit 0 on merged main.
- **pokemon-mod-lab** — PR #52, SQUASH `08d2611dd2e5682148df446aaa44cc87dc211236`; designed-red runs 29170471574/29170495911; final-head green runs 29170517166 (substrate-gate) + 29170517167 (ROM builds); banked bootstrap-1.12.0.py; carve-out 0 found; strict exit 0.
- **venture-lab** — PR #56, MERGE-COMMIT `296a1a9363716662bd8a1babeb0c21bea49f343a`; designed-red run 29170528723; final-head green runs 29170566915 (substrate-gate) + 29170566922 (host tests); banked bootstrap-1.12.0.py; carve-out 0 found; strict exit 0.
- **fleet-manager** — PR #90, SQUASH `e801da5c0e00ba1b1b96e4384b61000740cc786e`; designed-red runs 29170511310/29170538236; final-head green runs 29170563751 (substrate-gate) + 29170563738 (roster-freshness); banked bootstrap-1.12.0.py; carve-out 0 found; strict exit 0.

All four: asset sha256 `1055ca2cfd32a83e3dab7a978b05fbec2a82932a3375de0b1034f2519c16e4aa` (704108 B) matched on first download; all pre-existing banks byte-identical; heartbeat `kit:` bumps left lane-owed per Q-0261.3.

⚑ flagged to the status.md FOR MANAGER area (wave-B scoped): pokemon-mod-lab heartbeat still v1.6.0 (two versions stale) · claims-home decision open · `automerge.required_context` says "substrate-gate" but the real required check is "ROM builds"; fleet-manager heartbeat still v1.7.0 · chronic owner-action-fields advisory · no live root CLAUDE.md · 3×-re-flagged lane-owed items proposed for graduation into control/inbox ORDERs; venture-lab `docs/AGENT_ORIENTATION.md` points at a `.claude/CLAUDE.md` that doesn't exist live (2nd consecutive wave, kit-side fix pending); gba-homebrew clean.

💡 Session idea: kit `upgrade` should emit a `banks:` sha256-audit block into `.substrate/upgrade-report.md` — old + new bank hashes for every `.substrate/backup/` entry — so distribution workers stop hand-hashing the backup dir every wave. This wave alone cost 4 workers a full-dir before/after hashing pass each; the upgrade command already touches every bank file and can record the hashes for free.

⟲ Previous-session review: the v1.12.1 release session (PR #244/#246, release run 29170017074) was a clean fifth runbook exercise, and its deliberate choice to defer BOTH the distribution wave and the adopters regen to dedicated distribution seats is what let waves A and B run in parallel without contention — good scoping, not laziness. One concrete improvement: its ⚑ CLASS DECISION (v1.13.0-penciled payload shipped as PATCH v1.12.1) is defensible but was recorded only in status prose; a one-line entry in the release runbook's decision log (or the changelog) would make the version-class precedent findable at the next ambiguous cut instead of relying on status.md archaeology.
