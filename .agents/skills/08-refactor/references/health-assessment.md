# Health Assessment — the sequential code-health pass + the Decision Matrix

> Loaded by `08` at **ASSESS**. This is a **single sequential read** — a "launch 3 Explore subagents
> in parallel" fan-out is **deleted**: `shared/subagent-protocol.md` says build and refactor stay sequential. Read the code
> and the realization docs yourself, in one pass. Stance: **be a critic, not a builder** — findings bounded to what
> *changes this slice or violates the contract*, never nice-to-haves. Output: `docs/refactoring/health-assessment-
> sprint-NN.md` (template at `templates/health-assessment.md`).

## The signals (walk them in order; cite `file:line` evidence for each finding)

| Signal | Where | What to record |
|--------|-------|----------------|
| **God files / functions** | `src/**` | files > ~300 lines, functions > ~40 lines — with the line counts |
| **Duplication** | `src/**` | verbatim or near-verbatim blocks across ≥2 sites — quote the duplicated block + both locations |
| **Dead / unused code** | `src/**` | exported symbols with **zero importers** (grep the whole tree incl. tests/config for the name — a static "0 importers" can miss a dynamic/string reference); unreachable branches |
| **Complexity hotspots** | `src/**` | deep nesting, long conditionals, a function doing ≥3 distinct jobs |
| **Coupling / cycles** | `src/**` | circular import chains; a module importing many others; `domain → infra` direction violations |
| **Test health** | `test/**` | test-to-code ratio; **coverage gaps on the likely refactor targets** (these become characterization-test work); flaky/slow tests |
| **Doc↔code drift** | `docs/architecture/system.md` · `specs/**` · `docs/design/**` | a documented module/entity that **does not exist** in code (documented-but-missing); a significant code module **not** documented (undocumented-but-exists); a stale ADR referencing a pattern no longer used |
| **Constraint conformance** | `docs/spec/architecture-constraints.md` vs `src/**` + `system.md` | a **stated** constraint the realization **cannot honor** (a datastore that can't meet a stated scale; a "no X" the code violates) — *this is the seed of a declaration amendment, not a local fix* |
| **Guardrail clustering** | `.claude/rules/quality-guardrails.md` | ≥5 entries clustered on one module → a **systemic** problem, not isolated bugs |

**Doc-drift vs constraint-conformance is the fork that decides routing later** (see `reconcile-refactor.md`): a drifted
`system.md` is a **local** fix; a violated **stated constraint** is a **declaration** contradiction (an amendment).

## The Decision Matrix — classify before you touch anything

| Code structure | Business logic | Action |
|----------------|----------------|--------|
| Poor | Good | **Refactor** — preserve behavior, fix structure (this skill) |
| Poor | Poor | **Rewrite** — a fresh `/03`→/04` cycle, not a refactor. **Stop** and recommend it. |
| Good | Poor | **Pivot** — a product decision → `/00-discovery reflect`. **Stop.** |
| Good | Good | **Accept** — don't fix what isn't broken. Record ACCEPT and stop. |

If the answer is **Rewrite** or **Pivot**, do **not** refactor — say so and route. A healthy slice → **ACCEPT** with
~zero findings (the crying-wolf guard: inventing refactors on clean code is a failure, not diligence).

## Two Hats routing — a smell is `08`'s only if it is maintainability

Every finding that is **not** behavior-preserving maintainability is **deferred to its owner**, named explicitly in the
assessment — never fixed here:

- a **bug** (wrong output vs the spec) → `/05-reviewer`.
- a **vulnerability** → `/07-security`.
- a **missing feature / behavior** → `/04-builder` (via `/01` if it needs a REQ).
- a **new architecture decision / migration** → `/03-architect` → `/04-builder`.

## Before/after metrics (record the baseline now; the report re-measures after)

God files · god functions · duplicated blocks · dead exports · circular deps · test-to-code ratio · outdated deps ·
doc-drift items. These are the report's CLEAN evidence — a refactor with no metric moved did nothing.

## Required sections in the health assessment

The Decision-Matrix classification · the severity-scored findings table (each with `file:line` evidence) · the
Two-Hats routing of deferred findings · the guardrail-clustering note · a remediation estimate if a full pass is
warranted. Present it at **Gate 1** and — in `assess` mode — **stop.**
