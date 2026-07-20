---
name: 04-builder
description: "Build the sprint slice - turn 03's per-feature specs + Verification Contracts (+ 02/03's contracts, the 01 slice) into a working vertical slice under src/** with tests, then emit the build-handoff: the SOLE seed for the isolated reviewer (05). Sequential - no subagents, no user gate. TDD RED-first. Carries every VC row with an EXECUTED/OBSERVED/INFERRED evidence state + coverage map. A non-amender but honest escalator: surfaces build-time drift (code/test to 03, declaration to 00/05) and HALTs rather than faking a pass. Drives the fix pass: turns reviewer RED tests green and TDDs prose findings for re-review. Use when the user says 'build sprint N', 'implement the features', or 'fix the review findings'. Writes src/** + _artifacts/exports/build-handoff-sprint-NN.md; never edits docs/spec/**, docs/architecture/**, or docs/design/**. Do NOT architect or write ADRs - /03-architect. Do NOT verify or QA - /05-reviewer. Do NOT plan sprints - /01-planner. Do NOT design UX - /02-designer."
---

# 04 · Builder — build

One mode. **`04-builder sprint N`** turns the sprint's **realization layer** into a working vertical slice + tests and
emits the **build-handoff** — the *sole* seed for the context-isolated reviewer (`05`). Unlike `02`/`03` (two modes, a
Reconcile gate), `04` is **one sequential pass, no gate, no subagents**: the isolation that matters is `05`'s,
downstream. Your graded value is **not** "working code" (a strong builder writes that too) — it is the
**cold-reviewable, honest handoff + non-tautological tests** that let a fresh reviewer verify without inheriting your
build bias.

## Operating principle — build from realizations, hand off for isolated review

- **Build (the funnel).** Read `03`'s per-feature specs + **Verification Contracts**, `02`'s design contract, the
  slice's "Done When", `system.md`/ADRs as the **ambient contract**. Implement `src/**` sequentially, TDD RED-first
  for testable behaviors, happy-path (hardening is `05`). Never re-interpret the raw spine.
- **Hand off (evidence, not narrative).** Emit `_artifacts/exports/build-handoff-sprint-NN.md`: a frozen diff
  baseline + the per-behavior evidence state + a REQ coverage map + attestations, so `05` can *reconstruct the diff,
  re-run the oracles, and check coverage* with zero access to this session.
- **Non-amender, honest escalator.** `04` appends **no** `amendment-log.json` row (that stays `00/02/03/08`). It never
  silently patches code *or* spec to fake a pass — build-time drift is **surfaced** and recorded in the handoff.

## The flow — one sequential pass (craft lives in the references; load each as its step begins)

0. **FIX-PASS CHECK** — if a **FIX REQUIRED** `docs/quality/qa-report-sprint-NN.md` exists for this sprint, you are the
   **maker-half of the build↔review loop** (`05` is the checker): read its **Findings** + the committed reviewer **RED
   tests** as an added funnel input and run the **fix pass** (`references/build-discipline.md`) — drive each failing
   behavior to green (make a reviewer RED test pass, **never editing it** — the anti-circular rule; full TDD-for-bugs
   for a prose finding), then **re-emit** the handoff (fixed rows EXECUTED + a deviations note + fresh `final_commit`/
   `spec_slice_hash`). If **no** such report exists, this is inert — proceed to the normal build.
   **PATCH-FUNNEL CHECK** — if the dispatch is a certified **patch** (a `docs/planning/patches/patch-NNN.md` record
   with an open `## Patches` ledger row), the funnel narrows: inputs = **the patch record + the existing realizations
   its owning REQs already have** (no new specs, no sprint file); discipline = **TDD-for-bugs** (reproducing RED test
   first — the fix ships its regression test); scope = the record's behaviors, nothing wider. Flip the ledger row
   `planned → in-progress` at build start (your one routine ledger write). The handoff is **patch-keyed**:
   `_artifacts/exports/build-handoff-patch-NNN.md` with `review_mode: patch`, `patch: patch-NNN`, and
   `spec_slice_path` = the patch record (`spec_slice_hash` computed over it). **P3/P4 are HALT conditions**: a new
   dependency (P3) or the certified size budget exceeded (P4) → HALT, mark the ledger row **`escalated`**, re-enter
   the normal chain — **never silently widen**. (A small fix arriving here *without* a patch record? Propose patch
   classification and route to `/01-planner patch` — requester ≠ authorizer.) If neither applies, proceed normally.
1. **READ FUNNEL** — load the realizations as ambient contract: `docs/architecture/specs/<feature>.md` (+ Verification
   Contracts) · `system.md` · `docs/architecture/adr/**` · `docs/design/approved/sprint-NN/manifest.md` (if a UI
   slice) · `docs/design/design-system.md` (tokens) · `docs/planning/sprints/sprint-NN.md` (the slice + "Done When" +
   frozen Gherkin) · `.claude/rules/quality-guardrails.md` (if present). **Direct reads — no Explore subagent** (build
   stays sequential).
