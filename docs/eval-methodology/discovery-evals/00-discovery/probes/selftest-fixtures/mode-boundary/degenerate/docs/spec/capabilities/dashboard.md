# Capability — Dashboard

### REQ-001: Show all outstanding invoices at a glance
<!-- source: run prompt -->
WHEN the user opens the dashboard, the system SHALL display every unpaid invoice sorted by days-overdue.
<!-- /REQ-001 -->

### REQ-002: Flag an invoice as overdue past its due date
<!-- source: run prompt -->
WHEN an invoice's due date has passed, the system SHALL mark it overdue.
<!-- /REQ-002 -->

### REQ-003: Send an automatic reminder on overdue invoices
<!-- source: run prompt -->
WHEN an invoice becomes overdue, the system SHALL send a reminder to the client without a manual step.
<!-- /REQ-003 -->

### REQ-004: Sync the ledger across devices
<!-- source: run prompt -->
WHEN a change is made on one device, the system SHALL propagate it to all signed-in devices.
<!-- /REQ-004 -->

### REQ-005: Mark an invoice paid or re-send a reminder
<!-- source: run prompt -->
WHEN the user selects an invoice, the system SHALL let them mark it paid or re-send a reminder.
<!-- /REQ-005 -->
