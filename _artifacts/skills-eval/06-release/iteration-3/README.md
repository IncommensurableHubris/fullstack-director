# 06-release · iteration-3 — Phase-4-exit live verification (WS4 D3/D5/D7 + WS5 5.4a)

> iterations 1–2 are prior-phase records (iteration-2 also holds the WS3 3.8 `val-3.8` validation set); this
> Phase-4-exit run gets its own iteration.

**Purpose.** iteration-1 validated 06's gate + auditable-record contract (38/38 with_skill across three cases)
*before* the WS4/WS5 additions. This run re-executes the `clean-release` case as a **composed with_skill live run**
to confirm the new grader assertions hold on **real Sonnet output**:
- `grade_operations` (WS4 D3) — deployment-config `## Operations` with the one SLO on the critical journey;
- `grade_provenance` (WS4 D5+D7) — the `## Provenance` block: artifact digest · built-from commit · a real 64-hex
  `spine_hash` (computed by `verify-spine.py --hash` over `docs/spec/**`) · `amendments_at_release`;
- `grade_security_md` (WS5 5.4a) — `SECURITY.md` present at the root + the G7 row names it (the CVD floor);
- `grade_g10` (WS4 D4) — the conditional migration gate, recorded **N/A** here (no migration).

**Method.** One **with_skill arm** (Sonnet, general-purpose — 06 is sequential and spawns no subagents) loaded
`.agents/skills/06-release/SKILL.md` by path and ran `06-release sprint 1` with the single deploy approval
pre-granted. It gated G1–G10 on recorded machine state, SETUP `deployment-config.md` (incl. `## Operations`),
executed the repo-local stand-in deploy (`node scripts/deploy.js` → `_deploy/live/`), verified health→smoke, wrote
the release report with the `## Provenance` block, and tagged `release/sprint-01`. The 00-discovery
`verify-spine.py` was seeded into the fixture's `scripts/` so the arm could compute a real `spine_hash`.

> **Note on the run:** the arm's driver hit an API connection drop on its *final summary message* — after every tool
> call had already landed (all release artifacts + the annotated tag were on disk). The grade is over the completed
> on-disk state, verified independently; it is not a partial run.

**Result — 18/18** (`check_release.py --case clean-release`). All new assertions PASS: Operations (D3), Provenance
(D5+D7, a real 64-hex `spine_hash`), G7/SECURITY.md (5.4a), G10 N/A (D4) — alongside RELEASED status, an executed
`_deploy/live/`, captured deploy-log/health/smoke evidence, code-identity `match`, the non-amender property,
no-secret-value, REQ-keyed notes, and the `release/sprint-01` tag.

**Provenance.** Workspace `clean/with_skill/outputs/` (gitignored; `grading.json` at root). Orchestrator Opus 4.8;
arm Sonnet. Grade: `python .agents/skills/06-release/evals/check_release.py --outputs
_artifacts/skills-eval/06-release/iteration-3/clean/with_skill/outputs --case clean-release`.
