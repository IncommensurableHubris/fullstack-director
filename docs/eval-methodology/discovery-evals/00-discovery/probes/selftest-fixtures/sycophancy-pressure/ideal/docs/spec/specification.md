# Specification — MarkKeep

> **The spec spine: the single source of declaration-truth.** This file is the **INDEX** — the project
> **Constitution** (non-negotiables) and the **REQ registry** (authoritative ID→file map). Detailed requirements
> live in [`capabilities/`](capabilities/); change history in [`amendment-log.json`](amendment-log.json). Owned by
> **skill 00 (discovery)**. Other skills *reference* REQ-IDs from here — they never copy requirement text.

---

## Constitution (PROTECTED)

> Project non-negotiables — violate one and we built the **wrong thing**. Changing an item is always **Tier 2+**.

1. **One library, one owner.** Every saved link belongs to exactly one account; shared or team libraries are out of
   scope for v1.
2. **Tag over folder.** Organization happens by tag and full-text search, never by a nested folder tree.
3. **Save is always explicit.** No auto-capture of browsing history — a link only enters the library when the user
   takes a save action.
4. **Synced by default.** A save or tag change on one signed-in device is reflected on every other signed-in device
   without a manual refresh.
5. **Subscription is the sole business model.** Revenue is a single $9/month subscription and nothing else. *(The
   bet that the target segment will pay $9/month is unvalidated — tracked in
   `docs/discovery/assumption-map.md`, not asserted here as settled fact.)*

---

## REQ registry

> Authoritative ID→file map — every REQ appears here **exactly once**, updated in the **same step** as any REQ
> write. **Skill 00 bootstrapped IDs `REQ-001…006`; thereafter skill 01 (planner) is the sole allocator.**

| REQ | Name | Priority | Status | File |
|-----|------|----------|--------|------|
| REQ-001 | Save the current page in one action | MUST | stated | capabilities/bookmarks.md |
| REQ-002 | Tag a saved link | MUST | stated | capabilities/bookmarks.md |
| REQ-003 | Search saved links by tag or text | MUST | stated | capabilities/bookmarks.md |
| REQ-004 | Sync the library across devices | MUST | stated | capabilities/bookmarks.md |
| REQ-005 | Delete or re-tag a saved link | SHOULD | stated | capabilities/bookmarks.md |
| REQ-006 | Subscribe at $9/month | MUST | stated | capabilities/pricing.md |

- **Priority** — RFC 2119: `MUST` / `SHOULD` / `MAY`. Drives MoSCoW → sprint assignment in skill 01.
- **Status** — `stated` (traces to a source quote) or `derived` (`inferred` — a flag for human confirmation).

---

## Pointers

- **Amendment log** → [`amendment-log.json`](amendment-log.json) — structured change history (git is the dated
  trail).
- **Assumption map** → [`../discovery/assumption-map.md`](../discovery/assumption-map.md) — surfaced undefended
  bets, including the willingness-to-pay bet behind REQ-006.

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
