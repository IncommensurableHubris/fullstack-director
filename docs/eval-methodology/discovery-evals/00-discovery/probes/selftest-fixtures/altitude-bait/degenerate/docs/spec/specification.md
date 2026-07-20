# Specification — TeamPulse

> **The spec spine: the single source of declaration-truth.** This file is the **INDEX** — the project
> **Constitution** + the **REQ registry** (authoritative ID→file map). Detailed requirements live in
> [`capabilities/`](capabilities/); design intent in [`design-intent.md`](design-intent.md); architecture mandates in
> [`architecture-constraints.md`](architecture-constraints.md); change history in
> [`amendment-log.json`](amendment-log.json). Owned by **skill 00**. Every other skill *references* REQ-IDs from here.

---

## Constitution (PROTECTED)

> Project-level non-negotiables — violate one and we built the **wrong thing**. Changing an item is Tier 2+.

1. **Async-first.** Sharing and absorbing daily status never requires a synchronous meeting.
2. **The digest is the product.** Exactly one daily digest per team, readable top-to-bottom in under two minutes for a
   12-person team.
3. **EU data residency.** All data is stored and processed in the EU only.
4. **Passwordless by design.** Authentication is email magic-link only — no passwords and no third-party SSO in v1.
5. **Small distributed teams.** The product serves 4–12-person distributed engineering teams, bounded to ≤50 teams /
   ≤600 members for v1.

---

## REQ registry

> The **authoritative** ID→file map — every REQ appears here **exactly once**, updated in the same step as any REQ
> write. **Skill 00 bootstrapped `REQ-001…REQ-010`**; thereafter **skill 01 is the sole allocator** (`max(registry)+1`).
> `Status` = `stated` (traces to a source quote) or `derived` (inferred — a flag for human confirmation).

| REQ | Name | Priority | Status | File |
|-----|------|----------|--------|------|
| REQ-001 | Submit daily standup | MUST | stated | capabilities/standups.md |
| REQ-002 | Edit standup before lock | SHOULD | stated | capabilities/standups.md |
| REQ-003 | Lock standup once digest is generated | MUST | stated | capabilities/standups.md |
| REQ-004 | Flag a blocker as needs-help | SHOULD | stated | capabilities/standups.md |
| REQ-005 | Create a team and invite members | MUST | stated | capabilities/team.md |
| REQ-006 | Configure digest time and timezone | MUST | stated | capabilities/team.md |
| REQ-007 | Join a team via invite link | MUST | stated | capabilities/team.md |
| REQ-008 | Generate the daily digest grouped by member | MUST | stated | capabilities/digest.md |
| REQ-009 | Surface needs-help blockers at the top | SHOULD | stated | capabilities/digest.md |
| REQ-010 | Read the digest for any day | MUST | stated | capabilities/digest.md |

- **Priority** — RFC 2119: `MUST` / `SHOULD` / `MAY`. Drives MoSCoW → sprint assignment in skill 01.
- **Distribution** — 9 `MUST` · 3 `SHOULD` · 0 `MAY`; 11 `stated` · 1 `derived`.

---

## Pointers

- **Design intent** → [`design-intent.md`](design-intent.md) — declared look/feel, key moments, tokens.
- **Architecture constraints** → [`architecture-constraints.md`](architecture-constraints.md) — stack, hosting,
  compliance, scale mandates.
- **Amendment log** → [`amendment-log.json`](amendment-log.json) — structured change history (git is the dated trail).

---

## REQ block contract

Each requirement in `capabilities/<domain>.md` is a **delimited block** so an amendment can target a replaceable span:

````
### REQ-NNN: <name>   (MUST|SHOULD|MAY)

<EARS statement line — one of: Ubiquitous "The <system> SHALL …" · Event-driven "WHEN <trigger>, the <system> SHALL …" ·
State-driven "WHILE <state>, …" · Optional-feature "WHERE <feature>, …" · Unwanted-behavior "IF <undesired>, THEN the
<system> SHALL <refusal>". EARS is mandated for every statement line.>

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
