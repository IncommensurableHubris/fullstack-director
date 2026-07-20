# REVIEW gate — the single batched discovery gate

> Loaded by skill 00, phase 5. The **one** place skill 00 interrupts the user. It batches the CHALLENGE findings
> (phase 3) and the FIDELITY gaps (phase 4) into a single decision, so the user is asked **once** — never per finding
> (see `shared/spec-amendment-protocol.md`: "single gate, never per-finding").

## What to present (in one message)

1. **Undefended bets** (from `assumption-map.md`) — the Unknown+Important assumptions, each with why it matters and a
   cheap test if one is obvious.
2. **Fidelity gaps** — REQs marked `derived` (confirm or correct?); missing coverage (problem / user / JTBD / scope /
   success / constraints); ambiguities; contradictions.
3. **A compact REQ → source map** — rendered live from the `<!-- source -->` lines, so the user sees at a glance
   what is `stated` (with its quote) vs `derived`.
4. **The devil's-advocate dissent + the pre-mortem** (from `assumption-map.md`, per `challenge-2x2.md`) — the single
   strongest case against the leading framing, and the top pre-mortem failure modes. Present them **even when the
   spec is near-truth**; this is the anti-sycophancy check, not a formality.

Keep it scannable — a short list, not a wall of prose.

## The decision (PROCEED / CLARIFY / PIVOT — never KILL)

- **PROCEED** — the user accepts the spec (and any surfaced bets) as-is. Write the spine. `derived` REQs stay
  `derived`; unresolved non-blocking gaps become `[NEEDS CLARIFICATION]` markers (06-release blocks on survivors).
- **CLARIFY** — the user answers some or all gaps now. Fold each answer into the spine as `stated`
  (`source: "clarification: <topic>"`); re-present only if new gaps opened. This is the gap-driven interview, batched.
- **PIVOT** — a surfaced bet or contradiction means the premise needs rethinking. Loop back to ITCH with the new
  angle; record the pivot in the charter decision log.

**Never KILL.** The user already committed to building; discovery clarifies the spec — it does not decide whether to
build.

## Record the decision

Append the outcome (PROCEED / CLARIFY / PIVOT + a one-line rationale) to the charter **decision log**, then proceed
to WRITE SPINE (phase 6).
