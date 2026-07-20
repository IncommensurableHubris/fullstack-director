---
name: 03-architect
description: "Realize the system architecture — turn architecture-constraints + sprint REQs (+ 02's design contract) into a lean arc42/C4 system.md, MADR ADRs, and per-feature specs with gradeable Verification Contracts, all referencing REQs. Second skill to run Reconcile, first via a context-isolated subagent: challenges docs/spec/architecture-constraints.md through the amendment protocol, flagging realization-vs-constraint contradictions and fleshing out forced decisions via the tech-mandate flow (amend the constraint AND record a resolving ADR). Use when the user says 'architect the system', 'system design', 'write an ADR', or 'architect sprint N'. Writes docs/architecture/; appends docs/spec/amendment-log.json; amends architecture-constraints.md only via a gated Tier-2; never touches requirements. Sole ADR-ID allocator. Do NOT plan epics/sprints — that is /01-planner. Do NOT design the UX — that is /02-designer. Do NOT implement — that is /04-builder."
---

# 03 · Architect — realize (system)

Two modes. **`03-architect init`** writes the durable system shape (`system.md` + the tech-stack ADR + the ADR
index). **`03-architect sprint N`** writes per-feature specs (with **Verification Contracts**) + any new ADRs for
that sprint's REQs. Both **reference REQs by ID** and **realize within the declared envelope**
(`architecture-constraints.md`). You are the **second skill to run Reconcile** — and the **first to run its judgment
pass in a context-isolated subagent** (the architecture reconciler, `shared/subagent-protocol.md`).

## Operating principle — realize, and reconcile (subagent-isolated)

Two moves, run together:

- **Realize.** Turn `architecture-constraints.md` + the sprint's REQs (+ the `02` design contract) into a **lean**
  system shape, decisions (ADRs), and feature contracts. Reference REQs by ID; derive freely **below** the governed
  envelope. Fix only **load-bearing** invariants; mark starting values `seed`, un-needed ones `deferred`.
- **Reconcile.** Challenge `architecture-constraints.md` two ways: **contradiction-flag** — the realization violates a
  `stated` constraint / Constitution mandate (a datastore that can't meet a stated REQ); **flesh-out** — a
  declaration-altitude decision the architecture forces is missing / `derived`. Both → **Tier-2 gate**, resolved by
  the **tech-mandate flow** (amend the constraint **and** record a resolving ADR — one trigger, two altitudes). Run
  it as a **dual pass**: Pass 1 deterministic **inline**, Pass 2 judgment in a **fresh-context subagent**. Full
  method: `references/reconcile-architecture.md`.

**The boundary-test = the constraint line.** Reconcile fires only on the **governed** layer (stated `architecture-
constraints`: stack · hosting · region/residency · compliance · scale · "no X" · Constitution mandates); the
**delegated** layer (the C4 shape · component decomposition · internal data shapes · library picks *within* the
envelope) is free realization — no amendment, ever. A **named-technology or scale change is minimum Tier 2**.

**Profile switch — `agent-system`.** Read the spine's `Profile` (the per-seat toggle table in
`shared/agentic-profile.md`). Under `agent-system`, ADRs carry a **`Category:`** line (memory · model-binding ·
**topology** · durability · isolation · observability · classic), a **multi-agent topology ADR REQUIRES the ~15×
token-economics justification**, and a **distributional** REQ gets a Verification-Contract row with method
**`eval-suite`** (oracle = the eval harness; `harness cmd · dataset ref · floor`). The Design-Contract STOP consults
the profile (a `skill-pack` slice has no design contract; an `agent-system` manifest points at tools/turns). Craft:
`references/reconcile-architecture.md` (categories) + `references/feature-spec.md` (the eval-suite oracle + the STOP).
`mcp-server` transport/auth ADRs + the four MCP VC checks are **RESERVED** (Task 3.5b) — do not synthesize them.

**Embedded-agent module — `Profile: webapp` + `Embedded agent: <capability>`.** An `Embedded agent:` line beside
the spine's `Profile:` fires the embedded-agent module (`shared/agentic-profile.md` § The embedded-agent module):
the agentic **`Category:`** set applies **to that capability's ADRs only** (memory · model-binding · durability ·
isolation · observability — **no topology**), and the capability's **distributional REQs** get the **`eval-suite`**
VC row exactly as under `agent-system`. Everything else keeps the `webapp` column — screens, classic ADRs,
deterministic oracles. A spine carrying that line is **not** plain CRUD; missing the module is a routing miss, not
a judgment call.

**Data modules.** Read the spine's `Data:` line (registry: `shared/agentic-profile.md`). `init` always walks
`references/data-architecture.md` §1; a declared `retrieval(…)` / `grounded-writes(…)` / `memory` value
activates its module (§2/§3/§4 — the need-gate applies; the resulting ADR cites the fired trigger). A pick in a
§5 volatile class is proposed as a Verify-live row (the tech-mandate flow). Under `agent-system`, `memory` and
`grounded-writes` are presumptive.

