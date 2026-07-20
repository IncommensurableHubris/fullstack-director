<!-- Filename: _artifacts/exports/build-handoff-patch-001.md  (ephemeral; the reviewer's sole seed). -->
<!-- Placeholders {{...}} are filled by build_fixture.py with the real commit SHAs + recomputed hashes.
     PATCH funnel: spec_slice_path/hash bind the PATCH RECORD; the VC carry-forward is scoped to the owning REQ. -->

---
baseline_commit: {{baseline_commit}}
final_commit:    {{final_commit}}
spec_slice_path: docs/planning/patches/patch-001.md
spec_slice_hash: {{spec_slice_hash}}
review_mode:     patch
patch:           patch-001
---

# Build Handoff — patch-001

> The reviewer's sole seed, patch funnel: this record + the owning REQ's blocks bound the scope. The fix: standups
> submitted exactly at the lock minute are now included in the digest (REQ-008 boundary). TDD-for-bugs: the
> reproducing regression test was observed RED against the pre-patch impl, green after the one-comparison fix.

## (a) File List

| Path | Change | Notes |
|------|--------|-------|
| src/digest.js | modified | inclusive lock-boundary comparison (the fix; ~1 LOC) |
| test/patch-001-lock-boundary.test.js | added | the reproducing regression test (observed RED pre-fix) |

## (b) Verification-Contract carry-forward (scoped to the owning REQ)

| VC-ID | → REQ | Method | Assertion | Pass-criterion | Evidence state | Repro command | RED-note | Oracle hash | Non-EXECUTED reason |
|-------|-------|--------|-----------|----------------|----------------|---------------|----------|-------------|----------------------|
| VC-02 | REQ-008 | unit | each member's entry grouped under their display name | every member appears once, grouped | EXECUTED | `node --test test/digest.test.js` | re-run green post-fix (no regression) | {{oracle_hash}} | — |
| VC-P01 | REQ-008 | unit | a standup submitted exactly at the lock minute is included in that day's digest | the at-lock member appears in the digest | EXECUTED | `node --test test/patch-001-lock-boundary.test.js` | observed RED pre-fix: the at-lock member was missing | {{patch_oracle_hash}} | — |

## (c) REQ → test coverage map (owning REQs only — the patch's bounded scope)

| REQ | Covered by (test file:line) | Coverage |
|-----|-----------------------------|----------|
| REQ-008 | test/patch-001-lock-boundary.test.js:9 | FULL |

## (d) Attestations & log

- **Spine untouched:** the diff writes `src/digest.js`, the regression test, and the backlog's `## Patches` status
  cell (`planned → in-progress`) only; no `docs/spec/**`, `docs/architecture/**`, or `docs/design/**` file edited.
- **Budget:** within the certified size budget (3 files / 60 LOC): 2 source files, ~18 added LOC.
- **Deviations & surfaced drift:** none — the fix stayed inside REQ-008's existing acceptance.
- **HALT / blocked record:** none.
- **Dependency provenance + SBOM:** zero dependencies added (zero-dep stack).
- **Environment / repro facts:** `node --test`, Node 22.x; offline, deterministic. Headless core — no browser VC.
