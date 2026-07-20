# Final Discriminating Evals — Research Synthesis (§10, pre-design)

> Companion to [`final-evals-design.md`](final-evals-design.md). This file is the **research pass**: what the
> existing eval machinery gives us for free, the one keystone discovery that makes the integration test cheap, a
> coverage map of the five master-plan verification tests, and the reusable-assertion inventory. No decisions here —
> the design doc proposes; this doc grounds it. Read alongside `final-evals-continuation.md` (the handoff) and the
> master plan §Verification + §Migration 10 + §Eval strategy.

## 1. The unit-eval pattern (locked across `00`–`status` — what §10 reuses)

Every built skill carries an `evals/` folder with the same four-part shape, driven by **skill-creator's A/B method**
(deterministic grader, **no LLM judge**):

| File | Role |
|------|------|
| `build_fixture.py` | Assembles a **git-repo fixture** from `fixtures/` into an arm's `outputs/` (recreated fresh; Windows read-only-`.git` safe; `core.autocrlf false` for deterministic diffs). Often **self-checks** the planted condition and fails loudly. |
| `evals.json` | Case defs: `prompt`, `expected_output`, `files`, `assertions[]` + a `run_notes` describing the two arms. |
| `check_*.py` | The **deterministic grader** → writes `grading.json` (`{expectations:[{text,passed,evidence}]}`). File/JSON assertions + `git diff` + (where behavior matters) `node --test`. |
| `README.md` | Documents the A/B, the **grader-validation table** (hand-ideal + degenerate negatives), and the iteration-1 with_skill-vs-baseline numbers. |

**Invariants carried forward** (from the continuation + memory):

- **Deterministic grader; no LLM judge.** Validate on **hand-ideals AND real arms AND degenerate negatives** so the
  discriminators are provably non-vacuous (`feedback_grader_validate_on_real_outputs`,
  `feedback_mutation_grader_robustness`).
- **Workspaces live OUTSIDE `.agents/skills/**`** — `_artifacts/skills-eval/…`, gitignored (the `with_skill`
  write-refusal). Scripts live in the repo; run-workspaces do not.
- **The lift is STRUCTURAL** (`feedback_framework_skill_lift_is_structural`): a strong baseline also produces a
  spine / an architecture / a status summary. Grade **the structured contract the next skill consumes**, not prose.
- **Fresh-spawner isolation** for the subagent-spawning seats; **relax the harness `<SUBAGENT-STOP>` for `03`/`05`/
  `07`**. `00`/`01`/`02`/`04`/`06`/`08`/`status` are sequential (nothing to relax).
- **No auto-push** (`feedback_no_auto_push`); force-add the `_artifacts/*-continuation.md` + design/research docs with
  the commit, everything else under `_artifacts/` stays gitignored.

## 2. The keystone discovery — the chain is already latent in the fixtures

The single fact that makes the flagship integration test cheap and honest:

**`00-discovery/evals/fixtures/rich-spec/PRD.md` IS the TeamPulse PRD.** Feed it through `00 intake` and it produces a
spine that structurally matches `01-planner/evals/fixtures/teampulse/docs/spec/**` — the same Constitution
(async-over-sync, digest-is-the-one-artifact, timezone-fair, EU-residency, passwordless, zero-training), the same
REQ-001…010 registry across `capabilities/{standups,team,digest}.md`. And that teampulse spine is exactly what
`01 → 02 → 03 → 05 → status` consume as their seeded inputs. **One domain threads the entire chain.**

Consequence: the integration test is **seam-welding** — run the real skills over one seeded comprehensive spec and
watch the handoffs compose — and it can **reuse all four unit graders' logic** (`check_spine`, `check_backlog`,
`check_design`, `check_architecture`) plus **`/status` as an integrity oracle**, rather than inventing new checks.

### The planted Tier-2 is a fixture swap, not a new invention

The clean PRD's Constraints say *"PostgreSQL. (The team has committed to this.)"* — a **client-server** datastore that
satisfies the multi-instance shared-store availability requirement (a clean envelope). `03-architect`'s
`teampulse-sqlite` fixture instead mandates **SQLite (embedded, single-file)** while *also* stating the availability
requirement *"two or more stateless instances behind a load balancer … share one datastore"* — a **computed
contradiction** (an embedded single-file DB cannot be shared across instances). `check_architecture.py` already grades
this: a **Tier-2** `amendment-log.json` row, `disposition ∈ {gated, approved, pending}` (never `auto-applied`), citing
the datastore, `resolved_by` an ADR whose **Decision** names a client-server DB.

