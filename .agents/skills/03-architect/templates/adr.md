<!-- Filename: docs/architecture/adr/ADR-NNN.md  (zero-padded: ADR-001, ADR-002, … ADR-010). -->

# ADR-NNN: <short decision title>

> **A decision record — MADR 4.0 + the Binds/Prevents/Rule discipline.** Owned by **skill 03 (architect)**, the
> **sole `ADR-NNN` allocator** (next id = `max` in [`README.md`](README.md) **+ 1**). ADRs are **immutable**: to
> change a decision, write a new ADR that **supersedes** this one — never rewrite. The **Rule** is what makes this
> enforceable (a `static-conformance` Verification-Contract row can execute it). Method: `references/reconcile-architecture.md`.

- **Status:** _<Proposed | Accepted | Superseded by ADR-NNN>_
- **Category:** _<classic | memory | model-binding | topology | durability | isolation | observability>_  ← `classic` for a webapp decision; the agentic categories apply under `Profile: agent-system` (see `references/reconcile-architecture.md`). A **`topology`** ADR (single vs orchestrator-worker vs handoff vs swarm) MUST carry the ~15× token-economics justification.
- **Satisfies:** _<REQ-NNN | architecture-constraints "<field>" | Constitution item N>_  ← what declaration this serves
- **Supersedes:** _<ADR-NNN | none>_
- **Resolves amendment:** _<AMD-NNN | n/a>_  ← set when this ADR is the tech-mandate partner of an approved Tier-2 amendment
- **Verified-against:** _<docs/verification/&lt;tech&gt;.md (&lt;tech&gt;@&lt;version&gt;) | n/a>_  ← **on-demand(verify-live)**: **required** when the Decision below names a spine-declared verify-live tech (`architecture-constraints.md` § Verify-live) — cite the live-source record its API/config was verified against; else `n/a` (`shared/live-source-verification.md`; graded S18)
- **Review-Trigger:** _<the symptom-based condition that reopens this decision — observable ("autovacuum lag exceeds X", "recall@5 below floor two runs straight"), never "review periodically">_  ← framework-original field; required by DA-T04 for datastore decisions, recommended for every data-class ADR

## Context & Problem Statement

<!-- The forces at play, in 2–4 sentences. What decision has to be made, and why now? Reference the driving REQ /
     constraint by ID. If this ADR resolves a Reconcile Tier-2 conflict, state the contradiction it settles. -->

## Decision Drivers

- _<driver — e.g. a stated constraint, a §10 quality scenario, a REQ>_
- _<driver>_

## Considered Options

1. **_<Option A>_** — _<one line>_
2. **_<Option B>_** — _<one line>_
3. **_<Option C>_** — _<one line>_

## Decision Outcome

**Chosen:** _<Option X>_, because _<the decisive driver>._

> The **Decision** names the concrete technology/approach — this is the field the reconciler's **token-in-named-field
> check** reads. Be specific (`PostgreSQL 16`, not "a relational database").

- **Binds:** _<what this commits the build to — the constraint/REQ it satisfies>._
- **Prevents:** _<what it rules out — the alternatives now closed>._
- **Rule (Confirmation — how we enforce it):** _<a checkable statement a lint / test / grep can decide — e.g. "no
  module under `domain/` imports from `infra/`"; "the datastore driver is client-server, not embedded". A Rule that
  can't be checked is a weak ADR — sharpen it.>_

## Consequences

- **Positive:** _<what becomes easier/possible>._
- **Negative (the tradeoff — every decision has one):** _<what becomes harder; the sacrifice accepted>._
- **Risks:** _<what a key quality scenario is now sensitive to — ATAM risk>._

## Related

- _<ADR-NNN — related decision · docs/architecture/specs/<feature>.md — where the Rule is verified>_
