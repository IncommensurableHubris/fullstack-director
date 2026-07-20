# Capability: Accounts

> **The foundation.** A user connects a bank account; PennyPilot imports its transactions read-only. Nothing else in
> the product is meaningful until this exists — the transactions and insights layers both derive from a connected
> account. (Note: this domain sorts *last* in the registry, but it must be built *first*.) The REQ is a delimited
> block per the contract in [`../specification.md`](../specification.md).

### REQ-005: Connect a bank account   (MUST)

Before any transactions can be imported or categorized, a user must connect at least one bank account; PennyPilot
then imports that account's transactions read-only.

**Acceptance (outcome-level):**
```gherkin
Given a new user who has not yet connected any account
When they connect a bank account through the read-only aggregation flow
Then their transactions are imported and available to categorize
```
<!-- source: "Brief: 'Step one is always connecting a bank account read-only; everything flows from there.'" -->
<!-- /REQ-005 -->
