# WS4 Design — Classical-Depth Batch

> Revision workstream 4 of 4 from the 2026-07-06 framework review (§5.2, §5.4–§5.9).
> Seven small, independent additions — each a template/reference section on an
> existing seat, none a new skill or mode.
> Status: **APPROVED** (user, 2026-07-06) — all three defaults confirmed.
> Research grounding: ISO 25010:2023 (quality model, + Safety) · evolutionary-
> architecture fitness functions (Ford/Parsons/Kua) · Fowler test-shapes +
> flaky-test quarantine-with-governance (ticket/owner/SLA; >5% flake = trust
> collapse) · Google SRE small-team guidance (one journey, one SLO) · SLSA/SBOM
> norms (EU CRA trajectory) · Threat Modeling Manifesto four questions ·
> `spec_slice_hash` mechanism family (in-house precedent).

---

## D1 — Quality attributes (NFRs) + fitness functions  *(00 · 03 · 05)*

- **00:** the coverage checklist gains a 7th facet — **Quality attributes**: which
  ISO 25010 characteristics are load-bearing for this product, **with numbers**
  ("p95 < 500ms at 1k concurrent", "RPO ≤ 24h"). Quantified NFRs land in
  `architecture-constraints.md` (already the right home — they are declarations).
- **03:** each `system.md` §10 quality scenario must name its **fitness function** —
  the executable check that verifies it (a command, a load-test script, an ArchUnit-
  style rule) — or carry `deferred: <why>`. Prose-only quality claims stop being
  legal.
- **05:** Pass 1 re-runs declared fitness functions where a runtime exists
  (Capability-Probe discipline: attempt, record, never silently skip).

## D2 — Test strategy + flake policy  *(03, one new system.md section)*

`system.md` gains a short **§ Test Strategy**: the declared test shape (pyramid /
trophy / honeycomb — chosen per architecture, recorded with one line of rationale) ·
contract-testing stance (where services integrate) · property-based-testing
candidates (where invariants exist — PBT kills ~50× the mutations of an average
unit test) · **flake policy**: a quarantined test requires ticket + owner +
fix-or-remove SLA (default 2 weeks) + re-qualification criteria. 04 places tests
per the declared shape; 05 checks conformance as advisory.

## D3 — Operations minimum  *(03 feature-spec row · 06 SETUP section)*

- **03:** feature-spec template gains one **Observability row** per feature — what
  it logs/emits, and what "healthy" means (one line each).
- **06:** SETUP extends `deployment-config.md` with an **## Operations** section:
  the ONE SLO on the critical user journey (Google small-team guidance) · where
  logs live · one alert (burn-rate note) · rollback-drill cadence.
  *Leanness deviation from the review (§5.5 suggested a separate `operations.md`):
  folded into deployment-config.md — one runbook, one home. Vetoable.*

## D4 — Data-migration safety  *(03 VC row · 06 conditional gate G10)*

- **03:** when a feature changes the data model, its Verification Contract gains a
  **migration row**: forward-migration command + a rollback-compatibility statement
  (does rollback require a data action? is the migration destructive?).
- **06:** new **G10 — migrations** (conditional, the G6 "if present" pattern):
  evaluates only when the diff/plan contains migrations — the plan must identify
  pending migrations, a destructive migration requires a backup step, and the
  rollback path must state its data implications. Fail-closed when it applies.

## D5 — SBOM + provenance at release  *(06, a plan step + report lines)*

SBOM emission becomes a standard step in the deploy plan (syft/cdxgen where
available — attempted and recorded, WARN when tooling is absent, **not a hard
gate**), and the release report gains a **provenance block**: artifact digest ·
built-from commit · toolchain line. 04's build-time `sbom.json` stays optional;
06 owns the release-time record; 07's R4 consumes it when present.

## D6 — Design-time threat pass  *(03 init section · 07 lens extension)*

