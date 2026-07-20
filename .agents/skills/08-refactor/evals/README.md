# 08-refactor evals

Follows **`/skill-creator`'s A/B method** (deterministic grader; no LLM judge). The input is a seeded **pre-refactor
project state** — a git repo whose **root commit** carries TeamPulse's sprint-02 HTTP surface (the pure `digest.js`
core + `store.js` + `auth.js` + `server.js`), a spine (`docs/spec/**`), the realization docs (`docs/architecture/**`,
including `system.md` §5's module inventory), and a **green, biting** behavior oracle at `test/api.test.js`. For each
case in [`evals.json`](evals.json), run two arms and compare the skill's **lift**:

1. **with_skill** — a fresh agent loads `.agents/skills/08-refactor/SKILL.md` and runs `08-refactor sprint 2`:
   assesses health, executes a **behavior-preserving** refactor in baby steps under the oracle, reconciles the
   realization docs LOCALLY, and appends an `amendment-log.json` row **only** for a declaration contradiction.
2. **baseline** — a fresh agent performs the same prompt with **no skill** (ignore framework files). Shows what the
   *provably* behavior-preserving, correctly-routed refactor adds over an ad-hoc cleanup.

## Why a pre-refactor fixture (and a fixture-builder, not `cp`)

08 **changes** `src/**` while preserving behavior — the inverse of 07 (which proves value by `src/**` being
byte-identical). So the fixture ships a real behavior **oracle** (`test/api.test.js`) that is **green and biting** at
the root commit; 08 must keep it green **without editing it**. [`build_fixture.py`](build_fixture.py) assembles the git
repo (seed spine + realization docs + the built slice + the case overlay; root = the pre-refactor commit; `.env`
synthesized, gitignored) and **self-checks** the seeded suite is green and biting (a malformed oracle fails the build
loudly). The grader compares the **working tree** against the **root commit** — so it is robust to however 08's
baby-steps commits land.

```
python build_fixture.py --case <needs-refactor|clean|reconcile|behavior-trap> --out <arm>/outputs
# ... arm runs `08-refactor sprint 2` over outputs/ ...
python check_refactor.py --outputs <arm>/outputs --case <case>
```

`check_refactor.py` writes `grading.json` (`{expectations:[{text,passed,evidence}]}`) into `--outputs`; copy it to the
arm root for `eval-viewer/generate_review.py`. **08 is SEQUENTIAL** — no subagents, so there is **nothing to relax** in
the harness `<SUBAGENT-STOP>` (unlike 03/05/07). Workspaces live **outside `.agents/skills/**`** (e.g.
`_artifacts/skills-eval/08-refactor/iteration-N/<case>/<arm>/outputs/`).

## What the assertions check (the lift is BEHAVIOR-PRESERVATION + ROUTING + F1, never refactor prose)

08's value is **not** "cleaner code" — a strong baseline refactors too. It is the **provably behavior-preserving
change** + the **correctly-routed reconcile** that `/status` and `06`'s release gate can trust. The deterministic
discriminators (reusing 04's `run_node_test`/`mutation_kills` and 03's amendment-row/token checks):

- **Behavior preserved, provably** — the oracle `test/api.test.js` is **blob-SHA-unchanged** vs the pre-refactor commit
  (the refactor did **not** rewrite its own tests to fake green), `node --test` is **green** at HEAD, and the suite
  still **bites** (a single-point mutation fails it). *The killer pair: a refactor that breaks behavior (red suite) or
  weakens the oracle (blob mismatch) fails deterministically.*
- **Smell actually removed** — the duplicated block collapses to **one** occurrence; the dead export is **gone**
  (specific signatures, never a bare "duplication" word — the 07 grader-hardening lesson).
- **Local-vs-declaration routing (the F1)** — `needs-refactor`/`clean`/`behavior-trap` must append **zero** amendment
  rows (a code↔doc drift is a **local** `system.md` fix); `reconcile` must append a **Tier-2 gated** row + a resolving
  ADR (a declaration contradiction escalated, **not** silently fixed). The two directions are equal-and-opposite
  disqualifiers.
- **Crying-wolf guard** — `clean` returns **ACCEPT** with `src/**` byte-identical (no invented refactor, no invented
  amendment).
- **The behavior-trap discriminator** — a **false duplication** the oracle pins; a naive "remove the duplication"
  collapse breaks a path (the oracle goes red). Both divergent operators must survive.

A baseline refactors ad-hoc: it may rewrite the oracle to make it pass, break a subtle behavior, cry wolf on clean
code, collapse a false duplication, or silently "fix" a declaration contradiction locally (no amendment row). That gap
is the graded lift.

## The four fixtures (a two-axis F1 + the appender arm)

- **`needs-refactor`** (sensitivity + local reconcile + **no** amendment) — verbatim duplication (`assembleTeamDigest`
  copy-pastes `assembleDigest`) + a dead export (`legacyDigestText`) + a planted `system.md` drift (a phantom
  `src/reporting.js`). → dedupe + delete dead code (behavior preserved), reconcile `system.md` locally, **zero** rows.
- **`clean`** (specificity — the crying-wolf guard) — the hardened app/ → **ACCEPT**, `src/**` unchanged, no amendment.
- **`reconcile`** (the appender arm) — a stated **in-memory** datastore vs a stated **multi-instance** scale mandate →
  a **Tier-2 gated** amendment (AMD-003) + a resolving **ADR-003** naming a client-server store (tech-mandate flow).
- **`behavior-trap`** (behavior-preservation as a discriminator) — a **false duplication** (`dailyView` exact-day vs
  `cumulativeView` up-to-day) → the tempting collapse breaks a path; 08 must preserve behavior + keep both operators.

## Grader validated (not vacuous)

Before any A/B run, `check_refactor.py` was validated against **hand-built ideal outputs** AND **degenerate** ones:

| Output | Case | Score |
|--------|------|:-----:|
| hand-ideal (dedupe + dead-code removed + system.md reconciled, no amendment) | `needs-refactor` | **14/14** |
| hand-ideal (ACCEPT, src unchanged) | `clean` | **7/7** |
| hand-ideal (Tier-2 gated AMD-003 + resolving ADR-003) | `reconcile` | **8/8** |
| hand-ideal (shared shaping extracted, both operators preserved) | `behavior-trap` | **10/10** |
| **behavior-breaker** (dedupe'd but broke `assembleTeamDigest`) | `needs-refactor` | **12/14** — behavior-green + oracle-bites fire |
| **oracle-faker** (rewrote the golden master to weaken it) | `needs-refactor` | **12/14** — oracle-UNCHANGED + bites fire |
| **crying-wolf** (invented a refactor + an amendment on clean code) | `clean` | **5/7** — src-unchanged + non-amender fire |
| **mis-router** (didn't escalate — no amendment row) | `reconcile` | **4/8** — all 4 appender checks fire |
| **trap-collapser** (collapsed the false duplication) | `behavior-trap` | **7/10** — behavior-green + bites + divergence fire |

So the discriminators are **real, not vacuous**: the grader penalizes a behavior-breaker (a broken refactor), an
oracle-faker (a rewritten safety net), a cry-wolf (a refactor invented on clean code), a mis-router (a declaration
contradiction silently fixed locally), **and** a trap-collapser (a false duplication collapsed) — while crediting a
correct, provably behavior-preserving, correctly-routed refactor. (A key grader hardening: the smell-removal checks
require the **specific signature** — the needs-help mapping literal, `legacyDigestText`, the `e.day === day` /
`e.day <= day` operators — never a bare "duplication"/"dead code" word, so a report that merely *lists* the smell gets
no removal credit.)

## iteration-1

| Case | with_skill | baseline |
|------|:----------:|:--------:|
| `needs-refactor` | **14/14** | 13/14 |
| `clean` | **7/7** | 6/7 |
| `reconcile` | **8/8** | 8/8 |
| `behavior-trap` | **10/10** | 9/10 |

**with_skill passed every assertion on all four cases (39/39, 100%); baselines averaged 92% (36/39).** The baselines
were **strong refactorers** — exactly as the framework's eval doctrine (`feedback_framework_skill_lift_is_structural`)
predicts, **detection quality was not the differentiator**: every baseline genuinely preserved behavior (oracle green,
unchanged, biting), the `behavior-trap` baseline **recognized the false duplication** and parameterized the day
predicate (keeping both views distinct — a legitimate 9/10), and the `reconcile` baseline **caught the datastore↔scale
contradiction and wrote a valid Tier-2 amendment + a resolving ADR** (a legitimate **8/8 tie** — a strong baseline that,
given the amendment-log schema, produced the structured record).

**The lift is the machine-readable structural contract the baselines produced inconsistently:**

- **The machine verdict (the headline lift — 3 of the 4 non-tie points).** All three non-tie baselines emitted a
  **prose verdict** their release gate cannot read — `needs-refactor` → **"HEALTHY"**, `clean` → **"NO REFACTOR"**,
  `behavior-trap` → **"REFACTORED"** — so `06-release`'s G-gate and `/status` could not parse a
  PASS/PARTIAL/BLOCKED/ACCEPT signal off them. The `with_skill` arms emitted the framework vocabulary
  (`CLEAN` / `ACCEPT` / `BLOCKED` / `CLEAN`) in the report frontmatter. A refactor that is correct but stamps "HEALTHY"
  is invisible to the gate.
- **Decisiveness on the tech-mandate (the `reconcile` tie's residue).** The deterministic grader credits both arms
  8/8, but the `with_skill` arm resolved the Tier-2 **decisively** — `disposition: approved`, `resolved_by: ADR-003`
  naming **PostgreSQL**, the constraint amended in both altitudes — while the baseline left AMD-003 **`pending`** and
  ADR-003 **"Proposed"** with *two undecided options* and `[NEEDS CLARIFICATION]` markers (which `06` then **blocks**
  on). Both are defensible; the skill drives the crisper, gate-clearing resolution. (Not deterministically graded —
  judgment quality, noted honestly.)

Across every arm the `with_skill` refactor was **provably behavior-preserving** (the oracle blob-unchanged, green, and
biting — the deterministic honesty gate), **correctly routed** (a code↔doc drift fixed locally with **zero** amendment
rows on 3 cases; a declaration contradiction escalated as a Tier-2 row on `reconcile`), and **machine-verdicted**. That
gap — the structured, gate-readable contract — is the graded lift. (Run workspace:
`_artifacts/skills-eval/08-refactor/iteration-1/`, gitignored.)

> **Grader hardening during iteration-1** (validated on the real arms, per `feedback_grader_validate_on_real_outputs`):
> two false-negatives were fixed before finalizing — (1) `mutation_kills` now tries **every** operator occurrence
> (not just the first) across **test-imported files first**, so an agent comment like `(=== day)` can't shield the
> code operator; (2) the `behavior-trap` divergence check is now **behavioral** (a `node -e` probe that dailyView and
> cumulativeView still return different counts), robust to a valid parameterized-callback refactor a syntactic regex
> would wrongly fail. Ideals still score full and every degenerate still loses the right points after both fixes.

