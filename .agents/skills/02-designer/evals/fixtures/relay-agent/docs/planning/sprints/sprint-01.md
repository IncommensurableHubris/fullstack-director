---
sprint: 01
---

# Sprint 01 — Relay walking skeleton

> The thinnest agent loop end-to-end, **with tracing and the eval harness wired** (the walking skeleton for an
> `agent-system`, per shared/agentic-profile.md). Design the agent-experience for the in-scope REQs.

## In scope

| REQ | Name |
|-----|------|
| REQ-001 | Classify and draft a reply for each new ticket |
| REQ-002 | Send low-risk replies autonomously |
| REQ-003 | Refuse to send an ungrounded reply |
| REQ-004 | Refuse to execute a refund without human approval |

## Done when

- A new ticket is classified and a grounded reply is drafted (REQ-001).
- A simple how-to reply is sent without a human (REQ-002); an ungrounded one is refused and escalated (REQ-003).
- A refund is never executed without human approval (REQ-004) — the HITL touchpoint is exercised.
