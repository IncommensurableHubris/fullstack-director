# OWASP Remediation Patterns (2021 spine + 2025 augment)

> Load when writing a finding's **Remediation** column or the client summary. Quick-reference fixes per OWASP area,
> mapped to the panel's readers. **Audit against 2021 as the stable spine; augment with 2025's two new areas** (A03
> Software Supply Chain, A10 Mishandling of Exceptional Conditions) — record `owasp_edition: "2021+2025"`.

## R1 · Access & Authn

**A01 Broken Access Control** (incl. **SSRF in 2025**) — common: missing authz on an endpoint; **IDOR** (change an id
→ another user's data); CORS `*` with credentials.
→ Deny-by-default authz middleware on every protected route; validate resource ownership server-side
(`WHERE user_id = $verifiedUser`); prefer UUIDs over sequential ids; whitelist CORS origins.
**A07 Authentication Failures** — no brute-force protection; tokens in URLs; weak sessions.
→ Rate-limit + lockout on login; `HttpOnly; Secure; SameSite=Strict` cookies; idle + absolute session expiry;
invalidate on logout/password-change; use an established auth library, never a hand-rolled one.
**A04 Insecure Design** — no rate limiting; business-logic abuse.
→ Server-side business rules (never client-trusted); rate limits + anti-automation on public forms.

## R2 · Injection & Forgery

**A03 Injection** — SQL via concatenation; **XSS** via unescaped output; command injection.
→ **SQL:** parameterized queries / ORM — never concatenate. **XSS:** framework auto-escaping (JSX, template engines);
for raw HTML, a sanitizer (DOMPurify); set correct `Content-Type`. **Command:** avoid `exec`/`system` with user
input; if unavoidable, an **allowlist** not a blocklist. Treat all input as untrusted at every sink.
**A10 SSRF** (2021) — server fetches a user-supplied URL.
→ Allowlist schemes (`https`) + hosts; **block private IP ranges** (`10.x`, `172.16-31.x`, `192.168.x`, `127.x`,
`169.254.x`) and cloud metadata (`169.254.169.254`); resolve DNS then verify the IP is external; use a client with
timeouts + redirect limits.

## R3 · Secrets, Crypto & Config

**A02 Cryptographic Failures** — plaintext/weak-hash passwords (MD5/SHA1); **hardcoded secrets**; HTTP for sensitive
ops.
→ argon2/scrypt/bcrypt (cost ≥ 10) for passwords; secrets from **environment variables**, never source; **if a real
secret was committed, rotate it first** — history-scrubbing does not invalidate an exposed credential; TLS 1.2+ only,
HSTS; encrypt sensitive data at rest.
**A05 Security Misconfiguration** — stack traces in prod; default creds; missing headers.
→ Generic prod errors (log details server-side only); change all default creds; set `Content-Security-Policy`,
`X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`; run as non-root.
**A10:2025 Mishandling of Exceptional Conditions** — failing **open** on error; leaking internals in an error path.
→ Fail **closed** (an error denies, never grants); generic error responses; test the error paths, not just the happy
path.

## R4 · Supply Chain, Integrity & Observability

**A06 Vulnerable Components + A03:2025 Software Supply Chain** — known-CVE deps; **outdated**; unused deps widen the
surface. And the whole build/distribute/update process (2025 broadened the scope).
→ Run `npm audit` / `pip-audit` / `osv-scanner` before every ship; automate updates (Dependabot/Renovate); remove
unused deps; **pin versions + commit a lockfile**; verify checksums.

> **Slopsquatting (AI-specific supply-chain risk — first-class in 2026).** AI suggests **non-existent** package names
> ~**20%** of the time (open-source models ~22%, commercial ~5%), and ~**43%** of the hallucinated names **recur on
> every re-run** — so attackers pre-register them with malicious code. For **every** AI-suggested or unfamiliar
> dependency: **verify it exists on the registry** (`npm info <pkg>` / `pip show <pkg>`); check download counts + repo
> activity + maintainer reputation + **creation date** (a recently-created package mimicking established functionality
> is suspect); watch for **typosquats** (subtle misspellings of canonical names); pin the exact version.

**A08 Integrity Failures** — unsigned/unverified deps; unvalidated deserialization; insecure CI.
→ Lockfiles + checksum verification; review dependency changes in PRs; validate/sanitize deserialized input; sign
commits + verify in CI.
**A09 Logging & Alerting Failures** — auth events unlogged; **secrets/PII in logs**; no alerting.
→ Log login success/failure, logout, password-change, and 403s; **never** log passwords/tokens/full card numbers —
redact; alert on N failed logins from an IP, privilege-escalation attempts, unusual usage; retain logs off-server.

## R5 · LLM / Agentic (only if applicable)

See `llm-agentic-module.md`. Core patterns: separate system prompts from user input (never concatenate raw);
least-privilege tool scoping + human approval on destructive actions; **validate model output before any sink**
(SQL/shell/HTML/downstream request); redact PII/secrets from prompts + RAG context; pin + verify model/plugin
provenance.
