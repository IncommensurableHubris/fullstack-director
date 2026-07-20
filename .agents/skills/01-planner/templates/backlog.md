# Backlog — <Project Name>

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

1. **Epic 1 — <name>** — <one-sentence goal: what capability exists when this epic is done>.
   _Foundation: <what everything else depends on — accounts, auth, the core data model>._
2. **Epic 2 — <name>** — <goal>. _Depends on: Epic 1._
3. **Epic 3 — <name>** — <goal>. _Depends on: Epics 1–2._

## Ledger

> Every REQ in the spine appears here **exactly once**. `Epic` and `Sprint` are zero-padded sprint numbers
> (`sprint-01` → `01`). `Status` is execution-only. `Priority` is copied from the spine registry (RFC 2119) — it is
> a convenience mirror for sprint scoping, not a second source of truth.

| REQ | Name | Priority | Epic | Sprint | Status |
|-----|------|----------|------|--------|--------|
| REQ-007 | <short name> | MUST | 1 | 01 | planned |
| REQ-004 | <short name> | MUST | 1 | 01 | planned |
| REQ-001 | <short name> | MUST | 2 | 01 | planned |
| REQ-008 | <short name> | MUST | 3 | 01 | planned |
| REQ-009 | <short name> | SHOULD | 3 | 03 | planned |

- **Status vocabulary:** `planned` (not started) · `in-progress` (a sprint is realizing it) · `done` (shipped &
  verified). Skills 04/05/06 advance these as work lands; 01 sets them all `planned` at decomposition.
- **Sprint assignment** follows MoSCoW from the spine priority and the slicing craft: `MUST` REQs concentrate in the
  earliest sprints (sprint 1 = the walking skeleton); `SHOULD`/`MAY` widen the path in later sprints.

## Patches

> The **expedite-lane ledger** (the patch lane). Every certified patch appears here **exactly once** —
> patch → owning REQs → status. **This table is the sole origin of a patch's status** (the patch record in
> `docs/planning/patches/` carries none). Vocabulary: `planned` · `in-progress` · `done` · `escalated` —
> 04/05/06 advance these as the patch moves; a mid-build gate violation marks it `escalated` and the work
> re-enters the normal chain. **One patch in flight at a time.** ≥3 consecutive done-patches without a planned
> sprint, or any `escalated` row, is sprint pressure — `/status` surfaces the advisory.

| Patch | REQs | Status |
|-------|------|--------|

## Unallocated / flagged back to discovery

> If decomposition revealed a **genuinely missing** requirement (a foundation REQ with no home in the spine), it is
> **not invented here** — it is a Tier-3 scope finding flagged back to `/00-discovery reflect`. List any such gaps
> below so the handoff is explicit; leave empty if none.

- _(none)_ — or: _<the missing capability> — flagged to `/00-discovery reflect` (scope change; 01 does not invent scope)._
