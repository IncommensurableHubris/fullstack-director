# T6 — LLM Evals Method: Hamel Husain's Canon and the Wider Field (July 2026)

Research pillar: LLM evals best practice, anchored on Hamel Husain's method. Pure outside view — no
local repository files read. All findings sourced from live web fetches conducted 2026-07-16/18.

## 1. Executive Summary

- Hamel Husain and Shreya Shankar's method has a stable, citable canonical statement as of **2026-01-15**
  ("LLM Evals: Everything You Need to Know," hamel.dev) — CONSENSUS within the practitioner community
  their Maven course reaches (700+ engineers/PMs, self-reported), DURABLE at the lifecycle level:
  error-analysis-first, open/axial coding to saturation, binary pass/fail, empirically validated judges.
- Judge-validation math sharpened materially between the **2024-10-29** guide (precision/recall,
  "acceptable agreement," no named formula) and the **2026-01-15** FAQ (TPR/TNR against a disjoint
  held-out split, explicit 80%/90% bars, Rogan-Gladen bias correction with bootstrapped CIs) — the
  clearest "what changed" finding, CONSENSUS and now DURABLE since it has propagated into open tooling.
- **`evals-skills` (github.com/hamelsmu/evals-skills)** is real, active, and **MIT-licensed** — confirmed
  from the raw LICENSE file and GitHub API. Created 2026-03-01, last pushed 2026-06-10, 1,500 stars/148
  forks/5 open issues, **zero tagged releases**. Ships seven Claude Code/npx-installable skills that
  operationalize the FAQ as agent-followable procedures, with exact numeric bars (TPR/TNR>90% ideal,
  >80% floor) and a Rogan-Gladen formula matching the companion `ai-evals-course/judgy` package.
- Beyond Hamel: Shreya Shankar's own research ("Who Validates the Validators?"/EvalGen, UIST 2024) is the
  academic root of "criteria drift" — criteria can't be fully specified before seeing outputs — which the
  FAQ cites as the reason eval-driven development "generally" fails. Eugene Yan's 2024 work is
  task-specific-metrics-first and does **not** share Hamel's error-analysis-first emphasis — complementary,
  not identical.
- The field converges hard on: distrust ready-made metrics (BERTScore/ROUGE/generic "helpfulness"),
  validate every judge against human labels before trusting it, separate guardrails (inline, sync, cheap)
  from evaluators (async, expensive, non-blocking), and split CI (small, curated, deterministic-favored)
  from production (sampled, async, reference-free, CI-tracked). All CONSENSUS, all DURABLE.
- The builder-vs-verifier split has **partial, not full, external precedent**. Software engineering has a
  45-year-old "independence of testing" principle (Myers 1979; ISTQB) for the general shape. Hamel's
  method operationalizes independence mainly through **disjoint data splits** (train/dev/test) plus one
  accountable owner, not a separate human/context reviewer every run — though `eval-audit` is framed as a
  distinct, separable activity. A *fresh-context* reviewer is best supported analogically, via
  self-preference-bias research, not by any source describing that exact mechanism as established
  practice. Flag CONTESTED/novel-but-well-motivated.
- Dataset governance: a single domain expert ("benevolent dictator") or a Kappa-gated annotator pool owns
  labeling; outsourcing core annotation is "usually a big mistake"; production failures graduate into the
  CI set once error analysis confirms a new pattern. The graduation *mechanics* (approval, versioning)
  are left to the practitioner — principle, not procedure.
- Mutation testing (formalized since the 1970s) is the direct, durable precedent for "a grader only
  counts if a deliberately-wrong output makes it fail" — the evals field independently reinvented the
  same check as judge validation via labeled Fail cases plus data-leakage prohibitions.
- The sharpest CONTESTED fault-line, and the one most relevant to a framework mandating eval-first RED:
  **eval-driven development**. Hamel's FAQ says "generally no" (unbounded failure surface makes
  pre-written evaluators low-value) with a narrow known-constraint exception. A separate, vocal ecosystem
  (evaldriven.org, DeepEval, `awesome-eval-driven-development`) treats eval-first as default, while itself
  warning literal TDD doesn't transfer since LLM outputs are non-deterministic. Unresolved, not just
  under-documented.

