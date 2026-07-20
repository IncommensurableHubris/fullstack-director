# WS3 Design — the Agentic Project Profile

> Revision workstream 3 of 4 from the 2026-07-06 framework review (§7). The
> strategic bet: no SDD framework treats the agent as the system under construction,
> and the dominant empirical cause of multi-agent failure is specification +
> verification failure (MAST) — exactly what this framework prevents.
> Status: **APPROVED** (user, 2026-07-06) — all four review decisions confirmed.
> Calibration note: Sections B and the 07 flip are directly verified against
> published standards (GSA-TTS/CSA/AURA; OWASP Agentic 2026); the profile set and
> in-spine datasets implement verified *principles* with framework-native mechanisms
> in territory where the field has no convention yet (the verified market gap) —
> the two syntheses are marked inline below.
> Research grounding: MAST (arXiv 2503.13657) · EDDOps (arXiv 2411.13768) ·
> Anthropic engineering (effective agents · multi-agent system · tool-writing ·
> demystifying evals: 4×/15× token economics) · OWASP Agentic Top 10 (ASI01–10) +
> LLM Top 10 2025 + MCP Security Cheat Sheet · CSA autonomy levels L0–L5 · AURA
> risk dimensions · GSA-TTS AI Agent Specification Template · CaMeL / dual-LLM
> structural injection defenses · Husain/Anthropic eval-driven development ·
> model-migration playbook (shadow → classify → canary).

---

## Problem

The framework's machinery is domain-agnostic, but its assumptions are webapp-shaped:
acceptance is deterministic Gherkin, 02 designs screens, 03's oracle types have no
eval-harness form, `status` routes every sprint through `/02-designer`, and the
LLM/agentic lenses (05's llm-review, 07's R5) activate only as *detected add-ons*.
For projects whose deliverable IS an agentic system, the profile must be a declared,
governed property of the spine that reconfigures each seat.

**Extension doctrine: generalize the proven pattern.** 05/07 already gate optional
modules on detected AI components. WS3 promotes that gating from "detected
downstream" to "declared upstream" — a Project Profile in the spine — and keeps
every change a conditional module, never a fork of the chain.

---

## Section A — the profile declaration

- **Where:** a machine-readable field in `docs/spec/specification.md` (the index),
  above the Constitution: `- **Profile:** agent-system` — mirrored into the
  AGENTS.md emission. Parseable by the verify script and `status`.
- **Values (v1):** `webapp` (default when absent — backward compatible) ·
  `agent-system` · `mcp-server` · `skill-pack`.
