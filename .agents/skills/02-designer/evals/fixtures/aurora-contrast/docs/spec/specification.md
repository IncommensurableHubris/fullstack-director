# Specification — Aurora

> **The spec spine: the single source of declaration-truth.** This file is the **INDEX**. It holds the project
> **Constitution** (non-negotiables) and the **REQ registry** (the authoritative ID→file map). Detailed requirements
> live in [`capabilities/`](capabilities/) `<domain>.md` files; design intent in
> [`design-intent.md`](design-intent.md); architecture mandates in
> [`architecture-constraints.md`](architecture-constraints.md); the change history in
> [`amendment-log.json`](amendment-log.json).
>
> Owned by **skill 00 (discovery)**. Every other skill *references* REQ-IDs from here — it does **not** copy
> requirement text into its own artifacts.

---

## Constitution (PROTECTED)

> Project-level non-negotiables: the principles that, if violated, mean we built the **wrong thing**. On any
> product/scope question, the Constitution **wins**. Changing a Constitution item is always **Tier 2 or higher**.

1. **Single-user, local-first.** No accounts, servers, or cloud sync in v1 — all data lives on the user's own device.
2. **WCAG 2.2 AA is the floor.** Every screen meets WCAG 2.2 AA; nothing ships below it.
3. **Calm and distraction-free.** The list and the reader stay uncluttered — reading is the point. No badges, streaks,
   counts, or social signals.
4. **Keyboard-first.** Every action is reachable without a mouse.

---

## REQ registry

> The **authoritative** ID→file map — every REQ across all `capabilities/` files appears here **exactly once**.
> Updated in the **same step** as any REQ write. **Skill 01 (planner) is the sole allocator** once the spine exists;
> any other skill needing a new ID requests `max(registry)+1`.

| REQ | Name | Priority | Status | File |
|-----|------|----------|--------|------|
| REQ-001 | Save a link to the reading list | MUST | stated | capabilities/library.md |
| REQ-002 | Browse the reading list | MUST | stated | capabilities/library.md |
| REQ-003 | Open an item and mark it read | MUST | stated | capabilities/reader.md |

- **Priority** — RFC 2119: `MUST` / `SHOULD` / `MAY`.
- **Status** — `stated` (traces to a user source quote) or `derived` (inferred).

---

## Pointers

- **Design intent** → [`design-intent.md`](design-intent.md) — declared look/feel, brand, key screens, tokens.
- **Architecture constraints** → [`architecture-constraints.md`](architecture-constraints.md).
- **Amendment log** → [`amendment-log.json`](amendment-log.json) — structured change history (git is the dated trail).

---

## REQ block contract (how each `capabilities/<domain>.md` requirement is written)

Each requirement is a **delimited block** so an amendment can target a findable, replaceable span:

````
### REQ-NNN: <name>   (MUST|SHOULD|MAY)

<one-line statement of the capability>

**Acceptance (outcome-level):**
```gherkin
Given <context>
When <user-observable action>
Then <user-observable outcome>
```
<!-- source: "<verbatim quote — or `inferred` if 00 derived it>" -->
<!-- /REQ-NNN -->
````

The Gherkin here is **outcome-level** — a *declaration*. Detailed UI steps are **realization** (skill 03's
feature-spec Verification Contracts), not here.

---

## Open `[NEEDS CLARIFICATION]` markers

> Carried from the REVIEW gate. **06-release blocks deploy** on any survivor.

- _(none)_
