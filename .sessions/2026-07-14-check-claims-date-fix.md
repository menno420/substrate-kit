# 2026-07-14 · check_claims own-date fix (false claims-stale)

> **Status:** `in-progress`

About to happen (opening declaration): fix the `check_claims` work-claim
dating bug found live by the model-line-lint session (its card's
friction→guard recipe) — the checker dates a claim by the FIRST date-string
anywhere in the file, so a dated filename mentioned in the scope text makes
a fresh claim nag as stale. Fix: date the claim by the LAST date on the
bullet line (the taught grammar ends the bullet `· YYYY-MM-DD`), regression
tests, dist regenerated. Advisory posture unchanged.

- **📊 Model:** fable-5 · medium · runtime bugfix

Run type: worker session (coordinator-dispatched build).
