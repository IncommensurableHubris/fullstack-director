# TeamPulse — Product Requirements (v1.0)

## Summary
TeamPulse is an **async daily standup** tool for small distributed engineering teams. Instead of a synchronous
meeting, each member answers three prompts on their own schedule; TeamPulse assembles a single daily digest the whole
team reads in under two minutes.

## Problem & user
- **Problem:** distributed teams lose 3–4 hours/week to standup meetings scheduled across timezones; people in the
  wrong timezone either lose sleep or skip and fall out of sync.
- **Primary user:** an engineer on a 4–12 person distributed team (the "member").
- **Secondary user:** the team lead who configures the team and reads the digest first (the "lead").
- **Job to be done:** *When my team is spread across timezones, I want to share and absorb daily status without a
  meeting, so I can stay in sync without losing focus time.*

## Capabilities

### Standups
- A member can submit a daily standup answering three prompts: yesterday, today, blockers.
- A member can edit their standup until the daily digest is generated; after that it is locked.
- A member can mark a blocker as "needs help", which flags it in the digest.

### Team
- A lead can create a team and invite members by email.
- A lead can set the team's digest time and timezone.
- A member can join a team via an invite link and set their own display name.

### Digest
- TeamPulse generates one daily digest at the team's configured time, grouping entries by member.
- The digest surfaces all "needs help" blockers in a dedicated section at the top.
- A member can read the current and past digests for any day.

## Constraints (non-negotiable)
- **Stack:** TypeScript + Node; PostgreSQL. (The team has committed to this.)
- **Hosting:** single VPS via Docker; EU region only (data residency).
- **Auth:** email magic-link only — no passwords, no third-party SSO in v1.
- **Scale:** ≤ 50 teams, ≤ 600 members total; not a concern beyond that for v1.

## Scope
- **In scope (v1):** the three capability areas above.
- **Out of scope (v1):** Slack/Teams integration, analytics dashboards, mobile apps, paid plans/billing.

## Success criteria
- A member can submit a standup and see it in that day's digest.
- A lead can stand up a new team and have members contributing within one day, with no training.
- The daily digest reads top-to-bottom in under two minutes for a 12-person team.
