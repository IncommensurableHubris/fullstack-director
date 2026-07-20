# Build discipline — turning realizations into a trustworthy slice

> Loaded by skill 04 (builder) during **BUILD** (steps 3–6 of the flow). The **method + the why**; `SKILL.md` is the
> spine and `references/build-handoff.md` is the craft of the output artifact. 04 reads the realization funnel
> (`03`'s specs + Verification Contracts, `02`'s design contract, `system.md`/ADRs, the `01` slice) as an **ambient
> contract** and writes **only** `src/**` + the handoff. It **never** edits the spine (`docs/spec/**`) or the
> realization docs (`docs/architecture/**`, `docs/design/**`) — an error in them is *escalated*, not patched (the
> three-way verdict below). Sequential, **no subagents, no user gate** — the context-isolation that matters is
> `05`'s, downstream (`shared/subagent-protocol.md`, repo-root-relative). 04's graded value is not "working code" (a
> strong builder writes that too); it is a **cold-reviewable, honest handoff + non-tautological tests**.

## The funnel and the write-boundary

Read the realization layer as the contract you build against; do not re-interpret the raw spine (`docs/spec/**`).
The chain has already refined intent into a buildable target: `01` sliced it, `02` drew the design contract, `03`
turned the REQs into feature specs with **Verification Contracts** — mechanically-gradeable rows
(`behavior → REQ · method · assertion · boolean pass-criterion · oracle`). Your job is to satisfy those rows, in the
spec's implementation order, at the happy-path altitude (hardening is `05`).

- **Write** `src/**` (source + tests) and the handoff at `_artifacts/exports/build-handoff-sprint-NN.md`; optionally
  a light `Dockerfile`/`docker-compose.yml` if the stack/deploy calls for it, and `sbom.json`.
- **Never write** the spine (`docs/spec/**`) or the realizations (`docs/architecture/**`, `docs/design/**`). They
  are read-only inputs; when one is wrong, you *surface* it (below), you do not edit it.
- **Reference, never copy.** The handoff links `REQ-NNN` / `DM-NNN` / `VC-NN`; it never pastes requirement prose
  (`shared/spine-boundary.md`).

## The fix pass — when a FIX REQUIRED review exists (the build↔review loop-half)

`04` has one verb (build) but **two entry conditions.** Before a normal build, check for a **FIX REQUIRED**
`docs/quality/qa-report-sprint-NN.md` for this sprint. If one exists, you are the **maker side** of the build↔review
loop (`05` is the checker; `05/references/review-discipline.md` §the loop): `05` found real defects, routed them to
you, and — for each *testable* defect — committed a **reproducing RED test** you must turn green. This is where the
classic TDD-for-bugs lands, now **split across the isolation boundary: `05` owns RED, `04` owns GREEN.**

- **Read the report as an added funnel input** (like `quality-guardrails.md`): its **Findings** table (each finding's
  severity · the REQ/VC · a `file:line` · the route) and the **committed reviewer RED tests** it cites.
- **Drive each failing behavior to green with the minimal change:**
  - **A reviewer RED test → make it pass. Never edit it.** It is an oracle you did **not** author; editing it to fit
    buggy code is exactly the "circular verification" the split exists to prevent. Fix the *implementation* until the
    reviewer's test goes green (confirm you observed it red first, then green).
  - **A prose finding that arrived without a test → full TDD-for-bugs:** write the reproducing failing test *yourself*,
    watch it fail, fix, watch it pass (the anti-tautology gate still applies).
  - **A `07` security finding → the same TDD-for-bugs, and the test *is* the proof.** A REMEDIATE finding routed from
    `/07-security` is fixed exactly like any bug: reproducing failing test → minimal fix → green. That regression
    test **is the `proof_of_fix` 07's re-audit requires**, so it must **bite on revert** (revert the fix → the test
    goes red; the 08 oracle-bites mechanic / the bite rule). Capture the test command in the handoff — a security fix
    that ships without its biting regression test leaves the finding **open** at re-audit (H2).
- **Re-emit the build-handoff** (do not append to the old one): the fixed behaviors now **EXECUTED** with fresh repro
  + RED-note; a **deviations note** in (d) naming what was addressed (`"REQ-008 grouping fixed — reviewer RED test
  test/review/req-008-grouping.test.js now green"`); fresh `final_commit` + recomputed `spec_slice_hash`. A **fresh**
  `05` re-reviews it (it does **not** read the prior QA report), so an unfixed behavior is simply caught again.
- **The convergence guard.** If a finding cannot be driven green because the *spec* is wrong (not the code), do not
  thrash — **escalate** it (the three-way verdict below): a wrong realization → `03`, a wrong declaration → a pending
  amendment for `00`/`05`. A defect that survives a couple of fix rounds is a spec/architecture problem, and `05`'s
  convergence guard turns it into a BLOCK.

If **no** FIX REQUIRED report exists, this pass is inert — proceed with the normal build below.

## The patch funnel — when the dispatch is a certified patch (the expedite lane)

`01-planner patch` certified it (P1–P5 on the record); your job is the narrow fix, with the same honesty machinery.
**Doctrine: ceremony scales down by change class; independent verification and the release gate never do.**

