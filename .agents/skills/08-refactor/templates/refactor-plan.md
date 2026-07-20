# Refactor Plan — sprint-NN

> Fill at SCOPE + SAFETY NET (Gate 1). The plan the user approves before any code changes.

## In scope (address now)

| # | Finding | Category | Move(s) — TYPED | Files in scope |
|---|---------|----------|-----------------|----------------|
| 1 | _<from the assessment>_ | _<Targeted / Cross-cutting / Structural=plan-only / Modernization>_ | _<Extract Function / Dead-Code Elimination / …>_ | `src/…` |

## Deferred (Two Hats — routed, not fixed)

| Finding | Owner | Why not `08` |
|---------|-------|--------------|
| _<…>_ | _</05 · /07 · /04 · /03>_ | _<bug / vuln / feature / migration>_ |

## Behavior-preservation safety net

- **Existing oracle:** _<test files covering the targets — green at pre-refactor commit `<sha>`>_.
- **Coverage gaps → characterization tests to add first:** _<target → new golden-master test, or "none — suite covers all targets">_.
- **Anti-tautology:** the oracle bites (a mutated impl fails it) — _<confirmed / to establish>_.
- **Characterization required?** _<yes, for logic-changing moves | no — rename/move-only, existing suite sufficient>_.

## Structural / declaration items (plan-only or amendment)

- _<a structural migration → the Strangler-Fig plan, routed to `/03`→/04`>_
- _<a declaration contradiction → the Tier-2 amendment to raise at Gate 2 (constraint + resolving ADR `max+1`)>_

## Out of scope

_<files/areas explicitly NOT touched — the blast-radius boundary>_
