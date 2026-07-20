<!-- Filename: docs/architecture/specs/<feature>.md  (kebab-case, named by feature — not grouped by sprint). -->
<!-- budget: ≤120 lines — longer means restated methodology or copied spec prose; one home per fact. -->

# Feature Spec — <feature name>

> **The per-sprint "build contract" realization.** Owned by **skill 03 (architect)**. It *references* the sprint's
> REQs by ID and covers the `02` design manifest's DM-IDs — it never copies REQ prose. The **Verification Contract**
> below is mechanically gradeable (a boolean per row): `04-builder` implements against it, `05-reviewer` executes it.
> Craft method: `references/feature-spec.md`.

**Serves:** REQ-NNN, REQ-NNN _(reference IDs)_ · **Status:** _<Draft | Approved | Implemented>_

## Overview

<!-- One paragraph: what this feature does and why it exists. -->

## Related

- **Sprint:** `docs/planning/sprints/sprint-NN.md` · **Design contract:** `docs/design/approved/sprint-NN/manifest.md`
- **Architecture:** `docs/architecture/system.md` §<n> · **ADRs:** ADR-NNN

## API Endpoints

| Method | Path | Auth | Request → Response (schema / status codes) |
|--------|------|------|--------------------------------------------|
| _<POST>_ | _</standups>_ | _<session>_ | _<{answers} → 201 {entry} · 400 · 401>_ |

<!-- When a stack is known (sprint N>1), attach the higher-fidelity contract: an OpenAPI operation or a JSON-Schema
     for the api-contract rows below. -->

## Data-model changes

| Table / field | Type | Constraints | Notes (index / migration / relationship) |
|---------------|------|-------------|------------------------------------------|
| _<standups.id>_ | _<uuid>_ | _<pk>_ | _<…>_ |

## Migration `on-demand(this feature changes an existing data model)`

> Only when this feature **alters an existing** data model (not an initial/additive change). Name the forward
> migration and its rollback compatibility. A **destructive** change (drop / rename / alter-type / truncate) is what
> 06's **G10** gates: it requires a backup step and a stated rollback data-implication. Omit this section for a
> purely additive change.

- **Forward:** _<the forward-migration command — e.g. `alembic upgrade head` / `npm run migrate`>_.
- **Rollback compatibility:** _<does rollback need a data action? is it forward-only? is data loss possible? state
  the data implications so 06 can gate them>_.

## Components

| Component | Layer | Responsibility | Location |
|-----------|-------|----------------|----------|
| _<StandupForm>_ | _<frontend>_ | _<capture the three prompts>_ | _<src/…>_ |

## Observability

> One line each: what this feature **emits** (a log line / metric / event) and what **"healthy"** looks like for it.
> 06 SETUP's `## Operations` SLO is built on these. `core` = one row; richer signals are `on-demand`.

| Signal (log / metric / event) | What "healthy" means |
|-------------------------------|----------------------|
| _<`standup.submitted` count · error rate on POST /standups>_ | _<submit success > 99% · p95 < 300 ms>_ |

## Implementation order

> Small, independently-committable steps. Foundation first; the user-facing thread last.

1. _<step — (REQ-NNN)>_
2. _<step>_

## Verification Contract

> The gradeable core. Each row is a **boolean**: derive it from the spine's outcome Gherkin, at a finer altitude.
> Every in-scope REQ → **≥1 row**. The assertion is the **loosest claim that still catches a break** — not the
> implementation.

| VC-ID | → REQ | Derived-from (spine Gherkin) | Method | Assertion (loosest claim that catches a break) | Pass-criterion (boolean) | Oracle |
|-------|-------|------------------------------|--------|------------------------------------------------|--------------------------|--------|
| VC-01 | REQ-NNN | _<"Then their standup is recorded…">_ | _<api-contract \| browser \| unit \| static-conformance \| eval-suite>_ | _<POST /standups with a valid body returns 201 and the entry appears in that day's digest read>_ | _<HTTP 201 AND entry present in GET /digest>_ | _<the API + the digest read>_ |
| VC-02 | REQ-NNN | _<…>_ | _<…>_ | _<…>_ | _<…>_ | _<…>_ |

<!-- method = how it is verified. static-conformance rows execute an ADR's Rule (a fitness function): e.g.
     "no import from infra/ inside domain/" via dependency-cruiser/ArchUnit/lint. An eval-suite row (Profile:
     agent-system) verifies a distributional REQ: oracle = the eval harness; record `harness cmd · dataset ref ·
     floor`; pass-criterion = the suite meets its floor (boolean). The grader must bite (shared/agentic-profile.md). -->

## Design Contract Coverage

> Forward direction only: **manifest → specs**. Every DM-ID this feature implements, mapped to the VC row that
> verifies it. A DM-ID with no covering row is a **gap** (surface at the gate); a DM-ID pushed to "Future
> Considerations" is a **contract violation** (re-plan, never silently defer). Skip if no manifest exists (headless
> slice — say so).

| DM-ID | Element (from manifest) | Covered by |
|-------|-------------------------|-----------|
| DM-NNN | _<description>_ | VC-NN |

## Not-Tested This Sprint

> Name the exclusions — an unstated exclusion reads as an untested requirement and lets review scope-creep.

| Item | Reason | Deferred to |
|------|--------|-------------|
| _<pagination>_ | _<not in this slice; not in the design contract>_ | _<sprint NN>_ |

## Future Considerations

> Deliberate deferrals / known limitations. **HARD CONSTRAINT:** nothing here may be an element of the approved
> design contract (`manifest.md`). If a design element needs deferral, STOP and re-plan at `/01-planner plan-sprint N`
> — silent deferral here is a contract violation.

- _<e.g. caching the digest read — not in the design contract>_
