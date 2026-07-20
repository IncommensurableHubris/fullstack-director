---
name: status
description: "The project's read-only 'where am I / what's next' oracle - scans the artifact chain, INTEGRITY-CHECKS the spine, counts the governance blockers 06-release gates on, DERIVES live state, and routes the NEXT COMMAND. READ-ONLY with respect to truth: never edits the spine or realizations; the only writes are two generated views, keeping docs/spec/** byte-identical. SEQUENTIAL - no subagents (a single derive-only read). Graded value: the DETERMINISTIC verdict (PASS, or FAIL naming the REQ-ID), pending/deferred amendment + [NEEDS CLARIFICATION] counts, and the routed next command. Use when the user says 'status', 'where are we', or 'what's next', or at session start. Reads docs/spec/** and the artifact chain + git state. Writes ONLY CLAUDE.md Current State + AGENTS.md. Do NOT plan/design/architect/build/review/ship/secure/refactor - it ROUTES to the owning skill. Do NOT edit the spine to fix findings - an integrity FAIL is REPORTED (repair via /00-discovery), never silently corrected."
---

# status · Project GPS — scan, integrity-check, derive, route

The framework's **"where am I / what's next" oracle**. It is a **cross-cutting meta activity** (named by function, not
an SDLC seat — prefix-less, like `08-refactor`), and per the master plan it is **built and run last**: it scans
*everything*, so it is correct only once every other skill's shape is final. Give any project to `/status` and it
answers three questions from the files on disk — never from memory:

1. **Is the spine sound?** — the integrity verdict (PASS, or FAIL naming the offending REQ-ID).
2. **What's blocking?** — the `pending`/`deferred` amendment + surviving `[NEEDS CLARIFICATION]` counts that
   `06-release` gates on, surfaced *early*.
3. **What do I run next?** — the single exact next command, in the framework's vocabulary.

Its graded value is **not** "a nice summary" — a strong reader summarizes a repo too. It is the **deterministic derived
state**: the integrity verdict + the governance counts + the routed command, **computed from the files and emitted
machine-readably** into `CLAUDE.md § Current State` so the next seat — and `06`'s release gate, and the next `/status`
— can act on it, not re-derive it.

## The seat's two defining properties

- **Sequential — no subagents.** `shared/subagent-protocol.md`: subagents exist for context-isolated *verification*
  and a few *bounded parallel reads*. `status` is neither — it is a single **derive-only read**. There is **nothing to
  relax** in the harness `<SUBAGENT-STOP>` (the `04`/`06`/`08` precedent, not the `03`/`05`/`07` one). Nothing here
  spawns.
- **Non-appender + non-mutator of truth — the honesty gate.** `status` is **absent** from the amendment-protocol's
  appender list (`00`/`02`/`03`/`08`). It **never** edits the spine or a realization. It writes **only generated
  views** — `CLAUDE.md § Current State` and the `AGENTS.md` emission — both pure regenerable projections
  (`shared/spine-boundary.md`: a generated view is safe to overwrite because its source lives elsewhere). Its
  correctness proxy is the **inverse** of every other skill: after it runs, `docs/spec/**` and every realization are
  **byte-identical.** This is `status`'s analog of `05`'s EXECUTED / `08`'s behavior-preserved — *truth is unchanged.*

## Operating principle — read the files, derive the state, route the command, touch no truth

- **Derive from disk, never from memory.** Every claim — the phase, the integrity verdict, the counts, the route —
  traces to a file that exists (or is absent). If a file is unreadable, say `UNKNOWN` and name it; never guess, never
  edit a source to make the picture tidy.
- **Report a break; never fix it.** An integrity FAIL is *surfaced* with the offending ID and routed to repair
  (`/00-discovery` owns the spine write-path). `status` editing the spine to "fix" corruption would itself corrupt the
  declaration boundary — the one thing this seat must never do.
