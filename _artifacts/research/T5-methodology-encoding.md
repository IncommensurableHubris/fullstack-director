# T5 — How Gold-Standard Methodology Sources Encode Data/AI Architecture Craft

Research pillar: the FORM of world-class RAG / LLM-app / agentic-system guidance, for designing a new
data-architecture craft module in Fullstack Director. Live web research conducted July 2026.

---

## 1. Executive Summary

- Cloud architecture centers (Azure, AWS) converge on one FORM for datastore/retrieval guidance: **decision-factor
  lists ("if you need X, choose Y") + capability comparison tables + flowcharts** — not prose. Google Cloud is the
  outlier: catalog-style, no comparison criteria. (F1, F2 — CONSENSUS; DURABLE as form, FAST-MOVING as content.)
- AWS's new **Agentic AI Lens** (June 10, 2026) is the closest external analog to Fullstack Director's own
  discipline: **ID-coded best practices** (`AGENTOPS01`, `AGENTREL02`…) navigated via **staged reading paths**
  ("Building your first agent" → "Moving to production" → "Scaling to multi-agent" → "Hardening an existing
  deployment") over one fixed catalog. (F3 — structure DURABLE, generalizability CONTESTED.)
- Frontier labs do not publish architecture-center-style decision guidance. Anthropic gives narrative essays with
  embedded criteria plus separate empirical technique reports; OpenAI gives cookbooks plus one business-audience
  agent-building PDF. (F4 — CONSENSUS, DURABLE gap.)
- The dominant staleness-resistance technique is **encoding criteria, not winners** — "if you need sub-10ms
  latency, choose X" outlives "use Pinecone." No source formally instructs readers to consult a live leaderboard;
  that indirection is informal practitioner culture, not encoded methodology. (F9, F15 — CONSENSUS / confirmed gap.)
- Thoughtworks Radar Vol. 34 (April 2026) names the staleness problem outright — **"retaining principles,
  relinquishing patterns"**: as AI accelerates change, teams fall back to durable fundamentals (XP, DORA, zero
  trust, testability) over named tools. Direct, dated, primary evidence for tiered guidance. (F6 — CONSENSUS, DURABLE.)
- "Naive → Advanced → Modular" RAG is a real academic taxonomy, but vendors present RAG guidance as a **phased
  design process**, not an escalation ladder. The one numeric "maturity model" found is a single uncorroborated
  consultancy framework. (F8 — CONTESTED at the operational-ladder level.)
- Classic MADR has no AI-specific fields. Practitioner extensions (revisit trigger, model-version pinning,
  benchmark-backed alternatives) are emerging in 2026 blogs but unabsorbed by canonical ADR sources — genuinely
  open territory. (F7 — CONTESTED/emergent, FAST-MOVING.)
- The most durable "checkable teeth" lineage predates the LLM boom: **Model Cards (2019) → Datasheets for Datasets
  → System Cards (OpenAI/Anthropic, ongoing)**. All demand specific, falsifiable fields — named benchmark + score +
  date + method — not narrative assertion. (F10 — CONSENSUS, DURABLE.)
- The applied-evals community (Hamel Husain/Shreya Shankar) and OWASP's own LLM Top 10 independently converge on
  the same principle from opposite domains: a rubric/checklist is only real when backed by **evidence of actually
  looking** (read real failure cases; actively tested, not theoretically addressed) — not box-ticking. (F11, F12 —
  CONSENSUS, DURABLE.)
- Staleness handling can live in publishing infrastructure, not just content: Azure docs carry machine-readable
  `ms.update-cycle: 180-days` metadata forcing periodic freshness review. (F13 — DURABLE technique, portable
  regardless of AI-specific content.)

---

## 2. Findings

Each tagged **[Consensus/Contested] [Durable/Fast-moving]**.

### F1 — Decision-factor-list + comparison-table dominates datastore/retrieval-choice guidance
**[CONSENSUS] [DURABLE form / FAST-MOVING content]**

