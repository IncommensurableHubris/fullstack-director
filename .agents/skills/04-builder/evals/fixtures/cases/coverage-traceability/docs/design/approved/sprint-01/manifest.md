---
sprint: 01
prototype: none   # text-render slice (no visual mockup; the "elements" are structural parts of the rendered text)
supersedes: []
---

# Design Manifest — Sprint 01 (digest text render)

> **The coverage contract.** Owned by **skill 02 (designer)**, locked at Gate 2. Every distinctive element of the
> rendered digest gets a stable **`DM-NNN`** ID so downstream coverage is mechanical: `03-architect` covers every
> DM-ID, `04-builder` implements every one (and maps it to a `file:line` in the handoff), `05-reviewer` verifies every
> one. For this headless slice the "elements" are the structural parts of the **text-rendered** digest.

## Rendered artifact: daily-digest (text)  →  serves REQ-008, REQ-009

| DM-ID | Element | Location (in the rendered text) | Required |
|-------|---------|---------------------------------|----------|
| DM-001 | Digest header carrying the date | first line / header block | required |
| DM-002 | Per-member grouped sections (display name + that member's entry) | body, one block per member | required |
| DM-003 | "Needs help" section collecting flagged blockers, above the per-member sections | top block, before the member sections | required |
