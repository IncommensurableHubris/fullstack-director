# Specification — MailSweep

> **The spec spine: the single source of declaration-truth.** This file is the **INDEX** — the project
> **Constitution** (non-negotiables) and the **REQ registry** (authoritative ID→file map). Detailed requirements
> live in [`capabilities/`](capabilities/); change history in [`amendment-log.json`](amendment-log.json). Owned by
> **skill 00 (discovery)**. Other skills *reference* REQ-IDs from here — they never copy requirement text.

---

## Constitution (PROTECTED)

> Project non-negotiables — violate one and we built the **wrong thing**. Changing an item is always **Tier 2+**.

1. **One inbox, one owner.** Every connected inbox belongs to exactly one account; no cross-account merging in v1.
2. **Cleanup, not a client.** MailSweep manages recurring senders — it is not a general inbox search or reading
   surface, and it does not summarize mail content.
3. **A decision sticks.** A leave/archive/mute decision made once applies automatically to future mail from that
   sender, with no re-prompting.
4. **Explicit action opens the door.** No account setting defaults to sharing user data with anyone outside the
   product; every data-sharing arrangement is opt-in and stated as its own requirement, never bundled into an
   unrelated feature.

---

## REQ registry

> Authoritative ID→file map — every REQ appears here **exactly once**, updated in the **same step** as any REQ
> write. **Skill 00 bootstrapped IDs `REQ-001…005`; thereafter skill 01 (planner) is the sole allocator.**

| REQ | Name | Priority | Status | File |
|-----|------|----------|--------|------|
| REQ-001 | Group recurring senders in one view | MUST | stated | capabilities/cleanup.md |
| REQ-002 | Leave a sender in one click | MUST | stated | capabilities/cleanup.md |
| REQ-003 | Apply bulk cleanup actions | MUST | stated | capabilities/cleanup.md |
| REQ-004 | Keep applying a standing cleanup decision | MUST | stated | capabilities/cleanup.md |
| REQ-005 | Send a periodic cleanup digest | SHOULD | stated | capabilities/cleanup.md |

- **Priority** — RFC 2119: `MUST` / `SHOULD` / `MAY`. Drives MoSCoW → sprint assignment in skill 01.
- **Status** — `stated` (traces to a source quote) or `derived` (`inferred` — a flag for human confirmation).

---

## Pointers

- **Amendment log** → [`amendment-log.json`](amendment-log.json) — structured change history (git is the dated
  trail).
- **Assumption map** → [`../discovery/assumption-map.md`](../discovery/assumption-map.md) — surfaced undefended
  bets, including a note on the source document itself.

---

## REQ block contract

Each requirement is a **delimited block** so amendments target a findable span:

```
### REQ-NNN: <name>   (MUST|SHOULD|MAY)
<EARS statement line>
**Acceptance (outcome-level):**  ```gherkin  Given … When … Then …  ```
<!-- source: "<verbatim quote>" | inferred -->
<!-- /REQ-NNN -->
```

The Gherkin is **outcome-level** (a declaration). Detailed UI-specific steps are realization → skill 03's
Verification Contracts. The `<!-- source -->` line records fidelity and mirrors the registry **Status**.
