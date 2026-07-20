# Architecture Constraints — Beacon

> Declaration-truth for technical mandates. Owned by skill 00; skill 03 realizes these into ADRs.

## Stack mandates

- **Language / runtime:** agnostic — architect's choice.
- **Model:** agnostic — architect's choice (record the binding as an ADR).

## Hosting & infrastructure

- **Regions / data residency:** agnostic.

## Scale & performance

> **Boundary (S8):** the single home for quantified latency / throughput NFRs. The agent-contract's cost envelope
> references these targets.

- **Expected load:** a research question may span **10–30 independent sources**; coverage must not serialize.
- **Hard performance targets:** p95 end-to-end research < 3 minutes for a 15-source question.

## Compliance & security mandates

- Read-only external access; no external writes.