Azure and AWS independently converge on: a list of "If you need **[requirement]**, choose **[service]**"
statements plus a capability matrix. AWS: *"If you need ultra-low latency for real-time applications – Choose
Amazon MemoryDB… If you need to store billions of vectors cost-effectively – Choose Amazon S3 Vectors"*
(AWS Prescriptive Guidance, "Choosing an AWS vector database for RAG use cases," 2026). Azure pairs a flowchart
("begins by determining if vectors change frequently") with a seven-service matrix covering dimension limits,
indexing algorithms (DiskANN/HNSW/IVFFlat), and hybrid-search support (Azure Architecture Center, vector-search
guide, 2025-10-20, updated 2026-05-02). The criteria-branch → named-option *structure* is durable; the service
names in each leaf (S3 Vectors shipped only late 2025) are fast-moving.

### F2 — Google Cloud is comparatively weak: a catalog, not a chooser
**[CONSENSUS] [DURABLE finding about current GCP posture]**

Google's RAG reference-architecture index (last reviewed 2025-09-22) lists six architectures with purely
descriptive blurbs and **no comparison table, no decision tree, no "choose X when Y" language** — confirmed by
direct fetch. The Well-Architected AI/ML perspective (last updated 2024-10-11) is principles-level and defers to
that same criteria-free catalog for anything retrieval-specific. A real, current gap versus Azure/AWS.

### F3 — AWS Agentic AI Lens: ID-coded practices + staged reading paths
**[CONSENSUS on shape / CONTESTED generalizability] [structure DURABLE, content FAST-MOVING]**

Published 2026-06-10, this lens organizes 40+ best practices under IDs (`AGENTOPS01`, `AGENTREL02-BP05`,
`AGENTSEC04`, `AGENTCOST02`), pillar-tagged and cross-referenced, plus a **"Lens roadmap"**: four reading paths
keyed to maturity stage — *Building your first agent* (scope, security boundaries, predictable behavior) →
*Moving to production* (observability, eval, cost controls) → *Scaling to multi-agent systems* (orchestration,
coordination security) → *Hardening an existing deployment* (guardrails, human oversight, legacy integration).
One artifact serves both "what are all the practices" and "what do I read first." It also names why agentic
systems need new primitives: *"Agents reason, not only respond… act autonomously… behavior is stochastic…
collaborate… remember."*

### F4 — Frontier labs publish narrative essays and empirical technique reports, not architecture-center guidance
**[CONSENSUS] [DURABLE gap]**

Anthropic's "Building Effective AI Agents" (essay, Dec 2024) gives a qualitative rule, not a decision tree:
*"Agents can be used for open-ended problems where it's difficult or impossible to predict the required number of
steps… Workflows offer predictability and consistency for well-defined tasks."* Operational guidance instead ships
as separate technique posts with their own evidence: "Contextual Retrieval" (2024-09-19) reports specific deltas
(35%/49%/67% reduction in failed retrievals across configurations) and cost (~$1.02/million document tokens with
caching); "Effective Context Engineering for AI Agents" (2025-09-29) offers a durable principle — *"find the
smallest set of high-signal tokens that maximize the likelihood of your desired outcome"* — without an algorithmic
procedure. OpenAI's "A Practical Guide to Building Agents" (PDF, 2025) is program-management-flavored (use-case
selection, a three-way tool taxonomy), closer to that than an architecture guide, backed by ordinary API cookbook
docs. Neither lab publishes anything resembling Azure's phased series or AWS's lenses.

### F5 — Durable pattern *axes* survive; the tool references inside pattern catalogs rot
**[CONSENSUS] [MIXED — structure DURABLE, examples FAST-MOVING]**

