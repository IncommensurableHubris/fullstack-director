# Capability: Digest

> The single daily artifact the whole team reads. TeamPulse assembles one digest per day, grouped by member, with
> "needs help" blockers surfaced at the top; members can read current and past digests. Each REQ is a delimited block
> per the contract in [`../specification.md`](../specification.md).

### REQ-008: Generate one daily digest grouped by member   (MUST)

TeamPulse assembles exactly one daily digest for a given day from that day's standups, with each member's entry
grouped under their display name.

**Acceptance (outcome-level):**
```gherkin
Given a team with members' standups for a given day
When the digest for that day is assembled
Then a single digest for that day is produced, with each member's entry grouped under their display name
```
[NEEDS CLARIFICATION: how does the digest represent a member who did not submit a standup before generation — omit them, show a "no update" placeholder, or list them as missing?]
<!-- source: "PRD §Capabilities/Digest: 'TeamPulse generates one daily digest, grouping entries by member.'" -->
<!-- /REQ-008 -->

### REQ-009: Surface "needs help" blockers at the top   (SHOULD)

The digest collects every blocker flagged "needs help" into a dedicated section at the top of the digest.

**Acceptance (outcome-level):**
```gherkin
Given a day's standups in which one or more blockers are flagged "needs help"
When the digest for that day is assembled
Then all flagged blockers appear together in a dedicated section at the top of the digest
```
<!-- source: "PRD §Capabilities/Digest: 'The digest surfaces all \"needs help\" blockers in a dedicated section at the top.'" -->
<!-- /REQ-009 -->

### REQ-010: Read current and past digests   (SHOULD)

A member can read the current day's digest and the digest for any past day.

**Acceptance (outcome-level):**
```gherkin
Given a member of a team for which digests have been generated
When they open the digest for the current day or select a past day
Then they can read that day's digest
```
<!-- source: "PRD §Capabilities/Digest: 'A member can read the current and past digests for any day.'" -->
<!-- /REQ-010 -->
