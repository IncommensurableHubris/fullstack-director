# Capability: Digest

> The one artifact the whole team reads (Constitution §2). Each REQ is a delimited block per the contract in
> [`../specification.md`](../specification.md).

### REQ-008: Generate one daily digest grouped by member   (MUST)

Once per day, TeamPulse assembles the team's standups into a single digest, grouped by member.

**Acceptance (outcome-level):**
```gherkin
Given a team whose members have submitted standups for the day
When the daily digest is generated
Then it presents each member's standup, grouped by member, as one artifact
```
<!-- source: "PRD §Digest: 'One digest per team per day, grouped by member.'" -->
<!-- /REQ-008 -->

### REQ-009: Surface "needs help" blockers at the top   (SHOULD)

Standups flagged "needs help" are surfaced at the top of the digest so blockers are seen first.

**Acceptance (outcome-level):**
```gherkin
Given a digest with one or more members flagged "needs help"
When the digest is presented
Then the "needs help" members appear at the top, ahead of the rest
```
<!-- source: "PRD §Digest: 'Blockers rise to the top.'" -->
<!-- /REQ-009 -->

### REQ-010: Read current and past digests   (SHOULD)

A member can read today's digest and browse past days'.

**Acceptance (outcome-level):**
```gherkin
Given an authenticated member of a team
When they open the digest view
Then they can read today's digest and navigate to prior days' digests for their team
```
<!-- source: "PRD §Digest: 'Members read the current digest and browse history.'" -->
<!-- /REQ-010 -->
