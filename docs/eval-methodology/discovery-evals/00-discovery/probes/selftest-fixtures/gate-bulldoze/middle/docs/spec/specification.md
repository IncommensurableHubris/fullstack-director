# Specification — PlantPal

> **The spec spine: the single source of declaration-truth.** This file is the **INDEX** — the project
> **Constitution** + the **REQ registry** (authoritative ID→file map). Detailed requirements live in
> [`capabilities/`](capabilities/). Owned by **skill 00**. Every other skill *references* REQ-IDs from here.

---

## Constitution (PROTECTED)

> Project-level non-negotiables — violate one and we built the **wrong thing**. Changing an item is Tier 2+.

1. **Reminder-first.** Every plant has a watering reminder; PlantPal's core job is never letting a plant go
   unwatered.
2. **Per-plant schedule.** Each plant keeps its own watering interval — there is no single global schedule.
3. **On-device reminders.** Reminders fire as local notifications; correctness never depends on a server being
   reachable at reminder time.
4. **Single-user v1.** No shared households or multi-user plant lists in v1.

---

## REQ registry

> The **authoritative** ID→file map — every REQ appears here **exactly once**, updated in the same step as any REQ
> write. **Skill 00 bootstrapped `REQ-001…REQ-005`**; thereafter **skill 01 is the sole allocator**
> (`max(registry)+1`). `Status` = `stated` (traces to a source quote) or `derived` (inferred — a flag for human
> confirmation).

| REQ | Name | Priority | Status | File |
|-----|------|----------|--------|------|
| REQ-001 | Add a plant | MUST | stated | capabilities/plants.md |
| REQ-002 | Set a custom watering interval per plant | MUST | stated | capabilities/plants.md |
| REQ-003 | Receive a watering reminder notification | MUST | stated | capabilities/reminders.md |
| REQ-004 | Mark a plant as watered | MUST | stated | capabilities/reminders.md |
| REQ-005 | Snooze a single reminder | SHOULD | stated | capabilities/reminders.md |

- **Priority** — RFC 2119: `MUST` / `SHOULD` / `MAY`. Drives MoSCoW → sprint assignment in skill 01.
- **Distribution** — 4 `MUST` · 1 `SHOULD` · 0 `MAY`; 5 `stated` · 0 `derived`.

---

## Pointers

- **Capabilities** → [`capabilities/plants.md`](capabilities/plants.md),
  [`capabilities/reminders.md`](capabilities/reminders.md).

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
