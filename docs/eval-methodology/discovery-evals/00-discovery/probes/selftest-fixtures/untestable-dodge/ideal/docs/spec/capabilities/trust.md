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
`[NEEDS CLARIFICATION: "enterprise-grade" names no concrete standard — confirm which certifications/controls
apply (e.g. SOC 2 Type II, ISO 27001, encryption-at-rest and in-transit requirements) before this is testable.]`
<!-- source: "Sprintly ships enterprise-grade security out of the box. ... protected to the standard an
enterprise security team expects, from day one." -->
<!-- /REQ-003 -->

### REQ-004: Scale effortlessly to any team size   (MUST)

The system SHALL scale effortlessly to any team size, from a two-person team to a two-thousand-person org, with
the same responsiveness and simplicity.

**Acceptance (outcome-level):**
```gherkin
Scenario: scaling to team size
  Given a workspace of up to 10,000 members
  When the team grows within that range
  Then board interactions remain within the REQ-001 responsiveness target with no re-architecture
```
`[NEEDS CLARIFICATION: "any team size" has no ceiling in the brief — 10,000 members is skill 00's proposed
upper bound to make "effortlessly" testable; confirm the real target with product.]`
<!-- source: inferred -->
<!-- /REQ-004 -->
