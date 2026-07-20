---
sprint: 01
prototype: none   # ASCII-wireframe path (sprint 1, no stack yet)
supersedes: []
---

# Design Manifest — Sprint 01

> **The coverage contract.** Owned by **skill 02 (designer)**, locked at Gate 2. Every distinctive visual element
> gets a stable **`DM-NNN`** ID so downstream coverage is mechanical: `03-architect` covers every DM-ID, `04-builder`
> implements every one, `05-reviewer` verifies every one. Each DM-ID traces **REQ → screen → DM-ID**.

## Screen: sign-in  →  serves REQ-007

| DM-ID | Element | Location (wireframe region) | Viewports | Required |
|-------|---------|-----------------------------|-----------|----------|
| DM-001 | Email input for the magic-link request | sign-in card, row 1 | desktop, tablet, mobile | required |
| DM-002 | "Send magic link" primary button | sign-in card, row 2 | desktop, tablet, mobile | required |
| DM-003 | "Check your email" confirmation state | sign-in card, post-submit | desktop, tablet, mobile | required |

## Screen: submit-standup  →  serves REQ-001

| DM-ID | Element | Location (wireframe region) | Viewports | Required |
|-------|---------|-----------------------------|-----------|----------|
| DM-004 | Three-prompt standup form (yesterday / today / blockers) | standup card, body | desktop, tablet, mobile | required |
| DM-005 | Submit button, disabled until all three prompts are filled | standup card, footer | desktop, tablet, mobile | required |
| DM-006 | "Saved" toast + the entry appearing in today's list | top-right toast + list | desktop, tablet, mobile | required |

## Screen: daily-digest  →  serves REQ-008

| DM-ID | Element | Location (wireframe region) | Viewports | Required |
|-------|---------|-----------------------------|-----------|----------|
| DM-007 | Digest header with the date | digest page, header | desktop, tablet, mobile | required |
| DM-008 | Per-member grouped sections (display name + their entry) | digest page, body | desktop, tablet, mobile | required |
| DM-009 | Omission of a member who did not submit before generation (no placeholder row) | digest page, per-member row | desktop, tablet, mobile | optional |
