# Architecture Constraints — TeamPulse (HTTP API slice)

> **Declarations (spine).** User mandates on stack, hosting, compliance, scale. Owned by **skill 00 (discovery)**;
> `03`/`08` may only *amend* through a Tier-2 gate (+ a resolving ADR). A code↔doc drift is corrected locally; a
> realization that **cannot honor a stated constraint** is a declaration contradiction — surfaced through the
> amendment protocol, never silently changed.

## Stack

- **Language / runtime:** plain Node.js (LTS ≥ 20) — no transpile step.
- **HTTP:** the built-in `node:http` server — **zero runtime dependencies** by mandate. Tests use `node:test`.
- **Auth:** email **magic-link** sessions only (Constitution §5) — no passwords, no third-party SSO. Session tokens
  are server-issued and **server-verified**.
- **Datastore:** **in-memory (embedded, single-process)** — no external database server.

## Scale & deployment

- **Horizontal scale (stated, sprint-02 mandate):** the API runs as **multiple stateless instances behind a load
  balancer**. Any given request may land on any instance; no request affinity is guaranteed.

## Data & compliance

- **Data residency:** EU region for all persisted data.
- **Data sensitivity:** **medium** — personal standup content + member identities + team membership. Confidential,
  not regulated (no financial/health/PII-of-record). Per-team access isolation is a **MUST** (REQ-020, Constitution §6).

## Secrets

- The service reads secrets (the session-signing key, any channel webhook credentials) from the **environment**.
  Values live in the local env store (`.env`, gitignored) and are **never** committed or written into source or docs —
  code and documents record the variable **name** only.
