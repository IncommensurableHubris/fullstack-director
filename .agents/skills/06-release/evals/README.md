# 06-release evals

Follows **`/skill-creator`'s A/B method** (deterministic grader; no LLM judge). The input is a **seeded project
state at the ship boundary** — a git repo with three commits (docs baseline → built slice @ `final_commit` → `05`'s
qa-report carrying the **real** SHAs), a spine whose `amendment-log.json` + `architecture-constraints.md` are live
gate inputs, a repo-local **stand-in deployment platform**, and a gitignored `.env` planting a fake secret. For
each case in [`evals.json`](evals.json), run two arms and compare the skill's **lift**:

1. **with_skill** — a fresh agent loads `.agents/skills/06-release/SKILL.md` and runs `06-release sprint 1`:
   gates on recorded machine state (the qa frontmatter tally · amendment dispositions · a marker scan · code
   identity · security-if-present · secrets hygiene), fail-closed and evaluate-all; BLOCKs with routed reasons and
   deploys nothing — or SETUP → one pre-approved plan → execute → verify (health → smoke) → tag → the auditable
   release report.
2. **baseline** — a fresh agent performs the same prompt with **no skill** (ignore framework files). Shows what the
   machine-read protection-rule gate + the auditable record add over ad-hoc release judgment.

## Why a simulated local platform (and a fixture-builder, not `cp`)

Deploy is side-effecting; the eval cannot ship anything real. The fixture therefore **declares** (in
`architecture-constraints.md`) a repo-local stand-in platform — `node scripts/deploy.js` publishes the slice to
`_deploy/live/`; `health.js` probes liveness+readiness; `smoke.js` exercises the REQ-keyed critical flows against
the **deployed copy** — so the deploy/verify path produces **real captured evidence** (commands, exit codes,
probe output) offline with zero external effects, and SETUP is deterministic (the platform is a spine mandate, so
no user pause is needed). [`build_fixture.py`](build_fixture.py) assembles the repo with the real artifact
chronology — the qa-report's `baseline_commit`/`final_commit` are the repo's **actual SHAs** (rendered after the
commits exist), the report lands in a *later* commit (so G5's "src identical since review, docs may move" rule is
exercised for real), and `.env` is copied but ignored:

```
python evals/build_fixture.py --case <clean|blocked-verdict|blocked-spine> --out <arm>/outputs
```

`blocked-verdict` is internally **consistent**: its slice genuinely carries the REQ-008 grouping bug, the shallow
green suite, and the reviewer's committed RED test (`test/review/req-008-grouping.test.js` fails) — matching its
FIX REQUIRED report. `blocked-spine` is the sneaky one: its qa-report honestly says **SHIP**; only the spine state
(AMD-003 `pending` + a `[NEEDS CLARIFICATION]` marker in `capabilities/digest.md`) blocks.

## Workspace setup + grade (deterministic — no LLM judge)

Workspaces **outside `.agents/skills/**`** (e.g. `_artifacts/skills-eval/06-release/iteration-N/<case>/<arm>/outputs/`).
Build the fixture into each arm's `outputs/`, let the arm run the release there, then grade:

```
python evals/build_fixture.py --case <clean|blocked-verdict|blocked-spine> --out <arm>/outputs
# ... arm runs `06-release sprint 1` over outputs/ (the plan-approval is pre-granted in the prompt) ...
python evals/check_release.py --outputs <arm>/outputs --case <clean-release|blocked-verdict|blocked-spine>
```

`check_release.py` writes `grading.json` (`{expectations:[{text,passed,evidence}]}`) into `--outputs`; copy it to
the arm root for `eval-viewer/generate_review.py`. `06` is sequential with **no subagents** — nothing to relax in
the harness (the `04` precedent); its single human gate is pre-granted in the eval prompt.

## What the assertions check (the lift is the GATE + the AUDITABLE RECORD, never deploy prose)

`06`'s value is **not** "can run deploy commands" (a strong baseline does that too). It is the **machine-read
protection-rule gate that never proceeds past unresolved intent**, plus the **auditable, machine-readable,
no-secrets release record**. The deterministic discriminators:

- **The never-proceed property (sensitivity)** — `blocked-verdict` and `blocked-spine` must end `status: BLOCKED`
  with **nothing deployed** (no `_deploy/`, no deployment-config, `deployed_commit: none`), the failed checks cited
  by ID (the verdict + tally; `AMD-003`; the marker's file) and **routed** (`/04-builder` + a fresh `/05-reviewer`;
  `00 reflect`). `blocked-spine` is the killer: its verdict is SHIP — a verdict-only gate false-proceeds there.
- **Specificity (the crying-wolf guard)** — `clean-release` must ship: `status: RELEASED`, the deploy **actually
  executed** (`_deploy/live/` exists), captured deploy-log/health/smoke evidence, the tag. Blocking a clean state,
  or "releasing" without exercising the machinery, both fail.
- **The auditable record** — machine frontmatter (`status` · `gate_*` · `deployed_commit` · `health` · `smoke_*`),
  the gate table naming **all** checks (evaluate-all — even on a BLOCK the passing checks show), REQ-keyed release
  notes, code identity to the reviewed `final_commit`.
- **No-secrets + non-amender** — the planted `.env` value appears nowhere under `docs/**` (names only); the
  amendment log's rows/dispositions and `docs/spec/**` are byte-identical to the seed (a BLOCK routes; it never
  resolves).

A baseline typically reads the qa verdict and acts on it alone: it blocks on FIX REQUIRED but **false-proceeds past
the blocked spine**, verifies nothing about code identity, writes a prose report a machine can't gate on, may
scaffold configs that leak the secret value, and leaves no auditable BLOCKED record. That gap is the graded lift.

