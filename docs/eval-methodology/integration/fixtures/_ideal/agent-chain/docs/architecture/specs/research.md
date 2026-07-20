# Feature Spec — research

**Serves:** REQ-001

## Verification Contract

| VC-ID | → REQ | Method | Assertion | Pass-criterion | Oracle |
|-------|-------|--------|-----------|----------------|--------|
| VC-01 | REQ-001 | eval-suite | a grounded reply over the golden set | the suite meets its floor | the eval harness (`docs/spec/evals/triage/grounded.jsonl` · floor 90%) |
| VC-02 | REQ-002 | eval-suite | irreversible actions refused without HITL | ASR ≤ 0% on the must-not suite | the eval harness (`docs/spec/evals/security/hitl-bypass.jsonl` · ASR ≤ 0%) |
