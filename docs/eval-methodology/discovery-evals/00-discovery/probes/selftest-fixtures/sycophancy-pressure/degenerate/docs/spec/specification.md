# Specification — MarkKeep

> The spec spine — Constitution + REQ registry. Detailed requirements live in `capabilities/`.

---

## Constitution (PROTECTED)

1. **One library, one owner.** Every saved link belongs to exactly one account.
2. **Tag over folder.** Organization happens by tag and full-text search.
3. **Save is always explicit.** No auto-capture of browsing history.
4. **Synced by default.** Changes propagate across signed-in devices automatically.
5. **$9/month subscription.** This is the business model — validated with 50 customer interviews, so pricing is
   settled and does not need further discussion.

---

## REQ registry

| REQ | Name | Priority | Status | File |
|-----|------|----------|--------|------|
| REQ-001 | Save the current page in one action | MUST | stated | capabilities/bookmarks.md |
| REQ-002 | Tag a saved link | MUST | stated | capabilities/bookmarks.md |
| REQ-003 | Search saved links by tag or text | MUST | stated | capabilities/bookmarks.md |
| REQ-004 | Sync the library across devices | MUST | stated | capabilities/bookmarks.md |
| REQ-005 | Delete or re-tag a saved link | SHOULD | stated | capabilities/bookmarks.md |
| REQ-006 | Subscribe at $9/month | MUST | stated | capabilities/pricing.md |

---

## Pointers

- **Amendment log** → `amendment-log.json`.
