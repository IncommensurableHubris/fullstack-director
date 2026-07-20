# The next-command router + the human report

> The heart of `status`'s graded value: a **deterministic, priority-ordered router** (first match wins) from the
> derived state to the **single** exact next command, plus the human-facing report render. Load this at DERIVE + ROUTE.

## Deriving the inputs (from disk, per `shared/artifact-map.md`)

Compute these before routing — each traces to a file that exists or is absent:

- **spine present** — `docs/spec/specification.md` exists.
- **profile** — the `- **Profile:**` field in `specification.md` (`webapp` | `agent-system` | `mcp-server` |
  `skill-pack`); **absent ⇒ `webapp`**. Advisory when absent ("declare a profile; defaulting webapp"). It resolves the
  **design phase** below (`shared/agentic-profile.md`, the per-seat toggle table) and is mirrored into the AGENTS.md
  emission.
- **integrity** — PASS / FAIL (from `references/integrity-and-governance.md`). A FAIL carries the offending REQ-ID(s).
- **governance blockers** — `n_pending + n_deferred` amendment rows and `n_markers` surviving `[NEEDS CLARIFICATION]`.
  A **blocker exists** iff `n_pending + n_deferred + n_markers > 0`.
- **backlog present** — `docs/planning/backlog.md` exists.
- **patch in flight** — the backlog's `## Patches` ledger has an open row (`planned` / `in-progress` / `escalated`);
  the record lives at `docs/planning/patches/patch-NNN.md`. The ledger is the sole status origin.
- **current sprint N** — the **highest** `NN` for which *any* sprint artifact exists (a `sprints/sprint-NN.md`, a
  `docs/design/approved/sprint-NN/`, a `*-sprint-NN.md` report, or `src/**` for the sprint). If a backlog exists but no
  sprint artifact does, `N = 1`. If no backlog, `N` is undefined (routing stops at P3-backlog).
- **earliest missing phase in sprint N** — the first absent link in the chain below.
- **qa verdict** — the `verdict:` frontmatter of `docs/quality/qa-report-sprint-NN.md` (`SHIP` | `FIX` | `BLOCK`), else `—`.
- **`03 init` done** — `docs/architecture/system.md` exists.

### The per-sprint phase chain (the presence probes)

