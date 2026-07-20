# Data-architecture craft — selection · retrieval · grounding · memory

> Loaded by skill 03. **§1 datastore selection is always-on at `init`** — every project with state walks it. **§2
> retrieval · §3 grounding · §4 memory are modules**, each loading only when the spine's **`Data:`** line declares its
> trigger (registry: `shared/agentic-profile.md`, repo-root-relative per the no-`../` rule). §5 (volatile-decision
> classes) applies to any pillar; §6 is a dated reference appendix — **the only place product names appear.** The file
> is **criteria, not winners**: it fixes the durable decision axes and the enforceable teeth and delegates the volatile
> leaf facts (which engine, which model, which store) to §6's stamped tables and, at use time, to live-source
> verification (`shared/live-source-verification.md`). Reference REQs by ID; **state your own recall/latency/scale
> targets — never copy a borrowed benchmark number in as a constant.**

## The need-gate (§0)

Every module below opens with one shared question — **"do you need this capability at all?"** — asked before the
question of *how*. A retrieval stage, a grounding tier, a memory kind: each is earned by a **fired trigger** (a stated
requirement or a measured gap), and **the resulting ADR cites which trigger fired.** The corollary is what keeps the
craft from becoming ceremony: **when no trigger fires, the absence is correct — not a gap.** A plain CRUD app that
declares no `Data:` module is *complete*, not under-specified; a reconciler that invents a retrieval or memory finding
where the spine declared none is over-triggering (the critic-not-builder bound).

Enforcement splits by cost. The **deterministic pairing checks DA-T01–03** — a declared `Data:` value with no
realization, `retrieval(…)` with no eval floor, `grounded-writes(…)` with no write-path admission rule — run
mechanically in **Reconcile Pass 1** (`references/reconcile-architecture.md` §1b). The **content-clauses DA-T04–08**
live in each pillar's **teeth block** in this file and are cited by the reconciler exactly like the `topology` clause:
an ADR missing a required element is an *incomplete decision* — flagged, never silently accepted. Teeth carry stable
IDs (`DA-Tnn`); everything else here is rubric and protocol the architect applies with judgment.

## Datastore selection (§1 · always-on at init)

Every project with persistent state makes this decision; `init` walks the rubric even when the answer is the obvious
relational default. Decide along **seven dimensions in leverage order** — hardest-to-reverse first — each with a
default and the trigger that overrides it:

1. **Workload shape** (OLTP / OLAP / HTAP / mixed). *Default:* OLTP-primary until proven otherwise. *When-not:*
   analytical scans are a first-class, high-concurrency pattern (not a monthly report) → design a second engine or an
   embedded-OLAP rung from day one, even if you defer standing it up.
2. **Data-model fit** (relational / document / KV / wide-column / graph / time-series / vector). *Default:*
   **relational (Postgres-class)** — the one model that cheaply hosts the others as *secondary* patterns, **provided
   each secondary pattern names the specific mechanism it rides** (a JSONB column for document, a vector-index
   extension for embeddings, a time-series extension, recursive CTEs for shallow graph). An unfalsifiable "the database
   can handle it" is not a decision. *When-not:* a secondary pattern becomes **primary** at real scale (see the
   breakpoint classes below) → name the purpose-built store explicitly, never "NoSQL" generically.
