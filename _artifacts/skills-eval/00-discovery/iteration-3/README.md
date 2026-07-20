# 00-discovery iteration-3 — WS3 Task 3.2 (agentic discovery branch + agent-contract)

Live A/B (skill-creator method, native subagents on **Sonnet** — the Phase-3 executor-arm model; the orchestrator
that designed/validated the grader ran on Opus). Each arm a fresh general-purpose agent given only the workspace root
+ the `agent-brief` fixture. Graded by `check_spine.py --case agent`. Workspaces are gitignored (`_artifacts/**`);
this README is the durable record.

## Fixture

`evals/fixtures/agent-brief/brief.md` — **Relay**, a support-triage agent: reads a support inbox, drafts grounded
replies, can send low-risk replies itself, can issue a Stripe refund **only with human approval**, escalates
abuse/legal/uncertain, remembers prior tickets. Rich enough to elicit all six agent-contract sections, a HITL tool,
and ≥1 must-not; the latency ask ("under a minute") tests the S8 boundary (→ architecture-constraints, not the cost
envelope).

## Results

| Arm | Grade | What it demonstrates |
|-----|:-----:|----------------------|
| with_skill | **15/15** | Profile `agent-system`; `agent-contract.md` with all six core sections; a 6-row tool-permission matrix incl. the Stripe `refund.issue` row at `HITL: yes` (+ justification for every autonomous row); cost envelope with a token budget + a retry/step cap (latency referenced to architecture-constraints); 12 EARS REQs across 5 domains incl. must-not REQs for both high-risk tools; verify-spine PASS (exit 0) |
| baseline | **0/1** | a strong, thoughtful spec (defense-in-depth refund gate, traceability matrix) — but free-form `specification.md`/`tool-contracts.md`/`data-model.md` at the root: **no `docs/spec/` spine, no Profile field, no `agent-contract.md`, no delimited REQ blocks**. The lift is the entire governed agency contract, not raw insight (`feedback_framework_skill_lift_is_structural`) |

Sonnet-with-skill passing every deterministic check is the **honest portability claim**: the SKILL.md + the
`agent-contract.md` template + `shared/agentic-profile.md` carry the discipline, not model capability. (One benign
WARN in the with_skill arm: spine density 41 lines/REQ vs. the 40 guideline — WARN, exit stays 0.)

## Grader-validation (grader-first, before the live run)

Hand-ideal agent spine (`val-3.2/ideal/`, authored in the design's **literal** output form — the exact
`| Tool | Scopes | Risk | HITL |` header, real `IF …, THEN the system SHALL refuse …` must-nots) → **15/15**. Three
degenerates each fire **exactly** their target and nothing else:
- **missing HITL column** (drop `HITL` from the matrix header + rows) → *Tool-permission matrix carries a HITL column* fails;
- **dropped must-nots** (remove REQ-003/004) → *≥1 must-not (IF/THEN) REQ* fails;
- **dropped section** (remove Memory policy) → *agent-contract has all six core section heads* fails.

The six-section detector was widened to a **heading-or-bold-label** matcher (a Sonnet arm may render section heads as
bold labels, not `##` headings) and re-validated — the section-drop degenerate still bites, so the widening is robust,
not vacuous. Then the **real** with_skill output was re-graded at 15/15 (not just the hand-ideal) — the
`feedback_grader_validate_on_real_outputs` loop, closed.
