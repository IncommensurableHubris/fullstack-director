# WS6 Coherence + Simplification Review — the whole framework, before building WS6

> Pre-build check (user-requested, 2026-07-12; next-session agenda §1, run on Fable): do the 10 built seats +
> WS1–WS5 (built, phase-4-exit-verified) + the **WS6 design (not yet built)** + this session's maintenance
> (description trims · grader-robustness batch · doc refreshes) compose into ONE coherent SDLC — and does WS6
> **unify with** the tech-mandate flow (03), the evidence-states (04/05), and the gate model (06) rather than
> duplicate them? Modeled on `revision-coherence-review.md` (8 seams) + `revision-simplification-review.md`.

## Verdict

**Coherent, and WS6's shape is right — an additive doctrine module, not a duplicate.** No cross-skill
contradictions found in the as-built framework. WS6 duplicates **no existing machinery**: nothing today forces
live-source verification of too-new-tech *knowledge* (04's dependency-safety and 07-R4's slopcheck verify the
*artifact* exists; WS6 verifies the *interface knowledge* is live-sourced — a real, distinct gap, straight from the
city-claw failure). But the plan as written would have **added where it must reuse** at five points and left **two
contract gaps** (a degenerate with no owning grader; a parity invariant silently broken). **Nine adjustments
(V1–V9) applied to the plan + design record; one genuine design tradeoff gated to the user (GATE-1).** Also: an
as-built stale-string sweep (I1, seven sites) applied — the hand-synced-count disease the framework exists to kill.

## The composed lifecycle, with WS6 in place

00 declares verify-live techs in `architecture-constraints.md` § Verify-live (Tier-2 to change the set) and **seeds**
`docs/verification/<tech>.md` from live docs/source at WRITE SPINE (intake AND adopt — brownfield is the city-claw
case) → verify-spine **L7** stands guard (declared↔record↔citation integrity, FAIL) → 03's ADRs on a verify-live
tech carry `Verified-against:` (S18; the tech-mandate flow re-verifies on change) → 04 builds only against
record-backed shapes, appends newly-verified claims, and hands off VC rows with a `verified:` ref (an unverified
claim = INFERRED = the existing honesty gate holds SHIP) → 05 flags from its seed unchanged → 06 **G11** runs the
emitted script + a conditional currency clause, fail-closed → status mirrors L7 (parity contract) + a conditional
coverage line. One protocol file (`shared/live-source-verification.md`) is the single doctrine home; every seat
cites it. No new seats, no new ID scheme, no second enforcement implementation.

## Part I — whole-framework findings (as-built)

**I1 — stale hand-synced count-strings (applied now, seven sites).** The gate/check registries grew (WS2–WS5) but
prose counts didn't: `status/SKILL.md` says "L1–L5"/"A1–A5" ×3 while its body defines L6+A6; `06-release/SKILL.md`
says "all seven checks" + "G1–G7 pass conditions" while the table runs G1–G10; `06-release/evals/README.md` "the
same seven checks"; docstrings in `validate_script.py` ("L1–L5 today") + `check_release.py` ("all seven checks").
**Fix applied with drift-proof phrasing** (name the table/registry, not a number) — no grader couples to these
strings (verified by grep before editing).

**I2 — the toggle-table's webapp gate cell contradicted 06 (applied now).** `shared/agentic-profile.md` row 06 read
"webapp: gates G1–G7", but 06 (post-WS3/WS4) states G8 applies to **every** profile (n/a-pass), G9's Operations
clause bites on webapp, and G10 is conditional for all. The single-source table must not misstate its consumers —
cell rewritten to the clause-level truth.

**I3 — 06 SETUP already carries WS6's doctrine in miniature.** "Resolve the platform's **current** deploy interface
from live documentation or its CLI help — never from a memorized or baked-in API shape" *is* verify-before, applied
to the deploy platform. Not a contradiction — an existing instance. WS6's protocol **cites it as precedent** (V8);
no machinery change.

**I4 — this session's maintenance is clean.** The 7-description trim touched frontmatter lines only (1-line diffs;
Use-when + Do-NOT clauses intact). The grader-robustness batch (3 graders + agentic-panel + docs) validates green —
all four deterministic validators pass at review time. No seams introduced.

