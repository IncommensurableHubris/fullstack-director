# Feature spec — HTTP API (sprint-02)

> Realization for sprint-02 (owner 03). References REQ-020, REQ-021; covers DM-001, DM-002.

## Scope
The authenticated digest API + the needs-help webhook.

## Verification Contract

| # | REQ | Method | Pass criterion |
|---|-----|--------|----------------|
| VC-1 | REQ-020 | api-contract | `GET /digest` with a valid session returns the caller's team digest; a cross-team request returns 403 |
| VC-2 | REQ-021 | api-contract | a standup flagged "needs help" triggers one POST to the team's configured webhook |

## Design Contract Coverage
- DM-001 → VC-1 · DM-002 → VC-2.
