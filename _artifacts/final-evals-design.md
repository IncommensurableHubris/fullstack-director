# Final Discriminating Evals — Design (§10, cross-skill integration harness)

> The cross-skill integration harness — the final migration commit. Grounded in
> [`final-evals-research.md`](final-evals-research.md).
>
> **DESIGN GATE — APPROVED 2026-07-03 at MAXIMAL scope.** The user selected the flagship **plus all three optional
> legs**, i.e. the full plan §Verification surface: **Test 1** (flagship spec-first chain) · **Test 2** (chained
> `04→05` isolation) · **Test 3** (Tier-3 governance) · **Test 4** (spine-collapse hedge) · **Test 5** (roll-up,
> documented). Structured as **one `check_integration.py` with four `--case`s** (`spec-first` · `isolation-chain` ·
> `governance` · `spine-collapse`) — the `check_status.py`/`check_review.py` multi-case idiom. §6 below is superseded
> by this approval; §§2–5 (the flagship + validation discipline) stand and the three legs extend them.

## 1. The deliverable

A **cross-skill integration harness** at `docs/eval-methodology/integration/` (Layer A eval-methodology, alongside
`harness-reference/`), mirroring the unit-eval four-part shape:

```
docs/eval-methodology/integration/
  README.md                 # the A/B-style doc: the chain procedure, the grader-validation table, the run record
  build_fixture.py          # seeds a workspace with ONLY the comprehensive PRD (+ git init, one root commit)
  check_integration.py      # the deterministic grader over the COMPOSED end-state + the /status emission
  fixtures/
    teampulse-sqlite-prd/PRD.md      # the seed: TeamPulse PRD with the SQLite Tier-2 plant latent at intake
    _negatives/                      # hand-crafted degenerate COMPOSED states for grader-validation (see §5)
      broken-registry/…  silent-swap/…  retired-artifacts/…  dropped-req/…
```

Run-workspace: `_artifacts/skills-eval/integration/iteration-N/…` (gitignored). Scripts committed; workspace not.

## 2. The flagship eval — `spec-first` (Test 1, + `/status` composing Tests 3 & 5)

**Procedure** (the driver, per research §5 — five fresh subagents over one shared workspace, then grade):

| Stage | Fresh subagent | Writes |
|------|-----------------|--------|
| seed | `build_fixture.py --out <ws>/outputs` | `PRD.md` + `git init` (root commit = pre-chain) |
| 1 | load `00-discovery`, run **intake** over `PRD.md` | the spine (`docs/spec/**`, `AGENTS.md`, `charter.md`) |
| 2 | load `01-planner`, **decompose** | `docs/planning/backlog.md` + `sprints/sprint-01.md` |
| 3 | load `02-designer`, **sprint 1** | `docs/design/**` + `approved/sprint-01/manifest.md` |
| 4 | load `03-architect`, **sprint 1** (relax `<SUBAGENT-STOP>`) | `docs/architecture/**` + the Tier-2 amendment rows |
| 5 | load `status`, run **/status** | `CLAUDE.md § Current State` + re-emitted `AGENTS.md` |
| grade | `check_integration.py --outputs <ws>/outputs` | `grading.json` |

The Tier-2 gate in stage 4 is **pre-approved in the dispatch prompt** (the `06`-precedent: an eval pre-grants the single
human gate so the chain does not hang) — approving SQLite→client-server, so the row lands `approved` + a resolving ADR.

**The composition invariants `check_integration.py` asserts** (each maps to a plan §Verification clause; logic lifted
from the named unit grader — research §4):

1. **Spine tree populated** — `specification.md` (Constitution ≥3 + a REQ registry ≥6 rows) + `capabilities/*.md` with
   delimited REQ blocks + `design-intent.md` + `architecture-constraints.md` + valid `amendment-log.json`.
   *(check_spine)*
2. **Registry↔leaf integrity holds — via the `/status` oracle AND directly.** Assert `/status`'s emitted
   `Spine integrity: PASS` **and**, belt-and-suspenders, every registry `File` resolves + carries its `<!-- /REQ-NNN -->`
   block (no orphan/dup IDs). *(check_status integrity_verdict + check_spine registry↔leaf)*