Eugene Yan's "Patterns for Building LLM-based Systems & Products" (~2023) organizes seven patterns (Evals, RAG,
Fine-tuning, Caching, Guardrails, Defensive UX, Feedback collection) on two durable axes — infra-to-UX,
defensive-to-offensive — with a trigger/constraint pair per pattern; still sound methodology in 2026. a16z's
"Emerging Architectures for LLM Applications" (2023-06-20, never updated since, confirmed by direct fetch) is the
cautionary case: it self-flags fragility — *"This stack is still very early and may change substantially"* — and
contains a claim now flatly falsified: *"agents don't really work yet… most agent frameworks today are in the
proof-of-concept phase."* The stack-diagram shape survives; the named vendors are a dated snapshot.

### F6 — "Retaining principles, relinquishing patterns" — Thoughtworks names the staleness problem explicitly
**[CONSENSUS] [DURABLE]**

Radar Vol. 34 (2026-04-15) frames a headline theme exactly this way: as AI accelerates change, teams return to
durable fundamentals (XP principles, DORA metrics, zero-trust, testability) rather than chasing named tools. A
second theme, *"the challenge of evaluating technology in an agentic world,"* admits even the Radar's own
Adopt/Trial/Assess/Hold methodology strains against agentic pace. RAG's own ring history — Trial (Sep 2023) →
Adopt (Apr 2024) → confirmed Adopt (Oct 2024) — shows the Radar treating core retrieval as *settled infrastructure*
by late 2024, with the guidance frontier since moved to context engineering, agent evaluation, and permissioning.

### F7 — ADR practice for AI systems is real but unsettled; canonical sources haven't caught up
**[CONTESTED/emergent] [FAST-MOVING]**

