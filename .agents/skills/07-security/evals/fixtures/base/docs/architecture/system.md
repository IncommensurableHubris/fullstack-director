<!-- Filename: docs/architecture/system.md -->

# System Architecture — TeamPulse (HTTP API slice)

> **The durable "shape" realization.** Owned by **skill 03 (architect)**. An arc42 subset; it *references* the spine's
> REQs by ID. The **security audit reads this for trust boundaries + the tech stack** — and to decide whether the
> optional LLM/agentic module applies.

**Realizes constraints from** `docs/spec/architecture-constraints.md` · **serves REQ-008, REQ-020, REQ-021** _(by ID)._

---

## §1 · Constraints (the governed envelope)

| Constraint | Value | Honored by |
|---|---|---|
| Language / runtime | **Plain Node.js (LTS ≥ 20)** — no transpile step | §5 |
| HTTP | **Built-in `node:http`**; **zero runtime dependencies** | §5, ADR-001 |
| Auth | **Magic-link sessions**, server-issued + **server-verified** HMAC tokens | §5, ADR-002 |
| Data residency | EU region | §8 |
| **AI/LLM components** | **None.** TeamPulse has no LLM, RAG, agent, or model-inference component of any kind | §5 |

> **No AI surface.** This system contains **no LLM, embedding, vector-store, agent, or MCP component** — the optional
> LLM/agentic security module does **not** apply to this codebase.

---

## §3 · Context & Scope — C4 Level 1

**Purpose:** Serve a team's daily digest over an authenticated HTTP API and notify the team's channel on "needs help."

```
[Team member] --HTTP (session token)--> [TeamPulse API (node:http)] --reads--> [digest core + in-memory store]
                                                     |
                                                     +--outbound webhook--> [team's channel (external)]
```

**Trust boundaries:** (1) the **HTTP request boundary** — every request is untrusted until the session token is
verified and the member is authorized to the requested team's data (REQ-020). (2) the **outbound webhook** — a
member-influenced destination is an SSRF surface (REQ-021); only the team's configured channel host is a valid target.

---

## §5 · Building Block View — C4 Level 2

| Module | Technology | Responsibility |
|--------|-----------|----------------|
| `src/server.js` | `node:http` | routes requests; enforces authn + per-team authz; renders JSON; posts the webhook |
| `src/auth.js` | `node:crypto` | issues + **verifies** session tokens (HMAC over member id, key from env) |
| `src/store.js` | plain Node | in-memory entries/members access, scoped by team |
| `src/digest.js` | plain Node (pure) | the sprint-01 digest core (record + assemble) — unchanged |

### Bounded contexts

| Context | Owns |
|---------|------|
| Access | authentication (session token), authorization (a member → only their team) |
| Digest | assembly of the daily artifact (pure) |
| Notify | the outbound "needs help" webhook to the team's configured channel |

---

## §8 · Crosscutting Concepts

- **Trust boundary at the request.** Identity is derived from a **server-verified** session token — never from
  client-supplied identity or role fields. Authorization is a **server-side** check against the member's own team.
- **Secrets from the environment.** The signing key and any webhook credentials come from env vars; nothing is
  hardcoded (`architecture-constraints.md` § Secrets).
- **Outbound requests are constrained.** The webhook destination is validated against the team's configured channel
  host — user-influenced URLs are never fetched unrestricted.

### Banned-list (fitness functions enforce)

- Any runtime dependency (zero-dep mandate — a new dep is a HALT for `04`, and a supply-chain concern for `07`).
- Client-trusted identity or authorization (`role`/`member` from the request body/query as the source of truth).
- A hardcoded secret in source; an unrestricted outbound fetch of a user-supplied URL.

---

## §9 · Architectural Decisions

→ See [`adr/README.md`](adr/README.md). Load-bearing: **ADR-001** (plain Node.js + `node:test`, zero-dependency),
**ADR-002** (magic-link session auth with server-verified HMAC tokens + server-side per-team authorization).

---

## § Threats considered — design-time pass over the trust boundaries (§3)

> The Four Questions over the two trust boundaries §3 draws (STRIDE as an optional structuring aid). Each threat →
> its mitigation; 07's audit cross-references this — a designed threat with no verifying check is a gap.

| Boundary | Threat | Mitigation |
|----------|--------|------------|
| HTTP request | cross-team data access (IDOR) — a member reads another team's entries | server-side per-team authorization (ADR-002); the banned-list forbids client-trusted identity |
| HTTP request | session forgery / client-trusted identity | server-verified HMAC session tokens (ADR-002); identity never from request fields |
| HTTP request | reflected injection (XSS) in a rendered response | JSON responses only; output escaping; no dynamic HTML (§8) |
| Outbound webhook | SSRF to an internal/metadata host via a member-influenced URL | destination validated against the team's configured channel host (§8) |
| Build / deps | a malicious or hallucinated dependency (supply chain) | zero-runtime-dependency mandate (ADR-001) — a new dep is a HALT |
| Any module | a hardcoded secret in source | secrets from env only (§8); nothing hardcoded |

---

## §11 · Risks & Deferred

- **Deferred:** the web UI, durable persistence — later sprints.
- **Residual:** live-infrastructure hardening (TLS termination, network policy) is a **deployment** concern, verified
  outside this repo — a security audit of the codebase cannot evidence it and should say so.
