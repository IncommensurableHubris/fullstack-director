### REQ-001: Add a plant   (MUST)

The system SHALL let a user add a plant with a name to their plant list.

**Acceptance (outcome-level):**
```gherkin
Scenario: add a plant
  Given the user is on their plant list
  When the user adds a plant with a name
  Then the plant appears in the user's plant list
```
<!-- source: "A user adds each plant once, PlantPal works out when it needs water." -->
<!-- /REQ-001 -->

### REQ-002: Set a custom watering interval per plant   (MUST)

WHEN a user sets a watering interval for a plant, the system SHALL schedule that plant's reminders on that
interval independent of any other plant's interval.

**Acceptance (outcome-level):**
```gherkin
Scenario: set a watering interval
  Given a plant on the user's list
  When the user sets that plant's watering interval
  Then the plant's reminders are scheduled on that interval and no other plant's schedule changes
```
<!-- source: "A user adds a plant by name and gives it a watering interval (every plant is different — a cactus is not a fern)." -->
<!-- /REQ-002 -->