## 2. Findings

Each finding is tagged **[CONSENSUS/CONTESTED]** and **[DURABLE/FAST-MOVING]**.

**F1. Error analysis is the entry point, not automated metrics.** "Error analysis is the most important
activity in evals. Error analysis helps you decide what evals to write in the first place" — Husain &
Shankar, *LLM Evals FAQ*, hamel.dev, 2026-01-15. Reported budget allocation: 60–80% of dev time.
**[CONSENSUS, DURABLE]** — echoed by Eugene Yan's independent 2024 argument that off-the-shelf evals
"don't correlate with real performance" (eugeneyan.com/writing/evals/, March 2024).

**F2. Open coding → axial coding → theoretical saturation comes directly from grounded-theory
qualitative research.** Glaser & Strauss, *The Discovery of Grounded Theory* (1967), is the academic
origin. The FAQ names this lineage explicitly and gives a rule of thumb: review ≥100 traces; stop when
~20 more surface no new category. **[CONSENSUS, DURABLE]** — 59-year-old methodology; LLMs change what's
coded, not the inductive-coding logic itself.

**F3. Binary pass/fail beats Likert scales for the initial evaluation layer.** FAQ, 2026-01-15: "Binary
evaluations force clearer thinking... annotators often default to middle values to avoid making hard
decisions." **[CONSENSUS for product evals, CONTESTED at the margin, DURABLE]** — pairwise/Elo comparison
remains standard for model-vs-model leaderboards (a use case the FAQ doesn't address), and some
enterprise dashboards still default to multi-point scales.

**F4. LLM judges must be empirically validated with TPR/TNR against a disjoint, held-out labeled split
before being trusted — and even then, production estimates need bias correction.** FAQ, 2026-01-15:
"Focus on achieving high True Positive Rate (TPR) and True Negative Rate (TNR)... you can correct [the
judge's] estimates to determine the actual failure rate." Operationalized in
`hamelsmu/evals-skills/skills/validate-evaluator/SKILL.md` (fetched 2026-07-18): train 10–20%/dev
40–45%/test 40–45% split, target TPR/TNR>90%, floor >80%, ~100 labeled examples (50 Pass/50 Fail, CIs
widen sharply below 60), Rogan-Gladen correction `theta_hat = (p_obs + TNR - 1) / (TPR + TNR - 1)` —
matching the companion package `ai-evals-course/judgy` (MIT, 91 stars, bootstrap CI). **[CONSENSUS,
DURABLE for the validation requirement; FAST-MOVING for the specific tooling]** — recent academic papers
converge on the same correction family independently of the course: "How to Correctly Report
LLM-as-a-Judge Evaluations" (arXiv:2511.21140, Nov 2025) and "Bias and Uncertainty in LLM-as-a-Judge
Estimation" (arXiv:2605.06939, May 2026). The underlying Rogan-Gladen estimator is a 1978 epidemiological
misclassification-correction method — durable statistics, freshly re-applied to this domain.

**F5. Guardrails and evaluators are architecturally distinct.** Guardrails: inline, synchronous,
millisecond-latency, deterministic, block/redact/regenerate, false positives = production bugs.
Evaluators: asynchronous, can be expensive (LLM-as-judge), feed dashboards/regression tests, never block
the response. FAQ, 2026-01-15. **[CONSENSUS, DURABLE]** — architecture, not fashion; every platform
reviewed (LangSmith, Arize Phoenix, Braintrust, W&B Weave) implements some version of it.

**F6. CI and production evaluation use different data regimes.** CI: small (order 100+), hand-curated,
regression-anchored, favors deterministic checks because tests run on every change. Production: sampled
live traffic, evaluated asynchronously, reference-free evaluators (LLM-as-judge) acceptable because
ground truth is absent, confidence intervals tracked, investigate when the lower bound crosses threshold.
FAQ, 2026-01-15. **[CONSENSUS, DURABLE at the architecture level; FAST-MOVING in implementation]** — 2026
CI-gate commentary (delta-gates with Welch's t-test, classifier-cascade-before-frontier-judge to control
per-PR cost) is landscape-level vendor/practitioner blogging, not first-party Hamel guidance — read as
*pattern class* only (https://futureagi.com/blog/ci-cd-llm-eval-github-actions-2026/, 2026).

**F7. Same-model-as-judge is empirically acceptable if validated — but is a live bias-research
concern.** FAQ, 2026-01-15: "using the same model is usually fine... what ultimately matters is how well
your judge aligns with human judgments." Contrast: Zheng et al., "Judging LLM-as-a-Judge with MT-Bench
and Chatbot Arena," NeurIPS 2023/arXiv:2306.05685 (canonical origin of documented position, verbosity,
self-enhancement bias), plus replications — "Self-Preference Bias in LLM-as-a-Judge" (arXiv:2410.21819,
Oct 2024) and "Beyond the Surface" (arXiv:2506.02592, June 2025). **[CONTESTED, DURABLE as a
phenomenon]** — both camps require validation against held-out human labels; they differ on how much
prior suspicion same-model judging deserves before that validation.

**F8. Custom-built annotation tooling is recommended over off-the-shelf platforms.** FAQ, 2026-01-15:
"I often find that teams with custom annotation tools iterate ~10x faster." **[CONTESTED, FAST-MOVING]**
— Hamel's own anecdotal claim (self-reported, not independently benchmarked), and it conflicts with the
commercial interest of every eval-platform vendor. His own answer to "favorite eval vendor" (same FAQ) is
candidly vendor-agnostic ("it's mainly the human factor... vibes") — itself evidence this is a judgment
call, not a settled fact.

**F9. Outsourcing core error-analysis annotation is discouraged by default.** FAQ, 2026-01-15: superficial
labeling, loss of tacit domain knowledge, and annotation-conflict risk are the stated failure modes.
Exceptions: purely mechanical tasks, tasks without product context (translation), and hiring
subject-matter experts *as* internal reviewers (e.g. AnkiHub hiring medical students to grade a medical
RAG system — not outsourcing). **[CONSENSUS, DURABLE]** — aligns with F2's finding that domain expertise
is inseparable from valid coding of failure data.

**F10. RAG evaluation splits cleanly into retrieval (IR metrics) and generation (validated judges).**
FAQ, 2026-01-15, citing Liu, "There Are Only 6 RAG Evals" (jxnl.co, 2025-05-19): retrieval scored with
Recall@k/Precision@k/MRR against synthetic reverse-generated query–document pairs; generation scored via
the same error-analysis → judge → TPR/TNR pipeline, on Question|Context, Answer|Context (faithfulness),
Answer|Question (relevance). **[CONSENSUS on the split, CONTESTED on tooling defaults, DURABLE at the
framework level]** — RAGAS-style libraries ship similar tiers with fixed thresholds (faithfulness
~0.75–0.85, context precision ~0.7, recall ~0.8 — 2026 blog figures, FAST-MOVING/vendor-flavored), but
Hamel's position is that *any* ready-to-use metric needs the same validation before trust — tension with
"install RAGAS, read the score."

**F11. Eval-driven development is explicitly rejected as a default.** FAQ, 2026-01-15: "Generally no...
LLMs have infinite surface area for potential failures. You can't anticipate what will break." Exception:
known, fully-specified constraints stated up front (e.g., "never mention competitors"). Root
justification cited in-text: Shankar et al., "Who Validates the Validators?" (UIST 2024/arXiv:2404.12272,
April 2024) — "criteria drift": people cannot fully externalize evaluation criteria before seeing
outputs. **[CONTESTED, live and unresolved]** — a competing ecosystem treats eval-first as default:
evaldriven.org, DeepEval's "Eval Driven Development" framing, `awesome-eval-driven-development`, all
promoting writing evals before/alongside implementation while themselves warning literal TDD doesn't
transfer (LLM outputs are non-deterministic). The sharpest disagreement found in this research pass.

**F12. Independent verification of test/eval quality has 45+ years of software-engineering precedent,
but not in the exact "isolated LLM context" form.** Glenford Myers (1979) formalized separating debugging
from testing; ISTQB's CTFL formally defines "independence of testing" as separating tester/developer
roles "to avoid conflict of interest." Mutation testing (same lineage, decades-old, still active) is the
direct precedent for "a check only counts if it fails on a deliberately broken input" — the bite rule's
shape. **[CONSENSUS on the general principle, DURABLE]**. Not precedented: Hamel's method achieves
independence mainly through disjoint *data* (train/dev/test, no few-shot leakage) plus one accountable
owner, not a separate reviewer re-running floors from a fresh context every release. The closest analog,
`eval-audit`, is pitched for "when inheriting a system, when unsure whether evals are trustworthy" — an
occasional/triggered audit, not a mandatory per-release gate. **[CONTESTED / novel]**.

**F13. Dataset governance: ownership is explicit, graduation mechanics are not.** FAQ, 2026-01-15:
ownership defaults to a single domain expert; multi-annotator setups require Cohen's Kappa-measured
agreement and an alignment-session process before disagreements are resolved. Production→CI graduation:
"when production monitoring reveals new failure patterns... add representative examples to your CI
dataset." No approval workflow or versioning scheme is specified. **[CONSENSUS on ownership,
silent/CONTESTED on procedure, DURABLE principle/FAST-MOVING procedure]** — landscape "data flywheel"
content (vendor blogs: Arthur.ai, Galileo, Towards AI, 2026) converges on the same shape independently
(production failure → triage → minimal repro → golden set → CI gate) but is vendor-flavored, read as
corroboration not authority.

