### REQ-014: track pantry items   (MUST)
The system SHALL let a user record a pantry item.

```gherkin
Scenario: add an item
  Given the pantry screen
  When the user clicks the gear icon, then selects "Add", then taps the + button
  Then the item appears
```

```sql
CREATE TABLE pantry_items (id SERIAL PRIMARY KEY, name TEXT, qty INT);
```

The `pantryReducer` Redux slice dispatches `ADD_ITEM` to the `PantryList` component.
<!-- source: inferred -->
<!-- /REQ-014 -->
