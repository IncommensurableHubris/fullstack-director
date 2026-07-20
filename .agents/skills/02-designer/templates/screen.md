<!-- Filename: docs/design/<screen-name>.md  (kebab-case; one per key screen). -->

# Screen: <Screen Name>

**Serves:** REQ-NNN, REQ-NNN _(the in-scope REQs this screen realizes — references, never copied prose)._
**Job:** <the one thing the user does here, end-to-end>.

## Wireframe

> ASCII by default (tech-agnostic; the sprint-1 default). Conventions: `+--+` container · `[Button]` · `[____]` input
> · `( dropdown v )` · `[x]/[ ]` checkbox · `(*)/( )` radio · `[Icon:name]` · `@` avatar · `─` divider.

```
+--------------------------------------------------+
|  <wireframe — the layout skeleton for this screen> |
+--------------------------------------------------+
```

## Interaction table

> Every operable element — clickable, tappable, or keyboard-triggerable — gets a row. Count from rows, not memory.

| # | Trigger | Action | Result | Notes |
|---|---------|--------|--------|-------|
| 1 | <Click [Button]> | <what happens internally> | <observable outcome / navigation> | <state / disabled rule> |

### Smart defaults

| Condition | Behavior |
|-----------|----------|
| <only one option> | <auto-select, skip the control> |

## State spec — component contract

> For each non-trivial component: its interface + **every** visual state. The shape `03-architect` / `04-builder`
> consume. An incomplete state list (no empty / error) means the screen isn't specified yet.

### <ComponentName>

- **Attributes:** `<name>` (`<type>`) — <description>
- **Events dispatched:** `app:<event>` — <detail payload>
- **Expected children / slots:** <what composes inside>
- **States:** `default` · `hover` · `focus` · `active/pressed` · `disabled` · `loading` · `error` · `empty`
  — <name the trigger + look of each that applies>

## Accessibility annotations

> The WCAG 2.2 AA floor, per screen. A break in *this screen's* values is fixed here; a break that needs a
> **declaration** to change is a Reconcile contradiction-flag (`references/reconcile-critique.md`).

- **Keyboard / tab order:** <the focus sequence>; shortcuts <…>; no keyboard trap.
- **Focus management:** modal open → <…>; submit success → <…>; submit error → first invalid field; delete → <…>.
- **ARIA / landmarks:** <non-obvious labels, live regions for async status>. Native semantics first; ARIA last.
- **Color & contrast:** text ≥ 4.5:1 (≥ 3:1 large), non-text/UI ≥ 3:1; nothing relies on color alone.

## Responsive behavior

> Mobile-first: design the narrow column first, then widen. Name what moves / hides / stacks / transforms.

| Breakpoint | Layout change |
|------------|---------------|
| `< 768px` (mobile) | <single column; table → cards; nav behind menu> |
| `768–1023px` (tablet) | <stacked panels> |
| `≥ 1024px` (desktop) | <side-by-side; full table> |
