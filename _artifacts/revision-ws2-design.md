# WS2 Design — 00-Discovery Front-Door Overhaul

> Revision workstream 2 of 4 from the 2026-07-06 framework review (§5.3, §5.10, §8).
> Status: **APPROVED** (user, 2026-07-06) — EARS mandated; EXPLORE no-go confirmed;
> adopt-confirmed source naming confirmed. Research grounding: Topcu et al. (LLM
> requirements-engineering failure modes: premature requirement definition,
> unsubstantiated estimates, overspecification) · Devil's-Advocate sycophancy
> mitigation (63%→41%) · Double Diamond / diverge-before-converge · BMAD Analysis
> phase (the only praised SDD front end — mode-separated, facilitate-don't-generate)
> · Torres opportunity-vs-solution test · Mom Test · EARS (Mavin; Kiro-native,
> VS Code roadmap) · OpenSpec brownfield delta model · LLMREI (AI interviews steer
> stakeholders; tag AI-originated ideas).

---

## Problem

00 is a convergent intake machine — excellent when a doc or a formed idea arrives,
but from a bare itch it faithfully specifies the *first* plausible interpretation
(premature convergence, the worst-documented LLM failure in requirements work).
Separately: every entry path assumes greenfield (no spine-from-existing-code), REQ
statement syntax is free-form (no EARS), negative/abuse requirements have no
template slot, and CHALLENGE lacks the two quantified anti-sycophancy moves.

## Section A — mode structure (four entries, one spine writer)

| Invocation | When | Writes spine? |
|---|---|---|
| `/00-discovery` | a doc or a formed idea (existing flow, unchanged) | yes, after the gate |
| `/00-discovery explore` | **NEW** — a bare itch, pre-commitment | **never** — hard-gated |
| `/00-discovery adopt` | **NEW** — an existing codebase (brownfield / fork) | yes, after the gate |
| `/00-discovery reflect` | amendment backlog (unchanged) | via write-path |

All four stay inside 00 (one front door; modes are the 02/03 precedent — no new
seat). EXPLORE feeds the default flow; ADOPT is an alternative INGEST source; both
converge on the same CHALLENGE → FIDELITY → GATE → WRITE SPINE machinery.

## Section B — EXPLORE mode (divergent, hard-gated)

**Entry:** a bare itch ("I keep losing track of client invoices…"). **Exit:** a
chosen problem framing handed to ITCH — or a recorded decision *not* to proceed.

Steps:
1. **PULL** — facilitate, don't generate: elicit the itch via Mom-Test discipline
   (specific past events, the user's life, ≥80% listening). Named techniques, the
   model asking — not the model answering. Any option the model itself seeds is
   tagged `origin: model` in the artifact (LLMREI steering defense).
2. **DIVERGE** — force **≥3 distinct problem framings** (JTBD/opportunity space),
   each passed through the Torres test ("can multiple solutions address this? if
   not, it is a solution wearing a need's clothes — reframe"). Solutions appear only
   as option *families* per framing, each with a smallest-test.
3. **APPETITE** — Shape-Up style: how much is this itch worth (a size, not an
   estimate)? Recorded; feeds 01's slicing later.
4. **⟫ PICK GATE ⟪** — present the framings + a recommendation + a mandatory
   **Devil's-Advocate turn against the leading framing**. The user picks/ranks —
   or parks/declines. **"Don't build" is a legitimate outcome here** (pre-commitment,
   this is where go/no-go lives; the downstream REVIEW gate keeps its never-KILL
   rule, which applies *after* commitment).
5. **HANDOFF** — the chosen framing becomes ITCH's JTBD input; the decision is
   recorded in the charter decision log.

**Artifact:** `docs/discovery/exploration.md` — framings considered · origins ·
Torres-test results · appetite · decision + rationale. (artifact-map: owner 00,
role K, sibling of assumption-map.)

**The hard gate:** EXPLORE may not write anything under `docs/spec/**` — enforced in
the write-path section, graded in evals, and (post-WS1) caught by the verify script.
This is the structural defense against Topcu failure mode #1 (premature requirement
definition).

## Section C — ADOPT mode (brownfield: spine from an existing codebase)

**Entry:** an existing repo (yours, or a fork like OpenClaw/NanoClaw) with no spine.
**Exit:** a normal spine the whole chain can operate on.

Steps:
1. **EVIDENCE SCAN** — enumerate what the code *proves*: observable capabilities
   (routes, endpoints, CLI commands, screens, tests), constraints (stack, deps,
   hosting config), invariants (auth model, storage, residency hints). Existing
   docs/READMEs ingest as secondary sources.
2. **CANDIDATE DECLARATIONS** — every candidate REQ is authored per the normal
   rubric but with a new source form: `source: code:<path:line>` (or
   `docs:<path>` for found documents). **Registry Status: all `derived` by
   construction** — code evidences *existence*, never *intent*. No schema change to
   the stated/derived enum (avoids rippling through templates, status A4, graders).
3. **CHALLENGE (adopt-flavored)** — the 2×2 runs on intent: "the code does X — do
   you actually *want* X?" Zombie features (code proves it; user doesn't want it)
   surface as explicit out-of-scope notes or removal candidates, not silent keeps.
4. **CONSTITUTION PROPOSAL** — observed invariants ("all data stays local in
   SQLite") are *proposed* Constitution items, adopted only by explicit user
   decision at the gate — never auto-seeded (Constitution changes are Tier-2-class).
5. **⟫ REVIEW GATE ⟪** (existing, batched) — plus the **confirm-derived sweep**:
   each confirmed REQ flips to `stated` with `source: "adopt-confirmed: code:<path>"`;
   unconfirmed ones stay `derived` (flagged, as ever).
6. **WRITE SPINE** — the normal write-path; AGENTS.md emitted; chain unlocked.

**Anti-hallucination property (mechanically gradeable):** every adopt-sourced REQ's
`code:<path>` must resolve — a REQ citing a file that does not exist is an integrity
failure, same discipline as registry↔leaf.

**Boundary with 08-refactor:** 08 reconciles code↔docs *when a spine exists*; ADOPT
*creates* the spine. No overlap. (The framework-fork profile's auditability /
blast-radius assessment is WS3's hook into this mode — seam noted, not built here.)

## Section D — EARS statement syntax + must-not REQs

`references/requirements-authoring.md` gains EARS as the canonical form of the REQ
**statement line** (the one-sentence capability); outcome-Gherkin acceptance is
unchanged (altitude rule untouched).

Mapping table (added to the reference):
- **Ubiquitous** — "The <system> SHALL <response>" → invariants.
- **Event-driven** — "WHEN <trigger>, the <system> SHALL <response>" → the common case.
- **State-driven** — "WHILE <state>, the <system> SHALL <response>".
- **Optional-feature** — "WHERE <feature>, …" → MAY-priority REQs.
- **Unwanted-behavior** — "IF <undesired condition>, THEN the <system> SHALL
  <mitigation/refusal>" → **must-not REQs: the new home for negative/abuse-case
  declarations** (closes the loop with 07's "missing security declaration → route
  to /00" — there is now a template slot to route *into*).

Open question 1 (below): mandate EARS for every REQ statement vs recommend-with-
fallback.

## Section E — CHALLENGE enrichments (both paths, cheap edits to challenge-2x2.md)

1. **Devil's-Advocate turn** — one explicit dissent pass against the leading
   position before the gate (quantified: sycophantic agreement 63%→41%).
2. **Pre-mortem question** — "the spine shipped and the product failed — why?"
   (Klein: ~30% more risks surfaced, qualitatively different ones).
3. **Numbers-need-sources rule** — any quantitative claim entering the spine
   (latency targets, scale, TAM) carries a source quote or an explicit
   assumption/`[NEEDS CLARIFICATION]` tag (Topcu failure mode #2). This is just
   `derived`-status discipline applied to numbers.

## Eval strategy (00's existing suite extends)

1. **explore (A/B):** bare-itch prompt → with_skill produces ≥3 framings with
   origins tagged + appetite + NO `docs/spec/**` writes; baseline typically
   converges on idea #1 and writes spec-shaped files. Structural graders.
2. **explore-refusal:** prompt pressures immediate convergence ("just spec my
   idea") → the divergent round still runs (or an explicit user-override is
   recorded) — the anti-sycophancy assertion.
3. **adopt:** seeded mini-codebase fixture → spine where every REQ is `derived`
   with a **resolving** `code:` source; the planted zombie feature is surfaced at
   the gate, not silently kept; no invented capability (every REQ's source
   resolves); registry↔leaf integrity holds.
4. **EARS/must-not:** statement lines match an EARS pattern; a security-flavored
   fixture yields ≥1 Unwanted-behavior REQ.
5. **CHALLENGE enrichments:** gate presentation contains the dissent + pre-mortem;
   a seeded sourceless number gets flagged, not transcribed.

## Seat-contract deltas

- **00 SKILL.md:** + explore/adopt modes (flow sections + progress checklists +
  Reads/Writes rows); description gains trigger phrases ("brainstorm", "explore an
  idea", "adopt this codebase", "reverse-engineer a spec").
- **New references:** `references/explore-divergence.md` (PULL/DIVERGE/APPETITE/
  PICK craft) · `references/adopt-evidence.md` (scan taxonomy + confirm-sweep).
- **templates/:** exploration.md skeleton.
- **challenge-2x2.md:** Section E items.
- **requirements-authoring.md:** EARS mapping + must-not REQ form + numbers rule.
- **shared/artifact-map.md:** + exploration.md row.
- **status:** no router change needed (a spine-less repo already routes P0 →
  /00-discovery; explore/adopt are user-chosen entries of the same seat).

## Resolved decisions (review, 2026-07-06)

1. **EARS is MANDATED** — every REQ statement line must match one of the five EARS
   patterns. Graders check the SHALL-form; the registry stays machine-parseable.
   (requirements-authoring.md carries the mapping + phrasing guidance so mandated
   EARS stays readable.)
2. **EXPLORE may end in "don't build."** Pre-commitment go/no-go lives in EXPLORE;
   the downstream REVIEW gate keeps its never-KILL rule (post-commitment).
3. **Adopt confirm-flip source label:** `source: "adopt-confirmed: code:<path>"`
   (parallel to the existing `clarification: <topic>` form).

## Simplification deltas (approved 2026-07-07 — authoritative log: revision-simplification-review.md)

- **Packaging:** SKILL.md gains a 4-row mode **dispatch table** (entry ·
  writes-spine? · reference · convergence point); EXPLORE and ADOPT are
  **5–8-line stubs** (hard invariant + gate marker); their flows AND progress
  checklists live in `explore-divergence.md` / `adopt-evidence.md` ("copy that
  checklist as your first act"). SKILL.md target ≈140 lines.
- **One home:** exploration.md holds the full PICK decision + rationale; the
  charter decision log gets a one-line pointer. `templates/exploration.md` folds
  into `explore-divergence.md` (skeleton inline — one less file).
- The adopt path's WRITE SPINE checklist enumerates the emissions (S4).
