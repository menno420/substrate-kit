# Session 2026-07-09 — KL-3: telemetry substrate

> **Status:** `complete` *(kit-side KL-3 in one PR — #13.)*

**What happened (founding plan §10 KL-3 row, §5.2 B2, §5.3 B3):**

- **`src/engine/loop/telemetry.py`** — the guard-fire JSONL appender
  (`.substrate/guard-fires.jsonl`, the §5.3 record: ts · guard · cmd ·
  surface · posture · finding{path,kind,message} · verdict · reason · judge ·
  outcome) + the `📊 Model:` line parser and `session-close` harvest into
  `telemetry/model-usage.jsonl` (the PL-004 record; `tokens_out`
  null-tolerated per KF-9; `outcome` an all-null object the lab sweep
  backfills; one row per session slug). Fail-open by contract at every
  entry: telemetry can never crash a check, hook, or session-close. Writes
  engage only on an existing install (state dir present) so `check` stays
  read-only pre-adoption. **The `ci` surface and `did_not_run` are derived
  by readers from the Checks API, never written in CI** — a JSONL appended
  in an Actions runner dies with the job (plan §5.3, honored verbatim).
- **The two choke points wired:** `cmd_check`'s finding loop (all surfaced
  findings, allowlist suppressions with their verdicts, and session-log gate
  misses — the kit's flagship guard feeds B3 too) and `cmd_hook`'s dispatch
  (handlers now return their warnings; kinds stance / edit-advisor /
  stop-advisory; sessionstart is orientation, never a fire).
- **`src/engine/checks/allowlist.py`** — the reasons-required port
  (`.substrate/check-exceptions.yml`, schema `{path, kind, reason(REQUIRED),
  triaged, by, verdict?}`): stdlib YAML-subset parser; reason-less or
  malformed entries are refused and become findings; exact path+kind match
  only; creating an entry IS the false_positive/accepted_risk verdict event
  (the fire is recorded with the entry's verdict + reason). The session-log
  gate is never allowlistable.
- **The needle:** `📊 Model:` joined the default `session_markers` (new
  adopts require it from birth) and `upgrade` auto-adds it to an existing
  install's config with a loud report line — a consumer's gate only tightens
  when it upgrades, never mid-version (§5.2, honored).
- **`telemetry/` seeded:** `allocation-ladder.md` (the §5.2 program-wide
  ladder + KF-8 numbers N=2/M=3/14d/30d/≥3-runs, revised only with cited
  dataset rows) + `README.md` (feed schemas).
- **Dogfood (consumer #0):** the kit's own `substrate.config.json` carries
  the needle; `.sessions/README.md` names the marker; the first real
  guard-fire record committed is this session's own born-red gate hold; the
  `📊` line below is this repo's first harvested model-usage row (D6
  kit-side half).
- **Drift fixed on sight (Q-0166 class):** current-state's Next-action list
  still named KL-2's superbot companion + the KL-1 consumer pin PRs — all
  merged (superbot #1881 riders; superbot #1879 + superbot-next #42 pins;
  superbot-next #44 vendored-dist upgrade to v1.0.0, verified via GitHub).
  Next action now = KL-4.
- **Verified locally:** 535/535 pytest (501 → 535) · fresh-dist
  byte-compare clean · ruff engine bans green · `check_program_law` OK ·
  `dist/bootstrap.py check --strict --require-session-log` red on the
  born-red card exactly as designed, green at flip.

## ⚑ Flags

1. ⚑ Decide-and-flag: **one PR, not the plan's two** — the shared born-red
   card holds every PR it rides until it flips, so a same-card 2-PR split
   cannot merge PR 1; the band is one coherent seam and landed as one.
2. ⚑ Decide-and-flag: `guard` = the finding's `kind` (badge/link/ledger/…) —
   per-kind granularity is exactly the per-guard unit B3 computes FP rates
   over; a separate checker-name field would duplicate it.
3. ⚑ Decide-and-flag: "added at upgrade time, suggested by the upgrade
   report" (§5.2) read as **upgrade auto-adds the marker and reports it** —
   upgrade IS the version boundary where a gate may tighten; suggest-only
   would repeat the Phase-2.5 exhortation failure.
4. ⚑ Stop-hook advisories count as guard fires (kind `stop-advisory`) —
   they pass through the cmd_hook choke point and are the ritual guard's
   real signal; cheap to demote later if B3 shows noise.
5. ⚑ P10 note: this PR's merge behavior is itself evidence whether the
   `kit-quality` required-context swap landed; the `legacy-alias-*` job
   deletion stays gated on the owner's confirmation (current-state 👤 P10).

## 💡 Session idea

The Q-0248 taxonomy has **no class for new-capability building** — this very
session (engine feature work) had to file as its nearest neighbor, and KL-2
filed as an off-taxonomy compound ("docs-only + test writing") that the new
harvest would now warn on. Before the B2 dataset accumulates mislabeled
rows, mint a ruling: either a 9th class (`feature build`) via a PL-004
amendment, or a documented mapping rule ("a mixed session files its
dominant-cost class"). Cheap now, expensive after a thousand rows.

## ⟲ Previous-session review (kl2-governance-home)

Strong: the verbatim-import discipline (PL-002 kept to its provenance scope)
and the 8-word n-gram body-copy checker are exactly the enforce-don't-exhort
pattern, and it fixed the KL-1 tag-location drift on sight. Miss: its own
`📊 Model:` line used an off-taxonomy compound class — understandable
pre-harvest, but it shows a convention without a parser drifts immediately
(the same session *documented* the marker grammar it then bent).
**Workflow improvement shipped this session:** the harvest now
machine-checks the class against the 8 and warns — the drift class is
mechanized away; the remaining gap is the taxonomy itself (the 💡 above).

## Docs audit

`check --strict` green at flip (badges/links/reachability incl. the two new
`telemetry/` docs); CHANGELOG `[Unreleased]` extended (MINOR); D-0003 in the
decisions ledger; current-state stability/in-flight/next-action/recently-
shipped all updated (incl. the cross-repo DONE reconciliation); house-style
📊 row updated to the shipped mechanism; nothing left chat-only.

- **📊 Model:** fable-5 · high · kernel/architecture design
