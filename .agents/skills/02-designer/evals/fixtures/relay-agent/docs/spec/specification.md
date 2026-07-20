# Specification — Relay

> The spec spine index — Constitution + REQ registry. Owned by skill 00.

---

- **Profile:** agent-system   <!-- webapp | agent-system | mcp-server | skill-pack. See shared/agentic-profile.md. -->

---

## Constitution (PROTECTED)

1. **Grounded answers only.** Relay never sends a customer a claim not grounded in a help-center article.
2. **Humans move money.** No refund or payment executes without explicit human approval.
3. **EU data residency.** Customer data stays in the EU region.

---

## REQ registry

| REQ | Name | Priority | Status | File |
|-----|------|----------|--------|------|
| REQ-001 | Classify and draft a reply for each new ticket | MUST | stated | capabilities/triage.md |
| REQ-002 | Send low-risk replies autonomously | SHOULD | stated | capabilities/triage.md |
| REQ-003 | Refuse to send an ungrounded reply | MUST | stated | capabilities/triage.md |
| REQ-004 | Refuse to execute a refund without human approval | MUST | stated | capabilities/triage.md |

- **Priority** — RFC 2119: `MUST` / `SHOULD` / `MAY`.
- **Status** — `stated` / `derived`.

---

## Pointers

- **Architecture constraints** → [`architecture-constraints.md`](architecture-constraints.md)
- **Agent contract** → [`agent-contract.md`](agent-contract.md)
- **Amendment log** → [`amendment-log.json`](amendment-log.json)