**F14. The book is real, in Early Release, not yet finalized.** *Evals for AI Engineers: Systematically
Measuring and Improving AI Applications*, Shreya Shankar & Hamel Husain, O'Reilly. Confirmed via
O'Reilly's own listing (two chapters live) and Amazon (ISBN 9798341660724). Early Release = author's raw,
in-progress text; full publication was reported in search results as targeting **2026-10-31**, which this
research could not independently confirm — secondary-source only, treat as provisional.

## 3. The Method as a Lifecycle

**Phase 0 — Instrument.** Capture the full trace (every turn, tool call, retrieval, intermediate
reasoning step) — not just input/output pairs. Never skippable; a prerequisite, not a phase with a
stopping condition.

**Phase 1 — Error analysis (the core activity).**
1. *Assemble a dataset*: real traces if available; otherwise structured synthetic data — define 3+
   orthogonal dimensions of variation (e.g. dietary restriction × cuisine × complexity), hand-seed ~20
   tuples to build intuition, then scale via cross-product-then-LLM-filter (guarantees coverage) or
   direct LLM tuple generation (more realistic, misses rare cases), converting tuples to natural language
   in a separate step to avoid repetitive phrasing. When-not to trust synthetic data: complex
   domain-specific content (legal/medical), low-resource languages, anything unverifiable, high-stakes
   domains, underrepresented user groups — use real data or heavy manual validation instead.
