# Architecture Constraints — <Project Name>

> **Declaration-truth for technical mandates.** The architecture facts the **user** requires — stack they've
> committed to, where it must run, what it must comply with, the scale it must hold. Owned by **skill 00
> (discovery)**. Skill 03 (architect) **realizes** these into `system.md` / ADRs / specs that *reference* them.
>
> **Challenge flow:** when an expert skill disagrees with a constraint (e.g. "SQLite won't hold this write load →
> PostgreSQL"), it does **not** silently change it. Its Reconcile step raises a **Tier-2 amendment** → a single
> user gate → on approval the amendment updates the constraint **here** *and* a new **ADR** records the
> realization decision (one trigger, two altitudes). Only the user can relax a stated mandate.

## Stack mandates

> Only what the user actually committed to. If they were agnostic, write "agnostic — architect's choice" so skill
> 03 knows it's free to decide (and need not gate).

- **Language / runtime:** _<e.g., "TypeScript / Node" — or "agnostic">_
- **Framework(s):** _<…>_
- **Datastore:** _<…>_
- **Key libraries / services the user named:** _<…>_

## Verify-live

> **on-demand — declare only technologies too new for reliable training-data recall** (a just-released framework,
> a pre-1.0 library, an in-house SDK the model has never seen; for an `agent-system` adapting OpenClaw / Hermes
> Agent / NanoClaw, the **host framework**). For each, the model MUST live-source-verify its API/config and record
> it in `docs/verification/<tech>.md` **before** designing or building against it — **06 G11 gates the ship** on
> that record, `verify-spine.py` **L7** stands guard. **Omit this section entirely for a stack of stable,
> well-known technologies** — no ceremony where the model is reliable. Adding or changing the set is a **Tier-2
> amendment** (a named-technology decision). Full doctrine: `shared/live-source-verification.md`.

- **<tech-slug>:** docs: _<canonical doc URL>_ · source: _<repo URL>_
  <!-- <tech-slug> is the record basename — this row ↔ docs/verification/<tech-slug>.md. No version pin here: a
       version *mandate* belongs in Stack mandates / Integrations; the *verified* version lives in the record. -->

## Hosting & infrastructure

- **Deploy target:** _<e.g., "Coolify on a single VPS"; "Vercel">_
- **Regions / data residency:** _<e.g., "EU only">_
- **CI/CD or ops constraints:** _<…>_

## Compliance & security mandates

- _<e.g., "GDPR; SOC 2 roadmap; PII encrypted at rest.">_
- **ASVS target level:** L1 _<the OWASP **ASVS 5.0** verification bar 07 audits against. **Default L1** — the realistic
  solo bar (modern framework defaults + targeted hardening already meet most of it). **L2 only with a recorded
  justification** (sensitive / regulated data) — a Tier-2 decision the user gates. Absent ⇒ L1.>_

## Scale & performance

> **Boundary (S8):** this section is the **single home for quantified latency / throughput NFRs** (measured
> performance targets). Under `Profile: agent-system`, the agent-contract's cost envelope keeps token/spend budgets +
> retry caps and **references** these targets — it does not restate them.

- **Expected load:** _<e.g., "≤500 daily users; spiky at month-end.">_
- **Hard performance targets:** _<e.g., "dashboard TTI < 2s on 3G." · agent: "p95 first-response < 60s.">_

## Integrations

- _<external systems that must be integrated, with any fixed protocols/versions>_
