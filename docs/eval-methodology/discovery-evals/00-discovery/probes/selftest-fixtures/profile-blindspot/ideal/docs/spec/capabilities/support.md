<!-- budget: ≤25 lines per REQ block — one home per fact; detail is realization, not spine. -->

# Capability: Support

> The core ticket workflow: queue, claim, reply, tag, and monitor. Each REQ is a delimited block per
> [`../specification.md`](../specification.md).

### REQ-001: Queue and claim inbound tickets   (MUST)

WHEN an inbound support email arrives, the system SHALL create a ticket in the shared queue, sorted oldest-first
by default and filterable by tag, channel, and assigned agent.

**Acceptance (outcome-level):**
```gherkin
Given a new support email arrives
When RefundDesk processes it
Then a ticket appears in the shared queue, available for any agent to claim
```
<!-- source: "Every inbound support email becomes a ticket in a shared queue, sorted oldest-first by default and filterable by tag, channel, and assigned agent." -->
<!-- /REQ-001 -->

### REQ-002: Reply from a canned-response library   (MUST)

WHEN an agent replies to a ticket, the system SHALL let the agent select a canned response with per-response
variables — customer name, order number — filled in automatically.

**Acceptance (outcome-level):**
```gherkin
Given an agent has claimed a ticket
When the agent selects a canned response
Then the reply is sent with the customer name and order number filled in
```
<!-- source: "replies from a library of canned responses (with per-response variables like customer name and order number filled in automatically)" -->
<!-- /REQ-002 -->

### REQ-003: Tag a ticket   (SHOULD)

WHERE an agent wants to categorize a ticket, the system SHALL let the agent apply one or more tags (billing,
shipping, account, bug) for filtering and reporting.

**Acceptance (outcome-level):**
```gherkin
Given an open ticket
When an agent applies a tag
Then the ticket is filterable and reportable by that tag
```
<!-- source: "Any agent can apply one or more tags to a ticket (billing, shipping, account, bug) for filtering and reporting." -->
<!-- /REQ-003 -->

### REQ-004: Show a live ticket-volume dashboard   (MUST)

The system SHALL show a team lead a live dashboard of ticket volume, average resolution time, and per-agent
load, refreshed continuously through the day.

**Acceptance (outcome-level):**
```gherkin
Given a team lead opens the dashboard
When new tickets are created, replied to, or closed
Then the dashboard's volume, resolution-time, and per-agent figures update without a manual refresh
```
<!-- source: "A team lead sees a live dashboard of ticket volume, average resolution time, and per-agent load, refreshed continuously through the day." -->
<!-- /REQ-004 -->
