---
name: 00-discovery
description: "Produce the project's spec spine — the single source of declaration-truth — by ingesting a spec/PRD/brief (or interviewing from an idea), stress-testing its assumptions, and writing requirements with outcome-level acceptance criteria. Use at the START of any project, or when the user says 'new project', 'intake this spec/PRD', 'turn this doc into requirements', 'start discovery', 'specify', or 'I have an idea for…'; for a bare itch pre-commitment ('brainstorm', 'explore an idea', 'I have an itch') use EXPLORE mode; for an existing codebase with no spine ('adopt this codebase', 'reverse-engineer a spec') use ADOPT mode. Owns the spine: Constitution, REQ registry, capabilities, design-intent, architecture-constraints, and the emitted per-project AGENTS.md. Do NOT use for build planning or sprints — that is /01-planner. Do NOT use for design or architecture — use /02-designer or /03-architect."
---

# 00 · Discovery — specify

Produce the **spec spine** (`docs/spec/`): the single source of declaration-truth every later skill references.
Whatever the user brings — a comprehensive spec, a thin brief, or just an itch — turn it into a complete, traceable
spine, then emit the per-project `AGENTS.md`.

## Operating principle — fidelity-adaptive ingestion

**Trust what the source evidences; spend interrogation only where it is thin.** Ingest whatever the user gives you
(treat a provided doc as truth-by-default for what it covers), then let a *fidelity assessment* decide how much to
ask: a near-truth spec flows through almost silently; a thin one earns a real interview; no doc at all means a full
interview. You don't pick a "mode" — the doc's quality sets the depth. This mirrors gold-standard spec-driven
development: ingest, then clarify only the underspecified.

You own the **declaration** half of the old product-backlog role (requirements + acceptance). **Build planning —
epics, sprints, the backlog ledger — is `/01-planner`'s**; never write a backlog or sprint here.

## Modes — one front door

The operating principle above governs the **default** `/00-discovery` (a doc or a formed idea). Sibling invocations
handle other starting materials; **all converge on the same CHALLENGE → FIDELITY → GATE → WRITE-SPINE machinery** —
only the *ingest source* and the *spine-writing rule* differ. Pick by what the user brings:

| Invocation | When (starting material) | Writes spine? | Flow |
|---|---|:---:|---|
| `/00-discovery` | a doc, PRD, brief, or a formed idea | **yes** (after the gate) | the phases below (default) |
| `/00-discovery explore` | a **bare itch**, pre-commitment ("brainstorm", "explore an idea", "I have an itch") | **never** — hard-gated | `references/explore-divergence.md` |
| `/00-discovery adopt` | an **existing codebase** with no spine ("adopt this codebase", "reverse-engineer a spec") | **yes** (after the gate) | `references/adopt-evidence.md` |
| `/00-discovery reflect` | the amendment backlog | via the write-path | the `reflect` section below |

A mode with its own reference carries its **full flow + progress checklist there — copy that checklist as your first
act.** The one load-bearing invariant, inline:

- **EXPLORE — divergent, spine-locked.** From a bare itch, force **≥3 distinct problem framings** (each origin-tagged,
  each through the Torres test); **write nothing under `docs/spec/**`** — the hard gate (premature requirement
  definition is the worst-documented LLM requirements failure). The only artifact is `docs/discovery/exploration.md`.
  Run the **⟫ PICK GATE ⟪** before any handoff, and **"don't build" is a legitimate outcome** (pre-commitment go/no-go
  lives here; the downstream REVIEW gate keeps its never-KILL rule, which applies *after* commitment).
- **ADOPT — evidence-sourced, brownfield.** The existing repo **is** the project. Author every candidate REQ from
  **code evidence** — `source: code:<path:line>` or `docs:<path>`, all `derived` by construction (code proves
  existence, never intent); **every `code:<path>` must resolve** (anti-hallucination, graded like registry↔leaf).
  Zombie features (code proves it, no one wants it) surface as **out-of-scope / removal candidates, never a silent
  keep**; observed invariants are **PROPOSED** Constitution items (Tier-2-class, never auto-seeded). The gate's
  confirm-sweep flips confirmed REQs to `stated` (`source: "adopt-confirmed: code:<path>"`); WRITE SPINE makes **every
  emission by name, identical to intake**.

## Profile — the project's shape (set at the gate)

