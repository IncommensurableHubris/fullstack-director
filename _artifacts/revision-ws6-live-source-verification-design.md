# WS6 — Live-Source Verification (design record)

> **Approved 2026-07-12.** An **additive doctrine module** — a `shared/` protocol + a spine declaration + skill hooks
> + a 06 gate + a grader; **no new seats**. Same shape as the amendment + security guardrails. Motivated by the
> city-claw OpenClaw experience (memory `feedback_openclaw_verification`): training data is unreliable for too-new
> external frameworks, and confabulated API/config assumptions propagated spec → design → plan → build before
> doc-research caught them — *including corrections that fabricated their own explanations*.

## Problem

For external frameworks/libraries too new to be reliable in training data (OpenClaw, Hermes Agent, NanoClaw, …), the
model confabulates specifics — inventing APIs/config that do not exist, and even fabricating explanations **when
correcting** ("absence of contradiction is not verification"). These errors corrupt the spine and every downstream
realization. The framework needs a **structural** guardrail (not a predictive one) that forces live-doc +
latest-source verification for *declared* too-new technologies, records it as evidence, and gates the ship on it.

## ① Trigger — spine-declared verify-live technologies

`docs/spec/architecture-constraints.md` gains a **Verify-live** block. Each entry: `tech · canonical doc URL ·
source repo [· pinned version]`. It is a **declaration** (amendment-gated; adding/changing it is **Tier-2** — a
named-technology decision). The guardrail fires **only** for listed techs — stable, well-known libraries are
untouched (no ceremony where the model is reliable). For an `agent-system` project adapting OpenClaw/Hermes/NanoClaw,
`00` seeds the host framework here.

## ② Verification record — `docs/verification/<tech>.md` (one home per fact)

A per-tech **realization ledger** (dedicated file, chosen over embedding-in-ADRs so 03/04/05/06 all reference one
home and `/status` can audit the set):
- **Source anchor** — the exact version/commit verified against (the freshness anchor: a newer in-project version
  makes the record **stale**).
- **Docs fetched** — the doc URL(s) + which sections.
- **Verified-claims table** — each row = a claim (an API/config/behavior fact) **+ its source citation** (a doc
  anchor or `repo@commit:path`). A claim **without a citation is unverified.**
- **Corrections** — what prior assumption each claim overturned (the confabulation guard: a correction re-verifies
  **per claim**, with its own citation).

## ③ The three doctrine moves — `shared/live-source-verification.md`

1. **Verify-before** — never design/architect/build against a verify-live tech from memory; fetch live docs + read
   latest source first, then record it. Tools: **`chub`** (curated, versioned API docs) primary · WebFetch/WebSearch
   for live docs · GitHub for exact shapes. Absence of a tool is **recorded, never skipped**.
2. **Verify-the-correction** — *"absence of contradiction is not verification."* Every claim in a correction is
   **positively cited**, not merely "the old one was wrong." (Per-claim citation, **graded**.)
3. **Audit-before-ship** — `06` gates on the records (G11).

## ④ Skill hooks (all additive)