**I5 — checked, no contradiction found** (the sweep): appender set (00/02/03/08 +01-S1) vs escalators (04/05/07) vs
non-participants (01/06/status) consistent everywhere · sole-allocator rules (01 REQ, 03 ADR) · 04's funnel + 05's
seed boundaries · the bite rule single-homed (agentic-profile) with per-seat citations · the S8 boundary line in
both templates · gates read recorded state only · naming conventions (`sprint-NN`, `TYPE-NNN`) · patch lane P2 vs
`docs/verification/` (records are realizations outside `docs/spec/**` — a patch may update one; spine_hash
correctly excludes them). Agenda §2 note: the tree is **clean** — `35188e8`+`f89d86a` already landed the phase-2
continuation, so §2 reduces to "validators green" (they are).

## Part II — WS6 adjustments (V1–V9, applied to the plan + design record)

**V1 — the orphaned degenerate gets an owner (contract gap).** The design names four degenerates; the plan assigned
graders to three. "Undeclared-but-used" is not deterministically decidable in general ("too new" is a judgment) —
that is *why* the trigger is declaration-based. Resolution: **L7 becomes bidirectional** (a declared tech without a
resolving record fires; an **orphan record** without a declaration row fires — the registry↔leaf family; an uncited
claims-row fires), and used-but-undeclared is graded where it honestly can be: the **live 00 arm** must declare +
seed the obviously-too-new host framework named in the fixture spec (the A/B's point), plus the composed grader's
content-anchored plant. No fake determinism.

**V2 — the status parity invariant (contract gap).** `status` states: "L1–L6 mirror the emitted `verify-spine.py`
FAIL checks **exactly** — the two must never diverge on the integrity verdict." Task 6.5 added only a coverage
line. **Added:** L7 joins status's load-bearing table (`integrity-and-governance.md` + SKILL.md strings + the
parity eval), P1's routed repair for L7 says "re-verify via /00 (seed) or /03 (tech-mandate)", and the coverage
line is **conditional** (no Verify-live block → no line — the on-demand pattern, no webapp noise).

**V3 — say it in the honesty vocabulary (doctrine drift averted).** The plan's locked contract read "carries
`EXECUTED|OBSERVED` (**never** `INFERRED`)". Everywhere else, INFERRED-with-reason is the *honest* state that makes
SHIP unreachable — banning it from being *written* trains the builder to lie under tool absence (the exact failure
the evidence-states exist to prevent). Reworded: **an INFERRED verify-live row is a finding — SHIP unreachable;
G11 stays closed** (the design §④ already said this; the plan drifted). The tool-cascade's "absence is recorded,
never skipped" then terminates in an honest INFERRED + blocked ship, not a fake EXECUTED.

