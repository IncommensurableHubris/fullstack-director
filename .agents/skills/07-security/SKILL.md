---
name: 07-security
description: "Audit the built system for vulnerabilities - a bounded parallel READ-ONLY OWASP panel + a sequential synthesizer emitting a severity-keyed PASS / REMEDIATE / BLOCK verdict. Spawns four blind read-only readers across a fixed OWASP partition, plus a conditional 5th for LLM/agentic parts; the synthesizer de-dupes, takes MAX severity, builds the matrix. PASS: zero Critical/High. REMEDIATE: a code-fixable High to /04-builder. BLOCK: a Critical, an arch-level High to /03-architect, or missing declaration to /00. A non-amender: classifies, escalates, appends no amendment-log row; never edits code. Use when the user says 'security audit', 'OWASP check', or 'pen test'. Writes docs/security/security-audit-sprint-NN.md (or -full.md); appends security-guardrails.md; never writes src/** or docs/{spec,architecture,design,quality}/**. Do NOT build or fix code - /04-builder. Do NOT re-architect - /03-architect. Do NOT verify - /05-reviewer. Do NOT deploy - /06-release. Do NOT refactor - /08-refactor."
---

# 07 · Security — secure

Two modes. **`07-security sprint N`** audits one sprint's surface (post-ship or pre-ship of that slice);
**`07-security full`** audits the whole codebase (pre-release / periodic). `07` is the **deep security pass**: a
**bounded parallel read-only OWASP panel** whose findings a **single sequential synthesizer** reduces into
`docs/security/security-audit-sprint-NN.md` with a machine-readable **PASS / REMEDIATE / BLOCK** verdict that
`06-release`'s **G6** gates the ship on. Your graded value is **not** "finds vulnerabilities" — a strong reviewer
does that too (and cries wolf 68–97% of the time). It is the **isolated, de-duplicated, false-positive-controlled,
machine-verdicted audit** a release gate can trust: a *complete* OWASP partition (no area silently dropped), each
finding carrying a `source_quote` + a re-derived severity, read-only (the audit touched no code), routed to the
owning skill.

## Operating principle — partition completely, read blind, synthesize sequentially, verdict on severity

- **Panel — bounded, parallel, read-only, blind.** A **fixed complete partition** of the OWASP areas across **4
  readers** (+ a conditional **5th** for LLM/agentic), each seeded with **only** its area-slice + the code paths + a
  **neutral, evidence-required** prompt. Leading "find the vulnerability here" framing inflates false positives;
  neutral "analyze this code; cite `file:line` + the tainted source" is what controls them. Each reader is **blind**
  to the others and **writes no code**. Cap 3–5 (`shared/subagent-protocol.md`). Isolation is real **only** because
  the spawner is fresh.
- **Deterministic scanners under the panel.** Where a runtime exists, run `npm audit` / `osv-scanner`, `gitleaks`,
  `semgrep` and feed results to the owning reader — the AI panel *complements* deterministic tools (it catches IDOR,
  authz gaps, business logic they miss). Their absence is **recorded**, never silently skipped.
