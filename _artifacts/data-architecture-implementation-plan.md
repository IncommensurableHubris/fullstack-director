# Data-Architecture Craft Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
> **This repo's continuation prompt (`_artifacts/data-architecture-continuation.md`) recommends inline
> `executing-plans` — the tasks are sequential doctrine edits where voice coherence across sections matters.**

**Goal:** Land the data-architecture craft in `03-architect` (four pillars, trigger-gated) + the E1 evals
workstream, exactly per the approved design record [`data-architecture-design.md`](data-architecture-design.md)
(commit `275096a`).

**Architecture:** One new reference (`data-architecture.md`, §0–§6) authored pillar-by-pillar from the committed
research synthesis; then wiring commits (03 routing + teeth, shared registry + capability, cross-seat E1 edits);
then a deterministic verification sweep; finally the full calibrated-suite regression bridge as a user-gated phase.

**Tech Stack:** Markdown doctrine files · git · grep-based verification · the existing calibrated eval suite
(`.agents/skills/03-architect/evals/` — READ-ONLY) as the regression bridge.

## Global Constraints

- **NEVER create/edit/delete anything under `.agents/skills/03-architect/evals/**`** — the calibrated regression
  suite is read-only for this initiative (hard guardrail; new data-craft eval cases are a separate follow-up).
- **Never `git push`. Never create a remote.** The repo has zero remotes by design.
- **Criteria, not winners:** vendor/product names may appear ONLY inside `data-architecture.md` §6 (the stamped
  appendix). Verification grep in Task 9 enforces this over the full diff.
- **Teeth text is contractual:** DA-T01–T08 wording comes verbatim from the design record §5 (reproduced in the
  tasks below) — do not paraphrase IDs or requirements.
- **Voice:** FD's own voice; shared files cited repo-root-relative (`shared/<file>`),
  a skill's own files skill-root-relative (`references/<file>`); no `../` escapes.
- **Framework-original flags:** the three-tier check taxonomy, the use-time-research step, the Review-Trigger
  field, and the fresh-context verifier are marked framework-original/adopted-synthesis where introduced.
- **Commits:** one per task, repo message style (`feat(03-architect): …` / `docs(…): …`), ending with
  `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`. `_artifacts/**` files need `git add -f`.
- **Sources for section content:** `_artifacts/data-architecture-research.md` (§2 conclusions C1–C6, §3 pillar
  cores, §4 dispositions, §9 evals) + the briefs in `_artifacts/research/`. The reference distills; it never
  copies brief prose wholesale, and never carries a contested number as a constant (register §4: items 1–5, 10).

---

### Task 1: `data-architecture.md` — skeleton + §0 need-gate + §1 datastore selection

**Files:**
- Create: `.agents/skills/03-architect/references/data-architecture.md`

**Interfaces:**
- Produces: the file's section anchors (`## §0`-style headers listed below) that Tasks 2–5 append under; the
  `DA-T04` clause text Task 6's reconcile pointer cites; the need-gate doctrine sentence Tasks 2–4 reuse by
  reference (never restate).

- [ ] **Step 1: Read the sources** — `_artifacts/data-architecture-research.md` §2 (C1–C6) + §3.P1 + §6 wiring
  map; skim `_artifacts/research/T1-datastore-selection.md` §3 (rubric) + §4 (teeth).

