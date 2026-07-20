# WS6 — Live-Source Verification: Implementation Plan

> **For agentic workers:** implement in a **FRESH session**. First read
> `_artifacts/revision-ws6-live-source-verification-design.md` (the full rationale), then
> `_artifacts/ws6-coherence-simplification-review.md` (the 2026-07-12 pre-build review — its V1–V9 adjustments are
> folded in below), then this plan, then the files each task touches. Use `superpowers:executing-plans`. **This
> plan carries the LOCKED CONTRACTS** (paths, field names, gate rows, grader assertions) + the test cycle; the
> design record carries the prose. Steps track with `- [ ]`. **Grader-first, every task; never push.**
>
> ✅ **GATE-1 resolved (user, 2026-07-12): the pin is DROPPED.** The declaration row is
> `- **<tech>:** docs: <url> · source: <repo>` — a version *mandate*'s home stays Stack mandates / Integrations;
> staleness is G11's conditional currency clause (record `verified_against` vs the dependency manifest).

**Goal:** Add a structural guardrail that forces live-doc + latest-source verification for spine-declared too-new
technologies, records it per-tech, and hard-gates the ship on it — killing the confabulation failure mode (city-claw
`feedback_openclaw_verification`: fabricated APIs/config, and corrections that fabricate their own explanations).

**Architecture:** An **additive doctrine module** — one `shared/` protocol + a spine declaration (00) + skill hooks
(03/04/05) + a 06 gate (G11) + a `/status` line + a deterministic grader. **No new seats.** Mirrors the amendment +
security guardrails.

**Tech Stack:** Markdown skill bundles (SKILL.md + references/ + templates/); stdlib-only Python 3.8+ graders; the
repo's eval harness; `chub` + WebFetch/WebSearch + GitHub source as the verification tools.

## Global Constraints (apply to every task)

- **Portability:** no `../` escapes; `shared/*` repo-root-relative; a skill's own files skill-root-relative.
- **Eval discipline (grader-first):** every behavior-bearing change lands with its grader; graders validated
  (hand-ideal passes; each degenerate negative fires its target) BEFORE any live run. Workspaces under
  `_artifacts/skills-eval/**`, never `.claude/**` or `.agents/skills/**` fixtures at run time; a `.gitattributes`
  (`* text=auto eol=lf`) in any worktree a grader diffs.
- **Windows:** `claude.exe`; utf-8; `--num-workers 1`; relax `<SUBAGENT-STOP>` only for spawning seats.
- **Commits:** conventional scope prefixes; small + atomic; **never push** without the user's say-so.
- **LOCKED CONTRACTS (do not drift):**
  - **Declaration:** `docs/spec/architecture-constraints.md` § **Verify-live** — rows
    `- **<tech>:** docs: <url> · source: <repo>`. Adding/changing = **Tier-2** amendment. **No version term**
    (GATE-1 resolved: dropped) — a version *mandate*'s home is Stack mandates / Integrations; the *evidence*
    version lives in the record's `verified_against`.
  - **Record:** `docs/verification/<tech>.md` — frontmatter `verified_against: <tech>@<version>` + `docs_fetched:`;
    a **Verified claims** table `| claim | citation | corrects |` (citation = a doc anchor or `repo@commit:path`;
    an empty citation = unverified). One file per verify-live tech. **Ownership: 00 seeds · 03/04 append**
    (claims always cited — the `eval datasets: 00 seeds · 05 grows` precedent); a **realization** (outside
    `docs/spec/**`, outside `spine_hash`, patch-lane P2 unaffected). Sections carry **core / on-demand** markers.
  - **03 ADR:** a `Verified-against: docs/verification/<tech>.md (<tech>@<version>)` line on any ADR whose *Decision*
    names a verify-live tech — marked **on-demand(verify-live)** in the template. **This line is how the signal
    reaches 04's funnel** (04 reads `adr/**`, never `architecture-constraints.md` — the funnel doctrine holds).
  - **04/05 evidence-state:** a Verification-Contract / handoff carry-forward row for a verify-live tech API carries
    `EXECUTED|OBSERVED` **+ a `verified: docs/verification/<tech>.md` ref**; a row left `INFERRED` (or missing the
    ref) is **honest but a finding — SHIP unreachable via 05's existing honesty gate, and G11 stays closed**. (Never
    instruct "don't write INFERRED" — the tool-cascade's "absence recorded, never skipped" must terminate in an
    honest INFERRED + blocked ship, not a faked EXECUTED.)
  - **06 gate G11:** `| G11 | Live-source verification | run the emitted \`scripts/verify-spine.py --json\` → **L7
    ok**; plus the **currency clause**: each record's \`verified_against\` matches the project's version of the tech
    **where mechanically determinable** (the dependency manifest — or a version mandate in Stack mandates when one
    exists) — undeterminable ⇒ that clause **N/A, recorded** (the G10 pattern) | "verify-live <X> unverified/stale — re-verify
    via /00 or /03" |`. N/A (recorded) when nothing is declared. **06 never re-implements record parsing** — one
    implementation (the script), two consumers (06 + status).
  - **verify-spine L7 (FAIL, bidirectional):** a declared verify-live tech with no resolving
    `docs/verification/<tech>.md`, OR an **orphan record** (a `docs/verification/*.md` with no declaration row —
    the registry↔leaf family), OR a claims-table row with an empty citation.
  - **status parity:** L7 joins status's **load-bearing** set in the same workstream (the "never diverge" contract;
    the L6/Task-3.10 precedent).

