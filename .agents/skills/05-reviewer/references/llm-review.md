# LLM / RAG / agent error analysis — module (mandatory under `Profile: agent-system`)

> **Gating depends on the profile** (`shared/agentic-profile.md`, the per-seat toggle table): under **`webapp`** this
> module is **gated** — load it **only** if `system.md` names LLM / RAG / agent components (for a pure-domain slice,
> skip it; do not invent AI-quality findings where there are no AI components). Under **`agent-system`** (the
> deliverable IS the agent) it is **MANDATORY** — the AI *is* the system under test, so error analysis and the
> **re-execution of declared verifications at `final_commit`** (below) always run. This is a lean distillation of the
> Husain evaluation methodology. Findings follow the same read-only, routed-to-`04` rule as every other finding
> (`references/review-discipline.md`) — 05 verifies and reports, it does not re-prompt or re-tune.

## Why AI features need a different lens

An LLM feature can pass every deterministic test and still be wrong: the contract is a *distribution of outputs*, not
a fixed return value. So the evidence is **error analysis on real traces**, not a green unit bar. Keep it binary
(pass/fail with a written critique) — Likert scales blur the judgment and are harder to track.

## The pass — five checks, in order

1. **Map the LLM surface.** For each feature that calls an LLM / retrieves context / runs an agent loop: what model,
   what inputs (user input, retrieved context, state), what output (text, structured data, tool calls), and the
   acceptance criteria it must meet (from the in-scope REQ's outcome-Gherkin).
2. **Error analysis (the single most important step).** Collect or generate a representative set of traces
   (input → output). For each, make a **binary pass/fail** judgment and write a one-line **critique** of *why*.
   Open-code the failures into categories; report the **top 3 failure modes** as findings (severity re-derived,
   routed to `04`). Looking at real traces is how you discover what is actually wrong — do not rely on aggregate
   metrics alone. Method depth (sampling · saturation · fix-before-evaluator triage) is evals-operations — bind per
   the capability (`shared/agentic-profile.md` §eval-suite).
3. **Evaluation dataset exists.** Each LLM feature should carry a versioned eval set (a floor of ~20 cases; 50+ for
   critical features), spanning Features × Scenarios × Personas (the dimension→tuple synthetic-bootstrap method is the same capability), including adversarial / unanswerable / ambiguous /
   max-length inputs. Its **absence for a critical feature is a BLOCK** (there is no way to know it works).
4. **LLM-as-judge validation (only if the project uses one).** An automated judge gates nothing until its **judge-validation record**
   (`docs/verification/judges/<judge-name>.md`; schema: `shared/agentic-profile.md` §eval-suite) shows **TPR >90%
   AND TNR >90%** on a held-out test split (floor 80/80 — below it the judge is **untrusted**, fall back to human
   review). Check **presence and currency**: the pinned judge model matches the one in use, and
   `validated_at_commit` postdates the judge's last prompt/model change. Raw agreement/accuracy is not a
   validation metric. A production pass-rate reported from judge scores carries bias correction + a confidence
   interval. Judge *writing* and *validation* are evals-operations (the capability in `shared/agentic-profile.md`
   §eval-suite). This is the `02`/`03` lesson repeated: an unvalidated LLM judge is "generally not robust", so it is a
   **finding**, not a verification method 05 leans on. Check for over-pass / over-fail bias by category.
5. **Prompt · RAG · agent · guardrails (checklist, flag only what breaks a REQ).**
   - **Prompt:** version-controlled (not inline), structured, injection-safe (user input never concatenated into a
     system prompt unsanitized), few-shot where accuracy matters.
   - **RAG:** retrieval tested separately from generation (Precision/Recall@k); generation **faithful** (grounded in
     retrieved context, not hallucinated); unanswerable queries **refuse** rather than fabricate.
   - **Agent:** correct tool selection + parameters; graceful recovery from tool failure; stays on task; bounded steps
     / tokens (no unbounded generation loop).
   - **Guardrails:** content moderation + PII handling where user-facing; jailbreak / prompt-injection resistance
     tested with adversarial inputs; a defined fallback for model unavailability.

## Re-execute the declared verifications at `final_commit` (mandatory under `agent-system`)

05 is context-isolated, so it does not trust the builder's evidence — it **re-runs the declared verifications itself**
at the handoff's `final_commit` (pinned seeds/config), the same discipline the deterministic oracles get. "Declared
verifications" is **both** kinds the chain has recorded — this one section subsumes them so there is one home:

1. **Eval-suite floors.** For every spine `**Acceptance (eval-suite):**` block on an in-scope REQ, re-run its harness
   over the in-spine dataset (`docs/spec/evals/**`) with **pinned seeds + config** and confirm the score **meets the
   declared floor**. Count how many suites ran.
   - **Scope carve-out:** `docs/spec/evals/security/**` is **NOT** 05's to run — 07's security panel is the sole
     executor of security suites (`shared/agentic-profile.md`; avoids a double-run + a split verdict).
2. **Fitness functions.** Re-run every `static-conformance` Verification-Contract row (an ADR's *Rule* made executable
   — a lint / dependency rule / arch test) and confirm it still holds at `final_commit`. A fitness function green in
   the build but red on re-run is a regression finding.
3. **The grader hack-resistance spot-check (the bite rule).** For each eval suite, feed the grader a **degenerate
   output** (empty / constant / obviously-wrong) and confirm the grader **fails it**. A grader that passes garbage
   makes its floor fiction — a tautological grader is a **finding**, and its floor does not count as met. This is the
   `final_commit` re-run of 04's grader-bites (`shared/agentic-profile.md`).

**Record the tally in the qa-report frontmatter — exact tokens (06's G8 greps these):**

- `eval_floors_met: true` — every re-run eval suite met its floor **and** its grader bit;
  `false` — any floor missed or any grader hollow (⇒ the verdict cannot be SHIP);
  `n/a` — no eval-suite REQ in scope (a `webapp` slice with no declared eval floors).
- `evals_run: <int>` — how many eval suites 05 actually re-ran (0 when `n/a`).

## Verdict contribution

- **SHIP** additionally requires: error analysis complete with no critical failure mode unaddressed, an eval dataset
  present for every LLM feature, any LLM judge validated (>90%), guardrails verified — **and, under `agent-system`,
  `eval_floors_met: true`** (every declared floor re-met at `final_commit`, every grader bit).
- **FIX REQUIRED** if error analysis surfaces addressable failure modes, eval scores are below threshold but the
  architecture is sound, or guardrails are incomplete.
- **BLOCK** if a critical LLM feature has **no** eval dataset, the judge is untrusted and no human fallback exists, or
  error analysis reveals a systemic failure needing an architectural rethink (route to `03`).
