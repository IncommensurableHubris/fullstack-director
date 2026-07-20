# Screen-spec craft — the "works" realization

> Loaded by skill 02, **Phase B** (Per-screen). How to turn each key screen into a spec rich enough that
> `04-builder` implements it without guessing: a wireframe annotated with REQ-IDs, an interaction table, a state
> spec, a11y annotations, and the **DM-ID manifest** that makes coverage mechanical. Fill-in skeletons:
> `templates/screen.md` (one per screen) and `templates/manifest.md`. Each screen **references** the sprint's REQs by
> ID — it never copies REQ prose (`shared/spine-boundary.md`).

## One screen file per key screen, referencing REQs

Write `docs/design/<screen>.md` (kebab-case) for each screen in the slice. A screen earns a file when it carries a
distinct job from the sprint's REQs — derive the screen set from `design-intent.md`'s **key screens/moments** + the
sprint's REQ blocks, not from the data model. At the top of each screen file, **list the REQ-IDs it serves**
(`Serves: REQ-001, REQ-008`). That back-reference is the traceability the reviewer checks: every in-scope REQ should
be served by at least one screen, and every screen should trace to a REQ.

## Wireframe: ASCII by default at sprint 1, prototype when a stack is known

The wireframe is the layout skeleton. Two modes:

- **ASCII (the default, especially sprint 1).** No architecture exists yet at sprint 1 (that's `03-architect`,
  downstream), so ASCII is **tech-agnostic** and doubles as durable documentation. Announce the choice — don't ask:
  > "No stack is decided yet (architecture is the next skill), so I'm using ASCII wireframes — tech-agnostic and
  > documentation regardless. Say 'use prototypes' if you already know the stack."
- **Prototype (sprint N>1, when `docs/architecture/system.md` names a stack).** Generate real components under
  `prototype/`, review in a browser, and at Gate 2 **lock the prototype as the design contract** (copy to
  `docs/design/approved/sprint-NN/prototype/` + screenshots) — downstream skills verify against it. Keep this path
  available; it is the higher-fidelity contract when a stack is known.

ASCII conventions (consistent so they read unambiguously):

```
+--+ container / card        [Button] clickable button       [____] text input
( dropdown v ) select        [x] / [ ] checkbox              (*) / ( ) radio
[=====---] progress          << 1 2 3 >> pagination          [Icon:name] icon
... truncated content        @ avatar                        ─ divider
```

## Interaction table — every operable element, with its behavior

The single most valuable section for the builder. **Every** clickable / tappable / keyboard-triggerable element gets
a row — count rows from the table, not from memory:

| # | Trigger | Action | Result | Notes |
|---|---------|--------|--------|-------|
| 1 | Click **[Submit]** | record the standup | toast "Saved", entry appears in today's list | disabled until all three prompts filled |
| 2 | Press `Esc` in editor | discard unsaved edits | return to list | confirm dialog if dirty |

Add a **smart-defaults** sub-table where business rules reduce friction (auto-select the only option; pre-fill
last-used values). Make the rules explicit so the builder implements them rather than guessing.

## State spec — the component + state contract

For each non-trivial component on the screen, document the contract `04-builder` (and `03-architect`) consume. This
is the shape proven in the consultancy's component header — an interface, not a sketch:

- **Attributes** — name · type · description (the inputs the component takes).
- **Events dispatched** — `app:<event>` + the detail payload (what it emits outward).
- **Expected children / slots** — what composes inside it.
- **States** — enumerate **every** visual state and its trigger: `default · hover · focus · active/pressed ·
  disabled · loading · error · empty`. A component spec that lists only the happy state is incomplete — the empty
  and error states are where builds diverge most.

State-completeness is a forcing function: if you can't name what the *empty* digest or the *errored* submit looks
like, the screen isn't specified yet.

## Accessibility annotations — the floor, per screen

Annotate each screen against the **WCAG 2.2 AA floor** (the actionable checklist lives in
`references/reconcile-critique.md`; apply it here as *realization quality* — 02 fixes its own design to meet it):

- **Keyboard** — the full tab order (list the focus sequence); shortcuts; no keyboard trap.
- **Focus management** — where focus moves on modal open/close, submit (success → next section; error → first bad
  field), and deletion (→ previous item or empty state).
- **ARIA** — non-obvious labels, landmarks (`header`/`nav`/`main`/`footer`), live regions for async status. ARIA
  **last** — prefer native semantics first.
- **Color & contrast** — flag any element relying on color alone; confirm text ≥ 4.5:1 (≥ 3:1 large), non-text/UI
  ≥ 3:1. A contrast failure traced to a **declared** brand token is not a screen fix — it's a Reconcile
  contradiction-flag (escalate per `reconcile-critique.md`); a contrast failure in a value **you** chose is yours to
  fix here.

## Responsive behavior — mobile-first

State how the screen adapts across breakpoints (mobile-first: design the narrow column first, then widen):

| Breakpoint | Layout change |
|------------|---------------|
| `< 768px` (mobile) | single column; table → card list; nav behind a menu |
| `768–1023px` (tablet) | stacked panels; table scrolls horizontally |
| `≥ 1024px` (desktop) | side-by-side panels; full table |

Name what moves, hides, stacks, or transforms — not just the breakpoints.

## The DM-ID manifest — the coverage forcing-function

After the screens are specified, enumerate every **distinctive** visual element into a manifest at
`docs/design/approved/sprint-NN/manifest.md`, each with a stable **`DM-NNN`** ID. The manifest is what makes
downstream coverage *mechanical*: architecture must cover every DM-ID, build must implement every one, review must
verify every one.

**The inclusion rule (the "side-by-side" test):** an element belongs in the manifest if, **removed from the build, a
non-technical user would immediately notice it** in a side-by-side comparison with the design. Decorative
micro-details below that threshold are not manifest elements. **Cap ~10–15 per screen** — more than that and the
granularity is wrong; re-evaluate against the side-by-side test.

For each element record: **DM-ID · description (specific enough to verify) · location (selector or wireframe
region) · viewports it appears in · required/optional**. If this sprint redesigns a screen from an earlier sprint,
list the superseded DM-IDs in the manifest's `supersedes:` frontmatter.

> **The manifest is generated even on the ASCII path.** DM-IDs are taken over **wireframe regions** (not just
> rendered prototype elements), so the coverage contract exists from sprint 1 with no prototype. Confirm each DM-ID
> traces to a screen spec and, through it, to a REQ — that chain (REQ → screen → DM-ID) is the design contract the
> reviewer attests against.
