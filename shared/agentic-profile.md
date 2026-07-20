# Agentic Project Profile — the declared shape that makes every seat profile-aware

> **The profile protocol.** One declared field on the spine reconfigures each seat. Stated once, here; every
> profile-conditional section in a `SKILL.md` **cites this file rather than restating it**. It exists so the
> framework can treat *the agent as the system under construction* without forking the chain — the extension
> doctrine is **generalize the proven pattern**: 05/07 already gate optional modules on *detected* AI components;
> the profile promotes that gating from "detected downstream" to **declared upstream**. Every change is a
> conditional **module**, never a fork.

## The profile registry

A machine-readable field in `docs/spec/specification.md` (the index), above the Constitution:

```
- **Profile:** agent-system
```

| Value | Deliverable | Realization |
|-------|-------------|:-----------:|
| `webapp` | a web/app product — the framework's original shape (deterministic acceptance, screens, classic OWASP) | **live** (default) |
| `agent-system` | an AI agent or multi-agent system (single-agent and swarm are **one** profile — topology is an ADR *within* the envelope, not a profile) | **live** |
| `mcp-server` | an MCP server exposing tools/resources | **reserved**¹ |
| `skill-pack` | a pack of agent skills (SKILL.md + references) | **reserved**¹ |

- **Absent ⇒ `webapp`** — backward compatible; existing spines need no change (the verify script's `W4` is advisory,
  never a FAIL: *"declare a profile; defaulting webapp"*).
- **Who sets it:** skill 00, at the REVIEW gate — a presented decision, defaulting `webapp`.
- **Changing it later is a Tier-2 amendment minimum** — it is a named-technology-class decision (see
  [`spec-amendment-protocol.md`](spec-amendment-protocol.md)).
- **Shape is not the only test — the capability trigger.** The registry above asks *what the deliverable is*. It does
  not ask *what the deliverable may do unattended*, and a product can be a plain `webapp` in shape while embedding one
  capability that acts on the world by itself. The trigger needs **all three**:
  1. **It decides, it doesn't just execute** — the capability exercises **non-deterministic judgment** (a model, not a
     rule): it interprets, negotiates, chooses, or composes. A scheduled job that sends a fixed reminder on a fixed
     rule is **automation, not an agent** — deterministic behavior is specified by ordinary REQs and does not fire
     this trigger, no matter how unattended it is.
  2. **No human in the loop** — it acts without a person reviewing the specific action. A draft a human approves
     before it goes out does not fire the trigger; the human *is* the control.
  3. **It reaches the world** — it moves money, mutates external state, or sends outbound communication on someone's
     behalf, at a reach the brief does not already bound with a **structural** control (a code-enforced ceiling, not
     a prompt asking the model to behave).

  All three or it is not this module's business: judgment without reach is a suggestion engine; reach without judgment
  is a cron job; either with a human in the loop is a reviewed workflow. A fired trigger does **not** change the
  profile — it activates the **embedded-agent module** (below). **Escalate when uncertain** *within* the three-part
  test: an unneeded module costs one section nobody reads; a missed one ships an unattended actor with no agency
  declaration and no injection lens. But do not stretch the test to reach a deterministic feature — a module that
  fires on every webapp is ceremony, and ceremony gets ignored precisely when it matters.
- **`framework-fork` is not a fifth profile** — it is an entry-path × profile: `/00-discovery adopt` over an agent
  codebase with `Profile: agent-system`, plus ADOPT's one fork-specific step (the fork assessment:
  auditability / blast-radius / comprehension-debt recorded as candidate Constitution items).

¹ **Reserved** = the enum value, the `W4` parse, and this file's **routing/toggle rows exist now**; the profile's
*realization content* (mcp-server's transport/auth ADR + the four MCP checks; skill-pack's packaging ADR + trigger
evals) is **built on the first project that declares the profile** — the CLI-generator deferral precedent. A
reserved profile still routes correctly today; it just has no bespoke realization craft yet.

## The per-seat toggle table

**This table is the single source for how each seat behaves per profile.** The `status` router, 03's Design-Contract
STOP, and 02's skip decision all resolve against it — none of them restate it. A cell reading "← " inherits the cell
to its left.