3. **Consistency & availability — via PACELC, not CAP.** *Default:* strong consistency, single-region. *When-not:*
   name the **specific product requirement** forcing the tradeoff ("< 50 ms p99 reads from three regions", "stay
   writable through a regional outage") — never weaken consistency generically "for scale." PACELC is the working
   frame because it prices the latency/consistency tradeoff paid *every day*, not only during a rare partition.
4. **Scale envelope — single-node vs distributed.** *Default:* one well-tuned primary + read replicas until a
   **symptom** fires. *When-not — a symptom, never a fixed GB/row number* (the sources disagree by an order of
   magnitude): autovacuum persistently falling behind; a single table saturating I/O or CPU independent of overall
   load; write latency degrading despite tuning. The symptom *is* the revisit trigger; a copied "100 GB" threshold is
   the failure mode this dimension exists to catch.
5. **Operational maturity & cost — managed vs self-hosted.** *Default:* **managed**, for any team without a dedicated
   platform/DBA function. *When-not:* a platform team already operates many databases, residency/compliance a managed
   vendor cannot meet, or sustained scale where managed pricing crosses self-hosted TCO — argue it in **TCO** terms
   (personnel dominates the three-year cost), not sticker price, and treat the crossover figure as fast-moving.
6. **Team skill / choose-boring bias.** *Default:* what the team can debug unaided at 3 a.m. *When-not:* deviate only
   against a **named, budgeted** learning investment with a documented fallback — a novel store spends an innovation
   token against a stated need (the reconciler's novelty-budget lens), it is not a free preference.
7. **Exit / migration cost (reversibility).** **Not a when-not — a mandatory line either way.** State the
   reversibility class (**one-way vs two-way door**); if lock-in is accepted, say why the value justifies it
   ("accepted because X"). This is the dimension teams skip and later regret — record it even as a single sentence.

**Default posture and its breakpoints.** Start **relational + extensions**; split a workload out into a purpose-built
store only at a **named breakpoint class**, never a vague "when we outgrow it": sustained write throughput past a
single primary's ceiling · true multi-region active-active with local-write latency · multi-TB analytical scans under
concurrency · vector search past tens-of-millions of vectors under strict recall + latency SLAs · deep multi-hop graph
traversal as the *primary* access pattern. Between "query the primary directly" and "stand up a warehouse" sits a real
new middle rung — **embedded / in-process OLAP (DuckDB-class)** — reach for it first when analytical load is read-heavy
and single-writer. **LLM-app workloads reweight these categories; they do not invent new ones:** JSONB for
trace/transcript metadata, a co-located vector index for embeddings, a semantic cache for hot-context reuse, a queue in
front of async inference — each an existing category dialed up, not a new datastore class.

The **Review-Trigger** the teeth require is a **framework-original ADR field** (`templates/adr.md`): a symptom-based
revisit condition, observable ("autovacuum lag exceeds X", "single-table I/O saturates"), never "review periodically."

**DA-T04 — a datastore ADR REQUIRES:** ≥2 named alternatives · the decisive driver mapped to a rubric dimension
**and** a REQ-ID · a symptom-based **Review-Trigger** · an exit-cost statement · the durable commitment and the
vendor pick stated as two separate decisions. An ADR missing these is an incomplete decision — the reconciler
flags it (the `topology`-clause pattern).

## Retrieval (§2 · module: `Data: retrieval(<capability>)`)

Fires when the spine declares `Data: retrieval(<capability>)`. Retrieval is a **staged ladder**: start at the lowest
stage that meets a stated need and **escalate only on a measured gap or a stated query-share** — never because a
technique sounds sophisticated. Every escalation must leave a "why not simpler" trace in the ADR/spec.

- **Stage 0 — do you need retrieval at all?** Answerable from the model's parametric knowledge → **no retrieval.** A
  corpus that fits comfortably in context, is fairly static, and sees low query volume → **cache-and-stuff** the
  window. Revisit when the corpus outgrows the window, freshness tightens to daily+, or query volume makes even cached
  long-context cost exceed retrieval cost — **compute that $/query live at use time; never bake in a crossover
  multiplier** (published figures span orders of magnitude).
- **Stage 1 — the simplest retrieval that could work.** Structured/tabular data → a **structured query** (SQL/lookup)
  beats embeddings. Short single-purpose docs → **document-level** retrieval, no chunking. A small corpus already in
  an operational DB → an **in-database vector index** under *the architect's own stated scale target*, no dedicated
  engine yet.
- **Stage 2 — hybrid, the default first stage** (the center of gravity for most systems). **Lexical + dense, fused by
  a named fusion method** (RRF is the standard — "hybrid" with no named fusion is an incomplete decision). **Chunking**
  is declared as params (a token-size + overlap baseline the architect states), escalated to structure-aware / semantic
  / contextual chunking **only after a measured gap** the simpler setting cannot close; short or structured docs
  declare an explicit **no-chunking rationale** instead. The **embedding is a swappable seed** — shortlist via a public
  benchmark, *select via your own labeled eval set* (leaderboards are contaminated by training-on-eval-splits:
  shortlist tools, never decision-grade), name it with its **dimensions** and a **reindex trigger**, and design the
  reindex path so the model is not hardwired to one vendor's dimensionality.
- **Stage 3 — reranking (a measured addition, not a default checkbox).** *Add when* downstream precision matters and
  the first stage is measurably imprecise on the golden set. *When-not:* a small precise top-k, a structured corpus, or
  a latency budget that cannot absorb the extra pass — declare that latency budget if you add it.
- **Stage 4 — agentic retrieval (decomposition / retrieval-as-tool).** *Add when* queries are demonstrably multi-hop
  and the task value clears the token/latency multiple. **Bound it:** cap the iteration count (the first extra cycle
  yields most of the gain) and **route by a cheap difficulty classifier** — never send every query through an agent
  loop, and never on the default path for latency-sensitive, high-volume traffic.
- **Stage 5 — knowledge-graph augmentation (GraphRAG-class).** *Add only when* a real share of the workload is
  **global / sensemaking** (hybrid + rerank already cover fact lookup) and scale justifies the extraction cost — trace
  it to a **stated global-query-share**, re-derived from your own cost math, never a cited threshold. **Default to lazy
  / query-time construction** over full upfront indexing unless volume amortizes the index cost; budget for the real
  failure modes (imperfect entity extraction, silently hallucinated edges).
- **Stage 6 — evaluation, declared BEFORE Stage 2 (not after Stage 5).** A **golden query set** (≥20 hand-labeled
  queries, *graded* relevance, versioned beside the spec) · a **floor metric tied to the generator's actual k** · a
  **non-empty re-run trigger list** (embedding swap · chunking change · reranker change · index/quantization change ·
  corpus-schema change) · a production feedback loop (retrieval failures become new golden-set cases). This lands as an
  **`eval-suite` Verification-Contract row** — the anchor `DA-T02` pairs against.

Two durable cross-cutting facts the craft holds. **Context rot:** wider context windows absorb retrieval's *easy*
cases but do not replace it — accuracy degrades non-uniformly well before the advertised window limit, a real effect
independent of cost — so the 2026 default is **hybrid: retrieve a bounded window, then reason over it.** **Index posture
is architect-level; parameters are tuning:** the ANN index **family** (in-memory graph vs partitioned vs disk-backed),
**quantization**, and **CRUD posture** set the RAM-vs-SSD shape and the write path, and **must match the corpus's
stated freshness** (hourly updates paired with a batch-rebuild-only index is a contradiction). The per-family knobs
(`ef_*`, `nprobe`, PQ subvector count) are implementation work resolved against a recall/latency target — not
architecture.

**DA-T05 — a retrieval ADR/spec REQUIRES:** the stage declared · a "why not simpler" justification on any
Stage 3–5 escalation · chunking params or an explicit no-chunking rationale · the embedding named + dimensions +
a reindex trigger · **k-consistency** (the eval metric's k equals the k actually sent to the generator).

## Grounding & verification-against-data (§3 · module: `Data: grounded-writes(<capability>)`)

Fires when the spine declares `Data: grounded-writes(<capability>)` (presumptive under `Profile: agent-system`
wherever the agent mutates state). The governing principle: **LLM output is an untrusted proposal; only a separate
deterministic layer may turn it into committed state or a user-facing factual claim.** The architecture declares
**nine things** per grounded claim-type or write, each with a default and a when-not:

1. **Named ground-truth source** — the specific table / view / index / document-set, **never "our data"** (ideally
   referenced from an existing data catalog). *Default:* one canonical source per claim-type, with a precedence order
   if sources overlap. *When-not:* a greenfield prototype with no catalog still **names** the source — flagged
   ungoverned, not skipped.
2. **Freshness / staleness contract** — a max-staleness bound, TTL, "as-of" semantics surfaced to the user. *Default:*
   block or flag a response grounded past the bound. *When-not:* fixed reference data may be declared unbounded.
3. **Check tier per claim-type** — assigned from the three-tier taxonomy below.
4. **Numeric threshold + the action on crossing** — block / regenerate / auto-correct-and-flag / route to human. **A
   threshold with no declared action is not a control.** *Default:* require a declared number; a bare score name fails.
5. **Fallback per failure mode** — refuse (terminal — never silently retried against another provider), bounded-retry,
   degrade-to-safe-default, or escalate. **Silence — shipping the ungrounded response anyway — is never acceptable.**
6. **Provenance / audit line** — enough logged (source rows used · citation-resolution status · check scores +
   thresholds · model/schema version · admit-or-reject + reason) to **reconstruct "what grounded this output"** after
   the fact. *When-not:* pure UX copy with no factual claim and no downstream effect.
7. **Write-path admission rule** for state-mutating output: **schema → referential → business-rule → commit**,
   enforced at a layer the LLM cannot bypass (DB constraints, read-only connections, code allowlists) — never
   prompt-only. State what happens to a rejected proposal.
8. **Citation contract** — is a citation required; **resolution is deterministic** (it resolves to a real chunk/row —
   no excuse otherwise); **span-level support may be judged** (Tier 2/3); what happens with no valid citation (drop the
   claim / refuse / flag).
9. **Provider-portability note** — which provider-specific structured-output / grounding features are load-bearing and
   what breaks on a provider change (schema dialects are confirmed non-portable across providers).

**The three-tier check taxonomy** — flagged as **adopted synthesis** (this craft's organizing mental model, not
settled industry vocabulary): **Tier 1 — symbolic / deterministic** (schema, FK/constraint, allowlist, an encoded
formal-logic policy): passes an adversarial bite test. **Tier 2 — an independent learned classifier / NLI scorer** (a
provider grounding API or a dedicated NLI model — *not the generating model*), thresholded. **Tier 3 — same-model /
same-family self-check or LLM-judge**: weakest, because the blind spot that caused the error can also pass the grade.
Two rules bind the tiers: **Tier 1 is REQUIRED for any state-mutating claim** — money · identifiers · dates ·
regulated facts — and **Tier 3 is never the sole gate** for a claim a Tier-1/2 check could cover.

Two durable gotchas the craft must teach, because each disguises a weak check as a strong one:

- **Schema enforcement solves syntax, not truth.** Constrained decoding guarantees parseable, shape-correct JSON and
  **zero** guarantee the values are right. It is a precondition that removes parsing failures — never grounding, and
  never to be represented as one.
- **A "faithfulness score" may hide a judge one layer down.** Faithfulness-eval frameworks decompose a response into
  atomic claims *with an LLM call* before the entailment check runs — a number that looks deterministic inherits every
  judge-reliability problem, one layer removed from view. **Classify each check by what it actually is**, not by what
  it is named (and keep faithfulness — entailed by context — distinct from groundedness and from factuality; a response
  can be faithful-but-wrong or correct-but-unfaithful).

**LLM-issued queries are infrastructure-gated, not prompt-gated.** Read-only is enforced at the **driver / connection
layer** (a `read_only` connection, a DB-permission boundary), with table/column allowlisting checked in code against
the parsed query and `EXPLAIN`-based cost rejection — a prompt that "tells it not to write" fails by construction. This
is ordinary defense-in-depth applied to a new untrusted-input source; it generalizes to any LLM-driven mutation (files,
external APIs, queues), not only SQL. Any **judged** grounding check (a Tier-3 gate, or an NLI/faithfulness judge used
as a gate) is only as trustworthy as its **judge-validation record** — bind it via the evals-operations capability
(`shared/agentic-profile.md` §eval-suite); an unvalidated judge gates nothing.

**DA-T06 — a grounding spec REQUIRES:** a named ground-truth source per claim-type · a numeric threshold + the
action on crossing · a fallback per failure mode · driver-layer read-only enforcement for any LLM-issued queries.

## Agent memory (§4 · module: `Data: memory`)

Fires when the spine declares `Data: memory` (presumptive under `Profile: agent-system`), and backs the existing
`Category: memory` ADR (`templates/adr.md`). "Memory" means the **cross-session, learned/accumulated layer** — not
session state, workflow state, or audit records, which are different architectural layers that live outside model
context.

**Gate-0 — do you need designed memory at all?** Need **≥1** trigger: repeated same-domain/user tasks · corrections
that must stick · evolving domain rules · persistent entities across calls · a demonstrated token-cost of re-injecting
context · multi-agent shared state · a task that genuinely exceeds the context window. **Absent a trigger, session /
thread state (+ compaction for long single sessions) is correct** — and simpler; a bigger context window does not
eliminate designed memory, but it is no license to skip this gate. **The memory ADR itself cites which trigger fired.**

The **eight dimensions** (default · when-not):

1. **Kind scoping.** Working memory (the context window) is always on and free. *Default:* add **semantic** only if
   personalization / domain-fact accumulation matters; **episodic** only if the agent must recall *specific* past
   interactions; **procedural** last — newest and least-proven — and only with a real cross-task learning loop.
   *When-not:* skip episodic when only current-state facts matter; skip procedural without a learning loop.
2. **Substrate per kind.** *Default:* start relational/KV (+ an embedding column) or files; graduate to a dedicated
   vector store when fuzzy-recall volume demands it, and to a temporal knowledge graph only once multi-hop or
   contradiction-heavy reasoning is *demonstrated*. **Kinds want different backends** — a single undifferentiated
   "memory module" is itself a design smell. *When-not:* don't default straight to hybrid (two systems to operate is a
   named cost); don't stand up a graph for plain personalization.
3. **Write policy.** *Default:* **async / background consolidation** once past a demo (it protects user-facing
   latency); **retain verbatim alongside any extracted summary** where storage allows — extraction is a lossy,
   **one-way door**; declare explicit **add / update / delete / no-op** semantics for anything user-correctable.
   *When-not:* a hot-path synchronous write is defensible only for low-volume, latency-tolerant, high-value writes.
4. **Retrieval policy.** *Default:* **multi-signal** (recency + relevance + importance, extended with keyword / graph
   traversal as scale demands), with **recency first-class for episodic** content — plain similarity on episodic logs
   is a named anti-pattern. *When-not:* below ~a few hundred items a scoring formula is ceremony — a recency sort or
   return-all suffices until ranking matters.
5. **Lifecycle floor.** *Default:* **a TTL or a decay rule is mandatory** — **unbounded retention is a named failure
   mode**, not a neutral default (it degrades retrieval itself, not just cost); escalate from TTL to decay /
   importance-driven retention once TTL demonstrably drops still-true facts. *When-not:* never — some explicit
   lifecycle policy is required wherever memory beyond working memory exists.
6. **Sharing + authorization (multi-agent only).** *Default:* private-per-agent with a typed handoff contract unless
   deliberately designed around blackboard coordination; **name the sharing topology and the authorization boundary
   together** — shared mutable memory with no authorization model is an anti-pattern at any scale. *When-not:*
   single-agent systems skip this dimension.
7. **Privacy / retention.** *Default:* **tier by mutability / sensitivity**, redact PII at a **pre-write gate** (so
   every downstream store sees only the redacted form), and treat **derived-memory reach** as required whenever
   user-facing deletion is promised — deletion must reach summaries, indices, and profiles, not just source rows (an
   engineering mitigation for the GDPR-erasure ↔ audit-trail tension, not a legal guarantee). *When-not:* a
   non-personal-data store may skip GDPR-grade tiering — but says so explicitly, never by silent omission.
8. **Adversarial posture.** *Default:* treat **any write path fed by untrusted content as an injection surface**;
   **memory poisoning persists across sessions** (one successful write suffices, unlike prompt injection, which must
   re-land every turn) and, in shared setups, across agents — name provenance / source-attribution as a floor and
   freeze high-consequence memories behind human verification before trusting them as precedent. *When-not:* never
   optional once persistent memory exists — persistence itself changes the threat model.

**DA-T07 — a memory ADR REQUIRES:** the Gate-0 trigger cited · a per-kind substrate mapping · a lifecycle floor
(TTL/decay rule) · the sharing model + authorization boundary named together (multi-agent) · a deletion ⇒
derived-memory-reach pairing (when user-facing deletion is promised).

## Volatile-decision classes + use-time research (§5)

Applies to any pillar. Some decisions in this craft are **durable** (the rubric axes, the staged ladder, the tier
taxonomy) and some are **volatile leaf facts** that rot in months. The volatile ones fall into six **volatile-decision
classes**: **embedding model · reranker · vector store · memory product · grounding service · semantic cache.** This
file carries the *criteria* for choosing within each class; the winners live only in §6 and, at use time, in a
live-sourced record — **never in this section.**

A pick in a volatile class is **not** decided from training-data recall. It is proposed as a **Verify-live row** through
the existing flesh-out → Tier-2 flow (`shared/live-source-verification.md`): 03's Reconcile proposes the verify-live
constraint line, and the resolving ADR carries a **`Verified-against: docs/verification/<tech>.md`** citation to a
live-sourced record — that record is the **freshness anchor** `06`'s G11 gates on. The obligation rides the existing
L7/G11 enforcement unchanged; the craft adds no new gate.

This **use-time-research step is framework-original** — no studied gold-standard source encodes "consult the live state
of the world" as a guidance step; the field resists staleness only by encoding criteria and staging escalation. FD
already owns the mechanism (live-source verification), so extending it to volatile *data-stack* decision classes is a
structurally-enforced innovation — flag it as framework-original, not adopted consensus.

**DA-T08 — a volatile-class pick REQUIRES** a `Verified-against:` citation to its live-sourced record — the
existing S18 rule, applied to the six classes above.

## Landscape appendix (§6 · dated — verify at use time)

Reference only — **the one place product names appear.** These are *shortlist inputs*, never recommendations: the §5
protocol (a live-sourced `Verified-against:` record) is the authority, and every name here is subject to it. No
comparison numbers, no "best" — a name's presence here is not a pick.

**P1 · Datastore selection** — *landscape as of 2026-07; verify at use time (§5 is the authority)*

| Class | Named exemplars | Role |
|---|---|---|
| Serverless / managed Postgres | Neon · Supabase | scale-to-zero, branchable managed relational |
| Distributed SQLite / edge | Turso (libSQL) · Cloudflare D1 | edge-local, latency-critical SQL/KV |
| MySQL scale-out (+ Postgres) | PlanetScale | horizontally-sharded relational with optionality |
| Embedded / in-process OLAP | DuckDB (± `pg_duckdb`) | in-app columnar analytics before a warehouse |
| Warehouse / lakehouse | ClickHouse · Snowflake · BigQuery · Iceberg / Delta | multi-TB analytical scans at concurrency |

**P2 · Retrieval** — *landscape as of 2026-07; verify at use time (§5 is the authority)*

| Class | Named exemplars | Role |
|---|---|---|
| In-DB vector | pgvector / pgvectorscale | vectors co-located with SQL-joinable metadata |
| Dedicated vector store | Qdrant · Weaviate · Milvus · Pinecone · Turbopuffer · Vespa | scale / hybrid / filtering beyond the in-DB ceiling |
| Lexical / hybrid engine | Elasticsearch · OpenSearch | BM25 + hybrid where the stack already exists |
| Embedding model | Voyage · NV-Embed · Qwen3-Embedding · OpenAI text-embedding-3 · Gemini Embedding · BGE-M3 | dense representation; the fastest-moving class — swappable via reindex |
| Reranker | Cohere Rerank · Voyage Rerank · Zerank · Jina Reranker | cross-encoder precision on an imprecise first stage |

**P3 · Grounding & verification** — *landscape as of 2026-07; verify at use time (§5 is the authority)*

| Class | Named exemplars | Role |
|---|---|---|
| Provider grounding service | Bedrock (contextual grounding + Automated Reasoning) · Azure groundedness detection · Vertex Check Grounding | callable per-inference grounding score / symbolic check |
| Faithfulness-eval framework | RAGAS · DeepEval · TruLens | offline / CI groundedness + faithfulness scoring |
| Output validation / rails | Guardrails AI · NeMo Guardrails | programmatic output validation + dialog rails |

**P4 · Agent memory** — *landscape as of 2026-07; verify at use time (§5 is the authority)*

| Class | Named exemplars | Role |
|---|---|---|
| Memory framework | Letta (MemGPT) · Zep / Graphiti · Mem0 · LangMem · A-MEM | extract → store → selectively retrieve over transcripts |
| Provider-native memory | Anthropic memory tool (+ context editing) · OpenAI memory · Vertex Memory Bank | platform memory primitives, async consolidation |
| File-based | `CLAUDE.md` / `AGENTS.md` convention | low-volume, human-auditable, git-diffable memory |
