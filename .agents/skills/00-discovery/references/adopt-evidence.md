# ADOPT — evidence craft (brownfield: a spine from an existing codebase)

> Loaded by `/00-discovery adopt`. Entry: an existing repo (yours, or a fork) with **no spine**. Exit: a normal spine
> the whole chain can operate on. **Copy the progress checklist below as your first act**, then work the scan → confirm
> flow.
>
> **The anti-hallucination invariant (structural, mechanically graded):** every adopt-sourced REQ cites a
> `code:<path>` (or `docs:<path>`) that **resolves on disk**. A REQ citing a file that does not exist is an integrity
> failure — the same discipline as registry↔leaf. Code evidences **existence, never intent**: so every candidate is
> `derived` by construction until the user confirms it at the gate.
>
> **Boundary with 08-refactor:** 08 reconciles code↔docs *when a spine exists*; ADOPT **creates** the spine. No overlap.

## Progress checklist (copy this and track as you go)

- [ ] **EVIDENCE SCAN** — capabilities · constraints · invariants enumerated from the code; READMEs/docs as *secondary* sources
- [ ] **CANDIDATE DECLARATIONS** — each REQ `derived`, `source: code:<path:line>` (or `docs:<path>`); EARS statement lines
- [ ] **CHALLENGE (adopt-flavored)** — "the code does X — do you *want* X?"; zombie features → out-of-scope / removal note, **never a silent keep**
- [ ] **CONSTITUTION PROPOSAL** — observed invariants offered **PROPOSED** only (Tier-2-class); never auto-seeded
- [ ] **>>> REVIEW GATE + confirm-derived sweep: confirmed REQs flip to `stated` with `source: "adopt-confirmed: code:<path>"`; unconfirmed stay `derived` <<<**
- [ ] **WRITE SPINE** — every emission by name (below); every `code:<path>` resolves; `scripts/verify-spine.py` exits 0

## The flow

### 1 · EVIDENCE SCAN — enumerate what the code *proves*
- **Observable capabilities** — routes / endpoints, CLI commands, screens, public functions, and what the **tests**
  exercise. Each is a candidate REQ.
- **Constraints** — language/stack, dependencies, hosting/config (Dockerfile, CI, env). These land in
  `architecture-constraints.md`.
- **Invariants** — auth model, storage location, data-residency hints, access guards. These are candidate Constitution
  items *and* the natural home for **must-not REQs** (an auth guard → "IF … unauthenticated …, THEN the system SHALL
  refuse …").
- Existing **READMEs/docs** ingest as **secondary** sources (`docs:<path>`) — they describe intent the user may or may
  not still hold; the code is primary.

### 2 · CANDIDATE DECLARATIONS — author, but mark the source as evidence
Author each candidate REQ per the normal rubric (`requirements-authoring.md` — EARS statement line + outcome Gherkin),
but the fidelity source is the **evidence**, not a user quote:
```
<!-- source: code:notekeep/cli.py:31 -->      (a resolving path[:line]) — Registry Status: derived
<!-- source: docs:README.md -->               (a found document) — Registry Status: derived
```
**Every candidate is `derived`** — code proves the capability *exists*, not that the user *wants* it. No change to the
stated/derived enum; `adopt` just adds these two source forms.

### 3 · CHALLENGE (adopt-flavored) — run the 2×2 on *intent*
The lens flips from "is this evidenced?" to "**the code does X — do you actually want X?**" A **zombie feature** (the
code proves it, but nothing wires it / no one wants it) is surfaced as an explicit **out-of-scope note or removal
candidate** in `assumption-map.md` — **never a silent keep**, and never a silent delete. Record the Devil's-Advocate
turn + pre-mortem as usual (`challenge-2x2.md`).

### 4 · CONSTITUTION PROPOSAL — proposed, never seeded
An observed invariant ("all data stays local in a JSON file"; "every command requires an unlocked session") is offered
as a **PROPOSED** Constitution item — adopted only by explicit user decision at the gate. Constitution changes are
Tier-2-class; ADOPT never auto-seeds them. Mark them `PROPOSED` until the gate confirms.

### 5 · ⟫ REVIEW GATE + confirm-derived sweep ⟪
The existing batched gate (`review-gate.md`), plus a **confirm-derived sweep**: each REQ the user confirms flips from
`derived` to `stated` with `source: "adopt-confirmed: code:<path>"` (parallel to the `clarification: <topic>` form);
each PROPOSED Constitution item the user accepts becomes a real Constitution item; **unconfirmed REQs stay `derived`**
(flagged, as ever). Nothing is confirmed on the user's behalf.

### 6 · WRITE SPINE — the normal write-path, every emission by name (seam S4)
Write the spine via the write-path in `SKILL.md`, then make **every emission, by name — identical to the intake path**:
① `docs/README.md` (legibility index) ② the per-project `AGENTS.md` from `templates/agents-view.md` ③ the standing
gate — copy `templates/scripts/verify-spine.py` to `scripts/verify-spine.py` **verbatim, always** ④ the opt-in hook
templates to `scripts/hooks/`. The remaining emissions fire **identically to intake**: ⑤ the `agent-system`
`agent-contract.md` ⑥ `SECURITY.md` (always) ⑦ **under a declared `## Verify-live` block** — seed
`docs/verification/<tech>.md` per tech from live docs/source (`shared/live-source-verification.md` § seed). **A
fork/adopt over a too-new host framework is the city-claw guardrail's most important firing** — seed the host
framework here. ⑧⑨ the `CLAUDE.md` + `GEMINI.md` **bridges, create-if-absent only** — a brownfield repo often
already has a `CLAUDE.md`: **never edit it**; advise adding `@AGENTS.md` as line 1 instead. Then run
`scripts/verify-spine.py` — exit 0 on the fresh spine, and **every adopt `code:<path>` resolves**.