- *Synthesis note (deliberate deviation from the research's five project shapes):*
  single-agent and multi-agent/swarm are **one** `agent-system` profile — topology
  is an architecture decision *within* the envelope, so it lives in the mandatory
  orchestration ADR (with the ~15× token-economics justification), not in the
  profile. Evolving one agent into an orchestrator-worker system needs a gated ADR,
  not a spine amendment — the declaration/realization test applied to topology.
- **`framework-fork` is NOT a fifth profile** — it is an entry path × profile:
  `/00-discovery adopt` (WS2) over an agent codebase with `profile: agent-system`.
  ADOPT gains one fork-specific step under an agentic profile: the
  **fork assessment** — auditability/blast-radius/comprehension-debt recorded as
  candidate Constitution items (the breadth-vs-isolation-vs-learning decision the
  research says determines fork safety, e.g. OpenClaw's ~400k unreviewed lines vs
  NanoClaw's ~500 readable ones).
- **Who sets it:** 00, at the REVIEW gate (a presented decision, defaulting webapp).
  Changing it later is **Tier-2 minimum** (it is a named-technology-class decision).
- **New shared protocol: `shared/agentic-profile.md`** — the profile registry, the
  per-seat toggle table (Section D), the eval-suite acceptance contract (Section C),
  and three doctrine lines: *structural defenses, not predictive ones* · *eval
  datasets are declarations* · *ceremony scales down; verification never does*
  (WS1's doctrine, restated for the profile).

## Section B — the agent contract (new spine file, agent profiles only)

**`docs/spec/agent-contract.md`** — the *agency* declaration, sibling of
`design-intent.md` (the look/feel declaration) and `architecture-constraints.md`
(the system envelope). Owned by 00; amended only through the protocol (02/03 may
propose; Tier-2 gates). Contents (GSA-TTS/CSA/AURA-derived, kept lean):

1. **Autonomy tier** — CSA L0–L5 with the user-role ladder (operator → collaborator
   → consultant → approver → observer). One declared tier + rationale.
2. **Risk class** — from the reversibility / impact-scope / write-access test.
3. **Tool-permission matrix** — tool → scopes → risk tier → HITL required? The
   machine-readable capability manifest; least-privilege; no wildcard scopes.
4. **Escalation / HITL policy** — the explicit, non-overridable halt-and-escalate
   list (which actions always pause for a human).
5. **Cost envelope** — token/spend per task, latency p50/p95 targets, retry caps
   (the runaway-loop defense; a documented 63-incident failure class).
6. **Memory policy** — what may persist across sessions/users, at declaration
   altitude (the *architecture* of memory is 03's ADR).

Coverage checklist (00, agentic branch): every tool row with `HITL: no` and risk ≥
reversible-external needs an explicit justification; ≥1 must-not REQ (WS2's
Unwanted-behavior form) per high-risk tool.

## Section C — eval-suite acceptance (the deepest change)

For **distributional behaviors** (agent behaviors without a deterministic oracle),
a REQ carries an **Eval block** alongside (or instead of) outcome-Gherkin:

```
**Acceptance (eval-suite):**
dataset: docs/spec/evals/<domain>/<name>.jsonl   (versioned, in-spine)
grader:  code | judge(validated) | human
metric:  pass@k | pass^k | score
floor:   NN%          class: regression | capability
negatives: ≥1 must-not case in the dataset
```

- **Datasets live INSIDE the spine** (`docs/spec/evals/**`). Rationale: a golden
  dataset IS the behavioral spec — the user would object to it silently changing —
  so placing it under `docs/spec/` puts it behind the existing amendment write-path,
  the WS1 patch check P2 ("spine untouched"), and the verify script, with **zero new
  machinery**. Dataset edits = amendments (traceable evolution, which is exactly the
  Husain discipline: scorers evolve from real-trace error analysis, on the record).
- **Registry/verify additions:** every REQ eval `dataset:` path must resolve
  (same discipline as registry↔leaf; verify script gains the check).
- **Floors:** regression class ≈100%; capability class starts low deliberately
  (saturation = no signal). 20–50 seed cases from real failures, not hundreds of
  imagined ones — discovery records the *success definition*; the dataset grows
  through 05's error analysis.
- **spine-boundary.md** gains one line: eval datasets under `docs/spec/evals/` are
  declarations; eval *results* are realizations.
- *S1 patch-lane interaction (coherence review, approved 2026-07-06):* WS1's P2
  gains the **additive-case exception** — a patch may ADD eval cases (never
  edit/delete), with an automatic Tier-1 amendment row — so bug fixes feed
  regression cases into the dataset without leaving the patch lane; dataset
  *edits* stay amendment-gated on the normal road.
- *Escape hatch (recorded now, built if needed):* a dataset that outgrows in-spine
  scale (~hundreds of cases) externalizes to project-root `evals/` behind a
  **content hash recorded in the REQ eval block** (the `spec_slice_hash` mechanism
  family) — silent edits stay detectable, the spine stays lean. In-repo location is
  the verified portable/no-lock-in choice; in-spine placement is the
  framework-native mechanism for change-gating it (synthesis, marked as such).

## Section D — per-seat toggles (the table in shared/agentic-profile.md)

**01-planner** *(small)* — walking skeleton for agent profiles = the thinnest agent
loop end-to-end **with tracing and the eval harness wired** (harness is foundation,
not polish). Backlog notes evals-engineering ownership (corpus, judge calibration,
floors).

**02-designer** *(profile-switched realization)* — agent-experience design instead
of screens: **tool-surface design** (names/descriptions are the interface; tool
hit-rate is the quality metric — Anthropic tool-writing guidance), conversation/turn
design, persona/voice, error-and-refusal UX, HITL touchpoint UX. The manifest keeps
**DM-NNN ids** (no grader churn) but rows point at tools/turns/refusals instead of
screens. Reconcile targets: design-intent (voice/persona intent) + agent-contract
HITL rows. WCAG floor applies only where a GUI exists. Per profile: `agent-system`
and `mcp-server` → 02 REQUIRED in agent mode (the tool surface is always designable);
`skill-pack` → 02 SKIPPED (trigger/description design folds into 03/04's realization
+ the skill-creator eval method).

**03-architect** *(new ADR categories + one new oracle type)* —
- ADR categories (template gains a category line): memory/context architecture ·
  model selection + prompt-idiom binding · **orchestration topology** (single vs
  orchestrator-worker vs handoff vs swarm — a multi-agent choice REQUIRES the ADR to
  record the value justification against ~15× token economics) · durable execution ·
  isolation/sandbox + credential injection model · observability plan (OTel GenAI
  span tree `invoke_agent`→`chat`→`execute_tool`, token/cost attributes).
- **Verification Contracts gain oracle type `eval-suite`** (harness command +
  dataset ref + floor) alongside unit/api-contract/static-conformance/browser.
- `mcp-server` profile: transport + auth ADR (OAuth 2.1 + PKCE, audience
  validation) and named VC checks from the OWASP MCP cheat sheet: **no token
  passthrough · SSRF egress blocked · human-confirm on irreversible tools · tool
  budget ≤~8** (budget breach → split-server finding).

**04-builder** *(eval-first RED)* — for `eval-suite` VC rows the RED evidence is a
**failing eval case observed before the fix** (the harness run is the oracle; same
anti-tautology gate, new form: the **grader must bite** — a degenerate output must
fail it, mirroring 08's oracle-bites rule; reward-hacking defense).

**05-reviewer** *(module promoted)* — under agent profiles `references/llm-review.md`
is **mandatory, not detected**: eval suites re-run at `final_commit` (pinned
seeds/config), floors verified, judge validation (>90% agreement, already specified)
enforced, plus the **grader hack-resistance spot-check** (feed a degenerate output;
it must fail). Eval results land in the qa-report frontmatter tally (new fields:
`eval_floors_met: true|false`, `evals_run: N`).

**06-release** *(two gate rows + one conditional)* —
- **G8 eval floors:** qa-report frontmatter `eval_floors_met: true` (fail-closed
  like every G-check).
- **G9 observability:** tracing configured and emitting before traffic (the OTel
  span smoke is part of VERIFY), and a drift-monitoring note in the release report
  (solo-scale: production trace sampling + one drift alert, feeding `00 reflect`).
- **Model-facing changes:** a model/provider swap in the diff → the release plan
  must reference the model-migration protocol (Section F) or record an explicit
  waiver. EU AI Act GPAI checklist: **only when** `architecture-constraints.md`
  declares EU-market distribution (documented, off by default).

**07-security** *(panel flip)* — under agent profiles the partition INVERTS
(symmetric to today): the four primary readers are agentic — **R1 injection & goal
hijack** (LLM01 + ASI01; requires a *structural* defense — spotlighting / dual-LLM /
CaMeL-style provenance — "detect injection with more AI" is not a control) · **R2
tool misuse & code execution** (ASI02/05; sandbox + allowlists + budgets) · **R3
identity, memory & secrets** (ASI03/06 + LLM02/07) · **R4 agentic supply chain**
(LLM03 + ASI04: model/skill/MCP-server provenance, slopsquat, the 26.1%
skills-with-vulns stat) — plus a **conditional R5 classic-web reader** iff the
system exposes a web surface. **Spine-poisoning lens** joins R1's remit: the
Constitution/skill files are an injection surface — flag imperative override
clauses ("when X, ignore Y") in spine text.

**status** *(router gains a profile column)* — reads the profile field; P3
earliest-missing-phase resolves per profile (e.g. `skill-pack`: design phase not
expected; `agent-system`: design = interaction manifest presence). Advisory when a
spine has no profile field ("declare a profile; defaulting webapp").

**08-refactor** — unchanged (behavior preservation is profile-agnostic; its oracle
already includes eval suites when they exist).

## Section E — profile-specific acceptance summaries

- **`agent-system`:** agent-contract complete · every distributional REQ carries an
  eval block · orchestration ADR (with multi-agent justification if applicable) ·
  ASI-primary audit · G8/G9.
- **`mcp-server`:** server purpose one-liner (Constitution) · tool budget ≤~8 ·
  transport/auth ADR · MCP Inspector session evidence in VC rows · tool-selection
  (hit-rate) eval · the four named security checks.
- **`skill-pack`:** acceptance = the skill-creator A/B eval method (already
  in-house) · cross-harness load validation (SKILL.md parses under Codex/Gemini
  conventions) · trigger/description evals · packaging ADR (skill vs MCP vs plugin).
  07's R4 covers *consumed* third-party skills too.

## Section F — model migration (reserved, not built)

**`shared/model-migration-protocol.md`** — doctrine-level spec only, activity built
on first need (the CLI-generator deferral precedent): a model/provider swap is a
config change requiring full re-eval; the playbook is shadow (correlation IDs,
incumbent serves) → automated diff classification (improvement / neutral /
regression / novel) → triage novel behaviors → canary → full; prompt re-engineering
per model idiom (never find-and-replace); embedding reindexing budgeted. Evals alone
demonstrably miss co-adaptation regressions (~15% divergence outside eval
distribution). artifact-map lists it under Deferred.

## Eval strategy (Layer A)

1. **00 agentic branch (A/B):** agent-flavored brief → spine carries the profile
   field + a complete agent-contract.md (autonomy tier, tool matrix with HITL
   column, cost envelope) + ≥1 must-not REQ; baseline produces none of the
   structure. Grader: structural.
2. **Eval-block integrity:** every `dataset:` reference resolves; a REQ with a
   dangling dataset fails (verify-script parity fixture).
3. **03 agent mode:** `eval-suite` oracle rows present; a seeded multi-agent-shaped
   fixture forces the topology ADR with the economics justification.
4. **05 threshold gate:** fixture with a floor-failing eval → verdict cannot be
   SHIP; grader hack-resistance check runs (degenerate output fails).
5. **06 G8/G9:** missing `eval_floors_met` / missing tracing evidence → BLOCKED with
   routed reasons.
6. **07 flip:** agent fixture → panel manifest shows the ASI partition + structural-
   defense finding on a planted raw-concatenation injection path; a webapp fixture
   still gets the classic partition (no false flip).
7. **status profile routing:** skill-pack fixture → router does not demand design
   phase; missing profile → advisory.
8. **Integration leg (deferred decision):** a mini agent-system chain
   (00 → 01 → 03 → 04 → 05) as a fifth §10 case — decide at implementation
   planning whether it lands in WS3 or as a follow-up hardening pass.

## Seat-contract deltas (file-level)

- NEW: `shared/agentic-profile.md` · `docs/spec/agent-contract.md` (template in
  00's `templates/spec/`) · `shared/model-migration-protocol.md` (deferred spec) ·
  02 `references/agent-experience.md` · 03 additions to `references/
  reconcile-architecture.md` + `templates/adr.md` category line · 07
  `references/agentic-panel.md` (the flipped partition).
- EDIT: 00 SKILL.md (+agentic branch, profile at the gate) · 01/02/03/04/05/06/07/
  status SKILL.md (profile-conditional sections, each referencing
  `shared/agentic-profile.md` rather than restating) · `spine-boundary.md` (eval
  datasets line) · `artifact-map.md` (agent-contract row, evals/ rows, deferred
  entries) · 05 qa-report template (tally fields) · 06 release-gate reference
  (G8/G9).

## Out of scope for WS3

Building the model-migration activity (reserved only) · the EU AI Act checklist
beyond a documented optional block · production observability tooling (the gate
checks tracing exists; it does not build dashboards) · WS4 items.

## Resolved decisions (review, 2026-07-06 — all confirmed by user)

1. **Profile set v1 = 4** (`webapp` default · `agent-system` · `mcp-server` ·
   `skill-pack`); `framework-fork` = ADOPT × agent-system + the fork assessment.
2. **`docs/spec/agent-contract.md`** with the six sections (autonomy tier · risk
   class · tool-permission matrix · escalation/HITL policy · cost envelope ·
   memory policy).
3. **Eval datasets inside the spine** (`docs/spec/evals/**`), with the recorded
   content-hash externalization escape hatch for outsized datasets.
4. **The 07 panel flip** under agent profiles (agentic-primary partition +
   conditional classic-web R5 + spine-poisoning lens).

## Simplification deltas (approved 2026-07-07 — authoritative log: revision-simplification-review.md)

- **§B5:** latency/throughput targets live ONLY in architecture-constraints
  (WS4-D1 quantified NFRs); the cost envelope keeps token/spend + retry caps and
  *references* them; the S8 boundary sentence is extended accordingly.
- **§C:** ASR is a `metric:` value of THE eval block (no second floor grammar;
  the 0% HITL-bypass/irreversible defaults are stated once in
  requirements-authoring). The **bite rule** is defined once in
  `shared/agentic-profile.md`; 04/05/07/08 cite it with their object.
- **§D-05:** `docs/spec/evals/security/**` is carved OUT of 05's re-run remit —
  07's dynamic arm is the sole executor of security suites; 05's floor + fitness
  re-runs merge into one "re-execute declared verifications" section.
- **§D-06:** G9 = span-smoke evidence (Phase 3) + an Operations-completeness
  clause added when Operations lands; the drift/sampling line's single home is
  deployment-config `## Operations`.
- **§A/§D/§E:** `mcp-server` and `skill-pack` REALIZATIONS are **reserved** —
  the enum, W4 parsing, and toggle-table rows stay (marked "reserved — build on
  first project declaring this profile"); `mcp-scan` moves under agent-system
  (it audits *consumed* servers — R4 remit).
- **§D-07 packaging:** the profile-selected panel reference IS the manifest;
  only the two verdict preconditions + ONE checklist (two profile-conditional
  items) live in SKILL.md.
- **Eval 8:** fifth leg = grader + hand-ideal + degenerates now (5.5a); the live
  six-seat chain is deferred (5.5b — trigger: first real agent-system project).
