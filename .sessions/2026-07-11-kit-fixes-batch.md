# 2026-07-11 — Queued kit fixes batch (4) — v1.8.0 payload

> **Status:** `in-progress`

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

(in progress)
