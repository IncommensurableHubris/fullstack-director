# Architecture Constraints — Aurora

> **Declaration-truth for the technical envelope.** Owned by **skill 00 (discovery)**. Skill 03 (architect)
> **realizes** within these and may only **propose changes via amendment** (Tier-2 gate + ADR). Most of the stack is
> deliberately *unstated* at discovery — it is 03's to decide.

## Stated constraints

- **Local-first, no backend.** v1 stores all data on the user's own device; there is no server, account, or cloud
  sync. (Constitution item 1.) `stated`

## Deferred to architecture (03)

- Specific storage mechanism, framework, and packaging — **not yet decided**; 03 chooses and records an ADR.
