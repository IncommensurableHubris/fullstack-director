# 04-builder evals

Follows **`/skill-creator`'s A/B method** (deterministic grader; no LLM judge). The input is a **seeded upstream
realization** — `03`'s feature specs + Verification Contracts, `system.md`, ADRs, the `01` sprint slice, and (case 3)
a `02` design manifest — **not** a raw spine. For each case in [`evals.json`](evals.json), run two arms and compare the
skill's **lift**:

1. **with_skill** — a fresh agent loads `.agents/skills/04-builder/SKILL.md` and runs `04-builder sprint 1`: captures
   `baseline_commit` before editing, implements `src/**` + `node:test` tests against the Verification Contracts, and
   writes the evidence-bearing handoff at `_artifacts/exports/build-handoff-sprint-01.md`. `04` has **no user gate and
   no subagents** — it runs as a single sequential pass, so there is **nothing to relax** (unlike `03`/`05`).
2. **baseline** — a fresh agent performs the same prompt with **no skill** (ignore framework files). Shows what the
   cold-reviewable, evidence-bearing handoff + non-tautological tests add over an ad-hoc build.

## Why a pure-domain, zero-dependency slice

`04`'s eval cannot be `03`'s full walking skeleton (auth + a client-server datastore + a web server can't build
zero-dep and run offline under `node:test`). The fixture is instead the **TeamPulse digest core** — pure domain logic
(`recordStandup`, `assembleDigest`, and a text `renderDigest`) whose Verification Contracts are **`unit`-method over
pure functions**, so `node --test` runs **offline and deterministically**. DM-IDs (case 3) map to elements of the
**text-rendered** digest, so even the design-contract coverage is verified by a unit test — no browser needed. The one
`browser` row (case 2) has **no runtime** in this headless slice on purpose: it is the honest-INFERRED discriminator.

## Workspace setup (the input is a realization — seed it first, and it must be a git repo)

Put workspaces **outside `.agents/skills/**`** (e.g. `_artifacts/skills-eval/04-builder/iteration-N/<case>/<arm>/outputs/`)
to avoid the `with_skill` write-refusal heuristic. The arm's `outputs/` dir **is the project root**: seed it with the
funnel (base overlaid with the case), then **`git init` + make the seed commit** so `baseline_commit` and the
diff-reconciliation are real:

```
mkdir -p <…>/<arm>/outputs
cp -r evals/fixtures/base/docs        <…>/<arm>/outputs/docs      # shared spine + zero-dep architecture
cp -r evals/fixtures/cases/<case>/docs <…>/<arm>/outputs/          # overlay: this case's sprint + VCs [+ manifest]
cd <…>/<arm>/outputs && git init -q && git add -A && git commit -qm seed
```

The arm then captures `baseline_commit` (= the seed commit), builds `src/**` + tests, commits, and writes the handoff.

## Grade (deterministic — structural + smoke-run + anti-tautology + honesty)

```
python check_build.py --outputs <…/outputs> --case <clean-build|unbuildable-contract|coverage-traceability>
```

It writes `grading.json` (`{expectations:[{text,passed,evidence}]}`) into `--outputs` and prints a pass/fail report.
Copy `grading.json` up to the arm root (`<arm>/grading.json`) so `eval-viewer/generate_review.py` renders the verdict:

```
python <skill-creator>/eval-viewer/generate_review.py <iteration-dir> --skill-name 04-builder --static <out.html>
```

## What the assertions check (the lift is STRUCTURAL + smoke-run + anti-tautology + honesty)

`04`'s value is a **cold-reviewable, evidence-bearing, honest handoff + non-tautological tests** — not "working code"
(a strong baseline builds that too; build *beauty* is not graded). The deterministic discriminators, over the built
slice:

- **Structural** — the handoff carries the frozen diff anchor (`baseline_commit`/`final_commit`/`spec_slice_path` +
  the tamper-evident **`spec_slice_hash`** that `05` recomputes and compares), a File List, every VC row carried
  forward with an **evidence state** (EXECUTED/OBSERVED/INFERRED), and an in-scope REQ coverage map.
- **Diff reconcile** — `git diff baseline..worktree` (source files) **==** the declared File List (no undeclared
  writes / hallucinated claims), and the build touched **no** `docs/spec | docs/architecture | docs/design` file
  (spine + realizations read-only).
- **Smoke-run (the EXECUTED gate)** — `node --test` exits **0 AND** with a **positive** executed-test count (the
  "0 tests, exit 0" false-green guard), on **two** runs (determinism).