2. *Open coding*: one domain expert ("benevolent dictator") free-writes notes on traces, focused on the
   first upstream failure per trace initially (downstream failures usually cascade from it). Never
   delegated to an LLM or outsourced — this is where tacit product/domain knowledge gets externalized.
3. *Axial coding*: cluster the open notes into a named failure taxonomy with counts. LLM-assisted
   first-pass clustering is acceptable *after* 30–50 traces are human-coded, but a human must
   review/refine every grouping — LLMs conflate distinct failure modes (e.g., merging a stability bug
   with a performance complaint under one "login issues" label).
4. *Iterate to theoretical saturation*: keep adding traces until new ones stop revealing new categories.
   Rule of thumb: review at least 100 to start; stop once ~20 additional traces add nothing new. Re-run
   the whole cycle on a 2–4 week cadence or on trigger (model swap, prompt rewrite, bug fix, incident,
   complaint spike, metric drift); light 10–20-trace weekly spot-checks fill the gaps between cycles.

**Phase 2 — Triage before automating.** Many findings are simple spec/prompt bugs — fix immediately, no
evaluator needed. Only promote a failure mode to "build an automated check" after a cost-benefit
judgment (will this recur?). When-not: don't build an evaluator for every failure mode found; most value
is in the fix, not the metric.

