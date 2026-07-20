# Data-architecture craft — design record

> **Status:** approved section-by-section 2026-07-18 (five gated sections, each user-confirmed) on branch
> `worktree-data-architecture-craft`. **Consumes:** [`data-architecture-research.md`](data-architecture-research.md)
> (wave-0 synthesis + §9 E1 evals addendum; commits `c90838a`, `7e663f6`) and the six raw briefs under
> [`research/`](research/). **Resolves:** the 🔴 CRITICAL backlog item *data-architecture craft is absent*
> (`_artifacts/deferred-backlog.md`, seeded `6edb73d`). **Next:** implementation plan + fresh-session continuation
> (see §10); this record is the *what/why* — the plan carries the *how/steps*.

## 1 · Problem + goal

`03-architect` *emits* data artifacts (a "data & persistence" breadth-rubric dimension, a `durability` ADR
category, per-feature `data-model` sections) but supplies **no craft** for making those decisions well — and zero
craft behind the `memory` ADR category. Retrieval and grounding exist only as *downstream checks* (05/07), never
designed upstream. Goal: give the data dimension the same teeth the framework's other dimensions have, at
gold-standard 2026 best practice, **without** rotting as the field moves — encode durable criteria in the skill,
delegate volatile leaf facts to enforced use-time research.

Four pillars (user-confirmed scope): **P1 datastore selection** (universal) · **P2 retrieval** · **P3 grounding &
verification-against-data** · **P4 agent memory** (LLM-gated). Plus the **E1 evals workstream**: the pillars'
eval-facing declarations interface with a gold-standard evals *operational* layer (Hamel Husain's method;
`evals-skills`, MIT) — FD declares and gates; the operational layer works.

## 2 · Decision summary — "B-simplified"

