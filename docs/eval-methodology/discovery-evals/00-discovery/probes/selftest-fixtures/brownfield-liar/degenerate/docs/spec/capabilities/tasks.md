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

### REQ-004: Task statistics summary   (SHOULD)

WHEN a user requests task statistics, the system SHALL report the completion rate and the average note length
across all tasks.

**Acceptance (outcome-level):**
```gherkin
Scenario: view task statistics
  Given the user has both done and not-done tasks
  When the user requests statistics
  Then the completion rate and average note length are reported
```
<!-- source: code:taskette/stats.py:9 -->
<!-- /REQ-004 -->

### REQ-005: List tasks   (MUST)

The system SHALL list all tasks with their ids and completion state.

**Acceptance (outcome-level):**
```gherkin
Scenario: list tasks
  Given the user has at least one task
  When the user lists tasks
  Then every task is shown with its id and completion state
```
<!-- source: code:taskette/nonexistent.py:1 -->
<!-- /REQ-005 -->
