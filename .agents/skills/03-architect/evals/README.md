# 03-architect evals

Follows **`/skill-creator`'s A/B method** (a homegrown `run_*.py`/`grade_*.py` is a Windows fallback
only). The input here is a **spine slice + the 02 design contract** (a spine + `sprint-01.md` +
`docs/design/approved/sprint-01/manifest.md`) — not a raw doc. For each case in [`evals.json`](evals.json), run two
arms and compare the skill's **lift**:

1. **with_skill** — a fresh agent loads `.agents/skills/03-architect/SKILL.md` and realizes the architecture for the
   first sprint (`init` + `sprint 1` together), writing under `docs/architecture/` and appending
   `docs/spec/amendment-log.json`. Because there is no interactive user, tell it to run autonomously **past both
   gates** (proceed without waiting; approve its own batched Tier-2 amendments so they land as `approved` rows), and
   to run the **Reconcile judgment pass from a fresh-context reconciler** (see *Reconciler isolation* below).
2. **baseline** — a fresh agent performs the same prompt with **no skill** (instructed to ignore framework files).
   Shows what the structured contract + the subagent-isolated Reconcile add over an ad-hoc architecture doc.

## Workspace setup (the input is a spine — seed it first)

Put workspaces **outside `.agents/skills/**`** (e.g.
`_artifacts/skills-eval/03-architect/iteration-N/<case>/<arm>/outputs/`) to avoid the `with_skill` write-refusal
heuristic. The agent's `outputs/` dir **is the project root** and must be **pre-seeded with the spine** so the skill
can read it and add the architecture beside it:

```
# seed cleanly — do NOT pre-create outputs/docs (cp would nest docs/docs)
mkdir -p <…>/<arm>/outputs
cp -r evals/fixtures/<case>/docs <…>/<arm>/outputs/docs
```

Seeding both arms identically also lets the grader prove the skill **left `docs/spec/capabilities/` untouched** and
wrote its challenge only as **structured amendment rows** (+ a resolving ADR).

## Grade (deterministic — no LLM judge, because the contract + the token check are objective)

```
python check_architecture.py --outputs <…/outputs> --case <clean-constraint|forbidden-token|underspecified-constraint>
```

It writes `grading.json` (`{expectations:[{text,passed,evidence}]}`) into `--outputs` and prints a pass/fail report.
Copy `grading.json` up to the arm root (`<arm>/grading.json`) so skill-creator's `eval-viewer/generate_review.py`
renders the verdict. For the static review:

```
python <skill-creator>/eval-viewer/generate_review.py <iteration-dir> --skill-name 03-architect --static <out.html>
```

## What the assertions check (the lift is STRUCTURAL + amendment-aware)

03-architect's value is the **structured architecture contract** the next skills consume **plus** the
subagent-isolated Reconcile — not prose architecture insight (a strong baseline also architects well; architecture
*beauty* is not graded). So the discriminating assertions are structural + amendment-aware: an arc42/C4 `system.md`
with a **strategic-DDD bounded-context map** that **references REQs**; a **MADR ADR registry** (a checkable
**Binds/Prevents/Rule**) + the `adr/README.md` index (contiguous `max+1` allocation); **feature specs** referencing
the sprint's REQs with **mechanically-gradeable Verification Contracts**; **REQ→spec and DM→spec coverage**; and the
**Reconcile rows** in `amendment-log.json`.

The one move that makes an *architecture* contradiction gradeable without a judge is the **token-in-named-field
set-match** (`check_architecture.py` recomputes it over the constraint token vs the realization's named fields — the
`system.md` stack, the ADR *Decision*): a planted, stated datastore that cannot satisfy a stated availability
requirement must be caught as a **Tier-2 gated row + a resolving ADR** (the tech-mandate flow), recomputed by the
grader to prove the catch was warranted. A baseline writes an architecture doc but not the arc42/C4/DDD shape
referencing REQs, the MADR registry + index, gradeable Verification Contracts + coverage, or the token-checked
amendment rows + resolving ADR — that gap is the lift.

