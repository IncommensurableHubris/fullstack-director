<!-- budget: ≤25 lines per REQ block — one home per fact; detail is realization, not spine. -->

# Capability: Access & Identity

> How a person signs in (passwordless, email magic-link) and the tenant boundary that keeps one team's status
> private to that team. REQ-012 is `derived` (inferred) — a must-not flagged for human confirmation at first review.

### REQ-011: Email magic-link sign-in   (MUST)

WHEN a user requests access with their email address, the system SHALL email a single-use magic link that signs them in when followed.

**Acceptance (outcome-level):**
```gherkin
Given a member or lead with an email address on a team
When they request sign-in with that email
Then they receive a single-use magic link that, when followed, starts an authenticated session
```
<!-- source: "Auth: email magic-link only — no passwords, no third-party SSO in v1." -->
<!-- /REQ-011 -->

### REQ-012: Isolate team data across tenants   (MUST)

IF a user requests standups or a digest belonging to a team they are not a member of, THEN the system SHALL deny access.

**Acceptance (outcome-level):**
```gherkin
Given a signed-in user who is not a member of a given team
When they request that team's standups or digest
Then access is denied
```
<!-- source: inferred -->
<!-- /REQ-012 -->
