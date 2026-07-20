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

## Data architecture

> Declaration-truth for Beacon's data needs. The `Data:` line in `specification.md` routes these to skill 03's
> data modules; the need-gate still decides whether each module is warranted (03's data craft, §0).

- **Reference handbook (candidate for `retrieval(handbook-lookup)`):** operators keep a small internal source
  handbook — ~40 short, stable reference documents, revised roughly quarterly — that a research run may consult.
  It fits comfortably in a model context window and sees low query volume.
- **Cross-session learning (candidate for `memory`):** each research question is independent and self-contained.
  Operators explicitly value a from-scratch read on every question (reproducibility of the research method); no
  personalization, no repeat-topic learning, and no cross-session accumulated state is wanted.
