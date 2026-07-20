# iteration-data-1 — data-architecture cases: validation & run record

Grader: `.agents/skills/03-architect/evals/check_architecture.py` (the data-case path `grade_data_arch`).
Design record: `_artifacts/data-architecture-phase1-design.md`. Plan: `_artifacts/data-architecture-phase1-implementation-plan.md`.
Branch: `worktree-data-eval-cases`.

## 1 · Grader self-test (`--self-test`) — ALL GOOD

- **S18 (verify-live ADR citation):** 7/7 scenarios — ideal passes; uncited/missing fire; no-decl is N/A; the
  three Task-2 additions all green (qualified label links + validates; qualified label FIRES on an uncited ADR;
  uppercase bare label links the lowercase record).
- **Data (DA-T01..T08):** 22/22 scenarios — both ideals (data-modules, data-nogate) pass every check; each
  single-element degenerate flips exactly its target check (the mutation principle, design §6). Includes the
  DA-T06 conditional ADDITION degenerate (LLM-issued queries added ⇒ the driver-layer clause fires) and the DA-T07
  N/A direction (no spine deletion-promise + no derived-reach paragraph ⇒ still PASSES). `durable-vs-vendor` bites
  cleanly (ideal all-clauses True; the split-paragraph deletion fires) — the plan's pre-authorized demote was NOT
  taken.

## 2 · Real-output validation (zero-token) — the smoke tree

`--case data-modules --fixture-docs …/beacon-agent/docs` over the GREENLIT smoke output
(`smoke-2026-07-18/with_skill/outputs`): **14/14**.

Notable in-evidence:
- **S18 PASS (the flip):** `cited=['ADR-002.md→pgvector', 'ADR-005.md→bge-m3,pgvector']; uncited=none`. Pre-fix
  this tree reported the silent `N/A — no verify-live tech declared` (the qualified-label bug, SMOKE-RESULT.md
  §⚠️); the Task-2 slug normalization makes the mechanical label↔record linkage validate.
- **DA-T07:** `no user-facing deletion promise in the spine => pairing N/A` (the pairing gates on the spine's
  promise line — structure, not vocabulary).
- **DA-T05:** `stages=[1,2,3,4,6]; … stage [3] committed; why-not-simpler=True` (the Stage≥3 escalation clause).
- **DA-T04:** candidate ADR-002.md, all six rubric clauses True.

**Plan-vs-actual discrepancy (benign):** the plan predicted DA-T06 would read `no LLM-issued queries … N/A`. The
real smoke output *does* issue LLM queries and *does* pair a driver-layer read-only rule, so DA-T06 passes on the
stronger path (`LLM-issued queries present; driver-layer read-only=True`) rather than the N/A path. Check verdict
unchanged (PASS); 14/14 holds; no grader change.

**Environment note:** `_artifacts/` is gitignored, so the calibration trees live only in the primary worktree, not
in `.claude/worktrees/data-eval-cases`. Validation graded scratch copies of the primary worktree's trees with the
branch grader — the primary worktree's calibration records were left untouched.

## 3 · No-drift proof — old (main) vs new grader over every saved tree

`git show main:…check_architecture.py` (pre-change) vs the branch grader; grading.json compared:

| Saved tree | case | result |
|---|---|---|
| iteration-1/clean-constraint/baseline | clean-constraint | STABLE |
| iteration-1/clean-constraint/with_skill | clean-constraint | STABLE |
| iteration-1/forbidden-token/baseline | forbidden-token | STABLE |
| iteration-1/forbidden-token/with_skill | forbidden-token | STABLE |
| iteration-1/underspecified-constraint/baseline | underspecified-constraint | STABLE |
| iteration-1/underspecified-constraint/with_skill | underspecified-constraint | STABLE |
| iteration-3/clean-constraint/with_skill | clean-constraint | STABLE |

All 7 STABLE — the S12 refactor (shared `_attestation_recorded`) is behavior-identical, and S18 normalization is a
no-op on trees that declare no verify-live techs (every TeamPulse tree).

## 4 · Fixture sanity (bare-seed grading — the grader is not vacuous)

Grading each fixture's pure spine seed (no `docs/architecture/`), default `--fixture-docs`:

- **`beacon-data` / `--case data-modules`: 3/14.** Only amendment-log-valid (the seed's empty
  `{"amendments": []}`), capabilities-content-identical (seed == fixture), and S18-N/A pass; every realization
  check (system.md, ADR registry, attestation, spec+VC, DA-T01…T07) fails on the bare spine. _(The plan predicted
  2/14; the actual 3/14 includes the valid empty amendment-log — a benign plan miscount, not a grader issue.)_