**So the integration seed = the TeamPulse PRD with the SQLite swap**: the conflict is *declared at intake* (00 records
the SQLite mandate + the shared-store availability requirement faithfully — it is a valid-looking declaration, not 00's
to resolve), *carried untouched through 01 and 02* (both datastore-agnostic), and *surfaced + resolved at 03's
Reconcile*. A regression anywhere — 00 "helpfully" fixing it, 03 silently swapping the DB in prose with no gated row —
fails the grader. This is the **cross-skill discriminator**: the amendment channel working across four seats.

## 3. Coverage map — the five master-plan verification tests

The continuation flags that the per-skill unit evals "isolate one seat"; §10 is the *cross-skill* safety net. Mapping
each of the plan's five tests to what already exists vs. what is genuinely new:

| # | Test (plan §Verification) | Status | Where |
|---|---|---|---|
| **1** | **Spec-first integration** — `00 intake → 01 → 02 → 03`; spine populated; registry↔leaf integrity; planted Tier-2 → gated row + ADR; backlog + frozen snapshot; **no** retired artifacts | **GENUINELY NEW** — no unit eval chains the seats | The flagship §10 eval |
| **2** | **Isolation** — `05` on a planted violation → attestation present + valid; caught it; parent transcript has no builder reasoning | **COVERED (deterministic half)** by `05-reviewer` `isolation` + `defective-fix`; the transcript-absence half is **manual by design** (`subagent-protocol.md`). A `loop-integration` run already chained `04↔05` on real artifacts | `05-reviewer/evals` + its README §"Build↔review loop" |
| **3** | **Governance/markers** — `06` blocks on a `pending` amendment **and** a surviving `[NEEDS CLARIFICATION]` | **COVERED** by `06-release` `blocked-spine` (SHIP verdict, blocked on AMD-003 `pending` + a marker) **and** `status` `blocked` (routes to resolve, not ship) | `06-release/evals` + `status/evals` |
| **4** | **Spine-collapse hedge** — an upstream pivot (change a constraint) → spine regenerates from charter/loop-doc intent **without shattering** downstream | **GENUINELY NEW but subtle** — hardest to make deterministic | Proposed optional §10 case |
| **5** | **Roll-up** — structured-emission evals green at each commit | **ALREADY TRUE** — every skill's README records iteration-1 with_skill greens | The 10 `evals/README.md` files |

**Reading:** the genuinely-new surface is **Test 1** (the flagship) and, optionally, **Test 4** (the hedge). Tests
2/3/5 are already deterministically covered by unit evals — §10's value for them is *composition* (does the governance
block fire on a state the *real chain* produced?) and *documentation* (a roll-up that points at the greens), not
re-deriving machinery the unit evals already own.

## 4. Reusable-assertion inventory (what the integration grader lifts)

Concrete assertions already implemented that `check_integration.py` can reuse (by importing or transcribing the
proven regex/JSON logic — the graders are single-file and dependency-free):

- **`check_spine.py`** — `find_root` (walk to `docs/spec/specification.md`); `parse_registry` (the `| REQ | … | file |`
  rows); `parse_blocks` (the `### REQ-NNN: … <!-- /REQ-NNN -->` delimited spans + `<!-- source: -->`); **registry↔leaf
  integrity** ("every registry REQ resolves to a block"); Constitution ≥3 items; `AGENTS.md` generated-header; `charter.md`
  JTBD.
- **`check_backlog.py`** — `parse_ledger` (header-driven REQ→epic/sprint/status); **every spine REQ in the ledger
  exactly once** (none dropped/duplicated); **no invented REQ-IDs**; execution-vocab-only status; **build-order** (foundation
  epic precedes consumer); sprint-01 **frozen Gherkin + Done When**; the two-status separation.
- **`check_design.py`** — (02) design-system + manifest referencing REQs; the DM-ID manifest.
- **`check_architecture.py`** — the **token-in-named-field set-match** (`DB_CLIENT_SERVER`/`DB_EMBEDDED` etc.);
  `tier2_rows`; **the gated-row + resolving-ADR check** (the Tier-2 discriminator); **REQ→spec coverage** (S9);
  **DM→spec forward coverage** (S10); ADR contiguity (max+1); the reconciler **context attestation** (S12).