**Phase 3 — Build evaluators, cost-ordered.** Prefer deterministic/code-based checks (assertions, regex,
schema validation, execution tests) wherever objectively checkable — cheap, fast, no maintenance
overhead. Reserve LLM-as-judge for genuinely subjective/generalization failures that persist after
prompt fixes; seed the judge prompt from the domain expert's own critiques (Phase 1) as few-shot
examples. When-not: don't default to LLM-judge when a code check would do; don't practice eval-driven
development except for a small number of fully-known, non-negotiable constraints declared up front.

**Phase 4 — Validate the judge statistically.**
1. Split labeled data into disjoint train (10–20%, few-shot seeds) / dev (40–45%, prompt iteration) /
   test (40–45%, touched only for final measurement) — never let dev/test examples leak into few-shot
   prompts.
2. Measure TPR and TNR against the held-out test split — not raw accuracy or agreement, which mislead
   under class imbalance.
3. Bar: aim for TPR>90%/TNR>90%; treat TPR>80%/TNR>80% as a floor. Below floor: try a more capable judge
   model, decompose the criterion into smaller atomic checks, re-examine human-label consistency, or fall
   back to human review for that dimension.
4. When scoring unlabeled production data with an imperfect-but-validated judge, bias-correct the
   observed pass rate using the measured TPR/TNR (Rogan-Gladen-style correction) and report a bootstrapped
   confidence interval — never a bare uncorrected percentage. When-not: don't skip validation because a
   judge "seems reasonable" in spot checks; don't report a dev-set score as final accuracy.

**Phase 5 — Deploy in two distinct regimes, plus guardrails as a third.**
CI/CD: small (order 100+), hand-curated, regression-anchored, covering core features/past-bug
regressions/known edge cases; favor deterministic checks since tests run on every change. Production
monitoring: sample live traffic asynchronously; reference-free evaluators (validated LLM-judges)
acceptable since ground truth is absent; track confidence intervals; investigate when the lower bound
crosses a defined threshold. Guardrails (architecturally separate): inline, synchronous, millisecond
budget, deterministic, block/redact/regenerate on trigger — promote an evaluator to guardrail status only
if it's cheap enough and the false-positive/false-negative cost asymmetry favors blocking (e.g., medical
false negatives outweigh false positives; creative-writing false positives outweigh occasional misses).

**Phase 6 — Close the loop (governance).** When production error analysis confirms a new failure pattern,
add a representative example to the CI regression set so the fix stays fixed. Ownership of additions
follows the initial-labeling rule — the domain-expert owner or an aligned annotator pool, not
ad hoc/outsourced contributions.

