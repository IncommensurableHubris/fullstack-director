# Capability: Library

> The reading list. A user saves a link and browses what they've saved. Each REQ is a delimited block per the
> contract in [`../specification.md`](../specification.md); every REQ here also appears in that file's REQ registry.

### REQ-001: Save a link to the reading list   (MUST)

A user can save a link (URL) to their reading list to read later.

**Acceptance (outcome-level):**
```gherkin
Given a user with a URL they want to read later
When they save the URL to their reading list
Then the item is added to the list and is available to open later
```
<!-- source: "Brief: 'Save a link to read later — paste a URL and it joins the list.'" -->
<!-- /REQ-001 -->

### REQ-002: Browse the reading list   (MUST)

A user can browse their saved items, newest first.

**Acceptance (outcome-level):**
```gherkin
Given a user with one or more saved items
When they open the reading list
Then they see their saved items ordered newest first, each showing its title
```
<!-- source: "Brief: 'The reading list is home — saved items, newest first.'" -->
<!-- /REQ-002 -->
