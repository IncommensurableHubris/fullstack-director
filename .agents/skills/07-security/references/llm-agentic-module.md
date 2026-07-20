# R5 — LLM / Agentic security (conditional module)

> **Gated.** Load this **only** if `system.md` (or the dependencies / config) names an **LLM, RAG, embedding /
> vector-store, agent, or MCP** component. For a pure-domain codebase, **skip it entirely** and record
> `llm_module: absent` — never invent AI-security findings where there are no AI components (the `05`
> `llm-review.md` precedent). When it applies, R5 is the panel's **5th reader**, blind and read-only like the rest;
> its findings route and are severity-rated exactly like every other finding.

## Why AI components need their own reader

LLM/agentic risks have **no analogue** in a non-AI codebase — prompt injection, excessive agency, and memory
poisoning are not variants of the classic Top 10, they are their own attack surface. OWASP maintains them as a
separate project (the GenAI Security Project), with two current, live-verified taxonomies:

- **OWASP Top 10 for LLM Applications — 2025** (LLM01–LLM10).
- **OWASP Top 10 for Agentic Applications — 2026** (ASI01–ASI10) — layered *on top of* the LLM Top 10; load its
  checks when the system has **tool-calling, memory, or multi-agent orchestration**.

## Detecting the surface (the gate)

Trigger R5 when any of these appear in `system.md` / `package.json` / config: an LLM SDK or API client (Anthropic,
OpenAI, etc.), an embeddings / vector-DB dependency, an agent framework, an **MCP** server/client, a model registry
pull (Hugging Face, etc.), or a prompt-template / RAG-pipeline module. Absent all of these → **skip R5**.

## LLM Top 10 (2025) — the checks

- **LLM01 Prompt Injection** — trace **every** path where untrusted content (user input, retrieved docs, tool/web
  output, files) reaches a prompt. Is it structurally **separated** from instructions, or concatenated raw into the
  system prompt? Treat *all* retrieved/tool content as untrusted (indirect injection).
- **LLM02 Sensitive Information Disclosure** — grep for secrets/PII placed into prompts or system messages; check
  output filtering/redaction; verify RAG retrieval enforces **per-user access control** (no cross-tenant leakage).
- **LLM03 Supply Chain** — model/dataset/plugin provenance: pinned versions + hashes for models pulled from
  registries; signature/integrity verification; vetting of third-party plugins / MCP servers.
- **LLM04 Data & Model Poisoning** — can an external/RAG source inject malicious content into training/context?
- **LLM05 Improper Output Handling** — follow model output to its **sink**: rendered as HTML (XSS), passed to
  `eval`/shell/SQL (injection), or used in a downstream request (SSRF)? Validate/escape/parameterize it like any
  untrusted input.
- **LLM06 Excessive Agency** — enumerate the tools/functions the model can call + their permissions. Least-privilege
  scoping? Human-in-the-loop gating on destructive/irreversible actions? No blanket API keys?
- **LLM07 System Prompt Leakage** — does the system prompt hold secrets/credentials/business logic that a leak would
  expose? (Assume it can leak.)
- **LLM08 Vector & Embedding Weaknesses** — RAG-specific: embedding-space attacks, retrieval access control, data
  leakage through the vector store.
- **LLM09 Misinformation** — are unanswerable queries refused rather than fabricated (grounded generation)?
- **LLM10 Unbounded Consumption** — token/cost/quota limits per request; no unbounded generation loop; model-
  extraction / resource-exhaustion guards.

## Agentic Top 10 (ASI 2026) — add when the system has agents/tools/memory/multi-agent

ASI01 Agent Goal Hijack · ASI02 Tool Misuse (validate/allowlist tool arguments — no arbitrary paths/URLs/shell) ·
ASI03 Identity & Privilege Abuse · ASI04 Agentic Supply Chain · ASI05 Unexpected Code Execution · ASI06 Memory &
Context Poisoning · ASI07 Insecure Inter-Agent Communication · ASI08 Cascading Failures · ASI09 Human-Agent Trust
Exploitation · ASI10 Rogue Agents. For each present capability, the auditor's concrete check is: **can untrusted
input steer this capability into an unintended-but-authorized action, and is there a human gate on the irreversible
ones?**

## Verdict contribution

R5 findings feed the same severity ladder + routing as every other reader. Notably:

- A **prompt-injection path with no trust boundary** on a tool-calling agent that can take destructive actions is
  typically **Critical → BLOCK → /03** (the agency architecture is wrong).
- **Model output flowing unvalidated into a sink** (SQL/shell/HTML) is a **High → REMEDIATE → /04** (validate the
  output) unless the whole output-handling design is missing (then architectural).
- A **critical LLM feature with no evaluation/guardrail dataset** is a systemic gap — flag it; if it needs a design
  rethink, route to `/03`.
