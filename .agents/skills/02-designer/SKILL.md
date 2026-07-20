---
name: 02-designer
description: "Realize the UX for a sprint — turn the spine's design-intent + the sprint's REQs into a tiered design system, per-screen specs, and a DM-ID manifest, all referencing REQs. The FIRST skill to run the Reconcile step: it challenges docs/spec/design-intent.md through the amendment protocol — fleshing out derived/[NEEDS CLARIFICATION] intent, and flagging where the realization violates a stated intent or the WCAG 2.2 AA floor (a brand color failing contrast is a computed contradiction) — and emits structured amendment rows. Use when the user says 'design sprint N', 'design the UI', 'wireframe the screens', 'build the design system', 'design tokens', or 'how should this look'. Writes docs/design/; appends docs/spec/amendment-log.json; never edits the spine's requirements. Do NOT plan epics/sprints — that is /01-planner. Do NOT design the system architecture, ADRs, or the data model — that is /03-architect."
---

# 02 · Designer — realize (UX)

Sprint-scoped: invoked **`02-designer sprint N`**. Realize the UX for sprint N's REQs — a tiered **design system**, a
spec per key **screen**, and a **DM-ID manifest** — all *referencing* the spine by `REQ-NNN`, never copying its prose.
You are the **first skill to amend the spine**: while realizing, you run the **Reconcile step** against
`design-intent.md` and emit structured `amendment-log.json` rows.

## Operating principle — realize, and reconcile

Two moves, run together:

- **Realize.** Turn the thin `design-intent.md` declaration + the sprint's REQs into a full design-system + screens
  (the realization). Reference REQs by ID; derive freely below the governed layer.
- **Reconcile (your debut of the amendment protocol).** Challenge `design-intent.md` two ways: **flesh-out** —
  concretize `derived` / `[NEEDS CLARIFICATION]` intent (Tier-2 gate → `stated`); **contradiction-flag** — catch
  where the realization violates a `stated` intent, the a11y floor, or a Constitution non-negotiable (Tier-2 gate, or
  Tier-3 defer for scope). You run Reconcile **inline — no subagent**: design-intent conflicts are surfaced, obvious,
  and gated, so the fresh-context isolation that 03/05/07 need does not apply here.

**The boundary-test = the token-governance line.** Reconcile fires only on the **governed** layer (brand · semantic
tokens · the a11y floor · key screens · interaction principles · job-outcomes); the **delegated** layer (primitive
values · component tokens · layout/spacing · internals) is free realization — no amendment, ever. Full method:
`references/reconcile-critique.md`.

## Profile switch — `agent-system` realizes the agent experience

Read the spine's `Profile` (the per-seat toggle table in `shared/agentic-profile.md`). Under **`webapp`** (default)
the flow below is unchanged. Under **`agent-system`** (or `mcp-server`), **Phase B designs the agent experience, not
screens** — the tool surface (names/descriptions are the interface; tool hit-rate is the quality metric), turns,
persona/voice, refusal-UX, and HITL touchpoints — per `references/agent-experience.md`. Phase A (tokens) and the
Reconcile machinery are unchanged; the **`DM-NNN` manifest stays**, but its rows point at **tools/turns/refusals**.
Reconcile's governed layer shifts to the **design-intent voice** + the **agent-contract HITL rows**; the WCAG floor
applies **only where a GUI exists**. Under **`skill-pack`**, 02 is **skipped** (trigger/description design folds into
03/04 + the skill-creator eval; `status` routes no design phase).

## The flow

Two gates (Gate 1 = foundation, Gate 2 = screens), with Reconcile folded into Gate 1. Craft lives in the references —
load each as its phase begins.

### Phase A — Foundation → `docs/design/design-system.md`
1. **READ UPSTREAM** — `docs/planning/sprints/sprint-NN.md` (which REQs are in scope), `docs/spec/design-intent.md`
   (the declaration to reconcile), the sprint's `docs/spec/capabilities/<domain>.md` REQ blocks, and
   `docs/spec/specification.md` (Constitution + brand/a11y non-negotiables). Optionally `architecture-constraints.md`.
2. **STYLE DIRECTION** — from `design-intent.md` (adjectives, tone, references). A populated design-intent is usually
   a *strong* signal; if it's thin, pause **once** with a proposed direction, then proceed (don't interrogate).
3. **TIERED TOKENS** — primitive → semantic → component, referencing inward (never skip a tier). Start from the
   **seed vocabulary** in `templates/design-system.md`; concretize per project. Apply **density-as-intent**
   (light = bg/hover · base = main/CTA · dark = text/pressed). Theming = semantic override only.
4. **COMPONENT INVENTORY** — a loose hierarchy (foundations → components → patterns → screens); Atomic Design as a
   *mental model*, not rigid buckets. Define only what this sprint's screens use.
5. **CONTENT & UX PATTERNS** + the **banned / anti-patterns** list (AI-slop guardrails).
6. **⟫ RECONCILE (pass 1) ⟪** — run the **dual pass** (`references/reconcile-critique.md`) against `design-intent.md`
   at foundation altitude: the deterministic detector (WCAG + a11y floor + token-chain) ‖ the judgment pass (Nielsen
   + JTBD, every finding **anchored**). Classify findings into tiers; emit `amendment-log.json` rows + DDRs.

>>> GATE 1: present the foundation **and** the batched Tier-2 amendments together; wait for PROCEED / ADJUST / a decision on each amendment before Phase B. <<<