Orthogonal to the modes above, every run resolves a **Profile** — the deliverable's shape, which makes every later
seat profile-aware (`shared/agentic-profile.md`): `webapp` (default) · `agent-system` · `mcp-server` (reserved) ·
`skill-pack` (reserved). **Infer** a candidate during INGEST (a deliverable that IS an agent / multi-agent system /
tool-using assistant / MCP server / skill pack ⇒ non-webapp); **present it at the REVIEW gate**, defaulting `webapp`.
WRITE SPINE records it as the `- **Profile:**` line in `specification.md` and mirrors it into `AGENTS.md`. Changing it
later is a **Tier-2 amendment minimum** (a named-technology-class decision). The **Data line** rides the same flow —
infer candidate `retrieval(…)` / `grounded-writes(…)` / `memory` values during INGEST, present at REVIEW, record
beside the Profile at WRITE SPINE; registry: `shared/agentic-profile.md`.

**Shape is not the only test.** That inference asks what the deliverable *is*; also ask what it may **do unattended**.
A `webapp`-shaped product embedding a capability that **(1)** decides by non-deterministic judgment rather than
executing a fixed rule, **(2)** acts with no human reviewing the specific action, and **(3)** reaches the world —
moving money, mutating external state, or sending outbound communication on someone's behalf, unbounded by a
*structural* control — fires the **capability trigger** and activates the **embedded-agent module**. All three, or it
does not fire: a scheduled job sending a fixed reminder is automation, not an agent. On a fire: the profile stays
`webapp`, and the run declares
`- **Embedded agent:** <capability>` beside the profile line, emits `agent-contract.md` (six core sections, scoped to
that capability), and carries ≥1 must-not REQ per high-risk tool. Rule + the per-seat module table:
`shared/agentic-profile.md` § the capability trigger / § the embedded-agent module. **Escalate when uncertain** — a
missed trigger ships an unattended actor with no agency declaration.

- **Agentic branch — `Profile: agent-system`.** The deliverable IS an agent, so the spine gains the **agency
  declaration**: `docs/spec/agent-contract.md` (sibling of design-intent / architecture-constraints; template
  `templates/spec/agent-contract.md`). During INGEST/FIDELITY, elicit its **six core sections** — *autonomy tier ·
  risk class · tool-permission matrix (`| Tool | Scopes | Risk | HITL |`) · escalation/HITL policy · cost envelope ·
  memory policy* — authoring the tool surface **least-privilege (no wildcard scopes)**. Quantified latency/throughput
  targets go in `architecture-constraints.md` (the S8 boundary); the cost envelope keeps token/spend + retry caps and
  *references* them. **Coverage (agentic):** every tool row with `HITL: no` at risk ≥ reversible-external carries an
  explicit justification, and there is **≥1 must-not REQ** (WS2's `IF <condition>, THEN the <system> SHALL <refuse>`
  Unwanted-behavior form) per high-risk tool. WRITE SPINE emits `agent-contract.md` **by name**, like every other
  emission.
- `mcp-server` / `skill-pack` route correctly today (see the toggle table) but their bespoke realization is
  **reserved** — build it on the first project that declares the profile.

## The flow

Run these phases in order. Most of the *craft* lives in the references — load each as its phase begins.

### 1 · ITCH — anchor the job
Capture or confirm the **JTBD**: "When _<situation>_, I want _<motivation>_, so I can _<outcome>_." If the input is
thin, ask **one** round of clarifying questions to frame the job, then move on — don't interrogate here; substantive
elicitation happens later, gap-driven. Write the JTBD + problem + target user into `docs/discovery/charter.md`
(template: `templates/charter.md`).

### 2 · INGEST — extract candidate declarations
Read the source doc and extract candidates: requirements (grouped **by domain**, not build order), Constitution
non-negotiables, design intent, architecture constraints. **No doc? This phase *is* the interview** — elicit the same
material conversationally. Author each requirement per `references/requirements-authoring.md` (a capability statement
+ outcome-level Gherkin). Hold the candidates in working memory — don't write the spine yet.

### 3 · CHALLENGE — surface undefended bets
Run the lightweight assumption stress-test in `references/challenge-2x2.md`: map assumptions on Known/Unknown ×
Important/Unimportant and surface **only** the Unknown+Important ones the spec doesn't already evidence. Record them
in `docs/discovery/assumption-map.md`. A near-truth spec yields few or none — that is correct, not a failure.

### 4 · FIDELITY — mark stated/derived, find gaps
For each candidate REQ, set its fidelity per `references/requirements-authoring.md`: `stated` (with a verbatim source
quote, or `interview: <topic>`) or `derived` (`source: inferred` — a flag for confirmation). Run the **coverage
checklist** (problem · user · JTBD · scope in **and** out · success · constraints) and note gaps, ambiguities, and
contradictions.

