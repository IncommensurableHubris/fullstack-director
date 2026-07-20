# Triage capabilities — Relay

### REQ-001: Classify and draft a reply for each new ticket   (MUST)

WHEN a new support ticket arrives, the system SHALL classify it (billing / bug / how-to / abuse) and draft a reply grounded in help-center articles.

**Acceptance (outcome-level):**
```gherkin
Given a new ticket in the support inbox
When Relay processes it
Then it records a classification and a draft reply that cites a help-center article
```
<!-- source: "classify it (billing / bug / how-to / abuse) and draft a reply from our help-center articles" -->
<!-- /REQ-001 -->

### REQ-002: Send low-risk replies autonomously   (SHOULD)

WHERE a ticket is a simple how-to or billing-status question, the system SHALL send the drafted reply without human review.

**Acceptance (outcome-level):**
```gherkin
Given a drafted reply for a how-to question
When the draft is grounded in a help-center article
Then Relay sends it without waiting for a human
```
<!-- source: "For simple how-to and billing-status questions it should be able to send the reply itself" -->
<!-- /REQ-002 -->

### REQ-003: Refuse to send an ungrounded reply   (MUST)

IF a drafted reply is not grounded in a help-center article, THEN the system SHALL refuse to send it and escalate to a human.

**Acceptance (outcome-level):**
```gherkin
Given a drafted reply with no supporting help-center article
When Relay evaluates it before sending
Then it does not send the reply and escalates to a human
```
<!-- source: "It must never send a reply that isn't grounded in a help-center article" -->
<!-- /REQ-003 -->

### REQ-004: Refuse to execute a refund without human approval   (MUST)

IF a refund has not been approved by a human, THEN the system SHALL refuse to execute it.

**Acceptance (outcome-level):**
```gherkin
Given a proposed refund
When no human has approved it
Then Relay does not call the refund tool
```
<!-- source: "It must never issue a refund without a human approving it first" -->
<!-- /REQ-004 -->