- **Route, don't do.** The next command names the **owning skill**; `status` never plans, designs, builds, reviews,
  ships, secures, or refactors. It is the GPS, not the driver. (A demonstrably **wrong route** — the router, not
  the project — is framework friction: FB entry via the `feedback` skill; `shared/feedback-loop.md` § Activation.)

## The flow — one mode, one sequential pass, no gate

`/status` takes **no arguments** (one repo = one spine). It runs one pass; because it mutates no truth, there is **no
user-decision gate** — it scans and reports. Craft lives in the references; load each as its step begins.

1. **SCAN.** Enumerate the artifact chain against `shared/artifact-map.md` — spec → planning (incl.
   `docs/planning/patches/` + the backlog's `## Patches` ledger) → design → architecture → `src` → quality → release →
   security → refactoring — recording present/absent per sprint. Read-only. Determine the **current sprint** (the
   highest `sprint-NN` with any artifact), the **earliest missing phase** within it, and any **patch in flight**
   (an open `planned`/`in-progress` Patches row).
2. **INTEGRITY.** Run the **load-bearing** checks → the **PASS/FAIL verdict**; run the **advisory** checks → the
   WARN list. A FAIL names the **specific** offending entry. (`references/integrity-and-governance.md`.)
3. **GOVERN.** Count `amendment-log.json` rows by disposition (`pending` · `deferred` · `approved` · `auto-applied`)
   and the surviving `[NEEDS CLARIFICATION]` markers in the spine. **`pending` + `deferred` + markers are the
   release-blockers** — `06-release` blocks on any of them; surface the counts tied to that fact. **When a
   `## Verify-live` block is declared** (WS6), also derive the **verify-live coverage** (verified / stale / missing)
   from the declared techs vs their `docs/verification/<tech>.md` records — `06` G11 blocks on any missing/uncited
   (this is L7's data, re-read for the human line). **No block declared ⇒ omit the line** (the on-demand pattern).
4. **DERIVE + ROUTE.** Apply the **priority-ordered router** (`references/next-command.md`): P0 no-spine → P1
   integrity-halt → **patch-in-flight → the patch's next seat** → P2 governance-blocker override → P3
   earliest-missing-phase in the current sprint → P4 advisories. First match wins. Produce the **single** next command.
5. **REGENERATE VIEWS.** Write the machine-readable derived state into `CLAUDE.md § Current State` (the emission the
   grader and `06` read) and **re-emit `AGENTS.md`** from the spine Constitution + summary. Both are generated views —
   never a source of truth. Then print the human report. (`references/generated-views.md`.)

## The integrity verdict — load-bearing vs advisory (the spine write-path's rule #4)

The verdict is **PASS / FAIL**. Only **load-bearing** checks flip it — *the spine's ID→file→block map is internally
consistent and the amendment log is machine-readable* (what every skill and the release gate depend on). Advisory
findings **WARN** but never fail the verdict (they are realization drift, owned elsewhere). Full assertions in the
reference; the split:

**Load-bearing (FAIL the verdict, naming the offending entry):** L1 every registry `File` resolves · L2 each registry
REQ's leaf contains its delimited block (`### REQ-NNN:` … `<!-- /REQ-NNN -->`) · L3 no orphan blocks (every block has a
registry row) · L4 no duplicate REQ-IDs · L5 `amendment-log.json` is valid JSON with an `amendments` array · **L6 every
REQ eval-block `dataset:` path resolves** (`agent-system`; vacuously PASS with no eval block) · **L7 verify-live
records resolve** (WS6: every `## Verify-live` tech has a resolving, cited `docs/verification/<tech>.md`; no orphan
record; no uncited claim; vacuously PASS when nothing is declared). **The load-bearing set mirrors the emitted
`verify-spine.py` FAIL checks — the two must never diverge on the integrity verdict.**

**Advisory (WARN only — realization drift, not spine corruption):** A1 ID zero-padding/well-formedness · A2 ADR index
(`adr/README.md`) ↔ `ADR-NNN.md` files in sync (03's) · A3 backlog ledger ↔ registry exactly-once (01's) · A4 registry
`Status` (stated/derived) ↔ each block's `<!-- source -->` line (00's) · A5 an `approved` Tier-2's `resolved_by`
resolves to an existing ADR · A6 patch-lane pressure — ≥3 consecutive `done` patches since the last planned sprint,
or any `escalated` row → "this cadence is a sprint — run `/01-planner plan-sprint N` / consider `/08-refactor
assess`" (advisory, never a block).

## The next command — the priority-ordered router (first match wins)

The full table is `references/next-command.md`; the shape:

- **P0** no `docs/spec/specification.md` → `/00-discovery` (no spine — start the chain).
- **P1** integrity **FAIL** → **halt normal routing**; lead with the broken entry; repair routes to `/00-discovery`.
- **Patch-in-flight** (after P1, before P2) — an open `## Patches` row routes to **the patch's next seat**:
  `planned` → `/04-builder` (the funnel) · `in-progress` + no `qa-report-patch-NNN.md` → a fresh `/05-reviewer` ·
  qa `FIX`/`BLOCK` → `/04-builder` (fix pass) · qa `SHIP` + no `release-report-patch-NNN.md` → `/06-release` ·
  `escalated` → `/01-planner plan-sprint N` / `/00-discovery reflect` (+ the A6 advisory). One patch in flight
  finishes before sprint routing resumes.