- **03 init:** `system.md` gains **§ Threats considered** — the Four Questions
  (what are we building / what can go wrong / what do we do about it / did we do
  enough) walked over the C4 L1/L2 **trust boundaries the diagram already draws**,
  STRIDE as optional structuring. Each threat → a mitigation (constraint line, ADR,
  or an explicit accepted-risk note). A ten-minute pass, not a workshop.
- **07:** the completeness lens gains the cross-reference — audit findings vs
  designed threats: a designed threat with no verifying check is a gap; a finding
  in a zone the design called safe routes back as design feedback (existing
  routing). This converts 07's expensive BLOCK-on-architecture path into a cheap
  design-time catch.

## D7 — Spine release identity  *(06 report frontmatter)*

The release report frontmatter gains **`spine_hash`** — a content hash over
`docs/spec/**` computed by `scripts/verify-spine.py --hash` (WS1's script grows one
flag; same mechanism family as `spec_slice_hash`) — plus the amendment-log row
count at release. "Which spec state shipped in release N" becomes a lookup, and
spec-diff-between-releases becomes possible.

## Eval strategy (thin, structural — each extends an existing suite)

1. D1: a fixture with a seeded quantified NFR → 03 emits the scenario **with** a
   fitness-function line; a prose-only scenario fails the grader.
2. D2: 03 init → § Test Strategy present with a named shape + flake SLA.
3. D3: 06 SETUP → ## Operations with an SLO line; 03 feature spec → observability
   row.
4. D4: a schema-changing fixture → VC migration row; 06 plan carries the backup
   step (degenerate: destructive migration without backup → G10 fires).
5. D5: release report → provenance block present; SBOM step attempted-or-recorded.
6. D6: 03 init → ≥1 boundary-derived threat with a mitigation link; 07 fixture →
   completeness lens cross-references it.
7. D7: `spine_hash` present and recomputes identically over the shipped spine.

## Seat-contract deltas (file-level)

EDIT only — no new files beyond template sections: 00
`references/requirements-authoring.md` (facet 7) · 03 `templates/system.md`
(§ Test Strategy, § Threats considered, §10 fitness-function rule) +
`templates/feature-spec.md` (observability row, migration row) +
`references/system-architecture.md` · 05 `references/verification-evidence.md`
(fitness-function re-run) · 06 `references/release-gate.md` (G10) +
`references/deploy-verification.md` (Operations section, SBOM step, provenance) +
`templates/deployment-config.md` + `templates/release-report.md` (provenance,
spine_hash) · 07 `references/synthesis-and-verdict.md` (lens extension) · WS1's
`verify-spine.py` template (+`--hash`) · `shared/artifact-map.md` (notes).

## Resolved decisions (review, 2026-07-06 — all confirmed by user)

1. **D3:** Operations folds into `deployment-config.md` as an `## Operations`
   section — one runbook, one home (leanness deviation from the review's separate
   `operations.md`, accepted).
2. **D5:** SBOM is attempted-and-recorded with WARN on absent tooling — not a hard
   gate.
3. **D4:** G10 is conditional — evaluates only when migrations are present in the
   diff/plan (the G6 "if present" precedent); fail-closed when it applies.

## Simplification deltas (approved 2026-07-07 — authoritative log: revision-simplification-review.md)

- **D5+D7 merge** into one `## Provenance` release-report block: artifact digest
  · commit · `spine_hash` · `amendments_at_release`. The toolchain line is CUT
  (trigger to restore: an SLSA-attestation consumer); ML-BOM fields become one
  reserved line (deferred).
- **D3:** the G9 drift/sampling line lives here (single home); the IR lines are
  marked `on-demand(first release with real users/data)`.
- **Core/on-demand convention:** template sections are marked `core` or
  `on-demand(<trigger>)`; graders assert core-only on small fixtures (Test
  Strategy core = shape + flake SLA; contract-testing/PBT rows on-demand).
- 03's init checklist names §Test Strategy and §Threats considered explicitly.
