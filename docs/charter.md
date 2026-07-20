# The Fullstack Director Charter — the framework's own declaration layer

> **What this is.** The single home for Fullstack Director's *intent*: its mission, its non-negotiables, and how
> they change. It is the Layer-A analog of a project's spine Constitution — the same discipline the framework
> imposes on every product, applied to itself. Everything here is **extracted from the repo's existing doctrine**
> (each item names where it is realized), distilled 2026-07-20 and ratified by the user; nothing here is new law.
> It is deliberately **not** at `docs/spec/` — that path is the Layer-B shape, and a spine there would make the
> seat skills treat this repo as a target project (see C13).
>
> **Who consumes it.** Doctrine amendments cite the charter item they serve. Dogfood-triage dispositions
> (`shared/feedback-loop.md`) judge friction against it. The diagnostic track adjudicates findings against it.
> A proposed change that cannot name its charter item — or that contradicts one — pauses for the user, exactly
> as a Tier-2 amendment would.

## Mission

**One person directing every role of the software lifecycle — discovery, planning, design, architecture, build,
review, release, security — holding the entire system context, with zero handoff loss.** The director decides;
AI agents execute the seats; a single living spec spine carries the truth between them. The framework serves
products up to and including **agent systems as the deliverable** (the `agent-system` profile and the
embedded-agent module are that commitment, live), across any AI coding harness the director chooses.

## The non-negotiables

Each item: the principle, then where it is realized. On an intent question the principle wins; on a mechanics
question the realizing file wins.

- **C1 · Spec-first — the spine is the single source of declaration-truth.** Every product/scope question
  resolves against `docs/spec/`; realizations reference it by ID and never copy its prose. *Realized:*
  `shared/spine-boundary.md` · `AGENTS.md` § Operating model · README § four ideas.

- **C2 · Declaration vs realization — the would-the-user-object test.** A fact is a declaration iff the user
  would object to it changing without their say-so; everything derived is realization, drift-gated not
  amendment-gated. This single test draws every boundary in the framework. *Realized:*
  `shared/spine-boundary.md` (the keystone).

- **C3 · Amendments are controlled, never silent.** Expertise improves the spine through three tiers
  (auto-apply / gate / defer), each a structured, quoted row — and **escalate when uncertain**: misclassifying
  down corrupts the user's intent, misclassifying up costs one gate. A deferred scope decision is decided by the
  user at REFLECT, row by row — a blanket instruction is not a decision. *Realized:*
  `shared/spec-amendment-protocol.md` · `00-discovery` § reflect.

- **C4 · The human holds every consequential gate.** Skills batch decisions and pause; subagents report and
  never get the final say on ship or scope; the release gate blocks on unresolved intent (`pending`/`deferred`
  amendments, `[NEEDS CLARIFICATION]` markers). Autonomy is for execution, never for judgment the user owns.
  *Realized:* `shared/subagent-protocol.md` § Guardrails · `06-release` gate table · every seat's `⟫ GATE ⟪`.

- **C5 · Functional roles, no personas.** Each skill is one verb on the spine — specify, decompose, realize,
  build, verify, ship, secure — with exclusive write-paths and sole allocators (01 for `REQ-ID`, 03 for
  `ADR-ID`). Character personas measurably tax correctness; the framework has none. *Realized:* README § four
  ideas · `shared/artifact-map.md` § Single-source & allocation rules.

- **C6 · Verification is context-isolated and self-preference is designed out.** Judgment passes run from a
  fresh spawner that never inherits the producing conversation; judge ≠ producer at every stage, including the
  framework's own evals. *Realized:* `shared/subagent-protocol.md` · 05's seed contract · the eval method's
  model-tier convention (`docs/eval-methodology/`).

- **C7 · Structural defenses, not predictive ones — and honesty about which is which.** For the systems FD
  builds: a control that detects an attack with more inference is not a control; the defense is structural.
  For FD's own process: where a control is predictive (an instruction, an attestation), it is **declared as
  such and never dressed as proof** — a claimed proof mechanism must have a substrate. *Realized:*
  `shared/agentic-profile.md` § Doctrine · `shared/subagent-protocol.md` (the attestation is a declared-inputs
  statement, not proof).