- **Synthesizer — one sequential reduce, never parallel.** De-dupe by target, take **max severity**, **preserve
  every `source_quote`**, build the risk matrix, and run the **completeness lens** ("which area returned zero
  findings — clean, or under-looked?"). A parallel merge would re-amplify error.
- **Verdict on severity, routed; honest about limits.** PASS / REMEDIATE / BLOCK keyed to Critical/High presence
  (below), each finding routed to its owning skill. An AI audit is **not** a substitute for third-party penetration
  testing, and **live-infrastructure** hardening is out of the repo audit's reach — say both, don't pretend otherwise.

## The flow — five steps (craft lives in the references; load each as its step begins)

1. **SEED.** Read the audit context: `docs/architecture/system.md` (trust boundaries · tech stack · **whether any
   LLM/agent component exists** → gates R5), `docs/spec/architecture-constraints.md` (data sensitivity · compliance),
   `docs/spec/**` (the in-scope REQ blocks — an access-control REQ makes an IDOR a *declared* gap), `05`'s
   `qa-report-sprint-NN.md` (to **not** re-audit correctness; pick up data sensitivity), `06`'s `deployment-config.md`
   if present (config-level surface), any prior `docs/security/` audits (`full` / re-audit). **Pin `audited_commit`
   = HEAD.** Decide the panel: the fixed 4 readers + R5 iff AI components exist. `references/owasp-panel.md` (§SEED).
2. **PANEL (parallel, read-only, blind).** Spawn the readers per `references/owasp-panel.md`. Each gets **only** its
   area-slice remit + the code paths + the neutral evidence-required prompt; runs the deterministic scanners for its
   area where available; returns findings (`file:line` + `source_quote` + `proposed_severity` + OWASP area), blind to
   the others. **No reader edits code.** Skip R5 unless `system.md` names LLM/agent components
   (`references/llm-agentic-module.md`).
3. **SYNTHESIZE (sequential reduce).** De-dupe by target (the same vuln seen by two readers → **one** finding), take
   **max severity**, **preserve each `source_quote`**. Re-derive severity centrally (CVSS Critical/High/Medium/Low;
   an EPSS/KEV note only where a real CVE exists). Build the **risk matrix** + run the **completeness lens** (every
   OWASP area PASS/FAIL/N/A with a reason — a bare N/A is a gap, not a pass). `references/synthesis-and-verdict.md`.
4. **VERDICT + ROUTE.** Severity-keyed **PASS / REMEDIATE / BLOCK** (table below). Route **each** finding: a
   code-fixable defect → `/04-builder`; an architectural defect (broken trust boundary, insecure datastore design) →
   `/03-architect`; a **missing security declaration** (a needed control the spine never required) → `/00-discovery`.
   `07` **classifies + escalates**; it appends **no** amendment row (`shared/spec-amendment-protocol.md`).
5. **REPORT + LEARN.** Write `docs/security/security-audit-sprint-NN.md` (`templates/security-audit.md`): machine
   frontmatter (verdict + severity tally + `owasp_edition` + `audited_commit` + `panel_readers` + `llm_module`) +
   the panel manifest (readers · slices · **read-only attestation**) + the OWASP checklist + the Findings table +
   the risk matrix + the client-facing summary (secured / residual / recommendations / **third-party pen-test**) +
   the next command. Append `.claude/rules/security-guardrails.md` for any recurring class. The session summary
   **leads with the verdict + the severity tally**, never narrative.

## The panel (fixed complete partition; R5 conditional)

| Reader | OWASP areas owned (2021 spine · 2025 augment) | Core checks |
|--------|-----------------------------------------------|-------------|
| **R1 · Access & Authn** | A01 Broken Access Control · A07 Auth Failures · A04 Insecure Design (abuse) | authz on every endpoint · IDOR/ownership · session mgmt · CORS · rate-limiting |
| **R2 · Injection & Forgery** | A03 Injection · A10 SSRF *(A01 in 2025)* · improper output handling | SQLi/XSS/command injection · output encoding · SSRF allowlist · private-IP block |
| **R3 · Secrets, Crypto & Config** | A02 Cryptographic Failures · A05 Security Misconfiguration · A10:2025 Exceptional Conditions | hardcoded secrets · weak crypto · TLS/HSTS · security headers · generic errors / fail-closed |
| **R4 · Supply Chain, Integrity & Observability** | A06 + **A03:2025 Software Supply Chain** · A08 Integrity · A09 Logging/Alerting | dep audit · **slopsquat / hallucinated-dep verification** · lockfile pinning · CI/integrity · auth-event logging |
| **R5 · LLM/Agentic** *(conditional)* | OWASP LLM Top 10 (2025) + Agentic Top 10 (ASI 2026) | prompt-injection boundary · excessive agency · output→sink · tool-arg validation · model provenance |

**R5 gating:** load `references/llm-agentic-module.md` **only** when `system.md` (or deps/config) names LLM / RAG /
agent / MCP / vector-DB components. For a pure-domain codebase, **skip it entirely** — never invent AI findings
where there are no AI components. Panel size = **4** normally, **5** with AI components (both within the 3–5 cap).

**Profile flip — `agent-system` inverts the partition.** Read the spine's `Profile` (`shared/agentic-profile.md`).
Under `agent-system` the AI **is** the attack surface, so the panel **flips** — load `references/agentic-panel.md`
instead of the classic partition above: the four primary readers become agentic (**R1 injection & goal hijack** +
the **spine-poisoning lens** · **R2 tool misuse & code execution** · **R3 identity, memory & secrets** · **R4 agentic
supply chain**), and **classic-web** becomes the **conditional R5** (loaded iff the system exposes a web surface).
Doctrine: **structural defenses, not predictive ones** — a finding whose only fix is "detect the injection with more
AI" is incomplete. Under `agent-system` the panel also runs the **dynamic adversarial arm** (`agentic-panel.md` §
Dynamic arm): fire the security suites under `docs/spec/evals/security/**` at a running agent, gate on
**attack-success-rate (ASR)** — and **PASS requires the arm to have executed OR an explicit user-gated waiver**. 07 is
the sole executor of those suites (05 carves them out).

