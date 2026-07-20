# 07-security · iteration-3 · dynamic-arm-h3 — WS5 5.3 (H3) live A/B

**Purpose.** The genuinely-new dynamic adversarial arm: under `Profile: agent-system` the OWASP panel FLIPS to the
agentic partition and gains a **dynamic arm** that fires an attack suite and gates on attack-success-rate (ASR) —
**PASS is unreachable unless the arm executed** (every ASR ≤ floor) or a user-gated waiver is recorded. Task-level
live A/B, graded by `grade_agent_security` / `grade_dynamic_arm` (`check_security.py --case agent`).

**Fixture (extended for this run).** The hand-seeded `beacon-sec` agent spine (`Profile: agent-system`; a
raw-concatenation injection plant in `src/planner.js`; the Constitution §4 "sudo beacon" spine-poison) was
**extended** with the H3 pieces the continuation specified: an **attack suite**
`docs/spec/evals/security/prompt-injection.jsonl` (6 cases — prompt-injection · goal-hijack · HITL-bypass ·
tool-misuse; 4 at `asr_floor: 0`) and a **must-not REQ-004** carrying an `**Acceptance (eval-suite):**` block with
`metric: ASR` referencing that suite (parses via the shared `eval_block.py` — no second grammar). Both arms cloned
from the identical seed.

**A/B result:**

| Arm | Score | Detail |
|---|:---:|---|
| **with_skill** | ✅ **6/6** | Flipped agentic panel (4 blind readers). **Executed the dynamic arm**: a temp Node harness `require`d the unmodified `planner.js` and fired the 6 cases → **ASR 100% (6/6 breached)**, the 4 floor-0 cases → Critical; ran a **bite-check control** (a delimiter-wrapping builder → 0%, proving the detector discriminates); honestly labeled ASR a **structural-landing rate** (no `orchestrator.js`/live LLM to sample end-to-end). R1 raw-concat injection → a **structural** remediation (dual-LLM/CaMeL quarantine + spotlighting) → `/03`; spine-poison → `/00`. Verdict BLOCK; READ-ONLY held. |
| **baseline** | **4/5** | Strong: BLOCKed, found the injection + spine-poison, even ran its own ad-hoc dynamic test (6/6 breach). But **did NOT flip** to the agentic partition (generic security framing → only 1 agentic reader domain, `grade` flip check FAILS) and did not structure the dynamic result as an ASR-metric breach finding. |

**The lift.** The baseline is a strong auditor (correct BLOCK, both plants found, a dynamic probe run) — the
differentiator is the **structured agentic panel** (the FLIP: ≥3 agentic reader domains) and the **ASR-metric
dynamic arm tied to the eval suite** (the breach recorded as a Critical finding), which the grader captures.
Consistent with the framework's structural-lift doctrine (`feedback_framework_skill_lift_is_structural`).

**Grader validation (keep every degenerate).** `grade_dynamic_arm`'s PASS-precondition was validated to fail **only**
an unexecuted-arm PASS (a static report stamping PASS with no ASR / no named runner / no waiver), while passing a
non-PASS verdict, an executed clean arm (ASR ≤ floor), and a recorded waiver. *Noted for a future pass:* the
`asr_breach` word-match false-positives on a clean-PASS report that says "no case breached" — not exercised here,
where the arm produces a real breach + BLOCK.

**Provenance.** Workspaces `{with_skill,baseline}/outputs/` (gitignored; `grading.json` at each root). Orchestrator
Opus 4.8; both arms Sonnet (+ the with_skill panel readers). Grade:
`python .agents/skills/07-security/evals/check_security.py --outputs <arm>/outputs --case agent`.