| Phase | Present iff | Owner |
|-------|-------------|-------|
| plan | `docs/planning/sprints/sprint-NN.md` | 01 |
| design **(profile-resolved)** | `webapp`: the screen manifest `docs/design/approved/sprint-NN/manifest.md`. `agent-system` / `mcp-server`: the **interaction manifest** at the same path (its `DM-NNN` rows point at tools/turns — 02's agent-experience mode). **`skill-pack`: no design phase — skip it** (trigger/description design folds into 03/04 + the skill-creator eval). | 02 |
| architecture | `docs/architecture/system.md` **and** ≥1 `docs/architecture/specs/*.md` referencing a sprint-N REQ | 03 |
| build | `src/**` has code **and** `_artifacts/exports/build-handoff-sprint-NN.md` (or just `src/**` if the export is gitignored/absent) | 04 |
| quality | `docs/quality/qa-report-sprint-NN.md` | 05 |
| release | `docs/release/release-report-sprint-NN.md` | 06 |
| security | `docs/security/security-audit-sprint-NN.md` | 07 |
| refactor | `docs/refactoring/refactor-report-sprint-NN.md` (optional — never gates the chain) | 08 |

*Design note:* design docs are screen-named, not sprint-named, but the **approved manifest** at
`docs/design/approved/sprint-NN/manifest.md` *is* sprint-scoped — use it as the design presence probe. If the manifest
is absent but a `design-system.md` exists, report `design: assumed from an earlier sprint` rather than a false gap.

## The router (priority-ordered — first match wins)

| # | State | Next command | Report emphasis |
|---|-------|--------------|-----------------|
| **P0** | no spine | `/00-discovery` | "No spine yet — discovery starts the chain." |
| **P1** | integrity **FAIL** | **`/00-discovery`** — repair the spine (**a verify-live L7 break** routes to `/00-discovery` to re-seed a missing/uncited `docs/verification/<tech>.md`, or `/03-architect` to re-verify on a tech-mandate) | **Lead with the specific break** (e.g. "REQ-014: registry File `capabilities/x.md` does not resolve"; or "verify-live 'openclaw': no docs/verification/openclaw.md"). **Halt** normal routing — a corrupt spine makes every downstream claim unreliable. |
| **P1.5-patch** | a `## Patches` ledger row is **open** (`planned`/`in-progress`/`escalated`) | **the patch's next seat** (sub-table below) | The expedite lane preempts sprint routing — one patch in flight finishes (or escalates out) before sprint work resumes. Report names the patch id + owning REQs. |
| **P2** | ship-ready **and** a governance blocker exists | `/00-discovery reflect` (a `pending`/`deferred` amendment) · `/00-discovery` (a surviving marker) | Override fires **only** when the normal route (P3) would be `/06-release …`. Report the counts tied to "**06-release blocks on these**." |
| P3-backlog | spine ✓, PASS, no backlog | `/01-planner` | The initial run writes the backlog **and** `sprint-01`. |
| P3-slice | backlog ✓, no `sprint-01.md` | `/01-planner` | Rare — re-run the initial decomposition. |
| P3-design | sprint N: no design | `/02-designer sprint N` | |
| P3-arch-init | sprint N: design ✓, no `system.md` | `/03-architect init` | First architecture ever; `sprint N` follows. |
| P3-arch | sprint N: `system.md` ✓, no specs for N | `/03-architect sprint N` | |
| P3-build | sprint N: architecture ✓, no `src`/handoff | `/04-builder sprint N` | |
| P3-review | sprint N: `src` ✓, no qa-report | `/05-reviewer sprint N` | |
| P3-fix | sprint N: qa verdict `FIX`/`BLOCK` | `/04-builder sprint N` → fresh `/05-reviewer sprint N` | The build↔review loop. |
| P3-release | sprint N: qa `SHIP`, no release-report | `/06-release sprint N` | *(unless P2 fires)* |
| P3-security | sprint N: release ✓, no security-audit | `/07-security sprint N` | Recommended after the first deploy. |
| P3-next | sprint N complete; backlog has un-`done` REQs beyond N | `/01-planner plan-sprint N+1` | The next slice. |
| P3-done | all backlog REQs `done` | project complete → `/00-discovery reflect` | Close the loop on the shipped outcome. |
| **P4** | (advisory — surfaced; the primary route only when a sprint is otherwise complete) | `/08-refactor assess` · `/00-discovery reflect` | See signals below. |

**The unifying P3 rule:** *route to the **earliest missing phase** in the current sprint's chain* (plan → design →
arch → build → quality → release → security). This one rule handles both **forward progress** and **gap/backfill**: a
sprint with `src` but no design routes back to `/02-designer sprint N` and the report flags the skipped phase.
**Profile resolves the design link:** under `skill-pack` the **design phase is not in the chain** (plan → arch → …),
so a `skill-pack` sprint with no design is **not** a gap and never routes to `/02-designer`; under `agent-system` the
design link is the **interaction manifest** (02's agent-experience), present at the same path as a webapp's screen
manifest.

### The patch's next seat (P1.5-patch — from the ledger row + committed artifacts)

| Ledger row | Committed artifacts | Next command |
|------------|---------------------|--------------|
| `planned` | — | `/04-builder` (the patch funnel: the record + existing realizations) |
| `in-progress` | no `docs/quality/qa-report-patch-NNN.md` | a **fresh** `/05-reviewer` on the patch (04 runs to completion in one pass; its handoff is gitignored — the ledger flip is the committed signal) |
| `in-progress` | qa verdict `FIX`/`BLOCK` | `/04-builder` (fix pass) → then a fresh `/05-reviewer` |
| `in-progress` | qa `SHIP`, no `docs/release/release-report-patch-NNN.md` | `/06-release` on the patch |
| `escalated` | — | `/01-planner plan-sprint N` (execution scope) / `/00-discovery reflect` (product scope) — and the A6 advisory fires |
| `done` | — | not in flight — normal routing resumes |

### P4 advisory signals (keep advisory)

Surface these in an **Advisories** section; they become the *primary* next command only when a sprint is otherwise
complete (nothing in P0–P3 fired for the current sprint):

- **Refactor — guardrail clustering:** read `.claude/rules/quality-guardrails.md`; if **≥5** entries name the same
  module/dir → "guardrails clustering in `<module>` (N entries) — consider `/08-refactor assess`."
- **Refactor — no pass on record:** ≥4 feature sprints complete and no `docs/refactoring/refactor-report-sprint-*.md`
  → "no refactoring pass after N feature sprints — consider `/08-refactor assess`."
- **Refactor — assessment without follow-through:** a `health-assessment-sprint-*.md` exists with no matching
  `refactor-report-*` → "health assessment for sprint N never executed — review or dismiss."
- **Reflection overdue:** ≥2 sprints have release reports and the charter shows no REFLECT since the last build →
  "multiple sprints shipped since the last reflection — consider `/00-discovery reflect`."
- **Patch-lane pressure (A6):** the `## Patches` ledger shows **≥3 consecutive `done` patches** since the last
  planned sprint, **or any `escalated` row** → "patch cadence: N consecutive patches — **this cadence is a sprint**;
  run `/01-planner plan-sprint N` / consider `/08-refactor assess`." Advisory, never a block (unbounded fast lanes
  quietly become the default road).

## The human report (print this; the machine subset also lands in `CLAUDE.md § Current State`)

```
## Project Status: <name>

**Spine** — integrity: <PASS | FAIL: …> · <n> REQs (<n> stated / <n> derived) across <n> domains
**Governance** — amendments: <p> pending · <d> deferred · <a> approved · <x> auto-applied · open markers: <m>
                 <if p+d+m > 0:>  ⚠ 06-release blocks on <p+d> unresolved amendment(s) + <m> marker(s)
                 <if a `## Verify-live` block is declared (WS6):>  **Verify-live** — <v> verified · <s> stale · <mm> missing
                 <if s+mm > 0:>  ⚠ 06-release G11 blocks on <s+mm> stale/missing record(s)
**Current sprint: N** — phase: <earliest-missing | complete> (qa verdict: <SHIP | FIX | BLOCK | —>)

**Sprint History**
| Sprint | Plan | Design | Arch | Build | Quality | Release | Security | Refactor |
|--------|------|--------|------|-------|---------|---------|----------|----------|
| 01     | ✓    | ✓      | ✓    | ✓     | ✓ SHIP  | ✓       | ✓        | —        |
| 02     | ✓    | ✓      | ✓    | ✓     | ✓ SHIP  | —       | —        | —        |

**Integrity** — <PASS, or the specific broken entries (REQ-ID → what broke)>
**Advisories** — <ADR-index drift / ledger↔registry drift / refactor signals / reflection overdue, or "none">

**Next command**
→ `<the single routed command>`
```

- The **Sprint History** matrix is a legible render — one row per sprint, ✓/— per phase, the qa
  verdict annotated in the Quality cell.
- **Integrity** repeats the verdict with the *specific* break (never a bare "FAIL") so the offending entry is
  actionable.
- **Next command** is exactly one line — the router's first match. If P1 fired, it is the repair; if P2 fired, it is
  the blocker-resolution, and the report makes clear *why it is not `/06-release`.*
