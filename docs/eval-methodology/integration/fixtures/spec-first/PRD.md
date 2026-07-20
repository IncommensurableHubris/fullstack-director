# TeamPulse — Product Requirements (v1.0)

<!--
  INTEGRATION-EVAL SEED (case: spec-first). This is the COMPREHENSIVE spec fed to `00 intake` at the head of the
  chain 00 -> 01 -> 02 -> 03 -> /status. It is the clean-PRD TeamPulse domain the unit evals share, with two
  deliberate properties:

  (1) THE LATENT TIER-2 PLANT (surfaces at 03's Reconcile, not before). The Constraints below mandate SQLite
      (embedded, single-file) AS WELL AS a multi-instance, load-balanced web tier + a separate worker that all
      "share one datastore". Each reads as a valid user declaration; together they are a COMPUTED contradiction (an
      embedded single-file DB cannot be shared across instances/processes). 00 records both faithfully (it is not
      00's to resolve); 01/02 are datastore-agnostic; 03 catches SQLite-vs-shared-store, gates a Tier-2 amendment,
      and records a resolving ADR (client-server DB). This is the cross-skill discriminator.

  (2) DECISIVE (marker-free) on the two points the unit-eval spine left as [NEEDS CLARIFICATION], so 00 produces a
      marker-free spine and the only governance event is the RESOLVED Tier-2 -> /status routes to /04-builder. (The
      `governance` case reintroduces a deferred amendment + a surviving marker on purpose.) The decisive resolutions
      are flagged inline below.
-->

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
- A member can edit their standup until the daily digest is generated; **at the team's configured digest time the
  day locks for everyone** (a single team-wide lock instant — not per-member, not per-timezone). _(decisive: resolves
  the edit-lock timezone question — one lock moment for the whole team.)_
- A member can mark a blocker as "needs help", which flags it in the digest.

### Team
- A lead can create a team and invite members by email.
- A lead can set the team's digest time and timezone.
- A member can join a team via an invite link and set their own display name.

### Digest
- TeamPulse generates one daily digest at the team's configured time, grouping entries by member.
- **A member who did not submit before generation is omitted from that day's digest** (no placeholder row, no
  "missing" marker — the digest shows only real entries). _(decisive: resolves the non-submitter representation
  question — omit.)_
- The digest surfaces all "needs help" blockers in a dedicated section at the top.
- A member can read the current and past digests for any day.

## Constraints (non-negotiable)
- **Stack:** TypeScript + Node; **SQLite (embedded, single-file; no external database server).** (The team has
  committed to this.)
- **Availability:** the web API runs as **two or more stateless instances behind a load balancer** (no single point
  of failure for the web tier), and the daily digest generator runs as a **separate always-on worker process**. All
  app instances **and** the worker **share one datastore.**
- **Hosting:** containerized (Docker); EU region only (data residency).
- **Auth:** email magic-link only — no passwords, no third-party SSO in v1.
- **Scale:** ≤ 50 teams, ≤ 600 members total; not a concern beyond that for v1.

## Scope
- **In scope (v1):** the three capability areas above.
- **Out of scope (v1):** Slack/Teams integration, analytics dashboards, mobile apps, paid plans/billing.

## Success criteria
- A member can submit a standup and see it in that day's digest.
- A lead can stand up a new team and have members contributing within one day, with no training.
- The daily digest reads top-to-bottom in under two minutes for a 12-person team.
