# 00-discovery evals

Follows **`/skill-creator`'s A/B method** (not a homegrown `run_*.py`/`grade_*.py`, which is a Windows
fallback only). For each test case in [`evals.json`](evals.json), run two arms and compare the skill's **lift**:

1. **with_skill** — a fresh agent loads `.agents/skills/00-discovery/SKILL.md` and performs the prompt, writing the
   spine to a workspace `outputs/` dir (treated as the project root). Because there is no interactive user, tell it to
   run autonomously past the REVIEW gate (mark gaps `[NEEDS CLARIFICATION]`, inferences `derived`).
2. **baseline** — a fresh agent performs the same prompt with **no skill** (instructed to ignore framework files).
   Shows what the skill adds.

Put workspaces **outside `.agents/skills/**`** (e.g. `_artifacts/skills-eval/00-discovery/iteration-N/<case>/<arm>/outputs/`)
to avoid the `with_skill` write-refusal heuristic.

**Grade** each `outputs/` dir deterministically — no LLM judge, because the spine is objective:

```
python check_spine.py --outputs <…/outputs> --case <rich-spec|thin-spec|undefended-bet|no-doc> [--fixture <input doc>]
```

It writes `grading.json` (`{expectations:[{text,passed,evidence}]}`) and prints a pass/fail report. For the interactive
review, point skill-creator's `eval-viewer/generate_review.py` at the iteration dir.

**Fixtures** span the fidelity spectrum: `rich-spec` (near-truth PRD), `thin-spec` (gappy brief), `undefended-bet`
(planted Unknown+Important assumption), `no-doc` (idea only → interview path), `security-flavored` (explicit refusal
rules → must-not REQ). `no-doc` has no input file.

**WS2 Task 2.1 — EARS + must-not + numbers.** `check_spine.py` now asserts, on every spine-producing case: every REQ
statement line is **EARS-form** (one of the five patterns; keyword-case significant), and no *inferred* REQ
transcribes a **quantitative claim** (currency / percentage / measured unit) without a source quote or a
`[NEEDS CLARIFICATION]` marker. For `--case security-flavored` it also requires **≥1 must-not** (Unwanted-behavior
`IF … THEN … SHALL`) REQ. Grader-validated (grader-first): a hand-ideal EARS spine passes all three; three degenerates
each fire exactly their target — marker-stripped inferred number → numbers; must-not rewritten to ubiquitous →
must-not; a committed **pre-EARS** iteration-1 output → EARS. Evidence: `_artifacts/skills-eval/00-discovery/iteration-2/`.

**WS2 Task 2.2 — CHALLENGE enrichments.** For `--case undefended-bet`, `check_spine.py` also requires the
`assumption-map.md` to record a **`## Devil's advocate`** dissent and a **`## Pre-mortem`** section (heading or bold
label) — the two anti-sycophancy forcing moves — independent of the existing willingness-to-pay-bet check.

**WS2 Task 2.3 — EXPLORE mode.** `--case explore` / `explore-refusal` grade **inverted** (via `check_explore`): the
correct state is **no spine**. Six checks: the hard invariant (nothing under `docs/spec/**`), a `docs/discovery/
exploration.md` with **≥3 origin-tagged framings**, `## Appetite`, and `## Decision`. Degenerates: a written spec file
fires the hard invariant; a 2-framing artifact fires the ≥3 check. The `explore-refusal` case asserts the divergent
round survives a converge-now prompt.

**WS2 Task 2.4 — ADOPT mode.** The `adopt-mini` fixture is copied into the workspace root (the repo IS the project).
`--case adopt` runs the base spine checks + four adopt-specific: every REQ adopt-sourced (`code:`/`docs:`),
**anti-hallucination** (every `code:<path>` resolves on disk — the extractor stops at a wrapping quote so the design's
`"adopt-confirmed: code:<path>"` form resolves), the zombie surfaced out-of-scope (not kept as a REQ), and the auth
invariant captured (a must-not REQ or a Constitution item). Degenerates: a REQ citing a nonexistent file → the
anti-hallucination check; the zombie kept as an active REQ → the zombie check.

**iteration-1:** with_skill passed every assertion on all four cases; the no-skill baseline produced no spine
(failing the gating assertion) — the lift is the entire framework contract.