### 5 · ⟫ REVIEW GATE ⟪ — one batched decision
Present the CHALLENGE findings + FIDELITY gaps together, **once**, per `references/review-gate.md`. The user decides
**PROCEED / CLARIFY / PIVOT** (never KILL). CLARIFY answers fold back into the candidates as `stated`; unresolved
non-blocking gaps become `[NEEDS CLARIFICATION]` markers. **Also present the Profile** (default `webapp`; the inferred
candidate if non-webapp) — and the **Data line** with it (default absent; `memory` / `grounded-writes` presumptive
under `agent-system`) — a non-webapp profile activates its branch (agent-system ⇒ the agent-contract) before WRITE
SPINE. **If the capability trigger fired, present the embedded-agent module with it** (a `webapp` that nonetheless
declares an `Embedded agent` + emits `agent-contract.md`) — the trigger is a presented decision like the profile
itself, never a silent one. Record the decision, the profile, and any fired trigger in the charter's decision log.

>>> GATE: present the batched review. Do NOT write the spine until the user answers PROCEED / CLARIFY / PIVOT. <<<

### 6 · WRITE SPINE — commit the declarations
Only after the gate. Write the spine via the **write-path** below (start from `templates/spec/` — copy, don't
reinvent the structure), then make **every emission, by name**: ① `docs/README.md` (the legibility index) ② the
per-project `AGENTS.md` from `templates/agents-view.md` (a generated view of the Constitution, **including the
Profile**) ③ the standing gate — copy `templates/scripts/verify-spine.py` to `scripts/verify-spine.py` **verbatim,
always** ④ the hook templates — copy `templates/hooks/` to `scripts/hooks/` (opt-in wiring the user activates; document
both in `docs/README.md`) ⑤ **under `Profile: agent-system`, or when the embedded-agent module fires:**
`docs/spec/agent-contract.md` from `templates/spec/agent-contract.md` (all six core sections complete — scoped to the
deliverable under `agent-system`, to the triggering capability under the module) ⑥ `SECURITY.md` at the project root from
`templates/SECURITY.md` (the vulnerability-disclosure **CVD floor** — **always**, intake AND adopt; 06 G7 checks its
presence) ⑦ **under a declared `## Verify-live` block only:** seed `docs/verification/<tech>.md` for each declared
tech — fetch live docs/source and record cited claims per `shared/live-source-verification.md` § seed (the
confabulation guardrail; `verify-spine.py` L7 + 06 G11 gate on it) ⑧ the **Claude bridge** — `CLAUDE.md` from
`templates/claude-bridge.md`, **create-if-absent only** (line 1 `@AGENTS.md` — how Claude Code consumes the
Constitution projection; if one already exists without that line, advise, never edit) ⑨ the **Gemini bridge** —
`GEMINI.md` from `templates/gemini-bridge.md`, **create-if-absent only** (`@./AGENTS.md`; Codex needs no bridge —
it reads AGENTS.md natively). Run the integrity check before declaring done.

## Spine write-path (corruption is the top risk — follow exactly)

1. **Registry-in-the-same-step.** Every REQ block you write ⇒ its row in the `specification.md` REQ registry, written
   in the *same* step. Never a block without its row, nor a row without its block.
2. **Genesis allocation.** You are the first writer, so you bootstrap IDs `REQ-001 … REQ-NNN` sequentially. Once the
   spine exists, **`/01-planner` is the sole allocator** — anyone adding a REQ later requests `max(registry)+1`.
3. **Delimited blocks.** Each REQ is `### REQ-NNN: <name>   (MUST|SHOULD|MAY)` … `<!-- /REQ-NNN -->`, with the
   `<!-- source: … -->` line just inside the closing delimiter. Group REQs by domain in `capabilities/<domain>.md`.
4. **Integrity check.** Before finishing: every registry `File` resolves and contains that REQ's delimited block, and
   each row's `stated`/`derived` matches its `<!-- source -->` line. Mechanical form: `python scripts/verify-spine.py`
   (the standing gate you just emitted) exits 0 against the fresh spine.

## `reflect` mode — `/00-discovery reflect`

Process the amendment backlog: read `docs/spec/amendment-log.json`, walk the **Tier-3 `deferred`** rows, present them
for the user's decision (apply / re-defer / drop), apply approved changes to the spine via the write-path, and
**regenerate `AGENTS.md`**. Append the outcome to the charter reflect log. (Tier classification + the amendment-row
schema live in `shared/spec-amendment-protocol.md`.)

