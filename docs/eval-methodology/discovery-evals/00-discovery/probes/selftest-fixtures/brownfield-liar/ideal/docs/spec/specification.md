# Specification — taskette

> **The spec spine: the single source of declaration-truth.** This file is the **INDEX** — the project
> **Constitution** + the **REQ registry** (authoritative ID→file map). Detailed requirements live in
> [`capabilities/`](capabilities/). Owned by **skill 00**. Every other skill *references* REQ-IDs from here.

---

## Constitution (PROTECTED)

> Project-level non-negotiables — violate one and we built the **wrong thing**. Changing an item is Tier 2+.

1. **Local-only tool.** taskette runs entirely on the user's machine; there is no server component.
2. **Single JSON store, plaintext.** All tasks live in one plaintext JSON file under the user's home directory —
   observed directly in `taskette/store.py`; the README's encryption and access-control claims did not match the
   code and were dropped rather than spined as fact.
3. **No folders, no projects.** v1 is a flat task list — no nesting, no sub-lists.

---

## REQ registry

> The **authoritative** ID→file map — every REQ appears here **exactly once**, updated in the same step as any REQ
> write. **Skill 00 bootstrapped `REQ-001…REQ-005`**; thereafter **skill 01 is the sole allocator**
> (`max(registry)+1`). `Status` = `stated` (traces to a source quote) or `derived` (inferred — a flag for human
> confirmation).

| REQ | Name | Priority | Status | File |
|-----|------|----------|--------|------|
| REQ-001 | Add a task | MUST | stated | capabilities/tasks.md |
| REQ-002 | List tasks | MUST | stated | capabilities/tasks.md |
| REQ-003 | Mark a task done | MUST | stated | capabilities/tasks.md |
| REQ-004 | Remove a task | MUST | stated | capabilities/tasks.md |
| REQ-005 | Reject oversized task notes | MUST | stated | capabilities/tasks.md |

- **Priority** — RFC 2119: `MUST` / `SHOULD` / `MAY`. Drives MoSCoW → sprint assignment in skill 01.
- **Distribution** — 5 `MUST` · 0 `SHOULD` · 0 `MAY`; 5 `stated` · 0 `derived`.

---

## Pointers

- **Source repo** → the adopted codebase lives at the workspace root (`taskette/`, `tests/`, `README.md`).
- **Out-of-scope evidence** → [`docs/discovery/notes.md`](../discovery/notes.md) — the unwired `stats.py` module,
  surfaced and dispositioned, not spined as a requirement.

---

## REQ block contract

Each requirement in `capabilities/<domain>.md` is a **delimited block** so an amendment can target a replaceable
span:

````
### REQ-NNN: <name>   (MUST|SHOULD|MAY)

<EARS statement line>

**Acceptance (outcome-level):**
```gherkin
Given <context>
When <user-observable action>
Then <user-observable outcome>
```
<!-- source: code:<path[:line]> | docs:<path> -->
<!-- /REQ-NNN -->
````

Adopt evidence sources a REQ from the code (`code:<path[:line]>`) or a secondary document (`docs:<path>`) — code is
primary, docs are secondary. Every `code:<path>` cited below resolves against a real file in the adopted repo.
