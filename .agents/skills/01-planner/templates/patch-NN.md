---
patch: patch-NNN
reqs: [REQ-XXX]
size_budget: {files: 5, loc: 150}
---

<!-- The record carries NO status field — the backlog's `## Patches` ledger is the SOLE status origin.
     size_budget defaults <=5 files / <=150 LOC; override at certification time with the reason on the P4 row. -->

# patch-NNN — <one-line description of the fix>

## Fix

<2-4 sentences: the observed broken behavior, the declared behavior it violates (name the REQ), and the
intended fix — enough for /04-builder to work from this record + the existing realizations.>

## Classification gate (patch iff ALL five pass)

| # | Check | Evidence |
|---|-------|----------|
| P1 | Maps to **existing, named REQ-IDs** | <REQ-NNN: why the broken behavior belongs to it; no new REQ needed> |
| P2 | **`docs/spec/**` untouched** (one additive exception: adds under `docs/spec/evals/**` + exactly one Tier-1 row) | <expected: no spine files in the touched set / the additive exception invoked> |
| P3 | **No new dependency** beyond the envelope | <expected: lockfile untouched> |
| P4 | **Bounded size** (≤ the size_budget above) | <expected touched files + rough LOC; if the default budget is overridden, why> |
| P5 | **Fixes existing behavior, adds none** | <how the fix stays inside the named REQs' existing outcome acceptance> |

> **Escalate when uncertain** — any check failing or unclear ⇒ not a patch. Execution scope →
> `/01-planner plan-sprint N`; product scope → `/00-discovery reflect`. Misclassifying *down* silently corrupts
> intent; misclassifying *up* costs one sprint plan.

## Expected touched files

- `<path>` — <why>

## Dispatch

- [ ] Ledger row added (`## Patches` in `docs/planning/backlog.md`, status `planned`)
- [ ] Run `/04-builder` on this patch (funnel: this record + existing realizations; handoff carries `review_mode: patch`)
