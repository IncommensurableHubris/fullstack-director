### REQ-002: Encrypt the task store end-to-end   (MUST)

The system SHALL apply end-to-end encryption to every task store so task contents are unreadable outside the
owner's own client.

**Acceptance (outcome-level):**
```gherkin
Scenario: task store is encrypted at rest
  Given a task store with saved tasks
  When the underlying file is inspected outside taskette
  Then no task title or note is readable in plaintext
```
<!-- source: docs:README.md -->
<!-- /REQ-002 -->

### REQ-003: Role-based multi-user access control   (MUST)

WHERE a task store is shared, the system SHALL enforce role-based access control limiting each collaborator to
the actions their role permits.

**Acceptance (outcome-level):**
```gherkin
Scenario: a viewer cannot remove a task
  Given a shared task store and a collaborator with the viewer role
  When that collaborator attempts to remove a task
  Then the removal is refused
```
<!-- source: docs:README.md -->
<!-- /REQ-003 -->
