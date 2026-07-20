# Architecture Constraints — Beacon Research Agent

## Stack mandates

- **Language / runtime:** TypeScript + Node.
- **Framework(s):** OpenClaw (the agent host framework).

## Verify-live

> Technologies too new for reliable training-data recall — live-source-verify + record before use.
> See shared/live-source-verification.md.

- **openclaw:** docs: https://openclaw.dev/docs · source: https://github.com/example/openclaw

## Scale & performance

- **Expected load:** ≤ 100 research queries/day.