- **00-discovery** — declares verify-live techs in `architecture-constraints.md`; **seeds** the initial
  `docs/verification/<tech>.md` from live docs/source (the tech's core shape). Especially the `agent-system` host
  framework.
- **03-architect** — an ADR relying on a verify-live tech must **cite the verification record**
  (`verified against <source@version>`); the **tech-mandate flow** gains this. No ADR on unverified tech; an uncited
  reliance is a Reconcile finding.
- **04-builder** — before writing against a verify-live tech's API/config, verify the exact shape from live source;
  an API claim about a verify-live tech left **INFERRED** (not EXECUTED/OBSERVED) is a finding — **extends the
  existing evidence-states**. The build-handoff references the record.
- **05-reviewer** — the isolated review flags verify-live usage not backed by a **current** record (an unverified
  assumption grades like an INFERRED state — SHIP unreachable).
- **06-release — G11 (new gate)** — BLOCK the ship if any declared verify-live tech lacks a **current** (non-stale)
  record. Fail-closed, like G3/G4. Routed reason: *"verify-live tech <X> unverified/stale — re-verify via /00 or /03."*
- **status** — reports verify-live coverage (verified / stale / missing) in the derived state.

## ⑤ The grader (deterministic — no LLM judge)

`check_verification.py` (or folded into the touched seats' graders):
- A declared verify-live tech named in an ADR/spec/build **without a resolving** `docs/verification/<tech>.md` → finding.
- A verified-claims-table row (or a correction) **without a source citation** → finding (the confabulation guard).
- A verify-live API claim in the build left **INFERRED** → finding.
- **Ideal** (a project with a declared tech + a cited, versioned record) passes; **degenerates**
  (undeclared-but-used · uncited-claim · stale-version · inferred-build-claim) each fire their target.

## ⑥ Eval (grader-first A/B, the repo's method)

Fixture: a spine declaring a verify-live tech + a hand-ideal verification record + the four degenerates. Validate the
grader (ideal passes, each degenerate fires) **before** a composed live run: `00` seed (declare + seed record) → `03`
ADR-with-citation → `04` build-verified (no INFERRED verify-live claim) → `06` G11 gate. Live A/B on the genuinely-new
behavior (does a real arm actually fetch + cite, vs. confabulate?).

## Scope / non-goals

- **Not** for stable, well-known libraries — no ceremony where the model is reliable.
- **Not** a general "cite everything" mandate — scoped to the declared too-new set.
- Reuses: the evidence-states (04/05), the tech-mandate flow (03), the fail-closed gate model (06), the amendment
  protocol (declaration changes), and `chub`/live-source tools. Additive; no new seats.

## Provenance

Brainstormed + approved with the user 2026-07-12 (trigger = spine-declared; enforcement = verify+record early +
06 G11 hard-gate; record = dedicated ledger; confabulation guard = per-claim citation, graded). Adapts city-claw's
`feedback_openclaw_verification` (verify-before · verify-the-correction · audit-before-ship) into framework doctrine.

## Adjustments — coherence + simplification review (2026-07-12, pre-build)

Full rationale: `_artifacts/ws6-coherence-simplification-review.md` (V1–V9, applied to the plan). The design-level
deltas:

1. **L7 is bidirectional** (V1): an **orphan record** (a `docs/verification/*.md` with no declaration row) also
   FAILs — the registry↔leaf family. §⑤'s *undeclared-but-used* degenerate is not deterministically decidable in
   general; it is graded on the **live 00 arm** (declare + seed the planted too-new host) + the orphan clause.
2. **status gains L7 parity** (V2), not just the coverage line — the "L-set mirrors verify-spine, never diverge"
   contract; the coverage line is conditional (no Verify-live block ⇒ no line).
3. **Evidence-honesty wording** (V3): an INFERRED verify-live row is *honest but a finding* (SHIP unreachable, G11
   closed) — never "don't write INFERRED"; the tool-cascade's recorded-absence terminates in an honest INFERRED.
4. **The funnel carrier** (V4): 04 learns the verify-live set from 03's `Verified-against:` ADR lines + the records
   + the handoff's `verified:` field — never by reading `architecture-constraints.md`. Record ownership: **00 seeds
   · 03/04 append** (claims always cited).
5. **One implementation** (V5): G11's PASS source is the emitted `verify-spine.py` (L7) + a **conditional currency
   clause** (N/A recorded when the project version is not mechanically determinable — the G10 pattern).
6. **One home for the seed craft** (V6): the seed procedure lives in `shared/live-source-verification.md` § seed;
   00's SKILL.md carries the enumerated WRITE-SPINE **emission ⑦** (+ the adopt mirror — the S4 precedent).
7. **The eval rides the standing harness** (V7): the composed case joins `docs/eval-methodology/integration/`
   (`validate_grader --case all`); `validate_script.py` gains the `l7-*` rows; the live A/B is scoped to the
   00-seed arm.
8. **GATE-1 — RESOLVED (user, 2026-07-12): the pin is dropped.** The declaration row is
   `- **<tech>:** docs: <url> · source: <repo>` (this supersedes §①'s `[· pinned version]` term). Version *intent*
   homes in Stack mandates / Integrations; the record keeps `verified_against` as the *evidence* version;
   staleness = G11's conditional currency clause vs the dependency manifest.
