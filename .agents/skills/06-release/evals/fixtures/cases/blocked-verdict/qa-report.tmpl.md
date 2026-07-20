---
verdict:          FIX REQUIRED
sprint:           01
review_mode:      sprint
baseline_commit:  {{baseline_commit}}
final_commit:     {{final_commit}}
spec_slice_hash:  match
build_conversation: not-provided
findings_high:    2
findings_medium:  0
findings_low:     0
ledger_executed:  1
ledger_observed:  0
ledger_inferred:  1
ledger_total:     3
must_gap:         true
---

# QA Report — Sprint 01

> Written by **skill 05 (reviewer)** from a fresh context seeded with ONLY the build-handoff + the spec-slice paths.

## (a) Verdict

**FIX REQUIRED** — REQ-008 grouping is broken (a reproducing RED test is committed at
`test/review/req-008-grouping.test.js`) and REQ-009 is claimed FULL but has no covering test (a dishonest coverage
claim). A MUST-gap exists; one behavior is still INFERRED.

## (b) Verification Ledger

**Executed 1 · Observed 0 · Inferred 1 / Total 3.** _(SHIP requires Inferred = 0.)_

| # | Behavior (Done When / VC row) | → REQ | State | Evidence | Result |
|---|-------------------------------|-------|-------|----------|--------|
| 1 | a second standup for the same member+day replaces the first | REQ-001 | EXECUTED | test/digest.test.js:9 → PASS | PASS |
| 2 | each member grouped under their display name | REQ-008 | EXECUTED | test/review/req-008-grouping.test.js → FAIL (impl groups only the first member) | FAIL |
| 3 | needs-help blockers collected into the top section | REQ-009 | INFERRED | no covering test found (handoff claimed FULL) | FAIL |

## (c) Traceability

| REQ | Priority | Outcome-Gherkin (the frozen "Then") | Covering test (file:line) | Result | Coverage |
|-----|----------|-------------------------------------|---------------------------|--------|----------|
| REQ-001 | MUST | the day still holds exactly one standup for that member | test/digest.test.js:9 | PASS | FULL |
| REQ-008 | MUST | each member's entry grouped under their display name | test/review/req-008-grouping.test.js | FAIL | PARTIAL |
| REQ-009 | SHOULD | all flagged blockers appear together in a top section | — none found (handoff claimed FULL) | FAIL | NONE |

## (d) Findings

| # | Severity | REQ / VC | Location (file:line) | Finding | Route | Evidence / RED test |
|---|----------|----------|----------------------|---------|-------|---------------------|
| 1 | high | REQ-008 / VC-02 | src/digest.js:15 | assembleDigest keeps only the first member's entry; violates "each member grouped under their display name" | code → 04 | test/review/req-008-grouping.test.js → RED |
| 2 | high | REQ-009 / VC-03 | handoff (b) VC-03 row | claimed FULL/EXECUTED but no test asserts the needs-help section | test → 04 | coverage arithmetic; no oracle exists |

## (e) Capability Probe

| Capability | Command attempted | Exit code | Output excerpt |
|------------|-------------------|-----------|----------------|
| Unit runner | `node --test` | 0 | # pass 3 / # fail 0 (the suite is green — the grouping gap is hidden behind a single-member test) |
| Reviewer RED test | `node --test test/review/` | 1 | req-008-grouping FAILS against the current impl |

## (f) Context attestation (the isolation proof)

- **inputs:** `[build-handoff, spec slice]` · **build conversation: not provided**.
- **baseline_commit reviewed:** {{baseline_commit}} — equals the handoff's and resolves in the repo.
- **final_commit (oracles ran at):** {{final_commit}}.
- **spec_slice_hash:** match.
- **opened files ⊆ seed.**

## (g) Next command

- **FIX REQUIRED** → `/04-builder sprint 01` (the fix pass: make the committed RED test green, re-emit the
  handoff), then a **fresh** `/05-reviewer sprint 01` re-review.
