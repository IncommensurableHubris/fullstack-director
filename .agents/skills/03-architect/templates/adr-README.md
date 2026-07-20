<!-- Filename: docs/architecture/adr/README.md  (the ADR register — the single source for the ADR list). -->

# Architecture Decision Register

> **The canonical ADR index — and the `ADR-NNN` allocation source.** Owned by **skill 03 (architect)**, the **sole
> ADR allocator**. The next id is **`max(ID in this table) + 1`**, zero-padded. Any other skill that needs an ADR
> (e.g. `08-refactor`) requests `max + 1` from here. `system.md` §9 *links* this register — it never duplicates it.
> `/status` integrity-checks that every row resolves to a file and every `ADR-NNN.md` file appears in a row.

| ADR | Title | Status | Satisfies | Supersedes | Resolves |
|-----|-------|--------|-----------|------------|----------|
| [ADR-001](ADR-001.md) | _<Tech stack>_ | Accepted | _<architecture-constraints; REQ-NNN>_ | none | _<AMD-NNN \| n/a>_ |
| [ADR-002](ADR-002.md) | _<…>_ | _<Proposed \| Accepted \| Superseded by ADR-NNN>_ | _<…>_ | _<…>_ | _<…>_ |

<!-- Allocation: the next ADR is ADR-<max+1>. Add a row in the SAME step you write the ADR file — the register and
     the files must never drift. A superseded ADR keeps its row (status "Superseded by ADR-NNN"); ADRs are immutable. -->

## Conventions

- **Immutable.** An ADR is never rewritten. A changed decision is a **new** ADR that `Supersedes` the old one; the
  old row's status becomes `Superseded by ADR-NNN`.
- **Resolves** links an ADR to the `AMD-NNN` amendment it is the tech-mandate partner of (an approved Tier-2
  architecture conflict amends `architecture-constraints.md` **and** records the resolving ADR — one trigger, two
  altitudes; see `references/reconcile-architecture.md`).
- Every ADR carries a checkable **Rule** (MADR *Confirmation*) so it can back a `static-conformance` fitness function.
