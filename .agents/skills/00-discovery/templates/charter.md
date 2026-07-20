# Product Charter — <Project Name>

> **The product's intent anchor + decision log.** Owned by **skill 00 (discovery)**. This is the consolidated
> "loop document": the JTBD and problem framing the spine derives from, plus the running log of go/pivot decisions
> and REFLECT retrospectives. The spine (`docs/spec/`) is the *declaration-truth*; this charter is the *intent and
> history* behind it — so the spine stays regenerable from intent if an upstream pivot happens.

## Job to be Done

> The canonical job the product is hired for. Every requirement in the spine should trace back to this.

**When** _<situation>_, **I want** _<motivation>_, **so I can** _<expected outcome>_.

## Problem & user

- **Problem:** _<2–3 sentences, from the user's perspective — what is broken, painful, or missing>_
- **Target user:** _<a concrete segment — "a non-technical clinician seeing 5–20 patients/day", not "users">_
- **How they solve it today / what's painful:** _<the status quo this replaces>_

## Scope

- **In scope (this version):** _<the core capabilities that deliver the JTBD — these become the `MUST` requirements>_
- **Out of scope (explicitly excluded):** _<what is deliberately deferred — naming it prevents scope creep; old
  "Won't" items live here, not in the REQ registry>_

## Decision log

> Every PROCEED / CLARIFY / PIVOT at a discovery gate. Git carries the dates; this is the narrative.

| Decision | Phase | Rationale |
|----------|-------|-----------|
| _<PROCEED / CLARIFY / PIVOT>_ | _<initial discovery>_ | _<why>_ |

## Reflect log

> Appended by `/00-discovery reflect`: what we learned, what changed, which deferred (Tier-3) amendments were
> resolved. No date column — git is the trail.

- _<entry>_
