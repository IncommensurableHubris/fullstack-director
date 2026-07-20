# Backlog — TeamPulse

> **The maintained execution ledger** (owner 01). The single place a REQ's **execution status**
> (`planned`/`in-progress`/`done`) lives — distinct from the spine registry's **fidelity** status. Every spine REQ
> appears here **exactly once**.

## Build order (epics)

1. **Epic 1 — Standup + digest core** — a member submits a standup; the daily digest assembles and reads.
   _Foundation: the data model + the digest assembly everything else consumes._
2. **Epic 2 — HTTP delivery** — the digest served over an authenticated API + the needs-help webhook. _Depends on: Epic 1._

## Ledger

| REQ | Name | Priority | Epic | Sprint | Status |
|-----|------|----------|------|--------|--------|
| REQ-001 | Submit a daily standup | MUST | 1 | 01 | done |
| REQ-008 | Generate one daily digest grouped by member | MUST | 1 | 01 | done |
| REQ-009 | Surface "needs help" blockers at the top | SHOULD | 1 | 01 | done |
| REQ-010 | Read current and past digests | SHOULD | 1 | 01 | done |
| REQ-020 | Serve the digest over an authenticated API | MUST | 2 | 02 | in-progress |
| REQ-021 | Notify the team on a "needs help" flag | SHOULD | 2 | 02 | in-progress |

- **Status vocabulary:** `planned` · `in-progress` (a sprint is realizing it) · `done` (shipped & verified).

## Patches

> The **expedite-lane ledger**. Every certified patch appears here **exactly once** — patch → owning REQs →
> status (`planned` · `in-progress` · `done` · `escalated`). **Sole origin of a patch's status.** One patch in
> flight at a time.

| Patch | REQs | Status |
|-------|------|--------|
| patch-001 | REQ-009 | planned |

## Unallocated / flagged back to discovery

- _(none)_
