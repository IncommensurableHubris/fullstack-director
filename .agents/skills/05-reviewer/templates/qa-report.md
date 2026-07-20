<!-- Filename: docs/quality/qa-report-sprint-NN.md  (qa-report-full.md for review_mode: full;
     qa-report-patch-NNN.md for a patch review — which also carries `patch: patch-NNN`). -->
<!-- budget: ≤150 lines — longer means restated methodology or narrative; evidence rows, one home per fact. -->

---
verdict:          SHIP        # SHIP | FIX REQUIRED | BLOCK
sprint:           NN          # patch reviews: replace with  patch: patch-NNN
review_mode:      sprint      # sprint | full | patch
baseline_commit:  <the SHA reviewed — must equal the handoff's baseline_commit>
final_commit:     <the SHA the oracles ran at — the handoff's final_commit; 06's code-identity anchor (G5)>
spec_slice_hash:  match       # match | mismatch  (05 recomputed vs the handoff; mismatch ⇒ BLOCK)
build_conversation: not-provided   # the isolation attestation core — 05 was seeded with ONLY the handoff + spec slice
findings_high:    0
findings_medium:  0
findings_low:     0
ledger_executed:  0
ledger_observed:  0
ledger_inferred:  0
ledger_total:     0
must_gap:         false       # true if any in-scope MUST/P0 REQ is uncovered ⇒ cannot be SHIP
eval_floors_met:  n/a         # true | false | n/a  (agent-system: every re-run eval floor met + grader bit; false ⇒ not SHIP; n/a = no eval-suite REQ in scope). 06 G8 reads this exact token.
evals_run:        0           # <int> — how many eval suites 05 re-ran at final_commit (0 when n/a)
---

# QA Report — Sprint NN

> **The verdict a human and `06-release` act on without re-reviewing the code.** Owned by **skill 05 (reviewer)**,
> written from a **fresh context** seeded with ONLY `04`'s build-handoff + the spec-slice paths — never the build
> conversation. 05 is **read-only**: it renders a verdict and (for testable defects) commits a reproducing RED test;
> it **never edits implementation** — fixes loop to `04`. The frontmatter above is the machine-readable tally (`06`
> gates on it); the sections below are the evidence. Craft: `references/review-discipline.md` +
> `references/verification-evidence.md`.

## (a) Verdict

**SHIP | FIX REQUIRED | BLOCK** — _<one line: the single most decision-relevant fact. e.g. "FIX REQUIRED — REQ-008
> grouping is broken (a reproducing RED test is committed) and REQ-009 is claimed FULL but has no covering test.">_

<!-- Honesty gate: this word MUST agree with the frontmatter. SHIP is impossible while ledger_inferred > 0 or
     must_gap: true or spec_slice_hash: mismatch. If they disagree, the report is wrong — fix it before emitting. -->

## (b) Verification Ledger

**Executed X · Observed Y · Inferred Z / Total T.** _(SHIP requires Inferred = 0 over in-scope behaviors.)_

| # | Behavior (Done When / VC row) | → REQ | State | Evidence (test:line · screenshot · transcript) | Result |
|---|-------------------------------|-------|-------|-------------------------------------------------|--------|
| 1 | _<a second standup for the same member+day replaces the first>_ | _<REQ-001>_ | _<EXECUTED>_ | _<test/digest.test.js:12 → PASS; `node --test`>_ | _<PASS>_ |
| 2 | _<each member grouped under their display name>_ | _<REQ-008>_ | _<EXECUTED>_ | _<test/digest.test.js:31 → FAIL (impl groups only the first member)>_ | _<FAIL>_ |

<!-- INFERRED always counts as NOT verified. An INFERRED in-scope row makes SHIP unreachable — escalate it via the
     fallback cascade (verification-evidence.md) or it forces FIX REQUIRED / BLOCK. -->

## (c) Traceability

> Every in-scope REQ → its frozen outcome-Gherkin → the covering test `file:line` → PASS/FAIL, and FULL/PARTIAL/NONE.
> A **MUST** REQ at NONE (or claimed FULL with no real covering test) is a MUST-gap ⇒ FIX REQUIRED.

| REQ | Priority | Outcome-Gherkin (the frozen "Then") | Covering test (file:line) | Result | Coverage |
|-----|----------|-------------------------------------|---------------------------|--------|----------|
| _<REQ-001>_ | _<MUST>_ | _<the day still holds exactly one standup for that member>_ | _<test/digest.test.js:12>_ | _<PASS>_ | _<FULL>_ |
| _<REQ-008>_ | _<MUST>_ | _<each member's entry grouped under their display name>_ | _<test/digest.test.js:31>_ | _<FAIL>_ | _<PARTIAL>_ |
| _<REQ-009>_ | _<SHOULD>_ | _<all flagged blockers appear together in a top section>_ | _<— none found (handoff claimed FULL)>_ | _<FAIL>_ | _<NONE>_ |

