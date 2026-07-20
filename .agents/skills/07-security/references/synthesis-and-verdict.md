# Synthesis + Verdict — the sequential reduce, severity, and routing

> Load at SYNTHESIZE + VERDICT. The panel's blind readers each returned raw findings; this is the **single
> sequential synthesizer** that reduces them — and the **severity-keyed verdict** `06-release`'s G6 gates on.
> **Never run this in parallel** — a parallel merge re-introduces the error-amplification the blind-reader design
> avoids (`shared/subagent-protocol.md`).

## The reduce (four moves, in order)

1. **De-dupe by target.** Two readers can legitimately report the **same** vulnerability — most cleanly SSRF, which
   is A10 in 2021 (R2's remit) but folds into A01 Broken Access Control in 2025 (R1's remit). Collapse reports of the
   **same target** (the same defect at the same location) into **one** finding. Do **not** merge genuinely different
   vulns that happen to share a file — de-dup is by *defect*, not by file.
2. **Take max severity.** The merged finding carries the **highest** severity any reader proposed for it — never an
   average, never the first.
3. **Preserve every `source_quote`.** The merged finding keeps the code evidence (redacted if it contains a secret).
   A finding that loses its quote in the merge is no longer verifiable — keep it.
4. **Re-derive severity centrally.** Do **not** trust a reader's optimistic self-rating. Re-rate each finding against
   the ladder below, factoring the system's **data sensitivity** (from `architecture-constraints.md`) — the same
   IDOR is higher on confidential data than on public data.

## The severity ladder (CVSS labels; EPSS/KEV only where a real CVE exists)

Per-finding severity uses the standard **CVSS vocabulary — Critical / High / Medium / Low.** CVSS-alone is deprecated
for *prioritization*, so where a finding is a **known-CVE dependency**, attach an **EPSS** (30-day exploit
probability) or **CISA KEV** (known-exploited) note; for a code-level finding (IDOR, XSS, hardcoded secret) there is
no CVE, so use the CVSS label alone.

- **Critical** — trivially exploitable + high impact: an auth bypass, RCE, a live production credential exposed, a
  full-data-export path. Usually **architectural** or a live secret.
- **High** — a real, exploitable vulnerability with a bounded blast radius, **fixable in code**: an IDOR behind auth,
  a reflected XSS, an unrestricted SSRF, a hardcoded non-production secret, an unverified/floating dependency.
- **Medium** — exploitable only under specific conditions, or defense-in-depth: a missing security header, verbose
  errors, weak-but-not-broken config.
- **Low** — hardening / best-practice: a longer session timeout, an informational disclosure with no direct impact.

## The risk matrix (for the client-facing summary)

Independently of the per-finding severity, build the communication matrix — this is what a stakeholder reads:

| # | Threat | Likelihood | Impact | Existing controls | Residual risk | Priority |
|---|--------|-----------|--------|-------------------|---------------|----------|

**Likelihood × Impact → Residual** (factoring existing controls), then **Priority** P1 (critical) / P2 (important) /
P3 (monitor). The matrix is for *communication*; the **verdict keys off the per-finding severity**, not the P-count.

## The completeness lens — the ASVS 5.0 bar (H1) + the design's threat pass (D6)

**The bar is ASVS 5.0, not the Top 10.** OWASP positions the Top 10 as an *awareness* document and **ASVS as the
verification standard** — for a seat whose verb is *verify*, completeness is measured against **ASVS 5.0 chapters
V1–V14** (via their CWE tags), scoped to the declared **`asvs_level`** (`architecture-constraints.md` →
`- **ASVS target level:**`; **default L1**, the realistic solo bar; absent ⇒ L1; **L2 only with a recorded
justification**, a Tier-2 decision). The report's completeness section is the **ASVS chapter-coverage table** — per
chapter: verified / partial / N-A + an evidence pointer (a test · a scanner · reader judgment). The reader partition
(Top-10 / ASI areas) still *divides the work*; ASVS *measures* it. The ~58% test-automatable / ~10% scanner / ~30%
judgment-only split makes the fresh panel's manual remit exactly the judgment band (business logic, authz
consistency, architectural intent).

**Fold in the design's threat pass (D6).** 03's `system.md` **§ Threats considered** walked the C4 trust boundaries at
design time. **Cross-reference it against this audit** — it converts an expensive BLOCK-on-architecture into a cheap
design-time catch:

- **A designed threat with no verifying check is a GAP.** For each threat the design named, point at the audit
  check/finding that covers it. A threat with nothing covering it is a coverage gap — record it, and (if the control
  was never built) route it to `/03-architect` as an architectural finding.
- **A finding in a zone the design called "safe" is design feedback.** If the audit finds a real defect where the
  design's threat pass claimed no threat, the **threat model missed it** — route it back to `/03-architect` (the
  design owner), not only `/04` (the code owner). Fixing the code without fixing the map leaves the next slice exposed.

