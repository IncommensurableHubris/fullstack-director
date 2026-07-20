# T4 — Agent Memory Architecture: Research Brief

Pillar: agent memory as a datastore + retrieval + lifecycle decision. Compiled July 2026 from live web sources;
no local repository files were read.

## 1. Executive Summary

- The field has converged on a **cognitive taxonomy** of memory *kinds* (working / episodic / semantic /
  procedural, sometimes + sensory) but has **not** converged on which *substrate* (vector / graph / relational /
  KV / files) implements each kind — that remains the live architecture decision, not a solved default. CONSENSUS
  (taxonomy) / CONTESTED (substrate). DURABLE.
- Every system studied (Letta, Zep/Graphiti, Mem0, LangMem, A-MEM, Google Memory Bank, Anthropic's memory tool)
  embodies the same move — extract structured signal from raw transcript, store it apart from working context,
  retrieve selectively — differing only in WHEN extraction happens and WHAT structure it lands in. DURABLE
  pattern; FAST-MOVING implementations.
- Hybrid retrieval (dense + sparse/BM25 + graph traversal) is displacing pure vector-similarity as the 2026
  default beyond toy scale; the 2023 Stanford recency/importance/relevance formula is now one signal family among
  several, not the whole scoring function. CONSENSUS direction, CONTESTED specifics. FAST-MOVING.
- Asynchronous/background consolidation ("dreaming," post-ingestion batch passes) is now the dominant write
  pattern precisely because synchronous LLM-mediated writes tax user-facing latency — both OpenAI's and Google's
  2025-2026 systems moved this direction. CONSENSUS. DURABLE principle; FAST-MOVING technique.
- A June 2026 ablation reports verbatim-chunk storage beating LLM-extracted/summarized artifacts for
  long-conversation recall — contesting the summarize-everything orthodoxy that shaped 2024-2025 designs.
  CONTESTED, single-source. FAST-MOVING, but flags a DURABLE risk: extraction is a lossy, one-way door.
- Memory poisoning is a structurally distinct security surface: a write attack need succeed only once and then
  persists across sessions (and, in shared setups, across agents/users), unlike prompt injection which must
  re-land every turn. Query-only attacks hit ~95-98% injection success with zero elevated privilege. CONSENSUS
  this is a distinct threat class. DURABLE principle; FAST-MOVING attack/defense detail.
- GDPR's right-to-erasure and the EU AI Act's mandatory audit-trail obligation (full applicability 2 August 2026)
  are in direct, unresolved tension for any durable memory store. The practitioner mitigation is tiering memory
  by mutability/sensitivity so deletion and audit duties attach to different tiers. CONTESTED; DURABLE constraint.
- The scoping trigger practitioners actually use is narrower than "does the agent span sessions": repeated
  same-domain/user tasks, corrections that must stick, evolving domain rules, persistent entities across calls,
  or demonstrated token-cost from re-injecting context. Below that bar, session/context-window handling is
  correct and simpler. CONSENSUS. DURABLE.
- 2026 research visibly pivoted from *capability* (how to structure/retrieve memory) to *governance*
  (provenance, verified forgetting, type-isolation against contamination, audit trails), with several major
  surveys landing within months of each other in H1 2026; no source claims one winning architecture, and
  multiple 2026 sources frame the space as fragmented because different memory *kinds* structurally want
  different backends — making a one-size-fits-all "memory module" a design smell in itself. CONSENSUS both
  points. DURABLE — directly relevant to an anti-ceremony framework.
- Provider-native memory has split into two distinct products worth not conflating: consumer-facing always-on
  personalization (ChatGPT memory, Claude.ai memory) vs developer-platform building blocks (Anthropic's memory
  tool + context editing, Google's Memory Bank) — an architecture skill should target the latter. CONSENSUS.
  DURABLE.

## 2. Findings

### 2.1 Memory taxonomies
The dominant academic taxonomy is five "atomic cognitive memory systems" — sensory, working, episodic, semantic,
procedural — per the 27-institution survey "Rethinking Memory Mechanisms of Foundation Agents in the Second
Half" (arXiv 2602.06052v3, corpus through Q4 2025). Episodic memory "stores specific experiences situated in
time and context"; semantic memory "accumulates abstract facts and conceptual knowledge." Working memory is
consistently equated with the context window itself, not a separate store. LangGraph/LangMem's official docs
(docs.langchain.com/oss/python/concepts/memory, 2026) operationalize a narrower, practically-implemented
three-part subset — semantic, episodic, procedural — folding working memory into thread-scoped state. The
2602.06052 survey critiques prior schemes for conflating memory *kind* with memory *management strategy*, and
proposes kind, substrate (external: vector/text-record/structural/hierarchical; internal: weights/latent-state/
KV-cache), and subject (user- vs agent-centric) as three separate axes. CONSENSUS on kind vocabulary; CONTESTED
on substrate mapping — exactly the decision an architecture rubric must walk rather than assume. DURABLE
(cognitive-science grounding predates the LLM-agent wave, unlikely to be displaced by 2028).

### 2.2 Systems landscape
- **Letta (MemGPT lineage)** — OS-style virtual-memory paging, agent-directed. Three regions: main context
  ("managed like RAM"), archival memory (external DB/vector store), recall memory (searchable conversation log);
  the LLM issues function calls to page in/out and can self-edit its system prompt (leoniemonigatti.com/blog/
  memgpt.html). Distinguishing bet: the model decides what to page, not an external policy — a choice other
  systems reject. DURABLE pattern; FAST-MOVING product.
- **Zep/Graphiti** — bitemporal knowledge graph: every edge carries event-time and ingestion-time, enabling
  non-destructive handling of contradictory/updated facts; retrieval fuses dense + BM25 + graph traversal with no
  LLM call at read time (arXiv 2501.13956, Jan 20 2025, Zep's own team — VENDOR-AFFILIATED). Self-reported
  benchmarks (94.8% vs 93.4% on DMR against MemGPT; up to 18.5% gain and 90% latency cut on LongMemEval) are
  landscape data, not independent verification. DURABLE pattern; FAST-MOVING/unverified numbers.
- **Mem0** — extraction-then-reconciliation: an LLM extracts candidate facts, compares each against top
  semantically-similar existing memories, and emits ADD / UPDATE / DELETE / NOOP, resolving contradictions at
  write time rather than at retrieval-time ranking; an optional graph variant adds entity/relation edges
  (mem0.ai, Jul 16 2026 — VENDOR, self-reported, explicitly lacking independent adoption data). Caution: GitHub
  issue mem0ai/mem0#4896 documents a shipped path falling back to MD5-hash-only dedup with no semantic conflict
  resolution — reconciliation is the design intent, not always the shipped behavior. DURABLE pattern;
  FAST-MOVING/unreliable implementation.
- **LangMem/LangGraph Store** — namespaced KV store with pluggable update strategies: semantic memory as an
  overwritten "profile" or a growing "collection"; episodic memory as few-shot examples; procedural memory as the
  agent rewriting its own stored instructions via reflection (docs.langchain.com, 2026), with no prescriptive
  profile-vs-collection default — even the framework vendor treats this as open. DURABLE pattern; CONTESTED
  default.
- **A-MEM** — Zettelkasten-style dynamic linking: new memories are atomic notes with generated context/
  keywords/tags, and writing a new note can trigger *retroactive updates* to older notes ("memory evolution"),
  unlike one-way consolidation (arXiv 2502.12110, Feb 2025, NeurIPS 2025). Peer-reviewed but benchmark-only; no
  major commercial framework has adopted retroactive note-editing yet — promising but narrow.
- **File-based memory (CLAUDE.md/AGENTS.md convention)** — plain-text, git-diffable, human-and-agent-readable
  files read at session start (code.claude.com/docs/en/memory), conventionally kept under ~200 lines since
  "longer files consume more context and reduce adherence." The simplest possible substrate: no retrieval
  algorithm needed because the whole store fits in context. DURABLE as a default-first option for low-volume,
  high-stakes, human-auditable memory; wrong once volume exceeds what fits comfortably (degrades like any
  unmanaged context — 2.9).
- **Provider-native**: Anthropic's developer-platform **memory tool** (`memory_20250818`, GA on the Messages API)
  gives Claude file-CRUD over a memory directory, paired with **context editing** (stripping stale tool results
  past a token threshold); 84% token savings combined, self-reported (platform.claude.com/docs) — distinct from
  Claude.ai's separate consumer personalization memory. OpenAI's ChatGPT memory moved from explicit saved facts
  (Apr 2024) to background "dreaming" (Apr 2025) to a rebuilt "Dreaming V3" (Jun 2026) consolidating during idle
  compute rather than at request time, reporting large self-measured gains (time-sensitive accuracy 9.4%→75.1%;
  openai.com/index/chatgpt-memory-dreaming/). Google's **Vertex AI Memory Bank** (preview Jul 8 2025) separates
  Sessions (short-term) from Memory Bank (long-term) using Gemini for asynchronous topic-based extraction, on an
  ACL-2025-accepted method (peer-reviewed). Net DURABLE pattern across all three: decouple extraction/
  consolidation from the live request path.

### 2.3 Memory as a datastore decision
No datastore wins across workloads; the axis is query pattern, not raw performance. Vector stores: fast,
zero-cold-start, strong unstructured recall, but "don't reason about relationships between items"
(atlan.com/know/vector-store-vs-graph-database-agent-memory/, 2026). Knowledge graphs: deterministic, multi-hop,
explainable, but carry real cost — entity-extraction pipelines, ontology design, and a cold-start problem
(atlan.com/know/agentic-ai-memory-vs-vector-database/; machinelearningmastery.com, both 2026). CONSENSUS on the
trade-off shape; CONTESTED on where the threshold sits for a given app. Secondary sources call hybrid vector+
graph "the community standard for complex enterprise agent memory as of 2026," but an independent practitioner
source (agiusalexandre.com, May 16 2026) frames the landscape as fragmented and unsolved, warning against
over-engineering before a real retrieval problem exists — CONTESTED whether hybrid-by-default or
start-narrow-graduate-deliberately is right (§6). Plain relational/KV is the under-discussed pragmatic default:
"often enough until you genuinely need fuzzy recall" once the write/retrieval contract stays small
(agiusalexandre.com; redis.io/blog/long-term-memory-architectures-ai-agents/). Files (2.2) round out a fifth,
auditability-optimized option.

### 2.4 Retrieval from memory
The foundational model is Stanford's 2023 Generative Agents scoring: composite score = weighted **recency**
(exponential decay since last access) + **importance** (LLM-assigned salience) + **relevance** (embedding cosine
similarity) (arXiv 2304.03442), adopted by "virtually every subsequent system" including MemGPT, Mem0, LangGraph.
CONSENSUS as conceptual ancestor; DURABLE as a concept. By 2026, production systems extend this into
**multi-signal hybrid retrieval**: Zep fuses dense + BM25 + graph traversal; Mem0's 2026 default is "single-pass
hierarchical extraction with multi-signal retrieval (semantic, BM25, entity matching)," moving from external
graph-store dependencies toward in-line entity linking (mem0.ai, Jul 2026 — VENDOR). FAST-MOVING implementation
detail; DURABLE takeaway: pure embedding similarity is now considered under-powered alone for memory workloads.
A load-bearing correction from practitioner literature: plain semantic similarity on episodic logs is explicitly
wrong — a session from last week mentioning something in passing will outrank a more relevant one from two weeks
ago, so recency must be a first-class retrieval signal there — strategy must be chosen per memory kind, not
globally. Consolidation-time vs query-time organization is a named architectural fork: heavy write-path LLM
consolidation lowers query latency/cost but risks maintenance cost scaling with total accumulated memory when
consolidation does full-state rewrites rather than incremental updates (arXiv 2605.23986 MemForest;
hindsight.vectorize.io/blog/2026/05/21/agent-memory-consolidation). CONSENSUS the fork exists; CONTESTED which
side to default to (§6).

### 2.5 Consolidation, summarization, forgetting
Consolidation is standardly framed as summarization-plus-deduplication, with raw turn-level history likened to
hippocampal traces and the user-level store to consolidated cortical memory (arXiv 2603.11768; arXiv 2605.08538
"Human-Inspired Memory Architecture"). CONSENSUS framing, DURABLE analogy. **Directly contesting this**: a
controlled ablation, "Verbatim Chunks Beat Extracted Artifacts" (arXiv 2601.00821, v3 dated Jun 15 2026), reports
raw verbatim passages outperforming LLM-extracted/summarized artifacts for long-conversation recall — precise
effect size wasn't extractable from the fetched content, so treat the *direction* as flagged and emerging, not
settled. CONTESTED, single-author, unreplicated; FAST-MOVING, but names a DURABLE risk: extraction discards
detail irrecoverably, an asymmetric downside. Forgetting mechanisms cluster into three types: **time-driven**
(decays over elapsed time; simplest, but eventually drops facts that are old and still true), **frequency-
driven** (retains frequently-retrieved, discards inactive), **importance-driven** (fuses temporal + frequency +
semantic salience); a formal "forgetting-by-design" treatment (FiFA benchmark, bounded budget-aware Priority
Decay) cuts compute cost while preserving coherence and privacy. CONSENSUS taxonomy; DURABLE. TTL is the
simplest-but-crudest policy versus graceful decay-as-accessibility models; an architect must consciously choose
to keep or upgrade from TTL, not omit a lifecycle policy by default. Mem0's ADD/UPDATE/DELETE/NOOP (2.2) is the
clearest concrete memory-update-vs-append pattern found, though contested in production per the GitHub evidence
above.

### 2.6 Multi-agent shared memory
The **blackboard pattern** is specifically revalidated for LLM multi-agent systems: a shared medium where agents
"monitoring the blackboard can independently decide whether they possess the capability, knowledge, or interest
to contribute," shifting from single-coordinator to autonomous participation (arXiv 2510.01285, Oct 2025;
13-57% relative improvement over RAG and master-slave baselines; arXiv 2507.01701, Jul 2025). CONSENSUS the
pattern works for information-discovery-shaped tasks; evidence is benchmark-scale. DURABLE (blackboard
coordination predates LLMs by decades). The field names four multi-agent memory topologies — private-only,
shared-workspace, hybrid, orchestrated (arXiv 2602.06052) — a clean rubric dimension. 2026 work names the
governance gap explicitly: "Governed Shared Memory for Multi-Agent LLM Systems" (arXiv 2606.24535, Jun 2026)
models access as a "time-evolving principal-resource graph" rather than an undifferentiated shared store — shared
memory with no authorization model is now treated as an anti-pattern. CONSENSUS; DURABLE. Handoff is
increasingly protocol-mediated: MCP's 2026 roadmap externalizes memory/state to dedicated resources so facts
persist across sessions and handoffs stay traceable (blog.modelcontextprotocol.io, 2026-07-28 RC post) —
bleeding-edge/in-flux, treat as directional. DURABLE takeaway: handoff is being pulled from ad hoc prompt-stuffing
into an explicit, inspectable contract, independent of which protocol wins.

### 2.7 Privacy/retention
Core unresolved 2026 tension: **GDPR Article 17 erasure vs the EU AI Act's mandatory logging/audit-trail duty
for high-risk systems** (full applicability 2 August 2026 — law.berkeley.edu/research/bclt/bclt-legal-analysis/
eu-ai-act/) — when a user asks for deletion, GDPR compels compliance; months later, an EU AI Act audit for the
same decision may compel production of the very record that was deleted (channel.tel, 2026). CONTESTED/legally
unresolved; DURABLE as a standing constraint. The repeated practitioner mitigation: **tier memory by mutability/
sensitivity** — ephemeral working (run-scoped), episodic (short-horizon summaries), durable semantic (validated
long-term facts with explicit retention) — so different retention rules attach per tier
(atlan.com/know/data-privacy-for-ai-agents/). This is an engineering mitigation, not a legal guarantee — no case
law was found validating it as sufficient. Deletion must reach **derived** memories, not just source rows: teams
need "a data provenance map" linking personal data to every downstream memory store it fed — operationalizing
erasure-vs-derived-memories as **provenance tracking as a prerequisite for erasure**. "Verified forgetting" is
formalized as a named requirement in security literature, distinguishing soft delete (excluded from retrieval,
still indexed) from hard/verified delete (provably purged, including from compressed summaries and propagated
copies — a common residual-leakage vector) (arXiv 2604.16548v2's VMG framework, Jun 2026). CONSENSUS the
distinction matters; FAST-MOVING/immature tooling to prove it. PII handling is recommended as a **pre-write
gate** — redacted at the earliest detectable point so every downstream log/store receives only the redacted
form, inspecting both the assembled prompt and the model response (praesidia.ai, 2026). DURABLE pattern.

### 2.8 The scoping question
Convergent practitioner answer: memory architecture is warranted when an agent (a) runs repeatedly on related
tasks (same domain/user/workflow), (b) must retain human corrections rather than repeat mistakes, (c) tracks
domain rules that evolve, (d) interacts with persistent entities (customers, repos, projects) across calls, or
(e) demonstrably re-pays token cost re-injecting the same context every call. Below that bar: stateless,
single-session tasks with no expected carryover "do not need a memory overlay, as adding one only increases
latency and architectural complexity." CONSENSUS across independent sources; DURABLE. A related, framework-
relevant distinction: **memory, session state, workflow state, and audit records are different architectural
layers** — workflow state (task progress, approvals, retries) belongs outside model context, and session state
is not the source of truth for long-running workflows (aakashx.com/blog/ai-agent-memory-vs-state/, 2026) —
memory means specifically the cross-session, learned/accumulated layer, not a catch-all for anything persisted.
Bigger context windows do **not** eliminate the need for designed memory, but that's no license to skip the
scoping question on genuinely short-horizon agents. Strongest anti-ceremony evidence found: "many teams
overengineer long-term memory for AI agents before they have a real retrieval problem... a local database is
often enough until you genuinely need fuzzy recall" (agiusalexandre.com, May 2026).

### 2.9 Failure modes
**Memory poisoning** is a structurally distinct security surface: unlike prompt injection, whose payload must
land in the active context every time, memory poisoning "requires only one successful write" (arXiv 2604.16548v2).
MINJA (arXiv 2503.03704, Mar 2025) demonstrated query-only injection — no elevated privilege — achieving ~95-98%
success via bridging steps, indication prompts, and progressive shortening. Follow-on 2026 work proposes a
six-class taxonomy across four write channels. CONSENSUS distinct threat class; DURABLE principle (persistence
changes the threat model); FAST-MOVING technique detail. **Staleness/contradiction** as a reasoning failure, not
mere data-quality noise: the STALE benchmark (arXiv 2605.06527, May 7 2026) names "Implicit Conflict" — a later
observation invalidating an earlier memory without explicit negation, requiring inference to detect. CONSENSUS
the failure is real and underhandled; FAST-MOVING/nascent (single benchmark, 400 scenarios). **Unbounded growth
degrades retrieval itself**, not just cost — interference causes recall to worsen with scale even with unlimited
storage; MemGuard's "heterogeneous memory contamination" finding shows functionally distinct memories (stable
facts vs episodic events vs behavioral rules) collapsed into a shared space and retrieved interchangeably,
degrading reliability by up to 28.27% in-paper until type-isolation is enforced at write and retrieval time
(arXiv 2605.28009, UIUC/Columbia/Capital One). CONSENSUS the mode is real; the 28.27% figure is single-paper and
illustrative, not universal. **Context rot** is the failure mode that justifies externalized memory existing at
all: recall accuracy degrades as context length grows across 18 tested models (GPT-4.1, Claude 4, Gemini 2.5
among them), independent of whether the task got harder (redis.io/blog/context-rot/, describing a mid-2025
Chroma study). CONSENSUS, empirically demonstrated; DURABLE mechanism (finite attention budget). **Retrieval
interference** from naive similarity search surfaces semantically-similar-but-wrong memories from different
projects, timeframes, or contexts entirely — the practical motivation for multi-signal retrieval (2.4) and
type-isolation over pure similarity.

## 3. Candidate Decision Rubric

**Gate 0 — Do you need designed memory architecture at all?**
Trigger (need ≥1): repeated same-domain/user tasks; corrections must persist; evolving domain rules to track;
persistent entities spanning calls; demonstrated token-cost of context re-injection; multi-agent handoff needing
shared state; task genuinely exceeds context window. Default absent a trigger: **no** memory architecture —
session/thread state (+ compaction for long single sessions) is correct and simpler; naming "memory" as an ADR
category should itself cite which trigger fired. When-not: single-session stateless tools, low-frequency one-off
agents, short-horizon tasks a larger context window genuinely covers.

**Dimension 1 — Memory kind scoping.** Default: working memory (context window) always, free. Add semantic only
if personalization/domain-fact accumulation matters; episodic only if the agent must recall *specific* past
interactions, not just aggregate facts; procedural only with an actual cross-task learning/improvement loop —
newest and least-proven (Memp, Aug 2025), so reach for it last. When-not: skip procedural without a genuine
learning loop; skip episodic when only current-state facts matter.

**Dimension 2 — Datastore substrate.** Decision inputs: dominant query pattern (fuzzy recall→vector; multi-hop/
temporal reasoning→graph; exact lookups→KV/relational; low-volume/human-auditable→files); team's operational
capacity for a graph DB; latency budget; scale/tenancy. Default: start relational/KV (+ embedding column) or
files; graduate to a dedicated vector store once fuzzy-recall volume demands it; graduate to a temporal knowledge
graph only once multi-hop or contradiction-heavy relational reasoning is *demonstrated*, not hypothetical.
When-not: skip a temporal KG for plain personalization (ontology/cold-start cost unjustified); don't default
straight to hybrid without outgrowing the simpler option — hybrid means operating two systems, a cost to name
explicitly (§6).

**Dimension 3 — Write policy.** Decide: sync/hot-path vs async/background consolidation; verbatim vs
LLM-extracted retention; explicit conflict-resolution semantics (ADD/UPDATE/DELETE/NOOP-equivalent) vs
append-only. Default: async once beyond a demo (protects latency); retain verbatim alongside any extracted
summary where storage allows, given 2026 evidence favoring verbatim and extraction's one-way information loss;
explicit conflict resolution for anything user-correctable. When-not: hot-path sync write is defensible only for
low-volume, latency-tolerant, high-value-per-write agents.

**Dimension 4 — Retrieval policy.** Default: multi-signal (recency + relevance + importance, extended with
keyword/graph-traversal as scale demands), with recency first-class specifically for episodic content (plain
similarity on episodic logs is a named anti-pattern). When-not: below roughly a few hundred stored items, a
scoring formula is unneeded ceremony — recency sort or return-all suffices until the store is big enough for
ranking to matter.

**Dimension 5 — Forgetting/lifecycle.** Decide explicitly: TTL vs decay-based accessibility vs importance/
frequency-driven retention; soft-delete vs hard/verified delete. Default: name at least a TTL as the floor —
unbounded retention is a named failure mode, not a neutral default — and escalate to decay/importance-driven
retention once TTL demonstrably drops still-true facts. When-not: never; some explicit lifecycle policy is
required whenever memory beyond working memory exists.

**Dimension 6 — Multi-agent sharing model** (only if multi-agent). Decide: private-per-agent / shared-workspace
(blackboard) / hybrid / orchestrated, plus independently the authorization boundary (who reads/writes,
principal-scoped retrieval). Default: private-per-agent with a typed handoff contract unless specifically
designed around blackboard coordination — shared mutable memory with no named authorization model is an
anti-pattern at any scale. When-not: single-agent systems skip this dimension entirely.

**Dimension 7 — Privacy/retention constraints.** Decide: tiering by mutability/sensitivity; where PII redaction
happens (pre-write gate, mandatory); whether deletion must be provably verified given regulatory exposure; how
derived memories trace back to source. Default: tier explicitly, redact pre-write, and treat "derived memory
reach" as required whenever user-facing deletion is promised. When-not: a non-personal-data store can skip
GDPR-grade tiering but should say so explicitly rather than omit it silently.

**Dimension 8 — Adversarial/security posture.** Decide: write-authorization (what can trigger a write — user,
tool output, retrieved content, other agents?), provenance (is every entry source-attributable), and whether
high-consequence memories get human-verified freezing before being trusted as precedent. Default: treat any
write path fed by untrusted content as an injection surface requiring code-execution-level scrutiny; name
provenance as a floor. When-not: never optional once persistent memory exists — persistence itself changes the
threat model (§2.9).

## 4. Checkable-Teeth Candidates

Phrased as presence/absence/pairing checks a reviewer or script could apply to an architecture doc, in the spirit
of mechanically-gradeable Verification Contracts:

1. **Trigger justification present** — doc names which Gate-0 trigger fired before introducing a memory ADR.
2. **Per-kind datastore mapping** — an explicit substrate is named per memory kind in use, not one undifferentiated "the database."
3. **Write-path timing named** — sync vs async stated as a labeled decision, not merely implied by a diagram.
4. **Conflict-resolution semantics named** — an ADD/UPDATE/DELETE/NOOP-equivalent defined wherever the memory kind is mutable.
5. **Lifecycle/TTL parameter named** — a concrete retention number or decay rule, not "we'll periodically clean up."
6. **Verbatim-vs-extracted choice stated** — if not retained verbatim, the loss is acknowledged as deliberate.
7. **Deletion paired with derived-memory reach** — any user-facing deletion claim is paired with a statement covering derived artifacts (summaries, indices, profiles).
8. **Sharing model paired with authorization boundary** — if >1 agent touches memory, both the topology and who may read/write are named together.
9. **Write-authorization/provenance named** — what can trigger a write, and whether entries carry source attribution.
10. **Retrieval signals and latency budget named** — component signals stated explicitly whenever ranking is claimed (not just "semantic search"), plus a numeric latency budget for the query-time path.
11. **Negative scope stated** — what will NOT be persisted (mirrors ADR "rejected alternatives"), surfacing over-collection early.

Several are pairing checks (claim X present → claim Y must also be present) rather than pure keyword presence,
keeping them robust against a document that name-drops the right vocabulary without making the actual decision.

## 5. What Changed Since Early 2025

- **Jan 2025** — Zep/Graphiti formalizes bitemporal (event-time vs ingestion-time) knowledge-graph edges for
  agent memory (arXiv 2501.13956) — first widely-cited system treating contradiction handling as non-destructive.
- **Feb–Aug 2025** — A-MEM (Feb, retroactive Zettelkasten linking) and Memp (Aug, procedural memory) extend
  practical taxonomy reach beyond semantic/episodic; procedural memory gains a dedicated methodology, not just a
  taxonomy footnote.
- **Mar 2025** — MINJA shows query-only memory poisoning at ~95-98% success with zero elevated privilege
  (arXiv 2503.03704) — poisoning becomes empirically demonstrated, not hypothetical.
- **Apr–mid 2025** — OpenAI ships the first "dreaming" background memory-curation pass; "context rot" is named
  and shown empirically across 18 models (Chroma study) — the field gains shared vocabulary for why unmanaged
  context degrades regardless of window size.
- **Jun–Aug 2025** — Anthropic ships context-editing beta, then the memory tool GA on the Messages API; Google's
  Vertex AI Memory Bank reaches public preview on an ACL-2025-accepted method — memory becomes a first-class,
  provider-supported primitive rather than something every team hand-rolls.
- **Late 2025 → H1 2026** — center of gravity shifts from capability papers to governance papers: SSGM
  (arXiv 2603.11768), the Always-On Agents survey (arXiv 2606.30306, 435-paper corpus finding the literature
  "concentrates more heavily on accumulating and retrieving state than on governing, recovering, or relinquishing
  it"), the Mnemonic Sovereignty/VMG security survey (arXiv 2604.16548), and MemGuard's contamination finding
  (arXiv 2605.28009) all land within months of each other.
- **Jun 2026** — a controlled ablation (arXiv 2601.00821) contests the extraction/summarization-heavy write
  orthodoxy of 2024-2025, arguing verbatim retention wins; separately, OpenAI's "Dreaming V3" ships as the second
  major consolidation-architecture overhaul in 14 months — the FAST-MOVING implementation layer keeps churning
  even as the DURABLE async-consolidation pattern beneath it has stabilized.
- **Ongoing → Aug 2026** — the EU AI Act's phased applicability turns the GDPR-erasure-vs-audit-trail tension
  from an abstract concern into a live compliance deadline landing inside the current design window.

Net: 2025 was about proving memory architectures work; 2026 so far is about proving they can be governed,
secured, and unwound. A skill written now should weight governance/security/lifecycle at least as heavily as
retrieval cleverness — the opposite emphasis from 2024-era tutorials.

## 6. Contested Points Needing Designer Judgment

1. **Verbatim vs extracted storage as the write-policy default** (§2.5, §5) — a single 2026 ablation contests
   the prior summarization orthodoxy, unreplicated and unreconciled with the storage-cost/retrieval-noise
   reasoning that motivated summarization originally. A durable default here risks encoding an unproven claim.
2. **"Start narrow, graduate to hybrid" vs "hybrid is now baseline"** (§2.3, §2.6) — secondary sources call
   hybrid vector+graph the 2026 enterprise standard; an independent practitioner source calls the landscape
   fragmented/unsolved and warns against pre-emptive complexity. Not reconcilable without knowing a specific
   product's scale; the anti-ceremony goal favors the narrower reading, but that itself is a judgment call.
3. **Fixed multi-signal scoring vs learned/adaptive structure selection** (FluxMem, arXiv 2602.14038, Feb 2026)
   — the learned approach reports real gains but needs ML capacity (offline supervision, a probabilistic gate)
   most application teams won't have; recommending the simple formula vs flagging the learned frontier depends on
   the target team's ML maturity.
4. **GDPR erasure vs EU AI Act audit-trail retention** (§2.7) — a live, structural legal tension with no settled
   resolution found; memory tiering is an engineering mitigation, not a legal guarantee, and needs the adopting
   team's own legal judgment per jurisdiction/risk tier.
5. **Sync/hot-path vs async/background consolidation** (§2.4) — async is clearly dominant among 2025-2026
   provider moves, but freshness-vs-latency has no universal threshold; sources don't converge on when hot-path
   becomes necessary.
6. **Is procedural memory (skill libraries) production-ready to design for now, and how aggressively should
   verified/provable forgetting be pursued vs accepting soft-delete?** (§2.5, §2.7) — both are barely a year old
   with only benchmark-level validation or a dependency-tower proposal (write-authorization → provenance →
   rollbackability → verified-forgetting); recommending either as a standard rubric dimension risks pointing
   teams at unproven patterns or infrastructure investment whose payoff depends on exposure the skill cannot know
   a priori.

## 7. Source Registry

**arXiv (ID — title, date)**: 2602.06052v3 memory-mechanisms survey, 27 institutions (Q4 2025 corpus) · 2304.03442
Park et al. "Generative Agents" (Apr 2023, foundational) · 2501.13956 Rasmussen et al. "Zep" (Jan 20 2025,
VENDOR) · 2502.12110 "A-MEM" (Feb 2025, NeurIPS 2025) · 2503.03704 "MINJA" (Mar 2025) · 2508.06433 "Memp" (Aug 8
2025) · 2512.13564 "Memory in the Age of AI Agents" survey (Dec 2025) · 2512.12818 "Hindsight is 20/20" (Dec
2025) · 2601.00821 Tao An "Verbatim Chunks Beat Extracted Artifacts" (v3, Jun 15 2026) · 2602.14038 "Choosing How
to Remember"/FluxMem (Feb 15 2026) · 2603.07670v1 "Memory for Autonomous LLM Agents" · 2603.11768 "Governing
Evolving Memory... SSGM" · 2604.16548v2 Lin et al., "Mnemonic Sovereignty" (MemTensor/SJTU, Jun 11 2026) ·
2604.20874 Odriozola Schick "Root Theorem of Context Engineering" (Mar 29 2026) · 2605.06527 "STALE" benchmark
(May 7 2026) · 2605.08538v1 "Human-Inspired Memory Architecture" · 2605.23986 "MemForest" · 2605.28009 "MemGuard"
(UIUC/Columbia/Capital One) · 2606.15903 "Control-Plane Placement Shapes Forgetting" (Jun 2026) · 2606.24535
"Governed Shared Memory for Multi-Agent LLM Systems" (Jun 2026) · 2606.30306v1 Ding et al. "Always-On Agents"
survey (Jun 29 2026, 435-paper corpus) · 2510.01285 "LLM-Based Multi-Agent Blackboard System" (Oct 2025) ·
2507.01701v1 "Advanced LLM Multi-Agent Systems... Blackboard" (Jul 2025).

**Official provider/vendor docs**: anthropic.com/engineering/effective-context-engineering-for-ai-agents ·
platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool · platform.claude.com/docs/en/build-with-
claude/context-editing · anthropic.com/news/context-management · code.claude.com/docs/en/memory ·
openai.com/index/chatgpt-memory-dreaming/ (Jun 2026) · openai.com/index/memory-and-new-controls-for-chatgpt/ (Apr
2025) · docs.langchain.com/oss/python/concepts/memory (2026) · langchain.com/blog/langmem-sdk-launch ·
docs.cloud.google.com/gemini-enterprise-agent-platform/scale/memory-bank/setup.

**Vendor blogs** (landscape data, not independent evidence): mem0.ai/blog/state-of-ai-agent-memory-2026 (Jul 16
2026) · mem0.ai/blog/memory-eviction-and-forgetting-in-ai-agents · getzep.com/ai-agents/temporal-knowledge-graph/
· redis.io/blog/long-term-memory-architectures-ai-agents/ · redis.io/blog/context-rot/.

**Independent practitioner/secondary analysis**: agiusalexandre.com/blog/2026-05-16-agent-memory-problem-
landscape-decision-framework/ (May 16 2026) · leoniemonigatti.com/blog/{memgpt,claude-memory-tool}.html ·
hindsight.vectorize.io/blog/2026/05/21/agent-memory-consolidation · atlan.com/know/{types-of-ai-agent-memory,
vector-store-vs-graph-database-agent-memory, agentic-ai-memory-vs-vector-database, data-privacy-for-ai-agents}/
(2026) · github.com/mem0ai/mem0/issues/4896 · github.com/dsh3n77/MINJA ·
praesidia.ai/blog/how-to-redact-pii-from-agent-prompts (2026) · virtualizationreview.com/articles/2025/07/09/
googles-vertex-ai-memory-bank... (Jul 9 2025) · aakashx.com/blog/ai-agent-memory-vs-state/ (2026) ·
medium.com/tech-ai-made-easy Chapter 4 (2026).

**Legal/regulatory**: law.berkeley.edu/research/bclt/bclt-legal-analysis/eu-ai-act/ (2026) ·
channel.tel/blog/gdpr-delete-eu-ai-act-keep-memory-compliance (2026).

≥5 independent organizations represented: arXiv spans UIUC, Stanford, SJTU/MemTensor, Wuhan University,
Columbia, Capital One, Salesforce, Google, and Meta; five providers' own engineering docs; independent
practitioners; legal analysis.