## (d) Findings

> The executable, routed interface — **not** prose. Each finding: severity (re-derived by consequence), the REQ/VC it
> violates, a `file:line`, the route (**code/test → `04`** · **realization-spec → `03`** · **declaration → `00`/gate**),
> and — for a *testable* defect — the committed reproducing **RED test** (05 owns RED, `04` owns GREEN; `04` may not
> edit it). A clean review has **no rows here** — never manufacture findings to look thorough.

| # | Severity | REQ / VC | Location (file:line) | Finding | Route | Evidence / RED test |
|---|----------|----------|----------------------|---------|-------|---------------------|
| _<1>_ | _<high>_ | _<REQ-008 / VC-02>_ | _<src/digest.js:18>_ | _<assembleDigest returns only the first member's entry; violates "each member grouped under their display name">_ | _<code → 04>_ | _<test/review/req-008-grouping.test.js → RED>_ |
| _<2>_ | _<high>_ | _<REQ-009 / VC-03>_ | _<handoff (b) VC-03 row>_ | _<claimed FULL/EXECUTED but no test asserts the needs-help section; a dishonest coverage claim>_ | _<test → 04>_ | _<coverage arithmetic; no oracle exists>_ |
| _<3>_ | _<medium>_ | _<REQ-001 / VC-01>_ | _<test/digest.test.js:8>_ | _<the dedup test is tautological — the suite stays green when the dedup line is mutated>_ | _<test → 04>_ | _<mutation litmus: flipped `===`→`!==`, suite still PASS>_ |

<!-- If clean: replace the rows with a single line — "No findings. Clean review." -->

## (e) Capability Probe

> Every runtime attempted, with the exact command + exit code. **No row may read NOT_ATTEMPTED.** A capability that
> genuinely will not run holds its failing command + output here (a cited fact, not an excuse).

| Capability | Command attempted | Exit code | Output excerpt |
|------------|-------------------|-----------|----------------|
| _<Unit runner>_ | _<`node --test test/digest.test.js`>_ | _<0>_ | _<# pass 5 / # fail 0>_ |
| _<Oracle re-run @ final_commit>_ | _<`node --test`>_ | _<0>_ | _<confirms handoff EXECUTED claims>_ |
| _<Browser (Playwright MCP)>_ | _<— n/a: headless slice, no web container (system.md §…)>_ | _<n/a>_ | _<no UI this sprint>_ |

## (f) Context attestation (the isolation proof)

- **inputs:** `[build-handoff, spec slice]` · **build conversation: not provided** _(seeded fresh; the builder's
  reasoning was never read)._
- **baseline_commit reviewed:** _<SHA>_ — equals the handoff's `baseline_commit` and resolves in the repo.
- **spec_slice_hash:** _<match | mismatch>_ — 05 recomputed over `sprint-NN.md` (+ manifest) and compared to the
  handoff. _(mismatch ⇒ BLOCK: the spec slice drifted between build and review.)_
- **opened files ⊆ seed:** _<the handoff, the spec-slice paths, `src/**` at final_commit — and nothing from the build
  session>._

<!-- This section is what makes "isolated" auditable rather than asserted. The eval greps it; a human confirms the
     parent transcript carries no builder-reasoning markers (the manual half of the isolation proof). -->

## (g) Next command (05 recommends; the director runs it — 05 never auto-drives the loop)

- **SHIP** → `/06-release sprint NN` _(optionally `/07-security sprint NN` first)._
- **FIX REQUIRED** → `/04-builder sprint NN` — the fix pass reads this report's findings + the committed RED tests,
  drives each to green (never editing a reviewer-authored test), and re-emits the handoff for a **fresh** 05 re-review.
- **BLOCK** → route per the finding: a wrong **realization** → `/03-architect`; a wrong **declaration** or a
  `spec_slice_hash` mismatch → `/00-discovery` / the release gate.

## Session summary (paste as the conversational reply — lead with the ledger + verdict, never narrative)

```
QA — SPRINT NN — <SHIP | FIX REQUIRED | BLOCK>
Verification: Executed X · Observed Y · Inferred Z / Total T
Findings: high H · medium M · low L    spec_slice_hash: <match|mismatch>
Isolation: inputs [handoff, spec slice]; build conversation not provided
<if Inferred > 0: list each unverified behavior + why>
Report: docs/quality/qa-report-sprint-NN.md   Next: <the (g) command>
```

<!-- Consistency rule: if Inferred > 0 (or must_gap) and this line says SHIP, STOP — rewrite. The summary is the only
     surface the user always reads; any gap not on this line is hidden. -->
