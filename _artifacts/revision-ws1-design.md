# WS1 Design — Delta Path (patch lane) + Standing Gates (verify script)

> Revision workstream 1 of 4 from the 2026-07-06 framework review (§5.1, §6.3).
> Status: **APPROVED** (user, 2026-07-06); open questions resolved to proposed
> defaults. Research grounding:
> ITIL 4 standard-change pre-authorization + segregation of duties · Kanban expedite
> class (WIP-limited) · Ship/Show/Ask (the no-guardrail counter-example) · DORA
> uniform-pipeline doctrine · OPA/policy-as-code blast-radius gating · BMAD "Quick Flow"
> (the closest precedent: zero-blast-radius routing, hard size gate, adversarial
> subagent review preserved on the fast lane).

---

## Problem

The framework has exactly one road: every change belongs to a sprint, so even a
one-line bugfix formally wants planner → designer → architect → builder → reviewer →
release. This is the #1 documented failure mode of every spec-driven framework
(ceremony on small tasks). Separately, the spine's integrity rules are enforced only
*while a skill is running* — nothing guards `docs/spec/` between skill invocations.

Two additions fix this: **A. a patch lane** (a certified short road for small fixes)
and **B. a standing verify script** (spine integrity checked on every commit).

**Doctrine (from the research, held throughout):** ceremony scales down by change
class; independent verification and the release gate never do.

---

## Section A — the patch lane

### A1. Entry and authority

New mode: **`/01-planner patch "<description>"`**.

- The **planner certifies** patch-class, records it, and dispatches to the builder.
  One lightweight step (minutes) — classify, write the record, hand off.
- Why the planner and not the builder: a builder declaring its own change "small" is
  the grade-your-own-homework problem the framework refuses everywhere else (ITIL
  segregation of duties: requester ≠ authorizer). Structurally, the planner is the
  seat that would allocate a new REQ-ID — so it is the right seat to certify
  "no new REQ needed."
