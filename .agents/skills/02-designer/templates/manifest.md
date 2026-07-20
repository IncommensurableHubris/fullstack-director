<!-- Filename: docs/design/approved/sprint-NN/manifest.md  (zero-padded sprint token). -->
---
sprint: NN
prototype: ./prototype/index.html   # or: none (ASCII-wireframe path)
supersedes: []                      # DM-IDs from an earlier sprint this redesign replaces
---

# Design Manifest — Sprint NN

> **The coverage contract.** Owned by **skill 02 (designer)**, locked at Gate 2. Every distinctive visual element
> gets a stable **`DM-NNN`** ID so downstream coverage is mechanical: `03-architect` covers every DM-ID, `04-builder`
> implements every one, `05-reviewer` verifies every one. Generated even on the ASCII path — DM-IDs are taken over
> **wireframe regions**, so the contract exists from sprint 1 with no prototype.
>
> **Inclusion rule (the side-by-side test):** an element belongs here if, removed from the build, a non-technical
> user would immediately notice it side-by-side with the design. Decorative micro-details below that threshold do
> not. **Cap ~10–15 per screen** — more means the granularity is wrong. Each DM-ID traces **REQ → screen → DM-ID**.

## Screen: <screen-name>  →  serves REQ-NNN, REQ-NNN

| DM-ID | Element | Location (selector / wireframe region) | Viewports | Required |
|-------|---------|----------------------------------------|-----------|----------|
| DM-001 | <description — specific enough to verify in side-by-side> | <region or selector> | desktop, tablet, mobile | required |
| DM-002 | <…> | <…> | <…> | optional |

## Screen: <screen-name>  →  serves REQ-NNN

| DM-ID | Element | Location (selector / wireframe region) | Viewports | Required |
|-------|---------|----------------------------------------|-----------|----------|
| DM-003 | <…> | <…> | <…> | required |
