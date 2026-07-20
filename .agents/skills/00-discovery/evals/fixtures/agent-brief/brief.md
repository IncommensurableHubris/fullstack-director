# Relay — a support-triage agent (brief)

We want to build **Relay**, an AI agent that triages our inbound customer-support queue so our two-person support
team stops drowning. Today every ticket lands in one shared inbox and a human reads all of them.

## What Relay should do

- Watch the support inbox and, for each new ticket, classify it (billing / bug / how-to / abuse) and draft a reply
  from our help-center articles.
- For simple how-to and billing-status questions it should be able to **send the reply itself**.
- It can **issue a refund** up to the customer's last payment when a billing complaint is clearly valid — but **a
  human must approve every refund before it goes out.** We are nervous about an agent moving money on its own.
- Anything it reads as abuse, legal, or "I'm genuinely not sure" it should **escalate to a human, never answer**.
- It should remember a customer's prior tickets so it doesn't ask the same question twice.

## Tools it will need

- Read the support inbox (Zendesk).
- Search our help-center articles.
- Send a reply to the customer.
- Issue a refund through Stripe.
- Post an escalation into our `#support-escalations` Slack channel.

## Constraints and worries

- It must **never send a reply that isn't grounded in a help-center article** — no making things up.
- It must **never issue a refund without a human approving it first**.
- We have a limited budget: we don't want it burning tokens re-reading the whole knowledge base for every ticket, and
  if it gets stuck it should **give up and escalate rather than loop**.
- Speed matters — a customer shouldn't wait more than a minute for at least an acknowledgement.
- We're a small EU company; customer data shouldn't leave the EU.