3. **REQ-ID allocation coherent across the chain** — every REQ referenced by the backlog, the sprint snapshot, the
   design manifest, and the architecture specs exists in the registry; the backlog carries **every** spine REQ exactly
   once (none dropped/duplicated/invented). The corruption guard, across seats. *(check_backlog)*
4. **The planted Tier-2 surfaced + resolved (THE cross-skill discriminator)** — an `amendment-log.json` row: `tier 2`,
   `disposition ∈ {gated, approved}`, `source_quote` citing the SQLite/datastore contradiction, `resolved_by` an ADR
   whose **Decision** names a client-server DB — **not** `auto-applied`, **not** silent prose. *(check_architecture
   tier2 + resolving-ADR)*
5. **Backlog ledger + frozen sprint snapshot written** — ledger maps REQ→epic→sprint→status (execution vocab); build-
   order (foundation epic precedes consumer); `sprint-01.md` carries a frozen outcome-Gherkin snapshot + a `Done When`.
   *(check_backlog)*
6. **Handoff fidelity** — 02's required manifest DM-IDs are covered by 03's feature specs (S10); every in-scope sprint
   REQ is covered by ≥1 feature spec (S9); the architecture references the spine by REQ-ID, not copied prose.
   *(check_architecture)*
7. **Retired-artifacts guard** — **no** `docs/planning/requirements-brief.md`, **no** `docs/planning/user-stories/US-*.md`
   anywhere in the composed tree. A regression to the old flat topology fails here. *(new, cheap, discriminating)*
8. **`/status` routes correctly (Tests 3 + 5 composed)** — after the chain, `/status`'s `Next command:` is the correct
   next SDLC seat (`/04-builder`, the state being "03 done, sprint-01 architected, not yet built"), and its governance
   counts reflect the *real chain state* (the Tier-2 resolved → `approved`, so **0 pending/deferred** unless a marker
   survives). *(check_status next_command + amendment_counts + marker_count)*

**Why these are the lift** (research §1 doctrine): none is "did a seat do good work" — each is a **cross-skill handoff
a later seat can mechanically read**: a `gated`/`approved` row `06` would block on, a frozen snapshot `04`/`05` verify
against, a registry `/status` integrity-checks, a manifest→spec coverage link `04` funnels through. The discriminator
is *composition*, exactly what no unit eval covers.

## 3. Governance (Test 3) — composed via `/status`, not re-run

Test 3 ("06 blocks on a pending amendment + a surviving marker") is **already deterministically owned** by
`06-release/blocked-spine` (SHIP verdict, blocked on AMD-003 `pending` + a `[NEEDS CLARIFICATION]` marker) and
`status/blocked` (routes to resolve, not ship). **Recommendation: do not re-run a full `06` in the integration
harness.** Instead, the flagship's stage-5 `/status` asserts the *routing contract* on the real chain state
(invariant 8), and the README's roll-up (Test 5) points at the two committed unit cases as the governance evidence.
This avoids redundant, expensive machinery while still proving the cross-skill governance path is wired.

*(If desired as a hardening extra: a second integration case where stage 4's Reconcile surfaces a Tier-3 scope finding
that `01`/`03` defer as `pending` — leaving a real pending amendment — then `/status` blocks and routes to
`/00-discovery reflect`, and a `06` dispatch BLOCKs. This is Test 3 end-to-end on chain-produced state. It is the
lowest-value add of the options, since `blocked-spine` already nails it — flagged, not recommended.)*

## 4. Isolation (Test 2) — covered by unit evals; optional chained leg

Test 2's deterministic half (attestation present + valid; caught the defect) is **owned by `05-reviewer`'s `isolation`
+ `defective-fix`**; the transcript-absence half is **manual by design** (`subagent-protocol.md` — Pass-2 judgment is
never deterministically graded). The `05` README's `loop-integration` run already chained `04↔05→04→05` on real
artifacts across fresh spawners and converged (FIX REQUIRED → fix → SHIP).

