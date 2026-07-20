# Architecture Constraints

> User-declared architecture mandates (a **declaration** — 03 may only *amend* via a gated Tier-2 + a resolving ADR).
> Owned by 00.

- **Runtime:** Node.js (LTS), no framework — the standard library HTTP server.
- **Datastore:** PostgreSQL (client-server, EU-hosted) — a shared store for multiple app instances.
- **Region:** EU only (Constitution §4 — data residency).
- **Auth:** email magic-link sessions only — no passwords, no third-party SSO (Constitution §5).
- **Scale:** two or more stateless app instances behind a load balancer + a separate always-on digest worker.
