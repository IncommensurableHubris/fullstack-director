# Spec Amendment Protocol — how skills challenge and improve the spine

> Shared by every skill that touches the amendment channel. The **appenders** — skills that run a **Reconcile** step
> and emit `amendment-log.json` rows — are **00** (init), **02**, **03**, **08** (plus **01** in exactly one
> mechanical case: the patch lane's S1 additive-regression-case row, §schema below — no Reconcile step). Skills
> **04** (builder), **05**, and **07** *consume* this protocol to **classify and escalate** drift honestly but
> **append no row**: `04` surfaces a
> build-time contradiction in its build-handoff (a wrong realization → back to `03`; a wrong declaration → a pending
> amendment for `00`/`05`), never editing the spine itself. The spine is **mutable but not freely** — expertise
> improves it through a controlled channel, neither a wall nor a free-for-all. Read with `spine-boundary.md`: that
> file says *what* is a declaration; this one says *how* a declaration changes.

## The three tiers

| Tier | What | Disposition | Who decides, when |
|------|------|-------------|-------------------|
| **Tier 1** | Clarification — an addition with exactly **one defensible answer**, no user-observable behavior change | **auto-applied** to the spine (+ logged) | the skill |
| **Tier 2** | Expert conflict — changes a user-observable behavior, a named technology, or anything a stakeholder would have an opinion on (e.g. SQLite → PostgreSQL) | **gated** — pause for an immediate user decision (+ ADR if architectural) | the user, now |
| **Tier 3** | Scope change — adds, removes, or reprioritizes a capability | **deferred** to `00 reflect` as `pending` | the user, at REFLECT |

## Classification rule — escalate when uncertain

If a finding changes a **user-observable behavior**, a **named technology**, or **anything a stakeholder would have
an opinion on** → **minimum Tier 2**. Tier 1 is *only* for additions with exactly one defensible answer.

The asymmetry is deliberate: mis-classifying **down** (calling a Tier-2 change "Tier 1") silently corrupts the
user's intent; mis-classifying **up** costs one extra gate. **When in doubt, go up.**

## The Reconcile step (a mode, not a new skill or number)

Reconcile is a **step any spec-consuming skill runs in a mode**, wired into that skill's **existing gate** so it
can't be silently skipped. Its stance is **"be a critic, not a builder"** — bounded to findings that **change this
slice or violate the contract**, not nice-to-haves.

- **Input:** the slice's **declarations** (the in-scope REQ blocks + `design-intent` / `architecture-constraints`)
  **+** this skill's **realization** (its design system, architecture, etc.).
- **Output:** amendments (Tier 1/2/3) **emitted as structured rows in `amendment-log.json`** — not prose buried in a
  report. The structured emission is what the evals grade and what `/status` counts.

## Tier-2 gating

- **Batch** all Tier-2 conflicts from **one** Reconcile pass into a **single** gate — never interrupt the user once
  per finding.
- **Exclude** anything already settled (e.g. a decision an existing ADR already records).
- Reuse skill 02's existing **Gate** pattern for the pause.
- On approval, a Tier-2 amendment updates the **declaration** (the spine file) **and**, when architectural, records
  an **ADR** for the realization decision — one trigger, two altitudes.

## Spine write-path (corruption is the highest-rated risk — follow exactly)

1. The **REQ registry** table in `specification.md` is **authoritative** for ID→file and **must be updated in the
   same step** as any REQ write (intake, decomposition, amendment).
2. **Skill 01 (planner) is the sole REQ-ID allocator.** Any other skill needing a new ID requests `max(registry)+1`.
3. An amendment **edits the delimited block** — replace the span between `### REQ-NNN:` and `<!-- /REQ-NNN -->`.
   Never edit by fuzzy clause-matching.
4. `/status` integrity-checks the spine (every registry `File` resolves and contains its REQ block). Run it before
   trusting the spine and after any bulk change.

## `amendment-log.json` schema

The file is `{ "amendments": [ <row>, … ] }`. Each row:

```json
{
  "id": "AMD-007",
  "req": "REQ-014",
  "skill": "03-architect",
  "tier": 2,
  "disposition": "approved",
  "source_quote": "architecture-constraints.md: 'Datastore: SQLite'",
  "supersedes": null,
  "resolved_by": "ADR-005"
}
```

- `disposition` ∈ `pending` | `auto-applied` | `approved` | `deferred`.
- **A Tier-3 row stays `pending`/`deferred` until REFLECT resolves it.** `approved` on a `tier: 3` row is valid
  **only** as the outcome the user chose at `00 reflect` (with `resolved_by` naming that decision). A pass that
  *authors* a Tier-3 row — intake, Reconcile, or amendment — **may not disposition it `approved`, and may not write
  its REQ into the live spine in the same pass.** Deferring the scope decision *is* the tier's entire function: a row
  that arrives already-approved has skipped the only gate it ever gets, and the capability reaches `01-planner`'s
  backlog as actionable scope the user never chose. `auto-applied` on a Tier-3 row is the same violation wearing a
  different label — the tell is the *write*, not the word.
- **No `date` field** — git is the dated audit trail.
- **S1 additive-regression-case rows (the patch lane's one append):** a certified patch that *adds* eval cases
  under `docs/spec/evals/**` logs exactly one Tier-1 row — `skill: "01-planner"` (the certifying seat), `tier: 1`,
  `disposition: "auto-applied"`, `source_quote: "patch-NNN: added regression case(s) <dataset path>"` — same frozen
  schema, no new fields; dataset *edits* remain normal-road amendments.
- `tier` ∈ `1` | `2` | `3`.
- `source_quote` preserves the exact declaration text the finding is about, so a reviewer sees what changed without
  diffing.
- `supersedes` links a superseding amendment to the one it replaces; `resolved_by` points at the ADR or the REFLECT
  decision that closed it (`null` while `pending`).

## Release gate (skill 06)

`06 release` **blocks deploy** on any amendment still `pending` or `deferred`, and on any surviving
`[NEEDS CLARIFICATION]` marker in the spine. Unresolved intent must not ship silently.
