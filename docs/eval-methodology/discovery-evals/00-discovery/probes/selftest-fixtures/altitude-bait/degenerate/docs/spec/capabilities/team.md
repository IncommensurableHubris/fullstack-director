<!-- budget: ≤25 lines per REQ block — one home per fact; detail is realization, not spine. -->

# Capability: Team

> Standing up and joining a team: the lead creates it, invites by email, and sets the digest schedule; a member
> joins from an invite link. Each REQ is a delimited block per [`../specification.md`](../specification.md).

### REQ-005: Create a team and invite members   (MUST)

WHEN a lead creates a team and enters member email addresses, the system SHALL create the team and send each address an invitation.

**Acceptance (outcome-level):**
```gherkin
Given a signed-in lead
When they create a team and enter member email addresses to invite
Then the team is created and each address receives an invitation to join
```
<!-- source: "A lead can create a team and invite members by email." -->
<!-- /REQ-005 -->

### REQ-006: Configure digest time and timezone   (MUST)

WHEN a lead sets the team's digest time and timezone, the system SHALL adopt them as the schedule for that team's daily digest.

**Acceptance (outcome-level):**
```gherkin
Given a lead configuring their team
When they set the team's digest time and timezone
Then the team's daily digest is scheduled to generate at that time in that timezone
```
<!-- source: "A lead can set the team's digest time and timezone." -->
<!-- /REQ-006 -->

### REQ-007: Join a team via invite link   (MUST)

WHEN an invited person follows their invite link, the system SHALL add them to the team and let them set their own display name.

**Acceptance (outcome-level):**
```gherkin
Given a person who received an invite link
When they follow the link and choose a display name
Then they become a member of that team under that display name
```
<!-- source: "A member can join a team via an invite link and set their own display name." -->
<!-- /REQ-007 -->
