# Capability: Reader

> Reading a saved item. A user opens an item into the full-bleed reader and marks it read. Each REQ is a delimited
> block per the contract in [`../specification.md`](../specification.md); every REQ here also appears in that file's
> REQ registry.

### REQ-003: Open an item and mark it read   (MUST)

A user can open a saved item into the reader and mark it as read, which removes it from the unread list.

**Acceptance (outcome-level):**
```gherkin
Given a user viewing their reading list
When they open a saved item and mark it read
Then the item's content is shown in the reader and the item no longer appears in the unread list
```
<!-- source: "Brief: 'Open an item to read it; mark it read and it leaves the list.'" -->
<!-- /REQ-003 -->
