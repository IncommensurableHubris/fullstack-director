### REQ-001: Create a note   (MUST)

The system SHALL let a user create a note from any device with an optional note title and no required fields beyond note content.

**Acceptance (outcome-level):**
```gherkin
Scenario: create a note
  Given the user is signed in
  When the user creates a new note, with or without a note title
  Then the note is saved and appears in the user's note list, listed under its title when one was given
```
<!-- source: "Creating a note is a single action from any device — no required fields beyond note content." -->
<!-- /REQ-001 -->

### REQ-002: Edit a note   (MUST)

WHEN the owner edits an existing note, the system SHALL save the change and update the note's last-modified time.

**Acceptance (outcome-level):**
```gherkin
Scenario: edit a note
  Given a note the user owns
  When the user changes the note's content
  Then the change is saved and the note shows the new content on next view
```
<!-- source: "A note has exactly one editor of record." -->
<!-- /REQ-002 -->

### REQ-003: Delete a note   (MUST)

WHEN the owner deletes a note, the system SHALL remove the note from the owner's note list and revoke any active
share links for it.

**Acceptance (outcome-level):**
```gherkin
Scenario: delete a note
  Given a note the user owns
  When the user deletes the note
  Then the note no longer appears in the owner's note list and any share link for it stops working
```
<!-- source: "Collaboration happens through explicit sharing, never implicit team visibility." -->
<!-- /REQ-003 -->
