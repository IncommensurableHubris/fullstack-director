# T3 — Grounding & Verification-Against-Data: Research Brief

Scope: patterns for deterministically checking LLM output against a datastore as ground truth, and what an
architect should declare at design time. Pure outside-view research, live web sources only, July 2026.

---

## 1. Executive Summary

- **Schema enforcement solves syntax, not truth.** Constrained decoding (OpenAI, Gemini, Anthropic, and the
  open-source XGrammar/Outlines/Guidance stack) reliably produces parseable, shape-correct JSON. It gives zero
  guarantee the *values* inside are correct. Every credible source treats this as closed. CONSENSUS / DURABLE.
- **No canonical name yet exists for "LLM proposes → deterministic layer validates → commit/reject."** The
  principle is converged-upon; the vocabulary isn't. The most rigorous formal treatment ("Agentic Transaction
  Processing," Stanford/QuadriumAI, arXiv July 2026) is days old at research time — don't cite it as settled
  industry language. CONTESTED / FAST-MOVING.
- **All three major clouds now sell a grounding-check primitive as a separate callable service**, not just
  "better prompting": Bedrock (contextual grounding check + the genuinely deterministic Automated Reasoning
  checks), Azure AI Content Safety (groundedness detection), Vertex/Agent Search (Check Grounding API, <500ms).
  Biggest structural shift since early 2025. CONSENSUS / product surface FAST-MOVING, category DURABLE.
- **A three-tier verification taxonomy falls out of the evidence**: (1) symbolic/deterministic (schema, DB
  constraint, allowlist, formal-logic policy) — reliably passes an adversarial bite test; (2) independent learned
  classifier/NLI scorer (provider grounding APIs, RAGAS-style faithfulness under the hood) — probabilistic,
  thresholded, better than self-grading but not absolute; (3) same-model/same-family self-check (NeMo Guardrails'
  fact-checking and hallucination rails are confirmed LLM-based) — weakest, since the blind spot causing the
  error can also pass the grade. Synthesized here from corroborating primary sources / DURABLE as a mental model.
- **NL→SQL safety is solved at the infrastructure layer, not the prompt layer.** Read-only DB connections
  enforced at the driver, table/column allowlisting in code, AST parsing, `EXPLAIN`-based cost rejection.
  CONSENSUS / DURABLE. Benchmark numbers (BIRD ~75–82% vs. ~93% human baseline) are FAST-MOVING; the qualitative
  finding — dirty real schemas break text-to-SQL more than query complexity — is durable.
- **Citation faithfulness decomposes into three gradable layers**: cited at all (deterministic) → citation
  resolves to a real chunk/row (deterministic) → resolved source actually supports the claim (NLI/judge). Only
  the third is inherently non-deterministic. CONSENSUS structure / DURABLE. Reported hallucination rates vary
  wildly by task (11–57% general RAG vs. 78–90% in one narrow academic-citation-fabrication study) — treat any
  single number as context-specific, not constant.
- **"Faithfulness," "groundedness," "factuality" are different constructs vendors routinely blur.** Faithfulness
  = claims entailed by supplied context. Groundedness = faithfulness *plus* the retrieved evidence must itself be
  relevant and sufficient. Factuality = consistent with world knowledge, not just supplied context. A response
  can be faithful-but-wrong or correct-but-unfaithful. CONSENSUS in academic sources / DURABLE; CONTESTED in
  vendor marketing.
- **RAGAS-style "faithfulness scores" are not actually deterministic under the hood.** Claim decomposition is
  itself an LLM call before the NLI check runs; a miss or over-split silently corrupts the downstream score. A
  number that looks like a metric can be a judge call wearing a metric's clothes. CONSENSUS / DURABLE — the most
  important gotcha for the skill to teach.
- **Established practitioner consensus (Hamel Husain, Eugene Yan, the broader evals community) says never
  delegate to a judge what's mechanically checkable** — schema conformance, exact-match, calculations,
  referential integrity, low-latency gates. Reserve LLM-judges for subjective properties, and even then require
  100+ labeled examples, PASS/FAIL over Likert, pairwise over pointwise, measured precision/recall against human
  labels. Directly corroborates this framework's "bite rule." CONSENSUS / DURABLE.
- **LLM-judge self-consistency is not validity.** A 2026 study (21 judges, ~541K judgments) found judges can hold
  >0.95 test-retest reliability while carrying >0.10 position bias simultaneously — stable and still wrong.
  Exact-match agreement overstates judge quality by 33–41 points versus chance-corrected kappa. CONSENSUS /
  DURABLE finding, numbers study-specific.

---

## 2. Findings

### 2.1 Structured outputs / constrained decoding (Q1)

