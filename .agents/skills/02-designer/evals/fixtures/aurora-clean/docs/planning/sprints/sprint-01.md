<!-- Filename: docs/planning/sprints/sprint-01.md  (zero-padded). -->

# Sprint 01 — Walking skeleton: save a link → browse the list → read & mark read

**Goal:** A user can save a link, see it on the reading list (newest first), open it into the reader, and mark it
read so it leaves the unread list. The core save → read loop works end-to-end.
**Slice shape:** walking skeleton · spans domains: library, reader.
**REQs:** 3 — 3 MUST / 0 SHOULD / 0 MAY.

## REQs in this sprint — frozen acceptance snapshot

> **Sprint-freeze.** Each REQ is referenced by ID **and** carries a *frozen snapshot* of its outcome-level Gherkin as
> it read in the spine at slice time. The spine (`docs/spec/`) remains the live source of truth.

### REQ-001: Save a link to the reading list   (MUST)   →   `docs/spec/capabilities/library.md`

```gherkin
# frozen from spine @ sprint-01
Given a user with a URL they want to read later
When they save the URL to their reading list
Then the item is added to the list and is available to open later
```

### REQ-002: Browse the reading list   (MUST)   →   `docs/spec/capabilities/library.md`

```gherkin
# frozen from spine @ sprint-01
Given a user with one or more saved items
When they open the reading list
Then they see their saved items ordered newest first, each showing its title
```

### REQ-003: Open an item and mark it read   (MUST)   →   `docs/spec/capabilities/reader.md`

```gherkin
# frozen from spine @ sprint-01
Given a user viewing their reading list
When they open a saved item and mark it read
Then the item's content is shown in the reader and the item no longer appears in the unread list
```

## Done When

- [ ] A user can save a URL and it appears on the reading list.  _(REQ-001)_
- [ ] The reading list shows saved items newest first, each with its title.  _(REQ-002)_
- [ ] A user can open an item into the reader and mark it read; it then leaves the unread list.  _(REQ-003)_
- [ ] **End-to-end:** save a link → see it on the list → open it → mark read → it's gone from unread. _(REQ-001 → REQ-002 → REQ-003)_

## Implementation order

1. **Save a link** — the entry point; nothing to read without it.  _(REQ-001)_
2. **Browse the list** — the home surface that shows what was saved.  _(REQ-002)_
3. **Open + mark read** — the reader, closing the loop.  _(REQ-003)_

## Sprint boundary

- **In scope:** the thinnest happy-path thread — save one URL, see it listed, open it, mark it read.
- **Out of scope:** tags, search, folders, full-text extraction quality, sync — all later.
