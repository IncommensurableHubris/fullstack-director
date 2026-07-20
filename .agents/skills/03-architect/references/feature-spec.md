# Feature-spec craft — the per-sprint "build contract" realization

> Loaded by skill 03, **mode `sprint N`** (write `specs/<feature>.md`). How to turn a sprint's REQs (+ the `02`
> design contract) into a spec rich enough that `04-builder` implements without guessing and `05-reviewer` verifies
> mechanically. The concrete fill-in artifact is `templates/feature-spec.md`; this file is the **method** and the
> **why**. Each spec **references** the sprint's REQs by ID and covers the `02` manifest's DM-IDs — it never copies
> REQ prose (`shared/spine-boundary.md`, repo-root-relative).

## One spec per feature, referencing REQs

Write `docs/architecture/specs/<feature>.md` (kebab-case) per feature in the slice — named by feature, **not** grouped
by sprint (a feature outlives the sprint that introduced it). At the top, `Serves: REQ-007, REQ-004` — the
back-reference the coverage check reads. Derive the feature set from the sprint's REQ blocks + the `02` design
manifest, not from the data model. The body: **API endpoints** (method · path · auth · request/response schema ·
status codes) · **data-model changes** (tables/fields · relationships · indexes · migrations) · **components**
(backend/frontend, responsibility, location) · **implementation order** (small, independently-committable steps).

## The Verification Contract — mechanically gradeable, the loosest claim that catches a break

A naive Verification Contract is a loose `| Behavior | Method | Pass Criteria |` table. Sharpen it into
a **tool-emittable boolean row** — the bridge from the spine's outcome-level Gherkin (a *declaration*) down to a
finer, UI/technical altitude (*realization*). This is where a REQ's coarse "Done When" becomes an executable check.

Each row (fill `templates/feature-spec.md`):

| Field | What it is | Discipline |
|---|---|---|
| **behavior-id** | `VC-01`, stable within the spec | one per testable behavior |
| **→ REQ** | the REQ this verifies | every in-scope REQ → ≥1 row |
| **derived-from** | the spine Gherkin line it refines | traceable, not invented |
| **method** | `api-contract` \| `browser` \| `unit` \| `static-conformance` \| `eval-suite` | the *how* — architecture knows it, backlog doesn't |
| **assertion** | the **loosest claim that still catches a break** | not the implementation; the observable invariant |
| **pass-criterion** | a **boolean** — no ambiguity | PASS/FAIL, mechanically decidable |
| **oracle** | who/what decides pass | the endpoint, the DOM node, the type-check, the lint rule |

> **"The loosest claim that catches a break."** Over-tight assertions (`response body equals this exact JSON`) break
> on benign change and test the implementation, not the behavior; over-loose ones (`the endpoint responds`) pass a
> broken build. Aim between: *"POST /standups with a valid body returns 201 and the entry appears in that day's
> digest read"* — it catches the real regression and survives a refactor. This is the altitude the spine boundary
> asks for: the outcome is declared in the REQ; the **detailed, UI-specific steps that verify it** are realization
> and live **here**, not in the spine.

**Method fidelity rises with the stack.** At sprint 1 (no stack yet, or just decided) the contract is prose-boolean.
Once a stack is known (sprint N>1), promote high-value rows to the **higher-fidelity contract**: an **OpenAPI**
operation or a **JSON-Schema** for `api-contract` rows, a **static-conformance** rule (ArchUnit / dependency-cruiser
/ a lint) for a crosscutting-concept or banned-list invariant. A `static-conformance` row is a **fitness function** —
it is the MADR *Confirmation* of an ADR made executable (see `references/reconcile-architecture.md`).

