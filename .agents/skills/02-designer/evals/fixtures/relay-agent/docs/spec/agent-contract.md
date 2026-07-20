# Agent Contract — Relay

> The agency declaration. Emitted under Profile: agent-system. All six sections are core.

---

## 1 · Autonomy tier

- **Tier:** L3 — approver: Relay drafts and sends low-risk replies autonomously; a human approves anything that moves money or that Relay flags uncertain.
- **Rationale:** the volume win is in autonomous low-risk replies; money movement and abuse are rare and high-cost, so they stay human-gated.

## 2 · Risk class

- **Class:** high — Relay can issue refunds (moves money, externally visible, hard to reverse) and reply to customers in the company's voice.

## 3 · Tool-permission matrix

| Tool | Scopes | Risk | HITL |
|------|--------|------|:----:|
| `inbox.read` | read-only, support queue only | low | no |
| `kb.search` | read-only, help center | low | no |
| `reply.send` | one ticket, grounded text only | medium | no |
| `refund.issue` | ≤ last payment, one customer | high | **yes** |
| `slack.escalate` | `#support-escalations` only | low | no |

- **Justification for any `HITL: no` at risk ≥ reversible-external:** `reply.send` is grounded-only (enforced by REQ-003) and one-ticket-scoped; all other autonomous tools are read-only.

## 4 · Escalation / HITL policy

- Any refund or payment — a human approves before execution (non-overridable).
- Abuse, legal, or self-assessed "uncertain" → escalate to a human, never answer.

## 5 · Cost envelope

- **Token / spend budget per task:** ≤ 40k tokens per ticket; hard stop at 2×.
- **Retry / step cap:** ≤ 6 tool calls per ticket; on cap, give up and escalate — never loop.
- **Latency / throughput targets:** see [`architecture-constraints.md`](architecture-constraints.md) § Scale & performance (p95 first-response < 60s).

## 6 · Memory policy

- **Persists across sessions:** a customer's prior-ticket summary, keyed to their account.
- **Never persists:** payment card data; another customer's data in this customer's context.
