# Architecture Constraints — TeamPulse (HTTP API slice)

> **Declarations (spine).** User mandates on stack, hosting, compliance, scale. Owned by **skill 00 (discovery)**;
> `03` may only *amend* (Tier-2 gate + ADR). The security audit reads these for data-sensitivity + compliance context.

## Stack

- **Language / runtime:** plain Node.js (LTS ≥ 20) — no transpile step.
- **HTTP:** the built-in `node:http` server — **zero runtime dependencies** by mandate. Tests use `node:test`.
- **Auth:** email **magic-link** sessions only (Constitution §5) — no passwords, no third-party SSO. Session tokens
  are server-issued and **server-verified**.

## Data & compliance

- **Data residency:** EU region for all persisted data.
- **Data sensitivity:** **medium** — personal standup content + member identities + team membership. Confidential,
  not regulated (no financial/health/PII-of-record). Per-team access isolation is a **MUST** (REQ-020, Constitution §6).

## Secrets

- The service reads secrets (the session-signing key, any channel webhook credentials) from the **environment**.
  Values live in the local env store (`.env`, gitignored) and are **never** committed or written into source or docs —
  code and documents record the variable **name** only.
