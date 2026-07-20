# status evals

Follows **`/skill-creator`'s A/B method** (deterministic grader; no LLM judge; no node — `status` runs no code). The
input is a seeded **pre-status project state** — a git repo whose **root commit** carries a realistic mid-chain
TeamPulse chain: the spine (`docs/spec/**`), the backlog + sprint slices, design, architecture, `src/**`, and a
sprint-02 `qa-report` (verdict SHIP). For each case in [`evals.json`](evals.json), run two arms and compare the
skill's **lift**:

1. **with_skill** — a fresh agent loads `.agents/skills/status/SKILL.md` and runs `/status`: scans the chain,
   integrity-checks the spine, counts governance blockers, derives the live state, routes the single next command, and
   writes **only** the two generated views (`CLAUDE.md § Current State` + `AGENTS.md`).
2. **baseline** — a fresh agent performs the same prompt with **no skill** (ignore framework files). Shows what the
   deterministic, machine-readable derived state adds over an ad-hoc status summary.

## Why a pre-status fixture (and a fixture-builder, not `cp`)

`status` is the framework's only **read-only-w.r.t.-truth** seat: it derives state and writes **only** generated views,
so `docs/spec/**` + every realization must be **byte-identical** after it runs — the *inverse* of `08` (which changes
`src/**`) and the same polarity as `07` (which keeps `src/**` byte-identical). So the fixture is a git repo whose root
commit is the pre-status state, and the grader's honesty gate is a pure **`git diff`** vs that commit.
[`build_fixture.py`](build_fixture.py) assembles the chain (base + a per-case overlay; root = the pre-status commit)
and **self-checks** each case's planted condition is present (a malformed fixture fails the build loudly). The grader
compares the **working tree** against the **root commit** — robust to however the arm wrote its views.

```
python build_fixture.py --case <healthy|corrupted|blocked|backlog-gap> --out <arm>/outputs
# ... arm runs `/status` over outputs/ ...
python check_status.py --outputs <arm>/outputs --case <case>
```

`check_status.py` writes `grading.json` (`{expectations:[{text,passed,evidence}]}`) into `--outputs`. **status is
SEQUENTIAL** — no subagents, so there is **nothing to relax** in the harness `<SUBAGENT-STOP>` (the `04`/`06`/`08`
precedent, unlike `03`/`05`/`07`). Workspaces live **outside `.agents/skills/**`** (e.g.
`_artifacts/skills-eval/status/iteration-N/<case>/<arm>/outputs/`).

## What the assertions check (the lift is DERIVED STATE + READ-ONLY, never summary prose)

`status`'s value is **not** "a nice summary" — a strong reader writes that too. It is the **deterministic derived
state** the release gate and the next seat can act on, plus the **read-only-w.r.t.-truth** honesty gate. The
deterministic discriminators (a file/JSON + `git diff` grader like `03`'s — no mutation/behavior machinery):

- **Read-only w.r.t. truth** — after `/status`, `git diff` shows `docs/spec/**` + every realization **byte-identical**;
  only `CLAUDE.md` + `AGENTS.md` may change. On `corrupted` this doubles as the **report-don't-repair** check: the arm
  must **not** "fix" the missing delimiter (that would change `docs/spec`). *The killer: an arm that edits the spine to
  update or repair it fails deterministically.*
- **The machine-readable derived state** (`CLAUDE.md § Current State`) — the **integrity verdict** (PASS, or FAIL
  **naming the offending REQ-ID**), the **pending/deferred amendment + surviving-marker counts** the release gate
  blocks on, and the **single routed next command** in the framework's `/NN-role` vocabulary.
- **The faithful generated view** — `AGENTS.md` re-emitted as a faithful projection of the spine Constitution (the
  generated-view integrity check; verified on the PASS cases).

A baseline summarizes ad-hoc: it may improvise the integrity verdict as prose ("BROKEN" — invisible to a gate that
greps `FAIL`), name the next step conversationally ("run the planner (01)" rather than the actionable `/01-planner`),
vary the section format each run, or — worst — "helpfully" edit the spine to update or repair it. That gap is the
graded lift.

## The four fixtures (a two-axis F1: integrity × routing, + the governance arm)

- **`healthy`** (routing — mid-chain) — the clean state: sprint-02 built + qa SHIP, no release. → integrity **PASS**,
  0 blockers, next `/06-release sprint 2`.
- **`corrupted`** (integrity — sensitivity) — REQ-021's closing `<!-- /REQ-021 -->` delimiter is removed (an **L2**
  break): the registry still points at `api.md` (L1 ok) and the `### REQ-021:` heading is present, so a shallow read
  calls it complete → integrity **FAIL naming REQ-021**; next is the repair route (not a ship route); and the
  read-only proxy proves the arm **reported, didn't repair**.
- **`blocked`** (the governance arm) — a Tier-3 `deferred` amendment (AMD-003) + a surviving `[NEEDS CLARIFICATION]`
  marker, otherwise ship-ready → integrity PASS, the counts reported (≥1 deferred, ≥1 marker) tied to "06 blocks", and
  the route is **resolve** (`/00-discovery reflect`), **NOT** `/06-release`.
