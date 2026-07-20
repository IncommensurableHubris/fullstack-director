# discovery-evals — the `00-discovery` diagnostic track

A **diagnostic** harness, not a regression guard. Its job is to find where `00-discovery`'s doctrine bends under
adversarial pressure — engineered traps, each tempting one specific violation — and turn what it finds into a
triaged, human-reviewed ledger. **A case that makes the skill stumble is a success, not a regression to hide.**

## Nature

|  | Calibrated harness (`.agents/skills/00-discovery/evals/`) | This track |
|---|---|---|
| Question | does `with_skill` beat baseline + hold its contract? | where does the **doctrine itself** bend? |
| Unit | assertion pass/fail per arm | a **finding**, with evidence + disposition |
| Semantics | lift + regression guard | weak-spot ledger — zero findings is **"held"**, never "passed" |
| Cases | fidelity-spectrum inputs | engineered traps, one doctrine violation each |

The two tracks never share a file, a schema, or a vocabulary. See [`shared/`](../../../../shared/) at the repo root
for the methodology this track probes against.

## The V/B/G/C taxonomy

- **V — invariant Violation.** A deterministic probe fires against a hard rule (e.g. spine written under EXPLORE).
- **B — doctrine Bend.** No probe fires, but the auditor documents a violation of doctrine *intent*, verbatim.
- **G — doctrine Gap.** The run did something defensible that doctrine simply doesn't cover — the case exposed a
  missing or ambiguous rule.
- **C — Capability slip.** The rule is stated but a weaker executor missed it while a stronger one held; an
  enforcement-hardening candidate, not a doctrine defect.

## Pipeline

1. **Probe** — deterministic sensors over the run's outputs; a fired probe is data, never a pass/fail gate.
2. **Opus audit** — one subagent per run reads doctrine + outputs + probe report, emits candidate findings with a
   verbatim `evidence_quote` and a named `doctrine_anchor`.
3. **Fable adjudicate** — one batched subagent per wave, refute-by-default, emits the wave's findings ledger.
4. **Human review** — the user reviews the ledger before any doctrine edit or triage disposition is enacted.

## Isolation

This track never touches `.agents/skills/00-discovery/evals/**`, `check_spine.py`, or anything the calibrated
`aggregate_benchmark` reads — verified by a self-test at wave end. Vocabulary is deliberately distinct: *case /
probe / finding / wave*, never *eval / assertion / grading / iteration*; file names follow suit (`cases.json`,
`probe-report.json`, `findings-ledger.json`). Corpus artifacts (this directory) are committed under `docs/`; run
outputs are gitignored under `_artifacts/discovery-evals/00-discovery/wave-1/…` and never carry durable state.

## How to run a wave

Wave execution is window-staged (it spawns real Sonnet/Opus/Fable subagents) and runs from a fresh session — see
the wave-execution runbook, Phase 5 of the build plan, for the staged recipe.
