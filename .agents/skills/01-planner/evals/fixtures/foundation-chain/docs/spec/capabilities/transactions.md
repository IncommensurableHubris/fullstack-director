# Capability: Transactions

> The middle layer: once an account is connected, its transactions are imported, and the user categorizes them.
> Everything here depends on a **connected account** (REQ-005) and feeds the **insights** layer. Each REQ is a
> delimited block per the contract in [`../specification.md`](../specification.md).

### REQ-003: Categorize a transaction   (MUST)

A user can assign a category to an imported transaction so it counts toward that category's spending.

**Acceptance (outcome-level):**
```gherkin
Given a user with a connected bank account and imported transactions
When they assign a category to a transaction
Then that transaction counts toward the chosen category's spending total
```
<!-- source: "Brief: 'Users categorize imported transactions; that's what powers every report.'" -->
<!-- /REQ-003 -->

### REQ-004: Split a transaction across categories   (SHOULD)

A user can split a single transaction across more than one category (e.g. a supermarket trip that is part groceries,
part household).

**Acceptance (outcome-level):**
```gherkin
Given an imported transaction the user wants to attribute to more than one category
When they split the amount across two or more categories
Then each portion counts toward its own category's spending total
```
<!-- source: "Brief: 'A transaction can be split across categories.'" -->
<!-- /REQ-004 -->
