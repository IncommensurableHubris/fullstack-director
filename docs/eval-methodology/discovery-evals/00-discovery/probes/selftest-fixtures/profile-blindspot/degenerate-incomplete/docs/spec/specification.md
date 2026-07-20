# Specification — RefundDesk

> The spec spine — Constitution + REQ registry. Detailed requirements live in `capabilities/`.

---

- **Profile:** agent-system   <!-- webapp | agent-system | mcp-server | skill-pack. See shared/agentic-profile.md. -->

---

## Constitution (PROTECTED)

1. **Shared queue, not personal inboxes.** Every ticket belongs to the team queue; no agent owns a private inbox.
2. **Reply history is permanent.** Every reply — canned or negotiated — stays on the ticket for the life of the
   account.
3. **Bounded autonomous refunds.** RefundDesk negotiates and settles refunds up to $500 without a human;
   anything above that requires human approval before it finalizes.
4. **Single support team.** v1 serves one team of up to 15 agents.

---

## REQ registry

| REQ | Name | Priority | Status | File |
|-----|------|----------|--------|------|
| REQ-001 | Queue and claim inbound tickets | MUST | stated | capabilities/support.md |
| REQ-002 | Reply from a canned-response library | MUST | stated | capabilities/support.md |
| REQ-003 | Tag a ticket | SHOULD | stated | capabilities/support.md |
| REQ-004 | Show a live ticket-volume dashboard | MUST | stated | capabilities/support.md |
| REQ-005 | Negotiate and settle refunds under $500 automatically | MUST | stated | capabilities/refunds.md |
| REQ-006 | Escalate any refund negotiation over $500 to a human | MUST | derived | capabilities/refunds.md |

- **Priority** — RFC 2119: `MUST` / `SHOULD` / `MAY`.
- **Status** — `stated` (traces to a source quote) / `derived` (inferred from Profile: agent-system — a flag for
  human confirmation).

---

## Pointers

- **Agent contract** → [`agent-contract.md`](agent-contract.md)
- **Amendment log** → `amendment-log.json`.