**WS1 Task 1.2:** the grader gained the standing-gate assertions (`scripts/verify-spine.py` emitted at the project
root + exits 0 on the fresh spine). Per the revision A/B policy this is a template-presence assertion — the emission
was hand-applied to the iteration-1 `with_skill` outputs and re-graded green (no live re-run); live coverage arrives
with the next regenerated 00 run. The script itself is validated by
`docs/eval-methodology/integration/validate_script.py` (ideal passes; every degenerate fires its check).

## Current baselines — `with_skill`, re-baselined 2026-07-15

**Recorded here on purpose.** The previous baselines lived only in `_artifacts/skills-eval/**/iteration-N/README.md`,
which is **gitignored** — so they rotted invisibly: they recorded `rich-spec 15/15` against a grader that had since
grown to 18 assertions. A regression reference that vanishes with the workspace is not a reference. Update this table
whenever the assertion count changes.

| Case | `--case` | Score | Note |
|---|---|:---:|---|
| `rich-spec` | `rich-spec` | **17/18** | The one failure — "CHALLENGE near-silent (≤2 surfaced bets)" — is **real behavior**, not a grader defect: the run surfaced 4 bets on a near-truth PRD. Expected-red until someone decides whether 4 is wrong. |
| `thin-spec` | `thin-spec` | **12/12** | |
| `undefended-bet` | `undefended-bet` | **13/13** | |
| `no-doc` | `no-doc` | **12/12** | from `iteration-wave1-postfix2` (the arm run after the capability-trigger narrowing) |
| `security-flavored` | `security-flavored` | **11/11** | |
| `explore` | `explore` | **6/6** | graded inverted — the correct state is *no spine* |
| `explore-refusal` | `explore-refusal` | **6/6** | graded inverted |
| `adopt` | `adopt` | **14/14** | |
| `agent-brief` | **`agent`** | **16/16** | note the `--case` value is `agent`, not `agent-brief` |

Evidence: `_artifacts/skills-eval/00-discovery/iteration-wave1-postfix{,2}/` (gitignored; regenerate to re-verify).
Arms ran at `65d1516`; `no-doc` re-ran at `c52f552`. Baseline (no-skill) arms are exempt from a doctrine-edit
regression sweep — a no-skill arm cannot be reached by a doctrine change — so they were not re-run.

### Three grader defects fixed at the same time (2026-07-15)

Found while using this suite as the regression bridge for a `00-discovery` doctrine edit. **All three produced false
FAILs on correct output** — four of nine cases were red for reasons that had nothing to do with the skill. Each fix
was made by an agent with no stake in the findings, and each was validated grader-first (the check must still **bite**
its degenerate — `shared/agentic-profile.md` § the bite rule):

1. **`--case adopt` code-path resolution.** The strip only removed a single trailing `:line`, so a line **range**
   (`cli.py:18-22`) survived and could never resolve; the capture also swallowed a trailing comma from
   multi-citation sources. → `adopt` 13/14 → 14/14. Still bites: a fabricated `ghost.py:1-9` still FAILs.
2. **EARS demanded a literal `the <system> SHALL`.** `"TeamPulse SHALL send…"` — valid EARS for a proper noun —
   failed. The article is now optional in the four **delimited** patterns (WHEN/WHILE/WHERE/IF…THEN) only; the
   ubiquitous `^The .+ SHALL .+` is deliberately **unchanged**, so the user-centric anti-pattern
   (`"Users SHALL be able to…"`) still fails.
3. **`parse_blocks()` read only the first physical line** after a REQ heading. This repo wraps markdown at ~110
   chars, so **any EARS statement long enough to wrap failed** (line 1 ended at `THEN`, never reaching `SHALL`); a
   preceding HTML comment broke it the same way. Now skips comments and joins the wrapped statement to one logical
   line. → `thin-spec` 11/12 → 12/12, `agent-brief` 15/16 → 16/16. This was the largest of the three and was found
   only because fixing (2) failed to move two cases.

Bite proof for all three: the committed pre-EARS `iteration-1` outputs **still FAIL** the EARS check (rich-spec
14/18), and statements with no delimiter, no `SHALL`, or a user-centric subject still fail.

**Known, not fixed:** `no-doc` REQ-009/REQ-015 use `MAY` instead of `SHALL` in a `WHERE` statement — a genuine
authoring slip in that arm, not a grader defect (`WHERE` is EARS's optional-feature form; `MAY` is a MoSCoW
*priority*, not a modal for the statement body).
