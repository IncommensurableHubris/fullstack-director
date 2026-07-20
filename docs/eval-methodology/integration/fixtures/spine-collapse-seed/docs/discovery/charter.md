# Product Charter — TeamPulse

> **The macro-loop anchor.** Owned by **skill 00 (discovery)**. The product's enduring intent — its JTBD and the
> go/pivot/reflect decisions — from which the spine is *derived* and, on an upstream pivot, *regenerated*. The spine
> shatters only if this anchor is lost; it holds because the JTBD here does not move when a constraint does.

## Job to be done (the enduring intent)

> **When** my team is spread across timezones, **I want** to share and absorb daily status without a meeting, **so**
> I can stay in sync without losing focus time.

This JTBD is the invariant. Constraints (stack, hosting, data residency, scale) are *realizations of how* we serve it
in v1 — they may pivot without the job changing.

## Primary users

- **Member** — an engineer on a 4–12 person distributed team.
- **Lead** — configures the team, reads the digest first.

## Go / pivot / reflect decisions

| # | Decision | Disposition |
|---|----------|-------------|
| D1 | Async daily standup replacing the meeting — the core bet | **GO** (v1) |
| D2 | One daily digest as the single artifact | **GO** (v1) |
| D3 | Data residency: EU-only in v1 | **GO** (v1) — *a hosting constraint, not the JTBD; revisit if the user base widens* |

> **Reflect log.** Upstream pivots that change a *constraint* are processed here + through the amendment channel;
> the JTBD above does not change, so the spine regenerates rather than shatters.