### Phase B — Per-screen → `docs/design/<screen>.md`
For each key screen (`templates/screen.md`): wireframe (ASCII by default at sprint 1) → annotate with REQ-IDs →
**interaction table** → **state spec** → **a11y annotations**. Run the detector + heuristic pass on the *screens* as
**realization quality** — you fix your own design to meet the floor; escalate to a new amendment only on the rare
screen finding that can't be honored without changing a declaration. Generate the **DM-ID manifest**
(`templates/manifest.md`) — over wireframe regions, so it exists even on the ASCII path.

>>> GATE 2: present screen coverage + any escalations; on approval LOCK the design contract at docs/design/approved/sprint-NN/. <<<

### Phase C — Synthesis
Interaction flows (screen-to-screen map) · finalize the **DDRs** (the owner-tagged `## Design Decisions` section) ·
close-out.

## Design write-path (the spine's requirements are read-only here — do not corrupt them)

- **Write** the realization under `docs/design/`; **append** Reconcile rows to `docs/spec/amendment-log.json`. You
  **never edit** `docs/spec/capabilities/**` (the REQ text) — a requirement changes only through 00, not here.
- **Reference, never copy.** Every design artifact links `REQ-NNN`; if you're pasting requirement prose into a design
  doc, stop and link the ID instead (`shared/spine-boundary.md`).
- **Amendment rows are structured, not prose.** Append to the `{ "amendments": [ … ] }` array per the schema in
  `shared/spec-amendment-protocol.md`: `id` (`AMD-NNN`, `max+1`), `tier`, `disposition`, a `source_quote` of the
  exact declaration text, `resolved_by` (the `DDR-NNN`). **No `date`** — git is the trail.
- **Batch + escalate-when-uncertain.** All Tier-2 findings from the pass go into the **single** Gate 1 — never one
  gate per finding. When unsure whether a finding is governed, it touches brand/a11y/a key screen → **go up to Tier 2**.
- **DM-IDs / DDRs** are zero-padded `DM-NNN` / `DDR-NNN`; the manifest is locked (not regenerated) at Gate 2.

## Progress checklist (copy this and track as you go)

- [ ] A1 · READ UPSTREAM — sprint REQs + design-intent + REQ blocks + Constitution loaded (spine read-only)
- [ ] A2 · STYLE DIRECTION — set from design-intent; thin-signal pause capped at one round
- [ ] A3 · TIERED TOKENS — primitive→semantic→component from the seed vocab; density-as-intent; reference direction holds
- [ ] A4 · COMPONENT INVENTORY — loose hierarchy; only this sprint's components
- [ ] A5 · CONTENT & UX PATTERNS + banned list
- [ ] A6 · RECONCILE pass 1 — dual pass; findings anchored + tier-classified; `amendment-log.json` rows + DDRs emitted
- [ ] **>>> GATE 1: present foundation + batched Tier-2 amendments; wait for PROCEED / ADJUST / decisions <<<**
- [ ] B · SCREENS — per screen: wireframe + REQ refs + interaction table + state spec + a11y; detector as realization quality
- [ ] B · MANIFEST — DM-ID manifest generated (REQ → screen → DM-ID traces)
- [ ] **>>> GATE 2: present screen coverage + escalations; on approval lock docs/design/approved/sprint-NN/ <<<**
- [ ] C · SYNTHESIS — interaction flows + DDRs finalized (owner-tagged)
- [ ] Integrity: every in-scope REQ served by ≥1 screen; spine `capabilities/**` untouched; rows valid per schema

## Reads / Writes

**Reads:** `docs/planning/sprints/sprint-NN.md` · `docs/spec/design-intent.md` · `docs/spec/capabilities/<domain>.md`
· `docs/spec/specification.md` (the `Profile`) · (optionally) `docs/spec/architecture-constraints.md` · under
`agent-system`, `docs/spec/agent-contract.md` (the tool matrix + HITL rows the agent-experience realizes).
**Writes:** `docs/design/design-system.md` · `docs/design/<screen>.md` (per screen) ·
`docs/design/approved/sprint-NN/manifest.md` (+ `prototype/` + `*.png` when prototypes exist) · **appends**
`docs/spec/amendment-log.json`. **Never** writes `docs/spec/capabilities/**`.

## References (load when the phase needs them)

- `references/design-system.md` — Phase A craft: tiered tokens + seed vocabulary + density-as-intent + component
  hierarchy + content/UX patterns + banned-list + quality criteria.
- `references/screen-spec.md` — Phase B craft: wireframe + interaction table + state spec + a11y annotations + the
  component contract + the DM-ID manifest rule.
- `references/reconcile-critique.md` — the dual-pass Reconcile: boundary-test + deterministic detector (WCAG 2.2 AA +
  a11y floor + token-chain) + Nielsen heuristics + anchoring rule + tier classification + DDR format.
- `references/agent-experience.md` — **`agent-system` mode**: the tool surface / turns / persona / refusal-UX / HITL
  touchpoints that replace screens; the DM-NNN manifest over tools/turns; Reconcile against voice + agent-contract HITL.
- `shared/agentic-profile.md` — the per-seat toggle table (what 02 does per profile); repo-root-relative.
- `shared/spec-amendment-protocol.md` — amendment tiers + the row schema (your debut); repo-root-relative.
- `shared/spine-boundary.md` — declaration vs realization (the keystone); repo-root-relative.
