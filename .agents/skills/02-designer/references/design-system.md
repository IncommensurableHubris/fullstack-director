# Design-system craft — the "looks" realization

> Loaded by skill 02, **Phase A** (Foundation). How to turn the thin `design-intent.md` declaration + the sprint's
> REQs into a full design system: tiered tokens, a component hierarchy, content/UX patterns, and a banned-list. The
> concrete fill-in artifact is `templates/design-system.md` (it ships the *seed token vocabulary*); this file is the
> **method** and the **why**. The boundary it serves: the **semantic-token layer is the governed intent**; primitive
> values and component internals are free realization — see `shared/spine-boundary.md` (repo-root-relative, per the
> framework's no-`../` rule).

## The design system is a tiered token set, plus what consumes it

A design system that `04-builder` can implement without guessing has a **token spine**: three tiers, with named
references between them and a single rule about which way the references point.

1. **Primitive** (raw values) — the palette: `--color-blue-600: #1A56DB`, `--space-md: 1rem`. No meaning, just values.
   Primitives are **realization** — invent them freely; the user never declared `#1A56DB` specifically.
2. **Semantic** (roles) — what a value is *for*: `--text-link`, `--bg-surface`, `--primary-base`. A semantic token
   **references a primitive** (`--text-link: var(--color-blue-600)`). The semantic layer **is the governed intent
   vocabulary** — the place a brand decision or an a11y floor is encoded. This is the layer the Reconcile step
   guards (see `references/reconcile-critique.md`).
3. **Component** (per-component) — `--button-bg`, `--card-shadow`. A component token **references a semantic token**
   (`--button-bg: var(--primary-base)`), never a primitive. Component tokens are realization — free craft.

**Reference direction (the one rule that keeps the system coherent):** a token only ever references **inward, toward
primitives** — component → semantic → primitive. **Never skip a tier**, and **never reference outward**. A component
that reaches past the semantic layer to grab a raw `--color-blue-600` has broken the chain: re-theming, brand
changes, and contrast fixes all flow through the semantic layer, and a component that bypassed it won't get them.
This shape is the W3C **DTCG** model (`$value`/`$type`/`$description`, aliases) expressed as CSS custom properties;
markdown tables are an acceptable *human view* of the same tiers, but keep the reference direction visible so the
chain is auditable.

> **Why this matters for Reconcile.** The token reference-chain **is the traceability spine** of the design. A
> contradiction (a brand color that fails contrast, a component hardcoding a hex) is a *realization node violating
> the intent node it points to* — a mechanically findable break, not a matter of taste. The detector in
> `reconcile-critique.md` walks exactly these chains.

## Density-as-intent — the semantic naming convention

Each brand and status role carries **three densities**, and the density name encodes **where the value is used**, not
just how light it is:

- **`light`** = subtle background / hover state
- **`base`** = the main color / the CTA
- **`dark`** = text / pressed state

So `--primary-base` is the button fill, `--primary-dark` is brand-colored *text*, `--primary-light` is a tinted
*background*. This is what makes theming a **semantic-override-only** operation: a dark theme reassigns the semantic
vars (and the densities **flip** — `--error-light` goes from a near-white tint to a dark-red background) while the
*intent* (light = bg, base = main, dark = text) stays stable and primitives never change. Intent (governed) and
per-theme value (realization) live side by side in one place — the cleanest illustration of the spine boundary.

## The seed semantic vocabulary — concretize, don't reinvent

`templates/design-system.md` ships a **ready-made seed vocabulary** (global / brand / status semantic tokens +
type / spacing / radius / shadow scales + named z-index layers). Start there and **concretize per project** rather
than inventing a structure each time:

- **Global:** `--text-{primary,secondary,inverse,link}` · `--bg-{page,surface,elevated}` · `--border` · `--shadow`
- **Brand:** `--{primary,secondary}-{light,base,dark}`
- **Status:** `--{error,success,warning,info}-{light,base,dark}`
- **Scales:** type (`xs → 3xl`), spacing (`xs → 3xl`), radius (`sm/md/lg/full`), shadow (`sm/md/lg`)
- **Named z-index** (kills z-index wars): `dropdown 100 · sticky 200 · modal 300 · toast 400`

What you **derive** is the primitive values behind these roles (the actual hexes, the type family) — driven by
`design-intent.md`'s brand/feel. What you **must not silently invent** is a brand fact the user would object to:
if `design-intent.md` declares a brand color, the semantic `--primary-base` references *that*; if it declares none
(or a `derived` one), proposing a concrete brand is a **Reconcile flesh-out** (Tier-2 gate), not a quiet default.

## Component inventory — a loose hierarchy, not rigid buckets

Inventory the components this sprint's screens need, organized as a **loose hierarchy**:

> **foundations / tokens → components → patterns → screens**

Atomic Design (atoms → molecules → organisms → templates → pages) is a useful **mental model** for "small things
compose into big things" — but treat it as a model, **not five rigid buckets you must sort every element into**.
Brad Frost (its author) demoted the dogma himself and added tokens as a "subatomic" layer; enterprise practice finds
the strict five-level taxonomy more friction than signal. So: name a Button, a FormField, a Header, a DigestList —
note variants, sizes, and states for each — without agonizing over whether FormField is a "molecule" or an
"organism." **Define only the components this sprint actually uses** (the slice is thin; the system grows with it).

For each component, capture the shape `04-builder` and `03-architect` will consume — its **contract** (attributes,
events, expected children) and its **states**. The full per-component + state contract lives in
`references/screen-spec.md`; the inventory here is the index of what exists.

## Content & UX patterns

Decide these **once**, project-wide, so screens don't each improvise — inconsistency here is the most visible kind:

- **Empty state** — icon + heading + description + CTA, or text-only? Pick one shape.
- **Error message format** — `[what happened] + [what to do]` ("Couldn't load your digests. Check your connection
  and retry.").
- **Microcopy voice** — formal vs casual; align it to `design-intent.md`'s tone/voice.
- **Destructive-action confirmation** — what warrants a dialog, and the copy pattern ("This permanently deletes X.
  This can't be undone.").
- **Loading** — skeleton vs spinner vs optimistic; pick a default.
- **Navigation** — sidebar / top-nav + breadcrumbs / tabs.
- **Notification** — toast (position + duration) vs inline banner.

These are realization (free craft) **unless** `design-intent.md` declared an interaction principle — e.g.
"destructive actions always confirm; everything else is undoable." A declared principle is **governed**: honor it,
and if your pattern would violate it, that's a Reconcile contradiction-flag, not a silent override.

## The banned / anti-patterns list — AI-slop guardrails

Every design system carries an explicit **banned list** so the build can't drift into generic defaults. Seed it from
`templates/design-system.md` and extend per project. Typical bans:

- Raw/primitive tokens used directly in a component (bypassing the semantic layer) — the reference-direction
  violation above.
- Hardcoded hex / px values where a token exists (`background: #1A56DB` instead of `var(--primary-base)`).
- Tailwind palette utilities that bypass semantics (`bg-blue-600` banned; `bg-primary` mapped to a token, fine).
- `!important`, inline styles, and `outline: none` without a visible focus replacement (an a11y-floor break).
- Color as the **sole** carrier of meaning (a status shown only by hue) — fails WCAG 1.4.1.

The banned list is the design analog of a lint config: it turns "don't produce AI slop" into checkable rules a
reviewer (and the detector) can enforce.

## Design quality — what "good" means (and what the eval deliberately does *not* grade)

Aim the *craft* at four criteria, in priority order for an AI builder:

1. **Design quality** — does the set of screens feel like a **coherent whole** with a distinct mood that matches
   `design-intent.md`'s adjectives?
2. **Originality** — are there **custom decisions**, or is this raw library defaults? (Watch the banned-list slop.)
3. **Craft** — are typography scale, spacing rhythm, and color relationships sound?
4. **Functionality** — can a user complete the slice's job without guessing? (This is where the **JTBD test** and
   Nielsen heuristics in `reconcile-critique.md` bite.)

**Design beauty is subjective and is *not* what the eval grades** — a strong builder also designs well. The graded
lift is **structural**: a tiered-token system that *references REQs*, the DM-ID manifest, the WCAG-checked amendment
rows, and the DDRs. Spend craft on quality because the user sees it; rely on structure for the contract the next
skills consume.
