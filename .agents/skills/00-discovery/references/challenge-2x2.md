# CHALLENGE — assumption map (lightweight stress-test)

> Loaded by skill 00, phase 3. Purpose: surface the **undefended bets** in a spec the user *deliberately researched*
> — without re-litigating research they've already done. The gate is PROCEED / CLARIFY / PIVOT, **never KILL** (the
> user already committed to building; discovery's job is fidelity, not go/no-go).

## The 2×2

Place each assumption on two axes — **how well-evidenced** it is (Known / Unknown) and **how much it matters**
(Important / Unimportant):

|            | Important                | Unimportant      |
|------------|--------------------------|------------------|
| **Known**  | Validate & leverage      | Ignore           |
| **Unknown**| **⚠ SURFACE THESE**      | Park for later   |

Only the **Unknown + Important** cell reaches the gate. A *Known + Important* assumption the spec already evidences
needs no challenge; an *Unknown + Unimportant* one isn't worth the user's attention.

## What counts as "evidenced" (this is the calibration)

An assumption is **Known** (leave it alone) when the spec, the user's stated research, or a cited source already
backs it. It is **Unknown** (a candidate to surface) when nothing in the input defends it *and* getting it wrong
would change what's worth building. This keeps CHALLENGE lightweight by construction: a near-truth spec leaves few
Unknowns → CHALLENGE is near-silent; a thin spec leaves many → it challenges more. The intensity rides the same
fidelity dial as clarification.

## Three lenses (where killer assumptions hide)

Scan for Unknown+Important assumptions across:
- **Desirability** — will the target user actually want / adopt / pay for this? (the JTBD bet)
- **Feasibility** — can it be built as described, within the named constraints?
- **Viability** — does it hold up over time, at the stated scale, within the stated limits?

## Two forcing moves + the evidence trap (before the gate)

A near-truth spec can still hide **sycophantic agreement** — the model echoing the user's leading bet back as fact.
Two cheap, quantified moves counter it; run **both** before presenting the gate and record each as its own section in
`assumption-map.md`:

1. **Devil's-Advocate turn** — argue the **strongest case against** the leading framing or bet, once, explicitly. Not
   a hedge — a real dissent ("here is why this could be the wrong thing to build"). Record under `## Devil's advocate`.
   (Measured effect: sycophantic agreement 63% → 41%.)
2. **Pre-mortem** — ask "**assume the spine shipped and the product failed — why?**" and list the top few failure
   modes. Record under `## Pre-mortem`. (Klein: ~30% more risks surfaced, and qualitatively different ones than a
   forward "what could go wrong?" ask.)

**The confident-but-no-evidence trap.** Confidence is not evidence. A claim asserted flatly ("users obviously want
this", "it'll scale fine") with nothing in the input backing it is **Unknown**, however certain it sounds — surface
it. This is the qualitative sibling of the numbers-need-sources rule (`requirements-authoring.md`): unbacked prose
gets the same *surface-it* treatment as an unsourced number.

## Output → the gate

For each surfaced assumption, record in `docs/discovery/assumption-map.md`: the assumption (one line); the lens; why
it is Unknown+Important (what breaks if it's wrong); and a cheap way to reduce the risk (a "smallest test") if one is
obvious. Record the `## Devil's advocate` dissent and the `## Pre-mortem` alongside them. All of these feed the
**single batched REVIEW gate** (see [`review-gate.md`](review-gate.md)) — never a per-assumption interruption. The
user's call there is PROCEED (accept the bet), CLARIFY (add evidence now), or PIVOT (rethink the premise).
