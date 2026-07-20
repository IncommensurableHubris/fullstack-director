# Slicing craft — how to cut the spine into sprints

> Loaded by skill 01, phase 3 (SPRINT SLICES). How to turn build-order epics into thin, end-to-end sprint slices.
> Grounded in vertical-slicing / walking-skeleton / SPIDR practice. The boundary rule it serves: a sprint's
> **"Done When"** is the *coarse outcome-acceptance of the slice's REQs* — see `shared/spine-boundary.md`, Rule 2
> (repo-root-relative, per the framework's no-`../` rule).

## 1 · Vertical, never horizontal

Each slice cuts through **all layers** — UI → logic → data — to deliver one **observable outcome**. A horizontal
plan (all the database, then all the APIs, then all the UI) ships no value until the very end and defers every
integration to one big-bang merge. A vertical plan makes integration, validation, and learning **continuous**: each
sprint produces something a user can actually do.

Smell test: if a sprint's REQs all sit in one domain or one layer, it is probably horizontal. A vertical slice
usually touches **two or more domains** (e.g. *sign in* + *submit an entry* + *see the result*).

## 2 · Sprint 1 = walking skeleton

Sprint 1 is the **walking skeleton** (Cockburn) / **tracer bullet**: the *thinnest end-to-end thread* that proves the
whole path works and delivers the core job — rough, narrow, unpolished, but **real end-to-end**. It exercises every
architectural seam once (auth → core action → output the user reads), so the riskiest integration is hit on day one,
not deferred. The user can perform the core JTBD after sprint 1, even if only on the happy path.

**Bias the skeleton to the riskiest integration.** If two unknowns compete for sprint 1, pull in the one whose
failure would invalidate the most downstream work.

## 3 · Sequence by value + risk, within dependency order

Order is decided by three forces, in this precedence:

1. **Dependency first (hard constraint).** A slice cannot precede what it needs. Foundation REQs (accounts, auth,
   the core data model) almost always land in sprint 1 even though they are not user-facing — without them nothing
   downstream runs. This is why epics are **build-ordered**, not domain-ordered.
2. **Risk next (learn sooner).** Consult `docs/discovery/assumption-map.md`. **Bias sprint 1 to de-risk the top
   Unknown + Important bet** — make the walking skeleton exercise exactly the path that would prove or kill that
   assumption. This is the discovery → planning seam: the bet the user accepted at the discovery gate becomes the
   thread sprint 1 is built to test. (If no assumption-map exists, fall back to value + dependency.)
3. **Value last (within the above).** Among slices that are unblocked and equally risky, pull the
   highest-user-value one forward.

## 4 · SPIDR — splitting a REQ too big for one thin slice

When a single REQ won't fit one thin, token-bounded slice, split it with **SPIDR** (Mike Cohn) — never go horizontal
to make it fit:

- **S**pike — a time-boxed investigation when the REQ is too *unknown* to estimate; its output is knowledge, not
  shippable behavior.
- **P**ath — split by workflow path: the **happy path first**, alternate/error paths later.
- **I**nterface — split by surface (one input type / one screen / one client first, others later).
- **D**ata — split by data variety (one record type or one locale first).
- **R**ules — split by business-rule set (the simplest rule first, the edge rules later).

Default order: happy **path** first, then alternate paths / **rules** / **data** / **interface** variety. A REQ that
needs 4+ scenarios to express is often two REQs — flag it back to `/00-discovery` rather than absorbing the scope.

## 5 · Each slice's "Done When" = its REQs' outcome-acceptance

A sprint's **"Done When"** is the **coarse, observable, end-to-end** definition of done for the slice — derived from
the **frozen outcome-acceptance** of the slice's REQs (the sprint-freeze snapshot), traceable to their REQ-IDs. It is
**not** a re-paste of every detailed UI step — those finer steps are skill 03's feature-spec Verification Contracts,
at a lower altitude. If a reviewer can read the "Done When" list and unambiguously verify each item end-to-end, it is
right; if an item names a selector or an internal mechanism, it is at the wrong altitude.

## 6 · Token-bounded (~200k build budget)

Each sprint must fit within roughly a **200k-token** build context. If a slice is too big to fit, **split it with
SPIDR (§4)** — never widen it horizontally to fit. Later sprints **widen the path**: add the `SHOULD`/`MAY` REQs,
alternate paths, edge rules, and polish on top of the skeleton the earlier sprints proved.

---

### Sources
Vertical slicing & the walking skeleton (Cockburn); SPIDR (Mountain Goat Software, Mike Cohn); the 2026 SDD survey
(thin vertical slices = "one small, testable, end-to-end behaviour… not a layer"); Spec Kit `/tasks`
(dependency-ordered) and Kiro `tasks.md` (tasks build upon each other).
