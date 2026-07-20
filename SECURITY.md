# Security Policy

## Reporting a vulnerability

Report suspected vulnerabilities **privately via GitHub Security Advisories** — use *"Report a vulnerability"*
on this repository's Security tab. Please do not open public issues for security reports.

- **Acknowledgement:** within 7 days.
- **Coordinated disclosure:** we ask for up to 90 days to investigate and remediate before public disclosure.

## Scope

The framework's own content: the skills under `.agents/skills/`, the shared protocols under `shared/`, the
subagent definitions under `.claude/agents/`, and `tools/vendor.py`. Products built *with* the framework carry
their own `SECURITY.md` — the framework emits a coordinated-vulnerability-disclosure floor into every consumer
project it initializes (skill `00-discovery`; release gate G7 checks its presence).