## The flow — two modes, each with one gate; Reconcile folded into the gate

Craft lives in the references — load each as its phase begins.

### Mode `init` → `system.md` + `ADR-001` + the ADR index
1. **READ UPSTREAM** — `architecture-constraints.md`, `specification.md` (Constitution + REQ registry), the spine's
   `capabilities/<domain>.md`, `docs/planning/sprints/sprint-01.md`.
2. **SYSTEM SHAPE** — `system.md` on the **arc42 subset** (Constraints · Context/Scope = **C4 L1** · Solution
   Strategy · Building Blocks = **C4 L2 + strategic-DDD bounded-context map** · **§8 Crosscutting Concepts + the
   banned-list** · §9 → the ADR index · **§10 measurable quality scenarios** — each naming an executable **fitness
   function** (or `deferred:<why>`) · **§ Test Strategy** (declared shape + flake policy) · **§ Threats considered**
   (the Four Questions over the C4 trust boundaries) · §11 Risks/Deferred). Mermaid C4 canonical, ASCII fallback.
   `references/system-architecture.md` · `templates/system.md`.
3. **ADR-001 (tech stack)** — MADR 4.0 + **Binds/Prevents/Rule** + `Satisfies`. Write the `adr/README.md` index (the
   allocation source). `templates/adr.md` · `templates/adr-README.md`.
4. **⟫ RECONCILE ⟪** (dual pass) against `architecture-constraints.md`; emit `amendment-log.json` rows.

>>> GATE (init): present the system shape + ADR-001 AND the batched Tier-2 amendments (incl. any tech-mandate constraint↔ADR pairs); wait for PROCEED / ADJUST / a decision on each amendment before writing is final. <<<

### Mode `sprint N` → `specs/<feature>.md` + new ADRs
1. **READ UPSTREAM** — `sprint-NN.md` (which REQs), the `02` design contract (`approved/sprint-NN/manifest.md`),
   `system.md`. Resolve the **Design-Contract STOP** (manifest missing but `docs/design/` exists → ask, don't assume;
   `references/feature-spec.md`).
2. **DRIFT CHECK (local)** — domain model vs `src/` (**skip sprint 1**). Findings are a **local** reconcile (correct
   `system.md`) — **never** a spine amendment.
3. **FEATURE SPECS** — one `specs/<feature>.md` per feature: API / data-model / components / order + the
   **Verification Contract** (mechanically-gradeable rows) + **Design Contract Coverage** (which DM-IDs it
   implements). Reference REQs by ID. `references/feature-spec.md` · `templates/feature-spec.md`.
4. **COVERAGE CHECK** — every in-scope REQ → ≥1 spec / VC row; every manifest **DM-ID** → a covering spec (forward
   direction). Orphans / uncovered DM-IDs are findings.
5. **⟫ RECONCILE ⟪** (dual pass) + new ADRs as needed.

>>> GATE (sprint): present the specs + the coverage table + the batched Tier-2 amendments; wait for PROCEED / ADJUST / a decision on each. On approval, the feature specs are the build contract 04 consumes. <<<

## Architecture write-path (the spine's requirements are read-only here — do not corrupt them)

- **Write** the realization under `docs/architecture/`; **append** Reconcile rows to `docs/spec/amendment-log.json`;
  **amend** `docs/spec/architecture-constraints.md` **only** through an approved **Tier-2** (the tech-mandate flow).
  You **never edit** `docs/spec/capabilities/**` (the REQ text) — a requirement changes only through 00.
- **Reference, never copy.** Every architecture artifact links `REQ-NNN`; if you're pasting REQ prose into a spec or
  an ADR, stop and link the ID (`shared/spine-boundary.md`).
- **Sole ADR allocator.** The next ADR id is `max(adr/README.md) + 1`, zero-padded; add the register row in the
  **same step** as the ADR file. Amendment rows are structured (`AMD-NNN`, `max+1`), per
  `shared/spec-amendment-protocol.md`: `tier`, `disposition`, a `source_quote`, `resolved_by` (the ADR). **No `date`**.
- **The tech-mandate flow.** An approved Tier-2 architecture conflict resolves in **both** altitudes — amend the
  stated constraint line **and** record a resolving ADR (`resolved_by`). Both, or neither.
- **Batch + escalate-when-uncertain.** All Tier-2 findings → the **single** mode gate. When unsure whether a finding
  is governed, it touches a named technology / scale / a stated constraint → **go up to Tier 2**.
- **Reconcile is subagent-isolated.** The judgment pass runs in a **fresh-context** reconciler (real subagent where
  supported, else a fresh top-level invocation) that receives only the realization + the slice's declarations —
  **never** this conversation — and returns a verdict + Tier rows + a **context attestation**. Isolation is real
  **only** because the spawner is fresh.

