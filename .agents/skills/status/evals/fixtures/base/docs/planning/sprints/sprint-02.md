# Sprint 02 — HTTP delivery (authenticated digest API + needs-help webhook)

**Goal:** Serve the digest over an authenticated HTTP API scoped to the member's own team, and notify the team's
channel when a standup flags "needs help." The first networked surface.
**REQs:** 2.

## REQs in this sprint — frozen acceptance snapshot

### REQ-020: Serve the digest over an authenticated API   (MUST)   →   `docs/spec/capabilities/api.md`

```gherkin
# frozen from spine @ sprint-02
Given an authenticated member of a team
When they request the digest over the API
Then they receive their own team's digest, and never another member's or team's data
```

### REQ-021: Notify the team on a "needs help" flag   (SHOULD)   →   `docs/spec/capabilities/api.md`

```gherkin
# frozen from spine @ sprint-02
Given a team with a configured notification webhook
When a member submits a standup flagged "needs help"
Then TeamPulse posts a notification to that team's configured channel
```

## Done When

- [ ] An authenticated member reads their own team's digest over the API; another member's data is never disclosed. _(REQ-020)_
- [ ] A "needs help" flag posts a notification to the team's configured webhook. _(REQ-021)_
