<!-- budget: ≤25 lines per REQ block — a longer block is restating methodology or copying prose; one home per fact. -->

# Capability: Account & Access  _(EXAMPLE — delete when real domains exist)_

> One file **per domain** (e.g. `account.md`, `billing.md`, `reporting.md`). Group REQs by what they're *about*,
> not by build order (build order is skill 01's decision, recorded in the backlog ledger — not a declaration).
> Each REQ is a delimited block per the contract in [`../specification.md`](../specification.md). Every REQ here
> must also appear in that file's **REQ registry** table. Each **statement line is EARS-form** (mandated — see
> `references/requirements-authoring.md`). The closing `<!-- source: … -->` line records fidelity — the quote that
> grounds the REQ, or `inferred`. Below: REQ-001 `stated` (event-driven), REQ-002 `derived` (`inferred`,
> optional-feature), REQ-003 a **must-not** (Unwanted-behavior IF/THEN) — the three shapes you reach for most.

### REQ-001: Email + password sign-in   (MUST)

WHEN a returning user submits the email and password they registered with, the system SHALL authenticate them and start a session.

**Acceptance (outcome-level):**
```gherkin
Given a registered user with a verified email
When they submit the correct email and password
Then they are signed in and land on their dashboard
```
<!-- source: "PRD §2.1: 'Returning users sign in with the email and password they registered with.'" -->
<!-- /REQ-001 -->

### REQ-002: Self-service password reset   (SHOULD)

WHERE self-service reset is enabled, the system SHALL let a user who has forgotten their password regain access without contacting support.

**Acceptance (outcome-level):**
```gherkin
Given a registered user who has forgotten their password
When they complete the email-based reset flow
Then they can sign in with the new password
```
<!-- source: inferred -->
<!-- /REQ-002 -->

### REQ-003: Reject unauthenticated access   (MUST)

IF a request for a protected resource carries no valid session, THEN the system SHALL deny access and record the attempt.

**Acceptance (outcome-level):**
```gherkin
Given a request with no valid session
When it targets a protected resource
Then access is refused and the attempt is logged
```
<!-- source: "PRD §5: 'Unauthenticated requests to protected resources must be rejected.'" -->
<!-- /REQ-003 -->
