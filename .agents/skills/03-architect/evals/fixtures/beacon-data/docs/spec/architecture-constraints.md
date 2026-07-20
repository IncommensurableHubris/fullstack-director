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
> data modules; skill 03 realizes each into ADRs/specs (it does not decide *whether* — the need below is stated here).

- **Retrieval corpus (drives `retrieval(source-search)`):** Beacon maintains a **persistent semantic index** of
  previously-fetched source content. A worker queries this index before re-fetching, and newly-fetched sources
  are added to it continuously — so the corpus **grows daily-plus** and its contents age. Retrieval quality is
  measured on the versioned golden query set that already backs REQ-002.
- **Learned memory (drives `memory`):** Beacon persists **per-topic source-reliability signals** across sessions
  — which sources proved authoritative for which subject areas — so worker routing and grounding **improve on
  repeat questions in the same domain**. These signals are **operator-correctable**, and raw fetched content is
  not memory (it lives in the retrieval index cache under its own freshness policy).
- **Operator profiles (drives `memory`):** per-operator research-interest profiles personalize source routing on
  repeat use. Profiles are personal data, and operators **may request deletion of their profile**.
