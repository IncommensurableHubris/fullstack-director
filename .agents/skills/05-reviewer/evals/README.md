# 05-reviewer evals

Follows **`/skill-creator`'s A/B method** (deterministic grader; no LLM judge). The input is a **seeded BUILT slice** —
a `04` output: a git repo (baseline = spine + slice; final = + `src/**` + `node:test` tests) plus a build-handoff —
**not** a raw spine or a realization. For each case in [`evals.json`](evals.json), run two arms and compare the skill's
**lift**:

1. **with_skill** — a fresh agent loads `.agents/skills/05-reviewer/SKILL.md` and runs `05-reviewer sprint 1`: reads
   **only** the handoff + the spec-slice paths, verifies `baseline_commit` + recomputes `spec_slice_hash`, re-runs the
   oracles, re-derives judgment from a **fresh-context reviewer subagent**, and writes the verdict + a context
   attestation to `docs/quality/qa-report-sprint-01.md` (+ a reproducing RED test for a testable defect).
2. **baseline** — a fresh agent performs the same prompt with **no skill** (ignore framework files). Shows what the
   isolated, honest, FP-controlled verdict adds over an ad-hoc review.

## Why a seeded BUILT slice (and a fixture-builder, not `cp`)

`05` reviews an **already-built** slice, so — unlike `04`'s seed-then-build — the fixture needs a real **two-commit**
history (`baseline` = docs; `final` = + `src/**` + tests) and a build-handoff carrying the **real** SHAs, a
recomputed `spec_slice_hash`, and the test's oracle hash, so `05`'s diff-reconstruction, oracle re-run, and hash
verification are all real. [`build_fixture.py`](build_fixture.py) produces that:

```
python evals/build_fixture.py --case <clean|defective> --out <arm>/outputs
```

It reuses the zero-dep-Node/`node:test` **TeamPulse digest** domain (`recordStandup`, `assembleDigest`; REQ-001/008/009;
VC-01/02/03), so `node --test` runs offline and deterministically. `clean` and `defective` differ **only** in the
planted flaws (the `aurora-clean`/`aurora-contrast` isolation trick), so any behavior delta is attributable to them.

## Workspace setup + grade (deterministic — no LLM judge)

Workspaces **outside `.agents/skills/**`** (e.g. `_artifacts/skills-eval/05-reviewer/iteration-N/<case>/<arm>/outputs/`).
Build the fixture into each arm's `outputs/`, let the arm review it and write the report there, then grade:

```
python evals/build_fixture.py --case <clean|defective> --out <arm>/outputs   # clean-ship+isolation: clean; defective-fix: defective
# ... arm runs `05-reviewer sprint 1` over outputs/ ...
python evals/check_review.py --outputs <arm>/outputs --case <clean-ship|defective-fix|isolation>
```

`check_review.py` writes `grading.json` (`{expectations:[{text,passed,evidence}]}`) into `--outputs`; copy it to the
arm root for `eval-viewer/generate_review.py`:

```
python <skill-creator>/eval-viewer/generate_review.py <iteration-dir> --skill-name 05-reviewer --static <out.html>
```

## What the assertions check (the lift is the VERDICT + ISOLATION + HONESTY + F1, never review prose)

`05`'s value is **not** "reviews code" (a strong baseline does that too; review *beauty* is not graded). It is the
**isolated, honest, false-positive-controlled verdict** that can gate a ship. The deterministic discriminators:

- **Verdict correctness** — `clean` → **SHIP**; `defective` → **not-SHIP** (FIX REQUIRED/BLOCK).
- **Sensitivity** — the `defective` report **names each of the three orthogonal plants in a structured finding**, and
  **commits a reproducing RED test** that fails against the defective impl (the executable findings interface).
- **Specificity (the crying-wolf guard)** — the `clean` report has **~zero findings** and Inferred = 0. Together with
  sensitivity this is the **F1 frame**: a rubber-stamp (miss the defect) and a cry-wolf (flag a sound build) are
  *equally* disqualifying.
