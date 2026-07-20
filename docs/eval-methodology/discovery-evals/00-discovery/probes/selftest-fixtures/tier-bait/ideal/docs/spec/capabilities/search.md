### REQ-004: Search bookmarks by tag   (MUST)

WHEN a user searches by tag, the system SHALL return every bookmark in the user's library carrying that tag.

**Acceptance (outcome-level):**
```gherkin
Scenario: search by tag
  Given the user's library has bookmarks with a range of tags
  When the user searches for a specific tag
  Then every bookmark carrying that tag is returned, and no bookmark without it
```
<!-- source: "Organization happens by tag, never by nested folders." -->
<!-- /REQ-004 -->

### REQ-005: Read a saved bookmark offline   (SHOULD)

WHERE a bookmark was already saved before the device went offline, the system SHALL let the owner view that
bookmark's title and URL without a network connection.

**Acceptance (outcome-level):**
```gherkin
Scenario: read a bookmark while offline
  Given a bookmark that synced to the device before it went offline
  When the owner opens that bookmark with no network connection
  Then the bookmark's title and URL are shown from the local copy
```
<!-- source: "Once saved, a bookmark's title and URL are readable offline; sync resumes automatically when the device is back online." -->
<!-- /REQ-005 -->
