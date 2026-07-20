# Assumption Map — TeamPulse

> Skill 00, phase 3 (CHALLENGE). Surfaces only the **Unknown + Important** bets the PRD does not already evidence —
> the ones that change what's worth building if wrong. A near-truth spec yields few; that is correct, not a failure.
> These feed the single batched REVIEW gate (PROCEED / CLARIFY / PIVOT — never KILL).

## Accepted premise (Known + Important — not surfaced)

- **Async beats synchronous standup for a distributed team.** This is the product's core JTBD bet, and the user
  deliberately committed to it in the PRD. Known+Important → leverage, do not re-litigate.

## Surfaced bets (Unknown + Important)

| # | Assumption (the undefended bet) | Lens | Why Unknown + Important — what breaks if wrong | Smallest test |
|---|---|---|---|---|
| A1 | Standups and digests are **isolated per team** — a member can never read another team's entries. | Feasibility / Viability | The PRD is multi-team (≤50 teams) but never states tenant isolation. If wrong, one team reads another's private status — a confidentiality breach. | Confirm isolation is required; captured as `derived` must-not **REQ-012** for confirmation at the gate. |
| A2 | The **day boundary** ("yesterday" / "today") for a distributed team is the **team's configured timezone**, not each member's local day. | Feasibility | Members are spread across timezones; the digest generates at *one* team time. If "today" is ambiguous, entries land in the wrong day's digest and the record is inconsistent. | Confirm the day boundary follows the team's digest timezone. Carried as `[NEEDS CLARIFICATION]` on REQ-001 / REQ-008. |
| A3 | The digest **represents members who did not submit** before digest time (e.g. shown as "no update"), rather than silently omitting them. | Desirability | "Stay in sync" depends on knowing who is silent or stuck. If non-submitters vanish, the lead can't tell "nothing to report" from "fell off." | Confirm how absentees appear. Carried as `[NEEDS CLARIFICATION]` on REQ-008. |

## Scope-shape observation (not a bet — a priority note for the gate)

- **MUST ratio:** 9 of 12 REQs are `MUST` (75%), above the 60% smell-test. **Judged defensible:** v1 is deliberately
  lean and the PRD already shows scope discipline (a clear out-of-scope list). The `SHOULD` set is the genuine
  refinements — edit-before-lock (REQ-002) and the help-blocker feature pair (REQ-004 / REQ-009). Not pushed back on.

## Gate outcome

**PROCEED** (autonomous eval run — no interactive user). A1 → `derived` REQ-012 (confirm at first human review); A2 &
A3 → `[NEEDS CLARIFICATION]` markers (non-blocking; 06-release blocks on any survivor). No PIVOT: no surfaced bet
undermines the premise. Recorded in the charter decision log.
