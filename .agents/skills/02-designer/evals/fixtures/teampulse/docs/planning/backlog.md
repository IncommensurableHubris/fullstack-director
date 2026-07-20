# Backlog — TeamPulse

> **The maintained execution ledger.** Owned by **skill 01 (planner)**. This is the single place where a REQ's
> **execution status** lives — `planned` / `in-progress` / `done`. It maps every requirement in the spine to the
> **build-order epic** and **sprint** that realizes it. It is a *realization* (it references the spine by `REQ-NNN`
> and never copies requirement prose) but it is **maintained, not generated**: status **originates here** and is
> updated in place by later skills as work progresses — it is never regenerated from anything else.
>
> ⚠ **Two different "status" columns exist in this project — do not conflate them:**
> - The **spine registry** (`docs/spec/specification.md`) `Status` = `stated` | `derived` — *fidelity*, owned by 00.
> - This **ledger** `Status` = `planned` | `in-progress` | `done` — *execution*, owned by 01.
>
> They live in different files. **Never write execution status into the spine registry, and never write fidelity
> into this ledger.** Writing `done` into the spine would corrupt the declaration/realization boundary.

## Build order (epics)

> The spine is organized **by domain** (the user's declaration). Skill 01 regroups those REQs into **build-order**
> epics — chronological layers where each epic depends on the ones before it (foundation → core workflow →
> consuming features). Build order is **01's execution call**, recorded here — it is *not* a declaration and never
> goes back into the spine.

1. **Epic 1 — Team & Access** — a person can sign in by magic-link, a lead can create a team with a configured
   digest time/timezone, and an invited person can join it under their own display name.
   _Foundation: identity (magic-link auth), the team, its members, and the configured digest moment — nothing
   downstream runs without these. Covers REQ-007, REQ-004, REQ-006, REQ-005._
2. **Epic 2 — Standup capture** — a member can submit their daily standup (yesterday / today / blockers), revise it
   until the digest locks the day, and flag a blocker as "needs help". _Goal: the daily input that feeds the one
   artifact. Depends on: Epic 1 (a member must exist on a team). Covers REQ-001, REQ-002, REQ-003._
3. **Epic 3 — The daily digest** — TeamPulse assembles one digest per day grouped by member, surfaces "needs help"
   blockers at the top, and lets members read the current and past digests. _Goal: the single artifact the whole
   team reads — the product's payoff. Depends on: Epics 1–2 (it consumes standups). Covers REQ-008, REQ-009,
   REQ-010._

## Ledger

> Every REQ in the spine appears here **exactly once**. `Epic` and `Sprint` are zero-padded sprint numbers
> (`sprint-01` → `01`). `Status` is execution-only. `Priority` is copied from the spine registry (RFC 2119) — it is
> a convenience mirror for sprint scoping, not a second source of truth.

| REQ | Name | Priority | Epic | Sprint | Status |
|-----|------|----------|------|--------|--------|
| REQ-007 | Sign in with an email magic-link | MUST | 1 | 01 | planned |
| REQ-004 | Create a team and invite members by email | MUST | 1 | 01 | planned |
| REQ-006 | Join a team via invite link and set a display name | MUST | 1 | 01 | planned |
| REQ-005 | Configure the team's digest time and timezone | MUST | 1 | 01 | planned |
| REQ-001 | Submit a daily standup | MUST | 2 | 01 | planned |
| REQ-008 | Generate one daily digest grouped by member | MUST | 3 | 01 | planned |
| REQ-002 | Edit a standup until the digest locks it | SHOULD | 2 | 02 | planned |
| REQ-003 | Flag a blocker as "needs help" | SHOULD | 2 | 02 | planned |
| REQ-009 | Surface "needs help" blockers at the top | SHOULD | 3 | 02 | planned |
| REQ-010 | Read current and past digests | SHOULD | 3 | 02 | planned |

- **Status vocabulary:** `planned` (not started) · `in-progress` (a sprint is realizing it) · `done` (shipped &
  verified). Skills 04/05/06 advance these as work lands; 01 sets them all `planned` at decomposition.
- **Sprint assignment** follows MoSCoW from the spine priority and the slicing craft: `MUST` REQs concentrate in the
  earliest sprints (sprint 1 = the walking skeleton — all 6 MUSTs on the happy path); `SHOULD`/`MAY` widen the path
  in later sprints (sprint 2 = the 4 SHOULDs).

> **Epic-vs-sprint note.** Epics are the *build-order layers* (a REQ's permanent home); sprints are the *delivery
> slices* (which thin vertical thread carries it). Sprint 1 is a vertical slice that intentionally spans all three
> epics — it pulls the foundation MUSTs plus exactly one core MUST (REQ-001) and one consuming MUST (REQ-008) so the
> end-to-end JTBD loop is demonstrable. That is why Epic 2/3 REQs appear in Sprint 01: the slice is vertical, not the
> epic.

## Unallocated / flagged back to discovery

> If decomposition revealed a **genuinely missing** requirement (a foundation REQ with no home in the spine), it is
> **not invented here** — it is a Tier-3 scope finding flagged back to `/00-discovery reflect`. List any such gaps
> below so the handoff is explicit; leave empty if none.

- _(none)_ — every spine REQ has an epic and sprint home; decomposition revealed no missing foundation requirement.

> **Adjacent observation (not a scope finding, not invented here):** the assumption map's top Unknown+Important bet
> (A1 — async completion rate without a meeting's social pressure) notes that a *reminder/nudge before digest time*
> is **not** in the v1 capability list. Sprint 1 is deliberately built to **test** A1 (submit → generate → read),
> not to add a reminder. If the dogfood shows completion drops, a reminder is a **new capability** for
> `/00-discovery reflect`, never minted here.

## Open clarifications carried from the spine (not resolved here)

> Planner does not resolve declarations. These `[NEEDS CLARIFICATION]` markers live on REQs in this plan; they are
> surfaced per-sprint in the sprint files' "Risks & open questions" and must be resolved before `06-release`.

- **REQ-002** — edit-lock instant for members whose timezone differs from the team's digest timezone. (Sprint 02.)
- **REQ-008** — how the digest represents a member who did not submit before generation (omit / placeholder /
  missing). (Sprint 01 — the skeleton ships a defensible default; see sprint-01 risks.)
