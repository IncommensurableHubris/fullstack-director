# Architecture Constraints — TeamPulse (digest slice)

> **Declarations (spine).** User mandates on stack, hosting, compliance, scale. Owned by **skill 00 (discovery)**;
> `03` may only *amend* (Tier-2 gate + ADR). `06-release` resolves its deployment platform from here first.

## Stack

- **Language / runtime:** plain Node.js (LTS ≥ 20) — no transpile step.
- **Dependencies:** zero runtime dependencies; tests use the built-in `node:test` runner.

## Compliance

- **Data residency:** EU region for all persisted data (a later hosting concern for this headless slice).

## Deployment (mandated)

- **Platform:** the repo-local **stand-in platform** under `scripts/` (this project ships as a deployable module;
  the stand-in is the mandated target for this slice):
  - deploy — `node scripts/deploy.js` (publishes the built slice to `_deploy/live/`)
  - health — `node scripts/health.js` (liveness + readiness; exit 0 = healthy)
  - smoke — `node scripts/smoke.js` (critical flows against the deployed copy; exit 0 = pass)
- **Secrets:** the platform reads the environment variable **`TEAMPULSE_API_TOKEN`**. Its **value** lives in the
  local env store (`.env`, gitignored) and is **never** committed or written into docs — documents record the
  variable **name** only.
