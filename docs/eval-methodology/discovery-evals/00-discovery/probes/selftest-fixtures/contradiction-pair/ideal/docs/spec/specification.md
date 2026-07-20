# Specification — FieldLog

> **The spec spine: the single source of declaration-truth.** This file is the **INDEX** — the project
> **Constitution** + the **REQ registry** (authoritative ID→file map). Detailed requirements live in
> [`capabilities/`](capabilities/); change history in [`amendment-log.json`](amendment-log.json). Owned by
> **skill 00**. Every other skill *references* REQ-IDs from here.

---

## Constitution (PROTECTED)

> Project-level non-negotiables — violate one and we built the **wrong thing**. Changing an item is Tier 2+.

1. **Offline-first capture.** Every core capture workflow works end to end with zero network connectivity.
   Carried with an open `[NEEDS CLARIFICATION]` against REQ-001/REQ-002 — see below.
2. **Zero on-device retention of customer data.** No customer data may ever be stored on the device. Carried with
   the same open `[NEEDS CLARIFICATION]` against REQ-001/REQ-002.
3. **Hard delete on request.** A survey lead's deletion request removes a record immediately and permanently.
   Carried with an open `[NEEDS CLARIFICATION]` against REQ-004/REQ-005 — see below.
4. **Immutable audit trail.** Every change to every record is preserved in an append-only audit log. Carried with
   the same open `[NEEDS CLARIFICATION]` against REQ-004/REQ-005.
5. **Small crews.** v1 serves 2–15-person survey crews running short-duration projects.

---

## REQ registry

> The **authoritative** ID→file map — every REQ appears here **exactly once**, updated in the same step as any REQ
> write. **Skill 00 bootstrapped `REQ-001…REQ-006`**; thereafter **skill 01 is the sole allocator**
> (`max(registry)+1`). `Status` = `stated` (traces to a source quote) or `derived` (inferred — a flag for human
> confirmation).

| REQ | Name | Priority | Status | File |
|-----|------|----------|--------|------|
| REQ-001 | Capture a record fully offline | MUST | stated | capabilities/capture.md |
| REQ-002 | Never store customer data on the device | MUST | stated | capabilities/capture.md |
| REQ-003 | Tag a record with GPS coordinates | MUST | stated | capabilities/capture.md |
| REQ-004 | Hard-delete a record on request | MUST | stated | capabilities/records.md |
| REQ-005 | Maintain an immutable audit log | MUST | stated | capabilities/records.md |
| REQ-006 | Export a survey's records as CSV | SHOULD | stated | capabilities/records.md |

- **Priority** — RFC 2119: `MUST` / `SHOULD` / `MAY`. Drives MoSCoW → sprint assignment in skill 01.
- **Distribution** — 5 `MUST` · 1 `SHOULD` · 0 `MAY`; 6 `stated` · 0 `derived`.

---

## Roadmap (informational)

- Multi-team coordination and live crew-to-crew messaging — deferred past v1.

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
