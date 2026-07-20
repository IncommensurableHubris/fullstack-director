# Specification — PennyPilot

> **The spec spine: the single source of declaration-truth.** This file is the **INDEX**. It holds the project
> **Constitution** (non-negotiables) and the **REQ registry** (the authoritative ID→file map). Detailed
> requirements live in [`capabilities/`](capabilities/) `<domain>.md` files. Owned by **skill 00 (discovery)**;
> every other skill *references* REQ-IDs from here.

---

## Constitution (PROTECTED)

> Project-level non-negotiables. On any product/scope question, the Constitution **wins**. Keep to **3–7** durable
> statements.

1. **Read-only by design.** PennyPilot observes and categorizes; it never moves money, initiates a payment, or
   writes to a connected account.
2. **Every number is traceable.** Any figure shown to the user must trace back to a specific source transaction.
3. **The account connection is the root.** Nothing in the product is meaningful until the user has connected at
   least one bank account; all spending data derives from that connection.

---

## REQ registry

> The **authoritative** ID→file map — every REQ appears here **exactly once**, organized **by domain** (not build
> order). Skill 00 bootstrapped these IDs; **skill 01 (planner) is the sole allocator** thereafter.

| REQ | Name | Priority | Status | File |
|-----|------|----------|--------|------|
| REQ-001 | See a monthly spending summary | MUST | stated | capabilities/insights.md |
| REQ-002 | Set a category budget and get alerted | SHOULD | stated | capabilities/insights.md |
| REQ-003 | Categorize a transaction | MUST | stated | capabilities/transactions.md |
| REQ-004 | Split a transaction across categories | SHOULD | stated | capabilities/transactions.md |
| REQ-005 | Connect a bank account | MUST | stated | capabilities/accounts.md |

- **Priority** — RFC 2119: `MUST` / `SHOULD` / `MAY`. Drives MoSCoW → sprint assignment in skill 01.
- **Status** — `stated` (traces to a user source quote) or `derived` (inferred). All five here are `stated`.

---

## Pointers

- **Architecture constraints** → [`architecture-constraints.md`](architecture-constraints.md).
- **Amendment log** → [`amendment-log.json`](amendment-log.json) — structured change history (git is the dated trail).

---

## REQ block contract (how each `capabilities/<domain>.md` requirement is written)

Each requirement is a **delimited block** so an amendment can target a findable, replaceable span:

````
### REQ-NNN: <name>   (MUST|SHOULD|MAY)

<one-line statement of the capability>

**Acceptance (outcome-level):**
```gherkin
Given <context>
When <user-observable action>
Then <user-observable outcome>
```
<!-- source: "<verbatim quote — or `inferred`>" -->
<!-- /REQ-NNN -->
````

The Gherkin here is **outcome-level**. Detailed UI-specific steps are realization (skill 03's Verification
Contracts), not here.
