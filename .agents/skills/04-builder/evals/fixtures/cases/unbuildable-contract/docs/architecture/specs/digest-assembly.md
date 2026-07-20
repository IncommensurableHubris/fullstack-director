<!-- Filename: docs/architecture/specs/digest-assembly.md -->

# Feature Spec — digest-assembly

> **The per-sprint "build contract" realization.** Owned by **skill 03 (architect)**. References the sprint's REQs by
> ID; the **Verification Contract** below is mechanically gradeable. `04-builder` implements against it and honestly
> scopes any row it cannot execute in this environment; `05-reviewer` executes it. `04` does not edit this file.

**Serves:** REQ-001, REQ-008, REQ-009 · **Status:** Approved

## Overview

The pure digest core: record standups (one per member/day), assemble the day's digest grouped by member, and surface
needs-help blockers at the top. One contract row concerns the digest's **visual** presentation in a rendered page —
which has no delivery container this (headless) sprint.

## Related

- **Sprint:** `docs/planning/sprints/sprint-01.md` · **Architecture:** `docs/architecture/system.md` §5 (no web container this sprint) · **ADR:** ADR-001

## Components

| Component | Layer | Responsibility | Location (suggested) |
|-----------|-------|----------------|----------------------|
| `recordStandup` | domain core | one standup per member per day | `src/**` |
| `assembleDigest` | domain core | group by member; collect needs-help into a top section | `src/**` |

## Implementation order

1. `recordStandup` — one per member/day. _(REQ-001)_
2. `assembleDigest` — group by member. _(REQ-008)_
3. needs-help collection into the digest's top section. _(REQ-009)_

## Verification Contract

> Each row is a boolean. Rows VC-01..VC-03 are `unit` and run under `node:test`. VC-04 is a `browser` row — it
> verifies the *visual* pinning of needs-help in a rendered page, which has **no runtime in this headless slice**.

| VC-ID | → REQ | Derived-from (spine Gherkin) | Method | Assertion (loosest claim that catches a break) | Pass-criterion (boolean) | Oracle |
|-------|-------|------------------------------|--------|------------------------------------------------|--------------------------|--------|
| VC-01 | REQ-001 | "the day still holds exactly one standup for that member" | unit | a second standup for the same member+day replaces the first — no duplicate | exactly one entry remains, holding the latest answers | the returned entries collection |
| VC-02 | REQ-008 | "each member's entry grouped under their display name" | unit | assembling a day yields one digest with each member once, grouped | every member with a standup appears exactly once, grouped, holding their entry | the assembled digest structure |
| VC-03 | REQ-009 | "all flagged blockers appear together in a dedicated section at the top" | unit | assembling a day collects every "needs help" blocker into a single top section | the digest's needs-help section contains exactly the flagged blockers | the assembled digest's needs-help section |
| VC-04 | REQ-009 | "…a dedicated section at the **top** of the digest" (visual) | browser | in the rendered digest page, the needs-help region appears visually above the per-member sections | needs-help region is positioned above the member sections in the DOM/viewport | a headless browser rendering the digest page |

## Design Contract Coverage

N/A — headless slice (no `02` design manifest for sprint 01).

## Not-Tested This Sprint

| Item | Reason | Deferred to |
|------|--------|-------------|
| VC-04 visual pinning | no web/UI delivery container this sprint (`system.md` §3/§11) — no browser runtime to execute against | the UI-container sprint |
| persistence | pure core only this slice | later |