**The `eval-suite` oracle — `Profile: agent-system`, and the embedded-agent capability's REQs under `webapp`
(`shared/agentic-profile.md` § The embedded-agent module).** A **distributional** REQ (an agent behavior with no
deterministic oracle — one that carries an `**Acceptance (eval-suite):**` block in the spine) gets a VC row whose
**method is `eval-suite`**. Its **oracle is the eval harness**, and the row records the triple **harness command ·
dataset ref · floor** (the in-spine `docs/spec/evals/**` dataset the verify-script's `L6` guards); the
**pass-criterion is boolean — the suite meets its floor**. This is the architecture-altitude realization of the eval
block: the spine *declares* the dataset + floor; the VC row says *how the build runs it and who decides pass*. 04
takes the RED from a failing case, 05 re-runs it at `final_commit` (the mandatory floor check). The grader **must
bite** — a degenerate output must fail the harness before the row counts (see the bite rule in
`shared/agentic-profile.md`).

### Not-Tested — name the exclusions

List what this sprint's contract deliberately does **not** cover, with a reason and a deferral target. Naming
exclusions is what stops `05-reviewer` from scope-creeping — an unstated exclusion reads as an untested requirement.

## Observability — what it emits + what "healthy" means (D3)

Each feature spec carries one **Observability** row: what the feature **emits** (a log line, a metric, a domain
event) and what **"healthy"** looks like for it (one line each — a rate, a latency, an error-budget). This is the
build-time input to 06 SETUP's `## Operations` **SLO**: the SLO is chosen from the critical journey's feature
signals, so name them here rather than inventing them at release time. `core` = one row; richer signal catalogues
are `on-demand`. A feature that changes user-visible behavior but emits nothing observable is a gap — surface it.

## Migration — the data-model change contract (D4)

When a feature **alters an existing** data model (not an initial/additive change), the spec carries a **Migration**
row: the **forward-migration command** and a **rollback-compatibility statement** — does rollback need a data action?
is it forward-only? is data loss possible? A **destructive** change (drop / rename / alter-type / truncate) is what
06's **G10** gates at release (it demands a backup step + the stated rollback data-implication). Additive changes (a
new table, a nullable column) are N/A — omit the row. The contract is authored here; 06 operationalizes the backup +
the ordered commands in the deploy plan.

## Design Contract Coverage — the forward-direction check

If `docs/design/approved/sprint-NN/manifest.md` exists (the `02` design contract), every **DM-ID** it declares must
be covered by a feature spec. Check coverage in the **forward direction — manifest → specs, never the reverse** — so
you cannot hallucinate a DM-ID that the manifest never declared:

1. Read the DM-IDs from the manifest.
2. For each, find the covering spec via its `## Design Contract Coverage` section (`DM-003 → VC-02`).
3. Build the table `DM-ID → spec → VC-row`. **A DM-ID with no covering spec is a gap** — surface it at the gate.
4. **A DM-ID pushed into "Future Considerations" is a design-contract violation** — refuse it; the fix is a
   backlog re-plan (`/01-planner plan-sprint N`), not a silent deferral.

**Skip** the check when no manifest exists (a headless/API-only slice with no UI) — say so explicitly; do not invent
one.

## The Design-Contract STOP — never skip the contract silently

Before writing specs in `sprint N`, resolve the design contract's state — a Step-1
guard, kept because a silently-skipped contract is how UI coverage rots. **Consult the `Profile` first** (the
per-seat toggle table in `shared/agentic-profile.md`), because it sets what design contract to expect:

- **Manifest exists** (`docs/design/approved/sprint-NN/manifest.md`) → read it (and any mockups); run the coverage
  check above. Under **`agent-system`** the manifest's DM-IDs point at **tools/turns/refusals** (02's agent-experience
  mode), not screens — coverage is checked the same way.
- **`docs/design/` exists but no `approved/sprint-NN/`** → **STOP and ask** (do not assume): *"Wireframes exist but
  no approved design contract at `docs/design/approved/sprint-NN/`. Either (a) run `/02-designer sprint N` and
  complete Gate 2, (b) this slice has no UI to contract, or (c) override with rationale. Which?"* — making the skip
  an explicit user decision, never a default.
- **No `docs/design/` at all** → proceed; mark DM-coverage N/A. This is the **expected** state under **`skill-pack`**
  (02 is skipped — no design phase; `status` routes none) and for a **headless** `agent-system` slice with no tool
  surface to design; do not invent a manifest.

## Local drift check (sprint N>1) — a local reconcile, never a spine amendment

At `sprint N>1`, before writing specs, compare `system.md`'s domain model against `src/` (extract the documented
entities/aggregates; grep `src/` for each; flag documented-but-absent, present-but-undocumented, and name
mismatches). **Drift is corrected locally** — update `system.md` to match reality. It is a *realization* reconcile
(code ↔ doc), **never** a spine amendment: the spine declares *what*, not *how the code is shaped*. **Skip at sprint 1**
(the model was just written; there is no drift yet).

## What "good" means — and what the eval grades

A good feature spec lets the builder implement the slice on the first read and lets the reviewer decide PASS/FAIL
without a judgment call. The eval grades exactly that **structure**: specs that **reference the sprint's REQs**,
carry **Verification-Contract rows with a method + a boolean pass-criterion**, and **cover the manifest's DM-IDs** —
plus the coverage completeness (every in-scope REQ → ≥1 row; every DM-ID → a covering spec). It does **not** grade
prose quality or API elegance — a strong builder writes those too. The lift is the mechanically-checkable contract
the next skills consume.
