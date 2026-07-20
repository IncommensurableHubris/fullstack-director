<!-- Filename: _artifacts/exports/build-handoff-sprint-NN.md  (ephemeral, gitignored; the reviewer's sole seed).
     Patch funnel: _artifacts/exports/build-handoff-patch-NNN.md — review_mode: patch, plus the `patch:` line, and
     spec_slice_path/hash bind the PATCH RECORD (docs/planning/patches/patch-NNN.md) instead of the sprint file. -->

---
baseline_commit: <git SHA at build-start, BEFORE any edit — `git rev-parse HEAD`>
final_commit:    <git SHA after the last build commit>
spec_slice_path: docs/planning/sprints/sprint-NN.md
spec_slice_hash: <sha256:16hex — binds the built-against spec slice; 05 recomputes + compares (mismatch → BLOCK). See references/build-handoff.md>
review_mode:     full
<!-- review_mode: full (sprint) | patch. On a patch add:  patch: patch-NNN  — and delete this comment. -->
---

# Build Handoff — Sprint NN

> **The reviewer's sole seed.** Owned by **skill 04 (builder)**, consumed by **skill 05 (reviewer)** in a fresh
> context. Its only job: let a cold reviewer **reconstruct the diff (`baseline_commit..final_commit`), re-run the
> oracles, and check REQ coverage** with no access to the build session. **Evidence, never narrative** — no build
> conversation, no rejected approaches. Every claim is backed by a command that exits 0 or an honest INFERRED.
> Craft + the why of each field: `references/build-handoff.md`.

## (a) File List

> Every path new/modified/deleted in this slice, repo-root-relative. Must equal `git diff --name-status
> baseline_commit..final_commit`. **HALT completion if incomplete** — an incomplete map silently narrows the review.

| Path | Change | Notes |
|------|--------|-------|
| _<src/domain/digest.js>_ | _<added>_ | _<pure digest assembly>_ |
| _<test/digest.test.js>_ | _<added>_ | _<unit oracle for VC-01/VC-02>_ |

## (b) Verification-Contract carry-forward

> Every VC row from `03`'s feature specs, carried forward and stamped with the builder's **evidence state**
> (`05`'s exact vocabulary — consumed 1:1). **EXECUTED** = a test ran green and clears the anti-tautology gate
> (attach `test:line → PASS`, the repro command, and the RED-phase note). **OBSERVED** = you drove the real system
> and watched it (attach the transcript). **INFERRED** = read-and-argued, **no execution** = **NOT verified** —
> every INFERRED row cites *why* it couldn't run (a path/contract, not "standard patterns") **and** its Unknown.
> These INFERRED rows are exactly where `05` starts.
>
> **Verify-live rows (WS6).** A VC row exercising a spine-declared **verify-live** tech carries a **`verified:
> docs/verification/<tech>.md`** token beside its evidence state (put it in the reason/notes cell). It must be
> **EXECUTED/OBSERVED, never `INFERRED`** — citing a live-source record while claiming you couldn't verify the shape
> is contradictory; an `INFERRED` verify-live claim is a finding (`06` G11 blocks it). See
> `shared/live-source-verification.md`.

| VC-ID | → REQ | Method | Assertion (loosest claim that catches a break) | Pass-criterion (boolean) | Evidence state | Repro command | RED-note | Oracle hash | Non-EXECUTED reason + Unknown |
|-------|-------|--------|-----------------------------------------------|--------------------------|----------------|---------------|----------|-------------|-------------------------------|
| _<VC-01>_ | _<REQ-008>_ | _<unit>_ | _<assembleDigest groups each member's entry under their display name>_ | _<grouping equals expected>_ | _<EXECUTED>_ | _<`node --test test/digest.test.js`>_ | _<observed red before impl: assertion on grouping failed>_ | _<sha256:12hex>_ | _<— (n/a; EXECUTED)>_ |
| _<VC-02>_ | _<REQ-009>_ | _<unit>_ | _<needs-help blockers appear together in the top section>_ | _<top section lists all flagged blockers>_ | _<EXECUTED>_ | _<`node --test test/digest.test.js`>_ | _<observed red before impl>_ | _<sha256:12hex>_ | _<—>_ |
| _<VC-0N>_ | _<REQ-0NN>_ | _<browser>_ | _<the digest renders with needs-help visually pinned above the fold>_ | _<needs-help region above member sections in the DOM>_ | _<INFERRED>_ | _<— (no runtime)>_ | _<—>_ | _<—>_ | _<reason: no browser runtime in this headless Node slice (`system.md` §5: no web container this sprint). Unknown: visual pin-to-top unverified; `05` must escalate via browser verification.>_ |

<!-- One row per VC across all feature specs. A row you cannot honestly mark EXECUTED/OBSERVED is INFERRED — never
     dropped (hides a requirement) and never fake-passed (lies to the reviewer).
     eval-suite row (Profile: agent-system): the oracle is the eval harness over the in-spine dataset. Its RED-note
     is the failing eval CASE observed before the fix; and it carries a grader-bites line proving the grader is not
     tautological — e.g. "grader bites: degenerate '' scored 0 < floor -> FAIL, as required." A row EXECUTED without a
     grader-bites attestation is not trustworthy (05 re-runs the bite). See references/build-discipline.md. -->

## (c) REQ → test coverage map

> Every **in-scope** REQ (from `spec_slice_path`) → the test that covers it → **FULL / PARTIAL / NONE**. A PARTIAL or
> NONE is a first-class, declared output — not a gap to be discovered.

| REQ | Covered by (test file:line) | Coverage |
|-----|-----------------------------|----------|
| _<REQ-008>_ | _<test/digest.test.js:12>_ | _<FULL>_ |
| _<REQ-009>_ | _<test/digest.test.js:34>_ | _<PARTIAL — happy path only; empty-blocker case deferred to 05>_ |

### DM-ID → implementation map  _(if a `02` design contract exists; else "N/A — headless slice")_

> Forward direction: every manifest `DM-NNN` this slice implements → the code that realizes it. A DM-ID with no
> implementation location is an incomplete build.

| DM-ID | Element (from manifest) | Implemented at (file:line) |
|-------|-------------------------|----------------------------|
| _<DM-007>_ | _<digest header with the date>_ | _<src/domain/render.js:8>_ |

## (d) Attestations & log

- **Spine untouched:** _<the diff writes only `src/**` + this handoff (+ optional Dockerfile/sbom); no `docs/spec/**`,
  no `docs/architecture/**`, no `docs/design/**` was edited>._
- **Deviations & surfaced drift (three-way verdict):** _<where the build diverged from the spec, and each drift
  classified — **code** (fixed) / **test** (fixed) / **spec → escalated to `03`** / **declaration → pending
  amendment for `00`/`05`**). 04 escalates, never amends. "none" if the realization built cleanly.>_
- **HALT / blocked record:** _<every HALT with its reason (`06-release` blocks on these), or "none">._
- **Dependency provenance + SBOM:** _<allow-list/pin/audit result, or "zero dependencies added"; `sbom.json` path or
  "n/a — zero-dep stack">._
- **Environment / repro facts:** _<runner + version (e.g. `node --test`, Node 22.x); the exact test command;
  seeds/fixtures — so `05` reproduces the EXECUTED state on the first try>._

<!-- The honesty test: a reviewer with ONLY this file + the repo at final_commit must be able to rebuild the diff,
     re-run each EXECUTED command to exit 0, find each INFERRED row's cited reason, and read REQ/DM coverage — without
     opening the build conversation. If any is untrue from the file alone, the handoff is not done. -->
