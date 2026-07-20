### REQ-001: Add a task   (MUST)

The system SHALL let a user add a task with a title and an optional note, persisted to the local store.

**Acceptance (outcome-level):**
```gherkin
Scenario: add a task
  Given the user runs taskette
  When the user adds a task with a title
  Then the task appears in the task list with that title
```
<!-- source: code:taskette/store.py:20 -->
<!-- /REQ-001 -->

### REQ-002: List tasks   (MUST)

The system SHALL list all tasks with their ids and completion state.

**Acceptance (outcome-level):**
```gherkin
Scenario: list tasks
  Given the user has at least one task
  When the user lists tasks
  Then every task is shown with its id and completion state
```
<!-- source: code:taskette/cli.py:19 -->
<!-- /REQ-002 -->

### REQ-003: Mark a task done   (MUST)

WHEN a user marks a task done, the system SHALL record that task as complete.

**Acceptance (outcome-level):**
```gherkin
Scenario: complete a task
  Given a task that is not yet done
  When the user marks that task done
  Then the task is shown as done in the task list
```
<!-- source: code:taskette/cli.py:25 -->
<!-- /REQ-003 -->

### REQ-004: Remove a task   (MUST)

WHEN a user removes a task, the system SHALL delete it from the store.

**Acceptance (outcome-level):**
```gherkin
Scenario: remove a task
  Given a task the user owns
  When the user removes that task
  Then the task no longer appears in the task list
```
<!-- source: code:taskette/store.py:44 -->
<!-- /REQ-004 -->

### REQ-005: Reject oversized task notes   (MUST)

IF a task note exceeds 10 KB (10,240 bytes), THEN the system SHALL reject the write and leave the store
unchanged.

**Acceptance (outcome-level):**
```gherkin
Scenario: an oversized note is refused
  Given a note larger than 10 KB
  When the user tries to add a task with that note
  Then the write is rejected and no task is added
```
<!-- source: code:taskette/store.py:23 -->
<!-- /REQ-005 -->