2. **CAPTURE `baseline_commit`** — `git rev-parse HEAD` **before any edit**, into the handoff frontmatter. It anchors
   the reviewer's exact diff. (Fresh project with no commit? Make the initial commit first, then capture.)
3. **REVIEW VERIFICATION CONTRACTS** — for each VC row, confirm it is buildable in this environment. **Unbuildable →
   INFERRED with a cited reason** (e.g. a `browser` row with no runtime) — honest scoping, not silent dropping. This
   is the builder↔reviewer negotiation.
4. **IMPLEMENTATION ORDER** — consume the spec/slice order (foundation → domain → API → UI → wiring). Do not re-derive
   the slice.
5. **BUILD (sequential, per behavior)** — `references/build-discipline.md`:
   - **TDD RED-first, scoped** to `unit`/`api-contract` rows: write the test, **observe it fail** (record it —
     the anti-tautology capture), minimal code to green, refactor. `static-conformance`/`browser` rows use their own
     oracle.
   - **`eval-suite` rows** (`Profile: agent-system`): **eval-first RED** — the RED is a failing eval **case** observed
     before the fix (the harness over the in-spine dataset is the oracle); and the **grader must bite** — a degenerate
     output must fail the grader before the row counts EXECUTED (the bite rule, `shared/agentic-profile.md`). The
     handoff's eval-suite row carries both the RED-note and the grader-bites line. Writing a new judge for a row is
     evals-operations (`shared/agentic-profile.md` §eval-suite) — its validation record must exist before the row
     counts EXECUTED.
   - **Anti-tautology gate** before marking a row EXECUTED: RED evidence *or* the introduce-a-bug answer. Reject
     assertion-free / assert-the-mock / oracle-copied-from-impl tests.
   - **Reuse-first** (read the files a task touches; no duplicate modules) · **hardened dependency safety** (verify
     existence + reputation before install; pin + lockfile + audit; a new dep beyond the envelope is a HALT) ·
     **outcomes, not ceremony** (readable · SRP · no dead code; **no SOLID-acronym audit** — style is `05`/`08`'s
     seat). Small, atomic conventional commits.
6. **TRACEABILITY** — every VC row → `test:loc`; every in-scope REQ → FULL/PARTIAL/NONE; every DM-ID (if a manifest)
   → `file:line`.
7. **HANDOFF** — write the evidence-bearing build-handoff (`references/build-handoff.md` · `templates/build-handoff.md`):
   frontmatter (`baseline_commit`/`final_commit`/`spec_slice_path`/**`spec_slice_hash`**/`review_mode: full`) + File
   List + VC carry-forward (evidence state + repro command + RED-note + oracle hash + every non-EXECUTED reason/Unknown)
   + the REQ coverage map + attestations. **Compute `spec_slice_hash` mechanically** (the one-liner in
   `references/build-handoff.md`) so `05` can recompute + compare — a mismatch is `05`'s BLOCK. Capture `final_commit` last.

