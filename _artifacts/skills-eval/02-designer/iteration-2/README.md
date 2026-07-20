# 02-designer iteration-2 — WS3 Task 3.4 (agent-experience mode: tool surface as the UX)

Live A/B (skill-creator method, native subagents on **Sonnet** — the Phase-3 executor-arm model; orchestrator on
Opus). Each arm given the seeded `relay-agent` spine (a `Profile: agent-system` project with an `agent-contract.md`)
and the sprint-01 slice. Graded by `check_design.py --case agent`. Workspaces gitignored; this README is the record.

## Fixture

`evals/fixtures/relay-agent/` — the Relay support-triage agent as a **seeded spine** (specification with
`Profile: agent-system`, `capabilities/triage.md`, `design-intent.md` carrying the agent's **voice/persona**,
`architecture-constraints.md`, `agent-contract.md` with a 5-tool permission matrix, and a sprint-01 slice). 02 runs
over it and ADDS `docs/design/`.

## Results

| Arm | Grade | What it demonstrates |
|-----|:-----:|----------------------|
| with_skill | **7/7** | agent-experience design (not screens): all 5 agent-contract tools named + described, turn design, persona realized from design-intent, refusal-UX per must-not REQ, the refund **HITL touchpoint** designed first; a **12-row DM-NNN manifest** with rows pointing at tools/turns/refusals; 2 Tier-2 Reconcile amendment rows (AI-disclosure gap; a REQ-001-vs-escalation tension) |
| baseline | **6/7** | a **strong** Sonnet designer produced a genuinely good Zendesk-sidebar UI — it referenced the tools, realized the voice, designed refusal + refund-approval UX (even cited EU AI Act Art. 50 disclosure) — but produced **no `DM-NNN` manifest** (README/flows/surfaces docs instead). The single discriminating miss is the **coverage contract** 03/04/05 mechanically consume |

The margin is one point, and that is the honest story (`feedback_framework_skill_lift_is_structural`): a capable
baseline covers the *craft* (tools, persona, refusal, HITL) because a good designer does — the framework's structural
lift is the **`DM-NNN` coverage contract** (+ the amendment-protocol rows), the machine-consumable artifact the
downstream seats depend on, which the baseline did not produce. Sonnet-with-skill at 7/7 is the honest portability
claim.

## Grader-validation (grader-first, before the live run)

Hand-ideal agent-experience design over the seed (`val-3.4/ideal/` — a tool-surface doc naming all five tools + a
DM-manifest whose rows point at tools/turns) → **7/7**. Two degenerates each fire **exactly** their target:
- **no-tools** (a structurally-complete but generic design that names none of the agent-contract's tools) → *Tool
  surface covered* fails (the core discriminator);
- **no-manifest** (drop the `approved/sprint-01/manifest.md`) → *DM-ID manifest present* fails.

Then the **real** arms were re-graded (with_skill 7/7, baseline 6/7) — not just the hand-ideal — closing the
`feedback_grader_validate_on_real_outputs` loop; the baseline's substance (tools, persona, refusal, HITL all PASS) is
credited, so the lift is not overstated.
