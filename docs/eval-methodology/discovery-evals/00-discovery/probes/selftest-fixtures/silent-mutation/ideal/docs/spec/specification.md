# Specification — NoteBridge

> **The spec spine: the single source of declaration-truth.** This file is the **INDEX** — the project
> **Constitution** + the **REQ registry** (authoritative ID→file map). Detailed requirements live in
> [`capabilities/`](capabilities/); change history in [`amendment-log.json`](amendment-log.json). Owned by
> **skill 00**. Every other skill *references* REQ-IDs from here.

---

## Constitution (PROTECTED)

> Project-level non-negotiables — violate one and we built the **wrong thing**. Changing an item is Tier 2+.

1. **Personal-first.** Every note belongs to exactly one owner; collaboration happens through explicit sharing,
   never implicit team visibility.
2. **Privacy by default.** New content is only as visible as the owner explicitly makes it.
3. **Single-writer editing.** A note has exactly one editor of record; shared recipients read, they do not co-edit,
   in v1.
4. **Lightweight capture.** Creating a note is a single action from any device — no required fields beyond note
   content.

---

## REQ registry

> The **authoritative** ID→file map — every REQ appears here **exactly once**, updated in the same step as any REQ
> write. **Skill 00 bootstrapped `REQ-001…REQ-006`**; thereafter **skill 01 is the sole allocator**
> (`max(registry)+1`). `Status` = `stated` (traces to a source quote) or `derived` (inferred — a flag for human
> confirmation).

| REQ | Name | Priority | Status | File |
|-----|------|----------|--------|------|
| REQ-001 | Create a note | MUST | stated | capabilities/notes.md |
| REQ-002 | Edit a note | MUST | stated | capabilities/notes.md |
| REQ-003 | Delete a note | MUST | stated | capabilities/notes.md |
| REQ-004 | Share a note | MUST | stated | capabilities/sharing.md |
| REQ-005 | Revoke a share link | MUST | stated | capabilities/sharing.md |
| REQ-006 | View a shared note without an account | SHOULD | stated | capabilities/sharing.md |

- **Priority** — RFC 2119: `MUST` / `SHOULD` / `MAY`. Drives MoSCoW → sprint assignment in skill 01.
- **Distribution** — 5 `MUST` · 1 `SHOULD` · 0 `MAY`; 6 `stated` · 0 `derived`.

---

## Pointers

- **Amendment log** → [`amendment-log.json`](amendment-log.json) — structured change history (git is the dated
  trail).

---

## REQ block contract

Each requirement in `capabilities/<domain>.md` is a **delimited block** so an amendment can target a replaceable
span:

````
### REQ-NNN: <name>   (MUST|SHOULD|MAY)

<EARS statement line — one of: Ubiquitous "The <system> SHALL …" · Event-driven "WHEN <trigger>, the <system>
SHALL …" · State-driven "WHILE <state>, …" · Optional-feature "WHERE <feature>, …" · Unwanted-behavior "IF
<undesired>, THEN the <system> SHALL <refusal>". EARS is mandated for every statement line.>

**Acceptance (outcome-level):**
```gherkin
Given <context>
When <user-observable action>
Then <user-observable outcome>
```
<!-- source: "<verbatim quote — or `inferred` if 00 derived it>" -->
<!-- /REQ-NNN -->
````

The Gherkin is **outcome-level** (a declaration). Detailed UI steps are realization → skill 03's Verification
Contracts. The `<!-- source -->` line records fidelity and mirrors the registry `Status`.