Record the cross-reference in the report's completeness section (the **`Design-time threats × coverage`** table).
Where the design did **no** threat pass, say so — that absence is itself a finding to route to `/03`. The ASVS
chapter coverage and the threat cross-reference are **one lens**: each designed threat maps to the ASVS chapter that
verifies it, and each ASVS chapter marked `partial`/`N-A` is an honest statement of what the audit did and did not
reach at the declared level.

## The verdict (severity-keyed, routed)

| Verdict | Condition | Route each finding to | `06` G6 |
|---------|-----------|-----------------------|---------|
| **PASS** | zero Critical, zero High; any Medium/Low carry a remediation route or a documented residual-risk acceptance | — (ship) | **pass** |
| **REMEDIATE** | ≥1 High (or an unaddressed Medium cluster), **code-fixable without an architecture change** | `/04-builder` → re-audit | **fail (blocks)** |
| **BLOCK** | ≥1 Critical, **or** a High needing an architecture change, **or** a missing security *declaration* | `/03-architect` / `/00-discovery` | **fail (blocks)** |

**The REMEDIATE↔BLOCK line is "can code fix this in place?"** — an IDOR (add the ownership check), an XSS (escape the
output), a hardcoded secret (move to env + rotate), an SSRF (allowlist the host) are **REMEDIATE → /04**. A **broken
trust boundary** (identity/authorization taken from client-supplied fields; no server-side authz layer), an insecure
datastore *design*, or a control the spine **never required** are **BLOCK** — the fix is a *design* change (→ `/03`)
or a *declaration* change (→ `/00`), not a patch. **A Critical is always BLOCK.**

### Routing (07 classifies + escalates; it appends no amendment row)

- **code-fixable defect** → `/04-builder` (the fix), then a fresh `/07-security sprint N` re-audit.
- **architectural defect** → `/03-architect` (a wrong trust boundary, an insecure design) — record it as an
  architecture finding the architect reconciles; `07` writes no ADR and no amendment.
- **missing security *declaration*** (a control the product *should* require but the spine never stated) → `/00-discovery`
  as a **pending** concern for the user to decide — a spine-tier gap is the user's call, per `shared/spine-boundary.md`.
  `07` **routes** it; it never edits `docs/spec/**` or appends an `amendment-log.json` row (`07` *consumes* the
  amendment protocol to classify, it is not an appender).

## Re-audit — a finding closes only with proof of fix (H2)

07 routes a REMEDIATE finding to `/04`, but **routing is not closure.** A finding closes **only at re-audit**, and
only when the fix carries a **failing→passing regression test that BITES ON REVERT** — the 08 oracle-bites mechanic:
revert the fix and the test must go **red** (a test that stays green when the fix is undone proves nothing). For an
**agentic** finding, the biting case is an **ASR-gated red-team case** (H3), not a unit test.

- **The re-audit report gains a per-finding `proof_of_fix` column** — the regression test **plus** the captured
  revert-check (`git revert <fix> && <test cmd>` → RED; restore → GREEN). A finding whose `proof_of_fix` is absent,
  `none`, or a test that does **not** bite on revert **stays open**: the verdict remains REMEDIATE, never flips to
  PASS on an unproven remediation.
- **Enforcement belongs to the re-auditor, not the fixer** (segregation of duties, again): 04 *ships* the regression
  test (its TDD-for-bugs, `04/references/build-discipline.md`), but 07's **fresh** re-audit *verifies* it exists and
  bites. A "fixed" claim without a biting proof is treated as unremediated — the same rubber-stamp the verdict guard
  exists to catch.

## VERDICT HONESTY (the hard gate)

- **PASS is unreachable while any in-scope Critical or High is unremediated.** A rubber-stamp "PASS with
  recommendations" over a real High **false-proceeds `06` G6** — the exact lie `05` exists to catch, one seat over.
- **REMEDIATE is not "PASS with notes."** If the tally carries a High, the verdict is REMEDIATE or BLOCK, full stop.
- **Every finding carries a `file:line` + a `source_quote` + a traced source→sink.** No evidence ⇒ it is an
  inference the audit *flags for confirmation*, not a finding it asserts (false-positive control — the panel's whole
  point).
- **Never reproduce a secret VALUE.** Quote the offending line with the value **redacted** (`API_TOKEN =
  "sk-live-…[REDACTED]"`); record env-var **names** only, everywhere.
- The session summary **leads with the verdict + the severity tally**. If it says PASS while the tally shows a High,
  it is self-contradictory — rewrite before emitting.

## The client-facing summary (honest about limits)

Plain-language, stakeholder-readable — the framing:

- **What is secured** — the controls in place, in client-friendly terms.
- **What residual risks remain** — honestly, including what the audit *cannot* control.
- **Recommendations** — immediate (P1) / short-term (P2) / long-term (P3).
- **Third-party pen test** — an **AI-assisted audit is not a substitute for third-party penetration testing.** State
  this in **every** summary; recommend a third-party test more strongly as **data sensitivity** rises (medium/high →
  strongly recommended before a public launch).
- **Out of scope, said plainly** — **live-infrastructure hardening** (TLS termination, network policy, OS patching,
  running-server config) cannot be evidenced from the repo; name it as out of scope and route it to the deployment
  owner, rather than pretending a code audit covered it.