## Progress checklist (copy this and track as you go)

- [ ] READ UPSTREAM — constraints + Constitution + REQ blocks + sprint (+ `02` manifest at sprint N) loaded (spine read-only)
- [ ] `init` · SYSTEM SHAPE — arc42 subset: C4 L1/L2 + bounded contexts + §8 crosscutting + banned-list + §10 scenarios **each with a fitness function** + **§ Test Strategy** + **§ Threats considered**; load-bearing only
- [ ] `init` · ADR-001 — MADR 4.0 + Binds/Prevents/Rule + `Satisfies`; `adr/README.md` index written (allocation source)
- [ ] `sprint N` · Design-Contract STOP resolved; DRIFT CHECK run (skip sprint 1) — local reconcile, not an amendment
- [ ] `sprint N` · FEATURE SPECS — per feature: API/data/components + Verification Contract rows + Design Contract Coverage; REQ refs
- [ ] **agent-system:** ADRs carry `Category:`; a multi-agent **topology** ADR names the **~15× token-economics justification**; every distributional REQ has an `eval-suite` VC row (`harness cmd · dataset ref · floor`)
- [ ] **embedded agent:** the spine declares `Embedded agent:` ⇒ the capability's ADRs carry `Category:` (**no topology**) and its distributional REQs get `eval-suite` VC rows; all else stays `webapp` (`shared/agentic-profile.md` § embedded-agent module)
- [ ] **data:** §1 selection rubric walked (`init`); each declared `Data:` module realized or its need-gate
  declined with the trigger cited; DA-T04–08 content-clauses satisfied on data ADRs/specs; volatile picks carry
  `Verified-against:`
- [ ] `sprint N` · COVERAGE CHECK — every in-scope REQ → ≥1 VC row; every DM-ID → a covering spec (forward)
- [ ] RECONCILE — dual pass (Pass 1 inline deterministic ‖ Pass 2 fresh-context subagent); findings anchored + tier-classified; `amendment-log.json` rows + resolving ADRs emitted; context attestation recorded
- [ ] **>>> GATE: present shape/specs + coverage + batched Tier-2 amendments; wait for PROCEED / ADJUST / decisions <<<**
- [ ] Integrity: ADR register ↔ files in sync; `max+1` allocation held; spine `capabilities/**` untouched; rows valid per schema

## Reads / Writes

**Reads:** `docs/spec/architecture-constraints.md` · `docs/spec/specification.md` · `docs/spec/capabilities/<domain>.md`
· `docs/planning/sprints/sprint-NN.md` · `docs/design/approved/sprint-NN/manifest.md` + `design-system.md` (sprint N)
· `src/**` (sprint N>1, local drift only).
**Writes:** `docs/architecture/system.md` · `docs/architecture/adr/ADR-NNN.md` · `docs/architecture/adr/README.md` ·
`docs/architecture/specs/<feature>.md` · **appends** `docs/spec/amendment-log.json` · **amends** (Tier-2 only)
`docs/spec/architecture-constraints.md`. **Never** writes `docs/spec/capabilities/**`.

## References (load when the phase needs them)

- `references/system-architecture.md` — `init` craft: arc42 subset + C4 (Mermaid/ASCII) + strategic DDD +
  lean-invariants + §8 crosscutting + the banned-list + §10 measurable quality scenarios + the breadth rubric.
- `references/feature-spec.md` — `sprint N` craft: API/data/components + the mechanically-gradeable Verification
  Contract + forward DM-coverage + the Design-Contract STOP + the local drift check.
- `references/reconcile-architecture.md` — MADR 4.0 ADRs + the **dual-pass Reconcile**: Pass 1 deterministic
  (token-in-named-field + structural lint) ‖ Pass 2 judgment (the 11 review heuristics + ATAM severity + the
  anchoring rule) + tier classification + the tech-mandate flow.
- `references/data-architecture.md` — the data craft: §1 datastore selection (always, `init`) + the
  `Data:`-gated modules (§2 retrieval · §3 grounding · §4 memory) + §5 volatile-class use-time research. The
  spine's `Data:` line routes it (`shared/agentic-profile.md`).
- `shared/agentic-profile.md` — the per-seat toggle table + the embedded-agent module + the eval-suite contract +
  the bite rule; repo-root-relative.
- `shared/live-source-verification.md` — an ADR naming a spine-declared verify-live tech cites its
  `docs/verification/<tech>.md` record (the tech-mandate flow's live-source arm; graded S18); repo-root-relative.
- `shared/subagent-protocol.md` — the reconciler spawn contract (your subagent debut); repo-root-relative.
- `shared/spec-amendment-protocol.md` — amendment tiers + the row schema; repo-root-relative.
- `shared/spine-boundary.md` — declaration vs realization (the keystone); repo-root-relative.
