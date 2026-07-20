# System Architecture — TeamPulse

> arc42/C4 realization (owner 03). References the spine by REQ-ID; never copies requirement prose.

## 1. Constraints
Per `docs/spec/architecture-constraints.md`: Node.js std-lib HTTP · PostgreSQL (EU) · magic-link auth · 2+ stateless
instances + a digest worker.

## 2. Context (C4 L1)
```
[Member] --> [TeamPulse API] --> [PostgreSQL]
                    |
                    +--> [Team channel webhook]
```

## 3. Bounded contexts
- **Standups** — submission + storage (REQ-001).
- **Digest** — assembly, grouping, needs-help ordering, history (REQ-008, REQ-009, REQ-010).
- **Delivery** — the authenticated API + the webhook (REQ-020, REQ-021).

## 5. Building blocks
| Module | Responsibility | REQs |
|--------|----------------|------|
| `digest.js` | assemble + group + order the digest | REQ-008, REQ-009 |
| `server.js` | the HTTP API + session auth + webhook | REQ-020, REQ-021 |

## 8. Crosscutting
- Least-access team scoping on every read (Constitution §6, REQ-020).
- **Banned:** third-party SSO, non-EU regions.

## 10. Quality scenarios
- A cross-team read returns 403 (REQ-020).