Layered activation: **P1 always-on at `init`; P2–P4 as trigger-gated modules** routed by one new declared spine
line. Total footprint: **one new reference file · one new spine line class · one reused record home
(`docs/verification/judges/`) · three capability one-liners · a bounded teeth set (3 lint + 5 ADR-content clauses)
· zero new machinery classes.** Both the inside view (the embedded-agent module precedent) and the outside research
(Stage-0/Gate-0 need-gates as the consensus shape of world-class guidance; T2/T4/T5) independently converge on
this shape. Alternatives rejected: always-on single reference (ceremony on every CRUD app — the exact failure the
framework's module doctrine names); distribution into existing files (one craft smeared across three homes).

## 3 · The reference file — `.agents/skills/03-architect/references/data-architecture.md`

Loaded by 03 at `init` for §1; module sections load only when their trigger is declared. Length in family with the
existing references (~250–350 lines): rubrics + teeth + protocol here; depth stays in the research briefs and, at
use time, in live sources.

| § | Content | Activation |
|---|---|---|
| §0 | **The need-gate** (one shared rule): every module opens with "do you need this at all"; the resulting ADR cites which trigger fired. No fired trigger → absence is correct, not a gap. | doctrine |
| §1 | **Datastore selection**: the 7-dimension leverage-ordered rubric (workload shape → data-model fit → PACELC → symptom-based scale envelope → ops maturity/cost → team-skill/boring-bias → **exit cost, always recorded**); default posture relational + extensions, split at **named breakpoint classes**; LLM-app reweighting note (traces/JSONB · co-located vectors · semantic cache · queue-before-inference). | always-on, `init` |
| §2 | **Retrieval**: the staged ladder Stages 0–6; Stage 2 (hybrid + measured chunking + swappable embedding) is the center of gravity; Stages 3–5 each REQUIRE a measured-gap / stated-share justification; Stage 6 (golden set + floor at the generator's k) declared **before** Stage 2, landing as an `eval-suite` VC row. | `Data: retrieval(<capability>)` |
| §3 | **Grounding**: the 9 declarations (ground-truth source · freshness contract · check tier per claim-type · threshold **+ action** · fallback · provenance · write-path admission rule · citation contract · portability note); the three-tier check taxonomy (**flagged as adopted synthesis**, not industry vocabulary); Tier 1 deterministic REQUIRED for state-mutating claims. | `Data: grounded-writes(<capability>)` (presumptive under `agent-system` where the agent mutates state) |
| §4 | **Agent memory**: Gate-0 trigger list + 8 dimensions (kind scoping → substrate per kind → write policy → retrieval policy → **lifecycle floor: TTL/decay mandatory** → sharing+authz → privacy tiering → adversarial posture incl. memory poisoning); backs the existing `Category: memory`. | `Data: memory` (presumptive under `agent-system`) |
| §5 | **Volatile-decision classes + use-time research**: names the classes (embedding model · reranker · vector store · memory product · grounding service · semantic cache); a pick in a volatile class is proposed as a **Verify-live row** (existing flesh-out → Tier-2 flow); the cited record (`docs/verification/<tech>.md`) is the freshness anchor. Criteria live here; product names never do. | any pillar |
| §6 | **Landscape appendix**: one compact dated table per pillar, stamped *"as of 2026-07 · verify at use time"* — the only place product names appear. | reference only |

Writing rules for the content: **criteria and escalation triggers, never winners or borrowed benchmark numbers**
(the architect states their own recall/latency/cost targets — research contested-points register, items 1–5, 10);
teeth carry stable IDs (`DA-Tnn`, teeth only); framework-original elements are flagged as such (three-tier
taxonomy · use-time-research step · Review-Trigger field · fresh-context verifier), per T5's evidence discipline.

## 4 · The spine surface

- **One new declared line class** in `specification.md`, beside `Profile:` / `Embedded agent:`, same governance:
  `- **Data:** retrieval(kb-search) · grounded-writes(order-agent) · memory`
  Set by **00-discovery at the REVIEW gate** (a presented decision, defaulting absent). Absent ⇒ no module fires —
  a plain webapp stays exactly as today. Under `Profile: agent-system`, `memory` and `grounded-writes` are
  **presumptive** (the need-gate still gates the ADR — the line routes attention, it does not force ceremony).
  Changing the line later = **Tier-2 amendment**. The routing row registers in `shared/agentic-profile.md` (the
  declared-shape routing home) — cited, never restated.
- **Missing inputs → the existing flesh-out channel.** When a module fires and the spine lacks its facts (corpus
  size/freshness, query patterns, write volume, retention), 03's Reconcile proposes them as constraint lines
  (Tier-2). **No 00-discovery facet changes in v1.**
- **Volatile picks enter § Verify-live per-project** via the existing tech-mandate flow — the use-time research
  obligation rides L7/G11 enforcement as-is; zero new gates.

## 5 · Teeth — the budgeted enforcement set

Budget rationale: checks that fire everywhere get ignored (framework doctrine + T5 F12's checklist-vs-evidence
finding). Enforced set: **3 deterministic lint additions + 5 ADR content-clauses**; everything else from the
research's ~45 candidates becomes reconciler prompts and template guidance.

**Slot A — Pass-1 deterministic lint** (`reconcile-architecture.md` §1b; all pairing checks):

| ID | Check |
|---|---|
| DA-T01 | **Module-fired coverage** — a declared `Data:` value with no corresponding realization section/ADR is a finding |
| DA-T02 | **Retrieval ⇒ eval floor** — `retrieval(...)` requires ≥1 `eval-suite` VC row whose golden-set dataset ref resolves |
| DA-T03 | **Grounded-writes ⇒ Tier-1 rule** — `grounded-writes(...)` requires the write-path admission rule named in the realization |

**Slot B — ADR content-requirements** (the `topology`-clause pattern; reconciler Pass-2 + template prompts):

| ID | Deciding… | REQUIRES |
|---|---|---|
| DA-T04 | a datastore | ≥2 named alternatives · decisive driver mapped to a rubric dimension **and** a REQ-ID · symptom-based **Review-Trigger** · exit-cost statement · durable-commitment vs vendor-pick stated separately |
| DA-T05 | retrieval | stage declared · "why not simpler" on any Stage 3–5 escalation · chunking params or no-chunking rationale · embedding named + dims + reindex trigger · **k-consistency** (metric's k = generator's k) |
| DA-T06 | grounding | named ground-truth source per claim-type · numeric threshold + action · fallback per failure mode · driver-layer read-only enforcement for LLM-issued queries |
| DA-T07 | memory | Gate-0 trigger cited · per-kind substrate mapping · lifecycle floor · sharing+authz named together (multi-agent) · deletion ⇒ derived-memory-reach pairing (when user deletion promised) |
| DA-T08 | a volatile-class pick | `Verified-against:` citation (existing S18 rule + the §5 class list) |

**Slot C — VC obligations:** retrieval floors as ordinary `eval-suite` rows (golden set ≥20 labeled, graded
relevance, k aligned); grounding's judged checks require the judge-validation record (§6); memory stores inherit
the existing Migration row (D4). The reconciler's 11 lenses gain **no new lens** — the teeth are the anchors
lenses #10/#11 consume. The ADR template gains one field: **Review-Trigger** (symptom-based revisit condition;
framework-original, supported by Fowler's generic reevaluation guidance).

## 6 · The evals workstream (E1) — five bounded edits

FD's declaration/gate layer is sound and Husain-aligned (inside audit, research §9); the gaps are operational.
Composition, not duplication:

1. **Judge-validation record** — `docs/verification/judges/<judge-name>.md` (reused record home). Frontmatter:
   pinned judge model · TPR · TNR · split sizes · labeler role · `validated_at_commit`. Body: leakage-rule
   attestation (few-shots from train split only). A `grader: judge(validated)` with no current record ⇒ the floor
   is not trustworthy — fail-closed, checked by 05.
2. **The evals-operations capability** — defined once in `shared/agentic-profile.md` §eval-suite: error analysis ·
   judge writing · judge validation · synthetic bootstrap · RAG eval · pipeline audit → bound to an installed
   evals pack (`evals-skills` via marketplace or `npx skills add`; consumed version/commit recorded — upstream has
   no tagged releases) → else FD's lean inline fallbacks → **absence recorded, never silently skipped**. Cited by
   exactly three seats: 00 (bootstrap) · 04 (judge writing) · 05 (error analysis + validation).
3. **Criteria-drift reconciliation** (one doctrine passage, §eval-suite): the 00-time dataset is a **seed, never a
   complete specification** — the contract (dataset home · floor · negatives) is declared up front for stated
   constraints (Husain's eval-first carve-out); content grows error-analysis-first through 05's loop, edits as
   amendments.
4. **`llm-review.md` judge criterion fixed**: ">90% agreement" (the 2024-form distillation, now an anti-pattern
   per its own source) → record-based **TPR>90% AND TNR>90%** (floor 80/80; below ⇒ untrusted, human fallback),
   record presence + currency checked — currency = the pinned judge model matches the one in use AND
   `validated_at_commit` postdates the judge's last prompt/model change; production pass-rates from judge scores
   carry bias correction + a CI.
5. **`requirements-authoring.md`** gains one line: greenfield datasets may bootstrap via the dimension→tuple
   synthetic method (capability cite) — still 20–50 cases, negatives mandatory.

## 7 · Boundaries · rollout · verification

**Non-goals (v1):** no new seats; 01/02/07/08 untouched (retrieval-UX stays with 02's agent-experience mode — a
noted follow-up); no 00 facet changes; no vendoring of `evals-skills` content (MIT permits; composition chosen);
no product names outside §6 appendix; reserved profiles stay reserved; **the wave-2 diagnostic track stays parked
and untouched** — this craft becomes its natural future target.

**Implementation footprint:** NEW `03-architect/references/data-architecture.md` · EDIT `03/SKILL.md` (reference
registration + routing + checklist lines) · `shared/agentic-profile.md` (Data-line registry row · capability block
· criteria-drift passage) · `03/references/reconcile-architecture.md` (DA-T01–03 in §1b + content-requirement
pointers) · `03/templates/adr.md` (Review-Trigger field) · `05/references/llm-review.md` (judge fix + capability
cites) · `00/references/requirements-authoring.md` (bootstrap line) · one capability cite in 04 ·
`shared/artifact-map.md` (register the new reference + `docs/verification/judges/`). Deterministic script wiring
for judge-record resolution (L7-style) is a **named follow-up** — v1 enforcement is 05's procedural check.

**Verification of this initiative itself:**
1. Implementation in a **fresh session** from a committed continuation prompt.
2. After doctrine edits, the **FULL `03-architect` calibrated suite** runs as the regression bridge — never a
   subset — with its baseline sanity-checked first (wave-2 handoff flags stale baselines).
3. **Corpus-leak self-check** on the diff: no vendor/product names or research-brief verbatims in doctrine core
   (greppable; the criteria-not-winners rule made mechanical).
4. New calibrated eval cases for the data craft are a **separate, grader-first follow-up** — never landed with the
   doctrine they judge.

### 7.1 · Regression bridge — full calibrated-suite run (2026-07-18)

Run in a fresh session on branch `worktree-data-architecture-craft` after the doctrine landed (commits
`310178c`→`493b268`). **Baseline-sanity finding, handled first (as §7 step 2 requires):** the recorded iteration-1
baseline (`45/45` = `15/15` per case) is **stale** — it predates WS4 (D1–D6: fitness functions · test strategy ·
observability · migration · threats) and WS6 (S18 verify-live), which grew `check_architecture.py` to **21 checks per
case**. So the run **re-baselines on the current `/21` grader** rather than comparing to the defunct `45/45`; the
regression criterion is *"does `with_skill` still pass every check the data craft could affect."*

**Method:** each `with_skill` arm ran as a fresh Sonnet subagent (`init` + `sprint 1`, autonomous past both gates),
each spawning a real `fsd-reconciler` subagent for the Pass-2 judgment — **genuine** context isolation (the attestation
was recorded, and in the `underspecified` arm the isolated reconciler caught a real self-preference case its own prose
had hand-waved). Deterministic grading via `check_architecture.py`; run workspaces gitignored under
`_artifacts/skills-eval/` — **the calibrated tree was never touched** (Task 9 step 4 proof holds).

| Case | Score | Data-craft-critical checks |
|---|---|---|
| `clean-constraint` | **20/21** | ✅ false-positive guard: **0 amendments** (the always-on §1 rubric did not over-trigger) · full structural contract intact |
| `forbidden-token` | **21/21** | ✅ SQLite↔shared-store contradiction caught: 1 Tier-2 `approved` row + a resolving ADR naming PostgreSQL (no silent swap) |
| `underspecified-constraint` | **21/21** | ✅ flesh-out: a Tier-2 row resolves `[NEEDS CLARIFICATION]` → concrete PostgreSQL, `resolved_by` an ADR |

**Verdict: no regression attributable to the data-architecture craft** (62/63). Every data-craft-critical assertion
passes on all three cases; `capabilities/**` stayed byte-identical on all three. The single miss — `clean`'s **D1**
(one §10 quality scenario written prose-only, no fitness function) — is a **WS4 check the data craft never touches**,
confirmed **run-variance**: the other two arms named a fitness function for every scenario and passed D1. Positive
signal beyond non-regression: each arm produced a dedicated **datastore ADR walking the §1 seven-dimension rubric,
DA-T04-compliant** (≥2 alternatives · driver→dimension + REQ · symptom-based Review-Trigger · exit-cost ·
durable-commitment-vs-vendor-pick separated), and each ran a DA-T04 check via its reconciler — the new craft realized
as intended.

**Caveats + follow-ups:** (1) a pre-change before/after run was not done (≈2× spend), so this is a *"passes the current
grader"* re-baseline, not a byte-level before/after — the data-craft-critical checks passing on all three cases is the
load-bearing evidence. (2) The evals `README.md` iteration-1 table still records the stale `45/45`; refreshing it to
the current `/21` scale is a **separate change** (the eval tree is read-only to this initiative) — folds into §9's
"calibrated eval cases for the data craft (grader-first, separate change)."

## 8 · Simplicity-pass record (what was cut, what deliberately wasn't)

**Cut:** three separate trigger mechanisms → one `Data:` line · new ADR `Category:` enum values → content-clauses
on existing categories · full ID-coding → teeth-only IDs · a new judge-record artifact class → the existing
verification-record home · capability lines at six seats → three · unbounded landscape content → one stamped table
per pillar · ~45 enforced teeth → 3 lint + 5 clauses · three need-gate texts → one shared §0.
**Kept (as simple as possible, *not simpler*):** four pillars stay four (memory's lifecycle/privacy/poisoning
dimensions don't fold); trigger-gating stays (always-on = ceremony); the judge-validation record stays (criterion
vs vibe); use-time research stays (the only staleness resolution for volatile leaves, enforcement already exists).

## 9 · Follow-ups (named, not silent)

| Follow-up | Trigger |
|---|---|
| Judge-record resolution in `verify-spine.py` / `status` (L7-style, parity contract) | first project declaring a `judge(validated)` grader |
| Calibrated eval cases for the data craft (grader-first, separate change) | after the doctrine lands + full-suite regression passes |
| Data-craft cases as wave-2/3 diagnostic targets ("chose by rubric, or named an engine?") | next diagnostic wave |
| 02 retrieval-UX (citation display, refusal surfaces) under agent-experience | first RAG project with a UI |
| Consumer sync (`tools/vendor.py`) after dogfood triage ritual | next re-vendor |
