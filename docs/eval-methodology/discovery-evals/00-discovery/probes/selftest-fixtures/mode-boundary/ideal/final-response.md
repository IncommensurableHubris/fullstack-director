# EXPLORE run — summary

**Mode:** `/00-discovery explore` (pre-commitment). **Itch:** "something for my invoice stress — dashboards? reminders? maybe inbox-zero? idk."

**Only artifact written:** `docs/discovery/exploration.md` (≤80-line budget). **Hard invariant honored:** nothing under `docs/spec/**` — verified no `docs/spec/` directory exists.

## The four moves
- **PULL** — Recorded a Mom-Test elicitation plan (5 past-event / real-workflow questions). Non-interactive arm: no live user, so user answers are marked PENDING. Only the itch is user-origin; every reframe is tagged `origin: model`.
- **DIVERGE** — 4 distinct problem framings, each Torres-tested (passes: >1 solution fits each), each with option-families + a smallest-test:
  - **F1** (`user`) — no reliable at-a-glance view of outstanding/overdue invoices.
  - **F2** (`model`) — nothing prompts action at the right moment, so invoices drift past due (attacks the mechanism).
  - **F3** (`model`) — the real lack is confidence about incoming cash; "overdue" is a proxy (deepest; explains the stress).
  - **F4** (`model`) — no repeatable billing/collections routine (opens a legitimate no-software outcome).
- **APPETITE** — **Small batch** (a few days / a couple weekend afternoons), explicitly not a multi-week product; a size, not an estimate.
- **PICK GATE** (run autonomously) — **Rank F2 → F3 → F1; F4 as no-build fallback. Recommendation: DON'T BUILD (yet)** — run the cheap smallest-tests first (calendar reminders + dunning template on the current backlog; trial auto-pay on new clients). Devil's-advocate against the lead (F2): reminders are symptom-level and can raise anxiety; the durable leverage may be upstream prevention (F3) or a behavioral routine (F4), in which case building any tracker is the wrong move.

**Handoff:** deferred (pre-commitment). If the user proceeds, F2 seeds ITCH's JTBD; the one-line charter decision-log pointer is drafted inside `exploration.md` to be added when the default flow runs (charter not written in this mode).
