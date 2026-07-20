---
name: 08-refactor
description: "Improve codebase structure WITHOUT changing behavior - a cross-cutting activity refactoring under a non-negotiable test-oracle safety net and reconciling realization docs LOCALLY. One spine wiring: appends an amendment row only for a DECLARATION contradiction (a mere realization drift is fixed LOCALLY, no amendment). Two modes (assess, sprint N). SEQUENTIAL - no subagents; Reconcile runs INLINE. Use when the user says 'refactor', 'tech debt', 'clean up the code', or 'refactor sprint N'. Writes src/** + docs/refactoring/{health-assessment,refactor-plan,refactor-report}-sprint-NN.md; reconciles docs/architecture/**, docs/design/**, quality-guardrails.md; appends docs/spec/amendment-log.json; amends architecture-constraints.md via gated Tier-2; requests ADR max+1. Do NOT fix bugs or verify - /05-reviewer. Do NOT fix vulnerabilities - /07-security. Do NOT build features - /04-builder. Do NOT re-architect - /03-architect. Do NOT tidy only sprint-modified files - /05's within-sprint pass."
---

# 08 · Refactor — improve structure, preserve behavior, reconcile

A **cross-cutting refactor activity** (named by function, not an SDLC seat — like `status`). It fills the gap between
`05`'s within-sprint tidy and a rewrite: after several sprints, structural debt accrues that no one sprint owns —
cross-cutting duplication, dead code, god files, doc drift. `08` improves **structure** while preserving **behavior**,
reconciles the realization docs, and **appends amendment rows** only where a refactor surfaces a **declaration**
contradiction.

Kent Beck's rule frames it: *"For each desired change, make the change easy (warning: this may be hard), then make the
easy change."* `08` is the first half — it makes future change easy by improving structure **without changing what the
software does.** Its graded value is **not** "cleaner code" (a strong engineer writes that too). It is the **provably
behavior-preserving change** + the **correctly-routed reconcile** (a local doc fix vs a gated spine amendment) that
`/status` and the release gate can trust.

## The seat's two defining properties

- **Sequential — no subagents.** `shared/subagent-protocol.md`: "Build and refactor stay sequential." The health pass
  is a **single sequential read**, not a parallel panel; Reconcile runs **INLINE** — `08`'s Reconcile-sibling is `02`
  (the first inline appender), **not** `03` (which spawns a subagent). Nothing here spawns.
- **Appender — but most findings are local.** `shared/spec-amendment-protocol.md`: the appenders are **00 / 02 / 03 /
  08**. `08` emits `amendment-log.json` rows — but **only** for declaration-level findings. A code↔doc drift is a
  **realization** fix, corrected locally, **never** an amendment.

## Operating principle — improve structure, preserve behavior, reconcile locally, escalate only declarations

- **Two Hats (Fowler).** Either you change **structure** or **behavior** — never both in a commit. A bug found
  mid-refactor routes to `/05`; a vuln to `/07`; a feature to `/04`. `08` fixes **none** of them — it *notes and
  routes*. A smell is `08`'s **iff** it is maintainability, not a bug, a vuln, or missing behavior.
- **Behavior preservation is the non-negotiable gate** (below) — the safety-net oracle, unchanged, green before *and*
  after, and still **biting**. This is `08`'s honesty gate, the analog of `05`'s EXECUTED gate.
- **Baby steps + explicit move-typing.** One **named** move (Extract Method/Module, Move, Inline, Rename, Replace
  Conditional…) → run the oracle → commit, or **revert-don't-debug**. Telling the model the *exact move type* is the
  single biggest accuracy lever (ICSE: 15.6%→86.7% vs "clean this up").
- **Reconcile: critic, not builder.** Bound findings to "changes this slice / violates the contract." A clean, healthy
  slice yields **~zero** refactors **and ~zero** amendments — surfacing invented ones is the crying-wolf failure mode.

## The flow — two modes, sequential, two gates (Reconcile folded into the ship gate)

**`08-refactor assess`** — read-only health check (stops at Gate 1). **`08-refactor sprint N`** — the full pass.
Craft lives in the references; load each as its step begins.