**HALT conditions** (surface, don't push through): a new dependency beyond the envelope · 3 consecutive failures on a
behavior · missing config · a genuinely contradictory/unbuildable spec · a drift-repair loop that won't converge ·
**on a patch: the certified size budget (P4) exceeded — HALT + mark the patch's ledger row `escalated`**.
*Do not stop for milestones or session boundaries* — run to completion or a **recorded** HALT (in the handoff's
blocked record; `06-release` blocks on it). **Never fake a pass.** In a vendored consumer, a HALT whose cause is
the **framework itself** (not this project) also gets an FB entry before the session ends — the `feedback` skill
(`shared/feedback-loop.md` § Activation).

**Drift → honest escalation (the three-way verdict).** A failing VC is the **code** (fix it), the **test** (fix it),
or the **spec**. A wrong *realization* spec → flag to `03`. A wrong *declaration* → a pending amendment surfaced for
`00`/`05` in the handoff. `04` writes neither the spine nor the specs.

## Write-path (the realizations are read-only here — do not corrupt them)

- **Write** `src/**` (source + tests) and `_artifacts/exports/build-handoff-sprint-NN.md`; optionally a light
  `Dockerfile`/`docker-compose.yml` (only if the stack/deploy calls for it) and `sbom.json`.
- **Never write** `docs/spec/**` (the spine), `docs/architecture/**`, or `docs/design/**` (read-only realizations — an
  error is *escalated*, not edited).
- **Reference, never copy.** The handoff links `REQ-NNN` / `DM-NNN` / `VC-NN`; it never pastes requirement prose
  (`shared/spine-boundary.md`).
- **No amendment rows.** `04` classifies and escalates drift; it appends none (`shared/spec-amendment-protocol.md`).
- **No subagents, no gate.** Isolation is `05`'s seat (`shared/subagent-protocol.md`).

## Progress checklist (copy this and track as you go)

- [ ] FIX-PASS CHECK — a FIX REQUIRED qa-report for this sprint? → fix pass (make reviewer RED tests green, **never edit them**; TDD-for-bugs for prose findings; re-emit the handoff); else inert
- [ ] PATCH-FUNNEL CHECK — dispatched on a certified patch? → funnel = record + existing realizations; TDD-for-bugs; ledger row → `in-progress`; patch-keyed handoff (`review_mode: patch` + `patch: patch-NNN` + `spec_slice_path` = the record); P3/P4 exceeded → HALT + row `escalated`, never widen; else inert
- [ ] READ FUNNEL — specs + VCs + system.md/ADRs + slice/"Done When" (+ `02` manifest, tokens if UI) loaded; spine not re-interpreted
- [ ] CAPTURE `baseline_commit` — `git rev-parse HEAD` recorded **before** any edit (initial commit first if none)
- [ ] REVIEW VCs — each row buildable? unbuildable → INFERRED with a cited reason (not dropped)
- [ ] IMPLEMENTATION ORDER — consumed from the spec/slice (not re-derived)
- [ ] BUILD — TDD RED-first (observed fail recorded) for unit/api rows; anti-tautology gate cleared; reuse-first; dep-safety; outcomes-not-ceremony; atomic commits
- [ ] TRACEABILITY — every VC → test:loc; every in-scope REQ → FULL/PARTIAL/NONE; every DM-ID → file:line
- [ ] HANDOFF — frontmatter (incl. `spec_slice_hash`, computed mechanically) + File List (== `git diff` names) + VC carry-forward (evidence state + repro + RED-note + oracle hash + non-EXECUTED reason) + REQ coverage map + attestations; `final_commit` captured
- [ ] Integrity: spine + realization docs untouched; no amendment row appended; every EXECUTED row's command exits 0; every non-EXECUTED row cites why; HALTs recorded

## Reads / Writes

**Reads (the realization funnel — never the raw spine):** `docs/architecture/specs/<feature>.md` (+ Verification
Contracts) · `docs/architecture/system.md` · `docs/architecture/adr/**` · `docs/design/approved/sprint-NN/`
(`manifest.md` + `prototype/`, if a UI slice) · `docs/design/design-system.md` · `docs/planning/sprints/sprint-NN.md`
(slice + "Done When" + frozen Gherkin) · `docs/spec/specification.md` (REQ registry — to key the coverage map, by ID)
· `.claude/rules/quality-guardrails.md` (if present) · `docs/quality/qa-report-sprint-NN.md` (**only** if a FIX
REQUIRED review exists — the fix-pass input, carrying the findings + the reviewer's committed RED tests). On a
patch: `docs/planning/patches/patch-NNN.md` (the certified record — the funnel input + the slice binding).
**Writes:** `src/**` · `_artifacts/exports/build-handoff-sprint-NN.md` (patch: `…-patch-NNN.md`) · on a patch, the
backlog's `## Patches` row **status cell only** (`in-progress` at build start; `escalated` on a P3/P4 HALT) ·
**appends** `docs/verification/<tech>.md` (**WS6** — a newly-verified, cited claims row for a verify-live tech; a
realization outside `docs/spec/**`, so no spine write) · optionally `Dockerfile`/`docker-compose.yml` + `sbom.json`.
**Never** writes `docs/spec/**`, `docs/architecture/**`, or `docs/design/**`.

## References (load when the step needs them)

- `references/build-discipline.md` — BUILD craft (steps 3–6): TDD RED-first (scoped) + the anti-tautology gate +
  reuse-first + hardened dependency safety + outcomes-not-ceremony + HALT conditions + the three-way drift-escalation.
- `references/build-handoff.md` — HANDOFF craft (step 7): the `baseline_commit` anchor + per-row evidence state +
  reproduction command + oracle hash + the REQ coverage map + the attestations, and the *why* of each field (how it
  feeds `05`).
- `templates/build-handoff.md` — the fill-in handoff skeleton.
- `shared/subagent-protocol.md` — the build → reviewer (`05`) contract: your handoff is the reviewer's sole seed;
  repo-root-relative.
- `shared/spec-amendment-protocol.md` — the tiers you *classify* against when escalating drift (you append no row);
  repo-root-relative.
- `shared/spine-boundary.md` — declaration vs realization (the keystone); repo-root-relative.
- `shared/live-source-verification.md` — verify a verify-live tech's API/config from `docs/verification/<tech>.md`
  (or live source) before building; the handoff row carries a `verified:` ref, never `INFERRED`; repo-root-relative.

## Next skill

After the handoff is written: invoke `/05-reviewer sprint N` — it loads **only** the handoff + the spec-slice paths
(never this conversation) and renders the SHIP / FIX REQUIRED / BLOCK verdict.
