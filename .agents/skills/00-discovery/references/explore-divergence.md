# EXPLORE — divergence craft (bare itch → a chosen framing, or a decided "don't build")

> Loaded by `/00-discovery explore`. Entry: a **bare itch** ("I keep losing track of client invoices…"), pre-commitment.
> Exit: a chosen problem framing handed to ITCH — **or** a recorded decision *not* to proceed. **Copy the progress
> checklist below as your first act**, then work the four moves.
>
> **The hard invariant (structural, non-negotiable):** EXPLORE **may not write anything under `docs/spec/**`.** No
> spine, no REQ, no Constitution — this mode is pre-commitment, and premature requirement definition is the single
> worst-documented LLM failure in requirements work. The one artifact you write is `docs/discovery/exploration.md`.
> (Post-WS1 the verify script and the evals both enforce the no-spine rule.)

## Progress checklist (copy this and track as you go)

- [ ] **PULL** — itch elicited via Mom-Test discipline (past events, their life, ≥80% listening); model-seeded options tagged `origin: model`
- [ ] **DIVERGE** — **≥3 distinct** problem framings, each passed through the Torres test; solutions only as option-families with a smallest-test
- [ ] **APPETITE** — a size (not an estimate) recorded for the itch
- [ ] **>>> PICK GATE: present framings + recommendation + a Devil's-Advocate turn against the leading one; user picks / ranks / parks / declines — "don't build" is legitimate <<<**
- [ ] **HANDOFF** — chosen framing → ITCH's JTBD input; decision + rationale in `exploration.md`; one-line pointer in the charter decision log
- [ ] **No `docs/spec/**` written** (the hard invariant)

## The four moves

### 1 · PULL — facilitate, don't generate
Elicit the itch; do **not** answer it. Mom-Test discipline: ask about **specific past events** ("when did this last
bite you?"), about **their life and workflow**, not about your idea — and **listen ≥80%** of the time. Named techniques,
the model *asking*. When you must offer an option to keep momentum, **tag it `origin: model`** in the artifact (LLMREI
steering defense — AI-seeded ideas are marked so they can't masquerade as the user's).

### 2 · DIVERGE — force at least three framings
Produce **≥3 distinct problem framings** (JTBD / opportunity-space statements), not three solutions. Pass each through
the **Torres test**: *"can more than one solution address this? If not, it is a solution wearing a need's clothes —
reframe it upward."* Solutions appear only as **option-families** under a framing, each with a **smallest-test** (the
cheapest way to learn if it's real). Diverging before converging is the whole point — a single plausible reading is the
failure mode.

### 3 · APPETITE — a size, not an estimate
Shape-Up style: **how much is this itch worth** — a small batch, a big batch? Record an **appetite** (time/size the
user is willing to spend), never a bottom-up estimate. This feeds 01's slicing later; here it just bounds ambition.

### 4 · ⟫ PICK GATE ⟪ — converge, or decide not to
Present the framings + a **recommendation** + a **mandatory Devil's-Advocate turn against the leading framing** (the
strongest case that it's the wrong thing to build). The user **picks or ranks** — or **parks / declines**. **"Don't
build" is a legitimate outcome here**: pre-commitment go/no-go lives in EXPLORE. (This is distinct from the downstream
REVIEW gate, which keeps its never-KILL rule — that gate runs *after* commitment.)

## HANDOFF
The chosen framing becomes ITCH's **JTBD input** — EXPLORE feeds the default flow, it does not fork it. Record the full
decision + rationale in `exploration.md` (its single home); drop a **one-line pointer** in the charter decision log.
If the outcome is "don't build," record that and stop — no spine.

## `docs/discovery/exploration.md` skeleton (write this — the only artifact EXPLORE emits)

```markdown
<!-- budget: ≤80 lines — an exploration is a divergence record, not a spec; keep it scannable. -->
# Exploration — <itch, in the user's words>

## Framings   (≥3 — each a problem/opportunity, not a solution)
### F1: <one-line problem framing>
- origin: user | model
- Torres test: <can multiple solutions address it? if not, how it was reframed upward>
- option families: <family A — smallest-test> · <family B — smallest-test>
### F2: <…>   (origin · Torres test · option families)
### F3: <…>   (origin · Torres test · option families)

## Appetite
<a size, not an estimate — how much this itch is worth>

## Decision
<picked framing / ranking — or "don't build" / parked>, + one-line rationale.
Devil's-advocate against the leading framing: <the strongest case it's the wrong thing to build>.
```