## The verdict (severity-keyed, not count-keyed)

| Verdict | Condition | Routes to | `06` G6 |
|---------|-----------|-----------|---------|
| **PASS** | zero Critical, zero High; any Medium/Low carry a remediation route or documented residual-risk acceptance | ship / next sprint | **pass** |
| **REMEDIATE** | ≥1 High (or an unaddressed Medium cluster), **code-fixable without an architecture change** | `/04-builder` → re-audit `/07-security sprint N` | **fail (blocks)** |
| **BLOCK** | ≥1 Critical, **or** a High needing an architecture change, **or** a missing security *declaration* | `/03-architect` (arch) or `/00-discovery` (declaration) | **fail (blocks)** |

**Under `agent-system`, PASS additionally requires the dynamic adversarial arm to have executed** (every ASR ≤ its
floor) **or a user-gated waiver recorded** — arm-unexecuted + no-waiver ⇒ REMEDIATE. The agent-profile verdict table +
the ASR floors live in `agentic-panel.md` § Dynamic arm.

>>> VERDICT HONESTY (hard): **PASS is unreachable while any in-scope Critical or High finding is unremediated.**
Severity is **re-derived centrally** — never trust a reader's optimistic self-rating. **REMEDIATE is not "PASS with
recommendations":** a real High stamped PASS false-proceeds `06` G6 — the same lie `05` exists to catch. Every
finding carries a `file:line` + a `source_quote`; a behavior claim without one is an inference, not a finding.
**Never reproduce a secret VALUE** in the report — quote the offending line with the value **redacted**; record
env-var **names** only. The session summary **leads with the verdict + tally**; if it says PASS while the tally
carries a High, it is inconsistent — fix it before emitting. <<<

## Write-path (read-only — 07 never edits the code it audits)

- **Write** `docs/security/security-audit-sprint-NN.md` (or `-full.md`) — **always**, including a BLOCK; **append**
  `.claude/rules/security-guardrails.md` (a recurring class → a durable pre-audit check).
- **Never write** `src/**` (a real vuln is a **finding routed to `/04`/`/03`/`/00`**, not an edit), `docs/spec/**`
  (the spine), `docs/architecture/**`, `docs/design/**`, or `docs/quality/**` (realizations `07` only reads).
- **Never an amendment row** — `07` is a non-amender: a spine-tier finding (a missing security requirement) is
  **routed** to `/00`, not resolved (`shared/spec-amendment-protocol.md` — `07` *consumes* the protocol to classify).
- **Never a secret value** — env-var **names** only, in every artifact and every quoted line.
- **Reference, never copy.** The report cites `REQ-NNN` / `ADR-NNN`; it never pastes requirement prose
  (`shared/spine-boundary.md`).

## Progress checklist (copy this and track as you go)

- [ ] SEED — system.md (trust boundaries + **AI-components? → R5 gate**) · constraints (data sensitivity) · in-scope
      REQ blocks · 05's qa-report (don't re-audit) · deployment-config (if present); `audited_commit` pinned
- [ ] PANEL — 4 readers spawned **read-only + blind**, each its own area-slice + **neutral evidence-required** prompt;
      deterministic scanners run where available (absence recorded); R5 only if AI components exist