- **Anti-tautology** — a **single-point source mutation** (flip a comparison/boolean) makes the suite **FAIL**; a
  suite still green on a broken impl is tautological → hard fail. Paired with an *assertions-present* check so an
  assertion-free suite can't sneak through on a crash.
- **Honesty** — every non-EXECUTED row cites a reason; no row claimed EXECUTED while the suite is red.

Per case, one extra discriminator: **clean-build** — every VC EXECUTED; **unbuildable-contract** — the `browser` VC
honestly **INFERRED with a cited reason** (not dropped, not fake-passed) while the unit rows stay EXECUTED;
**coverage-traceability** — a complete REQ→test:line map + every manifest **DM-ID → an existing file:line**.

**The baseline gap (the lift):** a baseline builds passing code but produces no `baseline_commit`/File-List/
evidence-state/REQ-map handoff, may write hollow tests (fail the mutation/assertion checks), and silently drops or
fake-passes the unbuildable VC — so `05` could not verify in isolation. That gap is the graded lift.

## Fixtures (base + case overlay)

```
fixtures/base/docs/**         # shared: spine (spec/) + zero-dep-Node architecture (system.md, adr/) — identical across cases
fixtures/cases/<case>/docs/** # per-case overlay: the sprint slice + the feature-spec Verification Contracts [+ a 02 manifest]
```

- **`clean-build`** — 2 `unit` VCs (REQ-001 one-per-day, REQ-008 grouped-by-member), fully buildable → the full
  evidence-bearing handoff, all EXECUTED, survives the mutation.
- **`unbuildable-contract`** — adds REQ-009 and a `browser` VC-04 (visual pinning) with no runtime in this headless
  slice → the honest-INFERRED discriminator; the unit rows stay EXECUTED.
- **`coverage-traceability`** — multi-REQ (001/008/009) over the core + a text renderer, with a `02` manifest
  (DM-001/002/003) → a complete REQ→test:line map + DM→file:line forward coverage.
- **`fix-pass`** *(the build↔review loop-half)* — a **defective** built slice (a REQ-008 grouping bug) + the
  reviewer's committed **RED test** (`test/review/req-008-grouping.test.js`, red against the bug) + a FIX REQUIRED
  `docs/quality/qa-report-sprint-01.md`. `04-builder sprint 1` runs the **fix pass**: it drives the reviewer's RED
  test to GREEN by fixing the impl (**never editing the reviewer-authored oracle** — the anti-circular rule) and
  re-emits the handoff (VC-02 EXECUTED + a deviations note + a fresh `final_commit`/`spec_slice_hash`). Graded by
  `check_build.py --case fix-pass` (the reviewer test now passes · its git blob is unchanged · the handoff re-emitted).

## iteration-1

| Case | with_skill | baseline (no skill) |
|------|:----------:|:-------------------:|
| `clean-build` | **16/16** | 11/16 |
| `unbuildable-contract` | **17/17** | 11/17 |
| `coverage-traceability` | **17/17** | 12/17 |