| Seat | `webapp` (default) | `agent-system` | `mcp-server` (reserved¹) | `skill-pack` (reserved¹) |
|------|--------------------|----------------|--------------------------|--------------------------|
| **01** planner | screen-first walking skeleton | walking skeleton = the **thinnest agent loop end-to-end, with tracing + the eval harness wired** (harness is foundation, not polish); backlog notes evals-engineering ownership | ← + tool-budget note | trigger/description slice; the skill-creator A/B *is* the harness |
| **02** designer | **REQUIRED** — screens | **REQUIRED** — **agent-experience**: tool-surface design (names/descriptions are the interface; hit-rate is the quality metric), turn/conversation design, persona/voice, refusal-UX, HITL-touchpoint UX; manifest keeps `DM-NNN`, rows point at **tools/turns** not screens | **REQUIRED** — tool surface | **SKIPPED** — trigger/description design folds into 03/04 + the skill-creator eval |
| **03** architect | classic ADRs; unit / api-contract / static / browser oracles | **+ agentic ADR categories** (memory · model-binding · **topology** · durability · isolation · observability) **+ the `eval-suite` oracle**; a multi-agent **topology ADR REQUIRES the ~15× token-economics justification** | ← + transport/auth ADR + the four MCP checks | packaging ADR (skill vs MCP vs plugin) |
| **04** builder | test-first RED | **+ eval-first RED** for `eval-suite` rows (the failing case observed pre-fix) **+ grader-bites** (§ the bite rule) | ← | the skill-creator A/B is the RED |
| **05** reviewer | `llm-review` runs on **detected** AI components | `llm-review` is **MANDATORY**: eval floors re-run at `final_commit` (pinned seeds/config) · judge-validation (>90% agreement) · **grader hack-resistance spot-check** (§ the bite rule); tally fields in the qa-report | ← | trigger/description evals |
| **06** release | the full gate table (G8 passes `n/a` · G9 = the Operations clause · G10 conditional) | **G8 floors bite + G9 adds the span-smoke clause**; a **model/provider swap** → the release plan references the model-migration protocol or records a waiver | ← | cross-harness load validation |
| **07** security | classic OWASP panel | **the panel FLIPS**: R1–R4 are agentic-primary (injection & goal-hijack · tool-misuse & code-exec · identity/memory/secrets · agentic supply chain) + a **conditional** classic-web R5; the **spine-poisoning lens** joins R1 | ← + the reserved MCP checks | R4 also covers *consumed* third-party skills |
| **status** | design phase = the design manifest | design phase = **interaction-manifest presence** (tool surface / agent-experience) | ← | **no design phase expected** (design folds away) |
| **08** refactor | unchanged — behavior preservation is profile-agnostic (its oracle already includes eval suites when they exist) | ← | ← | ← |

## The embedded-agent module — an agentic capability inside a non-agentic shape

The intro's extension doctrine is *"05/07 already gate optional modules on **detected** AI components; the profile
promotes that gating from detected downstream to **declared upstream**."* This module is that promotion for the
hybrid case: the deliverable's **shape** is not an agent, but one **capability** inside it is. It is a **conditional
module, never a fork** — each seat's `webapp` column still governs everything else, so a mostly-CRUD product keeps
its screens, its classic panel, and its deterministic oracles.

Fired by the **capability trigger** (§ the profile registry) and **declared** beside the profile line in
`specification.md`, so later seats route on a field rather than re-deriving the judgment:

```
- **Profile:** webapp
- **Embedded agent:** stock-reorder   <!-- places supplier purchase orders unattended -->
```

| Seat | What the module **adds** (everything else stays `webapp`) |
|------|------------------------------------------------------------|
| **00** discovery | `docs/spec/agent-contract.md` becomes **on-demand(embedded agent)** — the same **six core sections**, scoped to the triggering capability rather than the product. **≥1 must-not REQ** per high-risk tool, as under `agent-system`. |
| **02** designer | screens **plus** the capability's tool-surface / refusal-UX / HITL-touchpoint design; the manifest keeps `DM-NNN` and **gains** rows pointing at its tools/turns. |
| **03** architect | the agentic ADR categories (memory · model-binding · durability · isolation · observability) **for the capability only**, + the `eval-suite` oracle on its REQs. |
| **05** reviewer | `llm-review` is **MANDATORY** for the capability, not merely "detected": eval floors re-run at `final_commit`, judge-validation, grader hack-resistance spot-check (§ the bite rule). |
| **06** release | G8 floors bite on the capability's eval rows. |
| **07** security | **R1 (injection & goal-hijack) + R2 (tool-misuse) go primary for the capability's surface** — its inputs are untrusted by default; the classic-web panel stays primary for the rest. |

- **Not a partial agent-contract.** When the module fires, the six sections are **core**. An unattended actor with a
  half-declared envelope is the exact failure this module exists to prevent; what narrows is the *object* (the
  capability), never the section set.
- **Promotion.** If the capability grows until it *is* the deliverable, the profile moves to `agent-system` — a
  Tier-2 amendment, like any profile change.

## The Data line — data-module routing

A declared line in `specification.md`, beside `Profile:` / `Embedded agent:`, same governance:

`- **Data:** retrieval(<capability>) · grounded-writes(<capability>) · memory`

