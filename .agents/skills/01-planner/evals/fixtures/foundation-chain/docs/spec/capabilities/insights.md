# Capability: Insights

> What the user gets *out* of PennyPilot once their transactions are connected and categorized: a monthly spending
> summary and category budgets. These are **consuming features** — every REQ here depends on categorized
> transactions, which in turn depend on a connected account. Each REQ is a delimited block per the contract in
> [`../specification.md`](../specification.md).

### REQ-001: See a monthly spending summary   (MUST)

A user whose transactions have been categorized can see how much they spent per category for a given month.

**Acceptance (outcome-level):**
```gherkin
Given a user whose imported transactions for a month have been categorized
When they open the summary for that month
Then they see total spending broken down by category, each figure traceable to its transactions
```
<!-- source: "Brief: 'The core payoff is a monthly summary showing spend per category.'" -->
<!-- /REQ-001 -->

### REQ-002: Set a category budget and get alerted   (SHOULD)

A user can set a monthly budget for a category and be alerted when spending in that category approaches or exceeds it.

**Acceptance (outcome-level):**
```gherkin
Given a user who can see their categorized spending for a category
When they set a monthly budget for that category and spending crosses the threshold
Then they are alerted that the category is near or over budget
```
<!-- source: "Brief: 'Users can set per-category budgets and get a heads-up before they blow them.'" -->
<!-- /REQ-002 -->