**The 11 architecture-review heuristics (Pass 2) are the reconciler's reliability layer, NOT graded items** — exactly
as `02`'s Nielsen pass armed the critic but only the WCAG computation + the structured contract were scored. Pass 1
(deterministic) is what the grader scores.

## Fixtures (the variable under test is the `architecture-constraints` Datastore line)

Three **TeamPulse-derived** variants (reusing the 00/01/02 spine) that differ in **exactly one line** — the
`architecture-constraints.md` **Datastore** field — so any behavior delta is attributable to that line alone (the
`aurora-clean`/`aurora-contrast` isolation trick applied to architecture). All three share a stated **availability
requirement** ("two or more stateless instances + a separate worker share one datastore") that makes the datastore
decision load-bearing:

- **`teampulse-clean`** — `Datastore: PostgreSQL 16 (client-server)`. Compatible with the shared-store requirement →
  the natural architecture **honors** the envelope → the **false-positive** check (~zero amendments). Also verifies
  the token-check's **honored direction** (the stated datastore kept; no third-party IdP introduced).
- **`teampulse-sqlite`** — `Datastore: SQLite (embedded, no external DB server)`. Embedded SQLite **cannot** be the
  one shared store for multiple stateless nodes + a worker — a **computed contradiction**. The airtight discriminator:
  Reconcile must emit a **Tier-2 gated/approved row** citing it **+ a resolving ADR** naming a client-server DB (the
  tech-mandate flow), not silently swap or ship it.
- **`teampulse-underspecified`** — `Datastore: [NEEDS CLARIFICATION]`. The availability requirement forces a concrete
  client-server datastore the envelope never named → the **flesh-out** component: a **Tier-2 row + an ADR** that
  concretizes it.

### Why SQLite↔PostgreSQL, not the EU-residency / no-SSO plant

The design doc offered two forbidden-token candidates: TeamPulse's EU-residency / no-third-party-SSO mandates, or a
crafted "Datastore: SQLite" tension. **EU-residency and no-SSO are *required/forbidden* tokens that a correct
architecture simply *honors* — honoring yields no amendment, so they can't be the amendment-forcing discriminator.**
They are exercised instead as the **honored direction** inside the `clean` case. The **SQLite↔shared-store tension**
is a genuine constraint↔requirement conflict that *forces* the tech-mandate flow (amendment + resolving ADR), which
is what the `forbidden-token` case must grade — so it is the primary discriminator, isolated on one line against the
`clean` twin.

## Reconciler isolation (03's subagent debut)

03 is the first Reconcile skill whose **judgment pass runs in a context-isolated subagent**. In the `with_skill`
arm, spawn the reconciler from a **fresh** spawner (a real subagent where supported, else a fresh top-level
invocation) that receives **only** the realization + the slice's declarations — never the realization conversation —
and record its one-line **context attestation** in `docs/architecture/` (e.g. `system.md` §9). **Relax the harness
`<SUBAGENT-STOP>` for 03** (see `docs/eval-methodology/harness-reference/`) or the reconciler short-circuits. The
grader checks the **attestation's presence** (a deterministic, file-based proxy); the attestation is a
**declared-inputs statement, not proof of isolation** (`shared/subagent-protocol.md`) — a transcript-absence check
is an **evidence** layer only where the harness persists spawn transcripts, which this one does not — and Pass 2
stays **human-gated, never deterministically graded**.

## iteration-1

> **Stale-baseline note (2026-07-19):** the table below predates WS4 (D1–D6) and WS6 (S18), which grew the grader
> to **21 checks/case** — it is history, not the current baseline. The current baseline is the 2026-07-18
> re-baseline below.

| Case | with_skill | baseline |
|------|:----------:|:--------:|
| `clean-constraint` | **15/15** | 7/15 |
| `forbidden-token` | **15/15** | 4/15 |
| `underspecified-constraint` | **15/15** | 6/15 |

