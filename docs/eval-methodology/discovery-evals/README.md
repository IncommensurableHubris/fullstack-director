# Discovery-evals — the adversarial diagnostic track

> **A diagnostic, not a regression gate.** A case that makes a skill stumble is a **success**. There is no pass/fail
> axis: the unit is a *finding* with evidence and a disposition, and zero findings is "**held**", never "passed".
> That framing is the structural guard against this track quietly becoming a second regression suite — which would
> re-calibrate the A/B harness it is supposed to complement.

Wave 1 (`00-discovery`, 2026-07-14/15) is complete: [`00-discovery/waves/wave-1.md`](00-discovery/waves/wave-1.md).
Read that record before running wave 2 — it holds the corpus feedback and the two ways the *fixes* went wrong.

## Why this track exists (and what the calibrated suite cannot do)

Every skill ships a **calibrated** eval suite (`.agents/skills/<skill>/evals/`). Those measure **lift**: does
`with_skill` beat a no-skill baseline? They answer *"is the skill worth loading?"* and they consistently say yes.

They are structurally blind to a different question: **is the doctrine itself wrong?** A lift suite tests cases where
the skill should shine. It cannot find a rule that is confidently, consistently wrong — because both arms are scored
against what the skill *intends*, and a wrong intention scores fine.

Wave 1 proved the gap is real, not theoretical. `DF-001`: `00-discovery`'s Profile test keyed only on deliverable
*shape*, so a webapp embedding an unattended money-moving LLM was classified `webapp` — no agent-contract, no
injection lens. The **baseline arm**, running with no doctrine at all, surfaced the governance gaps on its own.
Doctrine was not merely silent; it was **railroading** runs into the wrong answer. **On that axis the framework was
worse than no framework** — a finding a lift suite can never surface, because it only appears when the baseline
*wins*.

| | Calibrated suite | Diagnostic track (this) |
|---|---|---|
| Question | is the skill worth loading? | is the doctrine wrong? |
| Method | A/B lift vs. no-skill baseline | adversarial traps → probes → audit → adjudication |
| Unit | assertion pass/fail | **finding** (V/B/G/C) + disposition |
| Good result | high lift | **a case bites** |
| Blind to | wrong-but-consistent doctrine | ordinary quality/lift |

## The model-tier convention — and *why* each seat sits where it does

This is the load-bearing design decision of the track. It is not "use the big model for the hard part". Each tier is
chosen for a **property**, and the through-line is **judge ≠ executor at every stage** (self-preference is the
failure mode that quietly invalidates an eval).

| Seat | Model | Why this tier — the property being bought |
|---|---|---|
| **Executor** | **Sonnet** | *Realistic consumer-grade, higher failure yield.* The executor must be the model a real user actually runs the skill with. A too-strong executor holds on doctrine that is genuinely weak, and the trap never bites — you learn nothing and conclude wrongly that the skill is fine. Sonnet's higher slip rate is the **point**, not a compromise. |
| **Auditor** | **Opus** | *Rubric-anchored judgment over long, messy artifact trees.* Reading a whole spine against doctrine and deciding "is this a bend?" is the hardest reasoning in the pipeline, and it is where every real finding actually came from (wave 1: **every probe fire was a false positive; all 4 confirmed findings came from the audit**). One auditor per run, blind to other runs. |
| **Attribution re-run** | **Opus** *(as executor)* | *The capability/doctrine discriminator.* Re-run the confirmed case on the stronger model. **Opus holds → `capability`** (the rule exists; enforcement is weak → harden the gate). **Opus fails too → `doctrine`** (the rule is missing/wrong → write it). This one arm converts a flat finding list into two different kinds of work, and it is why wave 1 could say "harden these two, rewrite that one" instead of "here are four problems". |
| **Adjudicator** | **Fable** | *One batched, refute-by-default pass → the confirmed ledger.* A third model that judged neither the run nor the audit. Kills anything whose `evidence_quote` does not violate its cited anchor; uncertainty resolves to **kill**. Wave 1: 10 candidates → 4 kept (5 `duplicate`, 1 `non-reproducible`). |
| **Probes** | *(deterministic code)* | *Sensors, not gates.* Cheap leads that tell the auditor where to look. **Never** a verdict. |

