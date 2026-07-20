# Reconcile architecture — MADR ADRs + the dual-pass that challenges `architecture-constraints.md`

> Loaded by skill 03 at the **Reconcile step** (folded into each mode's gate). This is `03`'s debut of the
> **subagent-isolated** Reconcile — the second skill to run Reconcile, the **first to run its judgment pass in a
> fresh-context subagent** (`02` ran it inline). Read it with `shared/spec-amendment-protocol.md` (the tiers + the
> row schema), `shared/subagent-protocol.md` (the reconciler spawn contract), and `shared/spine-boundary.md` (the
> keystone) — all repo-root-relative, no `../`. Stance: **be a critic, not a builder** — bounded to findings that
> *change this slice or violate the envelope*, never nice-to-haves.

## What Reconcile is, and its two components

`architecture-constraints.md` is a thin **declaration** (the envelope the user requires); `system.md` / the ADRs /
the feature specs are `03`'s **realization**. While realizing, `03` challenges the declaration two ways, then logs
the results as structured amendment rows:

- **(a) contradiction-flag (correctness).** The realization *violates* a `stated` constraint or a Constitution
  mandate — the architecture the slice needs cannot be built inside the declared envelope (e.g. the datastore the
  constraint names cannot satisfy a stated REQ). Flag it → **Tier-2 gate**.
- **(b) flesh-out (completeness).** A declaration-altitude decision the architecture *forces* is missing or
  `derived` in `architecture-constraints.md` (hosting, region, a datastore the spine never pinned). `03` proposes
  the concretization → **Tier-2 gate** → on approval the constraint upgrades to `stated`.

Both resolve through the **tech-mandate flow** (below): one trigger, **two altitudes** — the constraint amendment
**and** a resolving ADR.

## The boundary-test, made concrete — the constraint line

Reconcile fires **only on the governed layer**. The delegated layer is free realization and **never** produces an
amendment. The seam is checkable — it is the stated-constraint line, not taste:

| Governed → **Reconcile fires** | Delegated → **free realization** |
|---|---|
| stated `architecture-constraints` (**stack · hosting · region/residency · compliance · scale · "no X"**) · Constitution mandates · declared crosscutting concepts | the C4 shape · component decomposition · internal data shapes · library picks *within* the envelope |

So *"would the user object to this changing silently?"* becomes the answerable *"does this change a stated
constraint / a named technology / a stakeholder-opinion decision, or is it craft within the envelope?"* **A
named-technology or a scale change is minimum Tier 2.** Picking Hono vs Express inside a stated "TypeScript/Node"
envelope is delegated — ship it. Swapping the stated datastore is governed — gate it.

## Decisions are MADR 4.0 ADRs — with Binds / Prevents / Rule

`03` is the **sole `ADR-NNN` allocator**; the next id is `max` in `adr/README.md` **+ 1**. Each decision is a
**MADR 4.0** record (`templates/adr.md`) — *Status · Context & Problem · Decision Drivers · Considered Options ·
Decision Outcome (incl. **Confirmation**) · Consequences* — extended with the BMAD discipline that makes an ADR
enforceable rather than a diary entry:

- **Binds:** what this decision *commits* the build to (the constraint/REQ it satisfies — `Satisfies: REQ-008` /
  `Satisfies: architecture-constraints "Datastore"`).
- **Prevents:** what it *rules out* (the alternatives now closed).
- **Rule:** a **checkable enforcement** — the MADR *Confirmation* stated as a fitness function ("no module under
  `domain/` imports from `infra/`", "the datastore driver is a client-server driver, not embedded"). A Rule that
  cannot be checked is a weak ADR — sharpen it until a lint / a test / a grep can decide it.
- **Supersedes:** the ADR this replaces (`null` for a new line). A superseded ADR stays on file, status
  `Superseded by ADR-NNN` — ADRs are immutable; you add, never rewrite.

The Rule is what lets the reconciler cite an ADR as an anchor and what a `static-conformance` Verification-Contract
row executes. This beats a homegrown ADR (no enforcement hook) and the SDD tools' steering-blob /
constitution-only rationale (no first-class, checkable record).

### Agentic ADR categories — `Profile: agent-system`, or the embedded-agent module (capability-scoped)

Under an agent profile, every ADR carries a **`Category:`** line (`templates/adr.md`) naming the decision class the
agentic architecture forces — so the categories the field has no convention for become first-class, checkable
records. Under `Profile: webapp` with an **`Embedded agent:`** line, the same requirement applies to **the declared
capability's ADRs only, minus `topology`** (`shared/agentic-profile.md` § The embedded-agent module) — the rest of
the architecture stays classic:

- **memory** — context/memory architecture (what persists · store · TTL · eviction — the *realization* of the
  agent-contract's memory **policy**, which is the declaration).
- **model-binding** — model selection + prompt-idiom binding (which model, and the prompt style it is tuned to;
  a swap is a config change requiring re-eval — see `shared/model-migration-protocol.md`).
- **topology** — the orchestration shape: **single vs orchestrator-worker vs handoff vs swarm**. **A multi-agent
  topology ADR REQUIRES a ~15× token-economics justification** — a multi-agent system burns ≈15× the tokens of a
  single agent (Anthropic's multi-agent economics), so the ADR must record the value that justifies that cost
  (parallel breadth · independent context windows · fault isolation) *against the ~15× multiplier*, or choose
  single-agent. **A swarm/orchestrator ADR with no economics justification is an incomplete decision — the reconciler
  flags it.** (Evolving one agent into an orchestrator is a **gated ADR**, not a spine amendment: topology is
  realization *within* the agent-system envelope — the declaration/realization test applied to topology.)
- **durability** — durable execution / retry / resumability of long-running runs.
- **isolation** — sandbox + credential-injection model (how tools run; how secrets reach them).
- **observability** — the tracing plan (the OTel GenAI span tree `invoke_agent → chat → execute_tool`, token/cost
  attributes) — the plan 06's **G9** checks is emitting.

`classic` is the default (a webapp decision). **`mcp-server` categories (transport/auth) are RESERVED** — built on
the first `mcp-server` project (Task 3.5b); do not synthesize them speculatively.

## Run the two passes independently, then merge

Run Pass 1 (mechanical) and Pass 2 (judgment) **without letting one bias the other** — interleaving lets an easy
mechanical "all clear" suppress a harder judgment finding. Then merge: de-dupe by target, keep the higher
tier/severity, preserve the anchor and the `source_quote`. **Pass 1 runs inline in the parent** (it is unbiasable, so
isolation buys nothing, and keeping it off the subagent path keeps the eval robust). **Pass 2 runs in a fresh-context
subagent** (architecture judgment is exactly where the realizer self-prefers).

---

### Pass 1 — the deterministic detector (mechanical, no taste; runs INLINE)

Two mechanical checks. Each produces a **computed** finding — which is what makes an *architecture* contradiction
gradeable without a human or an LLM judge.

#### 1a · The token-in-named-field constraint check (`03`'s WCAG-arithmetic)

A `stated` constraint that names a **forbidden or required token** — a technology, a region, a host, a protocol — is
checked by **set membership** over a *designated structured field* of the realization: the `system.md` **Stack** list,
an **ADR *Decision*** field, a dependency / data-model line, an OpenAPI `security` block.

```
HONORS   = required token present  (e.g. constraint "EU region" → hosting field contains an EU region)
         AND forbidden token absent (e.g. constraint "no third-party SSO" → no Auth0/Okta/Google-OAuth in the auth ADR)
VIOLATES = the inverse
```

Worked example (the eval's discriminator): `architecture-constraints.md` states **`Datastore: SQLite (embedded, no
external DB server)`**, but REQ-008 requires a **scheduled worker process** generating digests while the web app
serves members, and the deploy envelope is **multiple stateless instances behind a load balancer**. Embedded SQLite
is node-local and single-writer — it *cannot* be the shared store for multiple stateless nodes. The set-match on the
Stack field flags the conflict → a **Tier-2** contradiction. Never silently swap to PostgreSQL (the datastore is the
user's stated call) and never silently ship a build the constraint forbids — **gate it** and record the resolving
ADR. Grounded in real conformance tooling (ArchUnit, dependency-cruiser, Spectral, conftest/OPA): a constraint token
→ a set-membership check over a named field.

#### 1b · The structural lint (BMAD's `lint_spine`, architecture edition)

Mechanically detectable defects, each a finding:

- **placeholders** left in `system.md` / specs / ADRs; **unpinned versions** where a version matters.
- **duplicate or missing `ADR-NNN`**; an `adr/README.md` index out of sync with the files.
- **orphan REQs** — an in-scope sprint REQ with no covering feature spec / Verification-Contract row.
- **uncovered DM-IDs** — a `02` manifest element no spec claims (the forward-coverage gap).
- **a silently-owned dimension** — the breadth rubric (data · API · authN/authZ · **ops/deploy envelope** ·
  observability · scale · security), a dimension neither specified nor visibly deferred in §11.
- **a declared crosscutting concept absent** from §8; a mechanically-detectable smell subset (a cyclic dependency,
  a god container by size, a hub by fan-in/out).
- **data pairing checks (DA-T01–03):** a declared `Data:` value with no corresponding realization section/ADR
  (**DA-T01**); `retrieval(…)` declared with no `eval-suite` VC row whose golden-set dataset ref resolves
  (**DA-T02**); `grounded-writes(…)` declared with no write-path admission rule named in the realization
  (**DA-T03**).

---

### Pass 2 — the judgment pass, in the FRESH-CONTEXT reconciler subagent

Isolation is the point: architecture judgment is where the realizer's own reasoning self-prefers (~+25%). Per
`shared/subagent-protocol.md`:

- **Spawned from a _fresh_ `03` invocation** (a real subagent where the harness supports one; a fresh top-level
  invocation otherwise). It **receives only** the realization (`system.md` / the ADRs / the specs) **+** the slice's
  declarations (`architecture-constraints.md` + the in-scope REQ blocks + the declared crosscutting concepts).
  **Never** the realization conversation — that inheritance is what makes inline self-review fictional.
- It applies the **11 architecture-review heuristics** (the Nielsen-equivalent — named lenses that convert taste into
  judgment):

  1. **Quality-attribute coverage** — every prioritized ISO/IEC 25010:2023 attribute has a **measurable §10
     scenario**; an unmeasured "-ility" is a finding.
  2. **Tradeoff explicit** — Richards/Ford **First Law: everything is a tradeoff**; a decision naming no sacrifice is
     a finding.
  3. **Sensitivity & risk** — **ATAM**: locate the decisions a key scenario is *sensitive* to; flag where two
     attributes trade off; classify **risk / non-risk**.
  4. **Dependency direction** — the **Dependency Rule** / ports-and-adapters: source dependencies point toward
     stability/abstraction; **domain never depends on infrastructure**.
  5. **Connascence — strength × locality** — strong/dynamic connascence (Meaning, Position, Timing, Value, Identity)
     **crossing a module/context boundary** is a finding (Rules of Degree + Locality).
  6. **Coupling/cohesion smells** — no **cyclic · god · hub-like · unstable** dependency (Sharma); flag Martin's
     zone of pain/uselessness.
  7. **No structural anti-pattern** — big ball of mud · distributed monolith · leaky/ambiguous abstraction.
  8. **Distribution realism** — every distributed boundary answers the **8 Fallacies** (network reliable? latency
     zero? bandwidth infinite? secure? topology stable? …).
  9. **Essential vs accidental complexity** — complexity must be justified by a requirement, not incidental.
  10. **Novelty budget** — novel tech spends a counted **innovation token** (Choose Boring Technology) against a
      stated need; else a golden-hammer finding.
  11. **Enforceability** — each constraint that matters is (or can be) a **fitness function**; an unenforceable
      constraint is a finding.

  Plus **crosscutting-concept / banned-list conformance** (§8). **Data-decision ADRs/specs carry the DA-T04–08
  content-clauses** (`references/data-architecture.md`, per-pillar teeth blocks) — cite them like the topology
  clause. **Severity is ATAM-shaped:** *risk* (must fix) / *sensitivity* (watch) / *tradeoff* (accepted,
  documented) / *non-risk* (OK).

> **The anchoring rule — the single rule that converts taste into judgment.** Every finding cites **exactly one**
> anchor — a named **25010 attribute** (with its scenario), a **stated constraint**, a **named architecture smell**,
> a **connascence type / violated dependency metric**, or a **violated fitness function** — and names the **tradeoff**
> it implies. **Bare "cleaner / more scalable" is inadmissible** (the analogue of `02`'s banned "looks better"). If
> you cannot name the anchor, you are architecting (free realization — just do it), not reconciling.

- The reconciler **returns ONLY** a verdict + Tier-classified rows (each with a `source_quote`) + a **one-line
  context attestation** — never full prose. The attestation
  (`inputs: [architecture realization, architecture-constraints + in-scope REQ blocks]; realization conversation: not
  provided`) is a **declared-inputs statement, not proof of isolation**: the parent transcribes it into the
  artifacts, so a parent that leaked context would transcribe it unchanged. The eval grades its **presence**
  deterministically; isolation itself rests on the **fresh-spawner discipline + the seed-only instruction**
  (`shared/subagent-protocol.md`) — predictive controls, declared as such. A transcript-absence check (no
  realization-reasoning markers in the parent transcript) is an **evidence** layer only where the harness persists
  spawn transcripts; where it does not, that check is UNVERIFIABLE and must not be claimed as proof. **Pass 1 is
  what the eval grades** (deterministic, no subagent dependency); **Pass 2 is the isolation-critical quality
  layer — human-gated, never deterministically graded** (AI-interpreted judgment carries no 100% guarantee).

---

## Classify → amendment tiers, and the tech-mandate flow

Merge the passes, then classify each surviving finding (full semantics in `shared/spec-amendment-protocol.md`):

| Finding | Tier | Disposition |
|---|---|---|
| Realization contradicts a `stated` constraint / a Constitution mandate (named tech / region / scale) | **Tier 2** | `gated` → `approved` |
| Flesh out a missing / `derived` declaration-altitude decision the architecture forces | **Tier 2** | `gated` → `approved` |
| A pure clarification with exactly one defensible answer, no user-observable / named-tech change | Tier 1 | `auto-applied` (rare — most architecture calls touch a named technology, which is governed) |
| Honoring the finding adds / removes / reprioritizes a capability (scope) | **Tier 3** | `deferred` → `00 reflect` |

**Escalate when uncertain.** Mis-classifying *down* silently corrupts the user's intent; mis-classifying *up* costs
one extra gate. A named-technology or scale change is **minimum Tier 2**.

> **The tech-mandate flow — one trigger, two altitudes.** An approved Tier-2 architecture conflict resolves in **both**
> places: (1) the **declaration** — amend `architecture-constraints.md` (replace the stated line, e.g. `Datastore:
> SQLite` → `Datastore: PostgreSQL`); (2) the **realization** — record a **resolving ADR** (MADR + Binds/Prevents/Rule)
> whose *Decision* names the new technology and whose *Rule* makes it checkable. The `amendment-log.json` row's
> `resolved_by` points at that ADR. A constraint amendment with no resolving ADR (or vice-versa) is an incomplete
> tech-mandate — both, or neither.

**Batch** every Tier-2 finding from the pass into the **single** mode gate — never interrupt the user once per
finding. **Exclude** anything an existing ADR already settled. **Local code↔doc drift stays local** (a `system.md`
correction, no amendment).

> **Verify-live techs (WS6).** An ADR whose *Decision* names a spine-declared verify-live tech
> (`architecture-constraints.md` § Verify-live) **must carry a `Verified-against: docs/verification/<tech>.md`
> citation** — the API/config it commits to was live-source-verified, not recalled from memory. An uncited reliance
> is a **Reconcile finding** (graded S18). A tech-mandate that *introduces or changes* a verify-live tech
> **re-verifies** (a fresh, cited record) as part of the constraint-amendment + resolving-ADR pair — the record is
> the freshness anchor `06` G11 gates on. Full doctrine: `shared/live-source-verification.md`.

## Emit structured rows — the output Reconcile is graded on

Findings are logged as **rows in `docs/spec/amendment-log.json`**, not prose in a report. Append to the existing
`{ "amendments": [ … ] }` array; each row (schema in `shared/spec-amendment-protocol.md`):

```json
{
  "id": "AMD-001",
  "req": "REQ-008",
  "skill": "03-architect",
  "tier": 2,
  "disposition": "approved",
  "source_quote": "architecture-constraints.md: 'Datastore: SQLite (embedded, no external DB server)' vs REQ-008 scheduled worker + multi-instance deploy",
  "supersedes": null,
  "resolved_by": "ADR-002"
}
```

- `id` — `AMD-NNN`, zero-padded, `max(existing)+1`. `req` — the REQ if REQ-scoped, else `null`.
- `disposition` ∈ `pending | auto-applied | approved | deferred`. A gated Tier-2 is `approved` once accepted at the
  gate (`pending` only if logged before the gate resolves). **No `date`** — git is the trail.
- `source_quote` — the **exact declaration text** the finding is about (for a contradiction, quote the constraint
  **and** the REQ/mandate it collides with), so a reviewer sees what changed without diffing.
- `resolved_by` — the **ADR-ID** that records the realization decision (the tech-mandate partner), or the reflect
  decision for a Tier-3; `null` while `pending`.

## The over-trigger guard — critic, not builder

Reconcile earns its gate by being **bounded**. Before logging a finding, confirm it (a) is anchored and (b) either
**changes this slice** or **violates the envelope**. A nice-to-have, a future-sprint idea, or a delegated-layer
library preference is **not** an amendment — it is free realization or out of scope. A clean, fully-`stated`
`architecture-constraints.md` whose envelope the natural architecture honors should yield **~zero** amendments;
surfacing invented conflicts there is the failure mode the eval's clean-constraint (false-positive) case checks for.
