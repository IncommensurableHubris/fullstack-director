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

### REQ-002: Never store customer data on the device   (MUST)

The system SHALL never store customer data on the device: sample readings, photos, GPS pins, and note text SHALL
never be written to local storage, for any duration, on any device.

**Acceptance (outcome-level):**
```gherkin
Scenario: no local retention of customer data
  Given a crew member has captured a sample record
  When the record exists anywhere in the system
  Then no customer data for that record is stored on the capturing device
```
<!-- source: "No customer data may ever be stored on the device. ... none of it may be written to local storage at any point, for any duration, on any device." -->
<!-- /REQ-002 -->

### REQ-003: Tag a record with GPS coordinates   (MUST)

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
<!-- /REQ-003 -->