- **Isolation, made auditable** — a **context attestation** (`inputs: [handoff, spec slice]; build conversation: not
  provided`; the reviewed `baseline_commit` == the handoff's; opened-files ⊆ seed). No prior-art tool emits one.
- **Honesty** — `spec_slice_hash` recomputed and matched; ledger↔verdict consistent (SHIP unreachable while Inferred
  > 0 or a MUST-gap).

A baseline reviews ad-hoc: it may **rubber-stamp** the defective build (echo the handoff's optimistic EXECUTED/FULL
claims), **cry wolf** on the clean build, and emit **no attestation / no verification ledger / no structured finding /
no reproducing RED test** — so its verdict cannot honestly gate a ship. That gap is the graded lift.

## The three fixtures (F1-framed)

- **`clean-ship`** (`--case clean`) — a sound slice: all three VCs honestly EXECUTED by real, non-tautological tests →
  **SHIP, ~0 findings** (specificity / the false-positive guard).
- **`defective-fix`** (`--case defective`) — three **orthogonal** plants caught by three **different** mechanisms:
  (A) a **REQ-008 grouping logic bug** (`assembleDigest` returns only the first member) — hidden behind a single-member
  test, caught by the semantic pass → a reproducing **RED test**; (B) a **tautological VC-01 dedup test** (asserts only
  `Array.isArray`) — caught by the **anti-tautology litmus**; (C) **REQ-009 claimed FULL but uncovered** (no needs-help
  test) — caught by **coverage arithmetic**. Verdict **FIX REQUIRED**, each plant **named**.
- **`isolation`** (`--case clean`) — reuses the clean slice; grades the **context attestation** (present + valid;
  `baseline_commit` == handoff; opened-files ⊆ seed). The parent-transcript-absence half is a **manual** check (per
  `shared/subagent-protocol.md` — Pass 2 judgment is human-gated, never deterministically graded).

## Reviewer isolation (05's subagent debut, like 03)

`05`'s **Pass 2** runs in a **context-isolated reviewer subagent**. In the `with_skill` arm, spawn it from a **fresh**
spawner (a real subagent where supported, else a fresh top-level invocation) seeded with **only** the realization + the
spec-slice declarations — never the build conversation — and record the one-line **context attestation** in the QA
report. **Relax the harness `<SUBAGENT-STOP>` for 05** (the `03` precedent; `docs/eval-methodology/harness-reference/`)
or the reviewer short-circuits. The grader checks the **attestation's presence + the `baseline_commit`/hash match** (a
deterministic, file-based proxy); the **transcript-absence** half is manual.

## Grader validated (not vacuous)

Before any A/B run, `check_review.py` was validated against **hand-built ideal reports** AND **degenerate** ones:

| Report | Case | Score |
|--------|------|:-----:|
| hand-ideal SHIP | `clean-ship` | **9/9** |
| hand-ideal SHIP | `isolation` | **10/10** |
| hand-ideal FIX REQUIRED (+ RED test) | `defective-fix` | **13/13** |
| **rubber-stamp** (SHIP on the defective build) | `defective-fix` | **6/13** — the sensitivity discriminators all fire |
| **crying-wolf** (FIX REQUIRED, invented style findings, on the clean build) | `clean-ship` | **7/9** — the specificity discriminators fire |

So the discriminators are **real, not vacuous**: the grader penalizes both over-approval and crying-wolf (the F1
frame), and credits a correct, isolated, honest verdict.

## iteration-1

| Case | with_skill | baseline |
|------|:----------:|:--------:|
| `clean-ship` | **9/9** | 5/9 |
| `defective-fix` | **13/13** | 4/13 |
| `isolation` | **10/10** | 3/10 |

**with_skill passed every assertion on all three cases (32/32, 100%); baselines averaged 37.5% (12/32).** The
baselines were **strong reviewers** — each genuinely re-derived judgment: the `clean-ship` baseline reached **SHIP**
and even ran its *own* mutation testing to confirm the tests weren't tautological; the `defective-fix` baseline
reached **FIX REQUIRED** and **caught all three planted defects** (the REQ-008 grouping bug via a 3-member probe, the
tautological VC-01 test via mutation, the fabricated REQ-009 coverage claim). Review *quality* was **not** the
differentiator — as designed.

**The lift is the isolated, honest, executable verdict artifact the baselines did not produce** (the same gaps recur
across the cases):

- **No context attestation** — baselines emit no auditable `inputs: [handoff, spec slice]; build conversation: not
  provided` line, so isolation is asserted-at-best, never provable (the whole `isolation` case, and the attestation
  assertions everywhere → the biggest gap: `isolation` baseline **3/10**).
- **No committed reproducing RED test** — the `defective-fix` baseline mutation-tested on *scratchpad copies* and
  **committed no RED test to the workspace**, so `04` has no un-gameable oracle to drive to green (the executable
  findings interface — the anti-circular lever — is absent).
