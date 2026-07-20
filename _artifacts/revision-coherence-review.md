# Revision Coherence Review — WS1–WS4 composed over the base framework

> Pre-implementation check (user-requested, 2026-07-06): do the four approved
> revision designs + the existing ten seats compose into ONE coherent, effective
> SDLC for both software and agentic-AI engineering? Security-seat depth assessed
> separately (§ Security, appended after targeted research).

## Verdict

**Coherent — with eight seams found, one requiring a design decision (S1), seven
resolvable at implementation-plan level.** No contradictions between the four
designs; every new artifact has exactly one home; every new gate reads recorded
machine state; all five framework doctrines survive intact (declaration/realization
· amendments-controlled · isolation-from-fresh-spawners · one-home-per-fact ·
evidence-honesty), and the revisions add two new doctrine lines that compose
cleanly ("ceremony scales down, verification never does" · "structural defenses,
not predictive ones").

## The composed lifecycle (agent-system project, end to end)

explore (divergent, spine-locked) → intake/interview or adopt (brownfield, all
REQs code-sourced `derived`) → spine {profile · Constitution · EARS REQs incl.
must-not · agent-contract · quantified NFRs · eval datasets} + verify-spine.py
emitted → 01 decompose (walking skeleton = agent loop + tracing + eval harness) →
02 agent-experience (tool surface, interaction manifest) → 03 (system.md incl.
threats-considered + test strategy + fitness-function'd quality scenarios; ADRs
incl. topology-with-economics; feature specs with eval-suite/migration/
observability VC rows) → 04 (eval-first RED, grader-bites, TDD) → 05 (isolated;
floors verified at final_commit; llm-review mandatory; fitness functions re-run) →
06 (G1–G10 fail-closed; SBOM+provenance; spine_hash; Operations section) → 07
(ASI-primary flipped panel; designed-threats cross-reference) → 08 (unchanged) —
with `status` profile-aware throughout, the patch lane for small fixes, and the
verify script standing guard between all runs. Webapp projects run the same chain
with the classic toggles. Every seat's output feeds a named consumer; no orphan
artifacts found.

## Seams found (S1 = design decision; S2–S8 = implementation-plan notes)

**S1 — patch lane × in-spine eval datasets (the regression-case seam).** WS1's P2
says a patch leaves `docs/spec/**` byte-untouched; WS3 puts eval datasets inside
`docs/spec/evals/`. But the Husain discipline says a fixed bug on a distributional
behavior SHOULD add a regression eval case — which under strict P2 forces every
such fix out of the patch lane. **Resolution (approved 2026-07-06): the
additive-case exception** — a patch MAY add (never edit/delete) eval cases under
`docs/spec/evals/**`, accompanied by a mechanically-written Tier-1 amendment row
(`skill: 01-planner`, additive-regression-case class). Mechanically checkable
(diff = additions only within evals/ + exactly one new T1 row), preserves the
audit trail, and keeps behavioral-spec *changes* (edits) on the normal road.
Folded into WS1 (P2 refinement) + WS3 (Section C note).

**S2 — the verify script is extended by three workstreams; build it as a check
registry.** WS1 ships L1–L5 + schema + markers; WS3 adds profile parsing +
dataset-reference resolution (load-bearing class); WS4 adds `--hash`. Implementation
order: WS1 builds `verify-spine.py` with a check-registry structure so WS3/WS4
register checks instead of patching logic. Dataset-reference resolution is L-class
(FAIL), same family as registry↔leaf.

**S3 — one profile table, three consumers.** `status`'s router (patch-in-flight ×
profile column), 03's Design-Contract STOP (skill-pack expects NO manifest — the
STOP must consult the profile before asking), and 02's skip rule all read the same
per-profile expectations. They must all read `shared/agentic-profile.md`'s ONE
table, never restate it. Router precedence: P1 integrity → patch-in-flight → P2
governance → P3 profile-adjusted earliest-missing → P4 advisories (patch-pressure
advisory lives here).

**S4 — adopt emits the standing gates too.** WS2's ADOPT shares the WRITE SPINE
step; make explicit that verify-spine.py (+ hooks templates) are emitted on the
adopt path exactly as on intake — brownfield projects need the standing guard most.

