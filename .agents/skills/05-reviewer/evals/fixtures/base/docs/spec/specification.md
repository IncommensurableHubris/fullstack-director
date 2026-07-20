# Specification — TeamPulse (digest slice)

> **The spec spine: the single source of declaration-truth.** This is the **INDEX** — the **Constitution** and the
> **REQ registry** (authoritative ID→file). Detailed requirements live in [`capabilities/`](capabilities/). Owned by
> **skill 00 (discovery)**. Every other skill *references* REQ-IDs from here; `04-builder` keys its coverage map to
> them and never copies requirement prose. (A trimmed spine for the 04 build eval: the pure-domain digest slice.)

---

## Constitution (PROTECTED)

1. **Async over synchronous.** The product replaces the standup *meeting* — status is shared and absorbed without a
   synchronous call.
2. **The daily digest is the one artifact.** The whole team stays in sync by reading a single daily digest that reads
   top-to-bottom in under two minutes for a 12-person team; brevity and legibility win over completeness.
3. **Timezone-fair.** No member is penalized for their timezone.
4. **EU data residency.** All data stays in the EU region.
5. **Passwordless by design.** Email magic-link only — no passwords, no third-party SSO in v1.
6. **Zero-training setup.** A lead can stand up a team and have members contributing within one day.

---

## REQ registry

> The **authoritative** ID→file map — every REQ appears here exactly once, updated in the same step as any REQ write.
> Skill 01 is the sole allocator; others request `max(registry)+1`.

| REQ | Name | Priority | Status | File |
|-----|------|----------|--------|------|
| REQ-001 | Submit a daily standup | MUST | stated | capabilities/standups.md |
| REQ-002 | Edit a standup until the digest locks it | SHOULD | stated | capabilities/standups.md |
| REQ-003 | Flag a blocker as "needs help" | SHOULD | stated | capabilities/standups.md |
| REQ-008 | Generate one daily digest grouped by member | MUST | stated | capabilities/digest.md |
| REQ-009 | Surface "needs help" blockers at the top | SHOULD | stated | capabilities/digest.md |
| REQ-010 | Read current and past digests | SHOULD | stated | capabilities/digest.md |

- **Priority** — RFC 2119: `MUST` / `SHOULD` / `MAY`.
- **Status** — `stated` (traces to a source quote) or `derived` (inferred).

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

The Gherkin here is **outcome-level** (a declaration). Detailed, UI/technical steps are **realization** and live in
skill 03's feature-spec **Verification Contracts**, not here.

---

## Open `[NEEDS CLARIFICATION]` markers

> **06-release blocks deploy** on any survivor.

- **REQ-008** — how the digest represents a member who did not submit before generation (omit / placeholder / missing).
