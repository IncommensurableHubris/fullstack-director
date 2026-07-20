# Assumption Map — TeamPulse

> Loaded by skill 00, phase 3 (CHALLENGE). The lightweight 2×2 stress-test: only **Unknown + Important** assumptions
> reach the gate. TeamPulse ships from a deliberately-researched, high-fidelity PRD, so this list is intentionally
> short — a near-truth spec leaves few Unknowns. The gate is PROCEED / CLARIFY / PIVOT, never KILL.

## Surfaced bets (Unknown + Important)

### A1 — Async completion rate holds without a meeting's social pressure
- **Lens:** Desirability (the JTBD bet).
- **Why Unknown + Important:** The PRD evidences the *cost* of synchronous standups but not that members will
  reliably submit an async standup once the meeting's accountability is removed. The entire JTBD ("share **and
  absorb** daily status") depends on entries actually arriving before the digest is generated; if completion drops,
  the digest is empty and the product fails silently. Nothing in the input defends the completion-rate assumption.
- **Smallest test:** A one-team, two-week dogfood measuring daily submission rate; or a lightweight reminder/nudge
  before digest time (note: reminders are *not* in the v1 capability list — surfacing this, not adding scope).

## Parked (Unknown but not premise-breaking, or Known)

- **Scale (≤ 50 teams / ≤ 600 members on one VPS):** Known — trivially within a single Postgres/VPS footprint.
- **Stack & hosting (TS/Node, Postgres, single EU VPS, Docker):** Known — conventional, user-committed, feasible.
- **Magic-link auth as the only mechanism:** Known/feasible — standard pattern; captured as a `derived` REQ for the
  user-facing flow (see FIDELITY gaps, not a challenge).
- **"Digest reads in under two minutes for 12 people":** a design/UX target (skill 02 realizes it), not a
  premise-breaking bet — parked.