**Who sets it:** skill 00, at the REVIEW gate — a presented decision, defaulting **absent** (⇒ no module fires;
a plain webapp is untouched). Under `Profile: agent-system`, `memory` and `grounded-writes` are **presumptive**
— the line routes attention; the need-gate still gates each ADR. **Changing it later is a Tier-2 amendment.**
Consumer: 03's `references/data-architecture.md` (§2–§4 modules + the §0 need-gate + the DA teeth).

## Eval-suite acceptance — the contract

For **distributional behaviors** (agent behaviors with no deterministic oracle), a REQ carries an **Eval block**
alongside (or instead of) its outcome-Gherkin. The canonical schema — 00 authors it (see
`00-discovery/references/requirements-authoring.md`), 03's `eval-suite` oracle points at it, 05 re-runs it, 06's
G8 reads its floor:

```
**Acceptance (eval-suite):**
dataset:   docs/spec/evals/<domain>/<name>.jsonl   (versioned, in-spine)
grader:    code | judge(validated) | human
metric:    pass@k | pass^k | score
floor:     NN%          class: regression | capability
negatives: >=1 must-not case in the dataset
```

- **Datasets live INSIDE the spine** (`docs/spec/evals/**`). A golden dataset **is** the behavioral spec — the user
  would object to it changing silently — so it sits behind the existing amendment write-path, the WS1 patch check
  **P2** ("spine untouched"), and the verify script (**`L6`**: every `dataset:` path resolves). Zero new machinery.
- **Dataset edits = amendments** (traceable evolution — the Husain discipline: scorers evolve from real-trace error
  analysis, on the record). The one carve-out is the **additive-case exception**: a patch (WS1 lane) may **ADD** eval
  cases (never edit or delete), logged as an automatic Tier-1 amendment row — so a bug fix feeds its regression case
  into the dataset without leaving the patch lane.
- **Floors:** the **regression** class runs ≈100% (a regression is never acceptable); the **capability** class
  starts deliberately low (a saturated capability floor gives no signal). Seed **20–50 cases from real failures**,
  not hundreds of imagined ones — discovery records the *success definition*; the dataset grows through 05's error
  analysis.
- **Seed, never spec.** The 00-time dataset declares the *contract* (dataset home · floor · negatives) for
  stated constraints — the eval-first carve-out; its *content* is a seed that grows error-analysis-first through
  05's loop, edits as amendments. Criteria cannot be fully specified before outputs are seen (criteria drift) —
  the framework declares floors early and grows cases from evidence.
- **Negatives are mandatory:** ≥1 must-not case in every dataset (an agent that only passes happy-path cases is
  unverified against abuse).
- **Escape hatch (recorded, built on need):** a dataset that outgrows in-spine scale (~hundreds of cases)
  externalizes to project-root `evals/` behind a **content hash recorded in the REQ eval block** — silent edits
  stay detectable, the spine stays lean. In-repo location is the portable/no-lock-in choice; in-spine placement is
  the change-gating mechanism.

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

## The bite rule

**A grader or oracle counts as real verification only if a deliberately-wrong output makes it fail.** Before an
`eval-suite` (or any oracle-backed) row is marked EXECUTED, feed the grader a **degenerate output** and confirm it
**fails** — a grader that passes garbage is measuring nothing (the reward-hacking / grader-hacking defense). Defined
once here; cited with its object by:

- **04** (builder) — at RED, for `eval-suite` rows: the grader must bite before the row counts.
- **05** (reviewer) — the `final_commit` hack-resistance spot-check.
- **07** (security) — before trusting a security suite's PASS.
- **08** (refactor) — its behavior-preservation oracle must bite (the oracle-bites rule this generalizes).

## The core / on-demand section convention

A template section carries a **load marker**:

- **core** — always present; graders assert its presence on every fixture.
- **on-demand(&lt;trigger&gt;)** — present only when the trigger fires; its **absence on a fixture that does not trigger
  it is correct, not a gap.**

So graders assert **core sections only** on small fixtures. Example: an `agent-contract.md`'s six sections are
**core** under `agent-system`; the mcp-server transport/auth ADR is **on-demand(`mcp-server` profile)**; an incident-
response runbook is **on-demand(first release with real users/data)**.

## Doctrine (three lines, reused verbatim in prose)

- **Structural defenses, not predictive ones.** A control that *detects* an attack with more inference (a classifier,
  "ask the model whether this input is an injection") is not a control. The defense is **structural** — provenance
  tracking, sandboxing, capability allowlists, non-overridable HITL gates. "Detect injection with more AI" fails.
- **Eval datasets are declarations.** A golden dataset under `docs/spec/evals/` is *spec*, not scratch — it changes
  through amendment. Eval **results** are realization (they live in a skill's artifacts and drift-gate).
- **Ceremony scales down by change class; independent verification and the release gate never do.** (WS1's doctrine,
  restated for the profile.) A profile **adds** modules — it never removes the gate.