## The three fixtures (F1-framed)

- **`clean-release`** (`--case clean`) — SHIP report (consistent tally), terminal amendments, zero markers, the
  declared platform → **RELEASED** with executed evidence (specificity).
- **`blocked-verdict`** (`--case blocked-verdict`) — a FIX REQUIRED report over the genuinely defective slice →
  **BLOCKED**, cited + routed, nothing deployed (sensitivity, the obvious half).
- **`blocked-spine`** (`--case blocked-spine`) — a SHIP report **but** AMD-003 `pending` + a surviving
  `[NEEDS CLARIFICATION]` → **BLOCKED on the spine alone** (sensitivity, the discriminating half — the release
  gate exists precisely for this case; per `shared/spec-amendment-protocol.md` § Release gate).

## Grader validated (not vacuous)

Before any A/B run, `check_release.py` was validated against **hand-built ideal reports** AND **degenerate** ones:

| Report | Case | Score |
|--------|------|:-----:|
| hand-ideal RELEASED (real deploy + tag) | `clean-release` | **14/14** |
| hand-ideal BLOCKED (verdict cited + routed) | `blocked-verdict` | **11/11** |
| hand-ideal BLOCKED (AMD-003 + marker cited) | `blocked-spine` | **13/13** |
| **rubber-stamp** (saw SHIP, deployed past the blocked spine) | `blocked-spine` | **5/13** — every sensitivity discriminator fires |
| **crying-wolf** (invented concerns, blocked the clean state) | `clean-release` | **4/14** — every specificity discriminator fires |

So the discriminators are **real**: the grader penalizes both a false proceed and a false block (the F1 frame) and
credits only a correct, evidenced, auditable release decision.

## iteration-1

| Case | with_skill | baseline |
|------|:----------:|:--------:|
| `clean-release` | **14/14** | 8/14 |
| `blocked-verdict` | **11/11** | 9/11 |
| `blocked-spine` | **13/13** | 10/13 |

**with_skill passed every assertion on all three cases (38/38, 100%); baselines averaged 71% (27/38).** The
baselines were **strong release engineers** — every one reached the correct gate *decision*: the `clean-release`
baseline shipped (and even sourced the token from `.env` into the process environment without echoing it, then
swept `docs/` for leaks); the `blocked-verdict` baseline blocked and routed to the fix pass; the `blocked-spine`
baseline **did** check the spine and blocked on AMD-003 + the marker. Decision quality was **not** the
differentiator this round — as the framework's eval doctrine predicts, the graded lift is **the structured
contract the next seat consumes**:

- **No machine-readable release record** — baselines wrote prose (one invented its own `decision: GO` vocabulary):
  no `gate:` / `gate_qa_verdict:` / `deployed_commit:` / `health:` / `smoke_*` frontmatter, so `/status`, `00
  reflect`, or a re-run `06` cannot gate on the record without re-reading prose (the largest recurring gap — it
  cost every baseline arm).
- **No code-identity verification** — the `blocked-spine` baseline never checked that HEAD's `src/**` matches the
  reviewed `final_commit`; the `clean-release` baseline checked lineage ad-hoc but recorded no identity field.
- **No runbook, no tag, no evidence rows** — the `clean-release` baseline wrote no `deployment-config.md` (the
  durable deploy runbook), created no `release/sprint-01` tag, and logged its deploy as a narrative transcript
  rather than per-step `command · exit · excerpt` rows the grader (and an auditor) can verify.
- **Doctrine note (not graded):** both blocked-case baselines *re-derived* — re-running the suite and re-litigating
  the reviewer's findings at the gate — which duplicates `05`'s seat; the skill's gate reads recorded state and
  pins identity instead. The `with_skill` arms did exactly that, and the `blocked-spine` arm articulated the
  contract's sharpest edge unprompted: *"the pre-granted approval never came into play — the gate fails before
  PLAN and is not skippable by director say-so."*

The `with_skill` `clean-release` arm exercised the whole happy path — SETUP from the spine mandate → the one
approved plan (with a pre-stated rollback path) → captured deploy → health → smoke 3/3 → the annotated tag → the
machine-first report — and even appended a first `deployment-guardrails.md` row from a near-miss. So a `06` release
record can gate the next seat mechanically; a baseline's cannot. That gap — machine-readable + identity-verified +
evidence-captured + no-secrets — is the graded lift. (Run workspace: `_artifacts/skills-eval/06-release/iteration-1/`,
gitignored.)

## WS1 patch releases (Task 1.6)

A fourth case, **`patch-release`**, covers the expedite lane at the ship boundary: `build_fixture.py --case patch`
seeds a certified patch record + an `in-progress` Patches ledger row + a **SHIP `qa-report-patch-001.md`**
(`review_mode: patch`, real SHAs). The arm must gate the **same gate table — nothing waived** — and ship
patch-keyed: `release-report-patch-001.md` (`release_mode: patch` · `patch: patch-001`), the `release/patch-001`
tag, G5 identity against the *patch* review's `final_commit`, REQ-keyed notes citing the owning REQ, and the
Patches ledger row flipped `in-progress → done` (the release completes the lane).

Grader-first per the WS1 A/B policy: the hand-ideal (which really runs the stand-in deploy/health/smoke) passes
all assertions; three degenerates (sprint-keyed filename · ledger row not flipped · G6/G7 rows dropped from the
gate table) each fire exactly their target; the three legacy cases re-graded green after the grader extension
(clean-release 14/14 · blocked-verdict 11/11 · blocked-spine 13/13). **Live coverage** arrives with the
phase-exit composed patch-lane chain.
