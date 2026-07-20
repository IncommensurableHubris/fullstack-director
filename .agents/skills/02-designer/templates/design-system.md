<!-- Filename: docs/design/design-system.md  (one per project; grows sprint over sprint). -->

# Design System — <Project Name>

> **The "looks" realization.** Owned by **skill 02 (designer)**. It *references* `design-intent.md` and the spine's
> REQs by ID — it never copies declaration prose. The **semantic-token layer below is the governed intent
> vocabulary**; primitives and component tokens are free realization. Craft method + the *why*:
> `references/design-system.md`. Concretize the seed values below per project — keep the **tiers** and the
> **reference direction** (component → semantic → primitive, never skip).

**Sprint scope:** this iteration realizes REQ-NNN, REQ-NNN, … _(reference the sprint's REQ-IDs — never copy their prose)._

## Style direction

> Derived from `design-intent.md` (brand adjectives, tone, references/anti-references). Cite the source of each call
> so the user has a correction surface: `(from design-intent)` / `(derived — confirm)` / `(craft default)`.

- **Adjectives / mood:** _<calm, precise, trustworthy — from design-intent>_
- **Visual references:** _<"Product — aspect", e.g. "Linear — minimal chrome, keyboard-first">_
- **Anti-references:** _<what to avoid, and why>_
- **Constraints:** _<hard requirements: brand colors, WCAG level, device targets — from the Constitution / design-intent>_

---

## Tokens

> Three tiers. A token only references **inward, toward primitives** (component → semantic → primitive); never skip a
> tier, never reference outward. Theming overrides **semantic only** — primitives never change.

### Primitive (raw values — realization; invent freely)

| Token | Value |
|-------|-------|
| `--color-black` / `--color-white` | `#000000` / `#ffffff` |
| `--color-neutral-{900,700,500,300,100}` | `#171717` `#404040` `#737373` `#d4d4d4` `#f5f5f5` |
| `--color-brand-primary-{light,base,dark}` | _<concretize from design-intent; e.g._ `#eff6ff` `#1A56DB` `#0044cc`_>_ |
| `--color-brand-secondary-{light,base,dark}` | _<…>_ |
| `--color-error-{light,base,dark}` | `#fef2f2` `#ef4444` `#b91c1c` |
| `--color-success-{light,base,dark}` | `#f0fdf4` `#22c55e` `#15803d` |
| `--color-warning-{light,base,dark}` | `#fffbeb` `#f59e0b` `#b45309` |
| `--color-info-{light,base,dark}` | `#eff6ff` `#3b82f6` `#1d4ed8` |
| `--font-family-{base,secondary,mono}` | `'Inter', system-ui, sans-serif` / `<serif>` / `'Fira Code', monospace` |
| `--font-size-{xs…3xl}` | `0.75 · 0.875 · 1 · 1.125 · 1.25 · 1.5 · 2` rem |
| `--space-{xs…3xl}` | `0.25 · 0.5 · 1 · 1.5 · 2 · 3 · 4` rem |
| `--radius-{sm,md,lg,full}` | `0.25rem · 0.5rem · 1rem · 9999px` |
| `--shadow-{sm,md,lg}` | `0 1px 2px / 0 4px 6px / 0 10px 15px` rgba(0,0,0,.05–.1) |
| `--z-{dropdown,sticky,modal,toast}` | `100 · 200 · 300 · 400` (named layers — kills z-index wars) |
| `--transition-{fast,base,slow}` | `150ms · 250ms · 400ms ease` |

### Semantic (roles — **the governed intent vocabulary**)

> Density-as-intent: **`light` = subtle bg / hover · `base` = main / CTA · `dark` = text / pressed.** The name encodes
> *where it's used*. A change to what one of these *means* is a Reconcile-gated amendment, not a silent edit.

| Semantic token | → references | Intent (where it's used) |
|----------------|-------------|--------------------------|
| `--text-primary` | `--color-black` | body text |
| `--text-secondary` | `--color-neutral-500` | muted/secondary text *(verify ≥ 4.5:1 on its bg)* |
| `--text-inverse` | `--color-white` | text on dark/brand fills |
| `--text-link` | `--color-brand-primary-dark` | links *(must pass AA as text)* |
| `--bg-page` / `--bg-surface` / `--bg-elevated` | `--color-white` / `--color-neutral-100` / `--color-white` | page / cards / popovers |
| `--border` | `--color-neutral-300` | dividers, input borders *(≥ 3:1 non-text)* |
| `--shadow` | `--shadow-md` | elevation |
| `--primary-{light,base,dark}` | `--color-brand-primary-{light,base,dark}` | bg/hover · CTA · brand text |
| `--secondary-{light,base,dark}` | `--color-brand-secondary-{light,base,dark}` | bg/hover · accent · accent text |
| `--{error,success,warning,info}-{light,base,dark}` | `--color-{…}-{light,base,dark}` | tint bg · icon/badge · text |

### Component (per-component — realization; references semantic only)

| Component token | → references |
|-----------------|-------------|
| `--button-bg` / `--button-bg-hover` / `--button-fg` | `--primary-base` / `--primary-dark` / `--text-inverse` |
| `--card-bg` / `--card-shadow` / `--card-radius` | `--bg-elevated` / `--shadow` / `--radius-md` |
| _<add only the component tokens this sprint's components need>_ | |

### Theming (semantic override only)

> A theme (e.g. `[data-theme="dark"]`) **reassigns the semantic vars** — densities flip so the *intent* (light=bg,
> dark=text) is stable while the value inverts — and **never touches primitives**. Leave as "Light only" until a
> theme is in scope.

- **Mode:** _<Light only | Light + Dark>_

---

## Component inventory

> Loose hierarchy: **foundations/tokens → components → patterns → screens.** Atomic Design is a *mental model*, not
> rigid buckets. Define only what this sprint's screens use. Note variants · sizes · states for each. The full
> per-component + state contract lives in each `docs/design/<screen>.md`.

| Component | Variants | Sizes | States | Used on |
|-----------|----------|-------|--------|---------|
| Button | primary / secondary / ghost / destructive | sm / md / lg | default · hover · focus · active · disabled · loading | _<screens>_ |
| _<FormField, Card, Header, …>_ | | | | |

---

## Content & UX patterns

> Decide once, project-wide. A declared `design-intent.md` interaction principle is **governed** — honor it or flag a
> contradiction.

- **Empty state:** _<icon + heading + description + CTA | text-only>_
- **Error message format:** `[what happened] + [what to do]` — _<example>_
- **Microcopy voice:** _<formal | casual — align to design-intent tone>_
- **Destructive confirm:** _<when a dialog is warranted + copy pattern>_
- **Loading:** _<skeleton | spinner | optimistic>_
- **Navigation:** _<sidebar | top-nav + breadcrumbs | tabs>_
- **Notification:** _<toast (position + duration) | inline banner>_

---

## Banned / anti-patterns

> AI-slop guardrails — the design analog of a lint config. The reviewer and the detector enforce these.

- Raw/primitive token used directly in a component (bypasses the semantic layer).
- Hardcoded hex/px where a token exists (`#1A56DB` instead of `var(--primary-base)`).
- Palette utilities that bypass semantics (`bg-blue-600` banned; `bg-primary` → token, fine).
- `!important`, inline styles, `outline:none` without a visible focus replacement.
- Color as the **sole** carrier of meaning (status by hue only) — fails WCAG 1.4.1.
- _<project-specific bans>_

---

## Design Decisions (DDRs)

> The design analog of ADRs — one per **gated** design decision (and notable craft calls). `owner: intent` means it
> amended a declaration (it has an `amendment-log.json` row); `owner: craft` is a notable realization call, no
> amendment. Format + the dual-pass that produces these: `references/reconcile-critique.md`.

### DDR-001 · <title>

- **Status:** _<proposed | accepted | superseded>_
- **Linked REQ / job:** _<REQ-NNN | job-outcome | n/a>_
- **Decision:** _<what was chosen>_
- **Alternatives considered:** _<options + why rejected>_
- **Rationale:** _<the anchor — REQ / Nielsen heuristic / WCAG SC / brand intent>_
- **Consequences:** _<what this commits the build to>_
- **Owner:** _<intent (amended a declaration — see AMD-NNN) | craft>_

---

## Interaction flows

> Phase C synthesis — the screen-to-screen map `04-builder` uses for routing. Cover the happy path + key error/edge
> paths; at least one flow per screen.

```
[<screen>] --<action>--> [<screen>] --<action>--> [<screen>]
```
