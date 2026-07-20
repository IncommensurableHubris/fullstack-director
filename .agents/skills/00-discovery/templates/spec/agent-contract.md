# Agent Contract — <Project Name>

> **Declaration-truth for *agency*.** The sibling of [`design-intent.md`](design-intent.md) (the look/feel
> declaration) and [`architecture-constraints.md`](architecture-constraints.md) (the system envelope): this is the
> **agency** declaration — how much the agent may do on its own, with which tools, under what human oversight, at
> what cost, remembering what. **Emitted only under `Profile: agent-system`** (see
> [`shared/agentic-profile.md`](../../../../shared/agentic-profile.md)). Owned by **skill 00 (discovery)**; skills 02
> and 03 may only *amend* it (Tier-2 gate). Derived from GSA-TTS / CSA / AURA agent-specification practice, kept lean.
>
> All six sections are **core** — every `agent-system` spine carries all six.

---

## 1 · Autonomy tier

> One declared CSA level (L0–L5) with its user-role, plus a one-line rationale. The ladder: **operator** (human runs
> each step) → **collaborator** (agent acts, human in the loop) → **consultant** (agent proposes, human disposes) →
> **approver** (agent acts, human approves the risky ones) → **observer** (agent runs, human watches). Pick the
> *lowest* tier that does the job.

- **Tier:** _<e.g., "L3 — approver: Relay drafts and sends low-risk replies autonomously; a human approves anything
  that moves money or is uncertain.">_
- **Rationale:** _<why this tier and not the next one up>_

## 2 · Risk class

> From the **reversibility × impact-scope × write-access** test. Reversible + read-only + narrow → low; irreversible
> OR broad-write OR external side effects → high. This sets how hard the HITL gates and the audit trail must be.

- **Class:** _<low | moderate | high>_ — _<the one-line justification: what makes it this class>_

## 3 · Tool-permission matrix

> The machine-readable capability manifest — **least privilege, no wildcard scopes**. One row per tool the agent may
> call. `Risk` uses the reversibility/impact test; `HITL` says whether a human must confirm **before** the call.

| Tool | Scopes | Risk | HITL |
|------|--------|------|:----:|
| _<e.g., `inbox.read`>_ | _<e.g., "read-only, support queue only">_ | low | no |
| _<e.g., `refund.issue`>_ | _<e.g., "≤ last payment, one customer">_ | high | **yes** |

- **Justification for any `HITL: no` at risk ≥ reversible-external:** _<every autonomous power above read-only needs
  one line of why it's safe unattended — or raise the HITL flag>_

## 4 · Escalation / HITL policy

> The explicit, **non-overridable** halt-and-escalate list — the actions that **always** pause for a human,
> regardless of confidence. This is a *structural* control, not a prompt suggestion.

- _<e.g., "Any refund or payment — human approves before execution.">_
- _<e.g., "Abuse, legal, or self-assessed 'uncertain' → escalate, never answer.">_

## 5 · Cost envelope

> The runaway-loop defense (a documented failure class): a **token/spend budget per task** and **retry/step caps**.
>
> **Boundary (S8):** quantified **latency / throughput** NFRs live in
> [`architecture-constraints.md`](architecture-constraints.md) (the single home for measured performance targets) — the
> cost envelope **references** them, it does not restate them.

- **Token / spend budget per task:** _<e.g., "≤ 40k tokens / ticket; hard stop at 2×.">_
- **Retry / step cap:** _<e.g., "≤ 6 tool calls; on cap, give up and escalate — never loop.">_
- **Latency / throughput targets:** _<reference — see `architecture-constraints.md` § Scale & performance>_

## 6 · Memory policy

> What may persist **across sessions / users**, at *declaration* altitude (the *architecture* of memory — store,
> TTL, eviction — is skill 03's ADR). Default to the least memory that does the job.

- **Persists across sessions:** _<e.g., "a customer's prior-ticket summary, keyed to their account.">_
- **Never persists:** _<e.g., "payment card data; another customer's data in this customer's context.">_

---

<!-- Coverage (00, agentic branch): every tool row with HITL: no at risk ≥ reversible-external carries a
     justification above; at least one must-not REQ (IF/THEN Unwanted-behavior form) exists per high-risk tool. -->
