---
patch: patch-001
reqs: [REQ-008]
size_budget: {files: 3, loc: 60}
---

# patch-001 — Digest drops a member's standup at the grouping boundary

## Fix

REQ-008 declares one daily digest grouped by member; a boundary condition in `assembleDigest` (`src/digest.js`)
dropped an entry in a narrow case. The fix stays inside REQ-008's existing acceptance and ships its reproducing
regression test.

## Classification gate (patch iff ALL five pass)

| # | Check | Evidence |
|---|-------|----------|
| P1 | Maps to existing, named REQ-IDs | REQ-008 owns digest assembly; no new REQ needed |
| P2 | `docs/spec/**` untouched | expected touched set is src + tests only; spine diff empty |
| P3 | No new dependency | zero-dep stack stays zero |
| P4 | Bounded size | ~2 files (src/digest.js + a regression test), ~20 LOC — inside 3 files / 60 LOC |
| P5 | Fixes existing behavior, adds none | stays inside REQ-008's acceptance |

> **Escalate when uncertain** — any check failing or unclear ⇒ not a patch.

## Expected touched files

- `src/digest.js` — the boundary fix
- `test/` — the reproducing regression test

## Dispatch

- [x] Ledger row added (`## Patches` in `docs/planning/backlog.md`, status `planned`)
- [x] Run `/04-builder` on this patch (done — handoff carried `review_mode: patch`); reviewed by a fresh `/05-reviewer` (SHIP)