- **`check_status.py`** — `truth_changed` (the **read-only-w.r.t.-truth** `git diff` proxy); `integrity_verdict`
  (PASS/FAIL); `next_command` (the routed `/NN` slug); `amendment_counts` + `marker_count` (governance blockers);
  `agents_faithful` (the generated-view projection).

**`/status` as oracle.** The continuation's explicit preference — *"prefer running `/status` and grading its
emission where it fits"*. After the chain, running `/status` and asserting its `CLAUDE.md § Current State` emission
(integrity **PASS**, 0 unexpected blockers, the routed next command) **composes** the `status` seat into the
integration test as the integrity/routing assertion — instead of the grader re-implementing integrity logic. Belt-and-
suspenders: the grader *also* checks registry↔leaf directly (cheap, and it de-risks a `/status` mis-run).

## 5. Driver mechanics — how a multi-skill chain runs (the one novel harness piece)

The unit evals fit skill-creator's **one-prompt-per-arm** mold. A 5-stage chain does not — it needs **five sequential
fresh subagents sharing one workspace**. The honest realization (matches the framework's *fresh-spawner* +
*handoff-via-artifacts* doctrine):

1. `build_fixture.py --out <ws>/outputs` seeds the workspace with **only** the comprehensive PRD (+ `git init`, one
   commit = the pre-chain root).
2. **Fresh subagent** → *load `00-discovery`, run `intake` over `PRD.md`* → writes the spine.
3. **Fresh subagent** → *load `01-planner`, decompose* → writes backlog + sprints.
4. **Fresh subagent** → *load `02-designer`, sprint 1* → writes design + manifest.
5. **Fresh subagent** → *load `03-architect`, sprint 1* (relax `<SUBAGENT-STOP>`; its reconciler subagent runs) →
   writes architecture + the amendment rows.
6. **Fresh subagent** → *load `status`, run `/status`* → writes `CLAUDE.md § Current State` + `AGENTS.md`.
7. `check_integration.py --outputs <ws>/outputs` grades the **composed end-state** + the `/status` emission.

Each dispatch is a **fresh spawner** seeded with only the workspace path + "load skill NN, run its verb" — never the
prior stage's reasoning. That is the honest test of *handoff-via-artifacts*: if the chain composes, it composes because
each seat read the shared spine, not because one context remembered another. (The `05-reviewer` README's
`loop-integration` run is the precedent — it already chained `04↔05` on real artifacts across fresh spawners.)

**Not an A/B lift test.** Each seat's lift is already proven per-skill; re-running a no-skill 4-seat chain would just
re-test those lifts at 4× the cost. The integration test's job is **composition-correctness**, so its "negative" arm is
a set of **hand-crafted degenerate composed-states** (a chain output missing the gated row; one that created a `US-NNN`
file; one with a broken registry↔leaf link; one that dropped a spine REQ) that the grader must **fail** — the
`feedback_grader_validate_on_real_outputs` discipline applied to a *composition*. One optional baseline chain can be run
for completeness, but the core validation is degenerate-negative-based.

## 6. Home + naming

The integration harness is **cross-skill**, so it does not belong under any one `.agents/skills/<NN>/evals/`. The
natural home is **`docs/eval-methodology/integration/`** (alongside the existing `harness-reference/`) — Layer A
eval-methodology. Run-workspaces stay under `_artifacts/skills-eval/integration/` (gitignored), same as the unit
evals. Naming follows the locked conventions: `sprint-01` lowercase zero-padded; `REQ-/ADR-/AMD-NNN`; TeamPulse domain.

## 7. Open questions the design doc must settle (surfaced, not decided here)

1. **Scope of the final commit.** Flagship-only (Test 1 + `/status` composing Tests 3+5), or flagship **+** the Test-4
   spine-collapse hedge, or flagship **+** a chained `04→05` isolation leg (Test 2 end-to-end)? Each added leg is real
   cost + variance; Tests 2/3/5 are already unit-covered.
2. **`/status` composition depth.** Compose `/status` as the integrity+routing oracle (recommended), or re-implement
   integrity in the integration grader directly, or both (belt-and-suspenders — recommended)?
3. **Test-4 determinism.** If in scope, what is the deterministic proxy for "regenerates without shattering" — charter
   JTBD unchanged + registry stays integral through the pivot + the change logged as an amendment (not a silent
   rewrite)? Or is Test 4 better left as a documented manual hedge?

These are the design gate's decisions. → [`final-evals-design.md`](final-evals-design.md).
