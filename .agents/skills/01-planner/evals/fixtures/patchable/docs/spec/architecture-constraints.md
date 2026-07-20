# Architecture Constraints — TeamPulse

> **Declaration-truth for technical mandates.** Owned by **skill 00 (discovery)**. Skill 03 (architect)
> **realizes** these into `system.md` / ADRs / specs that *reference* them. Only the user can relax a stated
> mandate; an expert skill that disagrees raises a **Tier-2 amendment** (single gate + ADR), never a silent change.

## Stack mandates

- **Language / runtime:** TypeScript + Node.
- **Framework(s):** agnostic — architect's choice (none stated).
- **Datastore:** PostgreSQL (client-server; shared by all app instances and the worker). <!-- amended AMD-001: was
  "SQLite (embedded, single-file; no external database server)" — see amendment-log.json + ADR-001. -->
- **Key libraries / services the user named:** none named beyond the above.

## Hosting & infrastructure

- **Deploy target:** containerized (Docker).
- **Availability (stated):** the web API runs as **two or more stateless instances behind a load balancer** (no
  single point of failure for the web tier), and the daily digest generator runs as a **separate always-on worker
  process**. All app instances **and** the worker **share one datastore**.
- **Regions / data residency:** EU region only (data residency requirement).
- **CI/CD or ops constraints:** none stated — architect's choice.

## Compliance & security mandates

- **Data residency:** all data resides in the EU.
- **Authentication:** email magic-link only — no passwords, no third-party SSO in v1. (See Constitution item 5 and
  REQ-007.)

## Scale & performance

- **Expected load:** ≤ 50 teams and ≤ 600 members total. Beyond this is explicitly not a v1 concern.
- **Hard performance targets:** none stated as a system metric. The product-level bar (Constitution item 2) — the
  daily digest reads top-to-bottom in under two minutes for a 12-person team — is a UX target skill 02 realizes.

## Integrations

- **None in v1.** Slack/Teams integration is explicitly out of scope (see charter).
