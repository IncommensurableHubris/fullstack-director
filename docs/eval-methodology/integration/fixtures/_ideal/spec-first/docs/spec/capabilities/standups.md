# Capability: Standups

> Async daily status entries. A member answers three prompts (yesterday / today / blockers) on their own schedule;
> entries feed the daily digest. Each REQ is a delimited block per the contract in
> [`../specification.md`](../specification.md); every REQ here also appears in that file's REQ registry.

### REQ-001: Submit a daily standup   (MUST)

A member can submit a daily standup answering three prompts: yesterday, today, and blockers.

**Acceptance (outcome-level):**
```gherkin
Given a member of a team on a given day with no standup yet submitted
When they submit answers to the yesterday, today, and blockers prompts
Then their standup is recorded for that day and will appear in that day's digest
```
<!-- source: "PRD §Capabilities/Standups: 'A member can submit a daily standup answering three prompts: yesterday, today, blockers.'" -->
<!-- /REQ-001 -->

### REQ-002: Edit a standup until the digest locks it   (SHOULD)

A member can revise their standup for the current day up until that day's digest is generated; at the team's
configured digest time the day locks for **everyone** (a single team-wide lock instant, not per-member).

**Acceptance (outcome-level):**
```gherkin
Given a member who has submitted a standup for a day whose digest has not yet been generated
When they change their answers and resubmit
Then the updated answers replace the previous ones for that day

Given a day whose digest has already been generated
When the member attempts to edit that day's standup
Then the standup is locked and the edit is refused
```
<!-- source: "PRD §Capabilities/Standups: 'A member can edit their standup until the daily digest is generated; at the team's configured digest time the day locks for everyone.'" -->
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
