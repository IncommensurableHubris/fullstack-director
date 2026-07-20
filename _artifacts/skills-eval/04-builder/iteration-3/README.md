# 04-builder iteration-3 — WS3 Task 3.6 (eval-first RED + grader-bites for eval-suite rows)

Live A/B (skill-creator method, native subagents on **Sonnet**; orchestrator on Opus). Each arm given the seeded
`beacon-build` funnel (a `Profile: agent-system` project whose feature spec `research-loop.md` carries an
**`eval-suite`** VC row, VC-02/REQ-002) in a git-initialized workspace. Graded by `check_build.py --case agent`
(handoff-centric — a distributional row's oracle is the eval harness, not `node --test`). Workspaces gitignored; this
README is the record.

## Results

| Arm | Grade | What it demonstrates |
|-----|:-----:|----------------------|
| with_skill | **7/7** | frozen diff anchor in the frontmatter; the **eval-suite VC row carried forward EXECUTED** with a **RED-note** (the uncited-claim case observed FAIL at 0.0 < 0.80 floor before the citation gate, PASS at 0.94 after) **and a grader-bites line** ("degenerate `''` scored 0 < floor → FAIL, as required"); FULL/PARTIAL/NONE coverage for every in-scope REQ |
| baseline | **2/7** | a **genuinely strong** build — 43 tests, a real eval harness, and it even *broke the gate two ways to confirm it has teeth* — but a **free-form prose handoff**: no frontmatter diff anchor, no per-VC `EXECUTED` evidence states, no recognizable grader-bites attestation, no FULL/PARTIAL/NONE verdicts. Only *handoff exists* + *the spec has an eval-suite row* pass |

**The honest read** (`feedback_framework_skill_lift_is_structural`): the baseline **did the substance** — it observed
the must-not case fail (eval-first RED) and deliberately broke the grader to prove it isn't tautological (grader-bites)
— so the discipline is not unique to the skill. The lift is the **structured, cold-reviewable handoff contract**: the
frozen `baseline..final` diff anchor a context-isolated 05 reconstructs from, the `EXECUTED` evidence-state vocabulary
05 consumes 1:1, and the eval-first RED-note + grader-bites attestation in a **recognizable, machine-checkable** form.
A strong builder verifies the grader bites; the framework makes that verification *legible to the isolated reviewer*.
Sonnet-with-skill at 7/7 is the honest portability claim.

## Grader-validation (grader-first, before the live run)

Hand-ideal handoff (`val-3.6/ideal/`: the eval-suite VC row EXECUTED + a RED-note + a grader-bites line) → **7/7**.
Two degenerates each fire exactly their target:
- **no-bite** (strip the grader-bites attestation) → *Grader-bites* fails;
- **no-red** (blank the eval-suite row's RED-note, keep the grader-bites) → *Eval-first RED* fails.

Then the real arms were re-graded (with_skill 7/7, baseline 2/7) — the baseline's substance is credited in prose so
the lift is not overstated (`feedback_grader_validate_on_real_outputs`).
