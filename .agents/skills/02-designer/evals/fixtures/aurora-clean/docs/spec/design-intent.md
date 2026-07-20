# Design Intent — Aurora

> **Declaration-truth for look, feel, and experience.** What the product should *feel like* and the design facts the
> user cares about. Owned by **skill 00 (discovery)**. Skill 02 (designer) **realizes** this into a design system +
> screens that *reference* it, and may only **propose additions/changes via amendment**, never silently overwrite.
> A `derived` item is an inference skill 00 made, not a user statement; confirm before treating it as fixed.

## Brand & feeling

- **Adjectives (3–5):** calm, focused, legible. `stated`
- **Tone / voice:** plain and quiet; no marketing voice, no exclamation marks. `stated`
- **References / anti-references:** "like Instapaper's reading calm"; NOT a social feed, NOT a dashboard. `stated`

## Key screens / moments

> The handful of screens or moments that define the experience — not an exhaustive screen list (that's realization).

- **The reading list is home** — the saved items, newest first; the first thing you see. `stated`
- **The reader is full-bleed and single-column** — just the article text, nothing around it. `stated`

## Design tokens (user-specified only)

> Only tokens the **user** specified or that are brand-mandated. The full token set is realization (skill 02).

| Token | Value | Source |
|-------|-------|--------|
| `color.brand.primary` | `#1A56DB` | stated — used for primary actions and links |

## Interaction principles

- **Archiving is undoable** — removing an item from the list shows an undo affordance; it is never gated behind a
  confirm dialog. `stated`

## Accessibility / constraints

- **WCAG 2.2 AA**, and fully operable by keyboard alone. `stated`
