# Specification — BookNook

> **The spec spine: the single source of declaration-truth.** This file is the **INDEX** — the project
> **Constitution** + the **REQ registry** (authoritative ID→file map). Detailed requirements live in
> [`capabilities/`](capabilities/); change history in [`amendment-log.json`](amendment-log.json). Owned by
> **skill 00**. Every other skill *references* REQ-IDs from here.

---

## Constitution (PROTECTED)

> Project-level non-negotiables — violate one and we built the **wrong thing**. Changing an item is Tier 2+.

1. **Personal-first library.** Every bookmark belongs to exactly one owner's library; sharing bookmarks between
   users is out of scope for v1.
2. **Tag over folder.** Organization happens by tag, never by nested folders.
3. **Capture from desktop.** Saving a bookmark is a single action available from desktop; a dedicated mobile app is
   deferred to a future release.
4. **Offline-available.** Once saved, a bookmark's title and URL are readable offline; sync resumes automatically
   when the device is back online.

---

## REQ registry

> The **authoritative** ID→file map — every REQ appears here **exactly once**, updated in the same step as any REQ
> write. **Skill 00 bootstrapped `REQ-001…REQ-005`**; thereafter **skill 01 is the sole allocator**
> (`max(registry)+1`). `Status` = `stated` (traces to a source quote) or `derived` (inferred — a flag for human
> confirmation).

| REQ | Name | Priority | Status | File |
|-----|------|----------|--------|------|
| REQ-001 | Save a bookmark | MUST | stated | capabilities/bookmarks.md |
| REQ-002 | Tag a bookmark | MUST | stated | capabilities/bookmarks.md |
| REQ-003 | Delete a bookmark | MUST | stated | capabilities/bookmarks.md |
| REQ-004 | Search bookmarks by tag | MUST | stated | capabilities/search.md |
| REQ-005 | Read a saved bookmark offline | MUST | stated | capabilities/search.md |

- **Priority** — RFC 2119: `MUST` / `SHOULD` / `MAY`. Drives MoSCoW → sprint assignment in skill 01.
- **Distribution** — 5 `MUST` · 0 `SHOULD` · 0 `MAY`; 5 `stated` · 0 `derived`.

---

## Roadmap (informational)

- CSV import from a legacy browser export — approved.

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
