# The OWASP Panel — bounded, parallel, read-only, blind

> Load at SEED + PANEL. This instantiates `shared/subagent-protocol.md` § "parallel readers + synthesizer" for the
> security audit: a **fixed complete partition** of the OWASP Top 10 across **4 read-only readers** (+ a conditional
> 5th), each **blind** to the others, each returning `finding + source_quote + proposed_severity`. The synthesizer
> (a single sequential reduce) lives in `synthesis-and-verdict.md`. **Isolation is real only because the spawner is
> fresh** — the panel cannot self-prefer a build it never saw being written.

## Why a panel (not a single pass), and why blind

Splitting a security review across focused agents measurably lifts recall over one monolithic pass (mid-2026
research: a Detector/Locator/Repairer split reports **+18.7% detection F1 / +27.8% location precision**; focused
agents beat both single-pass LLMs and pattern SAST on recall). But a **parallel merge** re-amplifies error — so the
readers run parallel and **blind**, and the *synthesis* is a **single sequential reduce**. Each reader owning a fixed
slice guarantees **complete coverage**: no OWASP area is silently dropped because "someone else probably looked."

## The fixed partition (breadth fixed, depth risk-adaptive)

Every OWASP area is owned by **exactly one** reader. Within its slice, a reader **prioritizes by the system's real
risk surface** (from `system.md`'s trust boundaries) — fixed breadth, adaptive depth. Same partition in `sprint` and
`full` mode; the mode changes **which code each reader reads** (the sprint's changed surface vs the whole tree), not
the areas covered.

> **Partition vs bar (H1).** These readers **partition by the OWASP Top 10** — an *awareness* artifact that divides
> the work cleanly and completely. But the audit's **completeness is measured against ASVS 5.0 (V1–V14)**, the
> *verification standard* — OWASP itself positions the Top 10 as awareness and ASVS as verification. Two different
> axes: work-division (here) vs the verification bar (the synthesizer's completeness lens in
> `synthesis-and-verdict.md`). A reader owns its Top-10 slice; the synthesizer maps the findings onto ASVS chapters,
> scoped to the declared `asvs_level`.

- **R1 · Access & Authn** — A01 Broken Access Control · A07 Authentication Failures · A04 Insecure Design (abuse).
  Authorization on **every** protected endpoint; **IDOR / ownership** (can a user reach another user's or team's
  resource by changing an id?); session management (secure/expiry/invalidation); CORS; rate-limiting / anti-automation.
- **R2 · Injection & Forgery** — A03 Injection · A10 SSRF *(folded into A01 under 2025)* · improper output handling.
  SQL/NoSQL/command injection; **XSS** (reflected/stored/DOM); output encoding at every sink; **SSRF** (user-influenced
  outbound URLs — allowlist hosts, block private-IP ranges + cloud metadata).
- **R3 · Secrets, Crypto & Config** — A02 Cryptographic Failures · A05 Security Misconfiguration · A10:2025 Mishandling
  of Exceptional Conditions. **Hardcoded secrets** in source; weak/again-outdated crypto & password hashing; TLS/HSTS
  declarations; security headers (CSP, X-Frame-Options, X-Content-Type-Options); **generic errors / fail-closed** (no
  stack-trace or internal-detail leakage); default creds.
- **R4 · Supply Chain, Integrity & Observability** — A06 Vulnerable Components **+ A03:2025 Software Supply Chain** ·
  A08 Integrity · A09 Logging/Alerting. Dependency audit; **slopsquat / hallucinated-dependency verification** (AI
  suggests non-existent packages ~20% of the time — verify every dep exists on the registry, check for typosquats,
  pin versions + commit a lockfile); CI/update integrity; auth-event logging; **no secrets in logs**.
- **R5 · LLM/Agentic** *(conditional)* — the OWASP LLM Top 10 (2025) + Agentic Top 10 (ASI 2026). **Gated:** load
  `llm-agentic-module.md` **only** when `system.md` (or deps/config) names LLM / RAG / agent / MCP / vector-DB
  components; otherwise **skip R5 entirely** and record `llm_module: absent`.

## The reader's seed + the neutral, evidence-required prompt

Seed each reader with **only**: its area-slice remit (the row above), the **code paths** to read, the trust-boundary
context from `system.md`, and the data-sensitivity from `architecture-constraints.md`. **Never** the other readers'
findings; **never** this orchestrating conversation.

**Prompt neutrally — this is not optional craft, it is false-positive control.** Mid-2026 research: telling a model
"find the vulnerability here" barely changes its false-positive rate, but a leading frame collapses precision, and
LLM reviewers already run **68–97% false-positive on already-patched code**. So:

- **Neutral framing:** "Analyze the following code for `<area>` weaknesses. Report only what you can evidence." —
  **not** "find the security bug in this vulnerable code."
- **Evidence bar:** every finding **must** carry a `file:line` **and** a `source_quote` (the offending line) **and**
  the **tainted-source trace** (where untrusted input enters → the dangerous sink). A finding without a traced
  source is an inference, not a finding — the reader marks it "needs confirmation," it does not assert it.
- **Self-negation pass:** before returning a finding, the reader asks "is there a guard I missed that makes this
  safe?" (an upstream authz check, an escaping call, an allowlist). This is the single biggest FP reducer.
- **No quota:** a reader that finds nothing in its slice returns **zero** findings — that is a valid, valuable result,
  not a failure to try. Inventing a finding to look thorough is the crying-wolf failure the verdict guard penalizes.

Each reader returns rows of: `severity(proposed) · OWASP area · file:line · source_quote · why (the traced sink)`.

## The deterministic-scanner layer (AI complements, never replaces)

Where a runtime/toolchain exists, **run the deterministic scanners and feed their output to the owning reader** — the
AI panel *layers on top*, it does not replace them:

- **R4:** `npm audit` / `pip-audit` / `osv-scanner` (known-CVE dependencies) · a lockfile presence + pin check.
- **R3:** `gitleaks` / `trufflehog` (committed secrets) across the tree **and git history**.
- **any:** `semgrep` / CodeQL rulesets for the language, routed to the matching reader.
- **DAST (optional):** a **ZAP-baseline** scan against a staging URL where one exists — correctly *optional* for solo
  (the priority order is SCA → SAST/secrets → DAST); **recorded-if-absent** like every scanner, never a hard gate.

**Record what ran and what didn't** in the report's `scanners:` field. A scanner that could not run (no network, no
toolchain) is **recorded as not-run**, never silently treated as "clean." Deterministic coverage is auditable and
exhaustive; the AI catches what patterns miss (IDOR, business-logic, authz gaps) — the two are complementary.

## SEED specifics (what the audit reads before spawning)

- `system.md` — trust boundaries (each is a reader's first stop) · the tech stack (which scanners apply) · **whether
  any LLM/agent component exists** (the R5 gate).
- `architecture-constraints.md` — **data sensitivity** (drives the third-party-pen-test recommendation and the
  Likelihood×Impact of the risk matrix) · compliance (EU residency, etc.) · the **`ASVS target level`** (default L1,
  absent ⇒ L1) — the bar the completeness lens scopes its chapter coverage to.
- the in-scope `docs/spec/**` REQ blocks — a declared control (e.g. "a member reads only their own team's data")
  turns a missing check into a **declared** gap, not a matter of taste.
- `05`'s `qa-report-sprint-NN.md` — a SHIP there means "does what the spine says," **not** "is secure"; read it to
  **avoid re-auditing correctness**, and to pick up the data sensitivity. `07` does not re-run `05`'s oracles.
- `06`'s `deployment-config.md` (if present) — config-level surface (security headers, TLS-enforcement declarations,
  env-var hygiene).
- **Pin `audited_commit` = HEAD** — the staleness anchor recorded in the report (if code drifts after the audit, the
  verdict no longer describes it).

## The completeness lens (before the verdict) — anchored on ASVS 5.0

After synthesis, sweep completeness against the **ASVS 5.0 chapters (V1–V14)** scoped to the declared `asvs_level`
(the full craft + the chapter-coverage table live in `synthesis-and-verdict.md`): per chapter **verified / partial /
N-A — each with a reason.** A **bare N-A is a gap**, not a pass ("V10 OAuth: N-A because there is no OAuth surface").
"Which chapter is `partial` because the code is clean, or because the reader didn't look hard enough?" Re-examine the
highest-risk paths (auth, data access, outbound requests) once more. This is the audit's own anti-false-negative
pass; it is what makes a PASS mean "audited to the bar and clean," not "nobody looked."
