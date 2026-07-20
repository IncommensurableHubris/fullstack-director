# Specification — Beacon

> The spec spine index — Constitution + REQ registry. Owned by skill 00.

---

- **Profile:** agent-system   <!-- webapp | agent-system | mcp-server | skill-pack. See shared/agentic-profile.md. -->
- **Data:** retrieval(handbook-lookup) · memory   <!-- data-module routing; see shared/agentic-profile.md § The Data line. -->

---

## Constitution (PROTECTED)

1. **Every claim is cited.** No sentence in a Beacon report asserts a fact without a link to the source it came from.
2. **Breadth is the point.** Beacon's value is *parallel* coverage of many independent sources at once — not a deep
   read of one. A design that serializes source coverage defeats the product.
3. **Read-only research.** Beacon never modifies external state; it searches, fetches, and synthesizes only.

---

## REQ registry

| REQ | Name | Priority | Status | File |
|-----|------|----------|--------|------|
| REQ-001 | Fan out parallel research workers across independent sources | MUST | stated | capabilities/research.md |
| REQ-002 | Synthesize a grounded, comprehensive report | MUST | stated | capabilities/research.md |
| REQ-003 | Refuse to present an uncited claim | MUST | stated | capabilities/research.md |

- **Priority** — RFC 2119: `MUST` / `SHOULD` / `MAY`.
- **Status** — `stated` / `derived`.

---

## Pointers

- **Architecture constraints** → [`architecture-constraints.md`](architecture-constraints.md)
- **Agent contract** → [`agent-contract.md`](agent-contract.md)
- **Amendment log** → [`amendment-log.json`](amendment-log.json)