**The sweet spot, stated plainly:** spend the cheap tier where you want failure (executors), the expensive tier where
you need judgment (audit + attribution), and a third, disinterested tier where you need the count to be honest
(adjudication). Never let one model both produce and grade the same artifact.

**Observed costs** (16 runs, remarkably stable — use these to budget):
- Sonnet spine-producing executor: **~110k** subagent tokens (10 trial-1s averaged 110.1k; 6 repeats averaged 110.2k).
  Range 69k (EXPLORE, no spine) → 154k (agent-system arm with a full agent-contract).
- Opus auditor: **~55-85k**. Fable adjudicator (whole wave, batched): **~76k**.
- A full 11-case wave, all four stages: **~4M**. A 9-case calibrated regression sweep: **~1M**.

**Do not "upgrade" the executor tier.** If a wave comes back all-held on Sonnet, that is a *result* (escalate to an
adaptive wave 2 of harder variants), not a reason to re-run on Opus. Opus is the attribution instrument; using it as
the executor destroys the discriminator.

## The pipeline

```
   fixture + run_prompt                     (the trap: one doctrine anchor × one tempt vector)
        │
        ▼
   Sonnet executor  ──► outputs/           (a real spine, produced blind, in a corpus-free sandbox)
        │
        ├─► probe_<case>.py ──► probe-report.json     deterministic sensor · a LEAD, never a verdict
        │
        ▼
   Opus auditor     ──► audit.json         candidate findings: class · anchor · evidence_quote · severity
        │                                  (runs on EVERY trial-1, even where no probe fired — B-class
        │                                   findings, the ones this track exists for, appear only here)
        ▼
   reproduction (Sonnet ×2)                V/B/C confirm at ≥2/3 trials · G is confirmed against doctrine TEXT
   attribution  (Opus ×1)                  Opus holds → capability · Opus fails → doctrine
   baseline arm (Sonnet, no skill)         only when the auditor set needs_baseline_arm — did doctrine railroad?
        │
        ▼
   Fable adjudicator ──► adjudication.json  refute-by-default; uncertainty → kill
        │
        ▼
   collect_ledger.py ──► findings-ledger.json  (run ONCE per wave — re-running renumbers DF-NNN)
        │
        ▼
   human review ──► triage (doctrine-edit / calibrated-case-proposal / defer)
```

## Hard rules (learned, not invented)

1. **The RUNNER pre-seeds; the executor never copies fixtures.** Keeps `RUN-CONDITION.md`-style trap descriptions
   structurally unreachable.
2. **Executors run in a corpus-free sandbox** — `tools/make_sandbox.py`. See "Executor isolation" below. This is the
   wave-1 lesson that invalidates data if ignored.
3. **Probes are sensors, not gates.** A fired probe is a lead; a silent probe clears nothing.
4. **The auditor runs on every trial-1**, including cases where no probe fired.
5. **Never touch `.agents/skills/<skill>/evals/**` from this track** — `probe_lib.py` *copies* parsing from
   `check_spine.py`, never imports. The isolation self-test enforces it every stage. The rule exists because this
   track must not be able to tune the regression bridge that judges its own fixes. *If a calibrated grader needs
   repair, that is a separate task, done by someone with no stake in this track's findings.*
6. **Distinct vocabulary** — case / probe / finding / wave. Never eval / assertion / grading / iteration.
7. **Window-staged execution.** One stage per 5-hour window; estimate the run count against headroom and defer rather
   than strand a half-judged batch.
8. **`collect_ledger.py` runs once per wave.** Re-running renumbers `DF-NNN` and drops dispositions.

## Executor isolation — the wave-1 hole, and what closes it

