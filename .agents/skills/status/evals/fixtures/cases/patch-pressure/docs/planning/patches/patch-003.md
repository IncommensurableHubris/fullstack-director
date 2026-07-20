---
patch: patch-003
reqs: [REQ-010]
size_budget: {files: 3, loc: 60}
---

# patch-003 — Past-digest pagination off-by-one

## Fix

The oldest digest was unreachable from the history list. Maps to REQ-010's existing acceptance; no new REQ.

## Classification gate (patch iff ALL five pass)

| # | Check | Evidence |
|---|-------|----------|
| P1 | Maps to existing, named REQ-IDs | REQ-010 owns the behavior; no new REQ needed |
| P2 | `docs/spec/**` untouched | code + tests only; spine diff empty |
| P3 | No new dependency | stdlib only |
| P4 | Bounded size | ~2 files, ~20 LOC — inside 3 / 60 |
| P5 | Fixes existing behavior, adds none | stays inside REQ-010's acceptance |

> **Escalate when uncertain.**

## Expected touched files

- `src/` — the fix
- `test/` — the reproducing regression test

## Dispatch

- [x] Ledger row added (`## Patches`, status `planned`)
- [x] Run `/04-builder` on this patch (handoff carries `review_mode: patch`)
