# Capability: Standups

> A member's daily status input — the raw material of the digest. Each REQ is a delimited block per the contract in
> [`../specification.md`](../specification.md).

### REQ-001: Submit a daily standup   (MUST)

A member submits one standup per day — what they did, what's next, and an optional "needs help" flag.

**Acceptance (outcome-level):**
```gherkin
Given an authenticated member of a team
When they submit a standup for today
Then it is recorded as their standup for that day, replacing any earlier submission that day
```
<!-- source: "PRD §Input: 'Each member submits a short daily standup; at most one per member per day.'" -->
<!-- /REQ-001 -->
