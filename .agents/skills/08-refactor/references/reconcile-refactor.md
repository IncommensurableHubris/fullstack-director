# Reconcile (Refactor edition) — local doc fix vs the declaration-amendment appender

> Loaded by `08` at **RECONCILE** (folded into Gate 2). This is `08`'s spine wiring — the appender half. Read with
> `shared/spec-amendment-protocol.md` (the tiers + the row schema), `shared/spine-boundary.md` (the keystone), and
> `references/reconcile-critique`-style stance: **be a critic, not a builder.** Unlike `03`, `08`'s Reconcile runs
> **INLINE** (sequential — no subagent); its sibling is `02`.

## The one routing test — *which file fixes it?*

Every reconcile finding routes by a single, checkable question:

| The refactor reveals… | Fixed by editing… | Disposition |
|---|---|---|
| the code no longer matches `system.md` / a feature spec / `design-system.md` (a **realization**) | that realization doc — **locally** | **No amendment row** |
| a `stated` `architecture-constraints.md` line / a Constitution mandate / a REQ the realization **cannot honor** (a **declaration**) | `docs/spec/**` — via the **amendment protocol** | **A row** (T1 auto / T2 gate / T3 defer) |

A **realization** is anything `08` may correct without asking (the C4 module inventory drifted because you split a
module). A **declaration** is anything the user would object to changing silently (the stated datastore, a stated
"no external services", a capability's scope). **When unsure, treat it as a declaration and escalate** — mis-classifying
*down* silently corrupts intent; *up* costs one extra gate.

## Local reconcile (the common case — most refactor findings)

Correct the realization docs to match the refactored code, **no amendment**:

- **`system.md`** — the §5 building-block inventory (module names, responsibilities), the C4 diagrams, bounded-context
  map. If you split/renamed/removed a module, the inventory changes here. Remove a **documented-but-missing** module
  row (a phantom module the code never had); add an **undocumented-but-exists** module.
- **feature specs** (`docs/architecture/specs/**`) — update a Component Breakdown if module boundaries moved.
- **`design-system.md`** — component-inventory names that must match the actual component files.
- **`.claude/rules/quality-guardrails.md`** — walk it entry-by-entry: a guardrail whose pattern this refactor
  **eliminated** is marked `[RESOLVED — sprint N]` (with the reason) or deleted, so it stops misdirecting the next
  health pass's clustering analysis.

This is the `03` **Step-1b precedent**: *a code↔doc drift is local — it is not the spine's concern.* Emitting an
amendment row for a realization drift is the mis-router failure (it corrupts the appender signal `/status` and `06`
read).

## Declaration reconcile (the appender case — rare, consequential)

Where the refactor makes a **declaration** contradiction undeniable, append a structured row to
`docs/spec/amendment-log.json` (never prose buried in the report). Two shapes:

- **(a) contradiction** — a `stated` constraint the realization *cannot* honor. Worked example (the eval's
  discriminator): `architecture-constraints.md` states **`Datastore: in-memory (embedded, single-process)`**, but the
  scale mandate states **multiple stateless instances behind a load balancer**. An embedded single-process store
  **cannot** be the shared store for multiple stateless nodes — the refactor of the store layer makes it undeniable.
  This is **not** a local fix (you can't correct it by editing `system.md`); it is a **Tier-2** declaration
  contradiction. **Never** silently swap the datastore (the user's stated call) and **never** silently ship the
  contradiction — **gate it**.
- **(b) dead-at-scope** — dead-code removal proves a declared **capability** is unreachable/unbuilt. Is it still
  wanted? That's a **scope** question → **Tier-3 deferred** to `/00 reflect` (a row, `disposition: deferred`,
  `resolved_by: null`) — never delete the REQ yourself.

### The tiers (full semantics in `shared/spec-amendment-protocol.md`)

| Finding | Tier | Disposition |
|---|---|---|
| a `stated` constraint the realization can't honor (named tech / scale) | **Tier 2** | `gated` → `approved` |
| a pure clarification, exactly one defensible answer, no user-observable/named-tech change | Tier 1 | `auto-applied` (rare) |
| honoring it adds/removes/reprioritizes a capability (scope) | **Tier 3** | `deferred` → `/00 reflect` |

### The tech-mandate flow (one trigger, two altitudes) — for an approved Tier-2

Resolve in **both** places, or neither:
1. **Declaration** — amend the `architecture-constraints.md` line (e.g. `Datastore: in-memory` → `Datastore:
   PostgreSQL (client-server)`).
2. **Realization** — record a **resolving ADR** (`resolved_by`). `08` **requests `max+1`** from `03`'s
   `adr/README.md` index (`03` is the sole allocator); the ADR's *Decision* names the replacement, its *Rule* makes it
   checkable. The migration itself is **structural → plan-only**, routed to `/03`→/04` (Strangler Fig).

Batch every Tier-2 finding into the **single** Gate 2 — never interrupt once per finding. Exclude anything an existing
ADR already settled.

## The row schema (append to the existing `{ "amendments": [ … ] }` array)

```json
{
  "id": "AMD-003",
  "req": null,
  "skill": "08-refactor",
  "tier": 2,
  "disposition": "approved",
  "source_quote": "architecture-constraints.md: 'Datastore: in-memory (embedded, single-process)' vs 'multiple stateless instances behind a load balancer' — an embedded single-process store cannot back multiple stateless instances",
  "supersedes": null,
  "resolved_by": "ADR-003"
}
```

- `id` — `AMD-NNN`, `max(existing)+1`. `req` — the REQ if REQ-scoped, else `null`.
- `source_quote` — the **exact declaration text** the finding is about (quote the constraint **and** what it collides
  with), so a reviewer sees the contradiction without diffing. **No `date`** — git is the trail.
- `disposition` — a gated Tier-2 is `approved` once accepted at Gate 2 (`pending` only if logged before it resolves).

## The over-trigger guard

A clean, fully-honored envelope yields **~zero** amendments. Before logging a row, confirm the finding (a) is anchored
in a **stated** declaration and (b) genuinely **cannot** be fixed locally. A nice-to-have, a future idea, or a
delegated-layer preference is **not** an amendment — it is a local fix or out of scope. Inventing a declaration row on
clean code is the crying-wolf failure the eval's `clean` case guards against.
