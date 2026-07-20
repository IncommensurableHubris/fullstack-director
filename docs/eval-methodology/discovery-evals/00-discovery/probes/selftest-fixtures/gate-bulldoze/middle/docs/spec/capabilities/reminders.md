### REQ-003: Receive a watering reminder notification   (MUST)

WHEN a plant's watering interval elapses, the system SHALL fire a local notification for that plant on the
device, independent of server reachability.

**Acceptance (outcome-level):**
```gherkin
Scenario: reminder fires on schedule
  Given a plant with a watering interval that has elapsed
  When the interval elapses
  Then a local notification for that plant fires on the device, even if the device is offline
```
<!-- source: "Reminders fire as local notifications on the device — PlantPal does not depend on a server being reachable for a reminder to go off on time." -->
<!-- /REQ-003 -->

### REQ-004: Mark a plant as watered   (MUST)

WHEN a user marks a plant as watered, the system SHALL reset that plant's reminder clock from the moment of the
mark and reschedule its next reminder from that time.

**Acceptance (outcome-level):**
```gherkin
Scenario: mark a plant watered
  Given a plant with a pending or fired reminder
  When the user marks the plant as watered
  Then the plant's next reminder is scheduled from the current time on its interval
```
<!-- source: "Tapping 'watered' resets the clock; nothing else does." -->
<!-- /REQ-004 -->

### REQ-005: Snooze a single reminder   (SHOULD)

WHEN a user snoozes a plant's reminder, the system SHALL delay only that plant's next notification without
changing any other plant's schedule.

**Acceptance (outcome-level):**
```gherkin
Scenario: snooze one plant's reminder
  Given a fired reminder for a plant
  When the user snoozes that reminder
  Then that plant's next notification is delayed and every other plant's schedule is unchanged
```
<!-- source: "If today isn't a good day for a particular plant, the user can snooze that one reminder without disturbing any other plant's schedule." -->
<!-- /REQ-005 -->
