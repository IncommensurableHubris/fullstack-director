# Subagent Protocol — surgical context-isolation only

> Shared by skills 05, 03, 00, 07. The framework spine is **sequential by design**: multi-agent swarms amplify
> errors and *hurt* sequential tasks, so subagents are used **only** where context-isolation actually pays — chiefly
> **verification** (a fresh context that can't self-prefer) and a few **bounded parallel reads**. Build and refactor
> stay fully sequential.

## Spawn pattern — a capability tier

Subagent spawning is a **capability tier**, not a hard requirement; the protocol is portable across harnesses:

- **Where the harness supports subagents** (e.g. Claude Code's `Task`/`Agent` tool) — **spawn** one. For Claude,
  use a `subagent_type` backed by a `.claude/agents/*.md` definition (read-only tools where applicable; `skills:`
  preload so the subagent loads the right skill). The framework ships three: **`fsd-reviewer`** (05's Pass-2),
  **`fsd-reconciler`** (03's Pass-2), **`fsd-owasp-reader`** (07's panel — one definition, one area-slice per
  spawn); `tools/vendor.py` emits them into consumers.
- **Where it does not** — run the reviewer / reconciler / reader as a **fresh top-level invocation** instead.

**Isolation comes from a _fresh spawner_, not the spawn mechanism.** A reviewer spawned from the build session
inherits the builder's reasoning whether or not a subagent tool exists; a reviewer launched fresh — as a subagent
*from a fresh session*, or as a fresh top-level invocation — does not. Every harness can therefore achieve real
isolation; only the mechanism differs. (Per-harness deployment: `docs/harness-support.md`.)

Spawn config is **centralized here** — skills reference this file rather than re-specifying it.

## Per-role I/O contract

### build → quality reviewer (skill 05)

- **Spawned from a _fresh_ `05 reviewer` invocation — not from the build session.** Isolation is real **only**
  because the spawner is fresh. Spawn the reviewer from the session that just wrote the code and it inherits the
  builder's reasoning — the isolation is then fictional, and the self-preference it was meant to defeat is back.
- **Seeded with ONLY:** the handoff-file path (`_artifacts/exports/build-handoff-sprint-N.md`) **+** the spec-slice
  paths (the in-scope REQ blocks + the design contract). **Never** the build conversation.
- **Loads** the reviewer skill; **writes** the QA report itself.
- **Returns ONLY:** the verdict line **+ a one-line context attestation** —
  `inputs: [handoff, spec slice]; build conversation: not provided`.
  The attestation is a **declared-inputs statement, not proof**: the spawner transcribes it into the artifacts, so
  a spawn that leaked context would transcribe it unchanged. What the eval grades deterministically is its
  **presence** (the contract was followed in form). Isolation itself rests on the **fresh-spawner discipline plus
  the seed-only instruction** — predictive controls, declared as such. Where a harness persists spawn transcripts,
  a transcript-absence check (no builder reasoning markers in the spawner's transcript) adds an **evidence** layer;
  where transcripts are not persisted, that check is UNVERIFIABLE and no isolation proof may be claimed.

### architecture reconciler (skill 03)

- **Receives:** the architecture realization **+** the slice's declarations (`architecture-constraints.md` + the
  in-scope REQ blocks).
- **Returns:** amendment rows (per `spec-amendment-protocol.md`) — Tier-classified, each with a `source_quote`.

### parallel readers + synthesizer (skill 00 intake, skill 07 security)

For **intake over a user-provided document** and **security over OWASP areas** — **NOT** human-interview discovery
(an interview is inherently sequential and conversational).

- **Readers — bounded parallel, read-only.** Each returns `finding + source_quote + proposed_tier/severity`. Cap
  **3–5**. Each reader is blind to the others' findings.
- **Synthesizer — a single _sequential reduce_, never itself parallel.** De-dupe by target, take **max severity**,
  and **preserve source quotes**. A parallel "merge" would re-introduce the error-amplification this whole protocol
  is avoiding.

## Guardrails

- **Centralized config only** (here) — no skill invents its own subagent setup.
- **Cap 3–5** concurrent readers.
- **Build and refactor stay sequential** — no subagents.
- **The human stays at the verdict gate** — a subagent *reports*; it never gets the final say on ship or scope.

## Harness note (Windows evals)

The eval harness injects `<SUBAGENT-STOP>` (telling a dispatched subagent to skip skill bootstrapping). For the
**subagent-spawning skills (05, 03, 07)** this must be **relaxed**, or the reviewer / reconciler / security panel
short-circuits before it runs. See `docs/eval-methodology/harness-reference/`.