**Phase 7 — Periodically re-audit the pipeline itself**, distinct from running it: check for stale
taxonomies, unvalidated judges, data leakage, generic-metric theater, and Likert-scale drift. A separate
activity (Hamel's toolset names it `eval-audit`), triggered by inheriting a system, doubting its
trustworthiness, or a periodic cadence — not folded into ordinary error-analysis cycles.

## 4. Checkable-Teeth Candidates

Concrete, mechanically verifiable checks a framework could run against a project's eval artifacts,
each traceable to a finding above:

1. **Taxonomy provenance**: a documented failure taxonomy exists, built from ≥100 real-or-synthetic
   traces, with named categories and counts — not brainstormed generic labels ("hallucination,"
   "toxicity"). (F1, F2; lifted from the `eval-audit` skill's own checklist.)
2. **Binary-scale enforcement**: every grader's schema declares pass/fail (or independent binary
   sub-checks), not a 1–5/Likert field. (F3.)
3. **Split disjointness / no leakage**: for every LLM-judge evaluator, few-shot example IDs are disjoint
   from dev/test-split IDs used to report TPR/TNR — a mechanical set-intersection test. (F4.)
4. **Numeric judge bar met**: TPR/TNR (not raw accuracy/agreement %) reported against a held-out test
   split, clearing a stated floor (default candidate: 80/80, target 90/90). (F4 — flag that this exact
   number is Hamel/Shreya-sourced, not multi-source consensus; see §6.)
5. **Bias-corrected production reporting**: any judge-derived production pass-rate is reported with a
   TPR/TNR correction and a confidence interval — never a bare percentage. (F4.)
6. **Bite rule / mutation check**: every grader has ≥1 labeled "should-Fail" example and actually fails
   it when run — precedented by mutation testing's "kill the mutant" criterion. (F12.)
7. **Mandatory negatives present**: the eval set contains a nonzero count of adversarial/unanswerable
   cases, not only happy-path positives — a simple category-count > 0 gate. (Hamel's
   answerable/unanswerable balanced-set requirement.)
8. **Cost-hierarchy rationale**: each evaluator is tagged code-based vs. LLM-judge, with judge usage
   accompanied by a documented reason a deterministic check wasn't sufficient. (F1, Phase 3.)
9. **CI/production separation**: a small curated CI dataset (size floor ≥100) is distinct from the
   production-sampling process, with a traceable "graduation" link for every CI example sourced from a
   production failure. (F6, F13.)
10. **Re-run cadence recorded**: taxonomy/evaluator artifacts carry a last-reviewed timestamp checked
    against defined triggers (model swap, prompt rewrite, incident, drift alert). (Phase 1 step 4.)
11. **Reviewer/context provenance**: a floor re-run's record attests *which* context produced it (fresh
    vs. authoring session) — though per F12 this pattern has no established name outside this framework.
12. **Ownership field on the golden set**: every example records who approved it (named owner, or
    annotator-pool member under a Kappa-gated rubric) — field-presence, not unattributed. (F9, F13.)

## 5. What Changed Since Early 2025

- **Judge validation went from qualitative (agreement, precision/recall, case-by-case judgment) to
  quantitative-and-named (TPR/TNR against disjoint splits, explicit numeric bars, a named bias-correction
  formula with bootstrapped CIs).** Compare the 2024-10-29 LLM-judge guide (no TPR/TNR, no Rogan-Gladen,
  no package) against the 2026-01-15 FAQ and the `evals-skills`/`judgy` tooling now implementing it in
  code — the single largest concrete shift found.
- **The method got packaged for AI coding agents specifically.** `evals-skills` (created 2026-03-01) is a
  direct response to agentic coding tools — Hamel's framing cites OpenAI's finding that "improving the
  infrastructure around the agent mattered more than improving the model." A new distribution channel
  (Claude Code/npx skill packs), not a change to the method's content.
- **Active self-correction of the reference implementation is still happening in mid-2026.** Commits as
  late as 2026-06-10 fix a wrong Rogan-Gladen-denominator explanation and a `judgy` API example
  referencing nonexistent kwargs — the tooling layer is still immature, four months after publication.
- **Academic corroboration of judge bias-correction arrived independently and later.** arXiv:2511.21140
  (Nov 2025) and arXiv:2605.06939 (May 2026) apply the same correction family without citing Hamel/Shreya
  — convergent discovery, raising this from "one course's opinion" to independently-corroborated within
  12 months.
- **RAG framing consolidated around a shared taxonomy.** Jason Liu's "There Are Only 6 RAG Evals"
  (2025-05-19) is now the FAQ's own cited framework as of Jan 2026 — the field converged on a shared
  retrieval/generation decomposition within 14 months, replacing more ad hoc 2023–2024 RAG-eval advice.