- **No machine-readable verdict** — no frontmatter tally / Verification Ledger / recorded `spec_slice_hash`
  verification, so `06-release` could not gate on the verdict without re-reading prose, and the plants are named in
  prose rather than a structured Findings table.

The `with_skill` arms produced exactly this: the `defective-fix` arm caught all three plants **in a structured Findings
table**, **committed a reproducing RED test** (`test/review/req-008-grouping.test.js`, RED against the defective impl —
05 owns RED, 04 owns GREEN), re-ran the oracles + the anti-tautology litmus, recorded `spec_slice_hash: match`, and
emitted the auditable attestation; the `clean-ship` arm reached SHIP with **0 findings** and Inferred = 0. So a fresh
`05` verdict can gate a ship; a baseline's cannot. That gap — structural + isolation + honesty + F1 — is the graded
lift. (Run workspace: `_artifacts/skills-eval/05-reviewer/iteration-1/`, gitignored.)

## Build↔review loop — end-to-end integration check

The two unit-evals grade each *half* of the loop (05's `defective-fix` review pass · 04's `fix-pass`). The full
generator↔evaluator loop was additionally run end-to-end on **real chained artifacts** (the master-plan integration
test, exercised early — 05's actual round-1 output fed into a real 04, then a fresh 05):

1. **Round 1 — a fresh `05` on the defective slice → FIX REQUIRED** (13/13). It named all three plants in a structured
   Findings table and committed **three reviewer oracles**: a RED grouping test + two escalation tests (dedup,
   needs-help — both green, because only the grouping was a real bug; the other two were verification *lies*, not
   behavior bugs).
2. **Round 2 — a real `04` fix pass** consumes that report + the RED test: it fixes `assembleDigest` (the grouping RED
   test goes green) **without editing any `test/review/**` oracle** (its git blob is byte-identical — the anti-circular
   rule held), strengthens its own hollow VC-01 + adds the missing VC-03, and re-emits the handoff (fresh
   `final_commit`; `spec_slice_hash` re-matches).
3. **Round 3 — a fresh `05`, no prior verdict → SHIP** (9/9 on `check_review.py --case clean-ship`; 10/10 isolation).
   With the round-1 report archived + unread, the new reviewer re-derived independently — oracle hashes match,
   anti-tautology litmus bites 3/3, hash matches, Inferred = 0 — and reached SHIP on the build's own terms. It also
   surfaced two **routing notes, not defects** (a headless "at the top" spec ambiguity → `03`; the pre-existing
   `[NEEDS CLARIFICATION]` marker → the `06` gate).

**The loop converges — FIX REQUIRED → fix → SHIP** — with isolation preserved every round (each `05` is a fresh spawner
that never inherits the prior verdict) and the fixer never authoring the oracle it is graded against. This run also
**refined the grader**: a *routing note* (a spec-ambiguity escalation — a first-class output of the honest-escalation
discipline) must **not** trip the crying-wolf guard, so `finding_rows` now counts only **severity-graded defect** rows.
The committed `clean-ship`/`defective-fix` numbers are unchanged (their findings are severity-graded); only real
ambiguous slices that carry a routing note are affected. (Workspace `_artifacts/skills-eval/loop-integration/`, gitignored.)

## WS1 patch seed (Task 1.5)

A fourth case, **`patch-review`**, covers the expedite lane's seed variant: `build_fixture.py --case patch` stages
the shipped sprint-01 state + the certified patch record + the in-progress Patches ledger row as **baseline**, the
patch fix + its reproducing regression test as **final**, and a **patch-keyed handoff** (`build-handoff-patch-001.md`,
`review_mode: patch`, `spec_slice_path`/`hash` binding the **patch record alone** — no manifest half; 02 is skipped
by construction on a patch). `check_review.py`'s hash recompute is now `spec_slice_path`-aware, and the case asserts:
the seed manifest lists the patch record · the review is patch-keyed (`qa-report-patch-NNN.md`) · the sound patch
SHIPs with Inferred = 0 · **the honesty gate is unchanged** (SHIP unreachable while any behavior is INFERRED —
validated by a planted `ledger_inferred: 1` + SHIP degenerate, which the grader fires on).

Grader-first per the WS1 A/B policy: the hand-ideal patch report passes all assertions (including `grade_common`
with the record-bound hash); three degenerates (INFERRED-yet-SHIP · seed manifest omits the record · sprint-keyed
filename) each fire exactly their target; the legacy `clean` fixture still builds and grades identically after the
`build_fixture.py` restructure. **Live coverage** arrives with the phase-exit composed patch-lane chain.