1. **ASSESS (read-only, sequential).** One health pass over `src/**` + the realization docs. Signals: god
   files/functions (line counts), **duplication**, **dead/unused exports**, complexity hotspots, circular deps,
   test-to-code ratio + **coverage gaps on likely targets**, **doc↔code drift** (`system.md` modules/entities vs code),
   **constraint conformance** (does the realization still honor `architecture-constraints.md`?), guardrail-clustering.
   Apply the **Decision Matrix** — Refactor / Rewrite / Pivot / Accept; a **Rewrite** or **Pivot stops** and routes to
   `/03`+/04` or `/00 reflect`. Write `docs/refactoring/health-assessment-sprint-NN.md`. **`assess` mode ends here →
   Gate 1.** (`references/health-assessment.md`.)
2. **SCOPE + SAFETY NET.** Classify each finding (Targeted / Cross-cutting / **Structural = plan-only** /
   Modernization). **Two-Hats-defer** every non-maintainability finding to its owner (bug→`/05`, vuln→`/07`,
   feature→`/04`, arch-change→`/03`→/04`). Establish the **behavior oracle**: the existing suite (green at the
   pre-refactor commit) **+** characterization tests for any uncovered target **+** the anti-tautology check. Write
   `docs/refactoring/refactor-plan-sprint-NN.md`.
   **>>> GATE 1 — Diagnose + safety net:** present findings + scope + the oracle; wait for PROCEED / ADJUST.