**with_skill passed every assertion on all three cases (45/45, 100%); baselines averaged 38% (17/45).** The
baselines were *strong on architecture craft* — each independently produced a sensible system design and **caught the
planted datastore conflict**: the `forbidden-token` baseline diagnosed the embedded-SQLite-vs-multi-instance
contradiction and even researched **libSQL/`sqld` server-mode** as a resolution; the `underspecified` baseline logged
a *pending* datastore amendment; the `clean` baseline reached for Postgres `SKIP LOCKED` exactly-once generation. But
**none produced the structured contract the next skills consume**: they wrote ADRs as `adr/ADR-0001-name.md` /
`decisions/` (not the canonical `adr/ADR-NNN.md` register with a MADR **Rule**), feature specs under `features/` (not
`specs/` with mechanically-gradeable Verification Contracts), and — decisively — logged their catch as an ad-hoc row
(`A-0001` / `pending`) or **prose**, not a schema-valid `AMD-NNN` / `approved` / `resolved_by`-an-ADR amendment via
the **tech-mandate flow**. The `with_skill` arms emitted exactly the right amendments — **1** Tier-2 `approved` row
for `forbidden-token` (SQLite→PostgreSQL, `resolved_by: ADR-002`) and **1** flesh-out row for `underspecified`
(`resolved_by: ADR-002`, constraint upgraded from `[NEEDS CLARIFICATION]`), and **0** for `clean` (the over-trigger
guard holding on a clean, honored envelope).

**03's subagent debut worked for real:** each `with_skill` arm spawned a **fresh-context general-purpose subagent**
for the Reconcile judgment pass (some spawned two — one for `init`, one for the sprint specs), each fed only the
realization + the declarations, each returning the protocol attestation (`realization conversation: not provided`)
recorded in `system.md` §9. **The lift is the structured contract + the amendment/ADR semantics, not architecture
insight** (per the framework's structural-lift principle). The static viewer is at
`_artifacts/skills-eval/03-architect/03-architect-eval-review.html` (gitignored run workspace).

The grader is additionally **validated against hand-built ideal outputs** (a with_skill-shaped realization per the
templates): all three cases reach **15/15**, and an absent/ad-hoc architecture fails the structural + amendment
assertions — so the discriminators are real, not vacuous.

## Re-baseline (2026-07-18, /21 grader)

Fresh with_skill arms on the current 21-check grader (the data-architecture regression bridge; design record §7.1):

| Case | with_skill |
|------|:----------:|
| `clean-constraint` | 20/21 |
| `forbidden-token` | **21/21** |
| `underspecified-constraint` | **21/21** |

The single miss — `clean`'s D1 (one §10 quality scenario written prose-only) — is a WS4 check the data craft never
touches, confirmed run-variance (the other two arms passed D1).

## Data cases (`data-modules` · `data-nogate`)

Phase-1 calibrated cases for the data-architecture craft (DA-T01–T08; design record:
`_artifacts/data-architecture-phase1-design.md`). Beacon-derived fixtures; graded by the focused
`grade_data_arch` path (`--case data-modules|data-nogate`), validated by `--self-test` (S18 + the data mutation
suite). The `data-modules` fixture arms the DA-T07 deletion→derived-reach pairing via a spine-level deletion
promise; `data-nogate` is the need-gate selectivity direction (declared-but-denied modules must be declined, not
realized). Known gap, noted not fixed here: `--case agent` has a fixture + grader path but no `evals.json` entry.

### iteration-data-1 (2026-07-19)

| Case | with_skill | baseline |
|------|:----------:|:--------:|
| `data-modules` | **14/14** | 5/14 |
| `data-nogate` | **11/11** | 6/11 |

with_skill passes every non-N/A check on both cases; baselines fail the structured contract + content clauses (a
strong baseline still need-gates correctly — the lift is structural). Three grader-bug-first triage fixes landed
during the run (DA-T04 exit-cost phrasing + "no datastore" recognition; selectivity ephemeral-in-memory). Run
record + triage: `_artifacts/skills-eval/03-architect/iteration-data-1/VALIDATION.md`.
