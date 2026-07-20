<!-- Filename: docs/architecture/specs/team-and-digest.md -->

# Feature Spec — Sprint-01 walking skeleton (access → standup → digest)

> **Realization** owned by **skill 03 (architect)**. References the spine by `REQ-NNN` and the design contract by
> `DM-NNN`; carries the **Verification Contracts** (method + pass-criterion) `05-reviewer` executes. Detailed,
> UI-specific steps live here (realization), not in the spine (which holds outcome-level Gherkin).

**Serves:** REQ-007, REQ-004, REQ-006, REQ-005, REQ-001, REQ-008 · **Covers DM:** DM-001…DM-008.

## Components

- **Auth (REQ-007):** magic-link request + verify. Covers **DM-001** (email input), **DM-002** (send button),
  **DM-003** (check-your-email state).
- **Team (REQ-004, REQ-006):** create team + invite by email; join via link + set display name.
- **Scheduling (REQ-005):** configure digest time + timezone.
- **Standup capture (REQ-001):** three-prompt entry. Covers **DM-004** (form), **DM-005** (submit disabled until
  complete), **DM-006** (saved toast + list append).
- **Digest (REQ-008):** generate one digest per day grouped by member; a non-submitter is omitted. Covers **DM-007**
  (dated header), **DM-008** (per-member grouped sections).

## Verification Contracts

| VC | REQ | DM | Method | Pass criterion |
|----|-----|----|--------|----------------|
| VC-01 | REQ-007 | DM-001/002/003 | api-contract | a valid magic-link verify returns an authenticated session; an expired link is refused |
| VC-02 | REQ-004/006 | — | api-contract | creating a team + inviting an email yields an invite; opening it with a display name creates a named member |
| VC-03 | REQ-005 | — | api-contract | setting digest time/timezone persists and drives the generation moment |
| VC-04 | REQ-001 | DM-004/005/006 | browser | the three-prompt form records exactly one entry per member/day and shows the saved toast |
| VC-05 | REQ-008 | DM-007/008 | unit | assembling a day's standups yields one digest grouped by display name; a non-submitter is omitted |

> `method ∈ {api-contract, browser, unit, static-conformance}`. The `browser` VC has a runtime once the web
> container lands (sprint-01 builds it); until then it is executed against the running skeleton.