3. **EXECUTE (baby steps, test-guarded).** Per plan: one **explicitly-typed** move → run the oracle + full suite →
   **commit** `refactor(scope): …`, or **revert** immediately on any red (don't debug — revert, rethink, retry). Never
   touch out-of-scope files; never change behavior; small atomic commits. Structural migrations are **plan-only**
   (Strangler Fig through the normal `/03`→/04` chain — not executed here). (`references/refactor-execution.md`.)
4. **RECONCILE (the appender step — folded into Gate 2).** Route by the keystone test *which file fixes it?*
   - **Local (the common case).** Correct the **realization** docs to match the refactored code — `system.md`
     (component inventory, C4, module boundaries), feature specs, `design-system.md` component names, and **prune
     resolved guardrails**. A code↔doc drift is **local** — **no amendment row** (the `03` Step-1b precedent).
   - **Declaration (the appender case).** Where the refactor surfaces that a **declaration** is wrong/unsatisfiable —
     a `stated` constraint the realization cannot honor, a capability the code proves dead-at-scope — run **Reconcile**
     → append `amendment-log.json` rows: **Tier-1** auto (one defensible answer, no behavior/tech change — rare) /
     **Tier-2** gated (named-tech · scale · a stakeholder-opinion call — amend the constraint **and** a resolving ADR,
     `max+1` from `03`) / **Tier-3** deferred (scope → `/00 reflect`). **Escalate when uncertain.** Batch Tier-2 into
     the single Gate 2. (`references/reconcile-refactor.md`.)
5. **VERIFY + REPORT.** Full suite green (behavior preserved); before/after health metrics; **verdict** —
   **CLEAN** (all addressed) / **PARTIAL** (some deferred) / **BLOCKED** (revealed a structural/declaration change → a
   `/03`→/04` cycle) / **ACCEPT** (nothing warranted). Write `docs/refactoring/refactor-report-sprint-NN.md`.
   **>>> GATE 2 — Ship (Reconcile folded in):** present the report + before/after metrics + the batched Tier-2
   amendments; wait for PROCEED / ADJUST / a decision on each amendment.

## The behavior-preservation guarantee (the honesty gate — never fake a green)

Before you mark any move done, **prove behavior did not change** — a layered oracle, each layer objective:

1. **Green before and after.** The existing test suite passes at the pre-refactor commit **and** after the move
   (a positive executed-test count — never "0 tests, exit 0").
2. **Oracle unchanged.** You **never edit the pre-existing tests** to make them pass — that is the single most
   dangerous cheat (a refactor that rewrites its own oracle proves nothing). New characterization tests are additive;
   the golden master is read-only to you.
3. **The oracle bites.** The suite must **fail on a broken implementation** — if a mutated version still passes, the
   test is tautological and is not a safety net (write a real one first).
4. **Characterize the gaps first.** For any refactor target the existing suite does not cover, write **characterization
   tests** (golden-master) capturing *current* behavior — bugs included (Two Hats) — **before** touching the code.

If you cannot establish a biting oracle for a target, **do not refactor it** — say so and stop. LLM refactors silently
alter behavior in a meaningful fraction of edits; the oracle is the only defense.

## Write-path (corruption is the highest-rated risk — follow exactly)

- **Writes** `src/**` (refactored code + characterization tests) · `docs/refactoring/{health-assessment,refactor-plan,
  refactor-report}-sprint-NN.md`.
- **Reconciles (writes, LOCAL)** `docs/architecture/system.md` + `specs/**` · `docs/design/**` ·
  `.claude/rules/quality-guardrails.md` — realization drift, **not** amendments.
- **Appends** `docs/spec/amendment-log.json` — **only** for a declaration contradiction; schema per
  `shared/spec-amendment-protocol.md` (`id` `max+1` · `tier` · `disposition` · `source_quote` preserving the exact
  declaration text · `resolved_by` · **no `date`**).
- **Amends** `docs/spec/architecture-constraints.md` **only** through an approved **Tier-2** (the tech-mandate flow —
  the constraint line **and** a resolving ADR). **Never** edits `docs/spec/capabilities/**` (REQ text) — a requirement
  changes only through `/00` (a `08` scope finding is a **Tier-3 deferred** row routed there).
- **Requests `max+1`** for any refactoring ADR — `03` is the **sole ADR allocator**; `08` **never** allocates a REQ-ID.
- **Reference, never copy** — cite `REQ-NNN`/`ADR-NNN`; never paste REQ prose (`shared/spine-boundary.md`).

## Progress checklist (copy this and track as you go)

- [ ] ASSESS — sequential health pass: duplication · dead code · complexity · doc↔code drift · constraint conformance ·
      guardrail-clustering; Decision Matrix applied (Rewrite/Pivot → stop + route); health-assessment written
- [ ] SCOPE + SAFETY NET — findings classified; **non-maintainability findings Two-Hats-deferred** (bug→/05 · vuln→/07
      · feature→/04); the behavior oracle established (existing suite green at baseline + characterization for gaps +
      the anti-tautology check); refactor-plan written
- [ ] **>>> GATE 1 — present diagnosis + scope + safety net; wait for PROCEED / ADJUST <<<**
- [ ] EXECUTE — baby steps: one **typed** move → oracle + full suite green → commit, or **revert** on red; out-of-scope
      files untouched; behavior unchanged; structural migrations left plan-only
- [ ] RECONCILE — **local** realization fixes (system.md / specs / design / guardrails) for code↔doc drift; a
      **declaration** contradiction → an `amendment-log.json` row (T1 auto / T2 gate + resolving ADR / T3 defer),
      escalate-when-uncertain, Tier-2 batched into Gate 2
- [ ] VERIFY + REPORT — full suite green (behavior preserved: oracle unchanged + biting); before/after metrics;
      verdict CLEAN / PARTIAL / BLOCKED / ACCEPT; refactor-report written
- [ ] **>>> GATE 2 — present report + metrics + batched Tier-2 amendments; wait for PROCEED / ADJUST / decisions <<<**
- [ ] Integrity: **behavior preserved** (oracle blob-unchanged, green, biting) · smells actually removed · docs
      reconciled to code · **no** amendment row for a local drift · a declaration row only when a declaration is wrong ·
      ADR `max+1` (never a REQ-ID) · `capabilities/**` untouched

## Reads / Writes

**Reads:** `src/**` (the refactor target, at the pre-refactor commit) · `docs/architecture/system.md` + `specs/**` +
`adr/**` (realization, to reconcile) · `docs/spec/architecture-constraints.md` + `specification.md` +
`capabilities/**` (declarations, read-only unless amending) · `docs/planning/sprints/sprint-NN.md` ·
`docs/design/**` · `docs/quality/qa-report-sprint-NN.md` (context) · `.claude/rules/quality-guardrails.md` (clustering)
· `package.json` (dependency health) · git state.
**Writes:** `src/**` · `docs/refactoring/{health-assessment,refactor-plan,refactor-report}-sprint-NN.md` · **reconciles**
`docs/architecture/**` + `docs/design/**` + `.claude/rules/quality-guardrails.md` · **appends**
`docs/spec/amendment-log.json` · **amends** (Tier-2 only) `docs/spec/architecture-constraints.md`. **Never** writes
`docs/spec/capabilities/**`.

## References (load when the step needs them)

- `references/health-assessment.md` — the **sequential** health pass (the signal list, no parallel subagents) + the
  Decision Matrix + guardrail-clustering + the before/after metric set.
- `references/refactor-execution.md` — baby steps + explicit move-typing + the **behavior-preservation oracle**
  (unchanged · green-both · biting · characterize-the-gaps) + Two Hats + the HALT conditions.
- `references/reconcile-refactor.md` — the **local-vs-declaration** routing (which-file-fixes-it) + the INLINE Reconcile
  appender + the tiers + the tech-mandate flow (amend the constraint + a resolving ADR, `max+1` from `03`).
- `references/refactoring-catalog.md` — the catalog of moves with AI-prompt patterns + per-move verification.
- `shared/spec-amendment-protocol.md` — the amendment tiers + the row schema (you are an appender); repo-root-relative.
- `shared/spine-boundary.md` — declaration vs realization (the keystone — why a code↔doc drift is local); repo-root-relative.
- `shared/subagent-protocol.md` — why `08` stays **sequential** (build and refactor spawn nothing); repo-root-relative.

## Next skill

- **CLEAN / ACCEPT** → `/05-reviewer` (re-verify if behavior-adjacent) · the next sprint · `/00-discovery reflect`.
- **PARTIAL** → address the deferred items in a later `/08-refactor` pass, or route each to its owner.
- **BLOCKED** → a structural/declaration change: the routed owner (`/03-architect` → `/04-builder` for a migration;
  `/00-discovery reflect` for a deferred scope amendment), then re-assess.
