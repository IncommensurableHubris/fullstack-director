<!-- Filename: docs/architecture/specs/digest-assembly.md -->

# Feature Spec — digest-assembly

> **The per-sprint "build contract" realization.** Owned by **skill 03 (architect)**. References the sprint's REQs by
> ID and covers the `02` design manifest's DM-IDs; the **Verification Contract** below is mechanically gradeable.
> `04-builder` implements against it, `05-reviewer` executes it. `04` does not edit this file.

**Serves:** REQ-001, REQ-008, REQ-009 · **Status:** Approved

## Overview

The pure digest core plus a pure **text renderer**: record standups (one per member/day), assemble the day's digest
grouped by member with needs-help surfaced, and render it to legible text — a dated header, a needs-help section at
the top, then per-member sections. Every element is offline-verifiable via `node:test`.

## Related

- **Sprint:** `docs/planning/sprints/sprint-01.md` · **Design contract:** `docs/design/approved/sprint-01/manifest.md`
  · **Architecture:** `docs/architecture/system.md` §5 · **ADR:** ADR-001

## Components

| Component | Layer | Responsibility | Location (suggested) |
|-----------|-------|----------------|----------------------|
| `recordStandup` | domain core | one standup per member per day | `src/**` |
| `assembleDigest` | domain core | group by member; collect needs-help into a top section | `src/**` |
| `renderDigest` | domain core | render the digest to text: header (date) → needs-help → per-member sections | `src/**` |

## Implementation order

1. `recordStandup` — one per member/day. _(REQ-001)_
2. `assembleDigest` — group by member + needs-help. _(REQ-008, REQ-009)_
3. `renderDigest` — text rendering. _(REQ-008, REQ-009)_

## Verification Contract

> Each row is a boolean, all `unit` under `node:test`. Every in-scope REQ → ≥1 row; every manifest DM-ID → a covering
> row (see Design Contract Coverage).

| VC-ID | → REQ | Derived-from (spine Gherkin) | Method | Assertion (loosest claim that catches a break) | Pass-criterion (boolean) | Oracle |
|-------|-------|------------------------------|--------|------------------------------------------------|--------------------------|--------|
| VC-01 | REQ-001 | "the day still holds exactly one standup for that member" | unit | a second standup for the same member+day replaces the first — no duplicate | exactly one entry remains, latest answers | the returned entries collection |
| VC-02 | REQ-008 | "each member's entry grouped under their display name" | unit | assembling a day yields one digest with each member once, grouped | every member with a standup appears once, grouped, holding their entry | the assembled digest structure |
| VC-03 | REQ-009 | "all flagged blockers appear together in a dedicated section at the top" | unit | assembling collects every "needs help" blocker into one top section | the needs-help section contains exactly the flagged blockers | the assembled digest's needs-help section |
| VC-04 | REQ-008 | "grouped under their display name" (rendered) | unit | rendering the digest emits a dated header and one section per member under their display name | the rendered text contains the date header and each member's display name heading its entry | the rendered digest text |
| VC-05 | REQ-009 | "a dedicated section at the top of the digest" (rendered) | unit | rendering places the needs-help section above the per-member sections | in the rendered text the needs-help section precedes the first member section | the rendered digest text |

## Design Contract Coverage

> Forward direction: every manifest DM-ID → the VC row that verifies it.

| DM-ID | Element (from manifest) | Covered by |
|-------|-------------------------|-----------|
| DM-001 | Digest header with the date | VC-04 |
| DM-002 | Per-member grouped sections (display name + entry) | VC-04 |
| DM-003 | Needs-help section at the top | VC-05 |

## Not-Tested This Sprint

| Item | Reason | Deferred to |
|------|--------|-------------|
| persistence / any web delivery | pure core + text render only | later |
