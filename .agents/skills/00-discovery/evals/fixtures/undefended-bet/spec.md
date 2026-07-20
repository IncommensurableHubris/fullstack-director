# MealMate — Specification (v0.9)

## Summary
MealMate generates a personalized weekly meal plan and a consolidated grocery list from a user's dietary preferences
and pantry inventory. **Our core bet: home cooks will switch from their free spreadsheets and pay $15/month for
automated planning** — that subscription revenue is the whole basis of the business.

## Problem & user
- **Problem:** planning meals for the week and turning that into a non-redundant shopping list is tedious and
  error-prone.
- **Primary user:** a busy home cook who currently maintains an ad-hoc spreadsheet.
- **Job to be done:** *When I'm planning the week's meals, I want a plan and a grocery list generated for me, so I can
  shop once and cook without daily decisions.*

## Capabilities

### Preferences
- A user can set dietary preferences (restrictions, cuisines, calorie target).
- A user can record their current pantry inventory.

### Planning
- A user can generate a 7-day meal plan honoring their preferences and pantry.
- A user can swap any single meal and regenerate just that slot.
- A user can export the consolidated grocery list (deduplicated across the week).

### Account & billing
- A user can subscribe at $15/month and manage their subscription.

## Constraints
- **Stack:** architect's choice.
- **Hosting:** must run in North America.

## Scope
- **In scope (v1):** preferences, planning, grocery list, subscription billing.
- **Out of scope (v1):** recipe authoring, social sharing, grocery-delivery integrations.