- [ ] **Step 2: Write the file skeleton + header + §0 + §1.** Exact skeleton (H1 + doc-quote header stating: loaded
  by 03 `init` for §1 always; §2/§3/§4 load only when the spine's `Data:` line declares their trigger — registry:
  `shared/agentic-profile.md`; §5 applies to any pillar; §6 is reference-only):

  ```markdown
  # Data-architecture craft — selection · retrieval · grounding · memory

  ## The need-gate (§0)
  ## Datastore selection (§1 · always-on at init)
  ## Retrieval (§2 · module: `Data: retrieval(<capability>)`)
  ## Grounding & verification-against-data (§3 · module: `Data: grounded-writes(<capability>)`)
  ## Agent memory (§4 · module: `Data: memory`)
  ## Volatile-decision classes + use-time research (§5)
  ## Landscape appendix (§6 · dated — verify at use time)
  ```

  **§0 must state (3–6 lines):** every module opens with "do you need this at all"; the resulting ADR cites which
  trigger fired; no fired trigger ⇒ absence is correct, not a gap; the deterministic pairing checks DA-T01–03 run
  in Pass 1 (`references/reconcile-architecture.md` §1b); the content-clauses DA-T04–08 live in this file's
  per-pillar teeth blocks and are reconciler-cited like the topology clause.

  **§1 mandatory elements:** the 7-dimension leverage-ordered rubric as a numbered list, each with default +
  when-not — (1) workload shape (OLTP/OLAP/HTAP) · (2) data-model fit (relational default; extension-hosted
  secondary patterns must name the specific mechanism) · (3) consistency via PACELC not CAP (deviations name the
  specific product requirement) · (4) scale envelope (symptom-based triggers — autovacuum lag, single-table I/O
  saturation — never a fixed GB/row number) · (5) operational maturity & cost (managed default below a
  platform-team threshold) · (6) team skill / choose-boring bias · (7) exit/migration cost (always recorded, even
  as "accepted because X"); the default posture line (relational + extensions; split only at a **named breakpoint
  class**: sustained write throughput past single-primary · true multi-region active-active · multi-TB analytical
  scans · vector search past tens-of-millions under strict SLAs · deep multi-hop graph traversal); the embedded-
  OLAP middle rung; the LLM-app reweighting note (traces/JSONB · co-located vectors · semantic cache ·
  queue-before-async-inference — reweights existing categories, invents none); the **§1 teeth block** with this
  verbatim clause:

  ```markdown
  **DA-T04 — a datastore ADR REQUIRES:** ≥2 named alternatives · the decisive driver mapped to a rubric dimension
  **and** a REQ-ID · a symptom-based **Review-Trigger** · an exit-cost statement · the durable commitment and the
  vendor pick stated as two separate decisions. An ADR missing these is an incomplete decision — the reconciler
  flags it (the `topology`-clause pattern).
  ```

- [ ] **Step 3: Verify structure.** Run:
  `grep -c "^## " .agents/skills/03-architect/references/data-architecture.md` → Expected: `7`.
  `grep -n "DA-T04" .agents/skills/03-architect/references/data-architecture.md` → Expected: 1 hit in §1.

- [ ] **Step 4: Product-name spot check** (core sections must be clean; §6 doesn't exist yet):
  `grep -niE "pinecone|weaviate|qdrant|milvus|turbopuffer|lancedb|neon|supabase|planetscale|mem0|letta|zep|langmem|cohere|voyage" .agents/skills/03-architect/references/data-architecture.md` → Expected: no matches.
  (PostgreSQL/DuckDB *class* references in §1's posture line are allowed as engine-class exemplars ONLY if phrased
  "Postgres-class"/"DuckDB-class embedded OLAP" — the grep list above is the hard set.)

- [ ] **Step 5: Commit**
  `git add .agents/skills/03-architect/references/data-architecture.md && git commit -m "feat(03-architect): data-architecture reference — skeleton + need-gate + datastore-selection core (§0-§1)"` (+ trailer).

### Task 2: §2 Retrieval

**Files:**
- Modify: `.agents/skills/03-architect/references/data-architecture.md` (append under the §2 header)

**Interfaces:**
- Consumes: §0's need-gate (cite, don't restate). Produces: the `DA-T05` clause Task 6 cites; the Stage-6
  golden-set shape Task 8's 00-edit references.

- [ ] **Step 1: Read** synthesis §3.P2 + `research/T2-retrieval-architecture.md` §3 (the staged tree) + §4.