- **P2** otherwise ship-ready **and** a governance blocker exists → route to **resolve** it (`/00-discovery reflect`
  for a `pending`/`deferred` amendment; `/00-discovery` for a surviving marker) **instead of** `/06-release`.
- **P3** the normal chain — *route to the **earliest missing phase** in the current sprint* (this one rule subsumes
  forward progress **and** gap/backfill): no backlog → `/01-planner` · no design → `/02-designer sprint N` · no
  `system.md` → `/03-architect init` · no specs → `/03-architect sprint N` · no `src` → `/04-builder sprint N` · no qa
  → `/05-reviewer sprint N` · qa `FIX`/`BLOCK` → `/04-builder sprint N` · qa `SHIP`, no release → `/06-release sprint
  N` · no security → `/07-security sprint N` · sprint complete → `/01-planner plan-sprint N+1` (or project complete →
  `/00-discovery reflect`).
- **P4** advisories (surfaced, primary only when a sprint is otherwise complete) — refactor signals → `/08-refactor
  assess`; reflection overdue → `/00-discovery reflect`.

## The machine-readable emission (what the grader and `06` read)

`CLAUDE.md § Current State` carries the derived state — **derived status only** (methodology is framework-level, never
restated here). Exact shape in `templates/current-state.md`; the graded fields:

```markdown
## Current State
<!-- GENERATED by /status — derived status only. Do not hand-edit; re-run /status. -->

- **Spine integrity:** PASS            <!-- or: FAIL — REQ-014: registry File `capabilities/x.md` does not resolve -->
- **Sprint:** 2 · **Phase:** quality (qa verdict: SHIP)
- **Amendments:** 0 pending · 0 deferred (2 approved · 1 auto-applied)   <!-- 06-release blocks on any pending/deferred -->
- **Open [NEEDS CLARIFICATION]:** 0
- **Verify-live:** 2 verified · 0 stale · 0 missing   <!-- WS6: ONLY when a `## Verify-live` block is declared; omit the whole line otherwise (the on-demand pattern) -->
- **Next command:** `/06-release sprint 2`

