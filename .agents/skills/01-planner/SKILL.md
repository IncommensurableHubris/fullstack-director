---
name: 01-planner
description: "Decompose the project's spec spine into an executable build plan — build-order epics, thin end-to-end sprint slices, and the maintained backlog ledger (REQ→epic→sprint→status). Use after discovery, when the user says 'plan the build', 'decompose the spec', 'plan the backlog', 'plan sprint N', 'what do we build first', or 'break the spec into sprints'. Also the patch lane: when the user says 'patch this', 'small fix', 'hotfix', or 'quick fix', certify it patch-class ('/01-planner patch') — certify, record, dispatch to /04-builder. Reads the spine; writes docs/planning/. It is the sole REQ-ID allocator and the home of execution status. Do NOT declare or change requirements — that is /00-discovery. Do NOT design or architect — that is /02-designer and /03-architect. Never writes execution status into the spine."
---

# 01 · Planner — decompose

Turn the **spec spine** (`docs/spec/`) that discovery produced into an **executable build plan**: build-order epics,
thin end-to-end sprint slices, and the maintained **backlog ledger** (REQ → epic → sprint → status). You are the
bridge from *"what are we building?"* (the spine's declarations) to *"what do we build, in what order?"*.

## Operating principle — consume and decompose, never amend

The spine is **truth you read, not text you change.** Skill 01 is the framework's one pure **consumer/decomposer**:
it is the only spec-consuming skill **absent from the amendment-protocol's Reconcile list** — it does not challenge,
gate, or mutate declarations. Two consequences:

- **Decompose invents no scope.** Every REQ you plan already exists in the spine (00 bootstrapped them). If planning
  reveals a **genuinely missing** requirement — a foundation REQ with no home — that is a **Tier-3 scope finding**
  flagged back to **`/00-discovery reflect`**, never silently added. (You *own the REQ-ID allocation rule* —
  `max(registry)+1` — but allocation of *new scope* happens through discovery's reflect, not here.)
- **Execution status is yours alone, and it lives in the ledger.** A REQ's `planned`/`in-progress`/`done` originates
  in `docs/planning/backlog.md`. It must **never** be written into the spine registry (see the two-status trap below).

## The flow

Run these phases in order. The slicing *craft* lives in `references/slicing.md` — load it as phase 3 begins.

### 1 · READ SPINE — load the declarations
Read `docs/spec/specification.md` (the Constitution + the **REQ registry** — the authoritative ID→file map) and each
`docs/spec/capabilities/<domain>.md`. Note each REQ's **priority** (`MUST`/`SHOULD`/`MAY`). Read
`docs/discovery/assumption-map.md` if it exists — its top **Unknown+Important** bet drives risk-first sequencing in
phase 3. This phase is **read-only**; never edit a spine file.

### 2 · EPICS — regroup domain → build order
The spine is organized **by domain** (the user's declaration). Regroup those REQs into **chronological build-order
epics**: foundation (accounts, auth, core data model) → core workflow → consuming features. Each epic depends on the
ones before it. Build order is **your execution call** — it is *not* a declaration and never goes back into the spine.

### 3 · SPRINT SLICES — cut thin vertical threads
Per `references/slicing.md`: token-bounded (~200k build budget), **vertical end-to-end** (never horizontal). **Sprint
1 is the walking skeleton** — the thinnest end-to-end thread that delivers the core job, biased to **de-risk the top
assumption-map bet**. Split anything too big with **SPIDR**; never widen horizontally to fit.

### 4 · ⟫ LIGHT GATE ⟪ — confirm the shape once
Present the **build-order epics + the sprint-1 slice** in one message and ask for **PROCEED / ADJUST** before writing
any files. This is a light confirmation of *build shape*, not a discovery-style review — the declarations were
already gated in 00. On ADJUST, fold the change in and re-present only what moved.

>>> GATE: present build order + sprint-1 scope; wait for PROCEED / ADJUST before writing the backlog + sprint files. <<<

### 5 · BACKLOG LEDGER — write the maintained ledger
Only after the gate. Write `docs/planning/backlog.md` from `templates/backlog.md`: the build-order epics + the
**ledger table** where **every spine REQ appears exactly once**, each mapped to its epic, sprint, and execution
`status` (all `planned` at decomposition). **Status originates here** — later skills update it in place.

### 6 · SPRINT FILES — write the frozen slices
Write each `docs/planning/sprints/sprint-NN.md` (zero-padded) from `templates/sprint-NN.md`: the slice's REQ-ID
references **plus a sprint-freeze snapshot** of each REQ's outcome Gherkin at slice time, and the coarse **"Done
When"** (the slice's outcome-acceptance, traceable to its REQ-IDs). Write at least **sprint-01** now; later sprints
are filled on demand (see `plan-sprint N`).

## Read & write paths (the spine is read-only here — do not corrupt it)

- **Read** the spine; **write** only under `docs/planning/`. You never edit `docs/spec/**`.
- **REQ-ID allocation rule (yours).** The next REQ-ID is always `max(registry)+1`. Other skills that need a new ID
  request it by this rule; *new scope* is allocated through `/00-discovery reflect`, not minted here.
- **Exactly-once.** Every REQ in the registry appears in the ledger **exactly once** — no REQ dropped, none invented.
  Cross-check the ledger against the registry before finishing.
- **⚠ The two-status trap.** Two different "status" fields exist; keep them in their own homes:
  - spine registry `Status` = `stated` | `derived` (**fidelity** — 00's, in `docs/spec/specification.md`);
  - ledger `status` = `planned` | `in-progress` | `done` (**execution** — yours, in `docs/planning/backlog.md`).
  Writing execution status into the spine registry corrupts the declaration/realization boundary. **Never do it.**

## `plan-sprint N` mode — `/01-planner plan-sprint N`

Plan a subsequent sprint after the initial decomposition. Read `docs/planning/backlog.md` (full ledger + statuses)
and `docs/planning/sprints/sprint-<N-1>.md` (and its `docs/quality/qa-report-sprint-<N-1>.md` if it exists). Select
the next slice — pull `SHOULD` then `MAY`, plus anything deferred from N-1 — **respecting epic order** (don't pull
from a later epic while an earlier one is unfinished). Write `docs/planning/sprints/sprint-NN.md` (frozen snapshot +
Done When) and update the ledger's `Sprint`/`Status` columns in place. Re-freeze any REQ the spine has amended since.

## `patch` mode — `/01-planner patch "<description>"`

The **expedite lane** for small fixes: **certify** patch-class, **record** it, **dispatch** to the builder — one
lightweight step, no sprint machinery. *You* certify because a builder declaring its own change "small" is
grade-your-own-homework (requester ≠ authorizer); structurally you are the seat that would allocate a new REQ-ID,
so you are the seat that certifies "no new REQ needed." (04 handed a small fix directly *proposes* patch
classification and routes here — one hop.)

**Doctrine: ceremony scales down by change class; independent verification and the release gate never do.**
Skipped: 02-designer, 03-architect, sprint files — by construction (a fix that would touch a governed design
element or need an ADR fails the gate). Never skipped: the fresh-context review (05) and the release gate (06).

### The classification gate (patch iff ALL five pass)

| # | Check | Mechanical form |
|---|-------|-----------------|
| P1 | Fix maps to **existing, named REQ-IDs** | REQ refs listed on the patch record; no owning REQ → Tier-3 scope signal → `/00-discovery reflect` |
| P2 | **`docs/spec/**` untouched** by the fix — one additive exception, below | spine diff empty, OR additions-only under `docs/spec/evals/**` + exactly one Tier-1 amendment row (also enforced by the standing verify script) |
| P3 | **No new dependency** beyond the envelope | lockfile diff; 04's existing HALT rule |
| P4 | **Bounded size** | expected touched-file set + LOC budget written on the record (default ≤5 files / ≤150 LOC, overridable at certification); exceeded mid-build → HALT + escalate |
| P5 | **Fixes existing behavior**, adds none | stays within the named REQs' existing outcome acceptance |

**Escalate when uncertain.** Misclassifying *down* (treating real scope as a patch) silently corrupts intent;
misclassifying *up* costs one sprint plan. When in doubt, go up: execution scope → `plan-sprint N`; product scope
→ `/00-discovery reflect`. No partial patches.

**P2 additive exception (S1):** a patch MAY **add** — never edit or delete — eval cases under
`docs/spec/evals/**`, accompanied by exactly one mechanically-written Tier-1 amendment row (the S1 row form in
`shared/spec-amendment-protocol.md`). Dataset *edits* remain normal-road amendments.

### The route

1. **CLASSIFY** — run P1–P5 against the spine + the fix description; write the evidence as you go.
2. **RECORD** — `docs/planning/patches/patch-NNN.md` from `templates/patch-NN.md`; numbering `max(existing
   patches)+1`, zero-padded (none yet → `patch-001`). The record carries **no status field** — status lives in
   the ledger alone.
3. **LEDGER** — add the row to `## Patches` in `docs/planning/backlog.md` (create the section from
   `templates/backlog.md` if the project predates it): `| patch-NNN | REQ-… | planned |`. Every patch exactly
   once; **one patch in flight at a time** — an open `planned`/`in-progress` row means finish or escalate it first.
4. **DISPATCH** — name the next command: `/04-builder` on this patch (the builder's funnel takes the patch record
   + existing realizations; its handoff carries `review_mode: patch`), then `/05-reviewer` (fresh) →
   `/06-release`. All gates evaluated — nothing waived on the expedite lane.

### Patch progress checklist (copy this and track as you go)

- [ ] CLASSIFY — P1–P5 each evidenced; any fail or uncertainty → escalate, write no patch file
- [ ] RECORD — `patches/patch-NNN.md` written (max+1, zero-padded; **no status field**)
- [ ] LEDGER — `## Patches` row added exactly once, status `planned`; one patch in flight
- [ ] DISPATCH — `/04-builder` named as the next command (then 05 → 06; nothing waived)

## Progress checklist (copy this and track as you go)

- [ ] 1 · READ SPINE — registry + capabilities + assumption-map loaded; priorities noted (read-only)
- [ ] 2 · EPICS — domain REQs regrouped into build-order epics (foundation → core → consuming)
- [ ] 3 · SPRINT SLICES — thin vertical slices; sprint 1 = walking skeleton biased to the top bet
- [ ] **>>> GATE 4: present build order + sprint-1 scope; wait for PROCEED / ADJUST before writing <<<**
- [ ] 5 · BACKLOG LEDGER — `docs/planning/backlog.md`; every REQ exactly once; status = execution-only
- [ ] 6 · SPRINT FILES — `sprint-01.md` written; frozen Gherkin snapshots + Done When; REQ-IDs referenced
- [ ] Integrity: ledger ↔ registry exactly-once cross-check passes; spine files untouched

## Reads / Writes

**Reads:** `docs/spec/specification.md` · `docs/spec/capabilities/<domain>.md` · `docs/discovery/assumption-map.md`
(if present). On `plan-sprint N`: `docs/planning/backlog.md` · `docs/planning/sprints/sprint-<N-1>.md` ·
`docs/quality/qa-report-sprint-<N-1>.md` (if present). On `patch`: `docs/planning/backlog.md` ·
`docs/planning/patches/` (existing records, for `max+1` numbering).
**Writes:** `docs/planning/backlog.md` · `docs/planning/sprints/sprint-NN.md`. On `patch`:
`docs/planning/patches/patch-NNN.md` + the backlog's `## Patches` row. **Never** writes `docs/spec/**`.

## References (load when the phase needs them)

- `references/slicing.md` — the slice-selection craft: vertical/walking-skeleton, risk-first sequencing, SPIDR,
  "Done When" altitude, token-bounding (phase 3).
- `shared/spine-boundary.md` — declaration vs realization; maintained vs generated (the keystone); repo-root-relative.
- `shared/artifact-map.md` — canonical paths for the backlog ledger + sprint files; repo-root-relative.
