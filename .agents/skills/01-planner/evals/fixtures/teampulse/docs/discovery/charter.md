# Product Charter — TeamPulse

> **The product's intent anchor + decision log.** Owned by **skill 00 (discovery)**. This is the consolidated
> "loop document": the JTBD and problem framing the spine derives from, plus the running log of go/pivot decisions
> and REFLECT retrospectives. The spine (`docs/spec/`) is the *declaration-truth*; this charter is the *intent and
> history* behind it — so the spine stays regenerable from intent if an upstream pivot happens.

## Job to be Done

> The canonical job the product is hired for. Every requirement in the spine should trace back to this.

**When** my engineering team is spread across timezones, **I want** to share and absorb daily status without a
meeting, **so I can** stay in sync without losing focus time.

## Problem & user

- **Problem:** Distributed teams lose 3–4 hours/week to standup meetings scheduled across timezones. People in the
  wrong timezone either lose sleep to attend or skip the meeting and fall out of sync. The synchronous format taxes
  focus time and penalizes whoever is furthest from the chosen hour.
- **Target user:** An engineer on a 4–12 person distributed team (the **member**). Secondary: the **team lead** who
  configures the team and reads the digest first.
- **How they solve it today / what's painful:** A synchronous daily standup meeting scheduled across timezones —
  costly in focus time and inequitable across regions.

## Scope

- **In scope (v1):** the three capability areas — **Standups** (submit / edit-until-lock / needs-help), **Team**
  (create + invite, digest time & timezone, join via link), **Digest** (daily generation grouped by member,
  needs-help surfacing, read current & past).
- **Out of scope (explicitly excluded):** Slack/Teams integration; analytics dashboards; mobile apps; paid
  plans / billing. (These are the deliberate "Won't" items — recorded here, never as REQ rows.)

## Decision log

> Every PROCEED / CLARIFY / PIVOT at a discovery gate. Git carries the dates; this is the narrative.

| Decision | Phase | Rationale |
|----------|-------|-----------|
| PROCEED | initial discovery | High-fidelity PRD; stack/scope/success all stated. One adoption bet (async completion) accepted as a PROCEED risk; two behavioral gaps (no-submission digest handling, edit-lock timing across timezones) carried as `[NEEDS CLARIFICATION]`; magic-link auth captured as a `derived` REQ for confirmation. No contradictions found. |

## Reflect log

> Appended by `/00-discovery reflect`: what we learned, what changed, which deferred (Tier-3) amendments were
> resolved. No date column — git is the trail.

- _(none yet)_