**Recommendation: document Test 2 as covered** (point at `05`'s two cases + the loop-integration record) rather than
re-running a full `04→05` leg on the flagship's `03` output. Rationale: the isolation property is already
deterministically graded; a chained leg mostly re-tests `05`'s lift at high cost/variance. *(Optional leg, if the user
wants end-to-end-on-chain-output isolation: after stage 4, dispatch `04` then a **fresh** `05` over the chain's real
sprint-01, and assert `05`'s attestation + a caught planted violation. Flagged, not recommended.)*

## 5. Grader validation (the honesty discipline — non-negotiable, per the conventions)

Before any chain run, `check_integration.py` is validated against a **hand-ideal composed state** AND **degenerate
negatives** (research §5), each a small fixture under `fixtures/_negatives/`:

| Composed state | Expect | Which assertion must fire |
|----------------|--------|---------------------------|
| **hand-ideal** (clean chain output) | all pass | positive control |
| **broken-registry** (a registry REQ's `<!-- /REQ-NNN -->` removed) | FAIL | invariant 2 (integrity, both the `/status` verdict + the direct check) |
| **silent-swap** (03 swapped SQLite→Postgres in prose, **no** gated row) | FAIL | invariant 4 (the Tier-2 discriminator — the killer) |
| **retired-artifacts** (a `docs/planning/user-stories/US-001.md` present) | FAIL | invariant 7 (retired-artifacts guard) |
| **dropped-req** (backlog omits a spine REQ) | FAIL | invariant 3 (allocation coherence) |

This proves the integration grader discriminates a **broken composition**, not just a happy path — the
`feedback_grader_validate_on_real_outputs` + `feedback_mutation_grader_robustness` discipline applied cross-skill
(stdout-only git parsing; byte-exact fixture handling; credit substance not delimiter).

## 6. Recommended scope (my call — one flagship, reuse-and-document the rest)

**Build the flagship `spec-first` eval only** (Test 1 + `/status` composing Tests 3 & 5), grader-validated on hand-ideal
+ four degenerates, run green on one chain, committed with a README that **documents Tests 2/3/5 as owned by the named
unit evals** and records the chain run. **Defer Test 4 (spine-collapse) to a documented manual hedge** unless you want
it built now.

Rationale: Test 1 is the *only* genuinely-new cross-skill surface; Tests 2/3/5 are already deterministic at the unit
level and gain little from re-running expensive multi-seat machinery; Test 4 is real but the hardest to make
deterministic and the least load-bearing (it is an intent-anchoring *hedge*, not a handoff the framework relies on
every run). This is the highest-value-per-token cut and matches the doctrine "grade the cross-skill handoffs."

**The one decision I need from you:** how much of the optional surface to include now (Test 4 hedge; the chained `04→05`
isolation leg; the Tier-3 governance case). I'll ask this as the gate below.

## 7. Build plan (post-approval — step 3 of the continuation)

1. Author `fixtures/teampulse-sqlite-prd/PRD.md` (the clean TeamPulse PRD + the SQLite plant made user-stated:
   datastore = SQLite embedded; availability = multi-instance shared-store, in the PRD prose so it is not architect-
   invented).
2. Write `build_fixture.py` (seed the PRD + `git init`; a self-check that the plant is present) and
   `check_integration.py` (the 8 invariants; reuse the unit graders' regex/JSON logic; compose `/status`).
3. Build the five `_negatives/` composed states; **grader-validate** (hand-ideal all-pass + each negative fires its
   assertion) — this is the deterministic safety net and it runs with **no chain execution**.
4. Run the flagship chain once (five fresh subagents; relax `<SUBAGENT-STOP>` for stage 4), grade green.
5. Write the integration `README.md` (procedure + grader-validation table + the run record + the Tests 2/3/5 coverage
   pointers).
6. Commit **locally** (`test(integration): cross-skill spec-first chain eval + grader` / `feat(evals): …`), force-add
   the design+research docs + this continuation, **do not push** (ask first), check in. The framework build is then
   complete → ready for the pre-push squash (plan §0) when the user asks to push.

## 8. Risks

- **Chain-run cost/variance** — mitigated by making the *grader-validation* (step 3) chain-free and deterministic; the
  live chain (step 4) is the demonstration, the negatives are the safety net.
- **A stage under-produces** (e.g., 02 writes no manifest) → the handoff-fidelity invariant (6) fails loudly rather
  than the grader silently passing a thin tree; each stage's dispatch prompt names its required outputs.
- **`/status` mis-run masking integrity** → invariant 2 checks registry↔leaf **directly too**, so a `/status` that
  wrongly reports PASS is caught by the direct check (belt-and-suspenders).