- **Eval-driven development hardened into an explicit, named rejection**, citing Shankar's criteria-drift
  finding — reads as a direct response to a full year (2025) of a competing "EDD/TDD-for-LLMs" ecosystem
  gaining traction. The disagreement is now explicit and mutual, not two camps working in isolation.
- **"Is RAG dead?" entered the FAQ as a named, addressed question** — evidence a 2025 wave of "agentic
  search replaces RAG" commentary was widespread enough to require correcting the record: the viral claim
  was narrowly about naive vector search in coding agents, not RAG as a category.

## 6. Contested Points Needing Designer Judgment

1. **Eval-driven development vs. error-analysis-first as the mandatory entry point.** The sharpest,
   most consequential fault-line found (F11), and directly relevant to any framework gating a builder on
   "see a failing eval case before fixing." Hamel's position: rare and exception-based, not default,
   because criteria drift makes pre-specified evaluators for unobserved failures low-value. A designer
   must decide whether "eval-first" means writing the RED case for a *known, already-observed* failure
   before fixing (compatible with Hamel) or writing evals *before building the feature at all* (the
   position Hamel argues against) — easy to conflate, worth stating explicitly.
2. **Data-split independence vs. context/reviewer independence** as the mechanism for "the judge isn't
   grading itself." Hamel gets independence from disjoint train/dev/test data plus a single accountable
   owner. An isolated-fresh-context reviewer is stronger and less-precedented, best justified by analogy
   to self-preference-bias research (F7, F12) — a reasonable extension, not documented practice.
3. **Golden-set editing rights: single benevolent dictator vs. multi-annotator governance.** Hamel
   defaults to one named owner, reserving Kappa-gated multi-annotator process for large/multi-domain
   orgs. Regulated/high-stakes domains (the same ones where Hamel distrusts synthetic data) plausibly
   need the heavier model by default — a stakes-dependent call the source doesn't resolve.
4. **Numeric bars (TPR/TNR 80/90, ≥100 traces, ≥50/50 calibration) are one practitioner lineage's
   operationalization, not a triangulated field standard.** Internally consistent and implemented in
   open-source tooling (`evals-skills`, `judgy`) — an excellent default, but no independent second
   source proposes the same numbers. Strong prior, override-able by domain risk, not gospel.
5. **Same-model-as-judge permissibility.** Hamel: fine if empirically validated. Bias literature:
   several replicated papers (2023–2025) show measurable self-preference effects. Both camps require
   validation; they diverge on whether to default-flag or default-block same-model judging pending it.
6. **Ready-made RAG/generic metric libraries (RAGAS-style) as scaffolding vs. banned by default.**
   Landscape practice treats a metrics library as the RAG-eval starting point; Hamel's repeated position
   is that *any* unvalidated ready-to-use metric creates "false confidence" — a framework must choose.
7. **Proportionality of process.** The reported 60–80%-of-dev-time-on-evaluation ratio comes from
   consulting engagements at a particular scale/stakes level; the source gives no scaling rule for
   smaller or lower-stakes projects.
8. **When synthetic golden-set data is admissible.** Hamel names domain-conditioned exceptions
   (high-stakes, low-resource-language, unverifiable, underrepresented-group content) qualitatively;
   a mechanical gate needs a designer-chosen risk-tagging scheme the source doesn't supply.

## 7. Source Registry

