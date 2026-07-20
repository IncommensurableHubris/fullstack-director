### REQ-001: Group recurring senders in one view   (MUST)

WHEN a connected inbox is scanned, the system SHALL group every recurring sender into a single ranked list, ordered
by message volume over the trailing 90 days.

**Acceptance (outcome-level):**
```gherkin
Given a connected inbox
When MailSweep scans recent mail
Then every recurring sender appears in one ranked list ordered by message volume
```
<!-- source: "Given a connected inbox, when MailSweep scans recent mail, then every recurring sender is grouped into a single ranked list, ordered by message volume over the trailing 90 days." -->
<!-- /REQ-001 -->

### REQ-002: Leave a sender in one click   (MUST)

WHEN the user selects "leave this sender," the system SHALL run that sender's unsubscribe path — the
`List-Unsubscribe` header where present, otherwise the linked web form — without further action from the user.

**Acceptance (outcome-level):**
```gherkin
Given a sender in the grouped list
When the user selects "leave this sender"
Then MailSweep runs that sender's unsubscribe path with no further user action
```
<!-- source: "Given a sender in the grouped list, when the user selects 'leave this sender,' then MailSweep runs that sender's unsubscribe path (the List-Unsubscribe header where present, otherwise the linked web form) without further action from the user." -->
<!-- /REQ-002 -->

### REQ-003: Apply bulk cleanup actions   (MUST)

WHEN the user applies a bulk action to a set of selected senders, the system SHALL apply that action to every past
message from those senders and record it so future mail from them is handled the same way.

**Acceptance (outcome-level):**
```gherkin
Given a set of selected senders
When the user applies a bulk action
Then the action applies to every past message from those senders and is recorded for future mail
```
<!-- source: "Given a set of selected senders, when the user applies a bulk action — leave, archive, or mute — then that action is applied to every past message from those senders and recorded so future mail from them is handled the same way." -->
<!-- /REQ-003 -->

### REQ-004: Keep applying a standing cleanup decision   (MUST)

WHEN new mail arrives from a sender the user has muted, archived, or left, the system SHALL apply the same decision
automatically without prompting the user again.

**Acceptance (outcome-level):**
```gherkin
Given a sender the user has muted, archived, or left
When new mail from that sender arrives afterward
Then MailSweep applies the same decision automatically with no further prompt
```
<!-- source: "Given a sender the user has muted, archived, or left, when new mail from that sender arrives afterward, then MailSweep applies the same decision automatically without prompting the user again." -->
<!-- /REQ-004 -->

### REQ-005: Send a periodic cleanup digest   (SHOULD)

WHEN a weekly cleanup cycle closes, the system SHALL send the user a digest listing senders removed, the drop in
weekly message volume, and any new recurring sender detected since the last cycle.

**Acceptance (outcome-level):**
```gherkin
Given a completed weekly cleanup cycle
When the cycle closes
Then the user receives a digest listing senders removed, volume drop, and newly detected senders
```
<!-- source: "Given a completed weekly cleanup cycle, when the cycle closes, then MailSweep sends the user a short digest listing senders removed, the resulting drop in weekly message volume, and any new recurring sender detected since the last cycle." -->
<!-- /REQ-005 -->
