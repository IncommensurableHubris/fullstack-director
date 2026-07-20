# Model Migration Protocol — reserved doctrine (activity built on first need)

> **Doctrine-level spec only — the activity is deferred** (the CLI-generator deferral precedent). This file states
> *what* a model/provider migration requires and *why*, so that when the first project actually swaps a model the
> mechanism is designed, not improvised. Nothing here is wired into a skill's flow yet; the trigger and the artifact-
> map entry are below. Referenced by **06-release**'s model-swap gate (`references/deploy-verification.md` § model-
> facing changes) and **03-architect**'s `model-binding` ADR category.

## The core claim — a model swap is a full re-evaluation, not a config change

Swapping a model or provider (a changed model id / endpoint / SDK) looks like a one-line config change and is not one.
A model is **co-adapted** with its prompts, its tool-idioms, its output distribution, and its embedding space. **Evals
alone demonstrably miss co-adaptation regressions** — roughly **~15% of behavior diverges *outside* the eval
distribution**, where no existing case looks. So a swap requires the same re-evaluation rigor as a new build, plus a
staged rollout that watches for the divergence the evals cannot see.

## The playbook (shadow → classify → triage → canary → full)

1. **Shadow.** The **incumbent model still serves** production. The candidate runs in shadow on the same real inputs,
   tagged with **correlation IDs** so each candidate output pairs to the incumbent's for the same request. No user
   sees the candidate yet.
2. **Automated diff classification.** For each correlated pair, classify the candidate's output against the
   incumbent's into four buckets: **improvement · neutral · regression · novel** (a behavior neither model exhibited
   in the eval set — the co-adaptation surface). Automate the bulk; the classifier itself is validated (the judge >90%
   discipline).
3. **Triage the novel + regression behaviors.** The **novel** bucket is the point of the exercise — behaviors outside
   the eval distribution. Triage each: is it an acceptable change, a new capability to add a regression case for, or a
   regression to fix (prompt re-engineering, below)? Regressions block promotion until resolved or waived.
4. **Canary.** Route a **small traffic slice** to the candidate with live monitoring (the drift alerts 06's G9 wires);
   widen only while the classified regression rate stays under floor.
5. **Full.** Promote to 100% once canary holds; the incumbent stays as the instant rollback target.

## Two costs a swap always incurs (budget them up front)

- **Prompt re-engineering per model idiom — never a find-and-replace.** Prompts are tuned to a model's idioms (its
  system-prompt conventions, its tool-call format, its few-shot sensitivity). Porting them verbatim underperforms;
  re-engineer per the target model's idiom. (03's `model-binding` ADR records the binding.)
- **Embedding reindexing (RAG systems).** A different embedding model means a **different vector space** — the whole
  corpus must be **re-embedded and re-indexed**, and retrieval re-tuned (Precision/Recall@k). Budget the reindex time
  and cost; a half-migrated index silently degrades retrieval.

## EU AI Act (GPAI) — conditional, off by default

A GPAI/EU-AI-Act compliance checklist attaches to a migration **only when** `architecture-constraints.md` declares
**EU-market distribution** — documented, off by default. Do not run it for a project that has not declared EU scope.

## Trigger + status

- **Trigger to build the activity:** the **first project that swaps a model or provider** (06's model-swap gate fires
  and there is no migration activity to run), or an explicit user request to build it.
- **Status:** **reserved** — doctrine written, activity deferred. Listed under **Deferred activities** in
  [`artifact-map.md`](artifact-map.md). When built, the activity likely lands as a `06-release migrate` mode (or a
  small `shared/` harness) that executes the shadow→canary staging with the diff-classification report.
