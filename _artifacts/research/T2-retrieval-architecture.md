# T2 — Retrieval Architecture: Research Brief

Pillar: how a world-class architect designs retrieval/RAG for an LLM app, as of July 2026. Live web
research only (WebSearch/WebFetch), no local repo files read. Many results were SEO-pattern "2026 guide"
blogs recycling the same figures; claims traceable only to that cluster are marked **[SEC]**
(secondary/uncorroborated) and should carry less weight than unmarked claims, which trace to primary
sources (Anthropic, Microsoft Research, Jina AI, arXiv, Pinecone Research, HuggingFace, Cohere docs).

---

## 1. Executive Summary

- **Hybrid retrieval (lexical + dense, RRF-fused) is the uncontested default first stage.** 7–31% NDCG
  lift over single-method is consistent across sources; native support is now table-stakes across every
  major engine. Open question is sparse-method mix (BM25 vs. SPLADE), not hybrid-vs-not. **CONSENSUS / DURABLE.**
- **Chunking follows a default-then-escalate shape.** 400–600 tokens/~15% overlap is the 2026 baseline;
  escalate to structure-aware, then contextual (Anthropic, Sep 2024) or late chunking (Jina AI, Oct 2024)
  only after measuring a gap. Skip chunking entirely for short/structured docs. **CONSENSUS shape / DURABLE.**
- **MTEB/MMTEB are shortlist tools, not decision-grade.** MTEB co-creator Nils Reimers publicly confirmed
  (Dec 2024) leaderboard contamination from training-on-eval-splits. MMTEB (ICLR 2025) widened coverage but
  didn't fix this. Select via your own eval set. **CONSENSUS / DURABLE discipline, FAST-MOVING leaderboard.**
- **Cross-encoder reranking is a measured addition, not a default checkbox.** Reliable 5–15 NDCG@10 gain
  when first-stage retrieval is imprecise; diminishing-to-negative value at small k or on structured
  corpora per 2025–2026 studies. **CONTESTED as a default / DURABLE as a design question.**
- **Late-interaction (ColBERT/ColPali) is real in tooling/research adoption, not yet a production default**
  outside vision-native document retrieval (ColPali), where OCR pipelines lose fidelity. Raw ColBERT's
  ~50–60x storage overhead is the practical blocker. **CONTESTED adoption / DURABLE technique.**
- **GraphRAG earns its cost only for global/sensemaking query workloads at real scale.** Microsoft's own
  LazyGraphRAG (Nov 2024) exists because full upfront extraction (3–5x LLM cost, 60–85% entity accuracy,
  silent hallucinated edges) is often not worth it before query patterns are known. **CONSENSUS on cost /
  CONTESTED on exact scale thresholds. FAST-MOVING.**
- **Agentic retrieval beats single-shot on hard/multi-hop/high-value tasks at a quantified, real cost.**
  Anthropic's multi-agent researcher (Jun 2025): 90.2% quality lift, ~15x token cost. Route by query
  difficulty; don't apply universally. **CONSENSUS / DURABLE.**
- **Long-context is absorbing RAG's easy cases, not replacing it — "context rot" bounds how far.** Chroma
  (2025): 30–50% accuracy drops well before advertised limits; coherent input degrades attention *more*
  than shuffled input. 2026 default is hybrid (bounded retrieval + long-context reasoning over the
  window). **CONSENSUS on hybrid / CONTESTED on numeric crossover (cited multiples span 25x–1250x).**
- **ANN index family and quantization are architect-level; parameter tuning is not.** Family choice
  (HNSW/IVF/DiskANN) sets RAM-vs-SSD shape and write/CRUD posture; `ef_construction`/`nprobe`-style knobs
  are implementation work. **CONSENSUS / DURABLE.**
- **Vector-store selection should separate durable criteria (scale regime, native hybrid, filtering model,
  write pattern, ops posture, cost shape) from fast-moving landscape (which product wins this quarter).**
  pgvector under ~10–50M vectors already in Postgres is a recurring default; self-host-vs-managed crossover
  cited near 60–80M queries/month, but TCO (ops hours) frequently reverses sticker-price conclusions.
  **CONSENSUS on axes / FAST-MOVING on vendor.**

---

## 2. Findings