- **Funnel** = the patch record (`docs/planning/patches/patch-NNN.md`) + the existing realizations its owning REQs
  already have. No new feature spec, no sprint file, no design pass — by construction (the classification gate
  guarantees the fix touches none of that; if mid-build you discover otherwise, that is a P-check violation → HALT).
- **TDD-for-bugs, always** — the fix-pass machinery without a qa-report: write the reproducing test, watch it fail
  (the RED evidence), minimal fix, watch it pass. **The fix ships its regression test** — a patch that leaves no
  failing-then-passing test behind is not done.
- **Ledger** (`## Patches` in `docs/planning/backlog.md`, the sole status origin): flip `planned → in-progress` at
  build start. On a **P3 (new dependency) or P4 (size budget) violation mid-build: HALT, mark the row `escalated`**,
  and hand back — execution scope re-enters via `/01-planner plan-sprint N`, product scope via `/00-discovery
  reflect`. **Never silently widen** a patch: exceeding the certified budget while claiming patch review is exactly
  the misclassification-down the lane's asymmetry forbids.
- **Handoff**: patch-keyed (`build-handoff-patch-NNN.md`), `review_mode: patch` + `patch: patch-NNN`,
  `spec_slice_path`/`spec_slice_hash` bind the **patch record**; the VC carry-forward covers the owning REQs' rows
  (re-run — prove no regression) plus the new regression test's row; coverage map keyed to the owning REQs.

## Sequential — to completion or a recorded HALT

Run as a single continuous pass. **No subagents**: parallel self-directed building is exactly where correctness
breaks down (independent agents regenerate the same module or diverge on a shared type), and the spine is sequential
by design. **Do not stop for milestones or session boundaries** — carry on to a finished slice or a *recorded* HALT
(below). The one thing you never do is fake a pass to reach a stopping point.

## TDD RED-first — scoped to the testable rows

For every VC row whose `method ∈ {unit, api-contract}`: **write the test first, run it, and watch it fail**, then
write the minimal code to green, then refactor while green. The RED step is not a design ritual — it is the
**anti-tautology capture**: a test you have never seen fail is a test you cannot trust to fail when the behavior
breaks. (Anthropic's guidance names TDD the single strongest pattern for agentic coding precisely because the fresh
model over-eagerly writes code that makes a green bar appear; RED-first is what stops that.) Record the observed
failure — it becomes the **RED-phase note** in the handoff.

