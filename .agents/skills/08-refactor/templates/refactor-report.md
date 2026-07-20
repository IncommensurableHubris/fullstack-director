---
verdict: <CLEAN | PARTIAL | BLOCKED | ACCEPT>
sprint: NN
---

# Refactor Report — sprint-NN

**Verdict: _<CLEAN | PARTIAL | BLOCKED | ACCEPT>_** — _<one line>_.

> CLEAN = all findings addressed, behavior preserved, docs reconciled. PARTIAL = some deferred (list them).
> BLOCKED = revealed a structural/declaration change needing a `/03`→/04` cycle. ACCEPT = nothing warranted (healthy).

## Moves (baby steps, each test-guarded)

- `refactor(scope): <move>` — _<what + why; commit ref>_
- _<any move attempted and reverted, with the reason>_

## Behavior preservation

- The behavior oracle (`test/…`) was **not modified**; `node --test` green before and after; a mutation of the
  refactored code fails the suite (the oracle bites). _<+ any characterization tests added>_

## Reconcile

- **Local (realization):** _<system.md / specs / design-system / guardrails corrected — the code↔doc drift closed>_.
- **Declaration (amendment):** _<AMD-NNN (tier, disposition, resolved_by ADR-NNN) — or "none: no declaration contradiction surfaced">_.

## Deferred (Two Hats — routed)

_<bug → /05 · vuln → /07 · feature → /04 · migration → /03→/04 — or "none">_

## Before / after metrics

| Metric | Before | After |
|--------|--------|-------|
| God files / functions | | |
| Duplicated blocks | | |
| Dead exports | | |
| Doc-drift items | | |
| Circular deps | | |

## Next command

_</05-reviewer · next sprint · /00 reflect · /03-architect (BLOCKED migration)>_
