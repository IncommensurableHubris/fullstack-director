# Fullstack Director — Framework Instructions

> **This is the framework's own entry point (Layer A).** It tells any AI coding agent — Claude Code, Codex, Gemini
> CLI, Copilot, Cursor, OpenCode — how to drive **Fullstack Director** on a target project. It is **not** the
> per-project `AGENTS.md` that skill `00-discovery` generates from a product's Constitution (Layer B); that one
> lives in the *product's* repo and is a read-only emission of its spine. Don't conflate the two, and **don't build
> a product inside this framework repo.**
>
> 🚧 The skills are being built skill-by-skill in producer order — see [README](README.md) for current status.

**Fullstack Director** is a spec-first, cross-harness SDLC skills framework. A single living **spec spine**
(`docs/spec/`) is the canonical source of truth for a project's *declarations* — its requirements, design intent,
and architecture constraints. Each skill performs **one verb on the spine**, challenging and refining it through a
controlled amendment protocol rather than silently consuming or silently mutating it.

## Operating model

- **The spine is truth.** `docs/spec/specification.md` (the Constitution + the REQ registry) is authoritative for
  every product/scope question. Realization artifacts — design, architecture, code, tests — *reference* requirements
  by `REQ-NNN` and change through drift-detection, never by editing the spine directly.
- **Declaration vs realization.** A *declaration* is anything the user would object to changing without their
  say-so; it lives in the spine and is amendment-gated. Everything the framework *derives* is a *realization*; it
  lives in a skill's own artifacts and is drift-gated. The two rules and the "would-the-user-object?" test:
  [`shared/spine-boundary.md`](shared/spine-boundary.md) — the keystone.
- **Amendments are controlled.** A skill that finds the spine wrong proposes an amendment in one of three tiers —
  **auto-apply** (one defensible answer, no behavior change) / **gate** (user-observable or named-technology change —
  pause for the user) / **defer** (scope change → `00 reflect`) — each logged as a structured row. Classification
  rule: **escalate when uncertain.** Protocol: [`shared/spec-amendment-protocol.md`](shared/spec-amendment-protocol.md).
- **Verification is context-isolated.** Review and reconciliation run from a *fresh* spawner so they cannot
  self-prefer. Where a harness supports subagents they spawn; elsewhere they run as a fresh top-level invocation —
  isolation comes from the fresh spawner, not the spawn mechanism. Protocol:
  [`shared/subagent-protocol.md`](shared/subagent-protocol.md).
- **One home per fact.** Where every durable artifact lives and how it is named:
  [`shared/artifact-map.md`](shared/artifact-map.md). Each skill *also* self-declares its own I/O — the skill is the
  source of truth for its paths; the map is the cross-skill index.

## The role-skill sequence

Skills live in `.agents/skills/<NN-role>/SKILL.md` — the open Agent Skills convention that harnesses auto-discover.
Run them in SDLC order; `08-refactor`, `status`, and `feedback` are cross-cutting activities, not SDLC seats.

| Skill | Verb | What it does on the spine |
|---|---|---|
| `00-discovery` | **specify** | itch/JTBD → challenge → intake (doc→spine) or interview→spine → reflect. **Produces the spine**; emits the per-project `AGENTS.md`. |
| `01-planner` | **decompose** | spine (by domain) → build-order epics → token-bounded sprint slices → backlog ledger. **Sole `REQ-ID` allocator.** |
| `02-designer` | **realize (UX)** | design system + screens referencing REQs; reconciles design-intent ↔ design-system. |
| `03-architect` | **realize (system)** | `system.md` / ADRs / feature specs referencing REQs; reconciles arch-constraints ↔ architecture. **Sole `ADR-ID` allocator.** |
| `04-builder` | **build** | implements from realizations (the funnel: specs only). Sequential — no subagents. |
| `05-reviewer` | **verify** | fresh-context review against the spine's outcome-acceptance + the design contract; emits a context attestation. |
| `06-release` | **ship** | deploy flow; **blocks** on any `pending`/`deferred` amendment or surviving `[NEEDS CLARIFICATION]` marker. |
| `07-security` | **secure** | bounded parallel read-only OWASP panel + a single sequential synthesizer. |
| `08-refactor` | — | code↔doc reconciliation (local) + the shared Reconcile step for its docs pass. |
| `status` | — | scans `docs/spec/`, integrity-checks the spine, derives live state + the next command to run. |
| `feedback` | — | consumer repos only: logs **framework** friction (not product bugs) as a SHA-stamped, append-only ledger entry — the capture half of [`shared/feedback-loop.md`](shared/feedback-loop.md). |

## How to drive it

1. Identify the current SDLC phase, **load that phase's skill** from `.agents/skills/<NN-role>/`, and follow it
   exactly — each skill carries its own gates and checklists.
2. Skills read and write **project artifacts** at project-relative paths (`docs/spec/…`, `docs/planning/…`, `src/…`)
   per [`shared/artifact-map.md`](shared/artifact-map.md).
3. Cross-skill protocols live in [`shared/`](shared/) and are referenced **repo-root-relative** (`shared/<file>`). A
   skill's own bundled files live under its `templates/` and `references/` (skill-root-relative). No
   `${CLAUDE_PLUGIN_ROOT}`, no `../` escapes.
4. **Start a new project at `00-discovery`** — it gives every project a spine. Run `status` anytime to see where
   things stand and what command comes next.

## Further reading

- [`docs/charter.md`](docs/charter.md) — the framework's **own declaration layer**: mission + non-negotiables
  (C1–C14) + governance. A change that contradicts a charter item pauses for the user, like a Tier-2 amendment.
- [`docs/guide.md`](docs/guide.md) — the **Director's Guide**: the human-facing manual (this file's counterpart
  for the person holding the gates).
- [`docs/eval-methodology/`](docs/eval-methodology/) — how the skills are evaluated.
- [`docs/harness-support.md`](docs/harness-support.md) — per-harness discovery paths + the manual deployment recipe.
- **Claude Code:** [`CLAUDE.md`](CLAUDE.md) bridges this file and adds the methodology + governance-precedence layer.
