# Assumption Map — PennyPilot

> Loaded by skill 00, phase 3 (CHALLENGE). The lightweight 2×2: only **Unknown + Important** assumptions reach the
> gate. Skill 01 reads this for **risk-first sprint sequencing** — sprint 1's walking skeleton should be biased to
> de-risk the top bet below.

## Surfaced bets (Unknown + Important)

### A1 — Users will connect a real bank account to a new app
- **Lens:** Desirability + Feasibility (the foundation bet).
- **Why Unknown + Important:** The entire product derives from a connected account — no connection, no transactions,
  no insights, nothing. Whether a first-time user will trust PennyPilot enough to link their bank through the
  read-only aggregation flow is **undefended** in the brief, and if they won't, every downstream capability is
  dead on arrival. This is both the riskiest integration and the root dependency — they coincide.
- **Smallest test:** Get the connect-account → import → see-something path working end-to-end first and measure how
  many invited users actually complete the connection.

## Parked (Known, or not premise-breaking)

- **Categorization UX (manual vs auto-suggest):** a design refinement (skill 02), not a premise-breaking bet — parked.
- **Budget-alert delivery (email vs in-app):** realization detail, parked.
