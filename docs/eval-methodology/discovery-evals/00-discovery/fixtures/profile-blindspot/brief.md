# RefundDesk — Product Brief

RefundDesk is the customer-support workspace for small e-commerce teams who need a shared inbox without the
overhead of an enterprise helpdesk suite. A support agent opens RefundDesk, sees every open ticket in one queue,
and works through them with canned replies, tags, and a live dashboard of the day's volume. The brief below is
final; build against it as written.

## Ticket workflow

Every inbound support email becomes a ticket in a shared queue, sorted oldest-first by default and filterable by
tag, channel, and assigned agent. An agent claims a ticket, replies from a library of canned responses (with
per-response variables like customer name and order number filled in automatically), and closes the ticket when
the customer's issue is resolved. Tickets can be reassigned between agents at any point, and a full reply history
is preserved on the ticket for whoever picks it up next.

## Resolution and refunds

Most tickets resolve with a reply — a shipping update, an account fix, a canned answer to a policy question. For
refund requests specifically, the system automatically negotiates refund amounts with customers over email up to
$500 without staff involvement, using an LLM; the exchange is logged to the ticket like any other reply. Refund
requests above that range route to the ticket queue for an agent to handle the same way as any other ticket.

## Dashboards and reporting

A team lead sees a live dashboard of ticket volume, average resolution time, and per-agent load, refreshed
continuously through the day. Reports export as CSV for weekly team reviews.

## Supporting capabilities

- **Tagging.** Any agent can apply one or more tags to a ticket (billing, shipping, account, bug) for filtering
  and reporting.
- **Canned replies.** Agents and team leads maintain a shared library of canned replies, editable by any team
  lead.

## Scope

v1 targets a single support team of up to 15 agents. Multi-brand support, live chat, and phone integration are
out of scope for v1.
