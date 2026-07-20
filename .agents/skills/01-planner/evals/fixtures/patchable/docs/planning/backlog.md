# Backlog — TeamPulse

> **The maintained execution ledger.** Owned by **skill 01 (planner)**. This is the single place where a REQ's
> **execution status** lives — `planned` / `in-progress` / `done`. It maps every requirement in the spine to the
> **build-order epic** and **sprint** that realizes it. It is a *realization* (it references the spine by `REQ-NNN`
> and never copies requirement prose) but it is **maintained, not generated**.

## Build order (epics)

1. **Epic 1 — Team & Access** — a person can sign in by magic-link, a lead can create a team with a configured
   digest time/timezone, and an invited person can join it under their own display name.
   _Foundation: identity (magic-link auth), the team, its members, and the configured digest moment. Covers REQ-007,
   REQ-004, REQ-006, REQ-005._
2. **Epic 2 — Standup capture** — a member can submit their daily standup (yesterday / today / blockers), revise it
   until the digest locks the day, and flag a blocker as "needs help". _Depends on Epic 1. Covers REQ-001, REQ-002,
   REQ-003._
3. **Epic 3 — The daily digest** — TeamPulse assembles one digest per day grouped by member, surfaces "needs help"
   blockers at the top, and lets members read the current and past digests. _Depends on Epics 1–2. Covers REQ-008,
   REQ-009, REQ-010._

## Ledger

| REQ | Name | Priority | Epic | Sprint | Status |
|-----|------|----------|------|--------|--------|
| REQ-007 | Sign in with an email magic-link | MUST | 1 | 01 | done |
| REQ-004 | Create a team and invite members by email | MUST | 1 | 01 | done |
| REQ-006 | Join a team via invite link and set a display name | MUST | 1 | 01 | done |
| REQ-005 | Configure the team's digest time and timezone | MUST | 1 | 01 | done |
| REQ-001 | Submit a daily standup | MUST | 2 | 01 | done |
| REQ-008 | Generate one daily digest grouped by member | MUST | 3 | 01 | done |
| REQ-002 | Edit a standup until the digest locks it | SHOULD | 2 | 02 | planned |
| REQ-003 | Flag a blocker as "needs help" | SHOULD | 2 | 02 | planned |
| REQ-009 | Surface "needs help" blockers at the top | SHOULD | 3 | 02 | planned |
| REQ-010 | Read current and past digests | SHOULD | 3 | 02 | planned |

- **Status vocabulary:** `planned` (not started) · `in-progress` (a sprint is realizing it) · `done` (shipped &
  verified). Skills 04/05/06 advance these as work lands; 01 sets them all `planned` at decomposition.

## Unallocated / flagged back to discovery

- _(none)_ — every spine REQ has an epic and sprint home; decomposition revealed no missing foundation requirement.
