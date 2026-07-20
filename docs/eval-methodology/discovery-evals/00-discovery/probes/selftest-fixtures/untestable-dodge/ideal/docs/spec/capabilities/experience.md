<!-- budget: ≤25 lines per REQ block — one home per fact; detail is realization, not spine. -->

# Capability: Experience

> Sprintly's core interaction feel and first-run onboarding. Each REQ is a delimited block per
> [`../specification.md`](../specification.md).

### REQ-001: Feel instant during core interactions   (MUST)

The system SHALL feel instant during core interactions — creating a ticket, dragging a card, filtering the
board, switching sprints.

**Acceptance (outcome-level):**
```gherkin
Scenario: instant interaction
  Given a user is viewing the sprint board
  When the user creates a ticket, drags a card, or switches sprints
  Then the interface responds immediately, with no perceptible delay
```
`[NEEDS CLARIFICATION: "instant" has no response-time threshold in the brief — confirm a target (e.g. p95
latency in ms) with product before this is testable; REQ-005 proposes one for page loads only.]`
<!-- source: "Sprintly feels instant. Every interaction ... responds the moment the user acts on it. There is
no spinner Sprintly asks a user to sit through, no perceptible lag between intent and result." -->
<!-- /REQ-001 -->

### REQ-002: Deliver delightfully simple onboarding   (MUST)

WHEN a new user signs up, the system SHALL deliver a delightfully simple onboarding experience that gets them
planning their first sprint immediately.

**Acceptance (outcome-level):**
```gherkin
Scenario: first-time onboarding
  Given a new user has just signed up
  When the user lands in their workspace
  Then the user creates and assigns their first sprint ticket in 3 steps or fewer, each screen rendering
    within 300 ms
```
`[NEEDS CLARIFICATION: the "3 steps or fewer" / "300 ms" figures are skill 00's proposal to make "delightfully
simple" and "immediately" testable — the brief gives no step count or timing; confirm with product before
treating as a committed target.]`
<!-- source: inferred -->
<!-- /REQ-002 -->