- [ ] **Step 2: Write §2.** Mandatory elements: the staged ladder as a compact decision list — Stage 0
  do-you-need-retrieval (parametric-knowledge test · corpus-fits-context + static + low-volume ⇒ cache-and-stuff;
  the crossover is computed live at use time, never a baked multiplier) · Stage 1 simplest-that-works (structured
  query beats embeddings for structured data · document-level for short docs · in-existing-DB vector under the
  architect's own stated scale target) · Stage 2 the default first stage (hybrid lexical+dense with a **named
  fusion method** · chunking params declared with escalation only on a measured gap · embedding as **swappable
  seed**: shortlist via public benchmark, select via own eval set — leaderboards are shortlist tools, contaminated,
  never decision-grade) · Stages 3–5 rerank/agentic/graph, each REQUIRING a measured-gap or stated-query-share
  justification, each with its named when-not (rerank: small precise top-k or latency-bound · agentic: bounded
  iterations + difficulty routing, never for latency-sensitive high-volume paths · graph: lazy/query-time default,
  real global-query share required) · Stage 6 evaluation **declared before Stage 2** (golden set ≥20 hand-labeled,
  graded relevance, versioned · floor metric at the generator's k · re-run trigger list · production failures feed
  the set); the context-rot line (long-context absorbs easy cases; hybrid retrieve-then-reason is the default —
  degradation is real independent of cost); index **family** + quantization + CRUD posture are architect-level
  (parameters are tuning) and must match the stated freshness; the **§2 teeth block**, verbatim:

  ```markdown
  **DA-T05 — a retrieval ADR/spec REQUIRES:** the stage declared · a "why not simpler" justification on any
  Stage 3–5 escalation · chunking params or an explicit no-chunking rationale · the embedding named + dimensions +
  a reindex trigger · **k-consistency** (the eval metric's k equals the k actually sent to the generator).
  ```

- [ ] **Step 3: Verify.** `grep -n "DA-T05" …/data-architecture.md` → 1 hit in §2. `grep -n "Stage 6" …` → present.
  Re-run the Task 1 Step 4 product-name grep → still no matches.

- [ ] **Step 4: Commit** — `feat(03-architect): data-architecture §2 — retrieval staged ladder + DA-T05`.

### Task 3: §3 Grounding & verification-against-data

**Files:**
- Modify: `.agents/skills/03-architect/references/data-architecture.md` (append under §3)

**Interfaces:**
- Produces: the `DA-T06` clause Task 6 cites; the judge-record dependency Task 7/8 wire (`grader:
  judge(validated)` ⇒ a `docs/verification/judges/<name>.md` record).

- [ ] **Step 1: Read** synthesis §3.P3 + §9 + `research/T3-grounding-verification.md` §3.

- [ ] **Step 2: Write §3.** Mandatory elements: the **9 declarations** as a numbered list with default + when-not
  (named ground-truth source per claim-type — a specific table/view/index, never "our data" · freshness/staleness
  contract · check tier per claim-type · numeric threshold **+ the action on crossing** — a threshold without an
  action is not a control · fallback per failure mode — silence never acceptable · provenance/audit line — enough
  to reconstruct "what grounded this output" · write-path admission rule: schema → referential → business-rule →
  commit, enforced where the LLM cannot bypass · citation contract — resolution is deterministic, span-support may
  be judged · provider-portability note); the **three-tier check taxonomy** (symbolic/deterministic → independent
  learned classifier with declared threshold → same-model self-check), explicitly **flagged as adopted synthesis,
  not industry vocabulary**, with the two rules: **Tier 1 REQUIRED for state-mutating claims** (money · IDs ·
  dates · regulated facts) and Tier 3 never the sole gate for a Tier-1/2-eligible claim; the two durable gotchas
  (schema enforcement solves syntax, not truth · a "faithfulness score" may contain a judge one layer down —
  classify checks by what they actually are); LLM-issued queries: read-only enforced at the driver/connection
  layer, never prompt-only; judged checks require the judge-validation record (`shared/agentic-profile.md`
  §eval-suite); the **§3 teeth block**, verbatim:

  ```markdown
  **DA-T06 — a grounding spec REQUIRES:** a named ground-truth source per claim-type · a numeric threshold + the
  action on crossing · a fallback per failure mode · driver-layer read-only enforcement for any LLM-issued queries.
  ```

- [ ] **Step 3: Verify.** `grep -n "DA-T06" …` → 1 hit in §3. `grep -n "adopted synthesis" …` → present.
  Product-name grep → clean.

