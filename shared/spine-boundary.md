# Spine Boundary — what lives in the spec spine vs. a skill artifact

> **The keystone.** Stated once, here; every spine-touching skill cites it. It exists to prevent a common
> failure mode — one requirement's facets smeared across four hand-synced files. Two rules and one test.

## Rule 1 — Declaration vs realization

A fact is a **declaration** (it lives in the spine, `docs/spec/`, and changes only through an **amendment**) **if
and only if the user would object to it changing without their say-so.** Declarations are:

- **Requirements** — `capabilities/<domain>.md` (REQ blocks).
- **Design intent** — `design-intent.md` (look/feel, brand, key screens, user-specified tokens).
- **Architecture constraints** — `architecture-constraints.md` (stack, hosting, compliance, scale mandates).
- **The Constitution** — `specification.md` (project non-negotiables).
- **Eval datasets** — `docs/spec/evals/**` (golden datasets for distributional / agent behaviors; a dataset **is**
  the behavioral spec, so it is amendment-gated). Eval **results** are realization. *(WS3 — agent profiles; see
  [`agentic-profile.md`](agentic-profile.md).)*

Everything a skill **derives** is a **realization** (it lives in that skill's own artifacts, references the spine
via `REQ-NNN`, and changes through **drift detection**, not amendment). Realizations include:

- component inventory, design system, screens, DM-ID manifest (skill 02);
- C4 diagrams, domain model, ADRs, feature specs, **detailed Verification Contracts** (skill 03);
- the backlog ledger, epics, sprint slices (skill 01);
- test suites, QA reports (skill 05).

**The test — apply it whenever you're unsure:** *Would the user be upset to discover this changed without anyone
asking them?* **Yes →** declaration (spine, amendment-gated). **No →** realization (skill artifact, drift-gated).

A realization **references** a declaration by ID; it **never copies** the declaration's text. If you find yourself
pasting requirement prose into an ADR or a design doc, stop — link `REQ-NNN` instead.

## Rule 2 — Gherkin altitude

The spine holds **outcome-level** acceptance — a declaration of the user-observable result ("the user can reset
their password"). **Detailed, UI-specific steps** ("click the gear, then 'Security', then…") are **realization**,
and live in skill 03's feature-spec **Verification Contracts**.

Consequence: a sprint's **"Done When"** is the **coarse outcome-acceptance of the slice's REQs** — *traceable to*
them, not a re-paste of every detailed step. The detailed steps verify the same REQ at a finer altitude.

## Maintained artifact vs generated view

A third distinction, orthogonal to the first two:

- **Maintained artifact** — a human, or a skill under control, is the author of record; it carries state that
  *originates* there. The **backlog ledger** is maintained: a REQ's `status` originates in the ledger, nowhere
  else. The spine files are maintained.
- **Generated view** — a pure, regenerable projection of a maintained artifact; **never hand-edited**, because the
  next regeneration overwrites it. `AGENTS.md` (a projection of the Constitution) and any rendered **amendment
  table** are generated views.

If you're tempted to hand-edit a generated view, edit its **source** and regenerate. If a "view" carries state that
exists nowhere else, it isn't a view — it's a maintained artifact, and it needs a real home.
