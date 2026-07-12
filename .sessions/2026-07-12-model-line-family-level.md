# 2026-07-12 — Model line: family-level naming mandate (close the exact-model-ID gap)

> **Status:** `in-progress`

- **📊 Model:** fable-5 · high · runtime bugfix

## Scope (what is about to happen)

Coordinator-directed bounded slice (fleet reporting bar: family-level model
names only in repo artifacts, never exact model-ID tokens; context: a
websites-repo cleanup PR, websites #178 @ 6664b5f, corrected a card that
followed the narrower old wording). The kit's planted `.sessions/README.md`
model doctrine (`src/engine/adopt.py` `_model_doctrine_text`) currently bans
only a "full dated model ID" — but exact model IDs are not always dated
(e.g. a `claude-`-prefixed exact ID token with no date suffix), so cards
following the letter of the doctrine still recorded exact IDs. This slice:

1. Rewords the doctrine's ban from "full dated model ID" to ANY exact model
   ID / model-ID token (dated or not) — family-level names only. The
   idempotency detection phrase (`_MODEL_DOCTRINE_PHRASE`) is deliberately
   untouched so retroactive merges stay idempotent.
2. Applies the same rewording to the kit's own `.sessions/README.md` copy.
3. Aligns the one place that scans card Model: lines — the KL-3
   session-close harvest (`harvest_model_usage`) — with an advisory (never
   exit-affecting, like the task-class advisory beside it) when the model
   segment looks like an exact model-ID token.
4. Tests + CHANGELOG `[Unreleased]` + dist rebuild (byte-pin).

Adopter repos' existing cards/READMEs are NOT retro-edited — the fix reaches
adopters at the next release + `upgrade --apply-docs`.

Lane claim: `control/claims/claude-model-line-family-level.md` (deleted at
close, last commit).

## Close-out

(to be written)

## 💡 Session idea

(to be written)

## ⟲ Previous-session review

(to be written)