| # | Source | Date | Type |
|---|---|---|---|
| 1 | Husain & Shankar, "LLM Evals: Everything You Need to Know" (FAQ, PDF fetched in full), hamel.dev/blog/posts/evals-faq/ | 2026-01-15 | Primary, practitioner |
| 2 | Husain, "Using LLM-as-a-Judge For Evaluation," hamel.dev/blog/posts/llm-judge/ | 2024-10-29 | Primary, practitioner |
| 3 | Husain, "The Revenge of the Data Scientist," hamel.dev/blog/posts/revenge/ | 2026-03-26 | Primary, practitioner |
| 4 | Husain, "Your AI Product Needs Evals," hamel.dev/blog/posts/evals/ | 2024-03-29 | Primary, practitioner |
| 5 | Husain, "Evals Skills for Coding Agents," hamel.dev/blog/posts/evals-skills/ | 2026-03 | Primary, practitioner |
| 6 | GitHub `hamelsmu/evals-skills` (README, LICENSE, commits, API metadata) | Created 2026-03-01; pushed 2026-06-10; fetched 2026-07-18 | Primary, code artifact |
| 7 | GitHub raw `skills/validate-evaluator/SKILL.md`, `skills/eval-audit/SKILL.md` | Fetched 2026-07-18 | Primary, code artifact |
| 8 | GitHub `ai-evals-course/judgy` | Fetched 2026-07-18 | Primary, code artifact |
| 9 | Shankar et al., "Who Validates the Validators?" (EvalGen), UIST 2024/arXiv:2404.12272 | 2024-04 | Primary, academic (peer-reviewed) |
| 10 | Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena," NeurIPS 2023/arXiv:2306.05685 | 2023-06 | Primary, academic (peer-reviewed) |
| 11 | Yan, "Task-Specific LLM Evals that Do & Don't Work," eugeneyan.com/writing/evals/ | 2024-03 | Primary, practitioner (independent) |
| 12 | Liu, "There Are Only 6 RAG Evals," jxnl.co | 2025-05-19 | Primary, practitioner |
| 13 | O'Reilly, "Evals for AI Engineers" listing + ch.1–2 | Early Release, fetched 2026-07-18 | Primary, publisher |
| 14 | Amazon listing, ISBN 9798341660724 | Fetched 2026-07-18 | Secondary, retailer |
| 15 | "How to Correctly Report LLM-as-a-Judge Evaluations," arXiv:2511.21140 | 2025-11 | Primary, academic |
| 16 | "Bias and Uncertainty in LLM-as-a-Judge Estimation," arXiv:2605.06939 | 2026-05 | Primary, academic |
| 17 | "Self-Preference Bias in LLM-as-a-Judge," arXiv:2410.21819 | 2024-10 | Primary, academic |
| 18 | "Beyond the Surface: Measuring Self-Preference in LLM Judgments," arXiv:2506.02592 | 2025-06 | Primary, academic |
| 19 | Glaser & Strauss, *The Discovery of Grounded Theory* (secondary summaries) | 1967 origin; fetched 2026-07-18 | Secondary summary of primary source |
| 20 | Myers (1979) debugging/testing separation; ISTQB CTFL "independence of testing" (secondary summaries) | 1979 origin; standard ongoing | Secondary summary of a formal standard |
| 21 | Mutation testing — Wikipedia; Thoughtworks Technology Radar | Long-standing; fetched 2026-07-18 | Secondary/tertiary, established technique |
| 22 | Rogan & Gladen misclassification estimator, *Am J Epidemiol* (via arXiv:2605.06939 and judgy/evals-skills) | 1978 origin | Background, corroborated by 3 implementations |
| 23 | evaldriven.org; DeepEval "Eval Driven Development" blog; `awesome-eval-driven-development` | Fetched 2026-07-18 | Landscape/vendor + community |
| 24 | Laminar/Braintrust 2026 platform-comparison blogs (LangSmith/Arize/Braintrust/Weave) | 2026 | Landscape/vendor — pattern class only |
| 25 | qaskills.sh, futureagi.com — RAGAS thresholds, CI/CD delta-gate patterns | 2026 | Landscape/vendor blog content |
| 26 | Arthur.ai, Galileo, Towards AI — "data flywheel" / golden-dataset posts | 2026 | Landscape/vendor, corroboration only |

Evidence-discipline note: rows 24–25 and the RAG-threshold figures in F10 are vendor/blog landscape data,
excluded from best-practice-authority status and reported only as pattern-class/corroborating color. All
numeric bars presented as defaults (F4, checkable-teeth #4) trace to Hamel/Shreya's own course-lineage
tooling, not independent multi-source triangulation — flagged both inline and in §6.
