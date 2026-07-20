# Capability: Standups

> Async daily status entries. A member answers three prompts (yesterday / today / blockers) on their own schedule;
> entries feed the daily digest. Each REQ is a delimited block per the contract in
> [`../specification.md`](../specification.md).

### REQ-001: Submit a daily standup   (MUST)

A member can submit a daily standup answering three prompts: yesterday, today, and blockers. At most one standup per
member per day — a resubmission replaces the day's entry rather than adding a second.

**Acceptance (outcome-level):**
```gherkin
Given a member of a team on a given day with no standup yet submitted
When they submit answers to the yesterday, today, and blockers prompts
Then their standup is recorded for that day and will appear in that day's digest

Given a member who already submitted a standup for the day
When they submit again for that same day
Then the day still holds exactly one standup for that member, with the latest answers
```
<!-- source: "PRD §Capabilities/Standups: 'A member can submit a daily standup answering three prompts: yesterday, today, blockers.'" -->
<!-- /REQ-001 -->

### REQ-002: Edit a standup until the digest locks it   (SHOULD)

A member can revise their standup for the current day up until that day's digest is generated, after which it is locked.

**Acceptance (outcome-level):**
```gherkin
Given a member who has submitted a standup for a day whose digest has not yet been generated
When they change their answers and resubmit
Then the updated answers replace the previous ones for that day
```
<!-- source: "PRD §Capabilities/Standups: 'A member can edit their standup until the daily digest is generated; after that it is locked.'" -->
<!-- /REQ-002 -->

### REQ-003: Flag a blocker as "needs help"   (SHOULD)

A member can mark a blocker as "needs help" so it is surfaced prominently in the digest.

**Acceptance (outcome-level):**
```gherkin
Given a member filling in the blockers prompt of their standup
When they mark a blocker as "needs help"
Then that blocker is flagged so the digest can surface it in its "needs help" section
```
<!-- source: "PRD §Capabilities/Standups: 'A member can mark a blocker as \"needs help\", which flags it in the digest.'" -->
<!-- /REQ-003 -->
