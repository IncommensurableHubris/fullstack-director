# Live-Source Verification — the confabulation guardrail for too-new technologies

> **An additive doctrine module.** One protocol, cited by six seats (00 · 03 · 04 · 05 · 06 · status); **no new
> seat.** It exists because training data is unreliable for external frameworks/libraries too new to be well-
> represented (OpenClaw, Hermes Agent, NanoClaw, …): the model **confabulates** specifics — inventing APIs/config
> that do not exist — and, worse, **fabricates its own explanations when "correcting"** (the city-claw failure,
> memory `feedback_openclaw_verification`). Those errors corrupt the spine and every downstream realization. The
> defense is **structural, not predictive** (`agentic-profile.md`): not "ask the model whether it's sure," but a
> declared trigger, a cited record, and a fail-closed gate. Reuses the evidence-states (04/05), the tech-mandate
> flow (03), the fail-closed gate model (06), and the amendment protocol — it adds machinery to none of them.

## The trigger — spine-declared, scoped, never blanket

The guardrail fires **only** for technologies the spine **declares** in `architecture-constraints.md` §
**Verify-live**. Stable, well-known libraries are untouched — **no ceremony where the model is reliable.** This is
deliberate scope discipline, not a general "cite everything" mandate: the cost is paid exactly where memory fails.

- **Declaration (a `03`-governed constraint):** a `- **<tech>:** docs: <url> · source: <repo>` row under §
  Verify-live. **The `<tech>` label IS the record's lowercase basename** (`- **bge-m3:**` →
  `docs/verification/bge-m3.md`); descriptive text belongs after the colon, never inside the label — a qualified
  label breaks the mechanical label↔record linkage (the S18 check). **No version term** — a version *mandate* lives in `Stack mandates` / `Integrations`; the *evidence*
  version lives in the record (below). Adding or changing the verify-live **set** is a **Tier-2 amendment** (a
  named-technology-class decision — `spec-amendment-protocol.md`).
- **Who seeds it:** `00-discovery`, at WRITE SPINE, for every declared tech — including (especially) the
  `agent-system` **host framework** an adopt/fork project builds on.

## The three moves

1. **Verify-before.** Never design, architect, or build against a verify-live tech **from memory.** Fetch live docs
   + read latest source **first**, then record what you verified. A realization that relies on an unverified
   verify-live tech is incomplete by construction.
2. **Verify-the-correction.** *"Absence of contradiction is not verification."* When a claim overturns a prior
   assumption, the **new** claim is **positively cited** — not merely "the old one was wrong." A correction that
   cites nothing is itself a confabulation. (Graded: every claim **and** every correction carries a citation.)
3. **Audit-before-ship.** `06` gates the release on the records (**G11**), fail-closed like G3/G4 — an unverified or
   stale verify-live tech does not ship silently.

## The record — `docs/verification/<tech>.md` (one home per fact)

A per-tech **realization ledger** — a dedicated file (chosen over embedding in ADRs so 03/04/05/06/status all
reference **one** home and `/status` can audit the set). It is a **realization**: it lives **outside**
`docs/spec/**`, is **excluded from `spine_hash`**, and a patch (WS1 lane) may update it without touching the spine.

```markdown
---
verified_against: <tech>@<version>      # the freshness anchor — the exact version/commit verified against
docs_fetched:                           # the doc URL(s) + which sections were read
  - <url>#<section>
---

## Verified claims                       [core]
| claim (an API/config/behavior fact) | citation | corrects |
|--------------------------------------|----------|----------|
| <the fact relied on>                 | <a doc anchor  OR  repo@commit:path> | <prior assumption overturned · or —> |
```

- **A row without a citation is unverified** — it is a finding, never a silent pass.
- **Ownership: `00` seeds · `03`/`04` append** (claims always cited — the *eval datasets: 00 seeds · 05 grows*
  precedent). `05`/`06`/`status` **read only**.
- **Section markers** are **core / on-demand** (`agentic-profile.md`): the claims table is **core**; a `##
  Corrections` narrative section is **on-demand(a correction occurred)** — its absence on a clean record is correct,
  not a gap.

## § Seed — the seed procedure (its single home; 00 cites this, never restates it)