Constrained decoding compiles a JSON Schema into a finite-state machine; tokens that would leave the valid path
get logits set to −∞, so schema-violating tokens have zero probability
([Let's Data Science, 2026](https://letsdatascience.com/blog/structured-outputs-making-llms-return-reliable-json)).
This is a **mathematical guarantee of syntax, never semantics** — perfectly-shaped JSON can still hold hallucinated
values. Stated independently by Anthropic's own docs, academic benchmark authors, and practitioner blogs.
CONSENSUS / DURABLE.

Provider timeline: OpenAI shipped `response_format: json_schema` claiming 100% schema-match on its own evals in
August 2024 ([OpenAI](https://openai.com/index/introducing-structured-outputs-in-the-api/) — vendor claim,
landscape data only). Gemini added `response_schema` in May 2024. **Anthropic did not reach GA on structured
outputs/strict tool use until November 2025** — ~15 months after OpenAI — per its own docs, which still carry the
`structured-outputs-2025-11-13` beta-header artifact during a stated transition period
([platform.claude.com, fetched July 2026](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)).
Dated historical fact (DURABLE record); "who leads" is FAST-MOVING.

Anthropic's docs are unusually candid about what enforcement does **not** cover: safety refusals override the
schema (still 200 status, still billed, non-conforming payload), `max_tokens` truncation produces incomplete
output, and there's a documented enum-casing bug (Claude can return a value differing from the schema only in
capitalization). Claude's supported JSON-Schema subset lacks numeric bounds, string-length constraints, external
`$ref`, and recursive schemas — OpenAI's dialect differs at these same points. **Schema portability across
providers is not solved.** CONSENSUS (official docs, cross-checked below) / unsupported-feature list is
FAST-MOVING.

Independent corroboration: a 244-model, 23-provider compatibility test
([Requesty, May 30, 2026](https://www.requesty.ai/blog/structured-outputs-across-llm-providers-the-compatibility-mess))
found Anthropic's Messages endpoint passing conformance on 93% of tested models, OpenAI Responses 82%; only 14
providers had a perfect pass rate across every model and endpoint. Failure modes: some providers lack
`json_schema` entirely (DeepSeek errors explicitly), smaller/distilled models struggle even where the provider
supports the feature, and dialect incompatibilities (Anthropic rejects recursive `$ref`; OpenAI accepts it) block
naive portability. FAST-MOVING snapshot.

Academic anchor: JSONSchemaBench ([arXiv:2501.10868](https://arxiv.org/pdf/2501.10868), Jan 18 2025, rev. Feb 27
2025) benchmarked six engines (Guidance, Outlines, Llama.cpp, XGrammar, OpenAI, Gemini) against 10,000 real-world
schemas plus the official JSON Schema Test Suite — the field's first rigorous, engine-agnostic methodology.
XGrammar is now the default constrained-decoding backend for vLLM, SGLang, TensorRT-LLM, and MLC-LLM: open
infrastructure, not a research artifact. DURABLE methodology and infra-adoption fact / pass-rate numbers
FAST-MOVING.

**Implication**: schema enforcement is a precondition that removes an entire class of parsing failures, freeing
the deterministic-validation layer to focus on semantic/referential/business-rule correctness. It is not
grounding verification and must never be represented as one.

### 2.2 The write-path pattern (Q2)

The *principle* — LLM output is an untrusted proposal; only a separate deterministic layer may turn it into
committed state — is broadly convergent across 2026 practitioner writing
([Medium/Squalli](https://medium.com/@squalliahmed/deterministic-ai-at-work-the-llm-is-the-most-unreliable-function-in-my-pipeline-so-i-treat-it-88ff2888b20a);
[Medium/Rahaman](https://medium.com/data-science-collective/llms-should-reason-infrastructure-should-enforce-86493b936f84)).
CONSENSUS on the principle / DURABLE.

**No single settled name exists yet**, unlike "circuit breaker" or "saga" in distributed systems. The most
rigorous formalization is "Agentic Transaction Processing" (ATP) from "Mnemosyne"
([arXiv:2607.00269v2](https://arxiv.org/html/2607.00269), Stanford + QuadriumAI, **July 5, 2026**). It names:
proposal → **admission gate** (checks a declared constraint set 𝒞 over current effective state) →
**committed-transition log** (append-only source of truth) → **StateView** (effective-state projection). Rejected
proposals produce queryable rejection events with reasons; a bounded "localized cascading repair protocol"
attempts auto-repair before re-admission. Presented explicitly as **novel research**, not documented practice.
CONTESTED (too new to call established) / FAST-MOVING — describe the mechanism, don't cite ATP terms as settled
vocabulary.

Better-established prior art being explicitly repurposed for agentic write-paths: the **Saga** and **Transactional
Outbox** patterns, both pre-LLM and well-established
([InfoQ](https://www.infoq.com/articles/saga-orchestration-outbox/);
[Hendricks](https://brandonlincolnhendricks.com/research/implementing-saga-pattern-long-running-ai-agent-workflows)).
Outbox's core discipline — commit the state change and the "intent to act" atomically, then process the effect
from a durable queue — maps directly onto "LLM proposes a side effect, system records it durably, a separate
deterministic process executes/validates it." DURABLE pattern / application to LLM agents is FAST-MOVING (common
framing only since 2025–2026).

A parallel human-facing formalization: **HITL commit-point gating** — full autonomy on reversible actions,
mandatory human approval before any irreversible commit, framed as a "Reversible/Irreversible Action Taxonomy"
([ResearchGate](https://www.researchgate.net/publication/404949852_Human-in-the-Loop_at_the_Commit_Point_Architectural_Patterns_for_Trustworthy_Agentic_AI_Deployment_in_Enterprise_Scheduling)
— credibility contested, not obviously peer-reviewed; the reversible/irreversible split is a durable idea
independent of this paper).

The clearest productized deterministic-validation capability is **AWS Bedrock Automated Reasoning checks** —
genuinely symbolic: an encoded logical policy plus a formal solver mathematically verifies a response, explains
*why* a statement is or isn't supported, and surfaces unstated assumptions
([AWS ML Blog](https://aws.amazon.com/blogs/machine-learning/minimize-generative-ai-hallucinations-with-amazon-bedrock-automated-reasoning-checks/);
gated preview at re:Invent 2024, matured through 2025–2026). The clearest real-world proof that
symbolic-verification-of-LLM-output is commercially viable, not just academic, distinct from every other
grounding product here, which are learned classifiers. FAST-MOVING product surface / DURABLE proof-of-concept.

**Recommendation**: describe the write-path mechanism generically (proposal → deterministic admission → durable
commit-or-reject-with-reason) without anchoring to ATP, Saga, or HITL-commit-gate as *the* canonical name.

### 2.3 Ground-truth designation and provenance (Q3)

No branded "oracle table" industry pattern exists outside academic eval methodology, where swapping a
**ground-truth oracle** in place of real retrieval is standard to isolate hallucination-driven degradation from
retrieval-driven degradation (recurring across 2026 arXiv eval papers). Useful design-time device: specify "what
would the oracle condition look like" before building the real retrieval path. DURABLE / CONSENSUS within
academic eval design.

**W3C PROV** (a W3C Recommendation since 2013 — pre-LLM, DURABLE, standards-track) is repeatedly invoked as the
right conceptual vocabulary for LLM/agent provenance: entities, activities, agents, and relations between them
([Zylos Research, Apr 2026](https://zylos.ai/research/2026-04-25-agent-identity-provenance-signed-audit-trails/);
["From Agent Traces to Trust," arXiv:2606.04990v3](https://arxiv.org/html/2606.04990v3);
[AuditWeave, arXiv:2607.09682](https://arxiv.org/html/2607.09682)). One source assembles a fuller emerging stack:
PROV for the conceptual graph, SPIFFE for process identity, OPA-style decision logs for policy evidence,
OpenTelemetry for trace correlation, Sigstore/SLSA/in-toto/C2PA/SCITT for signed provenance. CONSENSUS that
PROV-style modeling is the right frame / DURABLE conceptually; assembly into one recognized "LLM-provenance
stack" is brand-new and FAST-MOVING — teach the conceptual shape, don't over-specify tooling.

Enterprise catalog vendors are extending existing governance to cover models/agents as governed objects rather
than treating AI grounding as a bespoke discipline: Databricks' **Unity AI Gateway** (June 16, 2026) extends
Unity Catalog's access-control/discovery/lineage/audit to models, MCP services, agents, and skills; "External
Lineage" (GA 2026) extends lineage beyond Databricks-native assets
([Databricks Blog](https://www.databricks.com/blog/ai-governance-data-ai-summit-2026-whats-new-unity-ai-gateway)).
Durable signal: **ground-truth designation is converging toward "register it in the same governance system as
the rest of your data,"** not a bespoke shadow system. FAST-MOVING product / DURABLE principle.

Amazon Bedrock Knowledge Bases exemplifies provenance-at-retrieval productized: `RetrieveAndGenerate` returns
citations to source chunks, though AWS already deprecated the original `citation` field for separate
`generatedResponse`/`retrievedReferences` fields — even citation-API shape is still churning
([AWS docs](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-retrieve-generate.html)). FAST-MOVING.

### 2.4 Citation / attribution faithfulness (Q4)

Fine-grained (span/sentence-level) attribution is the converged research direction over coarse document-level
citation ([survey, arXiv:2508.15396, Aug 2025](https://arxiv.org/pdf/2508.15396)). CONSENSUS / DURABLE.

Reported hallucination rates vary by what's measured and must not be treated as one number: general commercial
RAG is reported at 11–57% citation-hallucination (aggregated secondary source; the wide range itself signals
inconsistent methodology across studies); a narrower, more alarming figure — 78–90% "fabricated citations," 50+
found across 300 ICLR 2026 submissions — comes from **CiteGuard**
([arXiv:2510.17853v4, Apr 13 2026](https://arxiv.org/html/2510.17853v4)), specifically about LLMs fabricating
*references to nonexistent academic papers*, a narrower phenomenon than RAG span-attribution against a supplied
corpus. **Do not conflate the two.** CONTESTED (order-of-magnitude spread) / FAST-MOVING.

Verification decomposes into three layers of differing checkability: (a) did the model emit a citation at all —
deterministic presence check; (b) does it resolve to a real, currently-valid chunk/row — deterministic lookup;
(c) does the resolved source actually support the claim — an entailment/NLI problem, currently solved via
LLM-judge (CiteCheck, [arXiv:2502.10881](https://arxiv.org/pdf/2502.10881)) or hybrid retrieval-grounded agents
(CiteGuard, which explicitly moves beyond pure LLM-as-judge by requiring the checker to retrieve and examine
actual source content). Only (c) is inherently non-deterministic; (a) and (b) have no excuse not to be
deterministic in production. CONSENSUS on the three-layer structure (synthesized, methodologically consistent
with how Vertex's own API and Bedrock Knowledge Bases both separate "citation produced" from "citation supports
claim") / DURABLE structure, FAST-MOVING implementations.

Google's productized version (Vertex/Agent Search **Check Grounding API**) returns a single 0–1 "support score"
approximating the fraction of entailed claims, plus optional claim-level scores, with **no partial credit** — a
claim that's only partly correct scores fully ungrounded (worked example: "Google was founded by Larry Page and
Sergey Brin in 1975" scores entirely ungrounded because the year is wrong, despite correct founders). Documented
latency <500ms, designed for per-inference calls, not just eval time
([docs.cloud.google.com](https://docs.cloud.google.com/generative-ai-app-builder/docs/check-grounding)).
CONSENSUS (official doc) / FAST-MOVING specifics, DURABLE "no partial credit" design choice worth copying.

### 2.5 Groundedness-eval ecosystem (Q5)

RAGAS, DeepEval, and TruLens are all actively maintained in 2026 but occupy different niches: RAGAS for offline
experimentation, DeepEval as a Pytest-native CI/CD gate (DeepEval 4.0 added agent-native eval workflows; repo
updated July 8 2026), TruLens for production observability (its "Triad" = context relevance + groundedness +
answer relevance). TruLens's parent TruEra was acquired by Snowflake (announced May 2024); Snowflake committed to
keeping it open source and its maintainer list is now Snowflake employees — **not deprecated**, but roadmap-coupled
to Snowflake ([Snowflake blog](https://www.snowflake.com/en/blog/trulens-open-source-ai/)). CONSENSUS all three
are safe 2026 choices / FAST-MOVING on specific APIs.

**The load-bearing gotcha**: RAGAS-style "faithfulness" first has an LLM decompose the response into atomic
claims, *then* runs an NLI-style entailment check per claim against retrieved context
([saulius.io](https://saulius.io/blog/ragas-rag-evaluation-metrics-llm-judge)). **Decomposition is itself a judge
call** — a miss or over-split silently corrupts the downstream "deterministic-feeling" score. A faithfulness
score inherits every LLM-judge reliability problem, one layer removed from view. CONSENSUS / DURABLE — a
structural property of the design pattern, not a version-specific bug.

Three constructs are frequently conflated: **faithfulness** (claims entailed by context — continuous score),
**groundedness** (faithfulness *plus* retrieved evidence must be relevant and sufficient — closer to a hard
gate), **factuality** (consistent with world knowledge, which may diverge from supplied context)
([futureagi glossary](https://futureagi.com/glossary/groundedness/); corroborated empirically by
[Wallat et al., UvA 2025](https://staff.fnwi.uva.nl/m.derijke/wp-content/papercite-data/pdf/wallat-2025-correctness.pdf),
showing a response can be correct-but-unfaithful or faithful-but-incorrect). CONSENSUS academically / CONTESTED
in vendor marketing which uses these interchangeably; DURABLE distinction.

No dominant single "winner" exists; practitioner sources converge on running more than one tool together (e.g.,
RAGAS offline + DeepEval in CI + a provider grounding-check inline in production) rather than picking one
framework for everything.

### 2.6 NL→SQL / query-generation verification (Q6)

Converged best practice treats LLM-generated SQL as untrusted input requiring a multi-layer gate
([Dietrich](https://timdietrich.me/blog/sql-agent-safety-architecture/);
[Rietta](https://rietta.com/blog/ai-sql-database-data-protection-read-replica/)):

1. **Read-only enforcement at the driver/connection layer** (e.g., `psycopg3`'s `conn.set_read_only(True)`), so a
   generated `DROP TABLE`/`INSERT`/`UPDATE` is rejected by the database itself, independent of prompt or model
   output — the clearest "passes an adversarial bite test" candidate in this entire brief.
2. **Table/column allowlisting implemented in code**, checked against the parsed query, not asked of the model.
3. **AST-level static parsing** plus **`EXPLAIN`-based cost rejection** to block full-table-scans or pathological
   plans pre-execution.
4. **Sandboxed dry-run / sample execution** to catch runtime errors before production.

CONSENSUS across every source found / DURABLE — ordinary defense-in-depth applied to a new untrusted-input
source, nothing LLM-specific about the underlying wisdom.

Execution-accuracy benchmarks: Spider frontier systems ~85%; BIRD (dirtier, more realistic schemas) ~75–82% vs. a
reported ~93% human baseline ([Datost](https://datost.com/blog/text-to-sql-accuracy-benchmarks)). The durable
lesson underneath: **real-world schema messiness, not linguistic query complexity, breaks text-to-SQL.**
BIRD-Interact (ICLR 2026, BIRD Team + Google Cloud + HKU) targets query *ambiguity* specifically — the field's
next acknowledged frontier. FAST-MOVING numbers / DURABLE qualitative lesson.

### 2.7 Guardrails / output-validation ecosystem (Q7)

**Guardrails AI** (open source, ~6.6–6.8k stars, 65+ Hub validators, reported 10k+ monthly downloads) provides
programmatic output validation with re-ask-on-fail logic. A maintainer discussion
([#1399](https://github.com/guardrails-ai/guardrails/discussions/1399)) surfaces a real tension: individual
community validators can go stale (a cited ban-list validator, no updates since Aug 2024) even while the core
engine stays maintained. CONTESTED / FAST-MOVING at the individual-validator level, more DURABLE at the
core-framework level — treat any specific Hub validator as needing its own currency check.

**NeMo Guardrails** (NVIDIA, v0.23.0, July 1 2026, 6.7k stars, 3,730 commits — actively developed) is commonly
paired with Guardrails AI in production (NeMo for dialog-state rails, Guardrails AI for output validation).
**Important, well-evidenced nuance**: NeMo's own docs confirm its "self-check facts" rail works by prompting an
LLM for yes/no entailment, and its "self-check hallucination" rail works via SelfCheckGPT-style multi-sample
consistency voting — **both are LLM-based, not deterministic**
([NVIDIA docs](https://docs.nvidia.com/nemo/guardrails/latest/configure-rails/guardrail-catalog/fact-checking.html)).
A team adopting "guardrails" believing they've added a hard safety layer may have added another LLM call with a
correlated failure mode to the one it's checking — the concrete evidentiary basis for the three-tier taxonomy in
§1. CONSENSUS (unambiguous official docs) / DURABLE structural fact.

**Promptfoo** was acquired by OpenAI (announced March 9, 2026) but remains open source; it is primarily a
red-teaming/adversarial-eval-generation and CI-assertion tool, not a runtime output-validation layer — it belongs
in the review/CI toolchain, not the production request path. FAST-MOVING (4-months-old consolidation event,
neutrality consideration for teams red-teaming OpenAI-family models specifically).

Provider-native grounding checks (§2.3/2.4) sit structurally between Guardrails-AI-style validators and
NeMo-style self-checks: a *separately-trained* classifier scoring a (source, query, response) triple, not the
same generative model grading its own work — meaningfully more independent than same-model self-check, though
still a learned model, not symbolic logic (except Bedrock Automated Reasoning checks, which is symbolic). This
three-way split — same-model self-check / independent learned classifier / symbolic-deterministic — organizes
the rubric below.

---

## 3. Candidate Decision Rubric — what a grounded-LLM-feature architecture must declare

For each LLM-generated claim or write, force explicit answers. Each item states a **default** and a **when-not**.

1. **Designated ground-truth source, named explicitly** — the specific table/view/index/document-set/API,
   ideally referenced from an existing data catalog rather than invented fresh.
   *Default*: one canonical source per claim-type, with a stated precedence order if multiple sources overlap.
   *When not*: greenfield prototypes with no catalog yet — still name the source; flag it as ungoverned rather
   than skipping the declaration.

2. **Freshness/staleness contract**: snapshot cadence, TTL, versioning, "as-of" semantics surfaced to the user.
   Ties to the reported 30–50% hallucination-rate reduction attributed to explicit document-validity windows and
   temporal metadata in enterprise RAG (aggregated industry commentary — FAST-MOVING number, DURABLE practice).
   *Default*: declare a max-staleness bound per source; block/flag responses grounded past it.
   *When not*: static reference data (a fixed regulatory table) can be declared unbounded.

3. **Check tier per claim-type** (the three-tier taxonomy, §1/§2.7):
   - Tier 1 (symbolic/deterministic — schema, FK/constraint, allowlist, encoded rule, formal-logic policy):
     **required** for anything that writes state, touches money/identifiers/dates, or is a regulated fact.
   - Tier 2 (independent learned classifier/NLI scorer — provider grounding API or dedicated NLI model, not the
     generating model): default for open-ended factual claims grounded in retrieved text, with a declared
     numeric threshold.
   - Tier 3 (same-model/family self-check or LLM-judge): reserved for genuinely subjective properties — never the
     sole gate for anything Tier 1/2 could cover.
   *When not*: low-stakes, internal-only, human-reviewed-before-any-effect features can justify Tier-3-only — as
   a stated, conscious exception.

4. **Faithfulness/groundedness threshold as an explicit number**, plus the operational meaning of crossing it:
   block, regenerate, auto-correct-and-flag, or route to human review. A threshold without a declared action is
   not a control.
   *Default*: start from observed defaults (Bedrock's example config at 0.7 grounding/relevance; RAGAS community
   convention clusters 0.7–0.8) and require justification for deviation.
   *When not*: exploratory/internal tools with a human always in the loop before any downstream effect.

5. **Fallback behavior on failed verification**, per feature: refuse (terminal — must not be silently retried
   against a different provider, per the consensus that policy-shaped refusals are terminal, not a 5xx),
   regenerate with a bounded retry budget, degrade to a cached-safe-default, or escalate to a human. Silence
   (shipping the ungrounded response anyway) is never acceptable.

6. **Provenance/audit requirement**: what's logged per grounded output — source rows/chunks used,
   citation-resolution status, check-tier scores/thresholds, model/schema version, admit/reject decision with
   reason — modeled conceptually as a PROV-style entity/activity/agent record, retained per domain need.
   *Default*: log enough to reconstruct "what grounded this output" after the fact, even without formal PROV
   tooling.
   *When not*: pure UX-copy with no factual claims and no downstream consequence.

7. **Write-path admission rule** for any state-mutating LLM output: schema check → referential/FK/lookup check →
   business-rule check → commit, enforced at a layer the LLM cannot bypass (DB constraints, read-only
   connections, code-level allowlists) — never prompt-only. State what happens to a rejected proposal.

8. **Citation contract**: is citation required; is resolution checked (deterministic, always should be); is
   span-level support checked (Tier 2/3); what happens with no valid citation (drop the claim, refuse, or flag) —
   declared, not implicit.

9. **Cross-provider portability note**: which provider-specific structured-output/grounding features are relied
   on, and what breaks on provider change — given confirmed schema-dialect non-portability across at least
   OpenAI/Anthropic.

---

## 4. Checkable-Teeth Candidates

Ranked by how directly a grader could apply the framework's "bite rule":

- **Named, specific ground-truth source per grounded claim-type** — grep-checkable (a table/view/index, not
  "our data"). Bite test: mutate the reference to something nonexistent; a reviewer/grader should flag it.
- **Explicit numeric threshold wherever a support/faithfulness/groundedness score is declared** — a bare score
  name with no number is a fail. Bite test: strip the number; the check should fail.
- **Explicit check-tier (1/2/3) per claim-type**, with Tier 1 confirmed for anything state-mutating — mechanically
  checkable against a simple rule ("any REQ involving a database write must name a deterministic
  constraint/allowlist check").
- **Read-only enforcement declared at connection/driver layer**, not "the prompt tells it not to write." Bite
  test: a prompt-only control fails by construction; a driver-level `read_only` flag or DB-permission boundary
  passes.
- **Fallback action named per failure mode** (refuse/retry/escalate/degrade) — absence is structurally
  detectable, akin to this framework's existing positive-presence HONORS checks.
- **Citation-resolution declared as deterministic** versus left ambiguous — a doc claiming "citations are
  verified" without separating resolution-is-deterministic from support-is-judged is under-specified and
  gradeable as such.
- **Audit/provenance retention declared with a duration or regulatory anchor** — bare "we log things" is
  gradeable as insufficient.
- **Portability note present whenever a provider-specific grounding/structured-output feature is used** —
  cross-referenceable absence.
- **Same-model self-check never declared as the sole gate for a state-mutating or Tier-1-eligible claim** —
  hardest to grade mechanically (requires classifying claims), but a plausible target for a fresh-context
  reconciler pass given the claim inventory from `01-planner`.

---

## 5. What Changed Since Early 2025

- **Schema enforcement went from "OpenAI/Gemini only" to table stakes, non-uniformly.** Anthropic didn't reach
  GA on structured outputs/strict tool use until November 2025, over a year after OpenAI. By mid-2026 most
  providers support some form of it (244-model third-party study), but cross-provider dialect portability remains
  unsolved.
- **Provider-native grounding-check services matured from roadmap/preview into production APIs with documented
  latency budgets.** Vertex's Check Grounding API (<500ms), Azure's groundedness detection (now with a
  "Reasoning mode" and a "correction" preview), and Bedrock's contextual grounding checks are all GA-grade,
  callable-per-inference primitives rather than offline-only tooling. Bedrock Automated Reasoning checks moved
  from a re:Invent 2024 gated preview toward broader availability — the first mainstream-cloud example of
  *symbolic*, not learned, verification of LLM output.
- **LLM-as-judge scholarship turned more skeptical and more rigorous.** Early-2025 practice largely accepted
  LLM-judges with light validation; by mid-2026 a large-scale study (21 judges, ~541K judgments, including
  April-2026-frontier models) hardened the finding that self-consistency is not validity, and that naive
  exact-match agreement systematically overstates judge quality.
- **Pre-LLM distributed-systems vocabulary (saga, transactional outbox, HITL commit-gating) started being
  explicitly repurposed for agentic write-safety** — barely begun in early 2025, producing its first serious
  academic formalization (ATP/Mnemosyne) only in July 2026. The field is visibly reaching for older
  distributed-systems rigor because ad hoc prompt-based guardrails kept failing.
- **Citation-verification research moved from "does it cite" to "does the citation support the specific claim,"**
  with hybrid retrieval-grounded verification agents (CiteGuard, April 2026) explicitly designed to move past
  pure LLM-as-judge citation checking.
- **Enterprise data-governance platforms began treating AI agents/models as first-class governed objects inside
  existing catalog tooling** (Databricks Unity AI Gateway, June 2026) rather than leaving "ground truth
  designation" a bespoke per-project discipline.

---

## 6. Contested Points Needing Designer Judgment

- **Whether to name a specific write-path pattern in the skill at all.** The mechanism is sound; no name is
  settled. Naming one (e.g., borrowing "admission gate" from ATP) risks authority-washing weeks-old vocabulary;
  staying purely descriptive risks feeling under-specified. Recommend: describe the mechanism, offer 2–3 analog
  names as non-canonical references, let the project choose its own term.
- **How hard to push the three-tier taxonomy as prescriptive.** Strong synthesis, solid evidence per rung, but
  it's this brief's synthesis, not an already-coined term. Treat as a recommended mental model to adapt, not
  vocabulary to mandate verbatim.
- **Numeric thresholds (0.7 grounding/relevance, etc.) are illustrative defaults observed in vendor examples and
  community convention, not a validated universal constant.** Different domains need different floors; the
  rubric should require a declared number, not prescribe a specific one.
- **How much of the provenance/audit requirement should point at W3C PROV formally** versus just requiring
  "enough logging to reconstruct what grounded this output." Full PROV adoption is likely overkill for most
  projects; the conceptual shape is worth teaching, the standard itself probably isn't worth mandating.
- **Whether NL→SQL guidance belongs in this craft module or a broader "agent tool-use safety" module.** The
  read-only-driver/allowlist findings are clean and durable, but are one instance of a more general "any
  LLM-driven mutation needs an infrastructure-level backstop" principle that also applies beyond SQL (file
  systems, external APIs, message queues). Scope boundary is a designer call.
- **Citation-hallucination base rates are too inconsistent to put a single number in the skill itself**
  (11–57% general RAG vs. 78–90% academic-citation-fabrication are different phenomena). Any worked example
  should either avoid a specific rate or clearly scope which phenomenon it illustrates.
- **Guardrails-Hub-style validator marketplaces are architecturally attractive but empirically uneven in
  upkeep.** "Use a validator hub" versus "write your own thin deterministic checks" is a velocity-vs-currency-risk
  call; evidence here favors treating any third-party validator as needing its own currency check, not
  blanket-trusting a hub's brand.

---

## 7. Source Registry

Official/vendor documentation:
- AWS, [Bedrock contextual grounding check docs](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html); [Automated Reasoning checks docs](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html) + [launch post](https://aws.amazon.com/blogs/machine-learning/minimize-generative-ai-hallucinations-with-amazon-bedrock-automated-reasoning-checks/); [Knowledge Bases retrieve-and-generate docs](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-retrieve-generate.html).
- Microsoft, [Groundedness detection in Azure AI Content Safety](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/groundedness) (`ms.date: 2025-11-21`, updated 2026-06-05).
- Google Cloud, [Check grounding with RAG](https://docs.cloud.google.com/generative-ai-app-builder/docs/check-grounding), fetched July 2026.
- Anthropic, [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), fetched July 2026.
- OpenAI, [Introducing Structured Outputs in the API](https://openai.com/index/introducing-structured-outputs-in-the-api/), Aug 2024 (vendor claim).
- NVIDIA, [NeMo Guardrails fact-checking docs](https://docs.nvidia.com/nemo/guardrails/latest/configure-rails/guardrail-catalog/fact-checking.html); [GitHub repo](https://github.com/NVIDIA-NeMo/Guardrails) v0.23.0, July 1 2026.
- Guardrails AI, [GitHub repo](https://github.com/guardrails-ai/guardrails); [maintainer discussion #1399](https://github.com/guardrails-ai/guardrails/discussions/1399); [`provenance_llm` validator](https://github.com/guardrails-ai/provenance_llm).
- Databricks, [Unity AI Gateway announcement](https://www.databricks.com/blog/ai-governance-data-ai-summit-2026-whats-new-unity-ai-gateway), June 16 2026.
- Snowflake, [TruLens open-source commitment](https://www.snowflake.com/en/blog/trulens-open-source-ai/); [TruLens MAINTAINERS.md](https://github.com/truera/trulens/blob/main/MAINTAINERS.md).
- Confident AI, [DeepEval GitHub](https://github.com/confident-ai/deepeval); [2026 changelog](https://deepeval.com/changelog/changelog-2026).

Academic (arXiv, dated by submission/revision):
- [Mnemosyne: Agentic Transaction Processing, arXiv:2607.00269v2](https://arxiv.org/html/2607.00269), July 5 2026.
- [JSONSchemaBench, arXiv:2501.10868](https://arxiv.org/pdf/2501.10868), Jan 18 2025 / rev. Feb 27 2025.
- [CiteGuard, arXiv:2510.17853v4](https://arxiv.org/html/2510.17853v4), Apr 13 2026.
- [CiteCheck, arXiv:2502.10881](https://arxiv.org/pdf/2502.10881), Feb 2025.
- [Attribution, Citation, and Quotation survey, arXiv:2508.15396](https://arxiv.org/pdf/2508.15396), Aug 2025.
- [Reliability without Validity, arXiv:2606.19544](https://arxiv.org/html/2606.19544v1), 2026.
- [Neither Valid nor Reliable?, arXiv:2508.18076](https://arxiv.org/abs/2508.18076), Aug 2025.
- [Wallat et al., Correctness is not Faithfulness in RAG Attributions](https://staff.fnwi.uva.nl/m.derijke/wp-content/papercite-data/pdf/wallat-2025-correctness.pdf), UvA, 2025.
- [From Agent Traces to Trust, arXiv:2606.04990v3](https://arxiv.org/html/2606.04990v3), 2026.
- [AuditWeave, arXiv:2607.09682](https://arxiv.org/html/2607.09682), 2026.

Independent/third-party and practitioner sources:
- [Requesty, 244-model structured-outputs compatibility test](https://www.requesty.ai/blog/structured-outputs-across-llm-providers-the-compatibility-mess), May 30 2026.
- Hamel Husain (with Shreya Shankar), [Using LLM-as-a-Judge For Evaluation](https://hamel.dev/blog/posts/llm-judge/); [LLM Evals: Everything You Need to Know](https://hamel.dev/blog/posts/evals-faq/), Jan 15 2026.
- Eugene Yan, [Evaluating the Effectiveness of LLM-Evaluators](https://eugeneyan.com/writing/llm-evaluators/).
- Tim Dietrich, [Before You Build an AI SQL Agent, Build the Safety Layer](https://timdietrich.me/blog/sql-agent-safety-architecture/).
- Rietta, [Protect Production SQL Databases from AI/LLM Agentic SQL Query Risks](https://rietta.com/blog/ai-sql-database-data-protection-read-replica/).
- Datost, [Text-to-SQL Accuracy Benchmarks](https://datost.com/blog/text-to-sql-accuracy-benchmarks).
- InfoQ, [Saga Orchestration for Microservices Using the Outbox Pattern](https://www.infoq.com/articles/saga-orchestration-outbox/).
- Zylos Research, [Agent Identity and Signed Provenance](https://zylos.ai/research/2026-04-25-agent-identity-provenance-signed-audit-trails/), Apr 25 2026.
- Saulius, [Ragas Metrics Explained](https://saulius.io/blog/ragas-rag-evaluation-metrics-llm-judge).
- ResearchGate, [Human-in-the-Loop at the Commit Point](https://www.researchgate.net/publication/404949852_Human-in-the-Loop_at_the_Commit_Point_Architectural_Patterns_for_Trustworthy_Agentic_AI_Deployment_in_Enterprise_Scheduling) — credibility contested, used only for the reversible/irreversible taxonomy idea.

Evidence note: every numeric claim is attributed to its source; where two sources disagreed on the same construct
(citation-hallucination rate; execution-accuracy benchmarks), both are reported with the discrepancy flagged
rather than averaged or silently picked.
