# Assumption Map — PlantPal

> Skill 00, phase 3 (CHALLENGE). Surfaces only the **Unknown + Important** bets the brief does not already
> evidence — the ones that change what's worth building if wrong. These feed the single batched REVIEW gate
> (PROCEED / CLARIFY / PIVOT — never KILL).

## Accepted premise (Known + Important — not surfaced)

- **A per-plant reminder beats a single global schedule.** The brief states this directly ("every plant is
  different — a cactus is not a fern"). Known+Important → leverage, do not re-litigate.

## Surfaced bets (Unknown + Important)

| # | Assumption (the undefended bet) | Lens | Why Unknown + Important — what breaks if wrong | Smallest test |
|---|---|---|---|---|
| A1 | A missed reminder (device off, notification denied) needs **no catch-up behavior** — the next scheduled reminder is simply the next one, with no backlog of missed reminders to surface. | Desirability | If a user's device was off for the interval, silently skipping to the next scheduled reminder could mean a plant goes unwatered for two full intervals with no signal. Undefended in the brief. | Confirm whether a missed reminder should surface a "was this watered?" catch-up prompt on next app open. Carried as `[NEEDS CLARIFICATION]` on REQ-003. |
| A2 | The watering interval is a **fixed number of days**, not a range or a condition (e.g. soil-moisture based). | Feasibility | The brief only says "gives it a watering interval" without specifying units or whether it can vary by season. If the real need is a range, the REQ-002 acceptance criteria under-specify it. | Confirm the interval is a fixed day-count for v1. Carried as `[NEEDS CLARIFICATION]` on REQ-002. |

## Scope-shape observation (not a bet — a priority note for the gate)

- **MUST ratio:** 4 of 5 REQs are `MUST` (80%), above the 60% smell-test. **Judged defensible:** the brief is
  explicitly narrow ("v1 ships the reminder loop and nothing else") and the one `SHOULD` (snooze) is a genuine
  refinement, not core-loop scope creep. Not pushed back on.

## Gate outcome

**PENDING.** Findings batched above; presented in `final-response.md`. The gate is held open — nothing is written
under `docs/spec/` until the user returns a PROCEED, CLARIFY, or PIVOT.