- [ ] **Step 4: Commit** — `feat(03-architect): data-architecture §3 — grounding declarations + three-tier checks + DA-T06`.

### Task 4: §4 Agent memory

**Files:**
- Modify: `.agents/skills/03-architect/references/data-architecture.md` (append under §4)

**Interfaces:**
- Produces: the `DA-T07` clause Task 6 cites; the Gate-0 trigger list the `Category: memory` ADR must cite.

- [ ] **Step 1: Read** synthesis §3.P4 + `research/T4-agent-memory.md` §3.

- [ ] **Step 2: Write §4.** Mandatory elements: **Gate-0** (need ≥1: repeated same-domain/user tasks · corrections
  must stick · evolving domain rules · persistent entities across calls · demonstrated token-cost of re-injection ·
  multi-agent shared state · task exceeds context window; absent a trigger, session/thread state + compaction is
  **correct** — and the memory ADR itself cites which trigger fired); the **8 dimensions** with default +
  when-not (kind scoping — working free; semantic/episodic/procedural individually justified, procedural last ·
  substrate per kind — kinds want different backends; one undifferentiated "memory module" is itself a design
  smell; start narrow, graduate on demonstrated need · write policy — async default beyond a demo; verbatim
  retained alongside extraction where storage allows (extraction is a lossy one-way door); explicit
  add/update/delete/no-op semantics for anything user-correctable · retrieval policy — multi-signal; recency
  first-class for episodic; below a few hundred items a scoring formula is ceremony · **lifecycle floor — a TTL or
  decay rule is mandatory; unbounded retention is a named failure mode** · sharing + authz named together — shared
  mutable memory with no authorization model is an anti-pattern · privacy tiering + pre-write PII redaction +
  deletion reaching derived memories · adversarial posture — any write path fed by untrusted content is an
  injection surface; memory poisoning persists across sessions, unlike prompt injection); the **§4 teeth block**,
  verbatim:

  ```markdown
  **DA-T07 — a memory ADR REQUIRES:** the Gate-0 trigger cited · a per-kind substrate mapping · a lifecycle floor
  (TTL/decay rule) · the sharing model + authorization boundary named together (multi-agent) · a deletion ⇒
  derived-memory-reach pairing (when user-facing deletion is promised).
  ```

- [ ] **Step 3: Verify.** `grep -n "DA-T07" …` → 1 hit in §4. `grep -n "Gate-0" …` → present. Product grep → clean.

- [ ] **Step 4: Commit** — `feat(03-architect): data-architecture §4 — memory Gate-0 + eight dimensions + DA-T07`.

### Task 5: §5 volatile classes + §6 landscape appendix

**Files:**
- Modify: `.agents/skills/03-architect/references/data-architecture.md` (append under §5 and §6)

**Interfaces:**
- Produces: the volatile-class list Task 6's SKILL.md routing cites; `DA-T08`; the only file region where product
  names are permitted (§6).

- [ ] **Step 1: Write §5.** Mandatory elements: the six volatile-decision classes (embedding model · reranker ·
  vector store · memory product · grounding service · semantic cache); the rule — a pick in a volatile class is
  proposed as a **Verify-live row** through the existing flesh-out → Tier-2 flow (`shared/live-source-verification.md`),
  and its live-sourced record is the freshness anchor (this file carries criteria; product names never leave §6);
  flag the use-time-research step as **framework-original** (no studied gold-standard source encodes it); the
  **§5 teeth block**, verbatim:

  ```markdown
  **DA-T08 — a volatile-class pick REQUIRES** a `Verified-against:` citation to its live-sourced record — the
  existing S18 rule, applied to the six classes above.
  ```

- [ ] **Step 2: Write §6.** Four compact tables (one per pillar), each headed
  `*Landscape as of 2026-07 — verify at use time; the §5 protocol is the authority.*` Content: engine/product
  classes with 3–6 named exemplars each, drawn from the briefs' landscape sections (T1 §2.4, T2 F9, T3 §2.5/§2.7,
  T4 §2.2) — names + one-phrase role only, no comparison numbers, no "best".

