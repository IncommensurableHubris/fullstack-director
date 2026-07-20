<!-- Filename: docs/planning/sprints/sprint-01.md -->

# Sprint 01 — Digest core: record standups → assemble the day's digest grouped by member

**Goal:** The pure digest core works: a member's standup is recorded (one per member per day), and the day's standups
assemble into a single digest grouped by member. Headless — no UI this sprint.
**Slice shape:** domain core · spans: standups, digest.
**REQs:** 2 — 2 MUST-equivalent core behaviors.

## REQs in this sprint — frozen acceptance snapshot

### REQ-001: Submit a daily standup   (MUST)   →   `docs/spec/capabilities/standups.md`

```gherkin
# frozen from spine @ sprint-01
Given a member who already submitted a standup for the day
When they submit again for that same day
Then the day still holds exactly one standup for that member, with the latest answers
```

### REQ-008: Generate one daily digest grouped by member   (MUST)   →   `docs/spec/capabilities/digest.md`

```gherkin
# frozen from spine @ sprint-01
Given a team with members' standups for a given day
When the digest for that day is assembled
Then a single digest for that day is produced, with each member's entry grouped under their display name
```

## Done When

> The coarse, observable definition of done for the slice — traceable to the REQ IDs.

- [ ] Recording a member's standup twice for the same day leaves exactly one entry for that member, with the latest answers. _(REQ-001)_
- [ ] Assembling a day's standups produces one digest with each member's entry grouped under their display name. _(REQ-008)_

## Implementation order

1. **Record a standup (one per member/day)** — the entry the digest is built from. _(REQ-001)_
2. **Assemble the digest grouped by member** — the day's output. _(REQ-008)_

## Sprint boundary

- **In scope:** the pure `recordStandup` + `assembleDigest` core, happy path, verified by `node:test`.
- **Out of scope:** needs-help surfacing (REQ-009), rendering to text, persistence, any UI — later sprints.
