# Data-architecture Phase 1 — calibrated eval cases: design record

> **Status:** approved section-by-section 2026-07-19 (four clarifying decisions + three gated design chunks, each
> user-confirmed). **Consumes:** `_artifacts/data-architecture-phase1-continuation.md` (the launcher),
> `_artifacts/skills-eval/03-architect/smoke-2026-07-18/SMOKE-RESULT.md` (the Phase-0 greenlight + the S18 finding),
> `_artifacts/data-architecture-design.md` §5/§7.1/§9 (the teeth · the `/21` regression numbers · the follow-up this
> record resolves). **Next:** implementation plan (`superpowers:writing-plans`) + fresh-session execution on a fresh
> worktree; this record is the *what/why* — the plan carries the *how/steps*.

## 1 · Problem + goal

The data-architecture craft is merged and smoke-greenlit, but the calibrated `03-architect` eval suite carries **no
case that exercises it**: the DA-T01–T08 teeth have no deterministic graders, the suite's README still records the
stale `45/45` baseline, and the smoke exposed S18's Verify-live linkage silently no-oping on qualified labels
(DA-T08's enforcement gap). Goal: land the calibrated data eval cases **grader-first** — graders proven to bite
before any arm runs — plus the two fold-in fixes, as the separate change design-record §9 mandated ("never landed
with the doctrine they judge").

## 2 · Decisions (the four clarifying gates)

1. **Suite shape — extend the existing suite.** New `data-*` entries in `evals.json` + new per-case blocks, DA check
   functions, and a `_self_test_data` inside `check_architecture.py`, riding a focused grading path the way
   `--case agent` does. The S18 fix touches this file's shared helpers regardless; one grader file per skill stays
   the convention.
2. **Fixture family — 2 live cases, consolidated** (revised from the launcher's five after weighing full-suite-
   forever cost): `data-modules` (all modules, adopted direction) + `data-nogate` (need-gate selectivity, declined
   direction). The smoke proved the combined routing shape; the teeth are per-module, so a combined run still
   attributes failures.
3. **The declared-but-unrealized case lives in the self-test, not the live suite.** 03 has exactly two modes
   (`init`, `sprint N`) with Reconcile folded into each gate — no standalone reconcile invocation exists, and in a
   correct run of the natural modes a declared module never stays unrealized past the gate. The DA-T01–T03 pairing
   checks are graded on both live cases; their **bite** is proven by hand-built declared-but-unrealized degenerate
   trees in `_self_test_data` (the `_self_test_s18` pattern).
4. **`beacon-data` is enriched, not smoke-verbatim.** One extra coherent edit arms DA-T07's deletion→derived-reach
   pairing as a live REQUIRED-direction check (a conditional that would otherwise stay N/A on every live case — the
   exact silent-no-op class S18 just exposed). The N/A direction is still validated against the smoke's real
   outputs under their own spine.

## 3 · Scope + mechanics

**Branch:** fresh worktree off `main` (`.claude/worktrees/data-eval-cases`, branch `worktree-data-eval-cases`).
The locked `data-architecture-craft` worktree stays untouched. **No push (the repo has no remote); merge to `main`
only after explicit say-so.**

| File | Change |
|---|---|
| `.agents/skills/03-architect/evals/check_architecture.py` | S18 slug normalization · `grade_data_arch` focused path · DA check functions · `_self_test_data` · S18 self-test gains the qualified-label + case-mismatch degenerates |
| `.agents/skills/03-architect/evals/evals.json` | two new case entries: `data-modules`, `data-nogate` |
| `.agents/skills/03-architect/evals/fixtures/beacon-data/docs/**` | new fixture tree (beacon-agent derivative, four edits) |
| `.agents/skills/03-architect/evals/fixtures/beacon-nogate/docs/**` | new fixture tree (beacon-agent derivative, denial facts) |
| `.agents/skills/03-architect/evals/README.md` | `/21` re-record (append-style) + data-case documentation |
| `shared/live-source-verification.md` | one convention line: the Verify-live row label = the lowercase record basename |

**Teeth text stays verbatim** (DA-T01–T08 untouched — DA-T08 already delegates format to the S18 rule, whose single
home is `live-source-verification.md`). Product names appear nowhere in graders or fixtures' required tokens.

**Order is strictly grader-first:** S18 fix + degenerates → DA checks + `_self_test_data` (ideals + degenerates
bite) → re-validate on the smoke's real outputs → re-grade the saved webapp regression outputs (zero-token
no-drift proof) → fixtures → `evals.json`/README → A/B arms.

## 4 · Fixtures

**`beacon-data`** (case `data-modules`) — copy of `evals/fixtures/beacon-agent` + four coherent edits (1–3
reconstruct the smoke seed's shape):

1. `specification.md`: `- **Data:** retrieval(source-search) · grounded-writes(report-synthesis) · memory`.
2. `architecture-constraints.md` `## Data architecture`: the persistent, daily-growing retrieval corpus (queried
   before re-fetch; quality measured on the golden set backing REQ-002) + the per-topic source-reliability memory
   trigger, stated as "operator-correctable" **without** the PATCH-endpoint specifics the smoke arm fleshed out.
3. `agent-contract.md` §6 reconciled with the memory declaration (memory layer vs retrieval cache kept distinct).
4. **Enrichment:** a per-operator research-interest-profile memory aspect whose constraint line states only the
   **promise** — operators may request deletion of their profile — never the derived-reach answer. The declaration
   states the promise; the realization must bring the pairing. A fixture that spelled out "deletion must reach
   summaries/indices" would hand both arms the expected text and kill the discrimination. The same edit keeps
   `agent-contract.md` §6 coherent (the profile store listed as deletable memory-layer state) — an incoherent
   fixture would seed spine-inconsistency amendment noise from correct arms.

No `## Verify-live` section in the seed: the smoke proved the arm *proposes* it (Tier-2 + records) when making
volatile-class picks — that is DA-T08's live path.

**`beacon-nogate`** (case `data-nogate`) — copy of `beacon-agent` + denial facts:

- `specification.md`: `- **Data:** retrieval(handbook-lookup) · memory`.
- `## Data architecture` facts deny every trigger: the handbook is ~40 small, stable, quarterly-updated reference
  documents (fits comfortably in context, low query volume → Stage-0: no retrieval; cache-and-stuff); every
  research question is independent and operators explicitly value a from-scratch read (reproducibility) → no
  Gate-0 memory trigger.
- `grounded-writes` is **not declared and not asserted either way** — presumptive under `agent-system`, so a
  correct arm may still gate report-synthesis; grading its absence would false-fail correct arms.
- `agent-contract.md` §6 stays **verbatim** ("nothing persists") — under the denial facts that text is coherent
  with the expected declines; the fixture needs no reconciling edit, and adding one would weaken the case.

The always-on §1 datastore rubric still fires on `beacon-nogate` (`init` walks it regardless), so the case carries
positive DA-T04 content — a selectivity probe, not a pure-absence case. The two cases mirror the suite's
`clean`/`forbidden` twin logic at module altitude: adopted direction vs declined direction, the delta attributable
to the constraint-file facts alone.

## 5 · The grader — `grade_data_arch` + per-tooth keying

Data cases do not re-run the 17-check webapp contract (TeamPulse's job) nor the agent case's topology-economics
checks. **Core (both cases):** `system.md` present · ADR registry + index · valid `amendment-log.json` ·
reconciler context-attestation · ≥1 feature spec referencing a sprint REQ with a Verification Contract (the agent
path's spec+VC logic, reused — without it a zero-spec arm would pass `data-nogate`, where T02/T03 never run) ·
**`docs/spec/capabilities/**` content-identical to the fixture** (EOL-normalized compare, not byte-exact — the
threat is content edits, not line endings, and byte-exact invites the known Windows CRLF churn; new — the grader
knows its fixture dir, so the smoke's manual REQ-text eyeball becomes deterministic).

**Two keying principles:**

1. **DA-T01 rides bare token-presence.** Each declared `Data:` value's token must appear in the realization blob.
   On `data-modules` the realization satisfies it; on `data-nogate` the explicit decline satisfies it; **silent
   omission fails both** — §0's "says so explicitly, never by silent omission", with zero decline-vocabulary
   matching.
2. **Absence checks read commitment fields, never prose.** A decline legitimately *mentions* stores in negation,
   so `data-nogate`'s no-adoption check reads only structured commitment loci — Data-model tables, Components
   tables, ADR `Chosen:` lines — for vector/embedding-index/memory-store commitments. The token-in-named-field
   principle, applied to the absence direction.

| Check | Case | Keying (deterministic) | Conditional gate |
|---|---|---|---|
| DA-T01 pairing | both | declared value's token present in the realization blob | none |
| DA-T02 eval floor | `data-modules` | an eval-suite VC row whose `dataset:` path resolves on disk | unconditional — the fixture's facts make retrieval undeniable |
| DA-T03 admission rule | `data-modules` | the admission chain: ≥2 of schema/referential/business-rule + admit/commit within one paragraph | unconditional |
| DA-T04 datastore ADR | **both** | the ADR whose *Decision* names a DB token (reusing `DB_CLIENT_SERVER`/`DB_EMBEDDED`): ≥2 Considered Options · REQ-ref + rubric-dimension marker in drivers · a `Review-Trigger:` field that is not "review periodically" · exit-cost/reversibility statement · durable-vs-vendor split | none — §1 is always-on |
| DA-T05 retrieval | `data-modules` | stage declared (`Stage 0–6`) · chunking params (a token size + an overlap) or an explicit no-chunking rationale · embedding dims + reindex trigger · k-consistency marker | why-not-simpler required only when the committed stage ≥3 (gated on the stage number itself) |
| DA-T06 grounding | `data-modules` | named ground-truth source line · a number near threshold/tolerance + an action verb (block/drop/refuse/regenerate/route) · fallback per failure mode | driver-layer read-only clause is fixture-N/A (Beacon issues no LLM queries); its required direction is proven in the self-test |
| DA-T07 memory | `data-modules` | Gate-0 trigger cited · per-kind substrate · lifecycle floor (TTL/decay) · sharing+authz named together (required — Beacon is multi-agent) · deletion→derived-reach **required** | deletion pairing gates on the fixture's planted promise line — structure, not vocabulary |
| DA-T08 verify-live | both | the existing S18 check, post-normalization | as today |
| No-adoption + amendment bound | `data-nogate` | commitment-field absence (principle 2) + ≤1 amendment rows (the clean-constraint tolerance; one defensible line-narrowing row allowed) | none |

Each tooth is one compound check row with per-clause evidence (the D2 style). Approximate counts: `data-modules`
~14 rows, `data-nogate` ~11.

**Two flags decided consciously up front:**
- **DA-T04's durable-vs-vendor clause is the fuzziest keying.** If grader-first validation cannot make it bite
  without false-failing hand-ideals, that one sub-clause demotes to reconciler territory, recorded as such.
- **`Stage N` / `Gate-0` markers are doctrine vocabulary** — the discriminating assertion *is* the structured
  contract the doctrine mandates (the structural-lift principle, same as MADR `Rule` or `AMD-NNN` schema rows),
  not corpus leakage.

## 6 · Self-tests + validation ladder

`_self_test_data` (tempdir trees, `_self_test_s18` style):

- **Ideal tree** — all teeth present → every check passes. **Degenerates are single-element deletions of this one
  tree** (copy, remove exactly one clause): half the hand-built content, and each degenerate isolates exactly one
  check's bite — the mutation principle.
- **Declared-but-unrealized degenerates** (decision 3's home): declared value, no realization (T01 fires) ·
  realization without a resolving dataset ref (T02) · no admission chain (T03).
- **Content degenerates:** 1-option datastore ADR / missing Review-Trigger / missing exit-cost (T04) · no
  dims/reindex (T05) · threshold without action (T06) · no lifecycle floor (T07) · deletion-promised-but-no-reach
  (T07 fails) **and** deletion-not-promised-no-reach (T07 passes — the N/A direction) · an LLM-SQL component with
  no driver-layer rule (T06's conditional, required direction) · a substrate commitment on a nogate-shaped tree
  (no-adoption fires).
- **S18 additions:** the real-output-shaped qualified label (`**BGE-M3 (embedding model):**`) must resolve and
  validate; an uppercase-label/lowercase-record pair covers the latent case-mismatch miss.

**Validation ladder, in order:** self-tests green → the smoke's real tree (expect S18 flips N/A→PASS — its
citations genuinely resolve; DA checks pass with the deletion pairing N/A under the smoke's own spine) → re-grade
the **saved** webapp regression outputs (must stay 20/21 · 21/21 · 21/21) → anti-tautology grep of the diff for
smoke-output verbatims (the grader must never require "Source Index snapshot"-class phrasings as tokens) → only
then fixtures and arms.

## 7 · The two fold-in fixes

1. **S18/DA-T08 label linkage.** *Doctrine:* one line in `shared/live-source-verification.md`'s declaration
   bullet — the row label MUST be the lowercase record basename, descriptive text after the colon
   (`- **bge-m3:** BGE-M3 embedding model — docs: … · source: …`). *Grader:* `verify_live_techs` strips a trailing
   parenthetical and lowercases the slug; basename-matching becomes case-insensitive. The convention makes future
   arms write the linkable form; the normalization keeps the grader honest about arms that don't.
2. **Stale-baseline README — append, don't rewrite.** Iteration-1's `45/45` table stays as history with an
   explicit stale note (predates WS4 D1–D6 + WS6 S18; the grader has since grown to 21 checks/case); the
   2026-07-18 re-baseline lands beneath it at `/21` (clean 20/21 · forbidden 21/21 · underspecified 21/21; the D1
   miss noted as confirmed run-variance).

**Noted, not acted on:** `--case agent` exists in the grader and `beacon-agent` in fixtures, but `evals.json` has
no agent entry — recorded in the README's data-case section as a known gap; registering it is out of scope here.

## 8 · A/B run plan + success criteria

- **Arms:** `with_skill` = general-purpose **Sonnet** subagent (two roots: FRAMEWORK ROOT = repo root, PROJECT
  ROOT = the seeded `outputs/`; load + follow `03-architect/SKILL.md` in full; `init` then `sprint 1`; autonomous
  past both gates, own batched Tier-2s landing `approved`; real fresh-context `fsd-reconciler` Pass-2 +
  attestation in `system.md` §9; never touch `capabilities/**`). Baseline = Sonnet, same prompt, ignoring
  framework files. **2 cases × 2 arms = 4 runs**, one at a time (`--num-workers 1`), `claude.exe`, utf-8.
- **Case prompts stay neutral** (the TeamPulse shape: "the Beacon spine is in docs/spec/… run `03-architect init`
  then `sprint 1`") — no teeth restated, or the eval tests the prompt instead of the doctrine.
- **Workspaces:** gitignored `_artifacts/skills-eval/03-architect/iteration-data-1/<case>/<arm>/outputs/`, seeded
  from the fixtures; a `.gitattributes` (`* text=auto eol=lf`) in each workspace against CRLF grader churn.
- **Grading:** `check_architecture.py --outputs … --case data-*`; `grading.json` copied to arm roots;
  skill-creator's `generate_review.py` static viewer for the side-by-side.
- **Success criteria:** with_skill passes every non-N/A check on both cases; baselines fail the pairing/content
  discriminators (the lift is the structured contract); saved-output re-grades byte-stable; both self-tests green;
  the S18 flip demonstrated on the smoke tree. Any check a *correct* arm fails is a grader bug first, doctrine
  question second — triaged before any fixture tweaking.
- **Record:** README gains the data-case iteration table; a run record lands beside the workspaces (`git add -f`
  for anything under `_artifacts/` that must survive the gitignore); commits stay on the worktree branch.

## 9 · Simplicity-pass record (2026-07-19)

Reviewed on request for "as simple as possible, not simpler."
**Tightened:** capabilities check byte-exact → content-identical (EOL-normalized; the threat is content edits, not
line endings) · self-test degenerates = single-element deletions of one ideal tree (the mutation principle) ·
fixture coherence pinned in both directions (`beacon-data` updates `agent-contract.md` §6; `beacon-nogate` keeps it
verbatim).
**Added — a simpler-than-possible hole:** the ≥1-spec-with-VC core check (a zero-spec arm would otherwise pass
`data-nogate`, where T02/T03 never run).
**Kept, deliberately:** two live cases (the declined direction is doctrine — cutting to one loses the over-trigger
guard) · both denied modules in `beacon-nogate` (two gate probes, zero extra runs) · DA-T04's durable-vs-vendor
sub-clause on the build-then-demote path (grader-first validation decides, not prediction) · the full degenerate
set (an unproven check is the S18 class) · A/B with baselines + the static viewer (the suite's method).

## 10 · Out of scope

No doctrine/teeth edits beyond the one Verify-live convention line · no live drift-variant case (revisit only if a
future 03 mode makes reconcile-over-existing-tree a first-class path) · no agent-case `evals.json` registration ·
no `00-discovery` or other-seat changes · the wave-2 diagnostic track stays parked.

## 11 · References

Launcher: `_artifacts/data-architecture-phase1-continuation.md` · smoke: `_artifacts/skills-eval/03-architect/
smoke-2026-07-18/SMOKE-RESULT.md` (+ `with_skill/outputs/` — the real-output calibration set) · craft:
`.agents/skills/03-architect/references/data-architecture.md` (§0 need-gate · DA-T01–08) · pairing lints:
`.agents/skills/03-architect/references/reconcile-architecture.md` §1b · routing: `shared/agentic-profile.md`
§ The Data line / § eval-suite · S18 doctrine: `shared/live-source-verification.md` · design record:
`_artifacts/data-architecture-design.md` (§5 teeth · §7.1 `/21` numbers · §9 the follow-up this resolves).
