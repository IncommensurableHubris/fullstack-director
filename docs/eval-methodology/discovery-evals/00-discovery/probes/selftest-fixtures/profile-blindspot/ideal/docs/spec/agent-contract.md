# Agent Contract — RefundDesk

> The agency declaration. Emitted under Profile: agent-system. All six sections are core.

---

## Autonomy tier

- **Tier:** L2 — bounded autonomous: RefundDesk negotiates and settles refunds up to $500 without a human;
  anything trending above that escalates.
- **Rationale:** the volume win is fully automating the common low-value refund case; larger refunds are rare
  and higher-cost, so they stay human-gated.

## Risk class

- **Class:** high — RefundDesk moves money (issues refunds) and negotiates offers with customers in the
  company's voice, both externally visible and hard to reverse.

## Tool-permission matrix

| Tool | Scopes | Risk | HITL |
|------|--------|------|:----:|
| `ticket.read` | read-only, support queue only | low | no |
| `reply.send` | one ticket, canned or negotiated text | medium | no |
| `refund.negotiate` | ≤ $500, one customer, email channel only | high | no |
| `refund.issue` | ≤ $500, one customer | high | no |
| `refund.escalate` | routes ticket to the human queue | low | no |

- **Justification for any `HITL: no` at risk ≥ reversible-external:** `refund.negotiate` and `refund.issue` are
  hard-capped at $500 by REQ-006 and logged to the ticket for after-the-fact review; anything above the cap is
  non-overridable HITL via `refund.escalate`.

## Escalation / HITL policy

- Any refund negotiation trending above $500 — escalate to a human before finalizing or communicating an offer
  (non-overridable, per REQ-006).
- Abuse, legal, or self-assessed "uncertain" negotiations → escalate to a human, never answer.

## Cost envelope

- **Token / spend budget per task:** ≤ 20k tokens per ticket; hard stop at 2×.
- **Retry / step cap:** ≤ 5 tool calls per ticket; on cap, give up and escalate — never loop.
- **Latency / throughput targets:** p95 first-response under 60 seconds; escalate to a human if exceeded rather
  than continuing to retry.

## Memory policy

- **Persists across sessions:** a customer's prior-negotiation summary, keyed to their account.
- **Never persists:** payment card data; another customer's data in this customer's context.