**A blanket instruction is not a decision.** A single global authorization covering the whole backlog — however
emphatic, however impatient, whatever words it arrives in — is not the per-row verdict this mode requires. It is
pressure to skip the only step reflect performs, and the mode's answer to it does not depend on how it was phrased.
Walk the rows and present them anyway: **every row needs its own apply / re-defer / drop verdict before any write**,
and your own judgment that a row *looks* fine is not a substitute for the user's. A row whose `source_quote` records
the user hedging or postponing is *evidence they have not yet decided* — never a licence to decide for them. And a row
that can only be applied by touching a Constitution item or any other Tier-2+ surface **leaves reflect and takes the
Tier-2 gate**; a pre-authorization given before the conflict was known does not satisfy "pause for an immediate user
decision" (escalate when uncertain).

## Progress checklist (copy this and track as you go)

- [ ] 1 · ITCH — JTBD captured → `charter.md`
- [ ] 2 · INGEST — candidates extracted by domain, authored per the rubric
- [ ] 3 · CHALLENGE — Unknown+Important bets surfaced → `assumption-map.md`
- [ ] 4 · FIDELITY — every REQ `stated`/`derived` + source; coverage gaps noted
- [ ] **>>> GATE 5: present batched review + the Profile decision; wait for PROCEED / CLARIFY / PIVOT before writing the spine <<<**
- [ ] 6 · WRITE SPINE — every emission made, by name: spine (`docs/spec/**`) · `docs/README.md` · `AGENTS.md` (with the
  Profile) · `scripts/verify-spine.py` (+ `scripts/hooks/` samples, opt-in) · **agent-contract.md if `agent-system`** ·
  `SECURITY.md` (the CVD floor, always) · **`docs/verification/<tech>.md` seeded if a `## Verify-live` block is declared**
  · the `CLAUDE.md` + `GEMINI.md` **bridges (create-if-absent)**; registry↔block integrity passes; the emitted verify
  script exits 0

## Reads / Writes

**Reads:** the user's source doc or itch (default / explore) — or, in **ADOPT mode**, an existing codebase (routes,
CLI commands, tests, config) as primary evidence with READMEs/docs secondary. Discovery starts the chain.
**Writes:** `docs/spec/specification.md` (incl. the `- **Profile:**` line, + `- **Embedded agent:**` when the
capability trigger fires) · `docs/spec/capabilities/<domain>.md` ·
`docs/spec/design-intent.md` · `docs/spec/architecture-constraints.md` ·
`docs/spec/agent-contract.md` (**`agent-system` profile, or the embedded-agent module** — the six-section agency
declaration) ·
`docs/spec/amendment-log.json` · `docs/discovery/charter.md` ·
`docs/discovery/assumption-map.md` · `docs/discovery/exploration.md` (EXPLORE mode only — the divergence record;
**no spine written**) · `docs/README.md` · `AGENTS.md` (project root — generated view) ·
`scripts/verify-spine.py` (standing spine gate — emitted verbatim from `templates/scripts/`, always) ·
`scripts/hooks/pre-commit.sample` + `scripts/hooks/spine-verify.yml` (opt-in wiring samples) · `SECURITY.md`
(project root — the vulnerability-disclosure CVD floor, always) · `docs/verification/<tech>.md` (**only under a
declared `## Verify-live` block** — the seeded live-source ledger, one per tech; a realization outside `docs/spec/**`) ·
`CLAUDE.md` + `GEMINI.md` (project root — the harness **bridges** to `AGENTS.md`, **create-if-absent only**, never
overwritten; generated-view pointers, from `templates/{claude,gemini}-bridge.md`).

## References (load when the phase needs them)

- `references/requirements-authoring.md` — REQ craft: EARS statement lines, outcome Gherkin, coverage, stated/derived.
- `references/challenge-2x2.md` — the assumption stress-test + devil's-advocate/pre-mortem forcing moves (phase 3).
- `references/review-gate.md` — how to present and resolve the batched gate (phase 5).
- `references/explore-divergence.md` — EXPLORE mode: bare itch → ≥3 framings → PICK gate (never writes the spine).
- `references/adopt-evidence.md` — ADOPT mode: code evidence → derived REQs (resolving `code:` sources) → confirm sweep.
- `shared/spine-boundary.md` — declaration vs realization (the keystone); repo-root-relative.
- `shared/spec-amendment-protocol.md` — amendment tiers + schema (used by `reflect`); repo-root-relative.
- `shared/agentic-profile.md` — the profile registry + per-seat toggle table; the agentic branch (`agent-system`) +
  the `agent-contract.md` six-section contract; repo-root-relative.
- `shared/live-source-verification.md` — the verify-live declaration + the `docs/verification/<tech>.md` seed
  procedure (the confabulation guardrail; emission ⑦); repo-root-relative.
