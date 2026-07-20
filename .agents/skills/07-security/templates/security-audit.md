<!-- Filename: docs/security/security-audit-sprint-NN.md  (or security-audit-full.md for audit_mode: full).
     Written on EVERY 07-security run — including a BLOCK (the refusal is the auditable security record). -->

---
verdict:            PASS          # PASS | REMEDIATE | BLOCK   ← 06-release G6 gates the ship on this
audit_mode:         sprint        # sprint | full
sprint:             NN            # NN | full
owasp_edition:      "2021+2025"   # the edition(s) audited against — recorded, never a silent constant
asvs_level:         L1            # H1: the ASVS 5.0 verification bar (from architecture-constraints; default L1, absent ⇒ L1)
findings_critical:  0
findings_high:      0
findings_medium:    0
findings_low:       0
areas_audited:      10            # OWASP areas the panel covered (completeness)
areas_na:           0             # areas ruled N/A — each justified in (c)
llm_module:         absent        # absent | run   (the conditional R5; 'run' only when system.md names AI components)
panel_readers:      4             # 4, or 5 with the LLM/agentic reader
audited_commit:     <SHA>         # the commit the panel read (staleness anchor)
scanners:           none          # deterministic scanners actually run (npm-audit,gitleaks,…) or 'none'
data_sensitivity:   low           # low | medium | high → the third-party-pen-test recommendation strength
---

# Security Audit — Sprint NN <!-- (or: Full) -->

> **The auditable security record `06-release` G6, `/status`, and a human act on.** Owned by **skill 07 (security)**.
> The frontmatter is machine-readable state; the sections are the evidence. VERDICT HONESTY: **PASS is unreachable
> while any Critical/High is unremediated**; severity is re-derived centrally; every finding carries a `file:line` +
> `source_quote`; **no secret VALUE** appears anywhere. Craft: `references/owasp-panel.md` +
> `references/synthesis-and-verdict.md`.

## (a) Verdict

**PASS | REMEDIATE | BLOCK** — _<one line: the single most decision-relevant fact. e.g. "REMEDIATE — five HIGH
findings across the HTTP surface, all code-fixable; routed to /04-builder." or "BLOCK — a Critical client-trusted
authorization model; route to /03-architect." or "PASS — no Critical/High; the surface is hardened.">_

## (b) Panel manifest (read-only attestation)

| Reader | Area slice (OWASP) | Findings |
|--------|--------------------|----------|
| R1 · Access & Authn | A01, A07, A04 | _<n>_ |
| R2 · Injection & Forgery | A03, A10 | _<n>_ |
| R3 · Secrets, Crypto & Config | A02, A05 | _<n>_ |
| R4 · Supply Chain, Integrity & Logging | A06/A03:2025, A08, A09 | _<n>_ |
| _R5 · LLM/Agentic (only if run)_ | _LLM01–10 / ASI01–10_ | _<n>_ |

**Read-only:** `src/**` unchanged at `<audited_commit>` — the panel modified no code. Readers ran **blind** (each saw
only its area-slice). LLM/agentic module: **_<absent — system.md declares no AI components | run>_**.

## (c) OWASP checklist (every area — PASS / FAIL / N/A with a reason)

| Area | Status | Evidence / reason |
|------|--------|-------------------|
| A01 Broken Access Control | _<PASS\|FAIL\|N/A>_ | _<what was checked / why N/A>_ |
| A02 Cryptographic Failures | _<…>_ | _<…>_ |
| A03 Injection | _<…>_ | _<…>_ |
| A04 Insecure Design | _<…>_ | _<…>_ |
| A05 Security Misconfiguration | _<…>_ | _<…>_ |
| A06/A03:2025 Software Supply Chain | _<…>_ | _<…>_ |
| A07 Authentication Failures | _<…>_ | _<…>_ |
| A08 Software/Data Integrity | _<…>_ | _<…>_ |
| A09 Logging & Alerting | _<…>_ | _<…>_ |
| A10 SSRF *(2021)* / Exceptional Conditions *(2025)* | _<…>_ | _<…>_ |

<!-- A bare "N/A" is a GAP, not a pass — say WHY (e.g. "no auth surface this slice"). -->

### ASVS 5.0 chapter coverage — the verification bar (scoped to `asvs_level`)

> Completeness is measured against **ASVS 5.0 (V1–V14)**, the *verification standard* — the OWASP Top-10 partition
> above *divides the work*; ASVS *is the bar* (OWASP positions the Top 10 as awareness, ASVS as verification). Scope
> the rows to the declared level (**L1** by default). Status ∈ **verified / partial / N-A**, each with an evidence
> pointer (a test · a scanner · reader judgment). The ~58% test-automatable / ~10% scanner / ~30% judgment-only split
> means the readers' manual remit **is** the judgment band (business logic, authz consistency, architectural intent).

