---
verified_against: openclaw@0.4.2
docs_fetched:
  - https://openclaw.dev/docs/agents#loop
  - https://github.com/example/openclaw/blob/v0.4.2/src/agent.ts
---

# Verification record — OpenClaw

The live-source ledger for OpenClaw (a verify-live tech). Seeded by /00-discovery, appended by /03 and /04. See
`shared/live-source-verification.md`.

## Verified claims

| claim (an API/config/behavior fact) | citation | corrects |
|--------------------------------------|----------|----------|
| the agent loop entry point is `Claw.run(task)` | https://openclaw.dev/docs/agents#loop | assumed `Claw.start()` from memory — the docs show `Claw.run` |
| a tool is registered via `claw.tool({name, run})` | example/openclaw@v0.4.2:src/agent.ts#L88 | — |
