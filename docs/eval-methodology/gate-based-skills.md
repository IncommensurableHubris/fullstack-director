# Evaluating Gate-Based Skills

> Methodology for body-eval suites covering skills with user-approval gates mid-execution.

This doc captures the lessons from `.claude/skills/08-refactor/evals/` (v1.0.0 → v1.3.1, 2026-03-28 → 2026-04-18). It exists so the next author of a body-eval suite for a multi-gate skill (e.g., a future `/quality` or `/ship` that gains approval checkpoints) doesn't re-learn the same three surprises the hard way.

## TL;DR

1. **A skill with N user-approval gates needs N evals, not 1.** A monolithic eval can't clear gates 2+ under `-p` conditions — the subagent has no authority to approve its own gates.
2. **Pre-seed each gate eval with the prior gate's outputs as fixtures.** Each eval becomes one-shot-friendly: subagent starts mid-sprint, works inside one gate's boundary, stops.
3. **Put the eval workspace OUTSIDE `.claude/**`.** Under `_artifacts/skills-eval/<skill>/` is the correct location. Workspaces under `.claude/skills/**` trigger a path-heuristic that makes with_skill subagents refuse to Write files, silently inverting measurements.
4. **Gate prompt specificity controls what the eval measures.** Ambiguous prompts (Gate 1 "do a health assessment") measure the skill's taxonomy/framing value. Specified prompts (Gate 2 "write characterization tests for taskService, notificationService, userService") measure less — a capable baseline produces the same outputs. Decide which you want per gate.

## What is a gate-based skill?

A skill with one or more hard checkpoints where execution pauses until the user approves before proceeding. Examples:

- `/refactor sprint N` has 4 gates (diagnose → prepare → execute → reconcile)
- Any skill with language like "**wait for user approval before…**", "**present to the user and stop**", or an explicit `>>> GATE N: …`  boundary

A skill without gates (e.g., `/refactor assess`, which has only a single implicit Gate 1 and then stops) is a degenerate case — a monolithic eval works fine.

## Why monolithic evals fail (v1.2.0 eval-full-sprint finding)

When `run_body_evals.py` invokes `claude.exe -p`, the subagent has no human to approve gates. It must either:
- **Stop at the first gate** (honoring the prompt's "wait for approval") — gates 2+ never run, so assertions covering them fail
- **Bulldoze through all gates** — violates the skill's discipline, producing runs that don't match real user behavior

Both are measurement noise. Concretely, 08-refactor's v1.2.0 `eval-full-sprint` scored 11.1% with_skill vs 11.1% without_skill (+0 pp). The 0 pp delta wasn't skill parity — both configs stopped at Gate 1 and the 8 assertions covering Gates 2–4 failed identically for both. Zero information.

## The gate-split pattern

Replace one eval that tests all N gates with N evals, each testing one gate. Each eval's fixture directory is pre-seeded with plausibly-correct outputs from the prior gates.

### Fixture progression (08-refactor concrete example)

| Fixture | Contents | Used by |
|---------|----------|---------|
| `mock-project/` | Pristine TaskFlow codebase with seeded smells | Gate 1 + `assess` + `targeted` |
| `mock-project-gate2-input/` | = `mock-project` + `docs/refactoring/health-assessment-SPRINT-05.md` | Gate 2 |
| `mock-project-gate3-input/` | = gate2 + `src/tests/*.char.test.ts` + `docs/architecture/adr/ADR-004.md` | Gate 3 |
| `mock-project-gate4-input/` | = gate3 + refactored `src/services/` (event emitter applied) | Gate 4 |

Each fixture is created with `cp -r` from the previous and then edited to add the prior gate's artifacts. Fixtures are checked into git (they're small, static, and the "what Gate N starts with" state is contract).

### Prompt shape (gate-scoped, not sprint-scoped)

Each gate eval's prompt:
1. **Establishes the pre-condition** — "Gate 1 diagnose is complete. The health assessment at `docs/refactoring/health-assessment-SPRINT-05.md` identifies …"
2. **Scopes the work to one gate** — "Run the prepare gate (Steps 3-4): write characterization tests for …, draft an ADR at `docs/architecture/adr/ADR-004.md` …"
3. **Names the stop condition** — "Stop at Gate 2. Do NOT execute any refactoring moves on `src/services/` yet."

### Assertion scope (inside one gate's boundary)

Each gate eval's assertions cover ONLY that gate's work:
- **Gate 2**: char tests exist for each service, ADR-004 exists with required sections, `src/services/` unchanged, Gate 2 summary present
- **Gate 3**: `src/services/` modified, cycle broken, public signatures preserved, `docs/architecture/` NOT modified, Gate 3 summary present

"Stop before gate N+1" assertions are verified by *absence* of next-gate artifacts in the project dir — not by transcript language. Trust files, not prose.

## Workspace path — must be outside `.claude/**`

Set `WORKSPACE_BASE = REPO_ROOT / "_artifacts" / "skills-eval" / "<skill>"` in both `run_body_evals.py` and `grade_body_evals.py`. Rationale: the with_skill subagent is instructed to read `.claude/skills/<skill>/SKILL.md`, and afterward treats `.claude/skills/**` paths as sensitive. If the fixture project ALSO lives at `.claude/skills/<skill>-workspace/…/project/`, the subagent refuses to Write into it — even though `--dangerously-skip-permissions` is in effect.

