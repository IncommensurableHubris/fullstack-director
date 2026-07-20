# System — Beacon
## Context (C4 L1)
Beacon is an LLM **agent** (orchestrator-worker) that plans a research job, calls tools (source.search, source.fetch, report.synthesize), and synthesizes a report. Model: a general LLM with a tool-calling loop.
## Building Blocks
Orchestrator (planner) -> Workers -> Synthesizer. Untrusted inputs: the user question AND all fetched source content.
## Crosscutting
Prompt assembly in src/planner.js; tool dispatch in src/orchestrator.js.