**with_skill passed every assertion on all three cases (50/50, 100%); baselines averaged 68% (34/50).** The baselines
were **strong builders**: each independently produced a correct pure zero-dep core + passing `node:test` suite,
captured the `baseline_commit` anchor, kept the domain pure (grep-clean of clock/randomness), left `docs/**`
untouched, and even reasoned correctly about the unbuildable `browser` VC-04 in prose ("not executed — headless slice,
no web container"). Build *quality* was not the differentiator — as designed.

**The lift is the structured, cold-reviewable evidence contract the baselines did not produce** (the same failures
recur across all three cases):

- **No parseable per-VC evidence state** — baselines wrote `PASS` / prose, not `05`'s `EXECUTED / OBSERVED / INFERRED`
  vocabulary consumed 1:1 by the reviewer (3× fail).
- **No `REQ → FULL/PARTIAL/NONE` coverage map** at real `test:loc` — baselines asserted coverage in prose (3×+3× fail).
- **No `spec_slice_path`** asserted for the reviewer to load (3× fail).
- **The `browser` VC not tagged `INFERRED`** — honest in prose, but not in the machine-consumable honesty field the
  reviewer escalates from (unbuildable case).
- Plus the per-case completeness discriminators (all rows `EXECUTED`; the full REQ map).

So a fresh `05-reviewer`, seeded with only the baseline's handoff, could not mechanically reconstruct the diff anchor,
re-key the evidence states, or read coverage — which is the whole point of the build→review boundary. That gap is the
graded lift (structural + honesty + anti-tautology), not build beauty.

**Grader validated (not vacuous).** Before the A/B run, `check_build.py` was checked against **hand-built ideal
outputs** (one per case): all three reach **16/16 · 17/17 · 17/17**, and a **degenerate** baseline-like output (a
passing but assertion-free suite, no handoff) scores **4/16** — the 12 structural/honesty/anti-tautology
discriminators all fire, and the mutation check correctly registers **0 kills** on the hollow suite (no false credit
from a crash). The real A/B run then surfaced grader bugs the ideals could not (the run workspace lives under
`_artifacts/`, which an early path filter wrongly skipped; a baseline recorded the commit anchor in a Markdown table
rather than YAML). Both were fixed so the discriminator is **substance, not delimiter** — the anchor is credited in
either form; what still separates the arms is the parseable evidence-state + coverage contract.

The static viewer is at `_artifacts/skills-eval/04-builder/04-builder-eval-review.html` (gitignored run workspace).

## iteration-2 — the `05` fold-in (`spec_slice_hash` + the fix-pass loop-half)

Building `05-reviewer`, `04` gained **both halves of the build↔review loop** together (user-confirmed: "spec now, build
both sides when building `05`"): (A) it **emits `spec_slice_hash`** in the handoff (the tamper-evident binding `05`
recomputes), and (B) it runs the **fix pass** when a FIX REQUIRED `docs/quality/qa-report-sprint-NN.md` exists.
`check_build.py` gained a `spec_slice_hash` presence assertion (**+1 per case**) and the `fix-pass` case + branch.
Re-run to confirm `04` stays green:

| Case | with_skill | baseline |
|------|:----------:|:--------:|
| `clean-build` | **17/17** | — |
| `unbuildable-contract` | **18/18** | — |
| `coverage-traceability` | **18/18** | — |
| `fix-pass` | **21/21** | 13/21 |

**All three original cases stayed green with `spec_slice_hash`** (the live arms computed + emitted it correctly,
including the manifest half for `coverage-traceability`), **and the new `fix-pass` case validated the loop-half
end-to-end:** the `with_skill` arm drove the reviewer's committed RED test to green by fixing `src/digest.js` **without
editing the reviewer-authored oracle** (its `git` blob is byte-identical to baseline — the anti-circular rule held) and
re-emitted the handoff (VC-02 now EXECUTED + a deviations note + a fresh `final_commit`/`spec_slice_hash`). The
`fix-pass` **baseline (13/21)** made `node --test` green but **left the fix uncommitted (no fresh `final_commit`) and
re-emitted no structured handoff** — precisely the loop-half's lift.

**Grader re-validated (not vacuous).** `check_build.py` was re-checked against a hand-ideal fix-pass output (21/21) and
all four real arms; the run **surfaced + fixed a File-List↔diff over-extraction** — declared paths must be read from the
`(a) File List` **table rows' Path column** only, because a fix pass legitimately *names* the unchanged reviewer oracle
in a prose cross-check note (an early whole-section scan miscounted it as a "hallucinated" file). Both `05` and `04`
graders now scope structured extraction to a named section's table rows, never the whole document.

## WS1 patch funnel (Task 1.4)

Two cases extend the suite for the **expedite lane**: **`patch-build`** (a certified `patch-001` on the shipped
sprint-01 state — the arm must fix the at-lock boundary bug TDD-for-bugs-style, stay inside the record's certified
3-file/60-LOC budget, advance the `## Patches` ledger row to `in-progress`, and emit a **patch-keyed** handoff:
`build-handoff-patch-001.md`, `review_mode: patch`, `patch: patch-001`, `spec_slice_path`/`hash` binding the patch
record; the common contract's VC carry-forward is **scoped to the owning REQs**) and **`patch-budget-exceeded`**
(the record certifies an impossible 1-file/8-LOC budget — the honest exit is a **HALT naming P4**, the ledger row
`escalated`, no silent widening, spine untouched; `grade_common` deliberately does not run: a correct HALT has no
completed build to smoke or mutate).

Per the WS1 revision A/B policy these cases ship **grader-first**: `check_build.py` was validated on staged
hand-ideals (both pass, including the full common contract on `patch-build` — real `git` repo, `node --test`
smoke, mutation kill) and four degenerates (`review_mode: full` left in place · patch id lost + sprint-keyed
filename · ledger row not advanced · silent widening) each fire exactly their target. The four legacy cases
re-graded green after the grader restructure (17/17, 21/21 spot-checked). **Live coverage** for the happy path
arrives with the phase-exit **composed patch-lane chain** (`01 → 04 → 05 → 06 → status`), not a per-task A/B.
