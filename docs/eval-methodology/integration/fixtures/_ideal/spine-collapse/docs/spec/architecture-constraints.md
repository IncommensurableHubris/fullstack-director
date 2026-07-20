# Architecture Constraints — TeamPulse

> **Declaration-truth for technical mandates.** Owned by **skill 00 (discovery)**. Skill 03 (architect)
> **realizes** these into `system.md` / ADRs / specs that *reference* them.

## Stack mandates

- **Language / runtime:** TypeScript + Node.
- **Framework(s):** agnostic — architect's choice (none stated).
- **Datastore:** PostgreSQL (client-server; shared by all app instances and the worker). <!-- amended AMD-001. -->
- **Key libraries / services the user named:** none named beyond the above.

## Hosting & infrastructure

- **Deploy target:** containerized (Docker).
- **Availability (stated):** the web API runs as **two or more stateless instances behind a load balancer**, and the
  daily digest generator runs as a **separate always-on worker process**. All app instances **and** the worker
  **share one datastore**.
- **Regions / data residency:** EU and US regions — EU teams' data in the EU, US teams' data in the US (per-region isolation). <!-- PIVOTED via AMD-004 (was "EU region only"); the JTBD is unchanged, only this hosting constraint moved. -->
- **CI/CD or ops constraints:** none stated — architect's choice.

## Compliance & security mandates

- **Data residency:** each team's data resides in its home region (EU or US) — per-region isolation. <!-- AMD-004. -->
- **Authentication:** email magic-link only — no passwords, no third-party SSO in v1.

## Scale & performance

- **Expected load:** ≤ 50 teams and ≤ 600 members total. Beyond this is explicitly not a v1 concern.
- **Hard performance targets:** none stated as a system metric.

## Integrations

- **None in v1.**
