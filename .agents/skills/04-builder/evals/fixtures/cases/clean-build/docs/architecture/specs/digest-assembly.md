<!-- Filename: docs/architecture/specs/digest-assembly.md -->

# Feature Spec — digest-assembly

> **The per-sprint "build contract" realization.** Owned by **skill 03 (architect)**. References the sprint's REQs by
> ID; the **Verification Contract** below is mechanically gradeable (a boolean per row): `04-builder` implements
> against it, `05-reviewer` executes it. `04` does not edit this file.

**Serves:** REQ-001, REQ-008 · **Status:** Approved

## Overview

The pure digest core for sprint 01: record a member's standup (one per member per day) and assemble a day's standups
into a single digest grouped by member. No I/O, no clock reads — the day is passed in as data.

## Related

- **Sprint:** `docs/planning/sprints/sprint-01.md` · **Architecture:** `docs/architecture/system.md` §5 · **ADR:** ADR-001

## Components

| Component | Layer | Responsibility | Location (suggested) |
|-----------|-------|----------------|----------------------|
| `recordStandup` | domain core | add/replace a member's standup for a day (one per member/day) | `src/**` |
| `assembleDigest` | domain core | group a day's standups by member into one digest | `src/**` |

## Implementation order

1. `recordStandup(entries, standup) → entries'` — replace on same member+day. _(REQ-001)_
2. `assembleDigest(standups, day) → digest` — group by member. _(REQ-008)_

## Verification Contract

> The gradeable core. Each row is a **boolean**. Every in-scope REQ → ≥1 row. The assertion is the loosest claim that
> still catches a break — verified by `node:test`, offline.

| VC-ID | → REQ | Derived-from (spine Gherkin) | Method | Assertion (loosest claim that catches a break) | Pass-criterion (boolean) | Oracle |
|-------|-------|------------------------------|--------|------------------------------------------------|--------------------------|--------|
| VC-01 | REQ-001 | "the day still holds exactly one standup for that member, with the latest answers" | unit | recording a second standup for the same member+day replaces the first — no duplicate | after two submissions by one member for one day, exactly one entry remains and it holds the latest answers | the returned entries collection |
| VC-02 | REQ-008 | "each member's entry grouped under their display name" | unit | assembling a day's standups yields one digest in which each member appears once with their own entry | every member with a standup appears exactly once, grouped under their display name, holding their entry | the assembled digest structure |

## Design Contract Coverage

N/A — headless slice (no `02` design manifest for sprint 01).

## Not-Tested This Sprint

| Item | Reason | Deferred to |
|------|--------|-------------|
| needs-help surfacing | REQ-009 not in this slice | sprint 02 |
| rendering to text / any UI | no delivery container this sprint | later |
