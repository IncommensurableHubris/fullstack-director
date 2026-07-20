# 03-architect iteration-2 — WS3 Task 3.5a (agentic ADR categories + eval-suite oracle)

Live A/B (skill-creator method, native subagents on **Sonnet**; orchestrator on Opus). Each arm given the seeded
`beacon-agent` spine (a multi-agent research system, `Profile: agent-system`) + the sprint-01 slice. Graded by
`check_architecture.py --case agent`. Workspaces gitignored; this README is the record. **3.5b (mcp-server transport/
auth ADR + the four MCP VC checks) is RESERVED — not built.**

## Fixture

`evals/fixtures/beacon-agent/` — Beacon fans out parallel workers across 10–30 independent sources and synthesizes a
grounded report. REQ-001 (concurrent independent-source coverage) genuinely **forces a multi-agent topology**;
REQ-002 (synthesis quality) is **distributional** and carries an `**Acceptance (eval-suite):**` block →
`docs/spec/evals/research/synthesis.jsonl`; REQ-003 is a must-not. Verify-PASS (L6 resolves the dataset).

## Results

| Arm | Grade | What it demonstrates |
|-----|:-----:|----------------------|
| with_skill | **7/7** | 7 `Category:`-tagged ADRs (topology · model-binding · memory · isolation · durability · observability · classic); **ADR-002 (topology) carries the ~15× token-economics justification** — the ≈15× multi-agent multiplier weighed against parallel breadth, then bounded (model-tiering, capped fan-out, and a prompt-cache warm-up detail); **REQ-002 gets an `eval-suite` VC row** (harness cmd · `synthesis.jsonl` dataset · floor 80%); the headless-slice STOP resolves to DM-coverage N/A; Reconcile Pass-1 inline, 0 amendments (agnostic envelope) |
| baseline | **2/7** | a **strong** architecture — it *did* reason about the orchestrator-worker topology, cost governance, and an eval harness — but wrote ADRs at `docs/architecture/decisions/` and specs at `docs/architecture/features/` (non-canonical), with no `Category:` lines and no `eval-suite` method keyword. Only *system.md exists* + *amendment-log valid* pass |

Honest read (`feedback_framework_skill_lift_is_structural` + `_grader_validate_on_real_outputs`): the baseline's
*substance* is real (it knows how to architect a multi-agent system and even named the topology tradeoff), so the lift
is **not** raw insight — it is the **governed, machine-consumable contract**: the canonical `adr/` + `specs/` layout,
the `Category:` taxonomy, the mandatory ~15× topology justification, and the `eval-suite` oracle keyword that 04/05
mechanically consume. Sonnet-with-skill at 7/7 is the honest portability claim.

## Grader-validation (grader-first) + the robustness fix the live run surfaced

Hand-ideal architecture over the seed (`val-3.5a/ideal/`: ADR-002 `Category: topology` + the ~15× justification, a
feature spec with an `eval-suite` VC row) → **7/7**. Two degenerates each fire exactly their target:
- **no-economics** (strip the multiplier justification from the topology ADR) → *topology ADR carries the ~15×
  justification* fails — after tightening `ECON` to require the **multiplier** signal (15× / N-fold / N× tokens /
  order-of-magnitude / "token economics"), not a loose "token spend is bounded";
- **no-eval** (change the `eval-suite` VC row's method to `unit`) → *eval-suite VC row* fails.

**The live with_skill arm surfaced a real grader bug:** the topology-ADR detector broke on the *first* ADR mentioning
"orchestrat", and the arm's ADR-001 (tech-stack, `Category: classic`) names the orchestrator in passing — so the
grader checked the wrong ADR and scored 6/7. Fixed to **prefer the ADR whose `Category:` is `topology`** (falling back
to a topology/orchestration *title* only if none declares the category); re-validated the whole set (ideal + both
degenerates) and re-graded the real arm to 7/7. The `feedback_grader_validate_on_real_outputs` loop, exactly.

## Also fixed here (verify-spine `L6`/`W5` robustness, Task 3.3 code)

Building this fixture exposed that verify-spine's `"evals" not in p.parts` filter (meant to exclude `docs/spec/evals/**`
datasets from L6's ref-scan + W5's density) matched **"evals" anywhere in the absolute path** — so a spine nested under
an `.../evals/fixtures/...` ancestor (or any repo under an `/evals/` dir) had its whole spine skipped. Scoped the
filter to `p.relative_to(spec_dir).parts` (only `docs/spec/evals/**`). `validate_script.py` stays ALL GOOD
(temp-dir staging has no `evals` ancestor — behavior-preserving).