Observed consequence (v1.3.0): with_skill scored 11.1% / 18.2% on gates 2 and 4 because the subagent produced all intended artifacts as "INTENDED FILE" prose blocks in the transcript instead of persisting them. without_skill, which never reads `.claude/skills/**`, had no such heuristic and wrote the files normally, scoring 100% — producing a spurious −88.9 pp and −72.7 pp delta that reads as skill failure but is pure measurement noise.

Moving the workspace to `_artifacts/skills-eval/08-refactor/` fixed this in v1.3.1 (both configs 100% at both gates, wall-clock time for with_skill dropped ~60%).

**Rule for new eval suites:** put the workspace under `_artifacts/skills-eval/<skill>/` from day one.

## Prompt-specificity tradeoff — discrimination vs coverage

Once the path confound is removed, gate-split evals reveal a second phenomenon: **how specific the gate prompt is determines how much the skill can differentiate.**

From 08-refactor v1.3.1:

| Gate | Prompt shape | Delta |
|------|--------------|-------|
| Gate 1 diagnose | "do a health assessment before we plan sprint 5" — ambiguous | **+41.7 pp** |
| Gate 2 prepare | "write characterization tests for taskService, notificationService, userService, and draft ADR-004" — specified | 0 pp (tie 100%) |
| Gate 3 execute | "break the circular dependency using the event-emitter pattern from ADR-004" — specified | 0 pp (tie 100%) |
| Gate 4 reconcile | "update system.md entity names, mark ADR-003 as superseded, remove mongoose from package.json" — specified | 0 pp (tie 100%) |

When the prompt names every expected artifact and the approach, a capable executor baseline produces the same output as with_skill. The skill's incremental value is invisible.

**Design choice per gate:**
- **Measure skill enforcement value** (structure, gate discipline, checklist adherence) — use an *ambiguous* prompt that under-specifies what to do ("prepare the safety net and decision record, then stop")
- **Measure skill coverage** (does the skill produce the right artifacts when asked?) — use a *specified* prompt and a tight assertion list

Don't conflate them. An eval that uses a specified prompt AND asserts structure is likely to tie at 100% and tell you nothing.

## Template — gate sub-eval

```jsonc
{
  "id": <unique_id>,
  "prompt": "<pre-condition statement>. Run the <name> gate (Steps X-Y): <scoped work>. Stop at Gate N. Do NOT <out-of-scope work>.",
  "expected_output": "<deliverables>, then an explicit stop for user approval before <next gate>.",
  "files": [],
  "expectations": [
    "<positive assertion 1 — artifact exists>",
    "<positive assertion 2 — artifact structural property>",
    "<scope assertion — does NOT modify X (reserved for later gate)>",
    "<stop assertion — no next-gate artifacts in project dir>",
    "<presentation assertion — Gate N summary/decision language in transcript>"
  ]
}
```

## Runner + grader requirements

Both `run_body_evals.py` and `grade_body_evals.py` need a per-eval fixture mapping:

```python
EVAL_FIXTURES = {
    1: EVALS_DIR / "mock-project",                        # gate 1
    4: EVALS_DIR / "mock-project-gate2-input",            # gate 2
    5: EVALS_DIR / "mock-project-gate3-input",            # gate 3
    6: EVALS_DIR / "mock-project-gate4-input",            # gate 4
}
```

The grader must diff against the *starting fixture for that eval*, not the pristine `mock-project/`. Otherwise Gate 2's "new file created" assertions misfire because the health-assessment seeded in the fixture reads as a "new file vs pristine."

## When to apply the gate-split pattern

| Skill | Gates? | Apply? |
|-------|--------|--------|
| `/refactor sprint N` | 4 | **Yes** (done) |
| `/quality sprint N` | 0 (today) | Maybe (if Structured Scoring gains approval gates) |
| `/ship sprint N` | Implicit 1 (deployment confirmation) | Probably not — deployment is already gated by Git workflow |
| `/security sprint N` | 0 | No |
| `/architecture init` / `sprint N` | 0 (writes artifacts without approval loops) | No |

For gate-less skills, a single monolithic body eval is fine.

## Summary — checklist for a new gate-based eval suite

- [ ] Workspace under `_artifacts/skills-eval/<skill>/`, not `.claude/skills/**`
- [ ] One eval per gate, each with its own fixture under `evals/mock-project-gate{N}-input/`
- [ ] Fixture = previous-gate fixture + plausibly-correct prior-gate artifacts (copied in, trimmed if needed)
- [ ] `EVAL_FIXTURES` dict in both runner and grader maps eval_id → fixture
- [ ] Prompt establishes pre-condition, scopes work, names stop
- [ ] Assertions verify artifacts via file presence/diff, not transcript prose
- [ ] "Stop before gate N+1" verified by *absence* of next-gate artifacts
- [ ] Decide per-gate: ambiguous prompt (measures enforcement) or specified prompt (measures coverage)
- [ ] Record per-gate numbers in RESULTS.md; never aggregate across unrelated gates without showing the breakdown

## Source material

- `.claude/skills/08-refactor/evals/RESULTS.md` §§ v1.2.0, v1.3.0, v1.3.1 — raw findings
- `.claude/skills/08-refactor/evals/evals.json` — 4 gate evals + 2 mode evals
- `.claude/skills/08-refactor/evals/mock-project-gate{2,3,4}-input/` — fixture progression
- Memory: `feedback_skill_eval_path_heuristic.md` (path-heuristic gotcha)