*Derived by /status from docs/spec/ + the artifact chain. Not a source of truth.*
```

## Write-path (the read-only guarantee — follow exactly)

- **Writes ONLY two generated views:** `CLAUDE.md § Current State` (derived status) and `AGENTS.md` (re-emitted from the
  spine Constitution + summary — full re-emit each run: idempotent in-sync, self-healing on drift, per
  `references/generated-views.md`).
- **Never writes** `docs/spec/**` (the spine) or **any realization** (`docs/planning/**`, `docs/design/**`,
  `docs/architecture/**`, `src/**`, `docs/quality|release|security|refactoring/**`). An integrity break is **reported**,
  not repaired.
- **Reference, never copy.** The report and the emission cite `REQ-NNN`/`ADR-NNN`; they never paste requirement prose
  (`shared/spine-boundary.md`).
- **The honesty invariant:** after `/status`, `git diff` shows **only** `CLAUDE.md` and `AGENTS.md` changed — the spine
  and every realization are **byte-identical.** If you cannot honor that, you are doing something `status` must not do.

## Progress checklist (copy this and track as you go)

- [ ] SCAN — artifact chain enumerated vs `shared/artifact-map.md`; current sprint + earliest-missing-phase determined
      (read-only)
- [ ] INTEGRITY — load-bearing checks → PASS/FAIL (FAIL names the offending REQ-ID); advisory checks → WARN list
- [ ] GOVERN — amendment dispositions counted (`pending`/`deferred`/`approved`/`auto-applied`) + surviving markers;
      `pending`+`deferred`+markers surfaced as the `06`-release blockers; **verify-live coverage (verified/stale/missing)
      derived iff a `## Verify-live` block is declared** (else the line is omitted)
- [ ] DERIVE + ROUTE — the priority router applied (P0 → P1 halt → P2 blocker-override → P3 earliest-missing → P4
      advisory); **one** exact next command produced
- [ ] REGENERATE VIEWS — `CLAUDE.md § Current State` written (the machine emission: integrity · sprint/phase · counts ·
      next command); `AGENTS.md` re-emitted from the spine (Constitution verbatim + recomputed summary)
- [ ] Human report printed (Spine · Governance · Sprint History matrix · Integrity · Advisories · Next command)
- [ ] Honesty: `git diff` shows **only** `CLAUDE.md` + `AGENTS.md` changed — `docs/spec/**` + every realization
      byte-identical (the read-only proxy); no source edited to "fix" a finding

## Reads / Writes

**Reads:** `docs/spec/specification.md` + `capabilities/**` + `design-intent.md` + `architecture-constraints.md` +
`amendment-log.json` · `docs/planning/backlog.md` (incl. the `## Patches` ledger) + `sprints/**` + `patches/**` ·
`docs/design/**` · `docs/architecture/system.md` + `adr/**` + `specs/**` · `src/**` · `docs/quality/**` ·
`docs/release/**` · `docs/security/**` · `docs/refactoring/**` · `.claude/rules/*-guardrails.md` · git state. **Writes (generated views ONLY):** `CLAUDE.md § Current State` ·
`AGENTS.md`. **Never** `docs/spec/**` or any realization.

## References (load when the step needs them)

- `references/next-command.md` — the full P0–P4 decision table + the routing craft + the Sprint History render.
- `references/integrity-and-governance.md` — the load-bearing (L) + advisory (A) assertion tables + the governance counts
  (dispositions + surviving markers) and how they tie to `06`'s block.
- `references/generated-views.md` — the `CLAUDE.md § Current State` + `AGENTS.md` re-emission contracts (read-only *to
  truth*; the generated-view-vs-maintained-artifact rule).
- `shared/artifact-map.md` — the cross-skill index `status` verifies reality against; repo-root-relative.
- `shared/spec-amendment-protocol.md` — the dispositions counted + the write-path rule #4 (*`/status` integrity-checks
  the spine*); repo-root-relative.
- `shared/spine-boundary.md` — generated view vs maintained artifact (why writing the two views is not mutating truth);
  repo-root-relative.
- `shared/subagent-protocol.md` — why `status` stays **sequential** (it is neither verification nor a parallel read);
  repo-root-relative.
- `shared/live-source-verification.md` — L7 (verify-live records) joins the load-bearing set (the parity contract);
  the conditional verify-live coverage line; repo-root-relative.

## Next skill

`status` is informational — the report's **Next command** is what you run next. There is no downstream artifact and no
gate; re-run `/status` anytime to re-orient.
