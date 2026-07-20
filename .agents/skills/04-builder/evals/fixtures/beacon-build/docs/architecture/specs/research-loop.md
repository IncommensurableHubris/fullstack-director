# Feature Spec — research-loop

**Serves:** REQ-001, REQ-002, REQ-003 · **Status:** Draft

## Overview

The orchestrator-worker research loop: dispatch workers across sources (REQ-001), synthesize a grounded report
(REQ-002), and drop any uncited claim (REQ-003).

## Related

- **Sprint:** `docs/planning/sprints/sprint-01.md` · **Architecture:** `system.md` · **ADRs:** ADR-002 (topology)

## Components

| Component | Layer | Responsibility | Location |
|-----------|-------|----------------|----------|
| Orchestrator | backend | fan out workers, collect findings, synthesize | src/orchestrator |
| Worker | backend | search + fetch one source in its own context | src/worker |

## Verification Contract

| VC-ID | → REQ | Derived-from (spine Gherkin) | Method | Assertion (loosest claim that catches a break) | Pass-criterion (boolean) | Oracle |
|-------|-------|------------------------------|--------|------------------------------------------------|--------------------------|--------|
| VC-01 | REQ-001 | "workers search those sources concurrently" | unit | dispatching N sources starts N workers concurrently, each with a distinct context handle | N concurrent workers observed AND N distinct contexts | the orchestrator dispatch test |
| VC-02 | REQ-002 | "every claim is grounded in a retrieved source" | eval-suite | the synthesis quality suite meets its floor over the in-spine dataset | suite score ≥ floor | harness: `python evals/run.py --dataset docs/spec/evals/research/synthesis.jsonl` · floor 80% (capability) |
| VC-03 | REQ-003 | "the claim is not included" | unit | a drafted claim with no source reference is dropped from the assembled report | uncited claim absent from output | the assembler test |

## Design Contract Coverage

Skip — headless slice, no `docs/design/approved/sprint-01/manifest.md` (no tool-surface UI this sprint).

## Not-Tested This Sprint

| Item | Reason | Deferred to |
|------|--------|-------------|
| source allowlist admin | not in the slice | sprint 02 |
