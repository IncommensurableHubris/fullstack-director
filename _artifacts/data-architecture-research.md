# Data-architecture craft — research synthesis

> **What this is.** The evidence record for the data-architecture initiative (backlog: *🔴 CRITICAL — data-architecture
> craft is absent*). Live-sourced July 2026 by five parallel research subagents (Sonnet, repo-blind, one pillar each),
> verified and synthesized by the orchestrating session. The design record consumes this file; the five raw briefs
> under [`_artifacts/research/`](research/) carry the full findings + source registries and are committed beside it.
> A simplicity pass has been applied: this file carries only what the design needs — everything else stays in the briefs.

## 1 · Method + verification status

- **Five pillars, five briefs:** T1 datastore selection · T2 retrieval architecture · T3 grounding &
  verification-against-data · T4 agent memory · T5 methodology encoding (the *form* of gold-standard guidance).
- **Evidence discipline (enforced per brief):** ≥5 independent sources; URL + date per load-bearing claim;
  CONSENSUS/CONTESTED marking; **DURABLE vs FAST-MOVING tag on every finding** (durable ≈ still true ~2028;
  fast-moving ≈ stale in 6–12 months); vendor self-claims = landscape data, never best-practice evidence; a
  mandatory "what changed since early 2025" section.
- **Verification pass (orchestrator):** the three most design-load-bearing post-cutoff claims were re-verified
  against primary sources and **all confirmed** — DDIA 2nd edition (Kleppmann + Riccomini, O'Reilly, March 2026;
  martin.kleppmann.com 2026-03-24), the AWS Well-Architected **Agentic AI Lens** (docs.aws.amazon.com, published
  2026-06-10), and Thoughtworks Radar Vol. 34 (2026-04-15) carrying the theme *"retaining principles, relinquishing
  patterns."* Remaining claims ride on the briefs' own citations; every brief flagged its own gaps rather than
  fabricating (see §5), which is the honesty pattern the discipline was designed to force.

## 2 · Six cross-cutting conclusions

These recur independently across pillars; the design should treat them as load-bearing.

**C1 · Encode criteria, not winners.** The dominant staleness-resistance form across every studied gold-standard
source (Azure/AWS decision-factor lists; "if you need X → choose Y") — criteria like latency budget, update
frequency, and consistency need change far more slowly than which product satisfies them. Every pillar converged on
the same move unprompted: symptom-based triggers over fixed size numbers (T1), durable selection axes over vendor
names (T2), mechanism over settled-vocabulary pattern names (T3), pattern over product (T4). Named products belong
in **dated, clearly-volatile appendices** or use-time research — never inside the criteria. *(T5 F1/F9; T1 §3; T2 F9; T3 §2.2; T4 §2.2.)*

**C2 · Staged escalation, gated by "do you need this at all."** The consensus *shape* of good data/retrieval
guidance is a qualitative escalation ladder — start with the simplest thing that could work, escalate only on a
**measured gap or stated requirement**, and open with a Stage-0/Gate-0 test of whether the capability is needed at
all. T2's retrieval ladder (Stage 0 "no retrieval" → hybrid default → rerank/agentic/graph as justified
escalations) and T4's memory Gate-0 trigger list are the worked examples; T1's Postgres-first posture with named
breakpoint classes is the same shape for datastores. Numeric maturity models have no corroborated precedent —
encode **triggers**, delegate thresholds to the project's own evals. *(T2 §3; T4 §3; T1 §3; T5 F8/recommendation 5.)*

**C3 · Declare evaluation before building.** Golden query sets (≥20–50 hand-labeled, graded relevance), floor
metrics tied to the k the generator actually receives, thresholds with a declared operational action on crossing,
and re-run trigger lists — all declared at *design* time, before the pipeline exists. This is the retrieval/grounding
mirror of the framework's existing eval-suite acceptance contract; the field's error-analysis-first discipline
(Husain/Shankar) says rubrics derived from observed failures are the only ones teams trust. *(T2 F10/Stage 6; T3 §3.4; T5 F11.)*

