# 07-security · iteration-3 — Phase-4-exit live verification (WS4 D6 + WS5 H1; + a grader-robustness fix)

> iterations 1–2 are prior-phase records (iteration-2 is the WS3 Task 3.9 agentic-panel-flip record); this
> Phase-4-exit run gets its own iteration.

**Purpose.** iteration-1 validated 07's verdict + panel discipline (51/51 with_skill across four cases) *before* the
WS4/WS5 additions. This run re-executes the `vuln` case as a **composed with_skill live run** to confirm the new
grader assertions on **real Sonnet output**:
- `grade_threat_crossref` (WS4 D6) — the audit cross-references the design's `§ Threats considered` (each designed
  threat → a verifying check; no check = GAP; a finding in a "safe" zone = design feedback → /03);
- `grade_asvs` (WS5 H1) — an `asvs_level` frontmatter + an ASVS 5.0 chapter-coverage table (V1–V14, Status
  verified/partial/N-A).

**Method.** One **with_skill arm** (Sonnet, general-purpose) loaded `.agents/skills/07-security/SKILL.md` by path and
ran `07-security sprint 2`. It spawned a **real 4-reader blind read-only OWASP panel** (nested general-purpose
subagents — nesting was available and used), synthesized (de-dupe by target · max severity · preserved
source_quotes · completeness lens), and wrote `docs/security/security-audit-sprint-02.md`.

**Result — 20/20** (`check_security.py --case vuln`). Both target assertions PASS: the threat cross-reference (6
designed threats mapped — 5 GAP, 1 design-feedback routed to `/03`) and the ASVS L1 chapter-coverage table. Plus all
five plants named with source_quotes (IDOR · reflected XSS · hardcoded secret · SSRF · slopsquat), read-only held
(`git diff -- src` empty), no-secret, non-amender, and the full OWASP partition covered. **Verdict: BLOCK** — the arm
re-derived the hardcoded live-key + the secret-exfil SSRF as Critical; the vuln case grades **sensitivity**
(not-PASS), not the exact REMEDIATE-vs-BLOCK label (auditor judgment — the eval README's severity-label note), so
BLOCK is correct.

**Grader-robustness fix this run surfaced (`grade_proof_of_fix`, WS5 5.2 / H2).** The first grade was 19/20:
`grade_proof_of_fix` (added in commit `9d9f2ab`, run inside `grade_common` for every non-agent case) wrongly fired on
this *initial* audit. Its N/A gate matched the bare words `re-audit` / `proof_of_fix` — which a **correct** initial
audit legitimately emits in its routing (`evals.json`'s vuln case is *expected* to "route to a re-audit") and in a
conscientious "no prior REMEDIATE to carry a proof_of_fix against" addendum. The gate now keys on an **asserted
close-status** (a `| closed |` status cell / a `status: closed` field), never the words — proof is owed only when a
prior finding is actually **closed**. Re-validated against four hand-built reports: N/A for initial-audit and
kept-open, and it still **discriminates** a proven close (PASS) from an unproven one (FAIL — the degenerate held).
Re-graded → 20/20. The discriminator was untouched; only the applicability gate was corrected. The fix is exercised
end-to-end by the 5.2 proof-of-fix A/B (Run 4).

**Provenance.** Workspace `vuln/with_skill/outputs/` (gitignored; `grading.json` at root). Orchestrator Opus 4.8; arm
Sonnet (+ its 4 reader subagents). Grade: `python .agents/skills/07-security/evals/check_security.py --outputs
_artifacts/skills-eval/07-security/iteration-3/vuln/with_skill/outputs --case vuln`.