**The defect:** executors run with cwd = the framework repo (they must, to read `SKILL.md`). That same cwd exposed
the entire corpus — `cases.json` (every trap's `doctrine_anchor` **and** `tempt_vector`), `fixtures/**/RUN-CONDITION.md`,
`audit/rubric.md`, the probe scripts, and the wave records. We meticulously kept the answer *key* out of the sandbox
while leaving the answer *book* in the working directory.

**It was exploited, not hypothetically:** a wave-1 executor ran `probe_silent_mutation.py` on its own output, found
its wording tripped a keyword check, **reworded until the probe went quiet**, and deleted the probe-report it had
generated. A different executor independently *refused* to look, for exactly this reason. **That variance is the
proof**: "the executor won't peek" is a prediction, and `shared/agentic-profile.md` § Doctrine rejects predictive
controls by name.

**The rule:** a probe silence is evidence **only if the executor never saw the probe**.

**What closes it** — `tools/make_sandbox.py` builds a run root containing only:

```
<sandbox>/framework/.agents/skills/<skill>/   SKILL.md + references + templates (its own evals/ stripped)
<sandbox>/framework/shared/                   the cross-skill protocols
<sandbox>/work/                               the seeded project root
```

with an **opaque path** (`runs/<sha-token>/`) that names neither the track nor the case — because the old path
(`_artifacts/discovery-evals/…/silent-mutation/…`) was itself the breadcrumb that invited the peek. The builder
**fails closed**: it audits its own output and refuses to hand over a sandbox containing any corpus artifact.

**Residual, stated honestly:** the Agent tool inherits the session cwd and a subagent's cwd cannot be set, so an
executor that goes looking *can* still reach the repo. The sandbox removes the **need** and the **signal**, not the
possibility. `tools/check_executor_isolation.py` would detect it from the run transcript — but in this harness the
per-agent `.output` is **0 bytes once the agent completes**, so the tool reports `UNVERIFIABLE` (exit 3) and
deliberately **never** reports "clean" on empty evidence: a check that certifies garbage is worse than no check
(§ the bite rule). A hermetic fix needs harness cwd control, or the corpus living outside the repo. **Until then the
sandbox carries the load.**

## Layout

```
docs/eval-methodology/discovery-evals/
  tools/make_sandbox.py          corpus-free executor sandbox (fails closed)
  tools/check_executor_isolation.py   transcript check; UNVERIFIABLE unless transcripts exist
  tools/collect_ledger.py        audits + verdicts → findings-ledger.json
        ^ skill-agnostic (`--skill <name>`) — SHARED across waves, not per-skill (moved up 2026-07-19, wave 2)

docs/eval-methodology/discovery-evals/<skill>/
  cases.json                     the trap manifest (anchor · tempt vector · probes · fixture · run_prompt)
  probes/probe_<case>.py         one deterministic sensor per case
  probes/probe_lib.py            shared parsing (COPY-adapted from check_spine.py — never imported)
  probes/selftest.py             isolation + anti-tautology gate (every probe fires on its degenerate, silent on its ideal)
  fixtures/<case>/               the trap inputs (+ RUN-CONDITION.md — never seeded, never sandboxed)
  audit/{rubric,auditor-prompt,adjudicator-prompt}.md   reused verbatim ({doctrine_targets} is a per-case runtime fill)
  schemas/{probe-report,audit,findings-ledger}.schema.json   frozen — reuse unchanged
  waves/wave-N.md                the durable record (the run workspace is gitignored)
```

Runs live at `_artifacts/discovery-evals/<skill>/wave-N/` and sandboxes at `_artifacts/runs/<token>/` — both
gitignored. The wave record is the artifact that outlives them.

## Next: wave 2 → `03-architect`

See [`wave-2-handoff.md`](wave-2-handoff.md) for the full brief, the candidate corpus, what ports as-is, the carried
corpus feedback, and why `03-architect` is the chosen target.
