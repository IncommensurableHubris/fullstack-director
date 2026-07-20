# Capability: Team

> Forming a team and joining it. A lead creates a team, configures its digest schedule, and invites members by
> email; members join via an invite link and authenticate by email magic-link (the only auth mechanism in v1). Each
> REQ is a delimited block per the contract in [`../specification.md`](../specification.md); every REQ here also
> appears in that file's REQ registry.

### REQ-004: Create a team and invite members by email   (MUST)

A lead can create a team and invite members to it by email address.

**Acceptance (outcome-level):**
```gherkin
Given a lead who wants to set up a new team
When they create a team and enter one or more member email addresses to invite
Then the team exists and each invited address receives an invitation to join
```
<!-- source: "PRD §Capabilities/Team: 'A lead can create a team and invite members by email.'" -->
<!-- /REQ-004 -->

### REQ-005: Configure the team's digest time and timezone   (MUST)

A lead can set the time of day and timezone at which the team's daily digest is generated.

**Acceptance (outcome-level):**
```gherkin
Given a lead administering their team
When they set the team's digest time and timezone
Then the daily digest is generated at that time in that timezone
```
<!-- source: "PRD §Capabilities/Team: 'A lead can set the team's digest time and timezone.'" -->
<!-- /REQ-005 -->

### REQ-006: Join a team via invite link and set a display name   (MUST)

A member can accept an invitation through an invite link and choose their own display name on the team.

**Acceptance (outcome-level):**
```gherkin
Given a person who has received a team invite link
When they open the link and set their display name
Then they become a member of that team and their display name is used for their entries
```
<!-- source: "PRD §Capabilities/Team: 'A member can join a team via an invite link and set their own display name.'" -->
<!-- /REQ-006 -->

### REQ-007: Sign in with an email magic-link   (MUST)

A member can authenticate by requesting a one-time magic-link sent to their email — the only sign-in mechanism in v1
(no passwords, no third-party SSO).

**Acceptance (outcome-level):**
```gherkin
Given a person whose email is associated with a team membership
When they request a sign-in link and open the link sent to that email
Then they are signed in, with no password required
```
<!-- Derived: the PRD states magic-link as the *only* auth mechanism (a constraint) but does not state the
     user-facing sign-in capability or its acceptance — inferred here for confirmation. -->
<!-- source: inferred -->
<!-- /REQ-007 -->
