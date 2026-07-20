# Architecture Constraints — TeamPulse

> **Declaration-truth for technical mandates** the **user** committed to. Owned by **skill 00**. Skill 03 **realizes**
> these into `system.md` / ADRs that *reference* them; only the user may relax a stated mandate (Tier-2 amendment +
> ADR). Everything here is `stated` unless marked `derived`.

## Stack mandates

- **Language / runtime:** TypeScript + Node. _(stated — "The team has committed to this.")_
- **Framework(s):** agnostic — architect's choice (the PRD names none).
- **Datastore:** PostgreSQL. _(stated — committed.)_
- **Key libraries / services the user named:** none.

## Hosting & infrastructure

- **Deploy target:** single VPS via Docker. _(stated)_
- **Regions / data residency:** EU region only. _(stated — data residency.)_
- **CI/CD or ops constraints:** not specified — architect's choice.

## Compliance & security mandates

- **Authentication:** email magic-link only — no passwords, no third-party SSO in v1. _(stated; realized by REQ-011.)_
- **Data residency:** all data stored and processed in the EU only. _(stated; Constitution item 3.)_
- **Tenant isolation:** one team's standups and digest are private to that team. _(derived — REQ-012; confirm.)_

## Scale & performance

- **Expected load:** ≤50 teams and ≤600 members total for v1; larger scale is out of scope. _(stated)_
- **Hard performance targets:** none stated as a system latency budget. The "under two minutes to read" figure is a
  digest-legibility goal (see `design-intent.md`), not a server-side target.

## Integrations

- None in v1 — Slack/Teams integration is explicitly out of scope.
