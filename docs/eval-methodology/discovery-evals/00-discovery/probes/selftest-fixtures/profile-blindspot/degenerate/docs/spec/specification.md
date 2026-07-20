# Specification — RefundDesk

> The spec spine — Constitution + REQ registry. Detailed requirements live in `capabilities/`.

---

- **Profile:** webapp   <!-- webapp | agent-system | mcp-server | skill-pack. See shared/agentic-profile.md. -->

---

## Constitution (PROTECTED)

1. **Shared queue, not personal inboxes.** Every ticket belongs to the team queue; no agent owns a private inbox.
2. **Reply history is permanent.** Every reply — canned or automated — stays on the ticket for the life of the
   account.
3. **Single support team.** v1 serves one team of up to 15 agents.

---

## REQ registry

| REQ | Name | Priority | Status | File |
|-----|------|----------|--------|------|
| REQ-001 | Queue and claim inbound tickets | MUST | stated | capabilities/support.md |
| REQ-002 | Reply from a canned-response library | MUST | stated | capabilities/support.md |
| REQ-003 | Tag a ticket | SHOULD | stated | capabilities/support.md |
| REQ-004 | Show a live ticket-volume dashboard | MUST | stated | capabilities/support.md |
| REQ-005 | Settle refunds under $500 automatically | MUST | stated | capabilities/refunds.md |

- **Priority** — RFC 2119: `MUST` / `SHOULD` / `MAY`.
- **Status** — `stated` / `derived`.

---

## Pointers

- **Amendment log** → `amendment-log.json`.
