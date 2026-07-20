<!-- budget: ≤25 lines per REQ block — one home per fact; detail is realization, not spine. -->

# Capability: Capture

> The point-of-sample workflow: start a survey, log a record, attach a photo, pin a GPS position, all in the
> field. Each REQ is a delimited block per [`../specification.md`](../specification.md).

### REQ-001: Capture a record fully offline   (MUST)

The system SHALL support offline-first operation for every core capture workflow — starting a survey, logging a
sample record, attaching a photo, logging a GPS position, and tagging a record for follow-up — with zero
dependency on network connectivity at the point of capture.

**Acceptance (outcome-level):**
```gherkin
Scenario: capture a record with no connectivity
  Given a crew member has no network connection
  When the crew member logs a sample record, attaches a photo, and pins a GPS position
  Then all three actions succeed and the record is held for sync once connectivity returns
```
<!-- source: "FieldLog is offline-first. Every core workflow ... must work end to end with zero network connectivity at the point of capture." -->
<!-- /REQ-001 -->

### REQ-002: Tag a record with GPS coordinates   (MUST)

WHEN a crew member captures a record, the system SHALL attach the device's current GPS coordinates to the record
automatically.

**Acceptance (outcome-level):**
```gherkin
Scenario: automatic GPS tagging
  Given a crew member is capturing a record
  When the record is saved
  Then the record carries the device's current GPS coordinates without manual entry
```
<!-- source: "Every captured record carries the device's current GPS coordinates automatically; the crew member never enters coordinates by hand." -->
<!-- /REQ-002 -->

### REQ-003: Export a survey's records as CSV   (SHOULD)

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
<!-- /REQ-003 -->
