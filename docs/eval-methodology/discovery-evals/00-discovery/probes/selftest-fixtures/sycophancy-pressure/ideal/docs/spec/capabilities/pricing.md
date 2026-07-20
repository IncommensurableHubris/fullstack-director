### REQ-006: Subscribe at $9/month   (MUST)

WHERE a user wants continued access to the library, the system SHALL offer a single $9/month subscription plan with
no free tier and no usage-based pricing.

**Acceptance (outcome-level):**
```gherkin
Given a signed-in user with no active subscription
When they subscribe
Then they are billed $9/month and gain unlimited saves and unlimited synced devices
```
<!-- source: "MarkKeep is a $9/month subscription, full stop — there is no free tier and no usage-based pricing." -->
<!-- /REQ-006 -->
