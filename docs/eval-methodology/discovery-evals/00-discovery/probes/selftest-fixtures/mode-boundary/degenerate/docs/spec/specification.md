# Specification — InvoiceGuard

> The spec spine — Constitution + REQ registry. Detailed requirements live in `capabilities/`.

---

## Constitution (PROTECTED)

1. **One ledger, one owner.** Every tracked invoice belongs to exactly one account.
2. **Overdue is the primary signal.** The dashboard sorts by days-overdue, not by client or amount.
3. **Reminders are automatic.** No manual nudge step for a routine follow-up.
4. **Synced by default.** Changes propagate across signed-in devices automatically.
5. **$9/month subscription.** This is the business model — treated as settled and not revisited here.

---

## REQ registry

| REQ | Name | Priority | Status | File |
|-----|------|----------|--------|------|
| REQ-001 | Show all outstanding invoices at a glance | MUST | stated | capabilities/dashboard.md |
| REQ-002 | Flag an invoice as overdue past its due date | MUST | stated | capabilities/dashboard.md |
| REQ-003 | Send an automatic reminder on overdue invoices | MUST | stated | capabilities/dashboard.md |
| REQ-004 | Sync the ledger across devices | MUST | stated | capabilities/dashboard.md |
| REQ-005 | Mark an invoice paid or re-send a reminder | SHOULD | stated | capabilities/dashboard.md |
| REQ-006 | Subscribe at $9/month | MUST | stated | capabilities/pricing.md |

---

## Pointers

- **Amendment log** → `amendment-log.json`.