For each declared verify-live tech, at WRITE SPINE:

1. **Fetch** its core shape through the tool cascade (below) — the entry-point API, the config surface, the one or
   two behaviors the project's first slice will rely on. Not the whole surface — the shape the build needs next.
2. **Write** `docs/verification/<tech>.md`: `verified_against` = the version/commit fetched, `docs_fetched` = the
   URLs+sections, one **cited** claims row per fact captured.
3. **Absence is recorded, never skipped:** if no tool can reach a source (offline, private repo, no cache), write
   the record with the claim rows you *can* cite and an explicit `<!-- unreachable: <tool>, <reason> -->` note — the
   downstream evidence-state then stays honestly **INFERRED** and the ship stays blocked, rather than a fabricated
   pass. **Never invent a citation to fill the table.**

## The tool cascade (harness-neutral — name a capability, not a vendor)

1. **A curated, versioned doc cache** (e.g. `chub`) — primary where the tech is supported; deterministic and
   version-pinned.
2. **The harness's live web fetch/search** — the tech's official docs, release notes, current community consensus.
3. **Repository source** — the exact API/config shape at a commit (`repo@commit:path`), the ground truth when docs
   lag the code (the common case for too-new tech).

Portability rule (`AGENTS.md`): a skill names the **capability**; the harness binds the tool. **The absence of any
tier is recorded in the record, never silently skipped.**

## Two boundaries (adjacent controls — never merged)

- **Artifact vs interface-knowledge.** `04`'s dependency safety and `07`-R4's slopsquat/hallucinated-dep check
  verify that the **package artifact exists and is trustworthy**. This protocol verifies that the **interface
  knowledge** (the API/config the code calls) is **live-sourced, not confabulated**. A package can be real while the
  API you "remember" for it is invented — both controls run, neither substitutes for the other.
- **Existing instance (not a new idea).** `06`'s SETUP already **resolves the deploy platform's current interface
  from live documentation or CLI help, never a memorized API shape** — that *is* verify-before, applied to the
  deploy platform. This protocol generalizes the same move to declared build-time dependencies.

## The consuming seats (each adds one repo-root-relative reference line)

| Seat | What it does with a verify-live tech |
|------|--------------------------------------|
| **00-discovery** | declares the set in `architecture-constraints.md`; **seeds** each `docs/verification/<tech>.md` at WRITE SPINE (§ Seed) — intake **and** adopt |
| **03-architect** | an ADR whose *Decision* names a verify-live tech carries `Verified-against: docs/verification/<tech>.md (<tech>@<version>)`; a tech-mandate change **re-verifies** (fresh record). An uncited reliance is a Reconcile finding |
| **04-builder** | verifies the exact shape from the record/live source **before** building; **appends** newly-verified (cited) claims; a verify-live API row left `INFERRED` is honest but a **finding** — the handoff carries a `verified:` ref |
| **05-reviewer** | flags verify-live usage not backed by a **current** record — grades like an INFERRED state (SHIP unreachable). Reads its seed as-is; declared-set completeness is L7/G11's job |
| **06-release** | **G11** — BLOCK if a declared verify-live tech lacks a current, cited record (`verify-spine.py` L7 + the currency clause). Fail-closed; N/A recorded when none declared |
| **status** | reports verify-live coverage (verified / stale / missing); **L7 joins its load-bearing set** (the never-diverge parity contract) |

## Enforcement (deterministic — no LLM judge)

- **`verify-spine.py` L7 (FAIL, bidirectional):** a declared verify-live tech with no resolving
  `docs/verification/<tech>.md`; **or** an orphan record (a `docs/verification/*.md` with no declaration row); **or**
  a claims-table row with an empty citation. Mirrored by `status`'s load-bearing set (the parity contract).
- **`06` G11 (BLOCK):** L7 ok **plus** the **currency clause** — each record's `verified_against` matches the
  project's version of the tech **where mechanically determinable** (the dependency manifest, or a Stack-mandates
  version pin when one exists); undeterminable ⇒ that clause **N/A, recorded** (the G10 conditional pattern).
- **The live behavior** (does a real arm actually *fetch + cite* rather than confabulate?) is proven by the WS6
  A/B eval on the `00`-seed arm — structural graders alone cannot verify it.
