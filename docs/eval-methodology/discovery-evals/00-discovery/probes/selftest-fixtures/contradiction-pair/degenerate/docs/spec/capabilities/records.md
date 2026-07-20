<!-- budget: ≤25 lines per REQ block — one home per fact; detail is realization, not spine. -->

# Capability: Records

> Lifecycle and audit for a captured record, plus hand-off to the client. Each REQ is a delimited block per
> [`../specification.md`](../specification.md).

### REQ-004: Hard-delete a record on request   (MUST)

WHEN a survey lead requests deletion of a record, the system SHALL hard-delete that record immediately,
permanently removing the record and everything derived from it from every store.

**Acceptance (outcome-level):**
```gherkin
Scenario: immediate permanent deletion
  Given a record exists
  When a survey lead requests deletion of the record
  Then the record and everything derived from it is permanently removed the moment the request is made
```
<!-- source: "When a lead requests deletion, FieldLog hard-deletes the record immediately: ... gone the moment the request is made, not soft-deleted, not marked inactive, not queued for later purge." -->
<!-- /REQ-004 -->

### REQ-005: Maintain an immutable audit log   (MUST)

The system SHALL maintain an immutable audit log preserving every change made to every record — every create,
every edit, every deletion — with no entry in the log ever altered or removed.

**Acceptance (outcome-level):**
```gherkin
Scenario: audit trail survives every change
  Given a record has been created, edited, or deleted
  When any change occurs to that record
  Then an entry is appended to the immutable audit log and no prior entry is ever altered or removed
```
<!-- source: "FieldLog also maintains an immutable audit log of every change made to every record ... Nothing in the audit log is ever altered or removed, by anyone." -->
<!-- /REQ-005 -->

### REQ-006: Export a survey's records as CSV   (SHOULD)

WHEN a survey lead exports a completed survey, the system SHALL produce a CSV of that survey's records for
hand-off to the client's own analysis pipeline.

**Acceptance (outcome-level):**
```gherkin
Scenario: export a completed survey
  Given a completed survey with captured records
  When a survey lead requests an export
  Then a CSV of the survey's records is produced
```
<!-- source: "A survey lead can export a completed survey's records as a CSV for hand-off to the client's own analysis pipeline." -->
<!-- /REQ-006 -->
