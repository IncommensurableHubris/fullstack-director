### REQ-001: Save a bookmark   (MUST)

The system SHALL let a user save the current page's URL and title as a bookmark in a single action from any device.

**Acceptance (outcome-level):**
```gherkin
Scenario: save a bookmark
  Given the user is signed in and viewing any page, on any device
  When the user saves the page as a bookmark
  Then the bookmark is added to the user's library with the page's URL and title
```
<!-- source: "Saving a bookmark is a single action available from any device, phone included." -->
<!-- /REQ-001 -->

### REQ-002: Tag a bookmark   (MUST)

WHEN a user adds a tag to a bookmark, the system SHALL attach that tag to the bookmark and make it available for
tag-based search.

**Acceptance (outcome-level):**
```gherkin
Scenario: tag a bookmark
  Given a bookmark the user owns
  When the user adds a tag to the bookmark
  Then the tag appears on the bookmark and the bookmark is returned by a search for that tag
```
<!-- source: "Organization happens by tag, never by nested folders." -->
<!-- /REQ-002 -->

### REQ-003: Delete a bookmark   (MUST)

WHEN the owner deletes a bookmark, the system SHALL remove it from the owner's library and from all tag listings.

**Acceptance (outcome-level):**
```gherkin
Scenario: delete a bookmark
  Given a bookmark the user owns
  When the user deletes the bookmark
  Then the bookmark no longer appears in the owner's library or in any tag search
```
<!-- source: "Every bookmark belongs to exactly one owner's library." -->
<!-- /REQ-003 -->