- [ ] **Step 3: Verify.** `grep -n "DA-T08" …` → 1 hit in §5. Product-name grep scoped to §0–§5 (everything above
  the §6 header) → clean; over §6 → matches expected. File length sanity: `wc -l` → 250–380 lines.

- [ ] **Step 4: Commit** — `feat(03-architect): data-architecture §5-§6 — volatile classes + use-time protocol + dated landscape`.

### Task 6: 03 wiring — SKILL.md routing + reconcile teeth + ADR template field

**Files:**
- Modify: `.agents/skills/03-architect/SKILL.md` (References list · the Profile-switch paragraph area · the
  progress checklist)
- Modify: `.agents/skills/03-architect/references/reconcile-architecture.md` (§1b structural lint · the Pass-2 area)
- Modify: `.agents/skills/03-architect/templates/adr.md` (header field list, after `Verified-against:`)

**Interfaces:**
- Consumes: section anchors + DA-T04–08 from Tasks 1–5. Produces: the lint-trio definitions (DA-T01–03) the
  design names Pass-1-owned; the Review-Trigger field DA-T04 requires.

- [ ] **Step 1: SKILL.md — References list entry** (alongside the existing `references/` bullets):

  ```markdown
  - `references/data-architecture.md` — the data craft: §1 datastore selection (always, `init`) + the
    `Data:`-gated modules (§2 retrieval · §3 grounding · §4 memory) + §5 volatile-class use-time research. The
    spine's `Data:` line routes it (`shared/agentic-profile.md`).
  ```

- [ ] **Step 2: SKILL.md — routing paragraph**, appended to the "Profile switch" block:

  ```markdown
  **Data modules.** Read the spine's `Data:` line (registry: `shared/agentic-profile.md`). `init` always walks
  `references/data-architecture.md` §1; a declared `retrieval(…)` / `grounded-writes(…)` / `memory` value
  activates its module (§2/§3/§4 — the need-gate applies; the resulting ADR cites the fired trigger). A pick in a
  §5 volatile class is proposed as a Verify-live row (the tech-mandate flow). Under `agent-system`, `memory` and
  `grounded-writes` are presumptive.
  ```

- [ ] **Step 3: SKILL.md — checklist lines** (in the progress checklist, after the agent-system line):

  ```markdown
  - [ ] **data:** §1 selection rubric walked (`init`); each declared `Data:` module realized or its need-gate
    declined with the trigger cited; DA-T04–08 content-clauses satisfied on data ADRs/specs; volatile picks carry
    `Verified-against:`
  ```

- [ ] **Step 4: reconcile-architecture.md — §1b lint additions** (append to the mechanical-defects bullet list):

  ```markdown
  - **data pairing checks (DA-T01–03):** a declared `Data:` value with no corresponding realization section/ADR
    (**DA-T01**); `retrieval(…)` declared with no `eval-suite` VC row whose golden-set dataset ref resolves
    (**DA-T02**); `grounded-writes(…)` declared with no write-path admission rule named in the realization
    (**DA-T03**).
  ```

  And in the Pass-2/classification area, one pointer sentence: `Data-decision ADRs/specs carry the DA-T04–08
  content-clauses (references/data-architecture.md, per-pillar teeth blocks) — cite them like the topology clause.`

- [ ] **Step 5: templates/adr.md — the Review-Trigger field**, inserted after the `Verified-against:` bullet:

  ```markdown
  - **Review-Trigger:** _<the symptom-based condition that reopens this decision — observable ("autovacuum lag
    exceeds X", "recall@5 below floor two runs straight"), never "review periodically">_  ← framework-original
    field; required by DA-T04 for datastore decisions, recommended for every data-class ADR
  ```

- [ ] **Step 6: Verify.** `grep -n "data-architecture.md" .agents/skills/03-architect/SKILL.md` → ≥2 hits.
  `grep -n "DA-T01" .agents/skills/03-architect/references/reconcile-architecture.md` → 1 hit.
  `grep -n "Review-Trigger" .agents/skills/03-architect/templates/adr.md` → 1 hit.

