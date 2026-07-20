# Architecture Constraints — TeamPulse

> **Declaration-truth for technical mandates.** The architecture facts the **user** requires. Owned by **skill 00
> (discovery)**. Skill 03 (architect) **realizes** these into `system.md` / ADRs / specs that *reference* them. Only
> the user can relax a stated mandate; an expert skill that disagrees raises a **Tier-2 amendment** (single gate +
> ADR), never a silent change.

## Stack mandates

> Only what the user actually committed to. The team has committed to this stack.

- **Language / runtime:** TypeScript + Node.
- **Framework(s):** agnostic — architect's choice (none stated).
- **Datastore:** PostgreSQL.
- **Key libraries / services the user named:** none named beyond the above.

## Hosting & infrastructure

- **Deploy target:** single VPS via Docker.
- **Regions / data residency:** EU region only (data residency requirement).
- **CI/CD or ops constraints:** none stated — architect's choice.

## Compliance & security mandates

- **Data residency:** all data resides in the EU.
- **Authentication:** email magic-link only — no passwords, no third-party SSO in v1. (See Constitution item 5 and
  REQ-007.)

## Scale & performance

- **Expected load:** ≤ 50 teams and ≤ 600 members total. Beyond this is explicitly not a v1 concern.
- **Hard performance targets:** none stated as a system metric. Note the product-level bar (Constitution item 2):
  the daily digest reads top-to-bottom in under two minutes for a 12-person team — a UX target skill 02 realizes,
  recorded here for traceability.

## Integrations

- **None in v1.** Slack/Teams integration is explicitly out of scope (see charter).