- **`backlog-gap`** (routing — early) — spine only (no `docs/planning/`) → integrity **PASS**, next `/01-planner` (the
  master-plan's called-out row).

## Grader validated (not vacuous)

Before any A/B run, `check_status.py` was validated against **hand-built ideal outputs** AND **degenerate** ones:

| Output | Case | Score |
|--------|------|:-----:|
| hand-ideal (PASS, next `/06-release sprint 2`, read-only, faithful AGENTS.md) | `healthy` | **9/9** |
| hand-ideal (FAIL naming REQ-021, repair route, reported-not-repaired) | `corrupted` | **8/8** |
| hand-ideal (PASS, 1 deferred + 1 marker, route `/00-discovery reflect`) | `blocked` | **9/9** |
| hand-ideal (PASS, next `/01-planner`) | `backlog-gap` | **8/8** |
| **mis-router** (next `/05-reviewer` on healthy) | `healthy` | **8/9** — routing fires |
| **prose-only baseline** (no structured emission) | `healthy` | **1/9** — every emission/routing/integrity/governance check fires |
| **integrity-blind** (reported PASS + `/06-release`, missed the break) | `corrupted` | **5/8** — verdict + FAIL-caught + not-ship fire |
| **spine-repairer** ("fixed" the missing delimiter) | `corrupted` | **6/8** — read-only proxy + report-don't-repair fire |
| **governance-blind** (0 deferred/0 markers + `/06-release`) | `blocked` | **6/9** — count + marker + resolve-route fire |
| **truth-mutator** (edited the backlog) | `blocked` | **8/9** — read-only proxy fires |
| **mis-router** (next `/02-designer` on backlog-gap) | `backlog-gap` | **7/8** — routing fires |

So the discriminators are **real, not vacuous**: the grader penalizes a mis-router, a prose-only non-emitter, an
integrity-blind pass, a spine-repairer (mutated truth), a governance-blind ship, and a truth-mutator — while crediting
a correct, deterministic, read-only derived state. **A key grader-hardening pass** (per
`feedback_grader_validate_on_real_outputs`): the count parsers credit **substance** (a real number for pending /
deferred / markers) regardless of backticks or a synonym label ("Amendment counts" / "Open ... markers" / "0 open"),
so the lift is **not overstated** by a formatting delta — while the **integrity verdict** (`PASS`/`FAIL`) and the
**next-command `/NN` slug** stay strict, because those are the standardized tokens a machine gate and the next seat
actually consume (the `08` verdict-vocabulary precedent).

## iteration-1

| Case | with_skill | baseline |
|------|:----------:|:--------:|
| `healthy` | **9/9** | 9/9 |
| `corrupted` | **8/8** | 6/8 |
| `blocked` | **9/9** | 9/9 |
| `backlog-gap` | **8/8** | 7/8 |

**with_skill passed every assertion on all four cases (34/34, 100%); baselines scored 31/34 (91%).** As the framework's
eval doctrine predicts (`feedback_framework_skill_lift_is_structural`), **derivation quality was not the
differentiator** — the baselines were strong: they **caught the missing-delimiter corruption** (naming REQ-021 and its
absent closing delimiter), **surfaced the governance block** (1 deferred amendment + 1 marker, routed to resolve, not
ship), derived the healthy and backlog-gap states correctly, and — every arm — **stayed read-only** (spine +
realizations byte-identical). Two of four cases are honest **ties** (9/9).

**The lift is the standardized, machine-parseable emission the baselines produced inconsistently — the same finding
as `08`:**

- **The integrity verdict vocabulary (2 of the 3 points).** On `corrupted`, the baseline emitted the verdict as prose
  — **"Spine integrity: BROKEN"** — which a release gate / the next `/status` greps for `PASS`/`FAIL` cannot read; the
  `with_skill` arm emitted the framework token **`FAIL — REQ-021: …`**. A break that is *correctly diagnosed* but
  stamped "BROKEN" is invisible to the gate (the exact `08` "HEALTHY vs CLEAN" gap).
- **The actionable next-command slug (the 3rd point).** On `backlog-gap`, the baseline named the next step
  conversationally — **"run the planner (`01`)"** — while the `with_skill` arm emitted the runnable **`/01-planner`**.
  A human/dispatcher can act on the slug, not the prose.

Beyond the graded points (not deterministically scored — the honest residue): the `with_skill` arms emitted the **exact
template fields every run** (`Spine integrity:` · `Amendments: N pending · M deferred` · `Open [NEEDS CLARIFICATION]:
K` · `Next command:`) plus the Sprint History matrix and the advisory list, so the **next** `/status` and the release
gate parse them deterministically; the baselines improvised the section shape each time (different headings, "Amendment
counts" vs "Amendments", "BROKEN" vs `FAIL`, "the planner (01)" vs `/01-planner`). The standardized emission — and the
read-only-w.r.t.-truth guarantee — is `status`'s graded lift. (Run workspace:
`_artifacts/skills-eval/status/iteration-1/`, gitignored.)

## WS1 patch awareness (Task 1.7)

Two cases cover the router's expedite-lane input: **`patch-in-flight`** (one open `planned` Patches row + its
certified record on the otherwise-healthy state — the router must go to **the patch's next seat**, `/04-builder`,
NOT `/06-release sprint 2`; a patch-unaware router false-routes to the sprint chain) and **`patch-pressure`**
(three consecutive `done` patches, none open — the normal route holds AND the **A6 advisory** appears: "this
cadence is a sprint — `/01-planner plan-sprint N` / consider `/08-refactor assess`"; advisory, never a block).
The read-only truth proxy (byte-identical spine + realizations) is graded on both, unchanged.

Grader-first per the WS1 A/B policy: hand-ideal derived states pass all assertions (including `grade_common`);
three degenerates (a false `/06-release` route on the in-flight case · the advisory line missing · the advisory
wrongly *blocking* the route) each fire exactly their target; the four legacy cases re-graded green (9/9 · 8/8 ·
9/9 · 8/8). **Live coverage** arrives with the phase-exit composed patch-lane chain (its final leg runs /status
on the patch-in-flight state).
