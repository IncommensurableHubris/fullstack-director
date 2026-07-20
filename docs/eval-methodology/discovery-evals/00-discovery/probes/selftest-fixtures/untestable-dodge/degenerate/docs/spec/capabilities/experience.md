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
  Then the user is able to plan their first sprint without consulting documentation
```
<!-- source: "Onboarding is delightfully simple. ... requires no training, no documentation, and no ramp-up
period — a team lead who has never used Sprintly should be productive with it immediately." -->
<!-- /REQ-002 -->
