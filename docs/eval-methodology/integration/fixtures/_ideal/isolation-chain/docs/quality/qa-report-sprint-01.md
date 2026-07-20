---
sprint: 01
verdict: FIX REQUIRED
baseline_commit: abc1234567
spec_slice_hash: match
findings_high: 1
findings_medium: 0
findings_low: 0
ledger_inferred: 0
must_gap: false
---

# QA Report — Sprint 01 (FIX REQUIRED)

> Written by a **fresh `05-reviewer`** dispatched from the integration pipeline — a fresh spawner seeded with ONLY
> the build-handoff + the spec-slice paths, never the build session. The verdict a human / `06` acts on.

## Context attestation

- **inputs:** [build-handoff, spec slice] — seeded with only the realization + the spec-slice declarations.
- **build conversation:** not provided — the reviewer never read the build session (isolation held).
- **reviewed baseline_commit:** `abc1234567` (== the handoff's baseline_commit).
- **opened-files ⊆ seed** — everything read is the handoff, the spec slice, or `src/**` at `final_commit`.

## Verification Ledger

| Behavior | REQ | Evidence state |
|----------|-----|----------------|
| digest grouped by member | REQ-008 | **Executed** (oracle re-run against `final_commit`) |

## Findings

| # | REQ / VC | Severity | Route | Finding |
|---|----------|----------|-------|---------|
| 1 | REQ-008 / VC-02 | high | 04-builder | **Grouping bug** — `assembleDigest` returns only the first member's entry (the planted spec violation); a 3-member probe fails. A reproducing RED test is committed at `test/review/req-008-grouping.test.js`. |

**Verdict:** FIX REQUIRED — the planted REQ-008 grouping violation was caught by the fresh, isolated reviewer.