**F1 — Hybrid search as default first stage.** BM25 (or learned-sparse) run parallel to dense ANN, fused
via RRF, is standard production shape, not an advanced technique (Laforge, glaforge.dev, Feb 2026). RRF is
favored specifically because it's rank-only, sidestepping BM25-vs-cosine score incompatibility. Lift
consistently 7–31% NDCG over single-method [SEC, converges across many 2025–2026 write-ups]. Native
support now ships in Weaviate, Qdrant, Pinecone, Elasticsearch, OpenSearch, Turbopuffer, Vespa. Contested
edge: BM25 remains the safer default sparse leg for exact-match/OOV terms (IDs, codes); SPLADE is an
emerging complement with real latency cost (~100–300ms transformer inference), not yet a replacement.
**CONSENSUS: hybrid > single-method. DURABLE. FAST-MOVING: BM25/SPLADE mix, fusion weighting.**

**F2 — Chunking.** No single best method; a consensus escalation order. Baseline: 400–600 tokens, ~15%
overlap [SEC, converges heavily]. Two techniques address chunk-isolation specifically: **Contextual
Retrieval** (Anthropic, Sep 19 2024) prepends a 50–100 token LLM-generated context summary before
embedding and BM25-indexing — 35% failure-rate reduction alone, 49% combined with contextual BM25, 67%
with reranking added (5.7%→1.9% baseline failure rate); Anthropic's own guidance: skip this entirely under
~200K tokens (~500 pages) and just cache-and-stuff instead. **Late Chunking** (Jina AI, Günther et al.,
arXiv:2409.04701, Sep 2024; blog Oct 6 2024) embeds the full document first with a long-context embedder,
then mean-pools per-chunk after the fact — ~3% average relative gain on BeIR long-document benchmarks,
smaller than Contextual Retrieval's reported lift but far cheaper (no index-time LLM calls). Semantic
chunking (embedding-similarity breakpoints) reports the largest raw lift in some benchmarks but is ~14x
slower to build (0.33 MB/s vs. 4.82 MB/s, Chonkie benchmark). **Skip chunking** for short single-purpose
docs (FAQs, tickets) and structured/tabular data — document-level or direct structured query outperforms
forced chunking (Weaviate, Unstructured.io). **CONSENSUS on escalation order and the don't-chunk rule.
DURABLE. FAST-MOVING: exact lift percentages.**

**F3 — Embedding model selection.** MMTEB (arXiv:2502.13595, ICLR 2025, Feb 2025) expanded MTEB to 500+
tasks/250+ languages with Borda-count aggregation to blunt narrow overfitting — but contamination persists:
Reimers (X, Dec 22 2024) confirmed leaderboard submissions trained on published MTEB splits, calling it "a
big mistake." Raw aggregate scores mislead: high-overall models can trail meaningfully on the retrieval
subtask specifically [SEC]. Convergent practitioner process: shortlist 3–5 via public benchmarks, select
via your own labeled eval set — private-corpus rankings routinely diverge from leaderboard order.
**Matryoshka (MRL)** is now default production practice — most 2026 releases ship MRL-trained; one
benchmark reports 94–98% nDCG@10 retention at 512 dims, >88% at 256 dims [SEC, consistent with the MRL
paper's own claims]; recommended pattern is two-stage (truncated for candidate retrieval, full-size for
reranking). **Fine-tune vs. off-the-shelf** is genuinely contested (see §6) — domain-vocabulary gap favors
fine-tuning (~1–5% gains reported), architectural recency often favors modern generalists over stale
fine-tunes; consensus advice is "benchmark both before committing," not a rule of thumb. Because the
embedding-model landscape is the fastest-moving piece researched, the durable move is designing the index/
interface so the model is **swappable via full reindex** rather than coupled to one vendor's
dimensionality. **CONSENSUS: shortlist-via-benchmark, decide-via-own-eval; MRL mainstream. DURABLE
discipline. FAST-MOVING: current model leaders (landscape names gathered: Voyage-3.5, NV-Embed-v2,
Qwen3-Embedding, text-embedding-3-large, Gemini Embedding, BGE-M3 — re-verify at use time).**