**V4 — the funnel stays a funnel (04's awareness path).** 04 "never re-interprets the raw spine" — but the
verify-live set is declared in `architecture-constraints.md`. The signal must ride the realization layer: **03's
`Verified-against:` ADR lines** (04 already reads `adr/**` as ambient contract) + the records themselves + the
handoff's VC carry-forward gaining a **`verified:`** field. Task 6.4 therefore also touches
`references/build-handoff.md` + `templates/build-handoff.md`, and the record's ownership is fixed as **"00 seeds ·
03/04 append (claims always cited)"** — the `eval datasets: 00 seeds · 05 grows` precedent. 04's Writes gain
`docs/verification/<tech>.md` (append-only claims); 05 stays a flagger (no record writes, seed unwidened —
declared-set completeness belongs to L7/G11, which legitimately read everything).

**V5 — one implementation, two consumers (G11 must not re-implement L7).** 06 already executes the emitted script
(`verify-spine.py --hash` for Provenance). G11's PASS source is **`python scripts/verify-spine.py --json` → L7 ok**
plus the one thing L7 can't know: **currency** — the record's `verified_against` matches the project's version of
the tech **where mechanically determinable** (a declared pin if GATE-1 keeps it, else the dependency manifest);
undeterminable → that clause is **N/A, recorded** (the G10 conditional pattern). No second parser of records in 06;
no drift surface between gate and script.

**V6 — one home for the seed craft.** The seed procedure (fetch cascade, record format, per-claim citation, the
correction rule) lives **once, in `shared/live-source-verification.md`** — not split into
`requirements-authoring.md` (which is REQ craft; the Verify-live block isn't a REQ). 00's SKILL.md gains the
**enumerated WRITE-SPINE emission ⑦** ("under a declared Verify-live block: `docs/verification/<tech>.md` seeded
per tech, fetched live") + its checklist line, and `adopt-evidence.md` mirrors it ("identical to the intake path" —
the S4 precedent; adopt is the city-claw entry). `requirements-authoring.md` gets at most a pointer. Late-step
protection (delta #10) now covers the seed.

**V7 — the eval lands in the standing harness, not beside it.** Task 6.6's composed fixture/grader becomes a case
in `docs/eval-methodology/integration/` wired into **`validate_grader.py --case all`**, and Task 6.2 extends
**`validate_script.py`** with the `l7-*` mutation rows (declared-no-record · uncited-row · orphan-record) — the
session-close validators then guard WS6 forever. The **live A/B is scoped to the 00-seed arm** (fetch+cite vs
confabulate is the genuinely-new behavior; 03/04/06's template/gate mechanics are covered by the composed
`with_skill` run — the delta-#11 A/B policy).

**V8 — convention + boundary lines (protocol/template hygiene).** The ADR `Verified-against:` bullet and the
record's sections carry **core / on-demand(verify-live)** markers (delta #17) so graders never assert them on
non-verify-live fixtures. The protocol states the two boundaries once: (a) 04 dep-safety / 07-R4 slopcheck verify
the **artifact**; WS6 verifies **interface knowledge** — adjacent, never merged; (b) tools named as a capability
cascade ("curated doc cache (e.g. `chub`) → the harness's live web fetch/search → repository source"), absence
recorded — harness-neutral, per the portability rule.

**V9 — plan hygiene.** `deferred-backlog.md` has **no WS6 row** (grep-verified) — exit step reworded to *append*
one (done). The artifact-map row is specified: `docs/verification/<tech>.md | 00 seeds · 03/04 append | R |
per-tech live-source ledger; L7/G11 read it`. Line budgets stated: 00 +2 lines, 06 +1 row, status +2 lines — within
the terseness budgets.

## GATE-1 — the one user decision  ✅ RESOLVED (user, 2026-07-12): **drop the pin** (the recommended option below)

**Should the Verify-live declaration row keep its optional `[· version: <pin>]`?** The approved locked row is
`- **<tech>:** docs: <url> · source: <repo> [· version: <pin>]`.

- **Drop the pin (recommended).** Version-*intent* already has a home (`Stack mandates` / `Integrations` — "fixed
  protocols/versions"); the *evidence* version lives in the record's `verified_against`. Keeping a third home
  invites the smeared-fact failure mode, and makes every bump of a verify-live tech a spine amendment (Tier-2-ish
  ceremony per 0.x release — heavy for exactly the fast-churning tech this targets). Staleness is then G11's
  conditional currency clause (V5) — deterministic on fixtures via the dependency manifest.
- **Keep the pin.** Staleness becomes a pure L7 string-compare (no manifest parsing anywhere), and "upgrades are
  deliberate, amendment-logged events" is arguably the right discipline for too-new tech. Cost: version churn
  through the amendment channel + the duplicate home.

Both outcomes are compatible with everything applied above (L7 core = existence + citation + orphan either way;
currency sits in G11's conditional clause). The plan carries the open gate in its header.

## Checked and kept (do-not-change consensus)

The dedicated per-tech record file (vs embedding in ADRs — four consumers, one home) · G11 as its **own** gate row
(each protection rule owns its routed reason — the G7–G10 pattern) · **L7 as FAIL-class** (verify-*before*: a
corrupted/missing seed should halt routing, not warn) · Tier-2 for changing the verify-live **set** (a
named-technology-class decision) · records **outside** `spine_hash` (realization, correctly excluded from the
release identity) · **no** 01/02/07/08 hooks (01: records are outside P2's spine diff; 02: design-time API facts
bind at 03/04; 07-R4 audits the artifact supply chain, distinct by the V8 boundary; 08's oracle already defends
behavior) — scope discipline, deliberately not hooked · the live A/B itself (fetch-vs-confabulate is behavioral —
structural assertions alone can't prove it; one baseline arm is the memory-doctrine exception, not ceremony) ·
`docs/verification/` as the path (not `docs/spec/verification/` — it must stay amendment-free).

## Applied in this session

1. **I1 + I2** — the stale-string sweep + the toggle-table 06 cell (7 files; drift-proof phrasing; validators
   re-run green).
2. **V1–V9** — `ws6-implementation-plan.md` edited in place (locked contracts + tasks 6.2–6.6 + exit);
   `revision-ws6-live-source-verification-design.md` gains its **Adjustments** delta section (the per-record-delta
   precedent). GATE-1 marked open in both.
3. `next-session-continuation.md` updated: §1 done (this file), §2 reduced to "already landed — validators green",
   §3 builds the plan **as adjusted**, pending GATE-1.