**C4 · Deterministic-first verification hierarchy.** Never delegate to a judge what is mechanically checkable —
independently corroborated from the evals community, cloud grounding services, and NL→SQL safety practice, and it
directly validates the framework's own **bite rule**. T3's three-tier taxonomy (symbolic/deterministic → independent
learned classifier with numeric threshold → same-model self-check) is the organizing synthesis: **Tier 1 is required
for anything state-mutating** (money, IDs, dates, regulated facts); Tier 3 may never be the sole gate for a
Tier-1-eligible claim. Two durable gotchas the craft must teach: *schema enforcement solves syntax, not truth*, and
*RAGAS-style faithfulness scores contain an LLM judge one layer down* (claim decomposition). NL→SQL safety lives at
the driver/connection layer, never the prompt. *(T3 throughout; T5 F12.)*

**C5 · Use-time research is novel — and ours to build.** No studied gold-standard source formally encodes "consult
the live state of the world" as a guidance step (confirmed gap, T5 F15); they all resist staleness via C1/C2 only.
Yet the volatile leaf facts here (current embedding models, reranker leaders, vector-store landscape, memory
products) rot in months. The framework already owns the mechanism: **live-source verification** (spine-declared
Verify-live set → cited `docs/verification/<tech>.md` records → deterministic L7/G11 gates). Extending that pattern
to volatile *data-stack decision classes* is a genuine innovation with structural enforcement — flag it as
framework-original, not adopted consensus. *(T5 F15/recommendation 6; `shared/live-source-verification.md`.)*

