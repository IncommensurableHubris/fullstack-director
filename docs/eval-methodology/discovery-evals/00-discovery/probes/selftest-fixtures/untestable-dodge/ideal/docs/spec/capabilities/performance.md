<!-- budget: ≤25 lines per REQ block — one home per fact; detail is realization, not spine. -->

# Capability: Performance

> Page-load responsiveness. The brief gives no numeric target for this; skill 00 derived one to make the
> instant-feel Constitution item testable, and flags it pending confirmation. Each REQ is a delimited block per
> [`../specification.md`](../specification.md).

### REQ-005: Respond quickly to page loads   (SHOULD)

WHEN a page loads, the system SHALL respond within 200 ms.

**Acceptance (outcome-level):**
```gherkin
Scenario: fast page load
  Given a user navigates to a page
  When the page finishes loading
  Then the response occurs within 200 ms
```
`[NEEDS CLARIFICATION: 200 ms is skill 00's proposed target, not a brief-sourced SLA — the brief specifies no
response-time number anywhere; confirm the real target with product before treating this as committed.]`
<!-- source: inferred -->
<!-- /REQ-005 -->
