<!-- budget: ≤25 lines per REQ block — one home per fact; detail is realization, not spine. -->

# Capability: Digest

> The one artifact the whole team reads: generated daily at the team's time, grouped by member, with help-blockers
> surfaced, and readable for any day. Each REQ is a delimited block per [`../specification.md`](../specification.md).

### REQ-008: Generate the daily digest grouped by member   (MUST)

WHEN the team's configured digest time is reached, the system SHALL generate exactly one digest for that day, grouping entries by member.

**Acceptance (outcome-level):**
```gherkin
Given a team whose members have submitted standups for the day
When the configured digest time is reached
Then one digest is generated for that day with entries grouped by member
```
> [NEEDS CLARIFICATION: are members who did not submit before digest time represented (e.g. "no update") or omitted? (assumption A3)]
<!-- source: "TeamPulse generates one daily digest at the team's configured time, grouping entries by member." -->
<!-- /REQ-008 -->

### REQ-009: Surface needs-help blockers at the top   (SHOULD)

The daily digest SHALL present all blockers marked "needs help" in a dedicated section at the top.

**Acceptance (outcome-level):**
```gherkin
Given a digest for a day that has one or more "needs help" blockers
When the digest is assembled
Then those blockers appear together in a dedicated section at the top of the digest
```
<!-- source: "The digest surfaces all 'needs help' blockers in a dedicated section at the top." -->
<!-- /REQ-009 -->

### REQ-010: Read the digest for any day   (MUST)

WHEN a member opens the digest for a given day, the system SHALL display that day's digest — the current day's once generated, or any past day's.

**Acceptance (outcome-level):**
```gherkin
Given a signed-in member of a team
When they open the digest for a given day
Then they can read that day's digest, whether it is the current or a past day
```
<!-- source: "A member can read the current and past digests for any day." -->
<!-- /REQ-010 -->