- **C8 · Evidence before assertion.** Verification states are explicit (`EXECUTED`/`OBSERVED`/`INFERRED`);
  SHIP is unreachable while anything material is inferred; gates fail closed on missing or unparseable state;
  a grader counts only if a deliberately-wrong output makes it fail (the bite rule). Never fake a pass — HALT
  and surface. *Realized:* `05-reviewer` honesty gate · `06-release` fail-closed table ·
  `shared/agentic-profile.md` § The bite rule · `04-builder` HALT conditions.

- **C9 · Evals are the acceptance contract, grown from evidence.** Golden datasets are declarations (they live
  in the spine and change by amendment); cases are seeded small from real failures and grown error-analysis-first
  from real traces, not imagined in bulk. The calibrated suite guards regression; the adversarial diagnostic
  track hunts findings; they stay separate so calibration is never re-tuned mid-stream by its own findings.
  *Realized:* `shared/agentic-profile.md` § Eval-suite acceptance · `docs/eval-methodology/` (both tracks).

- **C10 · One home per fact.** Every durable fact has exactly one maintained home; generated views (`AGENTS.md`,
  status blocks) are regenerated, never hand-edited; no hand-synced cross-skill tables; a status lives where it
  originates and nowhere else. *Realized:* `shared/artifact-map.md` · `shared/spine-boundary.md` § Maintained vs
  generated · 01's two-status rule.

- **C11 · Cross-harness portability — no lock-in.** The canonical tree uses open conventions (`.agents/skills/`,
  `AGENTS.md`, spec-minimal `SKILL.md`); capability tiers degrade gracefully (a subagent spawn falls back to a
  fresh top-level invocation); one canonical copy, real files, no symlinks. The framework is not a plugin for
  any one harness. *Realized:* `docs/harness-support.md` · `shared/subagent-protocol.md` § capability tier.

- **C12 · Ceremony scales down by change class; independent verification and the release gate never do.** The
  patch lane skips planning and design machinery for a certified small fix — it never skips the fresh review or
  the release gate. *Realized:* `01-planner` § patch mode (P1–P5) · `shared/agentic-profile.md` § Doctrine.

- **C13 · Layer A is never Layer B.** The framework repo hosts no product; a project's `AGENTS.md` is a
  read-only emission of *its* Constitution; the same filenames in the two layers never collide because the
  layers never mix. Consumers receive vendored copies; fixes flow **master-first** through the feedback loop —
  never patched downstream. *Realized:* `shared/artifact-map.md` § Two layers · `docs/harness-support.md` ·
  `shared/feedback-loop.md`.

- **C14 · Reuse-first, gate-driven, recorded evolution.** Proven machinery is kept and rewired, not rewritten;
  every framework change is verified on real model output or deterministic graders before it lands; the *why*
  lives in git history and design records; the framework speaks in its own voice. *Realized:* `CLAUDE.md`
  § Methodology · the eval-green-per-commit build record · the design records under `_artifacts/`.

## Non-goals (deliberate, standing)

The framework targets **one director + AI agents**, not an organization: no multi-human team ceremony
(inter-person PR/branch conventions, standups); no hand-maintained requirements-traceability matrix (the
REQ-reference graph + `/status` replace it); no enterprise-scale threat-modeling programs or formal
production-readiness reviews; **no product built inside this repo** (C13); and no harness-exclusive packaging
(C11). Removing a non-goal is a charter amendment, not a drive-by.

## Governance

- **Authority.** On *intent* — what the framework is for, what may never regress — this charter wins over every
  craft file. On *mechanics* — how a seat executes — the skills and `shared/` protocols win. (The Layer-B mirror
  of this rule lives in `CLAUDE.md` § Governance precedence: a *project's* Constitution wins product questions;
  the methodology wins process questions.)
- **Change control.** Charter changes are **user-gated, always** — the Tier-2 reflex applied to the framework
  itself. Propose the edit, name what it changes and why, wait for the user's decision; the commit is the
  amendment record (git is the dated audit trail — no separate log, per C10).
- **The escalation reflex.** Work that discovers a conflict *with* the charter pauses and surfaces it — the
  charter may be wrong (it amends), the work may be wrong (it stops), but the user decides which. Escalate when
  uncertain, here as everywhere (C3).