- **`beacon-nogate` / `--case data-nogate`: 5/11.** amendment-log-valid, capabilities, selectivity (no substrate
  rows on the empty tree), False-positive-bound (0 amendment rows), and S18-N/A pass; core realization + DA-T01 +
  DA-T04 fail. Matches the plan.

Both confirm the grader bites on a bare spine (realization checks fail) while the spine-integrity and
N/A-conditional checks correctly pass.

## 5 · A/B run (iteration-data-1) — with_skill vs baseline

Four native Agent-tool `general-purpose` **Sonnet** arms (the smoke recipe, not the CLI scripts). Each `with_skill`
arm loaded `03-architect/SKILL.md` in full, ran `init` + `sprint 1` autonomously past both gates, and ran the
Reconcile Pass-2 from a **real nested `fsd-reconciler` subagent** (depth-1 nesting is available here — the prompt's
resilience fallback was unused). Baselines did the same task with no skill.

| Case | with_skill | baseline | lift |
|------|:----------:|:--------:|:----:|
| `data-modules` | **14/14** | 5/14 | +9 |
| `data-nogate`  | **11/11** | 6/11 | +5 |

**Both with_skill arms pass every non-N/A check.** N/A-by-design: on `data-nogate`, S18 is N/A (no verify-live tech
on a declined line). On `data-modules`, DA-T06's driver-layer clause and DA-T07's deletion-pairing are *satisfied*
(not N/A) — the arm's realization actually issues LLM queries (with a read-only driver rule) and the spine promises
profile deletion (with derived-reach).

**Need-gate behavior (the point of `data-nogate`):** the with_skill arm **realized retrieval at Stage 0**
(cache-and-stuff — the handbook fits in context, no RAG pipeline) and **declined memory** via a Category: memory
ADR (considered-and-rejected, not a silent gap) and grounded-writes (undeclared + read-only Constitution). Zero
amendments — the reconciler correctly rejected the arm's initial over-prediction that "agnostic — architect's
choice" needed flesh-out (explicit delegation ≠ a missing placeholder).

**Baseline gap (the lift is structural, per the framework principle):** both baselines *also* need-gated correctly
(the `data-nogate` baseline declined both modules; its selectivity + DA-T01 passed) — a strong baseline catches the
same calls. The lift is the **structured contract the next skills consume**: baselines wrote ADRs without an
`adr/README.md` index, feature specs under `features/` not `specs/`, no reconciler attestation, no DA-T04 datastore
ADR, and the content clauses (DA-T02/T03/T05/T06/T07) absent — and over-fired amendments (2–3 loose rows vs the
skill's structured 0–6).

### Triage (grader-bug-first; the plan's Step-4 discipline)

Three checks a *correct* arm failed — each a grader bug, fixed + reproduced as a `_self_test_data` scenario in
different words (never a fixture tweak), degenerates kept firing, anti-tautology grep clean:

1. **DA-T04 exit-cost too literal** (`data-modules` with_skill). The arm stated reversibility as "migrating … is a
   real project — accepted because X" (the teeth's own sanctioned form); the regex only matched
   one-way/two-way/exit-cost/reversib/lock-in. Broadened to a general migrate/switch-is-costly pattern. Commit
   `124534b`. (13→14/14.)
2. **DA-T04 could not recognize a "no datastore" decision** (`data-nogate` with_skill). ADR-002 walked every DA-T04
   clause (even labeled them) but *chose no store*, so the token-based candidate gate couldn't find it. Broadened
   the candidate gate to also recognize a rubric-walked "no datastore" outcome; clauses still bite; the baseline
   (no datastore decision at all) still finds no candidate. Commit `ff593ac`.
3. **Selectivity false-positive on "in-memory"** (`data-nogate` with_skill). An ephemeral `| In-memory run state |`
   Data-model row matched `memor` — but in-memory/in-process state is the *opposite* of a persistent memory
   substrate. Excluded ephemeral in-memory/in-process/transient rows. Commit `ff593ac`. (9→11/11.)

No with_skill DOCTRINE failure surfaced (nothing for the design record). `durable-vs-vendor` was never demoted.

### Execution notes

- **Reconciler nesting works** — every with_skill arm spawned a real `fsd-reconciler` subagent.
- **Arms 2–4 were run concurrently, not strictly one-at-a-time**, after arm 1 proved the recipe: the workspaces are
  independent and a flaky `claude-opus-4-8` classifier outage made "launch while available" the robust choice.
- Windows/EOL: run workspaces are gitignored under `_artifacts/skills-eval/**`; these run records are `git add -f`'d.
