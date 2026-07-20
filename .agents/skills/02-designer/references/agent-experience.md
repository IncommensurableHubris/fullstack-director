# Agent-experience craft — the tool surface is the UX

> Loaded by skill 02 when the spine's `Profile` is `agent-system` (or `mcp-server`) — see the per-seat toggle table
> in [`shared/agentic-profile.md`](../../../../shared/agentic-profile.md). It **replaces the screen-centric Phase B**:
> there are no screens to wireframe, so the realization is the **agent's experience** — its tools, turns, voice,
> refusals, and human-hand-off moments. Phase A (tokens) and the Reconcile machinery are unchanged; only *what you
> design* changes. **WCAG / the a11y floor applies only where a GUI actually exists** (a chat widget, an approval
> console) — for a headless agent it does not.

## 1 · Tool-surface design — names & descriptions ARE the interface

The tools listed in `docs/spec/agent-contract.md`'s permission matrix are the agent's UI. **The quality metric is
tool hit-rate** — does the model pick the right tool, first try, from the name and description alone? (Anthropic
tool-writing guidance.) For each tool the sprint touches:

- **Name** — a verb.noun the model reads unambiguously (`refund.issue`, not `doThing`). Keep the agent-contract's
  names; you are designing their *legibility*, not renaming them.
- **Description** — one line, action-first, that disambiguates it from its neighbours ("Issue an **approved** refund"
  vs. "Draft a reply"). Ambiguous descriptions are the #1 cause of wrong-tool calls.
- **Least privilege carries over** — the scopes are declared in the agent-contract; the design does not widen them.

## 2 · Conversation / turn design

Design the **turn shape**, not pixels: the canonical sequence (e.g. *acknowledge → ground → resolve-or-hand-off*),
where each tool sits in it, and the **clarifying-question budget** (how many times the agent may ask before it must
act or escalate). One `When` per turn, mirroring the spine's one-action-per-scenario rule.

## 3 · Persona / voice — the agent's look & feel

For an `agent-system`, `design-intent.md`'s voice **is** the brand. Realize it into concrete, checkable voice tokens
(tone · register · apology-budget · banned moves) the way a webapp realizes color tokens. This is the layer Reconcile
watches (below).

## 4 · Error-and-refusal UX

A refusal is a **designed experience**, not an error string. It is **honest and specific** — it names what the agent
will not do and **what happens next** — and it **ends in a hand-off** (`slack.escalate`, a human queue), never a
dead-end "I can't help." Every must-not REQ (the IF/THEN statements) has a refusal-UX counterpart here.

## 5 · HITL touchpoint UX

For every agent-contract row with **`HITL: yes`**, design the human moment: how the pending action is *presented* for
approval (the amount + reason + the un-reachable tool), what the *end user* sees while it waits ("a teammate is
reviewing"), and the fact that the gated tool is structurally unreachable until approved. These are the highest-stakes
moments in the whole experience — design them first.

## 6 · The manifest — DM-NNN over tools/turns

Generate the DM-ID manifest exactly as for screens (`templates/manifest.md`), but the **rows point at tools / turns /
refusals instead of screen regions** — `DM-001 = the refund.issue HITL touchpoint`, `DM-002 = the acknowledge→ground
turn`. **Keep the `DM-NNN` scheme** (downstream coverage — 03/04/05 — is unchanged; only the element *kind* changes).
Each row traces **REQ → tool-or-turn → DM-ID**.

## Reconcile targets under this mode

The dual pass still runs, but its **governed layer** shifts:

- **Voice/persona** (from `design-intent.md`) — a designed turn that contradicts a `stated` voice non-negotiable
  ("never promise a timeline") is a **contradiction-flag** → Tier-2 amendment, exactly like a brand-vs-a11y clash.
- **Agent-contract HITL rows** — if the experience needs an autonomous action the agent-contract marks `HITL: yes`
  (or vice-versa), that is a governed contradiction → Tier-2. The tool-permission matrix is a declaration; the design
  reconciles against it, never silently overrides it.
- The **deterministic detector** applies WCAG only where a GUI exists; otherwise the Reconcile pass is voice + HITL +
  JTBD judgment, every finding anchored.
