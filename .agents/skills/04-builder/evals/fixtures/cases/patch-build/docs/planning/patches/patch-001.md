---
patch: patch-001
reqs: [REQ-008]
size_budget: {files: 3, loc: 60}
---

# patch-001 — Digest drops standups submitted exactly at the lock minute

## Fix

REQ-008 declares one digest assembled at the team's configured time from the day's standups; sprint-01's review
accepted a member who did not submit *before* generation being omitted. A standup submitted **exactly at** the
lock minute is currently dropped too — a boundary comparison in `assembleDigest` (`src/digest.js`). Include the
at-lock submission in that day's digest.

## Classification gate (patch iff ALL five pass)

| # | Check | Evidence |
|---|-------|----------|
| P1 | Maps to existing, named REQ-IDs | REQ-008 owns digest assembly at the lock minute; no new REQ needed |
| P2 | `docs/spec/**` untouched | expected touched set is src + tests only; spine diff empty |
| P3 | No new dependency | a comparison flip + a node:test regression test; zero deps stays zero |
| P4 | Bounded size | ~2 files (src/digest.js + a regression test), ~20 LOC — inside 3 files / 60 LOC |
| P5 | Fixes existing behavior, adds none | stays inside REQ-008's acceptance (one digest at the configured time) |

> **Escalate when uncertain** — any check failing or unclear ⇒ not a patch (execution scope → `plan-sprint N`;
> product scope → `/00-discovery reflect`).

## Expected touched files

- `src/digest.js` — the boundary comparison at the lock minute
- `test/` — a reproducing regression test (at-lock submission included)

## Dispatch

- [x] Ledger row added (`## Patches` in `docs/planning/backlog.md`, status `planned`)
- [ ] Run `/04-builder` on this patch (funnel: this record + existing realizations; handoff carries `review_mode: patch`)
