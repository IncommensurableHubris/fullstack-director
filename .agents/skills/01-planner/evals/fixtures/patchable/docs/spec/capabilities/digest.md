# Capability: Digest

> The single daily artifact the whole team reads. TeamPulse assembles one digest per day at the team's configured
> time, grouped by member, with "needs help" blockers surfaced at the top; members can read current and past
> digests. Each REQ is a delimited block per the contract in [`../specification.md`](../specification.md); every REQ
> here also appears in that file's REQ registry.

### REQ-008: Generate one daily digest grouped by member   (MUST)

TeamPulse generates exactly one daily digest at the team's configured time, assembling the day's standups grouped by
member. A member who did not submit before generation is **omitted** from that day's digest (no placeholder row).

**Acceptance (outcome-level):**
```gherkin
Given a team with members' standups for a given day
When the team's configured digest time is reached
Then a single digest for that day is generated, with each member's entry grouped under their display name
```
<!-- source: "PRD §Capabilities/Digest: 'TeamPulse generates one daily digest at the team's configured time, grouping entries by member. A member who did not submit before generation is omitted from that day's digest.'" -->
<!-- /REQ-008 -->

### REQ-009: Surface "needs help" blockers at the top   (SHOULD)

The digest collects every blocker flagged "needs help" into a dedicated section at the top of the digest.

**Acceptance (outcome-level):**
```gherkin
Given a day's standups in which one or more blockers are flagged "needs help"
When the digest for that day is generated
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
