# Specification — TeamPulse

> **The spec spine: the single source of declaration-truth.** This file is the **INDEX**. It holds the project
> **Constitution** (non-negotiables) and the **REQ registry** (the authoritative ID→file map). Detailed
> requirements live in [`capabilities/`](capabilities/) `<domain>.md` files; design intent in
> [`design-intent.md`](design-intent.md); architecture mandates in
> [`architecture-constraints.md`](architecture-constraints.md); the change history in
> [`amendment-log.json`](amendment-log.json).

---

- **Profile:** webapp   <!-- webapp | agent-system | mcp-server | skill-pack. Sets each seat's profile-aware behavior (shared/agentic-profile.md). Absent ⇒ webapp. Changing it later is a Tier-2 amendment minimum. -->

---

## Constitution (PROTECTED)

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
> `/status` integrity-checks that every `File` resolves and contains that REQ's delimited block.

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

- **Priority** — RFC 2119: `MUST` / `SHOULD` / `MAY`.
- **Status** — `stated` (traces to a user source quote) or `derived` (inferred). REQ-007 is `derived`.

---

## Pointers

- **Design intent** → [`design-intent.md`](design-intent.md)
- **Architecture constraints** → [`architecture-constraints.md`](architecture-constraints.md)
- **Amendment log** → [`amendment-log.json`](amendment-log.json)

---

## Open clarification markers

> None. The comprehensive PRD was decisive on the edit-lock instant (a single team-wide lock at the configured
> digest time) and non-submitter representation (omit from the digest), so intake produced no surviving markers.

- _(none)_
