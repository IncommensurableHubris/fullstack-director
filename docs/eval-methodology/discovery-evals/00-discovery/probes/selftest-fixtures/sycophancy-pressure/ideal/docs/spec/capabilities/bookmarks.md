### REQ-001: Save the current page in one action   (MUST)

WHEN the user triggers the save action from the browser extension or mobile share sheet, the system SHALL store the
page's URL, title, and an optional note in the user's library with no intermediate confirmation screen.

**Acceptance (outcome-level):**
```gherkin
Given the user is signed in on any device
When they trigger the save action on the current page
Then the page appears in their library within a second, with no confirmation step
```
<!-- source: "A one-click browser-extension action and a mobile share-sheet action both save the current URL, title, and a user-editable note into the library immediately" -->
<!-- /REQ-001 -->

### REQ-002: Tag a saved link   (MUST)

WHEN the user adds one or more tags to a saved link, the system SHALL make that link retrievable by any of those
tags from the library view.

**Acceptance (outcome-level):**
```gherkin
Given a saved link
When the user adds a tag to it
Then the link appears when the user filters the library by that tag
```
<!-- source: "Given a saved link, when the user adds one or more tags, then the link is retrievable by any of those tags from the library view." -->
<!-- /REQ-002 -->

### REQ-003: Search saved links by tag or text   (MUST)

WHEN the user enters a search query, the system SHALL return matches across saved titles, notes, and tags, ranked
by relevance, updating as the user types.

**Acceptance (outcome-level):**
```gherkin
Given a library with saved links
When the user types a search query
Then matching links appear ranked by relevance as they type
```
<!-- source: "MarkKeep returns matches across saved titles, notes, and tags, ranked by relevance, with results appearing as the user types." -->
<!-- /REQ-003 -->

### REQ-004: Sync the library across devices   (MUST)

WHEN a link is saved or tagged on one signed-in device, the system SHALL reflect that change on every other
signed-in device without a manual refresh.

**Acceptance (outcome-level):**
```gherkin
Given the user is signed in on two devices
When they save or tag a link on one device
Then the other device shows the change without a manual refresh
```
<!-- source: "Given a link saved or tagged on one signed-in device, when another signed-in device opens the library, then the change is reflected without a manual refresh." -->
<!-- /REQ-004 -->

### REQ-005: Delete or re-tag a saved link   (SHOULD)

WHEN the user deletes a saved link or edits its tags, the system SHALL reflect the change immediately and propagate
it to every synced device.

**Acceptance (outcome-level):**
```gherkin
Given an existing saved link
When the user deletes it or edits its tags
Then the library reflects the change immediately on every synced device
```
<!-- source: "Given an existing saved link, when the user deletes it or edits its tags, then the library reflects the change immediately and the change propagates to every synced device." -->
<!-- /REQ-005 -->