- [ ] SYNTHESIZE — de-dupe by target · max severity · **source_quotes preserved** · risk matrix · completeness lens
      (every OWASP area PASS/FAIL/N/A with a reason)
- [ ] VERDICT + ROUTE — severity-keyed PASS/REMEDIATE/BLOCK; severity **re-derived centrally**; each finding routed
      (code→/04 · arch→/03 · declaration→/00); **VERDICT HONESTY held** (no PASS over an unremediated High)
- [ ] REPORT — machine frontmatter (verdict + tally + owasp_edition + audited_commit + panel_readers + llm_module) ·
      panel manifest + **read-only attestation** · OWASP checklist · Findings (file:line + source_quote) · risk
      matrix · client summary + **third-party pen-test** honesty · next command
- [ ] Integrity: **no `src/**` / spine / realization edit**; **no amendment row**; **no secret value** anywhere;
      LLM module gated correctly; session summary leads with verdict + tally

## Reads / Writes

**Reads:** `docs/architecture/system.md` (trust boundaries · stack · AI-components) · `docs/spec/architecture-
constraints.md` (data sensitivity · compliance) · `docs/spec/**` (in-scope REQ blocks — read-only) ·
`docs/quality/qa-report-sprint-NN.md` (avoid re-auditing correctness) · `docs/release/deployment-config.md` (if
present) · `src/**` (the audit target, at HEAD) · `docs/security/**` (prior audits; `full` / re-audit) ·
`.claude/rules/security-guardrails.md` (if present) · git state.
**Writes:** `docs/security/security-audit-sprint-NN.md` (or `-full.md`) · **appends**
`.claude/rules/security-guardrails.md`. **Never** `src/**`, `docs/spec/**`, `docs/architecture/**`,
`docs/design/**`, or `docs/quality/**`.

## References (load when the step needs them)

- `references/owasp-panel.md` — the panel contract: the fixed 4+1 reader partition + each reader's area-slice + the
  **neutral evidence-required prompt** + the read-only rule + the deterministic-scanner layer + the completeness lens.
- `references/synthesis-and-verdict.md` — the sequential reduce (de-dupe by target · max severity · preserve quotes) +
  the risk matrix + the CVSS+EPSS/KEV severity ladder + the PASS/REMEDIATE/BLOCK thresholds + routing + the
  client-facing summary + the third-party-pen-test honesty.
- `references/llm-agentic-module.md` — **conditional**, gated: the R5 checks on the OWASP LLM Top 10 (2025) + the
  Agentic Top 10 (ASI 2026); load **only** if `system.md` names LLM/agent components, else skip entirely.
- `references/agentic-panel.md` — **`Profile: agent-system` only**: the FLIPPED partition (R1–R4 agentic-primary +
  the spine-poisoning lens + conditional classic-web R5) + the structural-defenses doctrine + the **dynamic
  adversarial arm** (ASR-gated, the security suites under `docs/spec/evals/security/**`, the PASS precondition + the
  waiver, and the agent-profile verdict table). Replaces the classic partition. Repo-root-relative shared
  toggle: `shared/agentic-profile.md`.
- `references/owasp-remediation.md` — remediation patterns per OWASP area (2021 + 2025), incl. slopsquat verification.
- `shared/subagent-protocol.md` — the parallel-readers + sequential-synthesizer contract (cap 3–5, blind readers, the
  synthesizer never parallel); repo-root-relative.
- `shared/spec-amendment-protocol.md` — the tiers `07` *classifies* against when escalating (you append no row);
  repo-root-relative.
- `shared/spine-boundary.md` — declaration vs realization (why a missing security *requirement* routes to `/00`);
  repo-root-relative.

## Next skill

- **PASS** → `/06-release sprint N` (G6 will pass) · the next sprint · `/00-discovery reflect`.
- **REMEDIATE** → `/04-builder sprint N` (fix each routed finding), then a fresh `/07-security sprint N` re-audit.
- **BLOCK** → the routed owner: an architectural defect → `/03-architect`; a missing security declaration →
  `/00-discovery`; then re-audit.
