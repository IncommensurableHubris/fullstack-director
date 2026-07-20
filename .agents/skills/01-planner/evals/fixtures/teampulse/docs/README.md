# TeamPulse — docs index

> **Legibility index.** `docs/spec/` is **declaration-truth** (the spine); everything else **references** it by
> `REQ-NNN` and never restates requirement text. Owned by skill 00 (discovery).

## The spine (truth) — `docs/spec/`

- [`spec/specification.md`](spec/specification.md) — the index: project **Constitution** + the authoritative
  **REQ registry** (ID → file).
- [`spec/capabilities/`](spec/capabilities/) — REQ blocks grouped by domain:
  - [`standups.md`](spec/capabilities/standups.md) — submit, edit-until-lock, needs-help (REQ-001…003).
  - [`team.md`](spec/capabilities/team.md) — create+invite, digest time/timezone, join via link, magic-link
    sign-in (REQ-004…007).
  - [`digest.md`](spec/capabilities/digest.md) — daily generation, needs-help surfacing, read current & past
    (REQ-008…010).
- [`spec/design-intent.md`](spec/design-intent.md) — declared look/feel (mostly `derived`; user specified little).
- [`spec/architecture-constraints.md`](spec/architecture-constraints.md) — TS/Node, PostgreSQL, single EU VPS via
  Docker, magic-link auth, ≤ 50 teams / ≤ 600 members.
- [`spec/amendment-log.json`](spec/amendment-log.json) — structured change history (empty at genesis).

## Intent & history — `docs/discovery/`

- [`discovery/charter.md`](discovery/charter.md) — JTBD, problem/user, scope in & out, decision log.
- [`discovery/assumption-map.md`](discovery/assumption-map.md) — the CHALLENGE 2×2; one surfaced bet (async
  completion rate).

## How to use this

- **Need a requirement?** Look it up by `REQ-NNN` in [`spec/specification.md`](spec/specification.md); the block
  lives in the listed `capabilities/<domain>.md` file.
- **Changing a declaration?** It goes through an **amendment** (see `shared/spec-amendment-protocol.md`), not a
  silent edit. Realizations (design, architecture, code) change through drift detection.
- **Open questions:** 2 `[NEEDS CLARIFICATION]` markers (REQ-002 edit-lock timing, REQ-008 no-submission handling)
  — must reach 0 before release.

_Authoritative source: [`spec/specification.md`](spec/specification.md). On any product or scope question, the
Constitution wins._
