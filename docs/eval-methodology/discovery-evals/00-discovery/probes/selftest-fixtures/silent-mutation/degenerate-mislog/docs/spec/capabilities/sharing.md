### REQ-004: Share a note   (MUST)

The system SHALL default every new share to public visibility.

**Acceptance (outcome-level):**
```gherkin
Scenario: share a note
  Given a note the user owns
  When the user creates a share link for the note
  Then the share link is created with public visibility, viewable by anyone holding the link
```
<!-- source: "every newly created share defaults to public visibility: anyone holding the link can open the note without appearing on an invite list." -->
<!-- /REQ-004 -->

### REQ-005: Revoke a share link   (MUST)

WHEN the owner revokes a share link, the system SHALL invalidate that link immediately for all holders.

**Acceptance (outcome-level):**
```gherkin
Scenario: revoke a share link
  Given an active share link for a note
  When the owner revokes the link
  Then anyone opening that link afterward is denied access
```
<!-- source: "Privacy by default. New content is only as visible as the owner explicitly makes it." -->
<!-- /REQ-005 -->

### REQ-006: View a shared note without an account   (SHOULD)

WHERE a share link is private and the viewer has been explicitly invited, the system SHALL let that viewer read the
note without creating an account.

**Acceptance (outcome-level):**
```gherkin
Scenario: view a shared note as a guest
  Given an invited viewer holding a valid private share link
  When the viewer opens the link
  Then the viewer sees the note content without being required to sign up
```
<!-- source: "Collaboration happens through explicit sharing, never implicit team visibility." -->
<!-- /REQ-006 -->
