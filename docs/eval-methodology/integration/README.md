# Cross-skill integration evals (§10 — the final discriminating pass)

The **cross-skill** safety net the per-skill unit evals cannot provide — each of those isolates **one** seat; these
grade the **composition**, the handoffs a *later* seat mechanically reads. Deterministic grader, **no LLM judge**
(the locked framework doctrine). Covers the master-plan §Verification surface as five `check_integration.py --case`s:

| Case | Plan test | What it proves |
|------|-----------|----------------|
| `spec-first` | **Test 1** (+ 3/5 composed) | the chain `00 intake → 01 → 02 → 03 → /status` composes: spine populated, registry↔leaf integrity, coherent REQ-ID allocation across seats, the planted Tier-2 surfaced+resolved (gated row + resolving ADR — never silent prose), backlog+frozen snapshot, handoff fidelity (manifest DM → spec coverage), the retired-artifacts guard, and `/status` routing on the real end-state. |
| `governance` | **Test 3** | the two governance-consuming seats **agree** on the same chain-produced state: `/status` routes to *resolve* **and** `06` ends **BLOCKED** on a deferred amendment + a surviving `[NEEDS CLARIFICATION]` marker. |
| `spine-collapse` | **Test 4** | the **intent-anchoring hedge**: after an upstream constraint pivot + a `00` re-run, the spine regenerates anchored to the unchanged charter JTBD, the registry stays **integral** through the pivot (no shatter), and the pivot is **logged** as an amendment (not a silent rewrite). |
| `isolation-chain` | **Test 2** | a **fresh `05`** dispatched from the pipeline reviews a **built slice it never built** — attestation present + valid, reviewed-exactly-the-handed-diff anchor, caught the planted violation. |
| `agent-chain` | **§10 fifth leg (5.5a)** | the **agent-system composition** `00 profile+contract → 01 → 03 topology+eval-suite VC → 04 → 05 floors → status`: the profile propagates, the agent-contract is complete, an eval-suite VC row reaches **EXECUTED** with grader-bites, the qa tally is present + floor-consistent, a topology ADR carries its **~15× economics** justification, the router is agent-aware. **Grader + hand-ideal + 3 degenerates built; the LIVE six-seat run is DEFERRED (5.5b).** |
| `verify-live` | **WS6 sixth leg (6.6)** | the **live-source verification chain** `00 declares+seeds → 03 cites → 04 verifies → 06 gates`: one declared verify-live tech flows coherently across the chain, anchored on a single `docs/verification/<tech>.md` record (VL1 declared+cited/no-orphan; VL2 ADR `Verified-against`; VL3 handoff `verified:` EXECUTED; VL4 06 G11 PASS; VL5 record version current vs the manifest). **Grader + hand-ideal + 4 degenerates built; the LIVE 00-seed A/B (fetch+cite vs confabulate) is DEFERRED (6.6b).** |

**Test 5 (roll-up)** is the committed per-skill greens (each skill's `evals/README.md`) plus this file — pointed at,
not re-run.

## The keystone — the chain is already latent in the unit fixtures

`00-discovery`'s `rich-spec/PRD.md` **is** the TeamPulse PRD; feeding it through `00 intake` yields a spine that
structurally matches `01-planner`'s `teampulse/docs/spec/**`, which `02/03/05/status` all consume. **One domain
threads the whole chain**, so the integration grader **reuses the unit graders' proven logic** (`check_spine`
registry↔leaf, `check_backlog` ledger, `check_architecture` Tier-2/ADR + DM/REQ coverage, `check_status`
integrity/routing) and **composes `/status` as the integrity+routing oracle** rather than re-deriving it. The planted
Tier-2 is the `03-architect` `teampulse-sqlite` mechanism (embedded SQLite mandated **and** a multi-instance
shared-datastore required — a computed contradiction), seeded *latent in the comprehensive spec* so it must surface at
`03`'s Reconcile.

## Files

```
build_fixture.py        # seeds a workspace per case (spec-first: the PRD only; governance/spine-collapse: composed
                        #   from the spec-first ideal + a small overlay). Self-checks each seed's planted condition.
check_integration.py    # the deterministic grader — one grade_* per case (see the table above); composes /status.
validate_grader.py      # grader-validation: hand-ideal (all pass) + degenerate negatives (each fires its target).
fixtures/
  spec-first/PRD.md            # the comprehensive seed (latent SQLite Tier-2 plant; decisive => marker-free spine)
  governance-seed/             # overlay: restored REQ-008 marker + a deferred AMD-003 (pre-run deltas)
  spine-collapse-seed/         # overlay: the charter (the macro-loop anchor), pre-pivot
  _ideal/<case>/               # the hand-ideal COMPOSED end-state per case (the positive control for validation)
```

