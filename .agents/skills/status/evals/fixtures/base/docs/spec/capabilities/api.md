# Capability: HTTP API (sprint-02 delivery)

> The digest, served over HTTP — the sprint-02 delivery. Each REQ is a delimited block per the contract in
> [`../specification.md`](../specification.md).

### REQ-020: Serve the digest over an authenticated API   (MUST)

A member authenticates (magic-link session) and reads the digest over HTTP. **A member reads only their own team's
data** — the API must not disclose one member's or team's digest to another (Constitution §6, least access).

**Acceptance (outcome-level):**
```gherkin
Given an authenticated member of a team
When they request the digest over the API
Then they receive their own team's digest, and never another member's or team's data
```
<!-- source: "PRD §Delivery/API: 'Members read the digest over an authenticated HTTP API, scoped to their own team.'" -->
<!-- /REQ-020 -->

### REQ-021: Notify the team on a "needs help" flag   (SHOULD)

When a standup flags "needs help," TeamPulse posts a notification to the team's configured channel webhook.

**Acceptance (outcome-level):**
```gherkin
Given a team with a configured notification webhook
When a member submits a standup flagged "needs help"
Then TeamPulse posts a notification to that team's configured channel
```
<!-- source: "PRD §Delivery/API: 'A needs-help flag notifies the team via its configured webhook.'" -->
<!-- /REQ-021 -->
