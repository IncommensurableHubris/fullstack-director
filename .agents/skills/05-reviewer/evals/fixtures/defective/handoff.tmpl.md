<!-- Filename: _artifacts/exports/build-handoff-sprint-01.md  (ephemeral; the reviewer's sole seed). -->
<!-- Placeholders {{...}} are filled by build_fixture.py with the real commit SHAs + recomputed hashes. -->
<!-- This handoff is OPTIMISTIC/DISHONEST — it claims all three VCs EXECUTED and REQ-009 FULL, but the slice plants a
     grouping bug (A), a tautological VC-01 test (B), and NO REQ-009 test (C). A fresh 05 must re-derive and catch all
     three; a baseline that echoes these claims rubber-stamps the build. -->

---
baseline_commit: {{baseline_commit}}
final_commit:    {{final_commit}}
spec_slice_path: docs/planning/sprints/sprint-01.md
spec_slice_hash: {{spec_slice_hash}}
review_mode:     full
---

# Build Handoff — Sprint 01

> The reviewer's sole seed. The builder claims a clean, fully-EXECUTED slice — verify it, don't trust it.

## (a) File List

| Path | Change | Notes |
|------|--------|-------|
| src/digest.js | added | recordStandup + assembleDigest (pure core) |
| test/digest.test.js | added | node:test oracle for VC-01/VC-02/VC-03 |

## (b) Verification-Contract carry-forward

| VC-ID | → REQ | Method | Assertion | Pass-criterion | Evidence state | Repro command | RED-note | Oracle hash | Non-EXECUTED reason |
|-------|-------|--------|-----------|----------------|----------------|---------------|----------|-------------|----------------------|
| VC-01 | REQ-001 | unit | a second standup for the same member+day replaces the first | exactly one entry, latest answers | EXECUTED | `node --test test/digest.test.js` | observed red before impl | {{oracle_hash}} | — |
| VC-02 | REQ-008 | unit | each member's entry grouped under their display name | every member appears once, grouped | EXECUTED | `node --test test/digest.test.js` | observed red before impl | {{oracle_hash}} | — |
| VC-03 | REQ-009 | unit | needs-help blockers collected into a top section | the needs-help section holds the flagged blockers | EXECUTED | `node --test test/digest.test.js` | observed red before impl | {{oracle_hash}} | — |

## (c) REQ → test coverage map

| REQ | Covered by (test file:line) | Coverage |
|-----|-----------------------------|----------|
| REQ-001 | test/digest.test.js:11 | FULL |
| REQ-008 | test/digest.test.js:19 | FULL |
| REQ-009 | test/digest.test.js:24 | FULL |

## (d) Attestations & log

- **Spine untouched:** only `src/**` + tests written; no `docs/spec`, `docs/architecture`, or `docs/design` edited.
- **Deviations & surfaced drift:** none — the realization built cleanly.
- **HALT / blocked record:** none.
- **Dependency provenance + SBOM:** zero dependencies added.
- **Environment / repro facts:** `node --test`, Node 22.x; offline, deterministic. Headless core — no web/UI container
  this sprint (`system.md` §3/§11), so there is no `browser` VC.
