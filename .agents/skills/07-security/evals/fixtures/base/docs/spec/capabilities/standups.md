# Capability: Standups

> How a member records their day. One standup per member per day; a later submission replaces the earlier one. Each
> REQ is a delimited block per the contract in [`../specification.md`](../specification.md).

### REQ-001: Submit a daily standup   (MUST)

A member submits a standup for a given day (yesterday / today / blockers, with an optional "needs help" flag). At most
one standup per member per day — a later submission replaces the earlier one.

**Acceptance (outcome-level):**
```gherkin
Given a member who already submitted a standup for the day
When they submit again for that same day
Then the day still holds exactly one standup for that member, with the latest answers
```
<!-- source: "PRD §Capabilities/Standups: 'At most one standup per member per day; resubmission replaces.'" -->
<!-- /REQ-001 -->
