# 07-security · iteration-3 · proof-of-fix-h2 — WS5 5.2 (H2) live A/B

**Purpose.** The genuinely-new proof-of-fix behavior: a REMEDIATE security finding closes at **re-audit** only with a
failing→passing regression test that **bites on revert**. Task-level live A/B (with_skill vs baseline) over a
re-audit scenario, graded by `grade_proof_of_fix` (`check_security.py`).

**Fixture (authored for this run).** From `build_fixture.py --case vuln` (the 5-plant HTTP surface): `/04` fixed
**one** finding — the A03 reflected-XSS on `/search` (`src/server.js` now HTML-escapes the reflected input) — and
shipped a **biting regression test** at `test/xss-regression.test.js`; a **prior REMEDIATE audit**
(`docs/security/security-audit-sprint-02.md`) had flagged all five findings routed to `/04`. Fix + test + prior
report are committed (`FIX_SHA eb15063`; parent `73c3f5f` = the vulnerable version). **Fixture soundness
self-verified before the run**: the test is green at HEAD and goes **red when the fix is reverted**
(`git show HEAD~1:src/server.js`), then restores clean. Both arms cloned from the identical prep.

**A/B result — grade_proof_of_fix (the H2 discriminator):**

| Arm | grade_proof_of_fix | What it did |
|---|:---:|---|
| **with_skill** | ✅ **PASS** (overall **20/20**) | Re-audited and **mechanically executed** the bite-on-revert: `node --test test/xss-regression.test.js` green at HEAD → `git show HEAD~1:src/server.js` → **red** (the exact `AssertionError`) → restored → green. Closed the XSS **with the captured proof**; kept the other four Highs open. READ-ONLY held (`git diff HEAD -- src` empty after the revert cycle). |
| **baseline** | ❌ **FAIL** | Correctly saw the XSS was fixed and marked it **CLOSED** on "`npm test` (3/3) passes" + a live probe — but **never reverted** to prove the test *guards* the fix. An unproven close. |

**The lift.** Both arms reach the correct "XSS is fixed" conclusion; only the with_skill arm *proves* the close with a
biting-on-revert regression test. The baseline rubber-stamps the close on "the test passes" — which does not prove
the test would catch a regression.

**Grader-robustness fix this A/B validated end-to-end (`grade_proof_of_fix`).** The vuln composed run
(`iteration-3/vuln`) first surfaced that the N/A gate mis-fired on an *initial* audit that merely mentions
"re-audit"/"proof_of_fix" (routing, or a conscientious "no prior REMEDIATE" addendum). The gate now keys on an
**asserted close-status** (a `| closed |` status cell / a `status: closed` field, tolerant of markdown decoration
like `**CLOSED**`) — proof is owed only when a prior finding is actually closed. Validated across four hand-built
reports (N/A for initial-audit + kept-open; PASS for a proven close; FAIL for an unproven close — this baseline).
The discriminator (a biting-revert test is required to close) is untouched — the fix corrects only the applicability
gate.

**Provenance.** Workspaces `overlay-a/{with_skill,baseline}/outputs/` (gitignored; `grading.json` at each root).
Orchestrator Opus 4.8; both arms Sonnet. Grade: `python .agents/skills/07-security/evals/check_security.py --outputs
<arm>/outputs --case vuln`.
