# 2026-07-11 — Queued kit fixes batch (4) — v1.8.0 payload

> **Status:** `complete`

## What is about to happen

Coordinator-assigned dev slice (not an inbox order): the QUEUED KIT FIXES batch
carried in control/status.md — four fixes, each with a regression test and a
CHANGELOG `[Unreleased]` entry (v1.8.0 payload). NO release cut this session.

1. **Carve-out report explicit-when-clean** — `_regen_kit_owned_workflow()` /
   `upgrade_report_text()`: a clean scan now emits an explicit
   `carve-out scan: <relpath> — ran, 0 found` line and the upgrade report
   always states scan status (ran-clean vs nothing-to-scan vs never-ran).
2. **Already-banked backup hash-verify** — `archive_dist()`: a pre-existing
   archive at the target name whose bytes differ is NEVER overwritten; the
   dist banks under a content-hash-suffixed dedup name and the collision is
   reported.
3. **Mid-PR gate-regen born-red semantics** (venture-lab #14) — decide-and-flag:
   the generated gate's card-selection routes an ADDED card through the
   LOCKED DOOR when the same PR also touches the gate workflow file itself,
   so hold semantics can only tighten, never loosen, inside the PR that
   changes them.
4. **Code-span-aware unrendered-slot scan** (the #148/#150 poison) —
   `${VAR}` inside inline code spans / fenced blocks no longer reads as an
   unfilled interview slot; plus decide-and-flag on the fast-lane skip: the
   control fast lane (`check --strict --status-only`) now runs the
   unrendered scan scoped to control-plane planted docs, so a control-only
   PR can no longer smuggle a slot regression past the scan onto main.

Claim: `control/claims/kit-fixes-batch.md` (PR #155, fast lane, armed).

## What happened (close-out)

Shipped all four fixes, whole — none deferred. Build commit faffea3 on PR #156
(claim #155 squash c232804 landed on main before build; branch updated after).

1. **Carve-out scan explicit-when-clean** — `_regen_kit_owned_workflow()`
   (src/engine/adopt.py) appends `carve-out scan: <relpath> — ran, 0 found` on
   both clean shapes (kept-already-current and regenerated-clean); a dirty
   regen keeps reporting `carve-out:` hit lines instead. `run_upgrade()`
   collects both prefixes and `upgrade_report_text()` (src/engine/upgrade.py)
   now always writes a `## Carve-out scan` section: per-file clean lines, or a
   pointer at the ⚠️ hits section, or an explicit "no kit-owned live workflow
   installed, nothing to scan". The post-hoc `--apply-docs` report passes
   `carveouts=None` and carries no section — there the detector honestly never
   ran, which is exactly the distinguisher the fix creates.
2. **Already-banked backup hash-verified** — `archive_dist()`
   (src/engine/adopt.py): pre-existing target-name archive byte-compared;
   identical → the existing `(already banked)` line; DIFFERENT → the new bytes
   bank under `bootstrap-<version>.<sha8>.py` with a loud `name collision …
   NOT overwritten` report line; the earlier bank (a rollback source) is left
   byte-untouched; idempotent on the dedup name too.
3. **Mid-PR gate-regen born-red semantics (decided-and-flagged)** — chosen
   prevention: make the generated gate's card-selection ENFORCING and
   direction-stable — a card ADDED by a PR whose diff also touches
   `.github/workflows/substrate-gate.yml` gates through the full
   `--require-session-log` locked door instead of the added-card advisory
   sentinel. Rationale (one line): GitHub always runs the PR head's workflow,
   so true version-stability is impossible — the cheapest enforcing invariant
   is "hold semantics may only TIGHTEN, never loosen, inside the PR that
   changes them", and the locked door is the tighter of the two generations;
   the merge path is unchanged (flip the card complete). A checker warning
   (the documented alternative) would have been advisory-only — exhortation,
   not enforcement.
4. **Code-span-aware slot scan + the fast-lane call (decided-and-flagged)** —
   `find_placeholders_outside_code()` (src/engine/render.py; fences stripped
   first, then inline spans — the proven check_session_log pair, renamed
   `_MD_*` to satisfy the dist namespace-collision guard) feeds the
   `unrendered-slot` finding in `_unrendered_findings()`
   (src/engine/checks/check_engagement.py). The banner branch keeps FULL-TEXT
   slot evidence on purpose: a doc under the UNRENDERED banner is kit output,
   so a backticked template slot (the ai-project-workflow
   verify_command shape) still holds the gate via `unrendered-banner`.
   **Fast-lane call: the skip WAS the deeper bug and it was cheap to close** —
   `check --strict --status-only` now also runs `check_engagement_control()`
   (the same banner/slot scan scoped to planted docs under `control/`), so a
   control-only PR writing a bare slot regression into a heartbeat reds ITS
   OWN fast-lane run instead of poisoning main for every subsequent full-lane
   PR (the exact #148 shape). No new deadlock class: the only pre-render
   window where control docs carry slots is the adopt-seed state, which the
   status checker's no-heartbeat finding already holds red on the same lane.
5. Tests **927 → 938** (+11): 3 in test_adopt.py (clean-scan lines · archive
   dedup/never-overwrite · gate regen-guard text), 2 in test_upgrade.py
   (report clean-scan section · nothing-to-scan line), 5 in
   test_check_engagement.py (span/fence poison green · bare slot still red +
   span excluded from listing · banner keeps full-text evidence · control
   scope · cmd_check --status-only red/green pair), 1 in test_render.py
   (find_placeholders_outside_code unit). CHANGELOG `[Unreleased]` ### Fixed
   ×4 (v1.8.0 payload, NO release cut). Dist regenerated + byte-pin clean.
6. Verified: `python3 -m pytest tests/ -q` → **938 passed**; `python3 -m ruff
   check src/engine/` clean; `python3 dist/bootstrap.py check --strict` →
   sole pre-flip finding was this card's own born-red hold (verified again
   post-flip, exit 0). Mid-flight coordinator red ping on born-red head
   9acaced root-caused per PL-006 from job log 86489117880: the designed
   session-gate hold (missing close-out markers + in-progress badge); the
   two extra red jobs were the legacy-alias mirrors of kit-quality — no
   defect, no fix pushed for it.

- **📊 Model:** Fable 5 · high effort · kit-dev-slice (fixes batch + tests)

💡 Session idea: `upgrade-report.md` now proves the carve-out scan ran, but
NOTHING proves an adopter ever read the report — the enabler auto-merges the
upgrade PR on green. A cheap `check` advisory ("upgrade-report.md contains a
⚠️ carve-out section newer than the last session card — acknowledge by
moving the banked additions or allowlisting") would close the last silent
gap in the #137 protection chain: detection → banking → reporting →
**acknowledgement**. (Deduped against docs/ideas/ — nothing covers
report-acknowledgement.)

⟲ Previous-session review (§6.10, #152/#153/#154): exemplary shape — claim
first, born-red PR open within minutes, decided-and-flagged design calls with
one-line rationales, and the factored `_regen_kit_owned_workflow()` made this
session's fix 1 a two-hunk change instead of a two-file fork. What it could
have done better: it carried queued fix 1 knowing the report was silent when
clean but did not leave a failing-test sketch for it — a one-assert xfail
would have cut this session's re-derivation. Concrete workflow improvement:
queued-fix entries in status.md should each carry a guard recipe line
(function + file + test target), the .sessions/README.md convention, so the
next dev slice starts at the code anchors instead of a grep pass.

Docs audit: CHANGELOG carries the four payload entries; the gate semantics
change is documented in the generated workflow's own comments + the
live_ci_workflow docstring (the doc the regen distributes); status close-out
(squash SHA + CI run + next-slice pointer + queued-fixes clear + EAP §6
completion note) follows as the fast-lane heartbeat PR per the #148/#151/#154
precedent; claim `control/claims/kit-fixes-batch.md` is deleted there. No
inbox ORDER 012+ existed at preflight (highest 011, done — re-checked at the
close-out read).
