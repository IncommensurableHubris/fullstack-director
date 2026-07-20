# ShelfLife — Product Requirements Document

## Problem

Households throw away food they forgot they had, and re-buy food they didn't need. Existing grocery-list apps
track what to buy, not what's already on the shelf, so the loss keeps happening between trips. ShelfLife is a
mobile-first pantry tracker: log what you have, get nudged before it expires, and see what's actually running low
before you shop.

## Goals

- Cut self-reported household food waste by a noticeable margin within the first two months of regular use.
- Make logging a new item fast enough that people actually keep doing it — this is a habit product, not a
  spreadsheet replacement.
- Surface "use this soon" items automatically, without the user having to remember to check.

## Non-goals

- No barcode-scanning hardware integrations in v1 — manual entry and a basic photo capture only.
- No shared/multi-household inventory in v1; single-user pantry only.
- No recipe recommendation engine in v1 (tracked as a fast-follow, not in scope here).

## Target user

Home cooks who shop weekly and keep a moderately stocked pantry/fridge — not extreme preppers, not people who eat
out every meal. They're willing to spend a few seconds logging an item if it saves them from throwing food away or
re-buying something they already have.

## Core user stories

1. As a user, I want to add a pantry item in a few seconds so that logging doesn't feel like a chore.
2. As a user, I want to be reminded before an item expires so I can use it instead of tossing it.
3. As a user, I want to see what's running low so my next grocery trip is accurate.
4. As a user, I want to remove or adjust an item's quantity as I use it up.

## Feature requirements

### Add item

The add-item flow works as follows: from the pantry screen, the user taps the gear icon in the top-right corner,
selects "Add item" from the dropdown menu, fills in the name and quantity fields on the sheet that slides up, then
taps the + button at the bottom of the sheet to confirm. The new item appears at the top of the pantry list
immediately and is available for expiry tracking from that moment. We validated this exact flow in the spike and
it hit our speed target — median under six seconds from screen open to item saved.

Item cards in the mobile list use 16px horizontal padding, an 8px gap between the name and quantity labels, and a
44px minimum tap-target height per row. These values are settled; design has already signed off.

### Data model

Engineering has already sketched the schema for the items table:

```sql
CREATE TABLE pantry_items (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  name TEXT NOT NULL,
  quantity INTEGER NOT NULL DEFAULT 1,
  expires_on DATE,
  low_stock_threshold INTEGER,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);
```

Expiry nudges and low-stock surfacing both read from this table, so it should land in the first sprint.

### Client state

The frontend team has settled on a `pantryReducer` Redux slice with `ADD_ITEM` / `REMOVE_ITEM` / `ADJUST_QTY`
actions feeding the `PantryList` component, mirroring the pattern the shopping-list feature already uses. New
pantry work should follow this structure for consistency with the existing app.

### Expiry nudge

Given an item has an expiry date within the configured warning window, when that window is reached, the user
receives a notification naming the item.

### Low-stock surfacing

Given an item's quantity drops to or below its configured low-stock threshold, when the user opens the shopping
view, that item is listed there.

### Remove / adjust

Given an existing pantry item, when the user updates or deletes it, the pantry list reflects the change without
requiring an app restart.

## Success metrics

- Weekly active loggers as a share of installs.
- Median time from "open add-item flow" to "item saved."
- Self-reported waste reduction in the in-app monthly check-in survey.
- Retention at week 4 and week 8.

## Open questions

- Do we warn on expiry per-item (user sets each date) or default to a category-based shelf-life table the user can
  override? Leaning toward the latter to reduce logging friction, but needs a call before we can size v1.
- Where does the low-stock threshold come from — a flat default per category, or does the user set it per item?
