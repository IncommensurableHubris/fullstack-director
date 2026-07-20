# Product Charter — TeamPulse

> **The product's intent anchor + decision log.** Owned by **skill 00 (discovery)**. The JTBD and problem framing the
> spine derives from, plus the running log of go/pivot decisions. The spine (`docs/spec/`) is *declaration-truth*;
> this charter is the *intent and history* behind it.

## Job to be Done

> The canonical job the product is hired for. Every requirement in the spine traces back to this.

**When** my team is spread across timezones, **I want** to share and absorb daily status without a meeting, **so I can**
stay in sync without losing focus time.

## Problem & user

- **Problem:** Distributed engineering teams lose 3–4 hours/week to standup meetings scheduled across timezones.
  People in the wrong timezone either lose sleep to attend or skip the meeting and fall out of sync.
- **Target user:** An engineer on a 4–12-person distributed team (the **"member"**). Secondary: the **"lead"** who
  configures the team and reads the digest first.
- **How they solve it today / what's painful:** A synchronous daily standup meeting that never fits everyone's
  timezone — the status quo TeamPulse replaces with an async daily digest.

## Scope

- **In scope (v1):** Async standups (submit / edit-until-locked / flag-for-help), team setup (create + invite +
  configure digest time & timezone + join), the daily digest (generation grouped by member, help-blockers surfaced,
  read current & past), and the passwordless (email magic-link) access that gates all of it.
- **Out of scope (v1, explicitly excluded):** Slack/Teams integration; analytics dashboards; mobile apps; paid
  plans / billing. Named here to prevent scope creep — these are not registry rows.

## Decision log

> Every PROCEED / CLARIFY / PIVOT at a discovery gate. Git carries the dates; this is the narrative.

| Decision | Phase | Rationale |
|----------|-------|-----------|
| PROCEED | initial discovery | Near-truth PRD: all six coverage facets present and the JTBD is stated verbatim. Three Unknown+Important bets surfaced (tenant isolation, distributed-day boundary, non-submitter handling) — isolation captured as a `derived` must-not REQ for confirmation; the other two carried as `[NEEDS CLARIFICATION]` markers (non-blocking pre-release). No contradictions. Autonomous run: proceed without interactive clarification per eval protocol. |

## Reflect log

> Appended by `/00-discovery reflect`: what we learned, what changed, which deferred (Tier-3) amendments resolved.

- _(none yet)_
