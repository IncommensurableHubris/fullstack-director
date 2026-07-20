<!-- Filename: SECURITY.md (project root). Emitted by skill 00 at WRITE SPINE — a public vulnerability-disclosure
     policy, the coordinated-vulnerability-disclosure (CVD) floor. 06 G7 checks its presence at release. -->

# Security Policy

> How to report a vulnerability in this project, and what to expect back. This is the **CVD floor** (the CRA
> reporting trajectory's solo-scale baseline) — not a full PSIRT program.

## Reporting a vulnerability

- **Contact:** _<a monitored channel — e.g. `security@<project>` or a private GitHub Security Advisory>_.
- **Please include:** the affected version / commit, a reproduction, and the impact you observed. **Do not** open a
  public issue for a security report.
- **Please do not:** run automated scanners against production, access other users' data, or exfiltrate data — a
  proof-of-concept is enough.

## What to expect (the CVD window — stated once)

- **Acknowledgement:** within _<N business days — e.g. 3>_ of your report.
- **Assessment + a remediation plan:** within _<N business days — e.g. 10>_.
- **Coordinated disclosure:** we credit reporters and coordinate a disclosure date; please allow a reasonable
  embargo (default _<90 days>_) before public disclosure.

## Scope

> **Boundary (S8-style):** this policy governs the **application code in this repository**. Live-infrastructure
> hardening (TLS termination, network policy, OS patching) is the **deployment owner's** responsibility, not this
> repo's — report infrastructure issues to the operator, not here.