Run-workspaces live **outside** `.agents/skills/**` and under the gitignored `_artifacts/skills-eval/integration/`.

## Grader-validation (the safety net — chain-free, deterministic)

Before any live run, every case's grader is proved **neither over-strict** (a hand-ideal composed state passes every
assertion) **nor vacuous** (each degenerate composed state fires its target assertion). This is the
`feedback_grader_validate_on_real_outputs` + `feedback_mutation_grader_robustness` discipline applied to a
**composition**. Run it all with **no skill execution**:

```
python validate_grader.py --case all      # or --case spec-first|governance|spine-collapse|isolation-chain|agent-chain|verify-live
```

| Case | ideal | degenerate negatives → target that fires |
|------|:-----:|------------------------------------------|
| `spec-first` | **9/9** | `broken-registry`→Inv2 · `silent-swap`→Inv4 · `retired-artifacts`→Inv7 · `dropped-req`→Inv3 · `missing-gemini-bridge`→Inv9 |
| `governance` | **7/7** | `gov-ships`→G3 · `gov-06-deployed`→G4 · `gov-missed-blockers`→G2 · `gov-06-resolved`→G7 |
| `spine-collapse` | **5/5** | `sc-charter-drift`→SC1 · `sc-shatter`→SC2 · `sc-dangling`→SC3 · `sc-silent-pivot`→SC4 · `sc-not-applied`→SC5 |
| `isolation-chain` | **6/6** | `ic-rubber-stamp`→IC4 · `ic-no-attestation`→IC2 · `ic-baseline-mismatch`→IC6 |
| `agent-chain` | **6/6** | `ac-missing-contract`→AC2 · `ac-floor-fail-ship`→AC4 · `ac-topology-no-justification`→AC5 |
| `verify-live` | **5/5** | `vl-orphan-record`→VL1 · `vl-uncited-claim`→VL1 · `vl-stale-version`→VL5 · `vl-inferred-build-claim`→VL3 |

> Validation surfaced two real grader bugs a happy-path-only check would have shipped: the marker regex
> `\[NEEDS CLARIFICATION\]` never matched the canonical `[NEEDS CLARIFICATION: …]` colon form (the marker-free
> `spec-first` fixture hid it; `governance` exposed it), and an SC1 JTBD regex with literal spaces missed the
> markdown-bold charter. Both fixed; the fix is what makes the degenerate-negative discipline worth its cost.

`isolation-chain` validates only the **cross-seat isolation** properties (IC1–6). The FULL built-slice review grading
(oracle re-run, anti-tautology litmus, ledger↔verdict) reuses `05-reviewer`'s `check_review.py` — already validated in
`.agents/skills/05-reviewer/evals/README.md`; the live procedure below drives it.

## Live-run procedure (the demonstration — a scripted multi-skill run)

A chain does not fit skill-creator's one-prompt-per-arm mold; it runs as **sequential fresh subagents sharing one
workspace** (the fresh-spawner + handoff-via-artifacts doctrine — no seat inherits a prior seat's reasoning; the
handoff is strictly the shared spine). Relax the harness `<SUBAGENT-STOP>` for `03`/`05`. Each stage is dispatched
seeded with **only** the workspace path + "load skill `<NN>`, run `<verb>`".

**`spec-first`** (workspace `<ws>`):
```
python build_fixture.py --case spec-first --out <ws>        # seed: PRD.md only (+ git root)
# fresh subagent: load .agents/skills/00-discovery/SKILL.md, run `intake` over <ws>/PRD.md    -> the spine
# fresh subagent: load .agents/skills/01-planner/SKILL.md,   run `decompose`                  -> backlog + sprints
# fresh subagent: load .agents/skills/02-designer/SKILL.md,  run `sprint 1`                    -> design + manifest
# fresh subagent: load .agents/skills/03-architect/SKILL.md, run `sprint 1` (approve the SQLite→client-server Tier-2 gate)
# fresh subagent: load .agents/skills/status/SKILL.md,       run `/status`                     -> CLAUDE.md + AGENTS.md
python check_integration.py --outputs <ws> --case spec-first
```
The Tier-2 gate is **pre-approved in the stage-4 dispatch prompt** (the `06` precedent — an eval pre-grants the single
human gate so the chain does not hang), approving SQLite→client-server so the row lands `approved` + a resolving ADR.

