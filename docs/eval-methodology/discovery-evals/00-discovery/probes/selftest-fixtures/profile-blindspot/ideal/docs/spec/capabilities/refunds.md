<!-- budget: ≤25 lines per REQ block — one home per fact; detail is realization, not spine. -->

# Capability: Refunds

> Refund resolution for tickets tagged as refund requests. The negotiation itself is an autonomous agent
> action — see [`../agent-contract.md`](../agent-contract.md) for the agency declaration. Each REQ is a
> delimited block per [`../specification.md`](../specification.md).

### REQ-005: Negotiate and settle refunds under $500 automatically   (MUST)

WHEN a customer requests a refund by email, the system SHALL negotiate and settle a refund amount with the
customer up to $500 without staff involvement, logging the exchange to the ticket like any other reply.

**Acceptance (outcome-level):**
```gherkin
Given a customer emails a refund request
When the negotiated amount is $500 or less
Then RefundDesk settles the refund with the customer and logs the exchange to the ticket
```
<!-- source: "For refund requests specifically, the system automatically negotiates refund amounts with customers over email up to $500 without staff involvement, using an LLM; the exchange is logged to the ticket like any other reply." -->
<!-- /REQ-005 -->

### REQ-006: Escalate any refund negotiation over $500 to a human   (MUST)

IF a refund negotiation would settle at an amount exceeding $500, THEN the system SHALL escalate the ticket to
a human agent and SHALL NOT finalize or communicate an offer above the cap.

**Acceptance (outcome-level):**
```gherkin
Given a refund negotiation is trending toward an amount over $500
When RefundDesk evaluates the next offer
Then it does not send that offer and instead escalates the ticket to a human agent
```
<!-- source: "inferred from the $500 autonomy cap plus Constitution item 3 — the cap is only meaningful if crossing it is a hard stop, not a soft target" -->
<!-- /REQ-006 -->