- [ ] **Step 7: Commit** — `feat(03-architect): wire data craft — SKILL routing + Pass-1 pairing lint (DA-T01..03) + Review-Trigger field`.

### Task 7: shared wiring — agentic-profile registry + evals-operations capability + artifact map

**Files:**
- Modify: `shared/agentic-profile.md` (a new `Data:` subsection after the embedded-agent module; two additions in
  §Eval-suite acceptance)
- Modify: `shared/artifact-map.md` (one row beside the `docs/verification/<tech>.md` row)

**Interfaces:**
- Produces: the `Data:` registry Task 6's routing cites; the capability block + criteria-drift passage Task 8's
  edits cite; the `docs/verification/judges/` home.

- [ ] **Step 1: agentic-profile.md — the Data-line subsection** (new `##` after the embedded-agent module):

  ```markdown
  ## The Data line — data-module routing

  A declared line in `specification.md`, beside `Profile:` / `Embedded agent:`, same governance:

  `- **Data:** retrieval(<capability>) · grounded-writes(<capability>) · memory`

  **Who sets it:** skill 00, at the REVIEW gate — a presented decision, defaulting **absent** (⇒ no module fires;
  a plain webapp is untouched). Under `Profile: agent-system`, `memory` and `grounded-writes` are **presumptive**
  — the line routes attention; the need-gate still gates each ADR. **Changing it later is a Tier-2 amendment.**
  Consumer: 03's `references/data-architecture.md` (§2–§4 modules + the §0 need-gate + the DA teeth).
  ```

- [ ] **Step 2: agentic-profile.md — §Eval-suite additions.** (a) The seed passage, after the floors bullet:

  ```markdown
  - **Seed, never spec.** The 00-time dataset declares the *contract* (dataset home · floor · negatives) for
    stated constraints — the eval-first carve-out; its *content* is a seed that grows error-analysis-first through
    05's loop, edits as amendments. Criteria cannot be fully specified before outputs are seen (criteria drift) —
    the framework declares floors early and grows cases from evidence.
  ```

  (b) The capability block, at the end of the section:

  ```markdown
  ### The evals-operations capability

  The *operational* evals craft — error analysis · judge writing · judge validation · synthetic bootstrap ·
  RAG eval · pipeline audit — is a **named capability, not a vendor** (the tool-cascade doctrine): bind to an
  installed evals skill pack where present (e.g. the MIT `evals-skills` pack, marketplace or `npx skills add`;
  **record the consumed version/commit** — upstream tags no releases), else FD's lean fallbacks
  (`05/references/llm-review.md`, `00/references/requirements-authoring.md` §eval block); **absence is recorded,
  never silently skipped**. Cited by 00 (bootstrap) · 04 (judge writing) · 05 (error analysis + validation).
  A `grader: judge(validated)` declaration resolves to a **judge-validation record** at
  `docs/verification/judges/<judge-name>.md` — frontmatter: pinned judge model · TPR · TNR · split sizes ·
  labeler role · `validated_at_commit`; body: the leakage-rule attestation (few-shots from the train split only).
  No current record ⇒ the floor is not trustworthy (05 checks; fail-closed like G11).
  ```

