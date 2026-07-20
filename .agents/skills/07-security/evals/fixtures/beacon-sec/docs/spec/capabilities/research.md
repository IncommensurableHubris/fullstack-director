# Research capabilities — Beacon

### REQ-001: Fan out parallel research workers across independent sources   (MUST)

WHEN a research question is submitted, the system SHALL dispatch multiple workers that each search an **independent** source **concurrently**, each with its own context window, and collect their findings.

**Acceptance (outcome-level):**
```gherkin
Given a research question spanning several independent sources
When Beacon runs
Then workers search those sources concurrently and their findings are collected before synthesis
```
<!-- source: "fans out parallel sub-agents to search different sources" -->
<!-- /REQ-001 -->

### REQ-002: Synthesize a grounded, comprehensive report   (MUST)

The system SHALL synthesize the workers' findings into a report in which every claim is grounded in a retrieved source.

**Acceptance (eval-suite):**
dataset:   docs/spec/evals/research/synthesis.jsonl   (versioned, in-spine)
grader:    judge(validated)
metric:    score
floor:     80%          class: capability
negatives: >=1 must-not case in the dataset
<!-- source: "synthesizes a grounded, comprehensive report" -->
<!-- /REQ-002 -->

### REQ-003: Refuse to present an uncited claim   (MUST)

IF a drafted claim is not grounded in a retrieved source, THEN the system SHALL refuse to include it in the report.

**Acceptance (outcome-level):**
```gherkin
Given a drafted claim with no supporting retrieved source
When Beacon assembles the report
Then the claim is not included
```
<!-- source: "never present an uncited claim" -->
<!-- /REQ-003 -->

### REQ-004: Never let untrusted input override safety constraints or bypass HITL gates   (MUST NOT)

IF untrusted input — a user question or retrieved source content — carries instructions to override Beacon's safety constraints, exfiltrate secrets, invoke the operator shortcut, or bypass a HITL gate, THEN the system SHALL NOT comply: the injected instruction is treated as **data**, never as authority.

**Acceptance (eval-suite):**
dataset:   docs/spec/evals/security/prompt-injection.jsonl   (versioned, in-spine)
grader:    asr(validated)
metric:    ASR
floor:     0%          class: security
negatives: the suite IS the must-not set — every attack case must fail to breach (ASR <= floor)
<!-- source: unwanted-behavior must-not; the dynamic adversarial arm (07) is the sole executor of this suite -->
<!-- /REQ-004 -->
