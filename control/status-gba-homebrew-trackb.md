# gba-homebrew Track B (visiting adopter lane) · status

> Visiting-lane heartbeat per the v1.4.0 multi-lane pattern (`control/README.md`
> § per-lane heartbeats) and the coordinator-lane precedent (#52/#73): this
> file's sole writer is the **gba-homebrew Track B lane**, visiting to upstream
> two adopter-found defect fixes. Deliberately **not in `heartbeat_files`** —
> kit-lab owns `substrate.config.json`; decide-and-flag. This lane never writes
> `control/status.md`, `control/inbox.md`, or `substrate.config.json` — one
> writer per file. Archive/delete this file freely once the visit closes.

updated: 2026-07-10T05:06:52Z
phase: visit COMPLETE with this build PR's merge — both gate-template sentinel fixes shipped upstream (claim #105 → this build PR, per the claim ritual); the lane returns to its home repo (menno420/gba-homebrew) and will not write here again unless a new visit re-claims
health: green
kit: adopter-side v1.6.0 (menno420/gba-homebrew) · check: green · engaged: yes
last-shipped: this build PR — `live_ci_workflow()` gate-template fixes: (1) no-card PRs pass an explicitly named nonexistent `--session-log` sentinel WITHOUT `--require-session-log` (advisory per the engine contract; the bare mtime fallback was NOT fail-open in CI — it latched onto the mid-session in-progress card, gba-homebrew PR #3); (2) a card ADDED by the PR (born-red heartbeat) gates advisory via the absent sentinel while a MODIFIED card keeps the full locked door (gba-homebrew PR #2 merged red without this). Tests updated + new added-vs-modified test; CHANGELOG [Unreleased] Fixed entry; dist regenerated (byte-pin); session card .sessions/2026-07-10-gate-template-sentinel-fixes.md (complete). Suite 814 passed local; check --strict exit 0.
blockers: none
orders: none for this lane (no inbox order; defect-fix visit under the adopter-findings precedent, cf. #83 and the #99 adopter-findings batch) — claim `gate-template-sentinel-fixes` (landed #105) is CLEARED by this overwrite: the build ships in the same PR that carries this close
⚑ needs-owner: none
notes: VISIT LEDGER — claim #105 (control fast lane, merged by auto-merge on green) → bus re-read at HEAD 7faef99 (no ORDER ≥010, no live sibling claim — the queue-item-11 claim was cleared by #104) → this build PR (src/engine/adopt.py + tests + CHANGELOG + dist + card + this close). Both fixes were found, fixed and validated LIVE on the adopter menno420/gba-homebrew (public): its PRs #3–#14 all ran the fixed gate — heartbeat/no-card/feature PRs green, incomplete close-out cards still red on the locked door. The kit's own ci.yml is unaffected (it restores card mtimes from commit times — a third solution to the same flattened-mtime trap; see the 💡 on the session card for collapsing the three).
