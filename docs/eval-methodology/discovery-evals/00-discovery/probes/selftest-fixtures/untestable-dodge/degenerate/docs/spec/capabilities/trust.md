<!-- budget: ≤25 lines per REQ block — one home per fact; detail is realization, not spine. -->

# Capability: Trust and scale

> Security posture and team-size scaling. Each REQ is a delimited block per
> [`../specification.md`](../specification.md).

### REQ-003: Provide enterprise-grade security   (MUST)

The system SHALL provide enterprise-grade security for every workspace, ticket, and attachment, from day one.

**Acceptance (outcome-level):**
```gherkin
Scenario: enterprise-grade protection
  Given a workspace contains tickets and attachments
  When any data is stored or transmitted
  Then it is protected to the standard an enterprise security team expects
```
<!-- source: "Sprintly ships enterprise-grade security out of the box. ... protected to the standard an
enterprise security team expects, from day one." -->
<!-- /REQ-003 -->

### REQ-004: Scale effortlessly to any team size   (MUST)

The system SHALL scale effortlessly to any team size, from a two-person team to a two-thousand-person org, with
the same responsiveness and simplicity.

**Acceptance (outcome-level):**
```gherkin
Scenario: scaling to team size
  Given a workspace of any size
  When the team grows
  Then the board remains just as responsive and simple to use
```
<!-- source: "Sprintly scales effortlessly to any team size. A two-person team and a two-thousand-person org
run on the same product, with the same responsiveness and the same simplicity." -->
<!-- /REQ-004 -->
