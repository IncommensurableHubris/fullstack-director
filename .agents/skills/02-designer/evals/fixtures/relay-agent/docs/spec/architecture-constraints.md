# Architecture Constraints — Relay

> Declaration-truth for technical mandates. Owned by skill 00; skill 03 realizes these into ADRs that reference them.

## Stack mandates

- **Language / runtime:** agnostic — architect's choice.
- **Key services the user named:** Zendesk (support inbox), Stripe (refunds), Slack (escalation).

## Hosting & infrastructure

- **Regions / data residency:** EU only.

## Scale & performance

> **Boundary (S8):** the single home for quantified latency / throughput NFRs. The agent-contract's cost envelope
> references these targets; it does not restate them.

- **Hard performance targets:** p95 first-response (at least an acknowledgement) < 60s.

## Compliance & security mandates

- EU data residency; no customer data leaves the EU region.