**F4 — Rerankers and late-interaction models.** Standard shape: bi-encoder retrieval (top-50/100) →
cross-encoder rerank → top-5/10 to LLM (Cohere/OpenAI reference patterns), typically +5–15 NDCG@10 (up to
20+ on lexically hard sets) for <200ms. Genuinely contested: 2025–2026 studies find gains shrink or reverse
at small top-k and on structured/low-noise corpora — value concentrates exactly where first-stage
retrieval is imprecise. Current leaderboard snapshot (Agentset, dated Feb 15 2026): Zerank-2 (1638 ELO)
and Cohere Rerank 4 Pro (1629) lead; Cohere Rerank 4 quadrupled context to 32K vs. 3.5 (VentureBeat,
covering Cohere's release). Licensing is architecturally relevant: Cohere/Voyage/BGE-v2-m3 are
commercially licensed; Zerank and Jina Reranker v3 ship CC-BY-NC-4.0, blocking unmodified paid-product use.
**Late-interaction (ColBERT family)**: strong tooling adoption (RAGatouille, PyLate; "millions of HF
downloads" per one retrospective [SEC]) but production-system-of-record adoption lags — raw indexes run
~50–60x larger than source text (170GB for 3GB text [SEC]); PLAID compression and token-pooling
(arXiv:2409.14683; Answer.AI) shrink this substantially but IVF-PQ-style compressed indexes sacrifice
CRUD flexibility (slow inserts, unsupported deletes). **ColPali** (Faysse et al., arXiv:2407.01449, Jun
2024, ICLR 2025) embeds document page *images* directly (SigLIP encoder, MaxSim scoring) instead of
OCR-then-embed — targets visually-dense documents where OCR loses information; a dedicated 2026 workshop
(LIR @ ECIR 2026) signals active research growth, not yet broad production deployment. **CONSENSUS:
rerank is high-value-but-optional, evaluate before adding; late-interaction is specialist (esp. ColPali for
visual docs). DURABLE framing. FAST-MOVING: leaderboard, storage-mitigation state of the art.**

**F5 — GraphRAG and successors.** Original GraphRAG ("From Local to Global," arXiv:2404.16130, Apr 2024)
outperforms plain RAG specifically on **global/sensemaking** questions no single chunk can answer.
Evaluation corpora were narrow (two ~1–1.7M-token English datasets) — widely cited scale thresholds trace
to this single setting, not broad replication. Real, evidenced costs: 3–5x baseline LLM-call cost at index
time [SEC], 60–85% entity-extraction accuracy depending on domain, silent hallucinated entities/
relationships that corrupt the graph without failing loudly, super-linear index growth complicating
incremental updates, and 2–3x query-time latency. **LazyGraphRAG** (Microsoft Research blog, Nov 2024) is
Microsoft's own fix: defers relationship expansion to query time, cutting indexing cost to ~0.1% of full
GraphRAG while matching local-query quality — implicitly admitting the original indexing budget is
impractical for most deployments. Practical implication: **query-type mix, not corpus size alone, gates
value** — only a real share of global/thematic queries justifies graph augmentation, and lazy/query-time
construction should default over full upfront indexing absent volume to amortize it. **CONSENSUS: real
cost, real failure modes, value gated by query type. CONTESTED: specific scale thresholds (single-study
origin). FAST-MOVING: lazy/on-demand variants still evolving.**

**F6 — Agentic retrieval.** Self-RAG (Asai et al., arXiv:2310.11511, Oct 2023) and Corrective RAG/CRAG
(Yan et al., Jan 2024) established self-reflective/corrective retrieval loops pre-2025; two 2025–2026
surveys (arXiv:2501.09136; arXiv:2506.00054, May 2025) now treat agentic patterns as a mainstream category.
Production evidence: Anthropic's multi-agent research system (Jun 13 2025) replaced static top-k
retrieval with dynamic agent-directed search — Opus-4-lead/Sonnet-4-subagent config **outperformed
single-agent Opus 4 by 90.2%** on breadth-first tasks, at ~4x token cost for single agents and ~15x for
multi-agent vs. chat. Anthropic's guidance: justify only when task value clears that cost — heavy
parallelizability, information exceeding one context window, many complex tool calls. Azure AI Search
shipped a first-party "Agentic Retrieval" primitive in 2026, moving the pattern from framework territory
into managed-platform primitives. Cost profile, convergent: 3–10x tokens, 2–5x latency vs. single-shot;
on multi-hop benchmarks the *first* extra retrieval cycle yields most of the gain, later cycles taper or
regress — arguing for a bounded iteration budget. 2026 production pattern: route by query difficulty, fast
path for most traffic, agentic loop reserved for flagged-hard queries; never for latency-sensitive
surfaces. **CONSENSUS: wins on hard/high-value/multi-hop, loses on cost grounds for routine queries.
DURABLE (quantified costs come from primary vendor data).**

**F7 — Long-context vs. RAG economics.** Cost estimates converge directionally, not numerically — genuinely
contested. Cited framings span a 125x per-query multiple (500K-token-stuffed vs. ~4K retrieved) [SEC] to a
research-paper-derived ~$0.118/query (long-context) vs. ~$0.0045/query (RAG), over an order of magnitude.
Prompt caching narrows but doesn't close the gap — roughly 5–10x reduction in the best case (every query
hits the same cached prefix), rarely achieved in production traffic; multi-million-token windows with heavy
caching can become competitive specifically for repeated queries over the same stable document set, a
narrower case than "long context replaces RAG." Independent of cost: **Chroma's "context rot" study
(2025)** tested 18 frontier models (GPT-4.1, Claude 4, Gemini 2.5, Qwen3) and found non-uniform accuracy
degradation — sometimes 30–50% before the documented limit — from lost-in-the-middle effects, attention
dilution, and distractor interference; counterintuitively, coherent structured input degrades attention
*more* than shuffled input. This is primary research, not a vendor cost argument, and is the strongest
evidence against naive context-stuffing. Synthesized crossover: retrieval wins at large/growing corpora,
frequent freshness (daily+), or high query volume; long-context (cached) suits smaller/static corpora with
cross-a-few-documents reasoning, or where pipeline simplicity outweighs cost premium at the given volume.
2026 default is explicitly **hybrid**: retrieve a bounded window (tens of thousands of tokens), then
long-context-reason over it. **CONSENSUS: hybrid-over-pure-either; context rot is real and cost-independent.
CONTESTED: exact numeric crossover (25x–1250x spread across sources). DURABLE: the hybrid principle.
FAST-MOVING: context-window sizes and cache pricing, both still moving in 2026.**

**F8 — ANN index choice.** Three families: **HNSW** (in-memory graph, 95%+ recall out-of-the-box, absorbs
streaming inserts, 2–5x more memory than IVF); **IVF** (k-means/Voronoi partitions, faster build/lower
memory, recall drifts without periodic retraining); **DiskANN** (Subramanya et al., Microsoft Research,
NeurIPS 2019 — 5,000 QPS at 95%+ recall@1, sub-5ms latency, billion-point SIFT dataset, 64GB RAM + SSD via
the Vamana graph algorithm), positioned for billion-scale or high-mutation, cost-constrained workloads.
Quantization is now a standard companion decision: scalar, product (PQ — also underlies ColBERT's PLAID),
and binary quantization trade recall for memory; DiskANN's built-in Statistical Binary Quantization reaches
21MB where HNSW-on-half-precision costs 193MB for an equivalent workload [SEC, order-of-magnitude matches
DiskANN's published design goals]. Newer schemes (e.g., RaBitQ, pairing IVF with randomized binary
quantization) chase HNSW-like recall at IVF-like memory cost — the quantization sub-choice hasn't
converged on one winner. **Architect-level vs. tuning-level, explicitly**: index *family* is architect-level
— it sets RAM-vs-SSD infrastructure shape and write/CRUD posture, which must match the corpus's actual
freshness requirement. Parameters within a family (`M`/`ef_construction`/`ef_search`, `nlist`/`nprobe`, PQ
subvector count) are implementation/tuning, resolved empirically against a recall/latency target. Whether
to quantize at all, and how much, is architect-level when it determines memory-budget feasibility or the
need for a rerank-after-quantization compensating pass (binary quantization is lossy enough that
exact-score reranking of the top-N is a common pairing). **Metadata-filtered ANN** is a related
architect-level call: pre-filtering guarantees correctness but can be slow when unselective or
poorly-indexed; post-filtering is fast but silently loses recall when matches are sparse (documented
pgvector failure mode, DEV/MongoDB engineering). 2025–2026 engines increasingly ship integrated filtering
(Qdrant's filterable HNSW, Weaviate's ACORN, Pinecone's serverless filtering research) avoiding the pure
dichotomy — declare this upfront whenever filters (tenancy, ACL, date range) are near-universal in the
query mix, since it changes required engine capability, not just a query-time knob. **CONSENSUS on
family-vs-tuning split and quantization's architectural relevance. DURABLE. FAST-MOVING: which
quantization scheme currently wins the recall/memory Pareto frontier.**

**F9 — Vector-store selection: durable criteria vs. landscape.** Durable criteria converged on across
sources: (1) scale regime (vector count + growth) vs. RAM/tier budget; (2) native hybrid support, now
near-baseline (F1); (3) filtering model — pre/post-filter behavior and selectivity (F8); (4) write/update
pattern matched to index family; (5) operational posture the team can actually staff — self-hosted becomes
cost-favorable somewhere near 60–80M queries/month [SEC, several independent pricing analyses converge
without public methodology], but total cost of ownership (engineering time) frequently reverses sticker-
price conclusions [SEC: one cited case, a nominally cheaper option cost 15x more once ops time was priced
in]; (6) data locality/coupling — keeping vectors in an existing Postgres (pgvector/pgvectorscale) trades a
dedicated engine's ceiling for fewer moving parts and SQL-joinable metadata, a recurring default under
~10–50M vectors already in Postgres; (7) cost shape (storage/query/egress/rebuild), not sticker price —
2025–2026 saw Pinecone and Weaviate both introduce pricing floors, reshaping small-workload economics.
**Landscape (fast-moving, re-verify at use time):** Qdrant/Weaviate for filtering+hybrid+self-host-
friendliness; Milvus for billion-vector extreme scale with heavier ops weight; Pinecone for fully-managed
billion-scale, minimal ops team; Turbopuffer in vendor-adjacent migration claims (Notion, Cursor — [SEC],
unverified independently); Vespa for extreme scale (Vinted's ~1B-item migration off Elasticsearch) with an
8.5x–12.9x per-core throughput claim [SEC, not independently reproduced]; Elasticsearch/OpenSearch remain
dominant where the stack already exists. **CONSENSUS on the seven durable axes. FAST-MOVING and
vendor-interested: every specific comparison number.**

**F10 — Retrieval evaluation as a design-time artifact.** Consensus across eval tooling (RAGAS, ARES,
TruLens, DeepEval, Braintrust) and engineering write-ups: declare a **golden query set** upfront — even
20–50 hand-labeled queries with *graded* (not binary) relevance is repeatedly described as sufficient to
start and materially better than nothing. Core metrics: recall@k, nDCG@k (log-discounted by rank position),
MRR, precision@k; align the metric's k with the k actually sent to the generator (e.g., report nDCG@5 if
only top-5 chunks reach the LLM, recall@100 as a secondary depth check). RAGAS (reference-free:
faithfulness, answer relevancy, context precision/recall) is the common CI-friendly choice; ARES adds a
calibrated LLM-judge layer suited to production drift monitoring; a common pairing is RAGAS-in-CI +
ARES-style judging in production. Cadence: capture a baseline before any chunking/embedding/retrieval-stack
change; gate PRs touching retrieval on regression thresholds; feed production failures back into the golden
set — evaluation as continuous pipeline, not pre-launch checklist. **CONSENSUS: declare golden set + floor
metric before building, tie k to generator's k, re-run on every retrieval-affecting change. DURABLE
discipline. FAST-MOVING: which specific tool wins (this tooling sub-field churns quickly).**

---

## 3. Candidate Decision Rubric — Staged Decision Tree

```
STAGE 0 — Do you need retrieval at all?
├─ Answerable from parametric knowledge (no private/current data)? → NO RETRIEVAL.
├─ Corpus fits comfortably in context (anchor: ~200K tokens / few hundred pages, per Anthropic's own
│  contextual-retrieval guidance) AND fairly static AND low query volume? → CONTEXT-STUFF + CACHING.
└─ Otherwise → Stage 1. Revisit Stage 0 if corpus grows past the fits-threshold, freshness tightens to
   daily+, or query volume grows enough that even cached long-context cost exceeds retrieval cost
   (compute actual $/query — the multiplier moves, don't hardcode one).

STAGE 1 — Simplest retrieval that could work
├─ Structured/tabular/key-value data? → STRUCTURED QUERY (SQL/lookup). No embeddings.
├─ Short single-purpose docs (FAQs, tickets, cards)? → DOCUMENT-LEVEL retrieval, no chunking.
├─ Small corpus (anchor: <1–5M vectors) already in an operational DB? → pgvector + BM25/full-text.
│  No dedicated vector engine yet.
└─ Otherwise → Stage 2.

STAGE 2 — Hybrid retrieval (default first stage beyond Stage 1)
├─ ALWAYS: lexical (BM25, ± learned-sparse) + dense, fused via RRF.
├─ Chunking default: 400–600 tokens, ~15% overlap, structure-aware where source has reliable structure.
│  Escalate to semantic/late/contextual chunking only after MEASURING a gap against the golden set (6)
│  that simpler chunking can't close.
├─ Embedding: generalist off-the-shelf, shortlisted via public benchmark, SELECTED via own eval set.
│  Prefer MRL-capable models. Treat as swappable — design the reindex path, don't hardwire dimensionality.
└─ Escalate to 3+ only if golden-set metrics stay below floor after tuned hybrid + chunking.

STAGE 3 — Reranking (add when measured, not by default)
├─ Add when: downstream precision matters, first-stage is measurably imprecise on the golden set, or
│  query mix is heterogeneous.
├─ Skip when: small+structured corpus, top-k already small/precise, or latency can't absorb ~100–200ms.
└─ Declare an explicit latency budget if added.

STAGE 4 — Agentic retrieval (decomposition, self-correction, retrieval-as-tool)
├─ Add when: queries are demonstrably multi-hop, task value clears ~3–10x token / 2–5x latency cost, or
│  the failure mode is "retrieved the wrong thing" not "ranked it lower."
├─ Bound it: cap iteration count (first extra cycle gives most of the gain); route by a cheap difficulty
│  classifier rather than running every query through an agent loop.
└─ Never the default path for latency-sensitive, low-stakes, or high-volume traffic.

STAGE 5 — Knowledge-graph augmentation (GraphRAG / successors)
├─ Add ONLY when a real share of the query workload is global/thematic/sensemaking (hybrid+rerank already
│  covers fact lookup) AND scale justifies extraction cost (directional anchor: ~1M+ tokens / ~1K+ docs —
│  re-derive from your own cost math, don't cite as a hard cutoff).
├─ Default to LAZY/query-time graph construction over full upfront indexing unless query volume amortizes
│  the 3–5x upfront cost.
├─ Budget for real failure modes: 60–85% entity-extraction accuracy, silent hallucinated edges, weeks of
│  domain tuning — not a weekend integration.
└─ Never "because it sounds sophisticated" — must trace to a stated global-query-share in the doc.

STAGE 6 — Evaluation (declare BEFORE Stage 2, not after Stage 5)
├─ Golden query set: ≥20–50 hand-labeled queries, GRADED relevance, versioned alongside the doc.
├─ Floor metric tied to the generator's actual k (e.g., nDCG@5), plus recall@100 depth check.
├─ Re-run trigger list: embedding swap, chunking change, reranker change, index/quantization change,
│  corpus schema change.
└─ Production feedback loop: retrieval failures become new golden-set cases.
```

**Stated plainly:** Stage 2 (hybrid + measured chunking + swappable off-the-shelf embedding) is the center
of gravity for most RAG systems. Stages 3–5 are escalations, each requiring a measured-gap or stated-share
justification — the research consistently shows real costs and real null/negative scenarios for reranking,
agentic loops, and graph augmentation alike.

---

## 4. Checkable-Teeth Candidates

1. **Golden query set reference**: named file + minimum count (≥20) + graded (not binary) relevance —
   grep-checkable existence/count.
2. **Floor metric + threshold declared numerically** (e.g., "nDCG@5 ≥ 0.75"), not a vague quality statement.
3. **k-consistency**: the declared retrieval metric's k must match the k actually sent to the generator
   elsewhere in the spec — cross-reference defect if they diverge (e.g., nDCG@5 declared, top-20 sent).
4. **Chunking parameters declared, not TBD**: strategy + size + overlap, or an explicit no-chunking
   rationale (short-doc/structured-data).
5. **Embedding model + dimension + MRL-truncation status + named reindex trigger** (trigger's presence is
   itself checkable).
6. **First-stage composition named**: single-method or hybrid; if hybrid, the fusion method (RRF or other)
   must be named — "hybrid" with no named fusion method is a defect.
7. **Reranking stage present/absent + model class + latency budget**, with a traceable measured-gap
   justification if present.
8. **Index family + quantization + CRUD posture, cross-checked against stated freshness**: e.g.,
   "updated hourly" paired with a batch-rebuild-only index family is a flaggable contradiction.
9. **Metadata filter strategy declared whenever the schema implies near-universal selective filters**
   (tenant ID, ACL, date range) — absence when such a column exists is flaggable.
10. **Vector-store choice with a rationale sentence referencing ≥1 durable criterion** (scale/hybrid/
    filtering/write-pattern/ops-posture) — a bare product name with no rationale is a gap regardless of
    whether the product itself is defensible.
11. **Escalation justification ("why not simpler")**: reranking, agentic retrieval, or graph augmentation
    each require a nearby causal justification (measured gap / stated query-share), checkable via proximity
    of a causal connective to the escalation's introduction.
12. **Agentic-retrieval cost budget** (max iteration count + routing rule) and **graph-augmentation
    query-share + lazy-vs-upfront choice with reason**, required if Stage 4 / Stage 5 are used respectively.
13. **Long-context-vs-retrieval threshold stated numerically** (corpus tokens, growth rate, freshness
    cadence), enabling a later drift check in the same spirit as REQ-drift detection elsewhere, plus a
    **non-empty re-evaluation trigger list** rather than a general "we'll re-evaluate as needed."

Items 3, 8, 11, and 13 are the highest-value candidates — cross-consistency checks (comparing two
declarations, or a declaration against reality over time) rather than mere presence checks, matching the
kind of teeth this framework's Verification Contracts already favor elsewhere.

---

## 5. What Changed Since Early 2025

- **Contextual Retrieval and Late Chunking (both Sep/Oct 2024)** landed just before the cutoff but only
  became widely cited/replicated *during* 2025–2026 — now standard citations rather than novel research.
- **LazyGraphRAG (Nov 2024)** shifted the GraphRAG cost conversation from "prohibitive upfront investment"
  to "defer extraction to query time," lowering the bar for trying graph augmentation at all.
- **MTEB's contamination problem became publicly acknowledged** (Reimers, Dec 2024); MMTEB (Feb 2025)
  widened coverage but didn't fix it — 2026 guidance hardened toward "never trust the leaderboard directly,"
  more skeptical than typical 2024 "pick the top MTEB model" advice.
- **Matryoshka embeddings went from training trick to default expectation**; two-stage truncated-then-full
  retrieval is now a named production pattern.
- **Agentic retrieval crossed from research to shipped production architecture**: Self-RAG (2023)/CRAG
  (Jan 2024) were pre-2025 research; Anthropic's production multi-agent researcher (Jun 2025) and Azure AI
  Search's first-party "Agentic Retrieval" (2026) mark the move into managed-platform primitives with
  quantified cost/benefit numbers.
- **Context windows widened materially (1M–10M tokens discussed by 2026)**, reopening "does RAG still
  matter" — but Chroma's "context rot" research (2025) landed in the same window and is the primary reason
  2026 consensus settled on hybrid retrieve-then-long-context-reason rather than "long context replaces RAG."
- **The reranker market got more competitive and long-context-capable**: Cohere Rerank 4 (32K context) plus
  new entrants (Zerank-2, Voyage Rerank-2.5) displaced the more Cohere-v3-centric 2024 default assumption.
- **Native hybrid search became table-stakes** — a 2024 differentiator, a 2026 baseline whose *absence*
  would now be the notable fact.
- **Vector-database pricing models shifted**: Pinecone and Weaviate both introduced pricing floors in the
  2025–2026 window, strengthening the case for pgvector-in-existing-Postgres at the low end.
- **ColPali (2024, ICLR 2025) established vision-native document retrieval** as a credible alternative to
  OCR-then-embed, with a dedicated 2026 workshop (LIR @ ECIR 2026) — barely existed in practitioner
  conversation before mid-2024.

---

## 6. Contested Points Needing Designer Judgment

1. **Reranking: default or optimization?** Evidence supports both "always add it" and "limited-to-negative
   at small k/structured data" camps. No source resolves this — encode the measurement-gated framing
   (Stage 3), not a side.
2. **Fine-tune vs. off-the-shelf embeddings** has no clean rule; domain-vocabulary-gap and architectural-
   recency arguments pull opposite ways. Sources recommend "benchmark both," which is a policy, not a
   pre-computable decision.
3. **GraphRAG scale thresholds trace to one research setting** (Microsoft's own 1–1.7M-token corpora), not
   independent replication at multiple scales — treat any specific number as a hypothesis to validate, not
   a citable constant.
4. **Long-context-vs-RAG crossover numbers vary up to ~50x across sources** depending on caching-hit-rate
   and volume assumptions. Direction is solid; the exact threshold needs a live cost calculator against
   current pricing at use time, not a baked-in constant.
5. **How much late-interaction "adoption" is production vs. tooling experimentation is unclear** — download/
   integration counts show developer interest, not confirmed system-of-record share. Treat ColBERT/ColPali
   as worth-knowing, not assumed-default, pending better production evidence.
6. **"Vectorless"/agent-as-retriever framing vs. mainstream agentic-RAG-still-uses-an-index framing** are in
   real tension. Don't assume vector infrastructure disappears just because retrieval becomes agent-directed
   — Anthropic's own write-up treats agentic orchestration as compatible with, not a replacement for, an
   underlying index.
7. **SPLADE's real production share vs. BM25 is unsettled** — "emerging complement" in most sources, but
   real latency cost keeps BM25 the safer default sparse leg. Flag as an upgrade path, not a default.
8. **The ~60–80M-queries/month self-host-vs-managed crossover** appears in several independent write-ups
   with no disclosed methodology — a rough anchor for a user conversation, not a hard gate.

---

## 7. Source Registry

**Primary (vendor engineering blogs, research labs, arXiv/peer-reviewed papers, official docs):**
- Anthropic, "Contextual Retrieval" — anthropic.com/news/contextual-retrieval — Sep 19, 2024
- Anthropic, "How we built our multi-agent research system" — anthropic.com/engineering/multi-agent-research-system — Jun 13, 2025
- Microsoft Research, "LazyGraphRAG" — microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/ — Nov 2024
- Microsoft Research, "GraphRAG: Improving global search via dynamic community selection" — microsoft.com/en-us/research/blog/
- "From Local to Global: A Graph RAG Approach..." — arXiv:2404.16130 — Apr 2024
- Jina AI, "Late Chunking in Long-Context Embedding Models" — jina.ai/news/late-chunking-in-long-context-embedding-models/ — Oct 6, 2024
- "Late Chunking: Contextual Chunk Embeddings..." — arXiv:2409.04701 — Sep 2024 (rev. Jul 2025)
- "MMTEB: Massive Multilingual Text Embedding Benchmark" — arXiv:2502.13595 — ICLR 2025, Feb 2025
- Nils Reimers, X post on MTEB contamination — x.com/Nils_Reimers/status/1870812625505849849 — Dec 22, 2024
- "ColPali: Efficient Document Retrieval with Vision Language Models" — arXiv:2407.01449 — Jun 2024, ICLR 2025
- "Self-RAG" — arXiv:2310.11511 — Oct 2023
- DiskANN, Subramanya et al., Microsoft Research — NeurIPS 2019 — microsoft.com/en-us/research/publication/diskann-fast-accurate-billion-point-nearest-neighbor-search-on-a-single-node/
- Chroma Research, "Context Rot" — trychroma.com/research/context-rot — 2025
- Pinecone Research, "Accurate and Efficient Metadata Filtering..." — pinecone.io/research/
- Pinecone, "Cascading retrieval with multi-vector representations" — pinecone.io/blog/
- HuggingFace, "Introduction to Matryoshka Embedding Models" — huggingface.co/blog/matryoshka
- Answer.AI, "A little pooling goes a long way for multi-vector representations" — answer.ai/posts/colbert-pooling.html
- "Reducing the Footprint of Multi-Vector Retrieval... Token Pooling" — arXiv:2409.14683
- "RAG: A Comprehensive Survey of Architectures, Enhancements, and Robustness Frontiers" — arXiv:2506.00054 — May 2025
- "Agentic Retrieval-Augmented Generation: A Survey" — arXiv:2501.09136
- Cohere, Rerank documentation — docs.cohere.com/docs/rerank
- VentureBeat, "Cohere's Rerank 4 quadruples the context window..." — venturebeat.com/orchestration/
- Microsoft Learn, "Agentic Retrieval Overview - Azure AI Search" — learn.microsoft.com/en-us/azure/search/

**Secondary/landscape (practitioner and vendor-comparison blogs; used only for directional consensus,
flagged [SEC] inline wherever a specific figure depends on them):** Guillaume Laforge (glaforge.dev, Feb
2026); DEV Community/MongoDB engineering on pgvector pre-filtering; Agentset reranker leaderboard (snapshot
Feb 15, 2026); and a cluster of "2026 guide" vendor-comparison posts (digitalapplied.com, denser.ai,
futureagi.com, atlan.com, firecrawl.dev, zeroentropy.dev, kalviumlabs.ai, ranksquire.com, byteiota.com and
similar) trusted only for *direction*, never for precise percentages or vendor rankings, which churn
quickly and were frequently uncorroborated by any primary source. **Excluded from evidentiary weight:**
single-blog vendor-migration cost-savings percentages (Notion/Turbopuffer, Cursor/Turbopuffer,
Vespa-vs-Elasticsearch throughput) — named for landscape awareness only, not to be encoded as fact.
