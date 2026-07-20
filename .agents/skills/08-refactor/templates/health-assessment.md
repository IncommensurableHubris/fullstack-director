# Health Assessment — sprint-NN

> Fill from `references/health-assessment.md`. Read-only; no code changes. This is the whole output of `assess` mode.

**Decision Matrix:** _<Refactor | Rewrite | Pivot | Accept>_ — _<one-line rationale: code structure × business logic>_.
_(Rewrite/Pivot → stop and route; do not refactor.)_

## Findings

| # | Severity | Kind | Location (`file:line`) | Evidence |
|---|----------|------|------------------------|----------|
| 1 | _<H/M/L>_ | _<duplication / dead code / complexity / coupling / doc↔code drift / **constraint contradiction**>_ | `src/…` | _<quote the block / name the symbol / cite the drift>_ |

> Mark each finding's route (below). A **constraint contradiction** is **not** a local fix — it seeds a declaration
> amendment (`reconcile-refactor.md`).

## Two-Hats routing (deferred — NOT fixed here)

- Bugs → `/05-reviewer`: _<…>_
- Vulnerabilities → `/07-security`: _<…>_
- Missing behavior/features → `/04-builder` (via `/01` if a REQ is needed): _<…>_
- New architecture / migration → `/03-architect` → `/04-builder`: _<…>_

## Guardrail clustering

_<count entries per module in `.claude/rules/quality-guardrails.md`; flag ≥5 on one module as systemic — or "none">_

## Baseline metrics (the report re-measures after)

| Metric | Before |
|--------|--------|
| God files / functions | |
| Duplicated blocks | |
| Dead exports | |
| Circular deps | |
| Test-to-code ratio | |
| Doc-drift items | |
| Outdated deps | |

## Recommendation

_<Refactor scope + estimate | ACCEPT (healthy) | Rewrite/Pivot → route>_.
