# Agent Contract — TeamPulse Agent

## Autonomy tier

Tier 2 — proposes actions; executes read-only tools autonomously, mutations require confirmation.

## Risk class

Medium — reads team data; one irreversible tool (send_message).

## Tool-permission matrix

| Tool | Scopes | Risk | HITL |
|------|--------|------|------|
| search_docs | read: team corpus | low | no |
| send_message | write: team channel | high | yes |

## Escalation / HITL policy

Any irreversible tool (`send_message`) requires human confirmation; the HITL gate is non-overridable.

## Cost envelope

≤ 8 tool calls / turn; ≤ 20k tokens / turn; references the latency targets in `architecture-constraints.md`.

## Memory policy

Per-team memory isolation; untrusted content is never written to persisted memory without validation.
