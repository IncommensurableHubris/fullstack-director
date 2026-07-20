# Spine integrity + governance counts

> The precise assertions behind the **integrity verdict** and the **governance counts**. Load this at INTEGRITY +
> GOVERN. The verdict is **PASS / FAIL**: only **load-bearing** checks flip it; **advisory** checks WARN. This is the
> spine write-path's **rule #4** (`shared/spec-amendment-protocol.md`): *`/status` integrity-checks the spine.*

## What you parse (the spine, read-only)

- **The REQ registry** — the table in `docs/spec/specification.md`: `| REQ | Name | Priority | Status | File |`. The
  `File` column is the **authoritative** ID→leaf map (paths are relative to `docs/spec/`, e.g. `capabilities/api.md`).
  The `Status` column is **fidelity** (`stated`/`derived`) — *not* execution status (that lives in the backlog ledger;
  never conflate them).
- **The REQ blocks** — in each `docs/spec/capabilities/<domain>.md`: `### REQ-NNN: <name>   (MUST|SHOULD|MAY)` … a
  `<!-- source: … -->` line … `<!-- /REQ-NNN -->`.
- **The amendment log** — `docs/spec/amendment-log.json` = `{ "amendments": [ {id, req, skill, tier, disposition,
  source_quote, supersedes, resolved_by} ] }`.
- **The markers** — occurrences of the literal `[NEEDS CLARIFICATION]` anywhere under `docs/spec/**`.

## Load-bearing checks (FAIL the verdict — corruption of declaration-truth)

*The principle: the spine's ID→file→block map is internally consistent **and** the amendment log is machine-readable —
the two things every skill and the release gate depend on.* A FAIL names the **specific** offending entry.

| ID | Assertion | Failure message (name the entry) |
|----|-----------|----------------------------------|
| **L1** | Every registry `File` **resolves** — the leaf path exists on disk. | `REQ-NNN: registry File '<path>' does not resolve` |
| **L2** | Each registry REQ's leaf **contains its delimited block** — both `### REQ-NNN:` (heading) **and** `<!-- /REQ-NNN -->` (closing delimiter) are present in that file. | `REQ-NNN: leaf '<path>' is missing its delimited block (### REQ-NNN … <!-- /REQ-NNN -->)` |
| **L3** | **No orphan blocks** — every `### REQ-NNN:` block found under `capabilities/**` has a registry row. | `REQ-NNN: block present in '<path>' but absent from the registry` |
| **L4** | **No duplicate REQ-IDs** in the registry (each ID appears in exactly one row). | `REQ-NNN: appears in N registry rows (must be exactly one)` |
| **L5** | `amendment-log.json` **is valid JSON** with a top-level `amendments` array. | `amendment-log.json: invalid JSON / no 'amendments' array` |
| **L6** | Every REQ eval-block **`dataset:` path resolves** on disk (in-spine golden datasets under `docs/spec/evals/**`; `agent-system`). Vacuously PASS when no eval block exists. | `REQ-NNN: eval dataset '<path>' does not resolve` |
| **L7** | **Verify-live records resolve, bidirectionally + cited** (WS6): every `## Verify-live` tech has a resolving `docs/verification/<tech>.md`; no orphan record (a record with no declaration); no claims-table row with an empty citation. Vacuously PASS when nothing is declared and no records exist. | `verify-live '<tech>': no docs/verification/<tech>.md` / `orphan record docs/verification/<tech>.md` / `docs/verification/<tech>.md: uncited claim` |

If **all** load-bearing checks hold → **PASS**. If **any** fails → **FAIL**, and the report + the `CLAUDE.md §
Current State` emission lead with the offending entry (e.g. `FAIL — REQ-014: registry File 'capabilities/x.md' does
not resolve`). **The load-bearing set mirrors the emitted `verify-spine.py` FAIL checks exactly** — the script and
`status` must never diverge on the integrity verdict (the WS1 §B4 parity contract; L6 joined in Task 3.10, L7 in
WS6). A verify-live L7 FAIL routes to `/00-discovery` (re-seed) or `/03-architect` (re-verify on a tech-mandate).

**Never repair.** An L-failure is *reported* and routed to `/00-discovery` (the spine owner). `status` editing the
spine to fix it would corrupt the very boundary it verifies — the one thing this seat must not do.

## Advisory checks (WARN only — realization drift, not spine corruption)

These surface in the report's **Advisories** section; they **never** flip the verdict. Each is owned by another skill —
`status` observes the drift, it does not fix it.

| ID | Assertion | Why advisory | Owner |
|----|-----------|--------------|-------|
| **A1** | REQ/ADR IDs are zero-padded & well-formed (`REQ-008`, not `REQ-8`). | Cosmetic/sorting; resolvable; not ambiguous. | 00/03 |
| **A2** | ADR index (`docs/architecture/adr/README.md`) ↔ `ADR-NNN.md` files are in sync (each file indexed; each index row has a file). | Realization integrity, not the spine. | 03 |
| **A3** | Backlog ledger ↔ registry **exactly-once** — every spine REQ appears once in `docs/planning/backlog.md`. | Realization integrity. | 01 |
| **A4** | Registry `Status` (stated/derived) matches each block's `<!-- source: … -->` line (a `stated` row has a real quote; a `derived` row says `inferred`). | 00's write-path fidelity flag, not corruption. | 00 |
| **A5** | An `approved` Tier-2 amendment's `resolved_by: ADR-NNN` resolves to an existing ADR file. | Advisory realization link. | 03 |
| **A6** | Patch-lane pressure — scan `docs/planning/patches/` + the backlog's `## Patches` ledger: every row ↔ a record file (exactly-once); **≥3 consecutive `done` patches since the last planned sprint, or any `escalated` row** → the advisory "patch cadence: N consecutive patches — **this cadence is a sprint**; run `/01-planner plan-sprint N` / consider `/08-refactor assess`". | Expedite-lane overuse is a planning smell, not corruption; advisory, never a block. | 01 |

## Governance counts (the release-blockers `06` gates on)

Count `amendment-log.json` rows by `disposition` and tally the surviving markers:

- **`pending`** — awaiting a decision (a Tier-2 gate not yet answered, or a fresh row). **Blocks release.**
- **`deferred`** — a Tier-3 scope finding routed to `/00-discovery reflect`. **Blocks release.**
- **`approved`** — a resolved Tier-2 (informational).
- **`auto-applied`** — a resolved Tier-1 (informational).
- **surviving `[NEEDS CLARIFICATION]` markers** under `docs/spec/**`. **Blocks release.**

**The tie to the release gate (`shared/spec-amendment-protocol.md` § Release gate):** `06-release` **blocks deploy** on
any `pending`/`deferred` amendment and on any surviving marker. `status` surfaces `n_pending + n_deferred + n_markers`
**tied to that fact**, so the block is visible *before* someone runs `/06-release` — and, when a project is otherwise
ship-ready, the router's **P2** override sends them to resolve the blocker instead of hitting the gate.

Emit the counts into `CLAUDE.md § Current State` as:
`**Amendments:** <p> pending · <d> deferred (<a> approved · <x> auto-applied)` and
`**Open [NEEDS CLARIFICATION]:** <m>`.
