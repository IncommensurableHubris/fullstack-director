<!-- Filename: docs/planning/sprints/sprint-01.md -->

# Sprint 01 — Digest core + text render (grouped, needs-help first)

**Goal:** The pure digest core records standups (one per member/day), assembles the day's digest grouped by member
with needs-help surfaced, and **renders** the digest to legible text (a dated header, a needs-help section at the top,
then per-member sections). Headless text output — verified by `node:test`.
**Slice shape:** domain core + renderer · spans: standups, digest.
**REQs:** 3.  **Design contract:** `docs/design/approved/sprint-01/manifest.md` (the text-render elements).

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

### REQ-009: Surface "needs help" blockers at the top   (SHOULD)   →   `docs/spec/capabilities/digest.md`

```gherkin
# frozen from spine @ sprint-01
Given a day's standups in which one or more blockers are flagged "needs help"
When the digest for that day is assembled
Then all flagged blockers appear together in a dedicated section at the top of the digest
```

## Done When

- [ ] Recording a member's standup twice for the same day leaves exactly one entry, with the latest answers. _(REQ-001)_
- [ ] Assembling a day's standups produces one digest with each member's entry grouped under their display name. _(REQ-008)_
- [ ] All "needs help" blockers appear together in a dedicated top section of the digest. _(REQ-009)_
- [ ] Rendering the digest yields a dated header, a needs-help section at the top, then per-member sections. _(REQ-008, REQ-009)_

## Implementation order

1. **Record a standup (one per member/day).** _(REQ-001)_
2. **Assemble the digest grouped by member, with needs-help.** _(REQ-008, REQ-009)_
3. **Render the digest to text** (header → needs-help → per-member sections). _(REQ-008, REQ-009)_

## Sprint boundary

- **In scope:** the pure core + a pure text renderer, verified by `node:test`.
- **Out of scope:** persistence, any web/UI delivery, styling — later sprints.
