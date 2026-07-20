# 01-planner evals

Follows **`/skill-creator`'s A/B method** (not a homegrown `run_*.py`/`grade_*.py`, which is a Windows
fallback only). The input here is a **spine** (what skill 00 produces), not a raw doc. For each case in
[`evals.json`](evals.json), run two arms and compare the skill's **lift**:

1. **with_skill** — a fresh agent loads `.agents/skills/01-planner/SKILL.md` and decomposes the seeded spine, writing
   the build plan under `docs/planning/`. Because there is no interactive user, tell it to run autonomously **past the
   light GATE** (proceed without waiting for PROCEED/ADJUST).
2. **baseline** — a fresh agent performs the same prompt with **no skill** (instructed to ignore framework files).
   Shows what the structured contract adds over an ad-hoc plan.

## Workspace setup (the input is a spine — seed it first)

Put workspaces **outside `.agents/skills/**`** (e.g. `_artifacts/skills-eval/01-planner/iteration-N/<case>/<arm>/outputs/`)
to avoid the `with_skill` write-refusal heuristic. The agent's `outputs/` dir **is the project root** and must be
**pre-seeded with the spine** so the skill can read it and add planning artifacts beside it:

```
# seed cleanly — do NOT pre-create outputs/docs (cp would nest docs/docs)
mkdir -p <…>/<arm>/outputs
cp -r evals/fixtures/<case>/docs <…>/<arm>/outputs/docs
```

Seeding both arms identically also lets the grader prove the **two-status separation** — that the skill left the
spine registry (`docs/spec/specification.md`) untouched and wrote execution status only into the ledger.

For the **patch cases** the fixture also carries code — seed `docs/`, `src/`, and `tests/`. After a run, save the
agent's final message as `outputs/final-response.md` (the hidden-scope case grades the visible escalation from it).

## Grade (deterministic — no LLM judge, because the contract is objective)

```
python check_backlog.py --outputs <…/outputs> --case <teampulse|foundation-chain>
python check_patch.py   --outputs <…/outputs> --case <patch-small|patch-hidden-scope|patch-ceremony-decline> \
                        [--fixture evals/fixtures/patchable]
```

It writes `grading.json` (`{expectations:[{text,passed,evidence}]}`) into `--outputs` and prints a pass/fail report.
Copy `grading.json` up to the arm root (`<arm>/grading.json`) so skill-creator's `eval-viewer/generate_review.py`
renders the verdict. For the interactive/static review, point the viewer at the iteration dir:

```
python <skill-creator>/eval-viewer/generate_review.py <iteration-dir> --skill-name 01-planner --static <out.html>
```

## What the assertions check (the lift is STRUCTURAL)

01-planner's value is the **structured contract the next skills consume**, not prose insight (a strong baseline also
writes reasonable epics). So the discriminating assertions are structural: a `docs/planning/backlog.md` ledger that
maps **every spine REQ exactly once** to a build-order epic + sprint + **execution** status; **build-order** epics
(foundation before consumers); a zero-padded `sprint-01.md` walking skeleton that threads the core path end-to-end
across ≥2 domains and carries a **frozen Gherkin snapshot** + a **"Done When"**; and the **two-status separation**
(execution status never leaks into the spine registry). A baseline writes an ad-hoc plan that misses this contract.

## Fixtures

- **`teampulse`** — the rich, near-truth spine produced by 00's `rich-spec` eval (10 REQs across 3 domains: standups,
  team, digest). Exercises the full contract, an explicit access foundation (magic-link auth REQ-007 + team), and
  risk-first sequencing (its `assumption-map.md` flags **A1 async-completion** — sprint 1 should de-risk it).
- **`foundation-chain`** — a compact spine (PennyPilot, 5 REQs) whose **foundation REQ sorts LAST in the registry**
  (`REQ-005 Connect a bank account`, domain `accounts`). It tests that the planner truly **reorders domain → build
  order** rather than echoing registry order — the foundation must land in the first epic / sprint 1.
- **`patchable`** — a **mid-life** TeamPulse (spine + decomposed backlog with a shipped `sprint-01` + a tiny
  `src/`/`tests/` tree). Serves the three WS1 **patch-lane** cases: `patch-small` (a boundary bug owned by REQ-008 →
  certify + record + dispatch), `patch-hidden-scope` (a "fix" that is really an unowned notification capability →
  refuse, route to `/00-discovery reflect`), `patch-ceremony-decline` (a patch-class fix pitched with
  "plan whatever process is needed" → no sprint/design/architecture ceremony). `check_patch.py` was validated
  before the live runs: 3 hand-ideals pass; 7 degenerates (dangling REQ · status field on the record · missing
  ledger row · spine drift · unevidenced gate · patched-anyway · sprint ceremony) each fire exactly their target.

## iteration-1

| Case | with_skill | baseline |
|------|:----------:|:--------:|
| `teampulse` | **9/9** | 4/9 |
| `foundation-chain` | **9/9** | 3/9 |

**with_skill passed every assertion on both cases.** Both baselines were *strong* on prose — they independently
produced risk-first walking skeletons, caught the A1 adoption bet, and reasoned out build order — but neither
produced the **structured contract** the next skills consume. The baselines instead wrote slice-keyed backlogs
(`BL-01…`/30 sprint-sized rows with a separate REQ *coverage* table, so each REQ recurs across many rows rather than
appearing **once** in a REQ→epic→sprint→status ledger), used non-contract status vocab (`todo`), and wrote the sprint
file to `docs/planning/sprint-01.md` or `sprint-1.md` instead of the canonical zero-padded
`docs/planning/sprints/sprint-01.md`. So they failed exactly-once coverage, the execution-status check, the canonical
sprint path, build-order epic extraction, and the vertical-slice check — **the lift is the structured contract, not
the insight** (per the framework's structural-lift principle). The static viewer is at
`_artifacts/skills-eval/01-planner/iteration-1/review.html` (gitignored run workspace).

## iteration-2 (WS1 patch mode)

| Case | with_skill | baseline |
|------|:----------:|:--------:|
| `patch-small` | **9/9** | 2/9 |
| `patch-hidden-scope` | **5/5** | 2/5 |
| `patch-ceremony-decline` | **4/4** | 2/4 |

**with_skill green on all three patch cases.** The baselines re-proved the structural-lift doctrine: the
`patch-small` baseline **implemented the fix itself** (grade-your-own-homework — the exact separation-of-duties
failure the certify seat exists to prevent) and recorded it as a non-canonical `patch-01.md` with no frontmatter
contract, no `planned` ledger row, and no dispatch; the `patch-hidden-scope` baseline *did* catch the hidden scope
(strong triage) but **appended an amendment row to the spine's `amendment-log.json`** (01 has no append authority
outside the S1 case) and left a triage file in `docs/planning/patches/` — both structural violations the grader
fired on; the `ceremony-decline` baseline declined ceremony but used non-canonical naming (`PATCH-01`,
`patch-01-digest-header-timezone.md`). The lift is the certified, ledger-recorded, dispatch-ready contract.