- [ ] **Step 3: artifact-map.md — the judges row**, directly under the `docs/verification/<tech>.md` row,
  matching its column format:

  ```markdown
  | `docs/verification/judges/<judge>.md` | 04/05 write · 05 reads | R | judge-validation record (pinned model ·
  TPR/TNR · splits · `validated_at_commit`); realization outside `docs/spec/**`; backs `grader: judge(validated)`
  (`shared/agentic-profile.md` §eval-suite) |
  ```

- [ ] **Step 4: Verify.** `grep -n "The Data line" shared/agentic-profile.md` → 1. `grep -n "evals-operations"
  shared/agentic-profile.md` → ≥1. `grep -n "verification/judges" shared/artifact-map.md` → 1.

- [ ] **Step 5: Commit** — `feat(shared): Data-line registry + evals-operations capability + judge-record home`.

### Task 8: E1 cross-seat edits — 05 judge fix · 00 presentation + bootstrap · 04 cite

**Files:**
- Modify: `.agents/skills/05-reviewer/references/llm-review.md` (check 4 rewrite + two capability cites)
- Modify: `.agents/skills/00-discovery/SKILL.md` (the Profile section ~line 52–59 + the REVIEW-gate sentence ~line 116)
- Modify: `.agents/skills/00-discovery/references/requirements-authoring.md` (one line in the eval-block section)
- Modify: `.agents/skills/04-builder/SKILL.md` (one cite in the eval-suite-rows bullet, ~line 60)

**Interfaces:**
- Consumes: the capability block + judge-record schema from Task 7 (cite `shared/agentic-profile.md` §eval-suite —
  never restate the schema).

- [ ] **Step 1: llm-review.md — replace check 4's criterion.** Replace the sentence carrying `target **>90%
  agreement**; **< 80% ⇒ the judge is untrusted**` with:

  ```markdown
  An automated judge gates nothing until its **judge-validation record**
  (`docs/verification/judges/<judge-name>.md`; schema: `shared/agentic-profile.md` §eval-suite) shows **TPR >90%
  AND TNR >90%** on a held-out test split (floor 80/80 — below it the judge is **untrusted**, fall back to human
  review). Check **presence and currency**: the pinned judge model matches the one in use, and
  `validated_at_commit` postdates the judge's last prompt/model change. Raw agreement/accuracy is not a
  validation metric. A production pass-rate reported from judge scores carries bias correction + a confidence
  interval. Judge *writing* and *validation* are evals-operations (the capability in `shared/agentic-profile.md`
  §eval-suite).
  ```

- [ ] **Step 2: llm-review.md — two cites.** In check 2 (error analysis), append: `Method depth (sampling ·
  saturation · fix-before-evaluator triage) is evals-operations — bind per the capability
  (shared/agentic-profile.md §eval-suite).` In check 3 (dataset), after "Features × Scenarios × Personas", append:
  `(the dimension→tuple synthetic-bootstrap method is the same capability)`.

- [ ] **Step 3: 00/SKILL.md — two additions.** In the Profile section (after the "Changing it later" sentence):
  `The **Data line** rides the same flow — infer candidate `retrieval(…)`/`grounded-writes(…)`/`memory` values
  during INGEST, present at REVIEW, record beside the Profile at WRITE SPINE; registry:
  `shared/agentic-profile.md`.` In the §5 REVIEW-gate paragraph, extend the "Also present the Profile" sentence:
  `— and the **Data line** with it (default absent; `memory`/`grounded-writes` presumptive under `agent-system`)`.

- [ ] **Step 4: requirements-authoring.md — the bootstrap line**, appended to the eval-block bullet list:

  ```markdown
  - **Greenfield bootstrap:** with no real failures yet, seed the dataset via the dimension→tuple synthetic
    method (evals-operations capability, `shared/agentic-profile.md` §eval-suite) — still 20–50 cases, negatives
    mandatory, and the seed grows error-analysis-first from real traces (seed, never spec).
  ```

- [ ] **Step 5: 04/SKILL.md — one cite.** In the eval-suite-rows bullet (~line 60), append: `Writing a new judge
  for a row is evals-operations (`shared/agentic-profile.md` §eval-suite) — its validation record must exist
  before the row counts EXECUTED.`

- [ ] **Step 6: Verify.** `grep -rn "90% agreement" .agents/skills/05-reviewer/` → **no matches**.
  `grep -n "judges/" .agents/skills/05-reviewer/references/llm-review.md` → ≥1.
  `grep -n "Data line" .agents/skills/00-discovery/SKILL.md` → 2. `grep -n "evals-operations"
  .agents/skills/04-builder/SKILL.md` → 1.

- [ ] **Step 7: Commit** — `feat(evals): judge-validation record criterion + evals-operations cites across 00/04/05`.

### Task 9: deterministic verification sweep + backlog closure

**Files:**
- Modify: `_artifacts/deferred-backlog.md` (the 🔴 CRITICAL entry)
- No other file changes expected — this task verifies.

- [ ] **Step 1: Cross-reference existence.** Every path cited by the new/edited doctrine resolves:
  `for p in shared/agentic-profile.md shared/live-source-verification.md .agents/skills/03-architect/references/data-architecture.md .agents/skills/03-architect/references/reconcile-architecture.md; do test -f "$p" && echo "OK $p" || echo "MISSING $p"; done` → all `OK`.

- [ ] **Step 2: Full-diff product-name check.**
  `git diff 275096a..HEAD -- '.agents' 'shared' | grep -iE "^\+.*(pinecone|weaviate|qdrant|milvus|turbopuffer|lancedb|neon|supabase|planetscale|mem0|letta|zep|langmem|cohere|voyage)"` →
  matches ONLY on `data-architecture.md` §6 lines. Any other match = fix before proceeding.

- [ ] **Step 3: DA-ID uniqueness + coverage.**
  `grep -rn "DA-T0[1-8]" .agents/skills/ shared/ | grep -v "03-architect/evals"` → DA-T01–03 defined once
  (reconcile §1b), DA-T04–08 defined once each (data-architecture.md), citations only elsewhere.

- [ ] **Step 4: Calibrated-tree untouched proof.**
  `git diff --name-only 275096a..HEAD -- .agents/skills/03-architect/evals/` → **empty output** (hard guardrail held).

- [ ] **Step 5: Backlog closure.** In `_artifacts/deferred-backlog.md`, replace the 🔴 CRITICAL entry's body with a
  short closed record: design + implementation landed (link `_artifacts/data-architecture-design.md`; note the
  research record); remaining work = the design's §9 follow-ups table (link it); move the entry out of "Open
  capability gaps" into a `✅ resolved` line mirroring the existing resolved-item style.

- [ ] **Step 6: Commit** — `docs(backlog): close CRITICAL data-architecture gap — craft landed; follow-ups tracked in the design record` (use `git add -f` for `_artifacts/`).

### Task 10 (USER-GATED): calibrated-suite regression bridge

**Files:** none modified. `.agents/skills/03-architect/evals/**` stays read-only.

- [ ] **Step 1: STOP — window gate.** Confirm with the user before spend: the full 03-architect calibrated suite
  is live LLM runs (Sonnet-tier arch runs ≈110–160k tokens each per the discovery-evals README cost table). Do
  not start on a low window.

- [ ] **Step 2: Baseline sanity.** Read `.agents/skills/03-architect/evals/README.md` + `evals.json`; verify the
  recorded baseline matches the grader's current point scale (the wave-2 handoff flags stale baselines — a
  `15/15` claim against an `/18` grader means re-baseline FIRST, as a separate finding, before trusting any
  regression signal).

- [ ] **Step 3: Run the FULL suite** (never a subset — every case in `evals.json`, with_skill arms), per the
  suite's own README instructions. Collect per-case scores.

- [ ] **Step 4: Compare to baseline.** Any regression → investigate **grader-vs-doctrine first** (wave-1 found
  grader bugs masquerading as failures); a real doctrine-caused regression → fix the doctrine edit (never the
  calibrated tree) and re-run the full suite.

- [ ] **Step 5: Record.** Append the run's outcome (scores table + verdict + any findings) to the design record's
  §7 as a dated "Regression bridge" note; commit — `docs(data-architecture): calibrated regression bridge — full-suite results`.

---

## Plan self-review (run before handoff)

1. **Spec coverage:** design §3 (reference file) → Tasks 1–5 · §4 (spine surface) → Tasks 6–8 (routing/registry/00)
   · §5 (teeth) → Tasks 1–6 · §6 (evals) → Tasks 7–8 · §7 (rollout/verification) → Tasks 9–10 · §9 follow-ups →
   explicitly NOT tasks (named deferrals). No design section is uncovered.
2. **Placeholder scan:** no TBD/TODO; every edit step carries its text or a mandatory-element checklist + source.
3. **Name consistency:** `Data:` line syntax, DA-T IDs, `docs/verification/judges/<judge-name>.md`, section
   anchors §0–§6 — identical across tasks.