**S5 — one sentence missing in requirements-authoring:** when acceptance is
outcome-Gherkin vs an eval block vs both — rule: Gherkin wherever a deterministic
user-observable outcome exists; an eval block wherever the behavior is
distributional; both when a behavior has a deterministic shell and a
distributional core (e.g., "always responds within the tool budget" + "answers
correctly ≥90%").

**S6 — field-name contract:** 05's qa-report frontmatter gains `eval_floors_met` /
`evals_run` (WS3); 06's G8 reads them. Template and gate reference must be written
against the same names in the same implementation session (pair them in the plan).

**S7 — AGENTS.md emission gains the profile mirror.** Both emitters (00 at WRITE
SPINE, status at re-emission) must include it; update `templates/agents-view.md`
+ status's generated-views reference together.

**S8 — agent-contract ↔ architecture-constraints boundary line.** Cost envelope,
tool matrix, autonomy, HITL live ONLY in agent-contract; stack/hosting/compliance/
scale stay ONLY in constraints. One boundary sentence in both templates prevents
the smeared-facts failure mode from re-emerging between two spine
files.

## Effectiveness against the original review's findings

- The three structural gaps are closed by construction: ceremony (WS1 patch lane +
  usage bound), brownfield (WS2 adopt — prerequisite for the fork goal), agentic
  profile (WS3, with eval-suite acceptance as the declaration-level bridge).
- DORA amplifier capabilities: small batches (patch lane), strong version control +
  rollback (standing gates + spine_hash), clear AI stance (profile + doctrines) —
  the framework now implements the capability list rather than merely resembling it.
- MAST failure classes (specification + verification dominate): attacked at both
  ends — declarations gated upstream (agent-contract, must-not REQs, eval
  datasets), verification isolated and floor-checked downstream (05/06/07).
- EDDOps continuous loop: 06 becomes a checkpoint-on-a-loop at solo scale
  (G9 tracing + drift note + sampling feeding `00 reflect`) — deliberately lean;
  full online-eval operations remain out of scope by design.

## Residual open items (deliberate, tracked)

1. **Packaging/dev-bridge deferral now binds harder** — WS1–4 add files and modes;
   running under Claude Code still requires explicit path loading until the
   `.claude/skills` bridge / CLI generator lands. Unchanged decision, rising cost;
   revisit after implementation.
2. **Model-migration activity** — reserved spec only (WS3 F), built on first need.
3. **Fifth integration leg** (mini agent-system chain) — decide at implementation
   planning (WS3 eval item 8).
4. **Production observability depth** — one SLO/alert by design; anything more is
   a future profile module.
5. **Multi-human workflows** — explicit non-goal (README).
6. **Security-seat depth** — assessed below.

## Security assessment (07-security beef-up)

**Verdict: more work warranted — three real gaps + six cheap additions, designed
as WS5 (`revision-ws5-design.md`).** Targeted research (OWASP primary sources,
2025–2026) against the seat as it will stand after WS2–4:

1. **The verification-bar gap (structural):** OWASP positions the Top 10 as an
   *awareness* document and **ASVS 5.0 as the verification standard**. 07
   partitions readers by Top-10/ASI — fine for work division — but measures
   completeness against the same awareness artifact. WS5-H1 re-anchors the
   synthesizer's completeness lens on ASVS chapters (CWE-tagged), with a declared
   per-project target level (L1 solo default) and a per-release evidence schema.
2. **Static-only agentic audit is inadequate (consensus, quantified):** initially-
   secure code accumulates +37.6% critical vulns over five AI revision loops;
   OWASP's GenAI Red Teaming Guide and the Q2-2026 landscape both require runtime
   behavior analysis. WS5-H3 adds the dynamic arm: attack corpora as must-not eval
   datasets (reusing WS2 must-nots + WS3 in-spine eval blocks), promptfoo
   `owasp:agentic` as the PR-gateable suite, ASR-thresholded verdict, PASS
   requiring the arm executed (or an explicit recorded waiver).
3. **Unproven remediation:** findings route to /04 but close without proof. WS5-H2
   requires a failing→passing regression test per finding, enforced by the
   re-auditor (proof_of_fix column; the test must bite on revert).
4. **Cheap additions (WS5-H4):** slopcheck + dependency-cooldown policy; mcp-scan
   as the deterministic MCP scanner; SECURITY.md emission + G7 presence check
   (CRA trajectory); one-page IR lines in Operations; optional ZAP-baseline DAST;
   ML-BOM component fields in the release SBOM for agent profiles.
5. **Explicitly skipped as enterprise ceremony:** ASVS L2/L3 defaults, bespoke
   AI-BOM machinery, PSIRT/SLAs/threat-intel/red-team staffing, full DAST gating,
   continuous scanning platforms.

With WS5, the seat verifies against the right standard (ASVS), attacks what it
audits (runtime arm), and closes the loop it opens (proof-of-fix) — while staying
read-only w.r.t. code, panel-partitioned, and solo-operable.
