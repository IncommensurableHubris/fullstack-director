# Specification — TeamPulse (HTTP API slice)

> **The spec spine: the single source of declaration-truth.** This is the **INDEX** — the **Constitution** and the
> **REQ registry** (authoritative ID→file). Detailed requirements live in [`capabilities/`](capabilities/). Owned by
> **skill 00 (discovery)**. Every other skill *references* REQ-IDs from here. (A mid-chain spine for the `/status`
> eval: the digest core plus the sprint-02 HTTP delivery — enough of the artifact chain for the router to derive a
> real next command.)

---

## Constitution (PROTECTED)

1. **Async over synchronous.** The product replaces the standup *meeting* — status is shared and absorbed without a
   synchronous call.
2. **The daily digest is the one artifact.** The whole team stays in sync by reading a single daily digest.
3. **Timezone-fair.** No member is penalized for their timezone.
4. **EU data residency.** All data stays in the EU region.
5. **Passwordless by design.** Email magic-link only — **no passwords, no third-party SSO** in v1.
6. **Least data, least access.** A member sees only their own team's data; the service holds only what the digest
   needs. Personal standup content is treated as **confidential**.

---

## REQ registry

> The **authoritative** ID→file map — every REQ appears here exactly once. Skill 01 is the sole allocator.

| REQ | Name | Priority | Status | File |
|-----|------|----------|--------|------|
| REQ-001 | Submit a daily standup | MUST | stated | capabilities/standups.md |
| REQ-008 | Generate one daily digest grouped by member | MUST | stated | capabilities/digest.md |
| REQ-009 | Surface "needs help" blockers at the top | SHOULD | stated | capabilities/digest.md |
| REQ-010 | Read current and past digests | SHOULD | stated | capabilities/digest.md |
| REQ-020 | Serve the digest over an authenticated API | MUST | stated | capabilities/api.md |
| REQ-021 | Notify the team on a "needs help" flag | SHOULD | stated | capabilities/api.md |

- **Priority** — RFC 2119: `MUST` / `SHOULD` / `MAY`.
- **Status** — `stated` (traces to a source quote) or `derived` (inferred). *(Fidelity — not execution status, which
  lives in the backlog ledger.)*

---

## REQ block contract

Each requirement is a **delimited block** so an amendment can target a findable, replaceable span:

````
### REQ-NNN: <name>   (MUST|SHOULD|MAY)

<one-line statement>

**Acceptance (outcome-level):**
```gherkin
Given <context>
When <user-observable action>
Then <user-observable outcome>
```
<!-- source: "<verbatim quote — or `inferred`>" -->
<!-- /REQ-NNN -->
````

The Gherkin here is **outcome-level** (a declaration). Detailed, technical steps are **realization** and live in
skill 03's feature-spec **Verification Contracts**, not here.

---

## Open clarification markers

- None — every clarification raised during discovery and review has been resolved into its REQ block.