**`governance`** — `build_fixture.py --case governance` → fresh `status` then fresh `06-release sprint 1` → grade.
**`spine-collapse`** — `--case spine-collapse` → apply the pivot (edit `architecture-constraints.md` Regions EU→EU+US)
→ fresh `00-discovery reflect` → grade. **`isolation-chain`** — stage a defective built slice via
`python .agents/skills/05-reviewer/evals/build_fixture.py --case defective --out <ws>` → fresh `05-reviewer sprint 1`
→ grade (this grader for IC1–6, `05`'s `check_review.py --case defective-fix` for the full review).

## iteration-1 (live)

Every leg was run **live** — real fresh subagents driving the actual skills over the seeded workspaces (relaxed
`<SUBAGENT-STOP>` for `03`/`05`), then graded by `check_integration.py`. **All four green:**

| Leg | Live result | What the live run demonstrated |
|-----|:-----------:|--------------------------------|
| `spec-first` | **8/8** | the full `00→01→02→03→/status` chain composed. `03`'s Reconcile caught the SQLite-vs-shared-store contradiction and surfaced **AMD-002** (tier 2, `approved`, `resolved_by: ADR-002` whose Decision names **PostgreSQL**) + amended the constraint — not a silent swap. `/status` routed to `/04-builder`, read-only (only `CLAUDE.md`+`AGENTS.md` written). |
| `governance` | **7/7** | `/status` (routes to `/00-discovery reflect`) **and** `06` (BLOCKED, nothing deployed, cites AMD-003 + the marker) gated the SAME state — cross-seat agreement, with `06` blocking on a **SHIP** verdict purely on the spine. |
| `spine-collapse` | **5/5** | a live `00 reflect` processed the residency pivot: logged **AMD-004** (tier 2 `approved`), amended Constitution item 4 + the constraint, left the REQ registry byte-identical and the charter JTBD untouched — regenerated, did not shatter. |
| `isolation-chain` | **6/6** + **13/13** | a fresh `05` reviewed a built slice it never built → **FIX REQUIRED**, caught all three plants (grouping bug + tautological test + fabricated coverage), committed a reproducing RED test, attestation `build conversation: not provided` valid, `baseline_commit` matched. Full built-slice grading via `05`'s `check_review --case defective-fix`. |

**The live runs stress-tested the harness in ways the hand-ideals could not** — and it held:

- **Real decomposition variance.** The live `00` made a legitimately different choice than the seeded unit fixtures:
  it treated magic-link as a pure *constraint* (minted **no** derived auth REQ) and numbered `REQ-007`=digest-
  generation, so `digest.md` holds REQ-007–010. This broke invariant 5's original hard-coded build-order anchors
  (`REQ-007`=auth-foundation, from the seeded fixtures) — so the anchor was made **numbering-agnostic** (the `team`
  domain precedes the `digest` domain, by registry File, not REQ-ID). A single-skill eval never exposes this because
  its spine is seeded fixed; the integration chain does.
- **Cross-seat ID allocation.** `02`'s Reconcile emitted its own amendment (`AMD-001`, a WCAG-floor flesh-out); `03`
  then correctly allocated `AMD-002` (max+1, preserving `AMD-001`). The grader filters Tier-2 rows by the datastore
  tokens, so it binds to the SQLite amendment regardless of which id it landed on.
- **False-positive control across the chain.** `02` declined to invent design-intent conflicts on a clean intent
  (one legitimate a11y flesh-out, no cry-wolf); `03`'s fresh reconciler independently confirmed exactly one Tier-2
  contradiction and declined to add more. The composition did not manufacture scope.

Run workspaces: `_artifacts/skills-eval/integration/iteration-1/<case>/outputs/` (gitignored). The chain was driven
as sequential fresh-subagent dispatches per the procedure above; each seat's summary confirmed read-only-w.r.t.-spine
where required and the handoff-via-artifacts discipline (no seat inherited a prior seat's reasoning).
