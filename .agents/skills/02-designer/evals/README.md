# 02-designer evals

Follows **`/skill-creator`'s A/B method** (not a homegrown `run_*.py`/`grade_*.py`, which is a Windows
fallback only). The input here is a **spine slice** (a spine + a `sprint-01.md`), like 01 — not a raw doc. For each
case in [`evals.json`](evals.json), run two arms and compare the skill's **lift**:

1. **with_skill** — a fresh agent loads `.agents/skills/02-designer/SKILL.md` and realizes the design for sprint 1,
   writing under `docs/design/` and appending `docs/spec/amendment-log.json`. Because there is no interactive user,
   tell it to run autonomously **past both gates** (proceed without waiting; approve its own batched Tier-2
   amendments so they land as `approved` rows).
2. **baseline** — a fresh agent performs the same prompt with **no skill** (instructed to ignore framework files).
   Shows what the structured contract + the dual-pass Reconcile add over an ad-hoc design doc.

## Workspace setup (the input is a spine — seed it first)

Put workspaces **outside `.agents/skills/**`** (e.g.
`_artifacts/skills-eval/02-designer/iteration-N/<case>/<arm>/outputs/`) to avoid the `with_skill` write-refusal
heuristic. The agent's `outputs/` dir **is the project root** and must be **pre-seeded with the spine** so the skill
can read it and add the design beside it:

```
# seed cleanly — do NOT pre-create outputs/docs (cp would nest docs/docs)
mkdir -p <…>/<arm>/outputs
cp -r evals/fixtures/<case>/docs <…>/<arm>/outputs/docs
```

Seeding both arms identically also lets the grader prove the skill **left `docs/spec/capabilities/` untouched** and
wrote its challenge only as **structured amendment rows**.

## Grade (deterministic — no LLM judge, because the contract + the WCAG check are objective)

```
python check_design.py --outputs <…/outputs> --case <clean-intent|contrast-conflict|derived-intent>
```

It writes `grading.json` (`{expectations:[{text,passed,evidence}]}`) into `--outputs` and prints a pass/fail report.
Copy `grading.json` up to the arm root (`<arm>/grading.json`) so skill-creator's `eval-viewer/generate_review.py`
renders the verdict. For the interactive/static review, point the viewer at the iteration dir:

```
python <skill-creator>/eval-viewer/generate_review.py <iteration-dir> --skill-name 02-designer --static <out.html>
```

## What the assertions check (the lift is STRUCTURAL + amendment-aware)

02-designer's value is the **structured design contract** the next skills consume **plus** the debut of the amendment
protocol — not prose design insight (a strong baseline also designs well; design *beauty* is not graded). So the
discriminating assertions are structural + amendment-aware: a `docs/design/design-system.md` with **tiered tokens**
(a primitive layer + the semantic role vocabulary) that **references REQs**; **>=1 `<screen>.md`** referencing the
sprint's REQs; a **DM-ID manifest**; an owner-tagged **DDR** section; and the **Reconcile rows** in
`amendment-log.json`. The one move that makes a *design* contradiction gradeable without a judge is the **WCAG
relative-luminance contrast computation** (`check_design.py` implements sRGB → luminance → ratio): a planted, stated
brand color that fails AA against a stated a11y mandate must be caught as a **Tier-2 gated row**, recomputed by the
grader to prove the catch was warranted. A baseline writes a design doc but not tiered tokens referencing REQs, no
DM-manifest, no WCAG-checked amendment rows, and no DDRs.

## Fixtures (the variable under test is `design-intent.md`)

- **`aurora-clean`** — a compact reading-app spine (3 REQs across `library` + `reader`) whose `design-intent.md` is
  fully `stated` and whose brand `#1A56DB` **passes** AA (6.18:1 on white). Exercises the full contract and the
  **false-positive** check: a clean intent should yield ~zero amendments.
- **`aurora-contrast`** — the **same Aurora spine**, differing in exactly one value: the brand is `#7FB3FF`, stated
  for button/link **text**, which **fails** AA (~2.14:1 on white) against the stated "WCAG 2.2 AA" floor. The
  airtight deterministic discriminator — isolating the brand hex means any behavior delta is attributable to the
  contradiction alone.
- **`teampulse`** — the rich spine from 00/01 (10 REQs, 3 domains) whose `design-intent.md` brand adjectives are
  `derived` / `[NEEDS CLARIFICATION]` and which specifies **no tokens**. Exercises the **flesh-out** component:
  concretize the brand via a Tier-2 row, and produce concrete tokens the thin intent lacked.

## iteration-1

| Case | with_skill | baseline |
|------|:----------:|:--------:|
| `clean-intent` | **9/9** | 4/9 |
| `contrast-conflict` | **9/9** | 5/9 |
| `derived-intent` | **9/9** | 2/9 |

**with_skill passed every assertion on all three cases (27/27, 100%); baselines averaged 41% (11/27).** The
baselines were *strong on design craft* — each independently produced a sensible token set, held scope discipline,
and even **reasoned out the contrast conflict** (the `contrast-conflict` baseline computed `#7FB3FF` at 2.14:1 and
introduced an accessible variant; the `derived-intent` baseline concretized the brand from the thin intent) — but
**none produced the structured contract the next skills consume**: tiered primitive→semantic tokens with the
governed vocabulary, the DM-ID manifest, owner-tagged DDRs, or — decisively — a single **structured
`amendment-log.json` row**. Both "catching" baselines buried their finding as **prose** in the design doc (invisible
to `/status`, the release gate, and `03`/`05`), and several wrote a nested `docs/design/design-system/` directory
instead of the canonical `design-system.md` and skipped the manifest entirely. The `with_skill` arms emitted exactly
the right amendments — **1** Tier-2 `approved` row for `contrast-conflict` (the WCAG catch, recomputed by the grader
to 2.14:1) and **3** flesh-out rows for `derived-intent` (brand adjectives, the unstated a11y floor, the derived key
screens), and **0** for `clean-intent` (the over-trigger guard holding on a clean, AA-passing intent). **The lift is
the structured contract + the amendment semantics, not design insight** (per the framework's structural-lift
principle). The static viewer is at `_artifacts/skills-eval/02-designer/iteration-1/review.html` (gitignored run
workspace).