## Tasks

### Task 6.1 — the protocol (shared doctrine)
**Files:** Create `shared/live-source-verification.md`.
**Contract:** the 3 moves (verify-before · verify-the-correction · audit-before-ship) · the declaration + record
formats (locked above) · **§ seed — the one home for the seed procedure** (fetch cascade → record write; 00 cites
it, `requirements-authoring.md` does not restate it) · the tool cascade, **harness-neutral** ("curated doc cache
(e.g. `chub`) → the harness's live web fetch/search → repository source"; absence **recorded**, never skipped) ·
the confabulation rule ("absence of contradiction is not verification" — every claim AND every correction
positively cited) · tier interaction (declaration change = Tier-2) · **the two boundary lines** (04 dep-safety /
07-R4 slopcheck verify the *artifact*; this protocol verifies *interface knowledge* — adjacent, never merged) ·
**the existing-instance citation** (06 SETUP's live-interface rule *is* verify-before applied to the deploy
platform) · the consuming seats (00 · 03 · 04 · 05 · 06 · status — each adds the repo-root-relative reference line).
**Grader:** none (doctrine; cross-linked from the seats in later tasks).
**Commit** `docs(shared): live-source-verification protocol`.

### Task 6.2 — declaration + 00 seed + verify-spine L7  *(GATE-1 resolved: no pin term)*
**Files:** Modify `00-discovery/templates/spec/architecture-constraints.md` (+ the Verify-live block);
`00-discovery/SKILL.md` (**WRITE-SPINE emission ⑦, by name** — "under a declared Verify-live block:
`docs/verification/<tech>.md` seeded per tech, fetched live per `shared/live-source-verification.md` § seed" — +
its checklist line; ≤2 lines); `00-discovery/references/adopt-evidence.md` (the mirror line — "identical to the
intake path", the S4 precedent; **adopt is the city-claw entry**); `00-discovery/templates/scripts/verify-spine.py`
(+ L7, one `@register_check`). The **seed craft lives in the shared protocol (6.1), not in
`requirements-authoring.md`** — that reference gains at most a one-line pointer (it is REQ craft; the Verify-live
block is not a REQ).
**Grader-first:** extend **`docs/eval-methodology/integration/validate_script.py`** (the §B4 parity eval) with the
`l7-*` mutation rows — ideal spine (declared + cited record) → L7 ok; degenerates (**declared-no-record ·
uncited-row · orphan-record**) → L7 FAIL — plus `00-discovery/evals/` fixture bits as needed.
**Commit** `feat(00+shared): verify-live declaration + seeded verification ledger + verify-spine L7`.

### Task 6.3 — 03 ADR citation (tech-mandate flow)
**Files:** Modify `03-architect/references/reconcile-architecture.md` + `templates/adr.md` (the `Verified-against:`
bullet, **marked on-demand(verify-live)** — graders never assert it on non-verify-live fixtures) +
`references/system-architecture.md`. The ADR line doubles as **the funnel carrier**: it is what makes the
verify-live set visible to 04 without a spine read. A tech-mandate that *changes* a verify-live tech re-verifies
(fresh record) as part of the amendment+ADR pair. Add assertion **S18** to
`03-architect/evals/check_architecture.py` (an ADR whose Decision names a declared verify-live tech carries a
`Verified-against:` citation to a resolving record; else a Reconcile finding).
**Grader-first:** ideal (ADR cites the record) passes S18; degenerate (verify-live ADR, no citation) fires.
**Commit** `feat(03-architect): verify-live ADR citation in the tech-mandate flow`.

### Task 6.4 — 04 build evidence-state + 05 review
**Files:** Modify `04-builder/references/build-discipline.md` (a tech carrying a `Verified-against:` ADR / a
`docs/verification/` record ⇒ verify the exact API shape from the record/live source **before** building; append
newly-verified claims — cited — to the record; a verify-live row left `INFERRED` is honest but a **finding**, per
the locked contract) + `references/build-handoff.md` + `templates/build-handoff.md` (the **`verified:`** field on
verify-live VC carry-forward rows); 04's **Writes gain `docs/verification/<tech>.md` (append-only claims)**.
`05-reviewer/references/*` (flag verify-live usage not backed by a current record, from the **seed as-is** —
handoff rows + records; declared-set *completeness* stays L7/G11's job, the seat's seed is not widened). Add
assertions to `04-builder/evals/check_build.py` + `05-reviewer/evals/check_review.py` (a verify-live API row left
INFERRED / without a `verified:` ref fires).
**Grader-first:** ideal (row EXECUTED + verified-ref) passes; degenerate (INFERRED verify-live claim) fires.
**Commit** `feat(04+05): verify-live evidence-state enforcement`.

### Task 6.5 — 06 gate G11 + status L7 parity + coverage
**Files:** Modify `06-release/references/release-gate.md` + `SKILL.md` (the G11 row per the locked contract — the
emitted script as the PASS source; `references/deploy-verification.md` gains a one-line cross-cite: SETUP's
live-interface rule is an instance of `shared/live-source-verification.md` § verify-before). `status`:
`references/integrity-and-governance.md` (**L7 joins the load-bearing table** — the parity contract) +
`references/next-command.md` (P1's routed repair for an L7 FAIL: "re-verify via /00 (seed) or /03 (tech-mandate)")
+ `SKILL.md` (the L-set line + a **conditional** coverage line — verified / stale / missing; **no Verify-live block
⇒ no line**, the on-demand pattern). Add G11 to `06-release/evals/check_release.py` (BLOCK if a declared tech lacks
a current record; N/A recorded if none declared) + the status grader (L7 parity + the conditional coverage line).
**Grader-first:** ideal (all declared verified) → G11 pass; degenerates (a declared tech unverified → G11 blocks;
**stale** — record `verified_against` ≠ the fixture's manifest/pin version → the currency clause blocks);
no-declared → N/A recorded, no coverage line asserted.
**Commit** `feat(06+status): G11 verify-live gate + L7 parity + coverage line`.

### Task 6.6 — the composed live run (WS6 exit)
**Files:** a new **integration case** under `docs/eval-methodology/integration/` (`build_fixture.py --case
verify-live` + the grader wired into **`validate_grader.py --case all`** — the standing validators then guard WS6
forever): a spine declaring one verify-live tech + a hand-ideal `docs/verification/<tech>.md` + **4 deterministic
degenerates** (**orphan-record** [L7] · uncited-claim [L7] · stale-version [G11 currency] · inferred-build-claim
[6.4]). *Used-but-undeclared is NOT deterministically decidable* ("too new" is a judgment — that's why the trigger
is declaration-based); it is graded on the **live 00 arm**: the fixture spec names an obviously-too-new host
framework, and the arm must **declare + seed** it (content-anchored on the planted name, per the
integration-grader memory). Validate EVERY touched grader (ideal passes; each degenerate fires) — THEN a composed
`with_skill` live run: `00` (declare + seed the record, fetching live docs/source **for real**) → `03`
(ADR-with-citation) → `04` (build a verify-live API, `EXECUTED`/verified) → `06` (G11 passes). **The live A/B
(baseline vs with_skill) is scoped to the 00-seed arm** — fetch+cite vs confabulate is the genuinely-new behavior
(the delta-#11 policy); 03/04/06's mechanics are covered by the composed run + graders.
**Commit** `test(ws6): verification graders validated + composed live run green`.

## WS6 exit

**✅ DONE (2026-07-12, Opus) — deterministic exit complete + committed.** Tasks 6.1–6.5 built with a grader-first
self-test each; Task 6.6's **deterministic** part built:
- **6.1** `shared/live-source-verification.md` (`docs(shared)`).
- **6.2** declaration template + 00 emission ⑦ (+ adopt mirror) + `verify-spine.py` **L7** (bidirectional) +
  `validate_script.py` `l7-*` rows (`feat(00+shared)`).
- **6.3** 03 ADR `Verified-against:` + `check_architecture.py` **S18** + `--self-test` (`feat(03-architect)`).
- **6.4** 04 build-discipline + handoff `verified:` field + 05 review rule; `check_build`/`check_review`
  `--self-test` (`feat(04+05)`).
- **6.5** 06 **G11** (reads the emitted script) + status **L7 parity** + coverage line; `check_release`/`check_status`
  `--self-test` (`feat(06+status)`).
- **6.6 (deterministic)** the composed `verify-live` integration leg (`grade_verify_live_chain` VL1–VL5 + a
  self-contained ideal fixture + 4 degenerates in `validate_grader --case all`) + exit docs (`test(ws6)`).
- **Guarded forever:** all five WS6 self-tests are wired into `validate_script.py`'s session-close block; the
  composed leg into `validate_grader --case all`. All green.

**Deferred — 6.6b, the live A/B (trigger-gated, the 5.5b precedent).** A `with_skill` 00-seed arm that **fetches
live docs + cites** vs. a baseline that **confabulates** — the one genuinely-new *behavior* a structural grader
cannot verify. Deferred **on principle, not for expedience**: a meaningful fetch-vs-confabulate A/B needs a
**genuinely too-new-but-real** framework with live docs — the fixture's `openclaw` is fictional (nothing to fetch),
and any framework the model already knows won't confabulate. **Trigger:** the first real project declaring a
`## Verify-live` tech (logged in `_artifacts/deferred-backlog.md` §Trigger-gated).

## Self-review (done at write time; V1–V9 folded 2026-07-12)
- **Spec coverage:** design § trigger → 6.2 · record → 6.2 · verify-before → 6.1/6.2 · verify-the-correction
  (per-claim citation) → 6.2 (L7) + 6.3 (S18) · audit-before-ship → 6.5 (G11) · hooks 00→6.2, 03→6.3, 04/05→6.4,
  06/status→6.5 · grader → each task + 6.6. Every degenerate has an owner (V1: orphan-record→L7;
  used-but-undeclared→the live 00 arm). No gap.
- **Contract consistency:** `docs/verification/<tech>.md`, `Verified-against:`, `EXECUTED|OBSERVED` + `verified:`,
  G11 (script-sourced), L7 (bidirectional), status parity — used identically across tasks.
- **Scope:** one guardrail module; one plan; no decomposition needed. Deliberately **no** 01/02/07/08 hooks
  (review § Checked and kept).
- **No placeholders:** every task names its files, its contract, its grader assertion, and its commit.
- **GATE-1 resolved** (user, 2026-07-12): the declaration pin is dropped — no open items.
