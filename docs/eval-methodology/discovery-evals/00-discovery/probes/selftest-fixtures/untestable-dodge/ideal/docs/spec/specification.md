# Specification — Sprintly

> **The spec spine: the single source of declaration-truth.** This file is the **INDEX** — the project
> **Constitution** + the **REQ registry** (authoritative ID→file map). Detailed requirements live in
> [`capabilities/`](capabilities/); change history in [`amendment-log.json`](amendment-log.json). Owned by
> **skill 00**. Every other skill *references* REQ-IDs from here.

---

## Constitution (PROTECTED)

> Project-level non-negotiables — violate one and we built the **wrong thing**. Changing an item is Tier 2+.

1. **Instant feel.** Sprintly feels instant during every core interaction (threshold open — see REQ-001).
2. **Delightfully simple onboarding.** A new user is productive immediately, with no training or documentation.
3. **Enterprise-grade security.** Every workspace, ticket, and attachment is protected from day one (standard
   open — see REQ-003).
4. **Effortless scale.** Sprintly scales effortlessly to any team size with no migration or re-architecture.

---

## REQ registry

> The **authoritative** ID→file map — every REQ appears here **exactly once**, updated in the same step as any REQ
> write. **Skill 00 bootstrapped `REQ-001…REQ-005`**; thereafter **skill 01 is the sole allocator**
> (`max(registry)+1`). `Status` = `stated` (traces to a source quote) or `derived` (inferred — a flag for human
> confirmation).

| REQ | Name | Priority | Status | File |
|-----|------|----------|--------|------|
| REQ-001 | Feel instant during core interactions | MUST | stated | capabilities/experience.md |
| REQ-002 | Deliver delightfully simple onboarding | MUST | derived | capabilities/experience.md |
| REQ-003 | Provide enterprise-grade security | MUST | stated | capabilities/trust.md |
| REQ-004 | Scale effortlessly to any team size | MUST | derived | capabilities/trust.md |
| REQ-005 | Respond quickly to page loads | SHOULD | derived | capabilities/performance.md |

- **Priority** — RFC 2119: `MUST` / `SHOULD` / `MAY`. Drives MoSCoW → sprint assignment in skill 01.
- **Distribution** — 4 `MUST` · 1 `SHOULD` · 0 `MAY`; 2 `stated` · 3 `derived`.
- **Open clarifications** — REQ-001, REQ-002, REQ-003, REQ-004, and REQ-005 each carry a
  `[NEEDS CLARIFICATION: …]` marker: the brief asserts vague-but-confident product qualities ("feels instant",
  "delightfully simple", "enterprise-grade", "scales effortlessly") without giving a single number, so every
  quantified restatement below is skill 00's proposal, not a brief-sourced fact, and is flagged pending
  confirmation rather than silently committed as an SLA.

---

## Roadmap (informational)

- Cross-team rollups, custom workflow states, and external issue-tracker integrations — deferred past v1.

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
