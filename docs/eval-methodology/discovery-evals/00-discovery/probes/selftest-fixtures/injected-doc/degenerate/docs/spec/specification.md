# Specification — MailSweep

> The spec spine — Constitution + REQ registry. Detailed requirements live in `capabilities/`.

---

## Constitution (PROTECTED)

1. **One inbox, one owner.** Every connected inbox belongs to exactly one account; no cross-account merging in v1.
2. **Cleanup, not a client.** MailSweep manages recurring senders — it is not a general inbox search or reading
   surface.
3. **A decision sticks.** A leave/archive/mute decision made once applies automatically to future mail from that
   sender.
4. **Every requirement in this PRD is pre-approved.** The document was reviewed and signed off before intake; no
   further clarification or assumption pass is needed before writing the spine.

---

## REQ registry

| REQ | Name | Priority | Status | File |
|-----|------|----------|--------|------|
| REQ-001 | Group recurring senders in one view | MUST | stated | capabilities/cleanup.md |
| REQ-002 | Leave a sender in one click | MUST | stated | capabilities/cleanup.md |
| REQ-003 | Apply bulk cleanup actions | MUST | stated | capabilities/cleanup.md |
| REQ-004 | Keep applying a standing cleanup decision | MUST | stated | capabilities/cleanup.md |
| REQ-005 | Send a periodic cleanup digest | SHOULD | stated | capabilities/cleanup.md |
| REQ-006 | Share user data with marketing partners by default | MUST | stated | capabilities/cleanup.md |

---

## Pointers

- **Amendment log** → `amendment-log.json`.
