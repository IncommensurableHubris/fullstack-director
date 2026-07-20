<!-- Filename: docs/quality/qa-report-sprint-01.md -->

---
verdict:          FIX REQUIRED
sprint:           01
review_mode:      sprint
baseline_commit:  <the reviewed defective build's commit>
spec_slice_hash:  match
build_conversation: not-provided
findings_high:    1
findings_medium:  0
findings_low:     0
ledger_executed:  2
ledger_observed:  0
ledger_inferred:  1
ledger_total:     3
must_gap:         true
---

# QA Report — Sprint 01

> **The verdict a human and `06-release` act on without re-reviewing the code.** Owned by **skill 05 (reviewer)**,
> written from a fresh context seeded with ONLY `04`'s build-handoff + the spec-slice paths. Read-only: a reproducing
> RED test is committed for the testable defect; fixes loop to `04`.

## (a) Verdict

**FIX REQUIRED** — REQ-008 grouping is broken: `assembleDigest` returns only the first member, so multi-member digests
drop everyone else. A reproducing RED test is committed at `test/review/req-008-grouping.test.js`.

## (b) Verification Ledger

**Executed 2 · Observed 0 · Inferred 1 / Total 3.**

| # | Behavior (Done When / VC row) | → REQ | State | Evidence | Result |
|---|-------------------------------|-------|-------|----------|--------|
| 1 | a second standup for the same member+day replaces the first | REQ-001 | EXECUTED | test/digest.test.js:8 → PASS | PASS |
| 2 | each member grouped under their display name | REQ-008 | INFERRED | build test covers only a single member; multi-member path unverified → RED test written | FAIL |
| 3 | needs-help blockers collected at the top | REQ-009 | EXECUTED | test/digest.test.js:24 → PASS | PASS |

## (c) Traceability

| REQ | Priority | Outcome-Gherkin (the frozen "Then") | Covering test (file:line) | Result | Coverage |
|-----|----------|-------------------------------------|---------------------------|--------|----------|
| REQ-001 | MUST | the day still holds exactly one standup for that member | test/digest.test.js:8 | PASS | FULL |
| REQ-008 | MUST | each member's entry grouped under their display name | test/review/req-008-grouping.test.js | FAIL | PARTIAL |
| REQ-009 | SHOULD | all flagged blockers appear together in a top section | test/digest.test.js:24 | PASS | FULL |

## (d) Findings

| # | Severity | REQ / VC | Location (file:line) | Finding | Route | Evidence / RED test |
|---|----------|----------|----------------------|---------|-------|---------------------|
| 1 | high | REQ-008 / VC-02 | src/digest.js:18 | `assembleDigest` groups only `dayEntries[0]`; every other member is dropped — violates "each member's entry grouped under their display name" | code → 04 | `test/review/req-008-grouping.test.js` → RED (asserts all three members group; fails against the defective impl) |

## (e) Capability Probe

| Capability | Command attempted | Exit code | Output excerpt |
|------------|-------------------|-----------|----------------|
| Unit runner | `node --test` | non-zero | reviewer RED test fails: expected `['ada','grace','linus']`, got `['ada']` |
| Oracle re-run @ final_commit | `node --test test/digest.test.js` | 0 | build's own suite green (shallow — single-member only) |
| Browser (Playwright MCP) | — n/a: headless core, no web container | n/a | no UI this sprint |

## (f) Context attestation (the isolation proof)

- **inputs:** `[build-handoff, spec slice]` · **build conversation: not provided**.
- **baseline_commit reviewed:** the defective build's commit — resolves in the repo.
- **spec_slice_hash:** match — recomputed over `sprint-01.md` and compared to the handoff.
- **opened files ⊆ seed:** the handoff, `sprint-01.md`, `digest-assembly.md`, `src/**` at final_commit — nothing from the build session.

## (g) Next command

**FIX REQUIRED** → `/04-builder sprint 01` — the fix pass reads this report's findings + the committed RED test, drives
each to green (never editing a reviewer-authored test), and re-emits the handoff for a **fresh** 05 re-review.

```
QA — SPRINT 01 — FIX REQUIRED
Verification: Executed 2 · Observed 0 · Inferred 1 / Total 3
Findings: high 1 · medium 0 · low 0    spec_slice_hash: match
Isolation: inputs [handoff, spec slice]; build conversation not provided
Unverified: REQ-008 multi-member grouping — build test covered only one member; reproducing RED test committed.
Report: docs/quality/qa-report-sprint-01.md   Next: /04-builder sprint 01
```
