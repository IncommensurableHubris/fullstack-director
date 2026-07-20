# Backlog — TeamPulse

> **The maintained execution ledger.** Owned by **skill 01 (planner)**. Execution status lives here.

## Build order (epics)

1. **Epic 1 — Standup capture** — submit a daily standup. _Covers REQ-001._
2. **Epic 2 — The daily digest** — one digest per day grouped by member, needs-help on top. _Covers REQ-008, REQ-009._

## Ledger

| REQ | Name | Priority | Epic | Sprint | Status |
|-----|------|----------|------|--------|--------|
| REQ-001 | Submit a daily standup | MUST | 1 | 01 | done |
| REQ-008 | Generate one daily digest grouped by member | MUST | 2 | 01 | done |
| REQ-009 | Surface "needs help" blockers at the top | SHOULD | 2 | 01 | done |

- **Status vocabulary:** `planned` · `in-progress` · `done`. Skills 04/05/06 advance these as work lands.

## Patches

> The **expedite-lane ledger**. Every certified patch appears here **exactly once** — patch → owning REQs →
> status. **This table is the sole origin of a patch's status** (the patch record carries none). Vocabulary:
> `planned` · `in-progress` · `done` · `escalated` — 04/05/06 advance these as the patch moves. **One patch in
> flight at a time.**

| Patch | REQs | Status |
|-------|------|--------|
| patch-001 | REQ-008 | in-progress |

## Unallocated / flagged back to discovery

- _(none)_
