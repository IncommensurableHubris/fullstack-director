<!-- budget: ≤25 lines per REQ block — one home per fact; detail is realization, not spine. -->

# Capability: Standups

> A member's daily contribution: submit three prompts, revise until the digest locks it, flag a blocker for help.
> Each REQ is a delimited block per [`../specification.md`](../specification.md) and appears once in its registry.

### REQ-001: Submit daily standup   (MUST)

WHEN a member submits their standup for the day, the system SHALL record their answers to the three prompts — yesterday, today, and blockers.

**Acceptance (outcome-level):**
```gherkin
Given a signed-in member who has not yet submitted today
When they answer the three prompts (yesterday, today, blockers) and submit
Then their standup is saved and will appear under their name in that day's digest
```
> [NEEDS CLARIFICATION: is "today" the member's local day or the team's configured digest timezone? (assumption A2)]
<!-- source: "A member can submit a daily standup answering three prompts: yesterday, today, blockers." -->
<!-- /REQ-001 -->

### REQ-002: Edit standup before lock   (SHOULD)

WHILE that day's digest has not yet been generated, the system SHALL let a member revise their submitted standup.

**Acceptance (outcome-level):**
```gherkin
Given a member who submitted today's standup before the digest time
When they change an answer and resubmit
Then the updated answers replace the earlier ones for that day
```
<!-- source: "A member can edit their standup until the daily digest is generated; after that it is locked." -->
<!-- /REQ-002 -->

### REQ-003: Lock standup once digest is generated   (MUST)

IF a member tries to change their standup after that day's digest has been generated, THEN the system SHALL reject the change and preserve the digest's content.

**Acceptance (outcome-level):**
```gherkin
Given a member whose team digest for the day has already been generated
When they attempt to edit that day's standup
Then the change is refused and the digest remains unchanged
```
<!-- source: "A member can edit their standup until the daily digest is generated; after that it is locked." -->
<!-- /REQ-003 -->

### REQ-004: Flag a blocker as needs-help   (SHOULD)

WHEN a member marks a blocker as "needs help", the system SHALL flag that entry so the digest surfaces it.

**Acceptance (outcome-level):**
```gherkin
Given a member recording a blocker in their standup
When they mark that blocker as "needs help"
Then the entry is flagged and appears in the digest's help section
```
<!-- source: "A member can mark a blocker as 'needs help', which flags it in the digest." -->
<!-- /REQ-004 -->