- Ergonomics: if the user starts at `/04-builder` with a small fix, 04 *proposes*
  patch classification and routes to `/01-planner patch` for certification (one hop —
  BMAD's clarify-and-route pattern with separated authority).

### A2. The classification gate (patch iff ALL five pass; escalate when uncertain)

| # | Check | Mechanical form |
|---|-------|-----------------|
| P1 | Fix maps to **existing, named REQ-IDs** | REQ refs listed on the patch record; no owning REQ → Tier-3 scope signal → `/00 reflect` |
| P2 | **`docs/spec/**` untouched** by the fix — one additive exception, below | spine diff empty, OR additions-only under `docs/spec/evals/**` + exactly one Tier-1 amendment row (also enforced by Section B's script) |
| P3 | **No new dependency** beyond the envelope | lockfile diff; 04's existing HALT rule |
| P4 | **Bounded size** | expected touched-file set + LOC budget written on the record; exceeded mid-build → HALT + escalate |
| P5 | **Fixes existing behavior**, adds none | stays within the named REQs' existing outcome acceptance |

The asymmetry mirrors the amendment protocol: misclassifying *down* (treating real
scope as a patch) silently corrupts intent; misclassifying *up* costs one sprint
plan. **When in doubt, go up.**

**P2 additive-case exception (S1, approved 2026-07-06):** a patch MAY **add** —
never edit or delete — eval cases under `docs/spec/evals/**` (WS3's in-spine
datasets), accompanied by a mechanically-written **Tier-1 amendment row**
(`skill: 01-planner`, additive-regression-case class). Rationale: a fixed bug on a
distributional behavior should leave a regression case behind (the Husain
discipline); without the exception every such fix is forced off the patch lane.
Mechanically checkable: the spine diff contains only additions under `evals/**`
plus exactly one new T1 row. Dataset *edits* remain normal-road amendments.

### A3. The audit record

- **`docs/planning/patches/patch-NNN.md`** (zero-padded, TYPE-NNN convention):
  description · owning REQ-IDs · the five checks with evidence · the size budget ·
  expected touched files · status.
- **A Patches table in `docs/planning/backlog.md`** (patch → REQs → status:
  planned / in-progress / done / escalated). Every patch appears exactly once —
  the ITIL "governed catalog": every use of the short road is visible afterwards.

### A4. The route

```
/01-planner patch "…"          classify (A2) + record (A3) + dispatch
        │
        ▼
/04-builder                    patch funnel = patch record + existing realizations;
                               TDD-for-bugs discipline (existing fix-pass machinery);
                               handoff emitted with review_mode: patch
        │
        ▼
/05-reviewer  (fresh)          same isolation, same honesty gates; seed = handoff
                               + patch record + owning REQ blocks
        │
        ▼
/06-release                    ALL G1–G7 evaluated — nothing waived
```

**Skipped:** 02-designer, 03-architect, sprint files. By construction — if the fix
would touch a governed design element or need an ADR, it fails the gate (P2/P5) and
is not a patch.
**Never skipped:** the fresh-context review and the mechanical release gate.

### A5. Mid-flight escalation

Any check discovered violated during build → 04 **HALTs** (existing machinery), the
patch row is marked `escalated`, and the work re-enters the normal chain
(`/01-planner plan-sprint N` for execution scope, `/00-discovery reflect` for
product scope). Nothing silently widens.

### A6. The overuse guard

- **One patch in flight at a time** (Kanban expedite WIP rule).
- `/status` surfaces patch-lane pressure: **≥3 consecutive patches** without a
  planned sprint, or **any escalated patch**, triggers a P4 advisory —
  "this cadence is a sprint / consider `/08-refactor assess`." Advisory, never a
  block. (Research: unbounded fast lanes quietly become the default road.)

### A7. Seat-contract deltas

- **01-planner:** + `patch` mode (classify → record → dispatch); Patches table
  ownership; patch status lives in the ledger (execution truth, as ever).
- **04-builder:** + patch funnel input; `review_mode: patch` in the handoff
  frontmatter; P3/P4 enforcement folded into existing HALT conditions.
- **05-reviewer:** + patch seed variant (handoff + patch record + owning REQ
  blocks); scope bounded to the patch's behaviors; all honesty gates unchanged.
- **06-release:** unchanged gates; release report may reference patch-NNN instead
  of sprint-NN (report naming: `release-report-patch-NNN.md`).
- **status:** artifact scan includes `docs/planning/patches/`; router understands a
  patch in flight (routes to its next seat); the A6 advisory.
- **shared/artifact-map.md:** + rows for `docs/planning/patches/patch-NNN.md` and
  the Patches ledger section.
- **spec-amendment-protocol:** untouched (patches append no amendment rows;
  escalation reuses existing tiers).

---

## Section B — standing gates (the verify script)

### B1. What it is

A **single-file, stdlib-only Python script — `scripts/verify-spine.py`** — emitted
into each target project by `00-discovery` at WRITE SPINE (template lives in 00's
bundle). It mechanizes the spine's integrity rules so they run on every commit and
in CI, not only when a skill happens to run.

### B2. Checks

- **FAIL (exit 1):** the five load-bearing integrity checks from `status`
  (L1 registry File resolves · L2 leaf contains the delimited REQ block · L3 no
  orphan blocks · L4 no duplicate REQ-IDs · L5 `amendment-log.json` valid) — plus
  amendment-row schema validity.
- **WARN (exit 0, printed):** surviving `[NEEDS CLARIFICATION]` markers (legitimate
  pre-release), ledger↔registry exactly-once drift, ID zero-padding.
- `--json` flag for CI consumption; zero dependencies (Python 3.8+ stdlib).

### B3. Wiring

00 also emits (optional, documented in the project's `docs/README.md`):
- a **pre-commit** snippet invoking the script;
- a **GitHub Actions workflow** template (`.github/workflows/spine-verify.yml`).

The script is the contract; the hooks are wiring samples. Existing projects
backfill via a `status` advisory ("verify script absent — emit it").

### B4. Anti-drift (script ↔ status parity)

The script and `status`'s L1–L5 must never diverge. Two mechanisms:
1. **Parity eval in Layer A:** the script is validated against the same hand-ideal
   and degenerate-spine fixtures the integration graders already use (ideal passes;
   each degenerate fires its check).
2. **`status` runs the script when present** (a read-only execution — consistent
   with its derive-only guarantee) and falls back to inline checks when absent, so
   one implementation serves both paths wherever possible.

### B5. Patch-lane tie-in

P2 ("spine untouched") is enforced *for free* by the same script in pre-commit —
a patch that drifts into `docs/spec/` fails the commit, not just the review.

---

## Eval strategy (Layer A, per framework convention)

1. **01 patch mode (A/B):** a genuinely-small seeded fix → with_skill classifies,
   writes patch-NNN + ledger row, dispatches; a seeded fix that *secretly needs a
   new REQ* → must refuse/escalate to `00 reflect`, never patch it. Graders:
   structural (record file + ledger row + refusal), per the
   framework-lift-is-structural doctrine.
2. **Ceremony-decline eval:** given a patch-class fix, with_skill does NOT produce
   sprint/design/architecture artifacts (the crying-wolf guard applied to process
   weight).
3. **04/05 patch-mode contract:** handoff carries `review_mode: patch`; 05's
   attestation + honesty gates hold on the patch seed.
4. **verify-spine parity:** ideal spine passes; each degenerate fixture fires its
   corresponding check (reuses integration `_ideal` + degenerate fixtures).
5. **status advisory:** 3 consecutive patches in the ledger → the A6 advisory
   appears; a patch in flight → router routes to its next seat.

## Out of scope for WS1

Profile awareness in the router (WS3), EARS/EXPLORE/adopt (WS2), P3 classical-depth
items (WS4). The router change here is deliberately minimal (patch awareness +
advisory) so WS3's profile input lands on a clean seam.

## Resolved decisions (review, 2026-07-06)

1. **P4 size budget default: ≤5 files / ≤150 LOC**, written on each patch record and
   overridable per patch at certification time.
2. **Patch release reports are named `release-report-patch-NNN.md`** (06's report
   naming keys on the patch id, not a sprint token).
3. **The verify script is always emitted; hooks are opt-in.** `scripts/verify-spine.py`
   lands at WRITE SPINE unconditionally; the pre-commit snippet and GitHub Actions
   workflow are emitted as documented templates the user wires up (hook managers vary
   per project).

## Simplification deltas (approved 2026-07-07 — authoritative log: revision-simplification-review.md)

- **A3:** the patch record carries **no `status:` field** — the backlog ledger is
  the sole status origin (at most a certification-time snapshot line).
- **NEW §B6 — terseness invariant:** template budget headers
  (`<!-- budget: ≤N lines -->`, seeded from committed hand-ideals) +
  `W5_spine_density` WARN (lines under docs/spec/** excl. evals/ ÷ REQ count > 40)
  registered in verify-spine.py + one shared `check_budget()` grader helper —
  WARN in the script, hard in Layer-A graders only. Plan Task 1.8.
- **Emission manifest:** the WRITE SPINE checklists (intake AND adopt) enumerate
  every emission the seat makes (five once SECURITY.md lands).