**C6 · The field pivoted capability → governance.** H1-2026 research weight moved from "how to structure/retrieve"
to provenance, verified forgetting, memory poisoning (a write attack persists; ~95–98% injection success
query-only), audit trails, and the GDPR-erasure ↔ EU-AI-Act-audit tension (full applicability 2026-08-02). A craft
written now must weight **lifecycle/governance dimensions equal to retrieval cleverness** — the opposite emphasis
from 2024-era tutorials. *(T4 §2.7/§2.9/§5; T3 §2.3 provenance; C4's write-path guards.)*

## 3 · Per-pillar durable core

Format per pillar: decision dimensions (leverage-ordered) · defaults/when-nots · teeth shortlist (best
mechanically-checkable candidates; **[pair]** = pairing/cross-consistency check, the strongest kind) · what gets
delegated to use-time research. Full versions: the briefs' §3/§4.

### P1 · Datastore selection *(universal — every project with state)*

- **Dimensions (leverage order):** workload shape (OLTP/OLAP/HTAP) → data-model fit → consistency/availability via
  PACELC (not CAP) → scale envelope (symptom-based, never a fixed GB/row number) → operational maturity & cost
  (managed default below a platform-team threshold) → team skill/boring-tech bias → **exit/migration cost (always
  recorded, even as "accepted because X")**.
- **Default posture:** relational (Postgres-class) + extensions; split out only at a **named breakpoint class**
  (sustained write throughput past single-primary, true multi-region active-active, multi-TB analytical scans,
  vector search past tens-of-millions under strict SLAs, deep multi-hop graph traversal). Embedded OLAP (DuckDB
  class) is a real new middle rung before "stand up a warehouse." LLM apps **reweight** existing categories (JSONB
  traces, co-located vectors, semantic cache, queue before async inference) — they do not invent new ones.
- **Teeth shortlist:** ≥2 named alternatives · decisive driver maps to a named dimension **and traces to a REQ-ID**
  · symptom-based revisit trigger (not "if we outgrow this") · exit-cost statement present · reversibility class
  (one-way/two-way door) · **[pair]** durable commitment vs fast-moving vendor pick stated as two separate
  decisions · any "Postgres can do X" claim names the specific extension.
- **Use-time:** managed-DB landscape, extension maturity, TCO crossover numbers, DDIA-2e chapter specifics.

### P2 · Retrieval architecture *(fires when a knowledge/corpus feature exists)*

- **Shape:** the staged ladder. Stage 0 do-you-need-retrieval (parametric knowledge? corpus fits ~200K tokens +
  static + low volume → cache-and-stuff) → Stage 1 simplest-that-works (structured query beats embeddings for
  structured data; document-level for short docs; pgvector-in-existing-DB under ~1–5M vectors) → **Stage 2 hybrid
  (lexical + dense, RRF) as the default first stage** + chunking 400–600 tokens/~15% overlap escalated only on
  measured gap + embedding treated as **swappable seed** (shortlist via public benchmark, select via own eval set —
  MTEB is contaminated, shortlist-only) → Stages 3–5 (rerank / agentic / graph) each REQUIRE a measured-gap or
  stated-query-share justification — all three have documented null/negative regimes → Stage 6 eval declared
  **before** Stage 2 (golden set, floor at the generator's k, re-run triggers).
- **Key durable facts:** long-context absorbs easy cases but *context rot* (Chroma 2025, independently corroborated
  2026) bounds it — hybrid retrieve-then-reason is the consensus; agentic retrieval wins on hard/multi-hop at
  ~3–10× tokens (route by difficulty, bound iterations); index *family* + quantization + CRUD posture are
  architect-level, parameters are tuning.
- **Teeth shortlist:** golden-set reference (named file, ≥20, graded) · numeric floor metric · **[pair]**
  k-consistency (metric's k = k sent to generator) · chunking params or explicit no-chunking rationale ·
  **[pair]** index CRUD posture vs stated freshness (hourly updates + batch-rebuild index = contradiction) ·
  **[pair]** escalation present → nearby measured-gap justification ("why not simpler") · embedding named +
  dimensions + reindex trigger.
- **Use-time:** current embedding/reranker leaders, vector-store landscape, long-context-vs-RAG cost crossover
  (compute $/query live, never a baked constant).

### P3 · Grounding & verification-against-data *(fires when LLM output makes claims from, or writes to, owned data)*

- **What the architecture declares (9 items, condensed):** named ground-truth source per claim-type (a table/view/
  index, not "our data") · freshness/staleness contract · **check tier per claim-type** (T3's three tiers; Tier 1
  deterministic REQUIRED for state-mutating/money/IDs/dates) · numeric threshold + declared action on crossing
  (block/regenerate/escalate — a threshold without an action is not a control) · fallback behavior per failure mode
  (silence never acceptable) · provenance/audit line (what's logged to reconstruct "what grounded this output") ·
  **write-path admission rule** (schema → referential → business-rule → commit, enforced where the LLM cannot
  bypass) · citation contract (resolution is deterministic — no excuse otherwise; span-support may be judged) ·
  provider-portability note where provider-specific grounding/structured-output features are load-bearing.
- **Teeth shortlist:** named specific ground-truth source (bite: mutate to nonexistent → must flag) · numeric
  threshold present wherever a score is named (bite: strip the number) · **[pair]** state-mutating claim-type →
  Tier-1 check named · read-only enforcement declared at driver layer (prompt-only fails by construction) ·
  fallback action named per failure mode · **[pair]** "citations verified" → resolution-vs-support split declared.
- **Use-time:** provider grounding-service state (all three clouds now sell one), guardrails-ecosystem currency
  (individual validators go stale), structured-output dialect portability.

### P4 · Agent memory *(fires on Gate-0 triggers; agent-system profile or embedded agent)*

- **Gate 0 (do you need designed memory at all):** need ≥1 of — repeated same-domain/user tasks · corrections must
  stick · evolving domain rules · persistent entities across calls · demonstrated token-cost of re-injection ·
  multi-agent shared state · task exceeds context window. Absent a trigger: session/thread state + compaction is
  **correct**, and the memory ADR must itself cite which trigger fired.
- **Dimensions:** kind scoping (working free; semantic/episodic/procedural each individually justified —
  procedural last, least proven) → substrate per kind (fuzzy recall→vector; multi-hop/temporal→graph; exact→
  KV/relational; low-volume auditable→files; **kinds want different backends — a one-size memory module is itself
  a design smell**) → write policy (async default beyond demo; verbatim-alongside-extracted where storage allows —
  extraction is a lossy one-way door; explicit ADD/UPDATE/DELETE/NOOP semantics for anything user-correctable) →
  retrieval policy (multi-signal; recency first-class for episodic; below a few hundred items a scoring formula is
  ceremony) → **lifecycle (a TTL floor is mandatory — unbounded retention is a named failure mode)** → sharing
  model + authorization boundary (shared mutable memory with no authz model is an anti-pattern) → privacy tiering +
  pre-write PII redaction + derived-memory deletion reach → adversarial posture (any write path fed by untrusted
  content = injection surface; memory poisoning persists across sessions).
- **Teeth shortlist:** Gate-0 trigger cited in the memory ADR · per-kind substrate mapping (not one "the database")
  · **[pair]** mutable kind → conflict-resolution semantics named · lifecycle number/rule present · **[pair]**
  user-facing deletion → derived-memory reach statement · **[pair]** >1 agent → sharing topology + authz boundary
  named together · write-authorization + provenance named · negative scope (what will NOT be persisted).
- **Use-time:** memory-product landscape (Letta/Zep/Mem0/LangMem/provider-native — patterns are durable, products
  churn), verbatim-vs-extracted evidence state (single-source in 2026), procedural-memory maturity.

## 4 · Consolidated contested-points register

Deduplicated across briefs; each with a proposed disposition for the design to confirm.

| # | Contested point | Proposed disposition |
|---|---|---|
| 1 | pgvector→dedicated-store crossover (10M–100M spread) | Require the architect to state *their own* recall/latency/scale target; never cite a borrowed benchmark number |
| 2 | Reranking: default vs measured addition | Encode the measurement-gated framing (Stage 3), not a side |
| 3 | GraphRAG thresholds (single-study origin) | Directional anchors only; require own cost math + stated query-share |
| 4 | Long-context-vs-RAG crossover (25×–1250× spread) | Encode the decision *procedure* (compute $/query live); never a constant |
| 5 | Fine-tune vs off-the-shelf embeddings | Encode "benchmark both on own eval set" as the policy |
| 6 | Verbatim vs extracted memory (2026 ablation, unreplicated) | Default verbatim-alongside-extracted where storage allows; flag the evidence state |
| 7 | Hybrid-memory-by-default vs start-narrow-graduate | Anti-ceremony favors start-narrow; name hybrid's two-systems operating cost |
| 8 | Write-path pattern naming (no settled vocabulary; ATP days old) | Describe the mechanism generically; offer analog names as non-canonical |
| 9 | Three-tier check taxonomy (T3's synthesis, not industry vocabulary) | Adopt as the craft's mental model, flagged as framework-adopted synthesis |
| 10 | Numeric thresholds (0.7 groundedness etc.) | Require *a declared number*, never prescribe one |
| 11 | GDPR erasure ↔ EU-AI-Act audit tension (legally unresolved) | Teach the tiering mitigation; flag "engineering mitigation, not legal guarantee" |
| 12 | NL→SQL guidance placement (data craft vs general tool-safety) | Design call — the driver-layer principle generalizes to any LLM-driven mutation |
| 13 | "Boring tech has best AI-tooling support" corollary | Flag as possibly circular; don't encode |
| 14 | Use-time-research step (no external precedent) | Adopt via existing Verify-live machinery; mark framework-original |

## 5 · Known gaps (flagged by the researchers, preserved honestly)

DDIA-2e full ToC unconfirmed (O'Reilly 403'd automated fetch; themes primary-sourced) · AlloyDB native-vector
maturity unconfirmed · Momento-vs-Redis semantic-cache parity unconfirmed · verbatim-beats-extracted is
single-source · GraphRAG scale thresholds single-study · several TCO/crossover numbers converge without disclosed
methodology (directional only).

## 6 · Inside-view wiring map (framework side; researched inline, agents were repo-blind)

Every pillar's teeth attach to an **existing** mechanism — the craft needs zero new machinery classes:

| Need | Existing mechanism |
|---|---|
| Selection rationale teeth | ADR decision drivers + `Rule:` line; breadth rubric already makes silent "data & persistence" a finding |
| Retrieval eval floors | `eval-suite` VC row (harness cmd · dataset ref · floor) — a golden-set recall floor *is* this row |
| Grounding write-path + checks | VC rows + §8 crosscutting concepts + the bite rule |
| Memory ADR teeth | the `Category: memory` line (exists, zero craft today); `topology`'s "REQUIRES ~15× justification" clause is the teeth pattern to replicate per pillar |
| Volatile picks → use-time research | `shared/live-source-verification.md` (Verify-live rows → cited records → L7/G11 gates) |
| Missing upstream data facts (corpus size, freshness, query patterns) | Reconcile **flesh-out** channel (Tier-2) — the craft names its required inputs; no 00-discovery change needed in v1 |
| Anti-ceremony activation | the embedded-agent module pattern — declared trigger fields activating obligations only where real |

## 7 · Open design questions the approaches must answer

1. **Activation model** — always-on reference vs layered universal-core + trigger-gated LLM modules vs distribution
   into existing files.
2. **Home(s)** — one `references/data-architecture.md` vs per-pillar placement; how it splits stable-core vs
   volatile-appendix (C1/C5).
3. **Verify-live binding** — how volatile data-stack picks enter the Verify-live set (03 proposes rows via
   flesh-out? a named volatile-decision-class list in the craft?).
4. **ADR treatment** — new `Category:` values (datastore/retrieval/grounding) vs content-requirements independent
   of the agent-system category line (datastore ADRs exist under `webapp` too); the Review-Trigger field (T5 —
   adopt, flagged framework-original).
5. **Teeth placement** — which shortlist items land in Pass-1 deterministic lint vs VC-row obligations vs
   reconciler judgment lenses; keep the count lean (teeth that fire on every project get ignored).
6. **Upstream touch** — v1 stays 03-local (flesh-out covers missing inputs) vs also seeding a 00-discovery
   data-facts facet. Recommendation: 03-local first.

## 8 · Top source anchors

Primary anchors the design may cite directly (full registries in the briefs): DDIA 2e (Kleppmann/Riccomini,
O'Reilly, 2026-03) · AWS Agentic AI Lens (2026-06-10) + AWS/Azure vector-store decision guides · Thoughtworks
Radar Vol. 34 (2026-04-15) · Anthropic Contextual Retrieval (2024-09-19) + multi-agent research system (2025-06-13)
· Microsoft GraphRAG/LazyGraphRAG (2024) · Chroma context-rot (2025; corroborated arXiv 2606.29718) · MMTEB (ICLR
2025) + Reimers contamination note (2024-12-22) · JSONSchemaBench (arXiv 2501.10868) · Bedrock Automated
Reasoning / Azure groundedness / Vertex Check Grounding docs (2025–2026) · Generative Agents scoring (arXiv
2304.03442) · Zep/Graphiti (arXiv 2501.13956) · MINJA memory poisoning (arXiv 2503.03704) · memory-mechanisms
survey (arXiv 2602.06052) · Model Cards lineage (FAccT 2019) · Husain/Shankar evals discipline (hamel.dev,
2025–2026) · OWASP LLM Top 10 v2 (2025).

## 9 · Evals pass (E1 addendum) — inside audit + outside verification

> Added after the user widened scope: the data pillars' eval-facing declarations must interface coherently with a
> gold-standard evals **operational** layer (anchor: Hamel Husain). Evidence: all 7 installed `evals-skills` read in
> full (v0.2.0 plugin cache) · inside audit of FD's six eval touchpoints (00 eval-block authoring · 01 harness-first
> skeleton · 03 eval-suite oracle/VC · 04 eval-first RED + grader-bites · 05 llm-review · 06 G8) · outside brief
> [`research/T6-evals-method.md`](research/T6-evals-method.md) (Sonnet, live-sourced July 2026).

**Verdict: FD's declaration/gate layer is sound and Husain-aligned; the gaps are operational — confirming the
compose-don't-duplicate thesis.** Load-bearing facts:

- **License/maintenance:** `hamelsmu/evals-skills` is **MIT** (LICENSE + GitHub API confirmed), created 2026-03,
  active through 2026-06, seven skills, installable via Claude plugin marketplace **or `npx skills add`** (not
  Claude-only — portability concern resolved), zero tagged releases (record the consumed commit/version when
  composing).
- **The canonical method statement is the 2026-01-15 FAQ** ("LLM Evals: Everything You Need to Know", hamel.dev);
  judge-validation math **sharpened between the 2024-10 guide and the 2026-01 FAQ** — from "acceptable agreement"
  to TPR/TNR on disjoint splits + Rogan-Gladen bias correction + bootstrapped CIs. FD's ">90% agreement" distills
  the **old** form and is now named an anti-pattern by the source it distilled (`validate-evaluator`: "Using raw
  accuracy or percent agreement. Use TPR and TNR."). **Audit finding #1 (the headline): fix the criterion, not
  just deepen it** — a `judge(validated)` grader means a **judge-validation record** (TPR/TNR + split sizes +
  leakage rule honored + pinned judge model), presence/currency-checkable by 05.
- **Audit findings #2–6 (all operational-depth, none contract-layer):** judge-*writing* craft absent (one failure
  mode per judge · four components · critique-before-verdict · borderline few-shots) · error-analysis procedural
  depth (saturation ~100 traces · first-upstream-failure rule · observations-not-explanations · fix-before-
  evaluator triage) · synthetic bootstrap missing (dimension→tuple→two-step generation — FD's "seed 20–50 from
  real failures" has no greenfield answer; 05's "Features × Scenarios × Personas" line is literally this method's
  dimension structure, shape borrowed, method absent) · RAG-eval method (synthetic QA + adversarial distractors +
  chunking grid search + metric-by-query-type — the exact P2/P3 interface surface) · labeling ergonomics (leave
  wholly to the operational layer).
- **External standing of FD's originals:** the bite rule has a ~50-year precedent (**mutation testing**, 1970s) —
  durable, keep proudly; the **fresh-context verifier** has *partial* precedent (independence-of-testing, Myers
  1979/ISTQB) and is otherwise novel-but-well-motivated via self-preference-bias research — keep, flagged
  framework-original.
- **The sharpest contested point: eval-driven development.** Husain's FAQ: "generally no" — criteria drift
  (Shankar, *Who Validates the Validators*, UIST 2024) means criteria cannot be fully pre-specified — **except for
  known, non-negotiable constraints stated up front**. FD mandates eval-first RED. **Reconciliation the design
  must state explicitly:** FD's eval blocks declare the *contract* (dataset home · floor · negatives) for stated
  constraints — Husain's carve-out — while dataset *content* grows error-analysis-first (05 feeds failures back;
  edits are amendments). The 00-time dataset is a **seed, never a complete specification**; doctrine text should
  say so to stay on the right side of criteria drift.
- **Composition mechanism (the design's E1 shape):** the framework names an **evals-operations capability**
  (error analysis · judge writing · judge validation · synthetic data · RAG eval · pipeline audit) at each eval
  touchpoint via one reference line — bound to `evals-skills` where installed (any `npx skills add` harness),
  falling back to FD's lean inline distillations; absence recorded, never silently skipped. Same cascade doctrine
  as live-source verification ("name a capability, not a vendor"). The consumed pack version is recorded
  (no tagged releases upstream).
