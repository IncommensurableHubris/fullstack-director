# Specification — TeamPulse

> **The spec spine: the single source of declaration-truth.** This file is the **INDEX**. It holds the project
> **Constitution** (non-negotiables) and the **REQ registry** (the authoritative ID→file map). Detailed
> requirements live in [`capabilities/`](capabilities/) `<domain>.md` files; design intent in
> [`design-intent.md`](design-intent.md); architecture mandates in
> [`architecture-constraints.md`](architecture-constraints.md); the change history in
> [`amendment-log.json`](amendment-log.json).
>
> Owned by **skill 00 (discovery)**. Every other skill *references* REQ-IDs from here — it does **not** copy
> requirement text into its own artifacts. What belongs in the spine vs. a skill artifact is decided by the
> declaration-vs-realization test — a declaration is anything you'd object to changing silently.

---

## Constitution (PROTECTED)

> Project-level non-negotiables: the principles that, if violated, mean we built the **wrong thing**. On any
> product/scope question, the Constitution **wins**. Changing a Constitution item is always **Tier 2 or higher**.
> Keep to **3–7 durable statements**.

1. **Async over synchronous.** The product replaces the standup *meeting* — status is shared and absorbed without
   anyone attending a synchronous call. No feature may reintroduce a required real-time gathering.
2. **The daily digest is the one artifact.** The whole team stays in sync by reading a single daily digest that
   reads top-to-bottom in under two minutes for a 12-person team; brevity and legibility win over completeness.
3. **Timezone-fair.** No member is penalized for their timezone; the experience must not advantage whoever is
   closest to a chosen hour.
4. **EU data residency.** All data stays in the EU region.
5. **Passwordless by design.** Authentication is email magic-link only — no passwords and no third-party SSO in v1.
6. **Zero-training setup.** A lead can stand up a team and have members contributing within one day with no training.

---

## REQ registry

> The **authoritative** ID→file map — every REQ across all `capabilities/` files appears here **exactly once**.
> Updated in the **same step** as any REQ write. **Skill 00 bootstraps the initial IDs** (`REQ-001…`) when it first
> writes the spine; **thereafter skill 01 (planner) is the sole allocator** — any other skill that needs a new ID
> requests `max(registry)+1`. `/status` integrity-checks that every `File` resolves and contains that REQ's
> delimited block.

| REQ | Name | Priority | Status | File |
|-----|------|----------|--------|------|
| REQ-001 | Submit a daily standup | MUST | stated | capabilities/standups.md |
| REQ-002 | Edit a standup until the digest locks it | SHOULD | stated | capabilities/standups.md |
| REQ-003 | Flag a blocker as "needs help" | SHOULD | stated | capabilities/standups.md |
| REQ-004 | Create a team and invite members by email | MUST | stated | capabilities/team.md |
| REQ-005 | Configure the team's digest time and timezone | MUST | stated | capabilities/team.md |
| REQ-006 | Join a team via invite link and set a display name | MUST | stated | capabilities/team.md |
| REQ-007 | Sign in with an email magic-link | MUST | derived | capabilities/team.md |
| REQ-008 | Generate one daily digest grouped by member | MUST | stated | capabilities/digest.md |
| REQ-009 | Surface "needs help" blockers at the top | SHOULD | stated | capabilities/digest.md |
| REQ-010 | Read current and past digests | SHOULD | stated | capabilities/digest.md |

- **Priority** — RFC 2119: `MUST` / `SHOULD` / `MAY`. Drives MoSCoW → sprint assignment in skill 01.
- **Status** — `stated` (traces to a user source quote) or `derived` (inferred). A `derived` REQ is a flag for
  human confirmation, not a silent fact. REQ-007 is `derived`: the PRD states magic-link as the only auth
  *mechanism* (a constraint) but not the user-facing sign-in capability.

---

## Pointers

- **Design intent** → [`design-intent.md`](design-intent.md) — declared look/feel, brand, key screens, tokens.
- **Architecture constraints** → [`architecture-constraints.md`](architecture-constraints.md) — stack, hosting,
  compliance, scale mandates.
- **Amendment log** → [`amendment-log.json`](amendment-log.json) — structured change history (git is the dated trail).

---

## REQ block contract (how each `capabilities/<domain>.md` requirement is written)

Each requirement is a **delimited block** so an amendment can target a findable, replaceable span — never
"find the clause" in a long prose file:

````
### REQ-NNN: <name>   (MUST|SHOULD|MAY)

<one-line statement of the capability>

**Acceptance (outcome-level):**
```gherkin
Given <context>
When <user-observable action>
Then <user-observable outcome>
```
<!-- source: "<verbatim quote from the source doc that grounds this REQ — or `inferred` if 00 derived it>" -->
<!-- /REQ-NNN -->
````

The Gherkin here is **outcome-level** — a *declaration* ("the user can reset their password"). Detailed,
UI-specific steps are **realization** and live in skill 03's feature-spec **Verification Contracts**, not here.

The `<!-- source: … -->` line records **fidelity**: the verbatim quote from the user's doc or interview that grounds
this REQ, or `inferred` when skill 00 derived it. It mirrors the registry **Status** (`stated` ↔ a real quote;
`derived` ↔ `inferred`) — a `derived` REQ is a flag for human confirmation, never a silent fact.

---

## Open `[NEEDS CLARIFICATION]` markers

> Carried from the REVIEW gate (PROCEED with non-blocking gaps). **06-release blocks deploy** on any survivor.

- **REQ-002** — edit-lock instant for members whose timezone differs from the team's digest timezone.
- **REQ-008** — how the digest represents a member who did not submit before generation (omit / placeholder / missing).
