<!-- budget: ≤25 lines per REQ block — one home per fact; detail is realization, not spine. -->

# Capability: Refunds

> Refund resolution for tickets tagged as refund requests. Each REQ is a delimited block per
> [`../specification.md`](../specification.md).

### REQ-005: Settle refunds under $500 automatically   (MUST)

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