| ASVS chapter (V1–V14, in scope at the level) | Status | Evidence (test · scanner · reader judgment) |
|----------------------------------------------|--------|---------------------------------------------|
| V1 Encoding & Sanitization | _<verified \| partial \| N-A>_ | _<…>_ |
| V2 Validation & Business Logic | _<…>_ | _<…>_ |
| V3 Web Frontend Security | _<…>_ | _<…>_ |
| V6 Authentication | _<…>_ | _<…>_ |
| V7 Session Management | _<…>_ | _<…>_ |
| V8 Authorization | _<…>_ | _<…>_ |
| V11 Cryptography | _<…>_ | _<…>_ |
| V13 Configuration | _<…>_ | _<…>_ |
| V14 Data Protection | _<…>_ | _<…>_ |

<!-- Scope to the declared level: L1 rows only unless architecture-constraints declares L2 (a Tier-2, sensitive-data
     decision). A chapter with no in-scope requirement at the level is N-A-with-reason, not silently dropped. -->

### Design-time threats × coverage (D6 cross-reference)

> Cross-reference `system.md` **§ Threats considered** against this audit: each designed threat → its verifying
> check/finding. A **designed threat with no verifying check is a GAP**; an audit **finding in a zone the design
> called safe** is **design feedback** → route `/03-architect`. If the design did **no** threat pass, say so (route /03).

| Designed threat (system.md § Threats) | Verifying check / finding | Status |
|---------------------------------------|---------------------------|--------|
| _<threat from the design's boundary pass>_ | _<the audit check/finding covering it — or "none">_ | _<covered \| GAP \| design-feedback>_ |

## (d) Findings (each: severity · area · file:line · source_quote · remediation · route)

| # | Severity | OWASP area | Location | source_quote (secrets redacted) | Remediation | Route |
|---|----------|-----------|----------|----------------------------------|-------------|-------|
| 1 | _<High>_ | _<A01 IDOR>_ | _<`src/…`:LL>_ | _<the offending line — value REDACTED if a secret>_ | _<the fix>_ | _</04-builder>_ |

<!-- Route: code-fixable → /04-builder · architectural → /03-architect · missing security declaration → /00-discovery.
     PASS: keep this table empty ("None"). BLOCK/REMEDIATE: every finding carries a file:line + a source_quote. -->

### Re-audit addendum — proof of fix (H2; only when re-auditing a prior REMEDIATE)

> Each prior finding gains a **`proof_of_fix`**: the regression test **plus** the **revert-check**. A finding
> **closes only when its test BITES ON REVERT** (revert the fix → the test goes RED). A finding claimed fixed with
> `proof_of_fix` = `none` / a test that does **not** bite **stays open** — the verdict stays REMEDIATE. Enforcement is
> the re-auditor's, not the fixer's (04 ships the test; 07 verifies it bites).

| # | Prior finding | Remediation | `proof_of_fix` (regression test · revert-check) | Status |
|---|---------------|-------------|-------------------------------------------------|--------|
| 1 | _<High · A01 IDOR · `src/…`>_ | _<ownership check added>_ | _<`npm test -- idor` green; `git revert <fix> && npm test -- idor` → RED (bites)>_ | _<closed \| open>_ |

## (e) Risk matrix (for the client-facing summary)

| # | Threat | Likelihood | Impact | Existing controls | Residual risk | Priority |
|---|--------|-----------|--------|-------------------|---------------|----------|
| 1 | _<…>_ | _<Low/Med/High>_ | _<Low/Med/High>_ | _<…>_ | _<Low/Med/High>_ | _<P1/P2/P3>_ |

## (f) Client-facing summary

**What is secured:** _<controls in place, in client terms>_
**What residual risks remain:** _<honestly — including what the audit cannot control>_
**Recommendations:** immediate (P1) _<…>_ · short-term (P2) _<…>_ · long-term (P3) _<…>_
**Third-party testing:** _<An AI-assisted audit is not a substitute for third-party penetration testing. For **medium/
high** data sensitivity: "strongly recommended before a public launch." Live-infrastructure hardening (TLS, network
policy, OS patching) is out of the repo audit's scope — route to the deployment owner.>_

## (g) Next command (07 recommends; the director runs it)

- **PASS** → `/06-release sprint NN` (G6 passes) · next sprint · `/00-discovery reflect`.
- **REMEDIATE** → `/04-builder sprint NN` (fix each routed finding), then a fresh `/07-security sprint NN` re-audit.
- **BLOCK** → the routed owner: architectural → `/03-architect`; missing security declaration → `/00-discovery`;
  then re-audit.

## Session summary (paste as the conversational reply — lead with verdict + tally, never narrative)

```
SECURITY — SPRINT NN — <PASS | REMEDIATE | BLOCK>
Findings: <C>/<H>/<M>/<L> (critical/high/medium/low)   OWASP edition: 2021+2025   Panel: <N> readers (read-only)
LLM module: <absent|run>   Scanners: <…|none>   Data sensitivity: <low|medium|high>
<if REMEDIATE/BLOCK: one line per HIGH/Critical finding with its routed command>
Report: docs/security/security-audit-sprint-NN.md   Next: <the (g) command>
```
