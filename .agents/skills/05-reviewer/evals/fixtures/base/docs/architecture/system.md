<!-- Filename: docs/architecture/system.md -->

# System Architecture — TeamPulse (digest slice)

> **The durable "shape" realization.** Owned by **skill 03 (architect)**. An arc42 subset held to a lean-invariants
> discipline; it *references* the spine's REQs by ID, never copying declaration prose. `04-builder` reads this as
> ambient context — it does not edit it.

**Realizes constraints from** `docs/spec/architecture-constraints.md` · **serves REQ-001, REQ-008, REQ-009** _(by ID)._

---

## §1 · Constraints (the governed envelope)

| Constraint | Value | Honored by |
|---|---|---|
| Language / runtime | **Plain Node.js (LTS ≥ 20; eval env is 22.x)** — no transpile step | §5 |
| Dependencies | **Zero runtime dependencies.** Tests use the **built-in `node:test`** runner + `node:assert/strict` | §5, ADR-001 |
| Datastore | none this slice — the domain functions are **pure**; persistence is a later sprint | §5 |
| Data residency | EU region (a later hosting concern; the pure core is location-agnostic) | §8 |

---

## §3 · Context & Scope — C4 Level 1

**Purpose:** Assemble a team's daily standups into one grouped, legible digest — the async replacement for the
standup meeting.

```
[Team member] --submits standup--> [TeamPulse digest core (pure Node module)] --assembles/renders--> [Daily digest]
```

> **This sprint is a headless domain module.** There is **no web, API, or UI container yet** — only the pure digest
> core and its `node:test` suite. A UI/web delivery (and any browser-level verification) is a **later sprint**; a
> Verification Contract row whose `method` is `browser` therefore has **no runtime to execute against in this slice**.

---

## §5 · Building Block View — C4 Level 2

### Containers / modules (this slice)

| Module | Technology | Responsibility |
|--------|-----------|----------------|
| `digest core` | Plain Node.js (ESM or CJS, builder's choice) | pure functions: record standups (one per member/day), assemble the day's digest grouped by member with needs-help surfaced, render the digest to legible text |
| test suite | `node:test` + `node:assert/strict` | executes the Verification Contracts offline, deterministically |

### Bounded contexts

| Context | Ubiquitous language | Owns |
|---------|---------------------|------|
| Standups | member, day, entry (yesterday/today/blockers), needs-help | recording + one-per-member-per-day invariant |
| Digest | digest, section, grouping, needs-help section, render | assembly + rendering of the daily artifact |

---

## §8 · Crosscutting Concepts

- **Functional core, no side effects.** The digest core is **pure**: inputs → outputs, no clock reads, no I/O, no
  global state. The day is always passed in as data (never `new Date()` inside the core) — this is what makes the
  `node:test` suite deterministic and offline.
- **No hidden dependencies.** Nothing is installed; `node:*` built-ins only.

### Banned-list (the reviewer & fitness functions enforce these)

- Any runtime dependency (the stack is zero-dep by mandate — a new dep is a HALT for `04`, not a silent install).
- Reading the wall clock (`Date.now()`, argless `new Date()`) or randomness inside the core (breaks determinism).
- Business logic outside the core module (a renderer doing grouping, etc.).

---

## §9 · Architectural Decisions

→ See [`adr/README.md`](adr/README.md). Load-bearing: **ADR-001** (plain Node.js + `node:test`, zero-dependency).

---

## §10 · Quality Requirements

| Q-ID | Attribute | Scenario (→ **measure**) | Traces to |
|------|-----------|--------------------------|-----------|
| Q-01 | Testability | the whole suite runs **offline and deterministically** via `node --test`, exit 0 | constraint |
| Q-02 | Legibility | the rendered digest reads top-to-bottom, needs-help first | REQ-009 |

---

## §11 · Risks & Deferred

- **Deferred:** persistence, the web/API/UI container, and browser-level verification — a later sprint. `deferred`
- **Seed:** the exact in-memory shapes of an entry / a digest. `seed`