`static-conformance` rows (a lint / dependency rule — an ADR's *Rule* made executable) and `browser` rows are
verified by their own oracle, not a pre-written failing unit test; don't force a RED cycle where it doesn't fit.

## Eval-suite rows — eval-first RED + the grader-bites gate (`Profile: agent-system`)

For a VC row whose `method` is **`eval-suite`** (a *distributional* REQ — the oracle is the **eval harness over the
in-spine `docs/spec/evals/**` dataset**, not a unit test), RED-first takes a new form and the anti-tautology gate a
stricter one:

- **Eval-first RED.** The RED evidence is a **failing eval CASE observed before the fix** — run the harness over the
  dataset and watch a case (ideally the dataset's must-not / negative case) **fail**, *then* implement until it meets
  the floor. The harness run is the oracle; the observed failing case is the **RED-note** on the row.
- **Grader-bites — the reward-hacking defense.** Before an `eval-suite` row counts **EXECUTED**, the grader itself
  must **bite**: feed it a **degenerate output** (empty / constant / obviously-wrong) and confirm the grader **fails
  it**. A grader that passes garbage measures nothing, and the floor it reports is fiction. This is **the bite rule**
  (defined once in `shared/agentic-profile.md`; it is 08's oracle-bites rule generalized). Record the result on the
  row: *"grader bites: degenerate `''` scored 0 < floor → FAIL, as required."*
- **The handoff carries both** on the eval-suite row — the **RED-note** (the failing case pre-fix) **and** the
  **grader-bites** line. A row marked EXECUTED with no grader-bites attestation is not trustworthy: `05`'s mandatory
  `final_commit` hack-resistance spot-check (Task 3.7) re-runs the bite and will catch a hollow grader.

## The anti-tautology gate (the 2026 delta)

Before you mark any VC row **EXECUTED** in the handoff, it must clear one of two bars:

1. **RED evidence** — you observed the test fail before the implementation existed, or
2. **The introduce-a-bug answer** — *"if I broke this implementation, would this test catch it?"* If the honest
   answer is no, the test is hollow.

Reject and rewrite tests that are **assertion-free** (exercise code, assert nothing), **assert-the-mock** (verify the
test's own setup, not the code), or **oracle-copied-from-impl** (the expected value is computed the same way the
code computes it, so both are wrong together). On core domain logic, a **mutation check** is the mechanized form:
flip an operator / return a constant and confirm the suite goes red. This is the honest replacement for coverage% —
high coverage routinely masks logically hollow tests (Thoughtworks lists mutation testing as the "most honest signal"
for exactly this). Coverage is necessary, never sufficient.

## Reuse-first / no-duplication

Before implementing a task, **read the files it will touch.** The headline failure mode of agentic build is the
model regenerating a class/module that already exists because it never looked. Extend what's there; attest in the
handoff that no duplicate implementation was created.

## Dependency safety, hardened

Every dependency you propose to add must be **verified to exist in the registry with non-trivial reputation before
you install it** — then allow-list + pin the exact version + commit the lockfile + run `npm audit` / `pip audit`.
This is not busywork: **~19.7% of AI-recommended package names do not exist** (open-source-model suggestions ~21.7%,
commercial ~5.2%), and **~43% of the hallucinated names repeat across runs** — a stable, weaponizable target an
attacker can pre-register (slopsquatting). A new dependency **beyond the stated envelope** is a HALT, not a silent
install. (For a zero-dependency stack, the honest dependency-provenance result is "none added" — record that.)

- **Slopcheck at the install boundary (5.4b).** Before you run the installer, **verify the package name exists on the
  real registry** and is the one you mean (not a typosquat / hallucination — the react-codeshift incident spread
  through AI-generated skill files naming a non-existent package). Slopcheck **precedes** the install command, never
  after. 07's **R4** supply-chain reader re-checks this at audit; under `agent-system` `mcp-scan` is the deterministic
  scanner behind it.
- **Dependency cooldown (5.4b).** Apply **security patches immediately**; hold every **other** version bump until the
  release clears a **minimum package age** (a few days) — freshly-published versions are where supply-chain
  compromises land first. Record the cooldown decision when you bump a non-security dependency.

## Verify-live tech shapes (WS6)

Dependency safety above verifies the **package artifact** exists; this verifies the **interface knowledge** is
live-sourced (adjacent controls — never merged). Before you write against a spine-declared **verify-live** tech
(`architecture-constraints.md` § Verify-live — a framework/library too new for reliable recall), **read its exact
API/config from the `docs/verification/<tech>.md` record** — and, for a shape the record does not yet cover, from
live docs / latest source — **then append the newly-verified fact as a cited claims row.** Never call an API you are
recalling from memory. On the handoff, a VC row exercising a verify-live tech carries a **`verified:
docs/verification/<tech>.md`** ref beside its evidence state. **An API claim about a verify-live tech left
`INFERRED` is a finding** — SHIP unreachable via `05`'s honesty gate, `06` G11 blocks the ship — it is the honest
state when a source is unreachable (recorded, per the tool cascade), **never a faked `EXECUTED`**. Full doctrine:
`shared/live-source-verification.md`.

## Outcomes, not ceremony

Keep the outcomes that make code maintainable — **readable, single-responsibility, no dead code, no commented-out
blocks** — and stop there. **Do not run a SOLID-acronym audit or a gap-seeking style pass**: style- and
pattern-conformance is `05`/`08`'s seat, and a builder told to hunt for gaps *over-engineers* (adds abstraction the
slice doesn't need). Commit in **small, atomic, conventional commits** (`feat(scope):`, `test(scope):`,
`fix(scope):`), one commit ≈ one coherent step, so the diff reads as a sequence a reviewer can follow.

## HALT conditions — surface, don't push through

Stop and record a HALT (in the handoff's blocked record — `06-release` blocks on it) when you hit:

- a **new dependency beyond the stated envelope**;
- **3 consecutive failures** on the same behavior (you are guessing, not converging);
- **missing config** you cannot supply without inventing a declaration;
- a **genuinely contradictory or unbuildable spec** (see the three-way verdict);
- **non-convergence** — a drift-repair loop that runs past a few iterations;
- **on a patch: the certified size budget (P4) exceeded or a new dependency (P3) needed** — HALT **and mark the
  patch's `## Patches` ledger row `escalated`** (the expedite lane exits to the normal chain; never silently widen).

A HALT is honest scoping, not failure. Faking a green bar to avoid one is the only unrecoverable error here.

## Drift → honest escalation (04 is a non-amender)

When a Verification Contract cannot be satisfied, decide **which of three** is wrong, and act accordingly:

| The wrong thing | What it means | What 04 does |
|---|---|---|
| **the code** | your implementation is buggy | fix the code (normal loop) |
| **the test** | your test encodes the wrong expectation | fix the test (then re-clear the anti-tautology gate) |
| **the spec** | the *realization* (`03`'s feature spec / VC) is wrong | **flag to `03`** — record it as a surfaced deviation; do not edit the spec |
| **the declaration** | a *spine* fact (a REQ, a constraint) is wrong | **surface a pending amendment** for `00`/`05` in the handoff; do not touch the spine |

04 **appends no `amendment-log.json` row** — appending stays with `00/02/03/08` (`shared/spec-amendment-protocol.md`).
04's role in that protocol is to **classify and escalate**, honestly, in the handoff: a wrong realization goes back
to `03`; a wrong declaration is surfaced for the humans at `00`/`05`. **Never silently patch code *or* spec to fake a
pass** — a silently "resolved" contradiction is invisible to `/status`, the release gate, and the isolated reviewer,
which is the whole failure this framework exists to prevent. If repairing drift itself won't converge, HALT.