martinfowler.com/bliki/ArchitectureDecisionRecord.html (updated 2026-03-24) and adr.github.io describe **no
AI-specific fields**. Fowler: *"once an ADR is accepted, it should never be reopened or changed — instead it
should be superseded,"* plus a generic recommendation to record *"changes in the product context that should
trigger the team to reevaluate the decision."* AI-specific practice is being grafted onto that generic hook only
in secondary sources so far — e.g. a practitioner template (institutepm.com, 2026-05-23, not a standards body)
adds a **Review Trigger** field, forces specificity (*"not 'we chose RAG' but 'we chose retrieval-augmented
generation using OpenAI text-embedding-3-large…'"*), benchmark evidence in Alternatives Considered, and *"never
delete ADRs."* Common triggers: cost threshold exceeded, provider deprecation, new capability release, quality
metric below threshold, team-expertise change. By contrast, catio.tech's 2026 ADR guide covers Nygard/MADR/
Y-statements with **no** AI-specific section — evidence this is emergent, not mainstream.

### F8 — Staged retrieval framing is real at the technique level, not yet consensus as an operational maturity ladder
**[CONTESTED] [MIXED]**

Naive → Advanced → Modular RAG is a genuine academic taxonomy (arXiv 2312.10997, Dec 2023; agentic-RAG survey
arXiv 2501.09136, Jan 2025) describing capability escalation — but this is a taxonomy of what exists, not a
prescriptive ladder. Vendors don't repackage it that way: Azure's RAG series is a **phased design process**
(preparation → chunking → enrichment → embedding → retrieval → evaluation), gated per-phase, not tiered by
capability. The one explicit numeric maturity model found (ombrulla.com, six stages RMM-0…RMM-5 with quantified
exit criteria like "nDCG@10 +10% uplift") is a **single consultancy's proprietary framework**, well-constructed
but uncorroborated, with later stages reading as aspirational. Treat "start naive, escalate on measured need" as
a sound heuristic consistent with Azure's own framing (*"If your queries are straightforward enough that a single
search against a single index can resolve them, standard RAG is the better fit… Use agentic RAG when the
reasoning and flexibility justify these costs,"* 2026-06-23) — but no specific numeric ladder is consensus.

### F9 — "Criteria, not winners" is the load-bearing staleness-resistance technique
**[CONSENSUS] [DURABLE]**

The most consistent pattern found. AWS: *"If you need MongoDB-compatible document database with vector search –
Choose Amazon DocumentDB… If you need graph-based knowledge representations with vector search – Choose Amazon
Neptune Analytics."* Azure chooses between a traditional DB and AI Search based on *"whether you can perform live
or real-time vector searching,"* never by naming a "best" product. Eugene Yan's table keys each pattern to a
trigger/constraint pair, not a tool name. Mechanism: requirements (latency budget, update frequency, cost
sensitivity, need for hybrid/graph search, existing skills) change far more slowly than which product currently
best satisfies them.

### F10 — Model Cards → Datasheets for Datasets → System Cards: the most durable "checkable teeth" lineage
**[CONSENSUS] [DURABLE]**

Model Cards (Mitchell et al., FAT*/FAccT 2019) and Datasheets for Datasets (Gebru et al.) are the direct ancestors
of the System Cards OpenAI and Anthropic now ship with every frontier release (Claude Opus 4.6, Feb 2026; Claude
Sonnet 5, Jun 2026; GPT-5.6, referenced Jun 2026) — each documents specific, dated, sourced evaluation results
(named benchmark, named evaluator e.g. Apollo Research, specific finding) rather than narrative capability claims.
Model cards now do double duty as regulatory artifacts satisfying both EU AI Act Article 13 and ISO 42001
simultaneously. The durable lesson: the field succeeded by making specific, falsifiable fields the norm — named
benchmark + score + date + methodology link, not "performs well."

### F11 — Error-analysis-first, human-anchored rubrics: practitioner consensus on what makes a rubric real
**[CONSENSUS] [DURABLE]**

Hamel Husain and Shreya Shankar (hamel.dev, continuously updated through 2025, forthcoming O'Reilly book "Evals
for AI Engineers," 2026) converge on: **start with error analysis, not infrastructure** — read a real sample
(20–50 outputs) before writing grading criteria; keep one domain expert as quality arbiter rather than
crowd-averaging; only then formalize a rubric. The load-bearing claim is procedural: a rubric a team actually
trusts is derived from observed failure modes, not drafted from first principles or copy-pasted from a template.

### F12 — OWASP's self-correction: "coverage framework, not compliance checklist"
**[CONSENSUS] [DURABLE]**

OWASP Top 10 for LLM Applications (v2.0, 2025, current into 2026) is the clearest checklist-form artifact studied
— ten risk categories, each with a minimum control checklist. Independent commentary converges on the caveat that
is itself the finding: *"The goal is not to confirm that each category is theoretically addressed; it is to
confirm that each category has been actively tested against your specific deployment configuration and that the
findings from that testing have driven control design."* A checklist without an attached evidence artifact is
ceremony; the same checklist with one is teeth — the security-domain mirror of F11.

### F13 — Staleness handling can live in publishing infrastructure, not just document content
**[CONSENSUS mechanism exists] [DURABLE technique]**

Every fetched Azure Architecture Center page carries `ms.update-cycle: 180-days`, an `ms.date` (authorship), and a
separately tracked `updated_at` (last review) — confirmed on both the RAG design guide (2025-12-17 / 2026-07-02)
and agentic RAG guide (2026-06-23 / 2026-07-02). Microsoft's publishing pipeline enforces revisit cadence
independent of author memory. AWS lenses carry a "Publication date" plus a linked revision history. A structural
answer to staleness distinct from content: attach a machine-checkable freshness interval to every guidance
artifact and let tooling flag overdue ones.

### F14 — Vendor primary research is increasingly the actual source of new RAG technique knowledge
**[CONSENSUS this is happening] [MIXED — methodology durable, numbers fast-moving]**

Chroma Research publishes dated, narrow empirical reports rather than prescriptive guidance: "Evaluating Chunking
Strategies for Retrieval" (Jul 2024), "Embedding Adapters" (May 2024), "Generative Benchmarking" (Apr 2025),
"Context Rot" (Jul 2025), "Context-1" (Mar 2026). "Context rot" — that models don't process long context uniformly
— is framed as a generalizable phenomenon, later independently corroborated (arXiv 2606.29718, Jun 2026). **Caveat
per evidence discipline: Chroma sells a vector database.** Credible because empirical and falsifiable, but still
vendor-authored — a strong landscape/technique source, not independent best-practice authority; corroborate before
treating any single Chroma finding as settled.

### F15 — No gold-standard source formally encodes "check the current leaderboard"
**[Confirmed gap, not a contested claim] [DURABLE observation]**

Despite an active ecosystem of continuously-updated leaderboards in 2026 (BenchLM.ai, LMMarketCap, llm-stats.com,
Vellum's benchmark-saturation-aware leaderboard), none of the studied architecture-guidance sources (Azure, AWS,
GCP, Anthropic, OpenAI, Thoughtworks) formally instructs readers to consult a live leaderboard as a guidance step.
Every source that resists staleness does so via F9 (criteria over winners) or F6 (principles over patterns) —
never via "go check this live resource now." An explicit **use-time-research protocol** embedded in a skill would
be novel relative to this survey, not a known pattern to copy.

---

## 3. Recommended Encoding Forms

Ranked by evidence strength.

**1. Decision-factor list ("if you need X, choose/do Y") as the primary datastore/retrieval encoding.** Strongest,
most-repeated evidence (F1, F9): Azure and AWS independently converged on this shape because criteria (latency
budget, update frequency, cost sensitivity, hybrid/graph need, existing skills) outlive the products satisfying
them. **Recommendation:** encode criteria → guidance; demote named products to a dated, separately-labeled example
appendix, never embedded in the criteria themselves.

**2. Stable-core-plus-volatile-appendix, as two clearly separated sections.** Evidenced by F6 and by contrast with
F5's a16z cautionary case (durable structure and rotted specifics mixed indistinguishably, so the whole document
reads as stale). **Recommendation:** write the core (decision criteria, escalation triggers, evaluation
dimensions) to need no updates for ~2 years; stamp any named tool/benchmark reference with a date and revisit
interval per F13.

**3. ID-coded practices with staged reading paths, borrowed structurally from the AWS Agentic AI Lens (F3).** The
standout precedent — nearly isomorphic to Fullstack Director's REQ-ID/ADR-ID discipline: a flat, addressable
catalog navigated via maturity-specific reading paths instead of duplicated content per stage. **Recommendation:**
if the module exceeds ~15–20 discrete guidance items, give each a stable short ID and build 3–4 named reading
paths ("first RAG pipeline," "production hardening," "multi-source/agentic retrieval," "existing-system
retrofit") rather than repeating content at three maturity levels.

**4. ADR extended with a mandatory Review Trigger field — flagged as Fullstack-Director-original, not adopted
consensus.** F7 shows canonical ADR sources haven't added AI-specific fields; the one concrete template found is
non-authoritative. **Recommendation:** adopt it (Fowler's own generic "note the reevaluation trigger" guidance
supports it structurally) but don't claim it's settled industry practice.

**5. Qualitative escalation ladder, not a numeric maturity model, for retrieval-technique staging.** F8 supports
"start naive, escalate on measured need" as a heuristic; it does not support adopting anyone's numeric thresholds
as universal — those came from one uncorroborated source. **Recommendation:** encode escalation *triggers* ("move
to hybrid search when queries systematically miss on lexical/exact-match content") rather than numeric gates;
delegate thresholds to the project's own measured evals, consistent with F11's error-analysis-first discipline.

**6. A use-time-research protocol step, novel relative to all precedent (F15) but justified by the staleness
discipline itself.** No studied source does this explicitly. **Recommendation:** for genuinely volatile decision
points (embedding-model choice, reranker choice, current frontier-model claims), instruct the *executing agent* to
do a live check (per this project's own verify-with-live-sources convention) rather than rely on baked-in "current
best" claims — a decision *procedure* plus *criteria*, with volatile lookups deferred to execution time.

**Not recommended as primary:** pure narrative essay (F4) — valuable for judgment/worked examples but not
mechanically checkable; pure numeric maturity model (F8) — insufficiently corroborated; static catalog without
decision criteria (F2) — evidenced as the weakest of the three cloud-vendor approaches.

---

## 4. Checkable-Teeth Candidates

Ranked by portability into a mechanically-gradeable Verification Contract.

1. **Specific-value requirement in the Decision field** (F7): "not 'we chose RAG' but 'we chose RAG using
   text-embedding-3-large, threshold 0.78 cosine, top-8.'" Gradeable as concrete-parameters-present vs.
   generic-noun-only.
2. **Review Trigger field, graded in two tiers** (F7): presence, then specificity — a named external observable
   condition versus a vague placeholder ("review periodically").
3. **Evidence-attached-to-claim, never narrative-only** (F10, F12): any "X performs adequately" claim must cite a
   benchmark result, eval run, or explicit escalation trigger for why evidence wasn't gathered — never survives as
   bare assertion.
4. **Process-gate, not just artifact-gate** (F11): a rubric must point to the concrete failure case(s) it was
   derived from; if it can't, that's a signal it was written from first principles rather than evidence.
5. **Freshness metadata as a first-class, gradeable field** (F13): borrow Azure's update-cycle/updated-at pattern
   — every artifact touching a volatile decision carries a "valid as of / revisit by" stamp a drift check can flag
   as overdue. The cleanest mechanism found: grading it requires no judgment, only a date comparison.
6. **Named, falsifiable alternatives-considered with rejection reasons** (F7): checkable as presence of at least
   one named alternative plus a stated rejection reason — distinguishes real deliberation from asserted defaults.
7. **Coverage-vs-testing distinction as a grading rule** (F12): fail "checked" claims with no attached evidence,
   generalizing OWASP's self-critique beyond security to any checklist-shaped section.

---

## 5. What Changed Since Early 2025

- **AWS shipped an entirely new lens category.** The Agentic AI Lens (2026-06-10) didn't exist in early 2025; the
  Generative AI Lens itself was substantially restructured in a 2025-11-19 update adding agentic-workflow content
  for the first time. This formality level is under 8 months old.
- **Google Cloud's AI/ML Well-Architected content has stagnated relative to peers.** Last substantive update:
  2024-10-11, while Azure runs a 180-day cycle (both fetched pages touched within the prior two weeks) and AWS
  shipped two new/updated lenses in the same window. The GCP-vs-peers gap has widened, not narrowed.
- **Anthropic's own framing shifted** from "workflow vs. agent" (Dec 2024) to "context/memory as the central
  design problem" (Sep 2025) — tracking the field's move from "should this be an agent" to "how does an agent
  manage what it knows," directly relevant to this module's memory/grounding scope.
- **The vector-database market "settled," changing the decision itself.** The live question shifted from "which
  vector database" to "do you need a dedicated vector store at all," given pgvector-in-primary-DB maturity and new
  entrants like Amazon S3 Vectors (late 2025) — a new decision branch (dedicated vs. embedded vs. cold/archival)
  that didn't cleanly exist as a category in early 2025.
- **Chroma's "context rot" finding (Jul 2025), later corroborated (Jun 2026), pushed back** against "just use a
  huge context window instead of RAG" — retrieval/chunking discipline was re-legitimized empirically rather than
  assumed obsolete as windows grew.
- **Evals-as-a-discipline consolidated.** Husain/Shankar went from blog-and-course to a dedicated O'Reilly book
  (2026); Chip Huyen's "AI Engineering" (2025) is the first book-length treatment found giving the RAG-vs-fine-tuning
  decision full-chapter structured treatment rather than a blog aside.
- **AI-specific ADR practice emerged as a live, unsettled 2025–2026 genre** (review triggers, model-version
  pinning) that canonical ADR sources have not absorbed — room for a 2026-designed module to lead rather than summarize.

---

## 6. Contested Points Needing Designer Judgment

1. **Numeric vs. qualitative staged-adoption gates.** The only numeric maturity ladder found is one uncorroborated
   consultancy framework; vendor guidance is qualitative. Decide whether the module ships any numeric thresholds
   at all or pushes all thresholds to project-specific measured evals — evidence leans toward the latter, at some
   cost to perceived actionability.
2. **Whether to adopt a use-time-research protocol as an explicit skill step (F15).** No precedent found anywhere
   — a genuine Fullstack Director innovation, not a documented practice being followed. Adds process weight and a
   live-tool-access dependency at build time, but is the only mechanism that resolves staleness for genuinely
   volatile leaf-level facts.
3. **How much of the AWS Agentic AI Lens's ID-coded/staged-path structure to import.** Strongest structural
   precedent found, but built for ~40+ practices across 6 pillars, not one craft module. Over-import risks
   disproportionate bureaucracy; under-import forfeits the clearest available precedent.
4. **Trust weight for vendor-authored empirical research (Chroma) vs. vendor marketing.** Chroma's reports are
   methodologically real (falsifiable, later corroborated) yet commercially interested. This brief included Chroma
   with a caveat while excluding generic vendor "2026 RAG guide" SEO content throughout — a future designer
   extending this research should apply the same scrutiny rather than treat "has a technical report" as sufficient.
5. **The "facts→RAG, behavior→fine-tuning" heuristic's provenance.** Near-universal in secondary sources and
   consistent with Chip Huyen's book, but no single primary lab source states it in this crisp form. Reliable
   folk-consensus, not a single attributable primary claim.
6. **Weight given to Azure's self-reported latency/cost figures for agentic RAG** (2–3s standard vs. 8–15s
   agentic). Concrete and useful for illustrating trade-off magnitude, but self-reported and implementation-specific
   — landscape data, not a portable universal benchmark.

---

## 7. Source Registry

| # | Source | Org/Author | Date | Role |
|---|---|---|---|---|
| 1 | [RAG solution design and evaluation guide](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-solution-design-and-evaluation-guide) | Microsoft Azure Architecture Center | 2025-12-17, upd. 2026-07-02 | F1, F8 — phased-design FORM |
| 2 | [Develop an agentic RAG solution on Azure](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-agentic) | Microsoft Azure Architecture Center | 2026-06-23, upd. 2026-07-02 | F1, F8, §6.6 — decision criteria, cost/latency |
| 3 | [Choose an Azure service for vector search](https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/vector-search) | Microsoft Azure Architecture Center | 2025-10-20, upd. 2026-05-02 | F1, F9 — flowchart + matrix exemplar |
| 4 | [Generative AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html) | AWS Well-Architected | 2025-11-19 | F1, §5 — lens structure |
| 5 | [Agentic AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentic-ai-lens.html) | AWS Well-Architected | 2026-06-10 | F3 — strongest structural precedent |
| 6 | [Choosing an AWS vector database for RAG](https://docs.aws.amazon.com/prescriptive-guidance/latest/choosing-an-aws-vector-database-for-rag-use-cases/vector-db-options.html) | AWS Prescriptive Guidance | 2026 | F1, F9 — decision-factor-list exemplar |
| 7 | [Generative AI with RAG — reference architectures](https://docs.cloud.google.com/architecture/rag-reference-architectures) | Google Cloud Architecture Center | last reviewed 2025-09-22 | F2 — catalog-without-criteria counter-example |
| 8 | [Well-Architected Framework: AI and ML perspective](https://docs.cloud.google.com/architecture/framework/perspectives/ai-ml) | Google Cloud Architecture Center | upd. 2024-10-11 | F2, §5 — GCP staleness evidence |
| 9 | [Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents) | Anthropic | Dec 2024 | F4 — narrative-essay FORM |
| 10 | [Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval) | Anthropic | 2024-09-19 | F4, F14 — empirical technique report |
| 11 | [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Anthropic | 2025-09-29 | F4, §5 — durable-principle framing |
| 12 | [Anthropic system cards](https://www.anthropic.com/system-cards) | Anthropic | ongoing (Feb, Jun 2026) | F10 — documentation lineage |
| 13 | [A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) | OpenAI | 2025 | F4 — contrast to architecture-center depth |
| 14 | [OpenAI Retrieval platform docs](https://platform.openai.com/docs/guides/retrieval) | OpenAI | 2026 (current) | F4 — cookbook-level guidance |
| 15 | [Technology Radar Vol. 34](https://www.thoughtworks.com/radar) | Thoughtworks | 2026-04-15 | F6, §5 — staleness theme, RAG ring history |
| 16 | [bliki: Architecture Decision Record](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html) | Martin Fowler | upd. 2026-03-24 | F7 — canonical ADR definition |
| 17 | [Patterns for Building LLM-based Systems & Products](https://eugeneyan.com/writing/llm-patterns/) | Eugene Yan | ~2023 | F5 — durable pattern-axis catalog |
| 18 | [Emerging Architectures for LLM Applications](https://a16z.com/emerging-architectures-for-llm-applications/) | Andreessen Horowitz | 2023-06-20, unrevised | F5 — cautionary rotted-claim example |
| 19 | [RAG for LLMs: A Survey](https://arxiv.org/pdf/2312.10997) | arXiv | 2023-12 | F8 — naive/advanced/modular taxonomy origin |
| 20 | [Agentic RAG: A Survey](https://arxiv.org/html/2501.09136v4) | arXiv | 2025-01 | F8 — agentic-RAG taxonomy |
| 21 | [The Hitchhiker's Guide to Agentic AI](https://arxiv.org/abs/2606.24937) | arXiv (Roitman) | 2026-06-22 | §5 context — full-stack academic reference |
| 22 | [AI Architecture Decision Record Template](https://www.institutepm.com/knowledge-hub/ai-architecture-decision-record-template) | Institute of AI Product Management | 2026-05-23 | F7 — concrete AI-ADR field extensions (non-canonical) |
| 23 | [Architecture Decision Records: The 2026 Guide](https://www.catio.tech/blog/architecture-decision-record) | Catio | 2026 | F7 — contrast, no AI-specific fields |
| 24 | [RAG Maturity Model](https://ombrulla.com/insights/rag-maturity-model-stages-metrics-anti-patterns) | Ombrulla (consultancy) | dated 2026-03-11 | F8 — sole numeric maturity model, uncorroborated |
| 25 | [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) | OWASP GenAI Security Project | v2.0, 2025–2026 | F12 — checklist-vs-evidence distinction |
| 26 | [Chroma Research](https://www.trychroma.com/research) | Chroma (vendor) | reports 2024-05 to 2026-03 | F14 — empirical technique reports |
| 27 | [Diagnosing and Mitigating Context Rot](https://arxiv.org/pdf/2606.29718) | arXiv | 2026-06 | F14 — independent corroboration |
| 28 | AI Engineering: Building Applications with Foundation Models | Chip Huyen, O'Reilly | 2025 | §3, §5 — book-length decision framework |
| 29 | [LLM Evals: Everything You Need to Know](https://hamel.dev/blog/posts/evals-faq/) | Hamel Husain & Shreya Shankar | updated through 2025-07 | F11 — error-analysis-first methodology |
| 30 | [Choosing an AWS database service](https://docs.aws.amazon.com/pdfs/decision-guides/latest/databases-on-aws-how-to-choose/databases-on-aws-how-to-choose.pdf) | AWS | upd. 2026-05 | F1, F9 — general datastore decision-guide FORM |
| 31 | Model Cards for Model Reporting | Mitchell, Wu, Zaldivar et al. (Google, FAT*/FAccT) | 2019-01 | F10 — origin of checkable-documentation lineage |

**Excluded/down-weighted:** most "RAG in 2026," "enterprise RAG guide," and "best vector database 2026" search
results (onyx.app, techment.com, lastingdynamics.com, squirro.com, aggregator/Medium posts) were SEO content
restating the same claims without primary evidence — used only to triangulate near-universal folk heuristics
(§6.5), never cited as standalone best-practice evidence, per the rule that vendor/marketing claims about their
own product are landscape data only.
