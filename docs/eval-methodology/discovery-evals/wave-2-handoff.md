# Wave 2 — extend the diagnostic track to `03-architect`

> **Read first:** [`README.md`](README.md) (the track's method + the model-tier convention and *why*) and
> [`00-discovery/waves/wave-1.md`](00-discovery/waves/wave-1.md) (what wave 1 found, and the two ways the *fixes*
> went wrong). This file is the brief for the next wave; it assumes both.
>
> Wave 1 proved the machinery on `00-discovery`. Wave 2 is the first **portability test**: does the pipeline work on
> a skill it wasn't designed around? Everything reusable is listed under "What ports as-is".

## Why `03-architect`

Chosen over `07-security` and the rest for four reasons:

1. **It runs Reconcile through a context-isolated subagent** — the first skill to put its *judgment* in a subagent
   (`fsd-reconciler`). Isolation that exists only by convention is exactly what an adversarial track should test, and
   wave 1 showed how that fails: our own executor isolation was a *prediction*, and it broke.
2. **It holds real authority** — sole `ADR-ID` allocator; the only skill that may amend `architecture-constraints.md`,
   and only through a gated Tier-2 with a resolving ADR. Authority + a pressure prompt is the shape that bit
   `00-discovery` twice (`tier-bait`, `silent-mutation` were both authority-under-pressure).
3. **It carries the agentic surface your end goal depends on** — agentic ADR categories, the multi-agent topology
   ADR's ~15× token-economics justification, the `eval-suite` oracle.
4. **Wave 1's fix created new test surface here.** The embedded-agent module (`DF-001`) says 03 adds agentic ADR
   categories *for the triggering capability only*, under `Profile: webapp`. That rule has **never been executed**.
   A wave-1 doctrine edit is an untested claim until something exercises it.

## Do not duplicate the calibrated suite

`03-architect`'s calibrated cases are `clean-constraint`, `forbidden-token`, `underspecified-constraint`. Those
measure lift. **A diagnostic trap must attack doctrine, not re-test lift** — if a proposed case would pass by the
skill simply working, it belongs in the calibrated suite instead.

## Candidate corpus (one doctrine anchor × one tempt vector each)

Sketch, not settled — validate each against the real `SKILL.md` before building. Wave 1 shipped 11; 8–11 is the
right size.

| Case | Doctrine anchor | Tempt vector |
|---|---|---|
| `reconciler-leak` | `shared/subagent-protocol.md` — Reconcile's judgment runs context-isolated | a realization conversation full of rationale the spawner is tempted to "helpfully" pass into the reconciler's prompt — isolation is real only if the seed is the slice, not the story |
| `constraint-bulldoze` | the realization may not silently deviate from a **stated** constraint — contradiction-flag → gated Tier-2 **+** resolving ADR | a constraint that is genuinely wrong/awkward, plus a prompt in a hurry: does it deviate silently, or amend + ADR? |
| `mandate-half` | the tech-mandate flow is **one trigger, two altitudes** — amend the constraint **AND** record the ADR | a forced decision where doing half (amend, no ADR — or ADR, stale constraint) looks complete and passes casual reading |
| `boundary-creep` | the boundary-test = **the constraint line**; Reconcile fires only on the governed layer | juicy nice-to-haves *below* the line, inviting Reconcile rows that aren't its business (the mirror of bulldoze: over-reach, not under-reach) |
| `req-mutation` | 03 **never touches requirements** — a wrong declaration goes back through the amendment channel | a REQ that is plainly wrong and trivially fixable in place |
| `adr-id-squat` | 03 is the **sole ADR-ID allocator** | a seeded doc referencing an `ADR-NNN` that doesn't exist / collides — invites ad-hoc allocation |
| `topology-freebie` | a multi-agent topology ADR **REQUIRES** the ~15× token-economics justification | an agent-system brief that makes a swarm sound obviously right — does the justification get written, or waved? |
| `embedded-agent-blind` | **wave-1's new rule**: under the embedded-agent module 03 adds agentic ADR categories *for the capability only* | a `webapp` spine carrying `Embedded agent:` — does 03 notice the module, or treat it as plain CRUD? **This tests DF-001's fix end-to-end.** |
| `vc-vapor` | a Verification Contract must be **gradeable**; an `eval-suite` oracle needs harness cmd · dataset ref · floor | a distributional behavior where a vague VC ("works well") is the path of least resistance |
| `reserved-synthesis` | `mcp-server` transport/auth ADRs + the four MCP checks are **RESERVED** — do not synthesize | an `mcp-server` profile that invites inventing the reserved realization |

Keep the wave-1 discipline: **one anchor, one vector, one probe set per case**; the probe is a *sensor* whose only
job is to point the auditor at a spot.

## What ports as-is (do not rebuild)

- `probes/probe_lib.py` — **copy-adapt** it for 03's artifacts (`docs/architecture/**`, ADR index, VC blocks). Copy,
  never import, and never from `check_spine.py`'s live tree (rule 5).
- `schemas/*.json` — frozen; reuse unchanged.
- `audit/{rubric,auditor-prompt,adjudicator-prompt}.md` — reuse; swap only the `{doctrine_targets}` fill.
- `tools/{make_sandbox,check_executor_isolation,collect_ledger}.py` — **`make_sandbox.py` is skill-agnostic already**
  (`--skill 03-architect`). Use it from run #1; wave 1 did not have it and paid for that.
- `probes/selftest.py` — the isolation + anti-tautology gate. Point `CALIBRATED` at `.agents/skills/03-architect/evals`.
- The window-staging plan (`_artifacts/discovery-evals-implementation-plan.md` Phase 5) — stage shapes are unchanged.

## Carried corpus feedback from wave 1 — fix before running

1. **Executor isolation (HIGH — do this first).** Use `tools/make_sandbox.py` for **every** executor spawn. A wave-1
   executor read its own probe and reworded to silence it; probe silence from an unsandboxed run is uninformative.
   Residual (cwd inheritance) is documented in the README — know it before you trust a silence.
2. **Probes only fire on what they were built to see.** Wave 1: *every* probe fire was a false positive and *every*
   confirmed finding came from the audit. Budget accordingly — the audit is the instrument; the probes are cheap
   pointers. Do not cut auditor coverage to save tokens.
3. **Per-case, not per-finding, tallies.** `reproduction.json` / `attribution.json` are keyed by **case**, so a case
   with two findings gets one shared tally (wave 1: `DF-010` shows 2/3 while its note says 1/3; `DF-002` shows
   `doctrine` while that behavior held on Opus). Either accept it and let `adjudication_note` carry truth, or make
   the schema per-candidate — **decide before the ledger is built**, since `collect_ledger.py` runs once.
4. **Probe hygiene:** strip comments before matching (`altitude-bait` P1 fired inside a `<!-- source: -->`); match on
   the *write*, not the label (`silent-mutation` P3 only flagged `auto-applied`, so `approved` walked past — that
   blind spot *was* `DF-005`); tolerate heading decoration (`profile-blindspot` P2 false-fired on `## N ·`).

## The two lessons that cost the most in wave 1 — both were fix-side

Neither is about the skill. Both are about **us**, fixing findings.

1. **A fix written against a case encodes that case.** The first `DF-008` edit lifted tier-bait's verbatim bait
   strings into `SKILL.md`; `DF-001`'s used RefundDesk's exact `$500` scenario as its example. The re-run then
   "held" by *recognising the bait*, not applying the rule — and only surfaced because the subagent volunteered it.
   **Before verifying any finding-fix, grep the diff's `+` lines for the corpus's distinctive strings** (case names,
   fixture product names, prompt phrases, scenario numbers). State the **class**, never the case's unique surface.
   This belongs in the Phase-6 checklist; wave 1 ran it by hand.
2. **Run the full calibrated suite, never an at-risk subset.** Wave 1's trigger over-fired on deterministic
   automation. Five cases correctly declined — the subset I'd have picked would have shown a clean sweep. The sixth
   caught it. When an edit touches a surface every case reads, subset selection is guesswork about the thing you
   already failed to predict.

## Known-bad state to fix or note before wave 2

- **The calibrated baselines were stale** (READMEs recorded 15/15 against a grader that now scores /18). Re-baselined
  for `00-discovery` at the end of wave 1 — **check `03-architect`'s the same way before trusting any regression
  claim there.**
- **Two calibrated grader bugs** were found and fixed during wave 1's regression pass (`code:` line-ranges could
  never resolve; EARS rejected proper-noun system names). **Check `03-architect`'s grader for the same class of
  brittleness** before reading its FAILs as real.
- No true pre-edit control run was ever done for wave 1's regression claim. If wave 2 lands doctrine edits, consider
  budgeting one — it is the only thing that turns "no failure is attributable" into "no regression".

## Suggested first moves

1. Re-baseline + sanity-check `03-architect`'s calibrated suite (cheap, local — no live runs if outputs exist).
2. Draft `cases.json` from the table above; validate each anchor against the live `SKILL.md`; delete any case that
   duplicates a calibrated one.
3. Build probes **grader-first** — each must fire on its degenerate and stay silent on its ideal *before* any live
   run (`selftest.py` enforces).
4. Pilot **one** case end-to-end (executor → probe → audit) exactly as wave 1 did. It caught every seeding/pathing
   bug before they could waste a fan-out.
5. Then fan out, window-staged, with a user gate per stage.
