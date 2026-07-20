# Fullstack Director Revisions (WS1–WS5) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Session pattern (repo convention, overrides defaults):** one FRESH implementation
> session per phase. Each session's first act: read this plan's phase section + that
> phase's design record (`_artifacts/revision-wsN-design.md`) + the files the phase
> touches. The design record carries the full prose rationale; THIS plan carries the
> locked contracts (paths, field names, tokens, gate rows) and the test cycle.

**Goal:** Implement the five approved revision workstreams — patch lane + standing
gates (WS1), 00-discovery front-door overhaul (WS2), agentic Project Profile (WS3),
classical-depth batch (WS4), security hardening (WS5) — every commit eval-green.

**Architecture:** All changes are additive modules on the existing ten seats + two
new shared protocols; no new seats; one new emitted script (`verify-spine.py`,
check-registry architecture that phases 3–4 extend); the eval suites extend each
seat's existing `evals/` following the skill-creator A/B + deterministic-grader
method already proven in this repo.

**Tech Stack:** Markdown skill bundles (SKILL.md + references/ + templates/),
stdlib-only Python 3.8+ (script + graders), the repo's existing eval harness.

## Global Constraints (apply to every task)

- **Portability rules:** no `../` escapes; `shared/*` referenced repo-root-relative;
  a skill's own files skill-root-relative; no `${CLAUDE_PLUGIN_ROOT}`.
- **Eval discipline:** every behavior-bearing change lands with its grader; graders
  are validated (hand-ideal passes; each degenerate negative fires its target) BEFORE
  live A/B runs. Eval workspaces live under `_artifacts/skills-eval/<skill>/` — never
  under `.claude/**` or inside `.agents/skills/**` fixtures dirs at run time.
- **Windows harness notes (from repo memory):** `claude.exe` (not `.cmd`), UTF-8
  encoding, `--num-workers 1`, threading for pipes; relax `<SUBAGENT-STOP>` only for
  the spawning seats (03/05/07).
- **Commits:** conventional scope prefixes (`feat(01-planner): …`,
  `docs(shared): …`, `test(00-discovery): …`); small and atomic; **never push**
  without the user's say-so; CRLF warnings from git are benign on this machine.
- **ID/naming:** `TYPE-NNN` zero-padded everywhere; `patch-NNN` follows it.
- **Doctrine lines (verbatim, reused in prose):** "ceremony scales down by change
  class; independent verification and the release gate never do" · "structural
  defenses, not predictive ones" · "escalate when uncertain."
- **Amendment-log schema is FROZEN** (id, req, skill, tier, disposition,
  source_quote, supersedes, resolved_by — no new fields, no date). S1's
  additive-regression-case rows encode the class in `source_quote`
  (`"patch-NNN: added regression case(s) <dataset path>"`), `skill: "01-planner"`,
  `tier: 1`, `disposition: "auto-applied"`.
- **Cross-phase contract tokens (do not drift):**
  `review_mode: full|patch` (04 handoff frontmatter) ·
  `eval_floors_met: true|false|n/a` + `evals_run: <int>` (05 qa-report frontmatter;
  06 G8 reads these exact names) ·
  `- **Profile:** webapp|agent-system|mcp-server|skill-pack` (specification.md
  header line; absent ⇒ webapp) ·
  verify-script check IDs `L1…L6` (FAIL) / `W1…W5` (WARN) as defined in Tasks 1.1 /
  3.3 / 1.8 · `python scripts/verify-spine.py [--json] [--hash]`, exit 0 = pass/warn,
  1 = any FAIL.

## Simplification amendments (approved 2026-07-07 — READ FIRST; these override task bodies)

Authoritative log: `_artifacts/revision-simplification-review.md`. The design
records carry matching delta sections. **Four sessions, not five** (Phases 4+5
merged). Task count after merges/splits ≈ 31.

**A/B policy (replaces every task's live-A/B step):** per-task deterministic
graders stay, validated (hand-ideal + degenerates) BEFORE commit. Task-level live
A/B only for the genuinely-new behaviors: **1.3, 2.1, 2.2, 2.3, 2.4, 3.2, 3.4,
3.5a, 3.6, 3.9, 5.2, 5.3.** Every other task is covered by ONE composed with_skill
live run per phase (baseline arms dropped for template-presence assertions):
Phase 1 = one patch-lane chain `01→04→05→06→status` (covers 1.4–1.7); Phase 3 =
one agent-mini run (covers 3.7/3.8/3.10); Phase 4 = one 03-init + one 06-release +
one 07-audit run (covers all WS4/WS5 mechanical tasks). Shared helpers, written
once: EARS regex constants (2.1) · eval-block parser (3.3; reused 3.7/5.3) ·
`check_budget()` (1.8).

**Per-task amendments:**
- **1.2 / 2.4:** the WRITE SPINE checklist **enumerates every emission** the seat
  makes (spec · docs/README.md · AGENTS.md · verify-spine.py; + SECURITY.md once
  5.4a lands) — intake AND adopt paths.
- **1.3:** patch template has **no `status:` field** (ledger = sole origin);
  P-table footer "escalate when uncertain"; dispatch (`/04-builder`) gets its own
  checklist line.
- **2.1:** add a step — grep downstream graders (01/02/03) for statement-line-shape
  assertions before scoping the EARS check.
- **2.3 / 2.4:** SKILL.md carries the 4-row mode **dispatch table** + 5–8-line
  stubs only; flows AND progress checklists live in `explore-divergence.md` /
  `adopt-evidence.md` ("copy the checklist as your first act");
  `templates/exploration.md` folds into the reference (do not create the file).
- **3.1:** `shared/agentic-profile.md` additionally carries: the **bite rule**
  (single definition; 04/05/07/08 cite it) · **reserved rows** for `mcp-server` +
  `skill-pack` ("build on first project declaring this profile") · the
  **core/on-demand template-section convention** (sections marked `core` /
  `on-demand(<trigger>)`; graders assert core-only on small fixtures).
- **3.2:** the cost envelope **references** latency/throughput targets in
  architecture-constraints (single home, per D1); S8 boundary sentence extended.
- **3.4:** skill-pack skip case deferred with the reserved profile.
- **3.5 → 3.5a only** (agent-system: ADR categories + eval-suite oracle +
  profile-aware STOP + topology-justification named in the gate checklist).
  **3.5b (mcp-server content: transport/auth ADR + four named MCP VC checks +
  fixture) is RESERVED** — build on first mcp-server project.
- **3.7:** 05's remit **excludes `docs/spec/evals/security/**`** (07 executes
  those); implement floors + fitness functions as ONE "re-execute declared
  verifications" reference section (subsumes Task 4.1's 05 leg); named checklist
  line for the final_commit re-run + hack-resistance check.
- **3.8:** G9 = **span-smoke evidence only** in this phase; the
  Operations-completeness clause is added in Phase 4 alongside Task 4.3; add the
  span-smoke to 06's VERIFY checklist line.
- **3.9:** leave an explicit `## Dynamic arm — WS5, reserved` stub in
  `agentic-panel.md`; do NOT touch the verdict table here (5.3 owns it).
- **3.10:** replace the skill-pack fixture with the **agent-system vs webapp**
  router discriminator (design phase = interaction-manifest presence).
- **4.1:** the 05 leg folds into 3.7's re-execution section (03/00 legs unchanged);
  03's init checklist must NAME §Test Strategy + §Threats considered (with 4.2/4.6).
- **4.3:** + G9's Operations-completeness clause (from 3.8) · the drift/sampling
  line lives HERE (single home) · IR lines marked `on-demand(first release with
  real users/data)`.
- **4.5 + 4.7 MERGE** into one task: the `## Provenance` block — artifact digest ·
  commit · `spine_hash` · `amendments_at_release` (toolchain line CUT; ML-BOM =
  one reserved line); `--hash` registration via Task 1.1's registry; one grader,
  covered by the Phase-4 composed 06 run.
- **5.1:** grader = chapter-coverage table scoped to the declared level; NO
  machine frontmatter counts; NO date field (`audited_commit` + git).
- **5.2:** named re-audit checklist line (`proof_of_fix` column).
- **5.3:** ASR expressed via the WS3 eval-block `metric:` (no second grammar;
  reuse 3.3's parser); waiver presentation reuses 02's Gate pattern (one line);
  the arm + the PASS precondition land here with their grader.
- **5.4 SPLITS:** **5.4a** (00↔06: SECURITY.md template + emission + G7 wording +
  IR-on-demand marking) · **5.4b** (04↔07: slopcheck + cooldown lines + `mcp-scan`
  [agent-system scope] + optional ZAP). Graders only for load-bearing items
  (SECURITY.md emission + G7 row + the two build-discipline lines); **no graders
  for optional-scanner doc mentions**.
- **5.5 SPLITS:** **5.5a** (grader + hand-ideal + 3 degenerates) builds now;
  **5.5b** (the live six-seat chain) is DEFERRED — trigger: first real
  agent-system project or first composed-invariant bug; record in artifact-map
  §Deferred.

---

## Phase 1 — WS1: Delta Path + Standing Gates
*(fresh session; read `revision-ws1-design.md`; seats: 01, 04, 05, 06, status, 00-emission, shared)*

### Task 1.1: `verify-spine.py` template with a check registry

**Files:**
- Create: `.agents/skills/00-discovery/templates/scripts/verify-spine.py`
- Test: `docs/eval-methodology/integration/validate_script.py` (new, mirrors
  `validate_grader.py` style)

**Interfaces:**
- Produces: `CHECKS: list[tuple[str, str, callable]]` populated via
  `@register_check(check_id, severity)` decorator, severity ∈ {"FAIL","WARN"};
  `main(argv) -> int` honoring `--json`; check IDs:
  `L1_registry_file_resolves`, `L2_leaf_contains_block`, `L3_no_orphan_blocks`,
  `L4_no_duplicate_req_ids`, `L5_amendment_log_valid` (FAIL) ·
  `W1_surviving_markers`, `W2_ledger_registry_sync`, `W3_id_zero_padding` (WARN).
  Phases 3–4 register `L6` and `--hash` — build nothing bespoke for them, the
  registry must make registration a 3-line change.
- Consumes: fixture spines at
  `docs/eval-methodology/integration/fixtures/_ideal/spec-first/docs/spec/` (pass
  case) and the degenerate seeds from `validate_grader.py` (fire cases).

- [x] **Step 1: Write the failing validation harness** — `validate_script.py`
  runs the script against the `_ideal` spine expecting exit 0, then against each
  degenerate (`broken-registry`→L1, `dropped-req`→L2/L3 variants, duplicate-id
  seed→L4, malformed-json seed→L5, marker seed→W1-in-json-not-exit-1) asserting the
  named check id appears in `--json` output with the right severity.
- [x] **Step 2: Run it** — Expected: FAIL (`scripts/verify-spine.py` template absent).
- [x] **Step 3: Implement the script** — stdlib only (`re`, `json`, `pathlib`,
  `argparse`, `hashlib` reserved); parse the registry table (`| REQ-NNN |` rows →
  File column), assert file resolves (L1), contains `### REQ-NNN:` …
  `<!-- /REQ-NNN -->` (L2), sweep `capabilities/*.md` for blocks without registry
  rows (L3), duplicate IDs (L4), `json.load` + `"amendments"` array + frozen-schema
  key check per row (L5); markers regex `\[NEEDS CLARIFICATION` (W1);
  `docs/planning/backlog.md` ledger REQ set == registry set when ledger exists (W2);
  zero-padding regex (W3). `--json` emits
  `{"result":"PASS|FAIL","checks":[{"id","severity","ok","detail"}]}`.
- [x] **Step 4: Run validation** — Expected: all pass/fire as asserted.
- [x] **Step 5: Commit** — `feat(00-discovery): verify-spine.py template — check-registry integrity script (L1-L5/W1-W3)`

### Task 1.2: 00 emits the standing gates

**Files:**
- Modify: `.agents/skills/00-discovery/SKILL.md` (WRITE SPINE step 6 + Writes list)
- Create: `.agents/skills/00-discovery/templates/hooks/pre-commit.sample`,
  `templates/hooks/spine-verify.yml` (GH Actions, runs the script on push/PR)
- Modify: `shared/artifact-map.md` (+ rows: `scripts/verify-spine.py` owner 00
  role gen; hooks noted opt-in)
- Test: extend `.agents/skills/00-discovery/evals/check_spine.py` — assert
  `scripts/verify-spine.py` exists in outputs and `python scripts/verify-spine.py`
  exits 0 on the freshly written spine.

**Interfaces:** Produces the emitted path `scripts/verify-spine.py` (project root
`scripts/`); WRITE SPINE contract line: "emit the verify script (always) + hook
templates (opt-in, documented in docs/README.md)".

- [x] **Step 1:** Add the grader assertion; run existing suite → new assertion FAILS on prior fixtures' outputs.
- [x] **Step 2:** Edit SKILL.md step 6 (one sentence + Writes row), add templates, artifact-map rows.
- [x] **Step 3:** Re-run grader on a regenerated `rich-spec` A/B output (or hand-apply to the iteration-1 ideal) → PASS.
- [x] **Step 4: Commit** — `feat(00-discovery): emit verify-spine.py + opt-in hooks at WRITE SPINE`

### Task 1.3: 01-planner `patch` mode

**Files:**
- Modify: `.agents/skills/01-planner/SKILL.md` (+ `patch` mode section + checklist
  + Reads/Writes) ; `.agents/skills/01-planner/templates/backlog.md` (+ `## Patches`
  table: `| Patch | REQs | Status |`) ; `shared/spec-amendment-protocol.md` (one
  sentence naming the S1 additive-regression-case T1 row form, encoded per Global
  Constraints)
- Create: `.agents/skills/01-planner/templates/patch-NN.md` — frontmatter
  `patch:`, `reqs: []`, `size_budget: {files: 5, loc: 150}`, `status: planned`;
  body: description · the five gate checks P1–P5 each with evidence line · expected
  touched files.
- Test: `.agents/skills/01-planner/evals/check_patch.py` (new) + `evals.json`
  cases: (a) genuinely-small fix → patch-001.md + ledger row + all five checks
  evidenced + dispatch line names `/04-builder`; (b) hidden-scope fix (fixture
  seeds a fix that needs a new REQ) → NO patch file; a Tier-3-routed escalation to
  `/00-discovery reflect` in the transcript/summary; (c) ceremony-decline — no
  sprint/design/architecture artifacts created.

**Interfaces:**
- Produces: `docs/planning/patches/patch-NNN.md` (schema above) + the Patches
  ledger table; classification gate P1–P5 verbatim from
  `revision-ws1-design.md §A2` (copy the table into SKILL.md).
- Consumes: WS1 gate table; `max(patches)+1` numbering.

- [x] **Step 1:** Write `check_patch.py` (validate: frontmatter keys, REQs resolve
  against the fixture registry, ledger row exactly-once, forbidden-artifact absence
  for case c) + degenerate validation (a patch file with a dangling REQ fails).
- [x] **Step 2:** Run grader validation → fires correctly, ideal passes.
- [x] **Step 3:** Write the SKILL.md mode + templates + protocol sentence.
- [x] **Step 4:** Live A/B per skill-creator method on cases a–c → with_skill green.
- [x] **Step 5: Commit** — `feat(01-planner): patch mode — certify, record, dispatch (5-check gate, ledger-recorded)`

### Task 1.4: 04-builder patch funnel

**Files:**
- Modify: `.agents/skills/04-builder/SKILL.md` (step 0 extension: patch input;
  HALT list + P3/P4 wording) ; `templates/build-handoff.md` (+ frontmatter
  `review_mode: full|patch`, `patch: patch-NNN` when patch) ;
  `references/build-discipline.md` (fix-pass note: patch budget exceeded → HALT +
  mark patch `escalated`)
- Test: extend `.agents/skills/04-builder/evals/` — handoff frontmatter carries
  `review_mode: patch` + the patch id on a patch fixture; budget-exceeded fixture
  → HALT recorded, patch row `escalated`, no silent widening.

- [x] **Step 1:** Grader assertions first (fail on current). **Step 2:** implement SKILL/template edits. **Step 3:** A/B green. **Step 4: Commit** — `feat(04-builder): patch funnel — review_mode:patch handoff + budget HALT/escalate`

### Task 1.5: 05-reviewer patch seed

**Files:**
- Modify: `.agents/skills/05-reviewer/SKILL.md` (SEED: patch variant = handoff +
  patch record + owning REQ blocks; scope bounded) ;
  `references/review-discipline.md` (§SEED patch note)
- Test: extend `.agents/skills/05-reviewer/evals/check_review.py` — on a patch
  fixture: attestation present, seed manifest lists the patch record, honesty gates
  unchanged (a planted INFERRED still blocks SHIP).

- [x] Steps: grader-first → implement → A/B → **Commit** `feat(05-reviewer): patch-mode seed variant (isolation + honesty gates unchanged)`

### Task 1.6: 06-release patch naming

**Files:**
- Modify: `.agents/skills/06-release/SKILL.md` + `references/release-gate.md` +
  `templates/release-report.md` (report name `release-report-patch-NNN.md`; G1–G7
  wording covers "sprint N or patch NNN"; nothing waived)
- Test: extend 06 evals — patch fixture: BLOCKED/RELEASED report lands at the
  patch-keyed filename; all seven checks evaluated.

- [x] Steps: grader-first → implement → A/B → **Commit** `feat(06-release): patch-keyed release reports; gates unchanged`

### Task 1.7: status patch awareness

**Files:**
- Modify: `.agents/skills/status/SKILL.md` + `references/next-command.md`
  (precedence: P1 integrity → **patch-in-flight → its next seat** → P2 governance →
  P3 → P4 advisory) + `references/integrity-and-governance.md` (scan
  `docs/planning/patches/`; A6 advisory: ≥3 consecutive done-patches since last
  sprint OR any `escalated` → advisory text "this cadence is a sprint — run
  /01-planner plan-sprint N / consider /08-refactor assess")
- Test: extend `.agents/skills/status/evals/` — (a) patch in flight → next command
  is the patch's next seat; (b) three consecutive patches → advisory line present;
  (c) truth untouched (byte-identical guarantee still holds).

- [x] Steps: grader-first → implement → A/B → **Commit** `feat(status): patch-in-flight routing + patch-pressure advisory`

### Task 1.8: terseness invariant (budget headers + W5 + check_budget)

**Files:**
- Modify: `.agents/skills/00-discovery/templates/scripts/verify-spine.py`
  (register `W5_spine_density`, WARN: lines under `docs/spec/**` excluding
  `evals/**` ÷ registry REQ count > 40 → "likely restated methodology / copied
  prose — one home per fact")
- Modify: every template this revision set touches gains a header line
  `<!-- budget: ≤N lines -->` (seed N from the committed hand-ideals: system.md
  ≤250 · feature-spec ≤120 · qa-report ≤150 · REQ block ≤25 · exploration
  skeleton ≤80)
- Create: `docs/eval-methodology/harness-reference/check_budget.py` (shared
  helper: read the produced artifact's template budget line; assert produced ≤
  budget; imported by the big-producer graders 00/03/05/06 and the integration
  grader)
- Test: `validate_script.py` gains a W5 fixture (a bloated spine fires it); a
  `check_budget` unit case (over-budget artifact fails).

**Interfaces:** Produces `W5_spine_density` (WARN) · `check_budget(artifact_path,
template_path) -> None|AssertionError`. WARN in the script; **hard only in
Layer-A graders** (hard-failing users on length invites truncation-gaming).

- [x] **Step 1:** W5 + check_budget failing fixtures. **Step 2:** implement
  (3-line registry addition + helper). **Step 3:** validation green.
- [x] **Step 4: Commit** — `feat(shared): terseness invariant — W5 spine density + template budgets + check_budget`

**Phase 1 exit:** ✅ **MET (2026-07-08).** full per-skill suites green + `validate_script.py`
green (12/12: ideal + 10 degenerates + check_budget self-test) + the composed patch-lane
live run `01→04→05→06→status` green — all five seats verified correct, spine byte-identical
through every leg (`git diff fc50c4f -- docs/spec` empty). Evidence + grader-artifact catalogue:
`_artifacts/skills-eval/patch-lane-chain/iteration-1/README.md`. Phase-2 handoff:
`_artifacts/phase-2-continuation.md`. (Four grader-robustness follow-ups logged — unit graders
made chain-aware; not blockers.)

---

## Phase 2 — WS2: 00-Discovery Front Door
*(fresh session; read `revision-ws2-design.md`; seat: 00 + shared)*

### Task 2.1: EARS mandate + must-not REQs + numbers rule

**Files:**
- Modify: `.agents/skills/00-discovery/references/requirements-authoring.md`
  (EARS section: the five patterns + mapping table verbatim from design §D; the
  MANDATE sentence; must-not = Unwanted-behavior form; numbers-need-sources rule) ;
  `templates/spec/specification.md` + `templates/spec/capabilities/_EXAMPLE.md`
  (statement-line examples in EARS form)
- Test: `check_spine.py` gains `ears_statement_shape` — every REQ block's statement
  line matches one of five regexes:
  `^The .+ SHALL .+` · `^WHEN .+, the .+ SHALL .+` · `^WHILE .+, the .+ SHALL .+` ·
  `^WHERE .+, the .+ SHALL .+` · `^IF .+, THEN the .+ SHALL .+`
  — plus: a security-flavored fixture yields ≥1 IF/THEN (must-not) REQ; a seeded
  sourceless number in the input doc must NOT appear in the spine unquoted (grader:
  the number string appears only with a `source:` quote or a marker/assumption tag).

- [x] **Step 1:** regex grader + degenerate validation (free-form statement fires it).
- [x] **Step 2:** run against iteration-1 outputs → FAILS (pre-EARS) — expected.
- [x] **Step 3:** implement the reference/templates; **re-seed the affected unit
  fixtures' expected patterns** (graders must not demand EARS of *old committed
  fixture spines* used by 01/02/03 — scope the check to 00's own outputs). *(No
  re-seed needed: grep confirmed no 01/02/03 grader asserts statement-line shape;
  `check_spine.py` is the sole caller, so EARS is scoped to 00's outputs.)*
- [x] **Step 4:** live A/B (rich-spec + thin-spec + security-flavored) green. **Step 5: Commit** —
  `feat(00-discovery): EARS-mandated statement lines + must-not REQ form + numbers-need-sources`

### Task 2.2: CHALLENGE enrichments

**Files:** Modify `references/challenge-2x2.md` (+ Devil's-Advocate turn +
pre-mortem question + confident-but-no-evidence trap) ; `references/review-gate.md`
(present both).
**Test:** transcript/gate-artifact assertions — dissent + pre-mortem present at the
gate on the `undefended-bet` fixture.
- [x] grader-first (assumption-map `## Devil's advocate` + `## Pre-mortem` sections;
  ideal passes, degenerate-without fires, willingness-to-pay stays independent) →
  implement (challenge-2x2 forcing moves + evidence trap; review-gate presents both)
  → A/B (undefended-bet with_skill 12/12; baseline fails the structural checks) →
  **Commit** `feat(00-discovery): devil's-advocate + pre-mortem + evidence traps in CHALLENGE`

### Task 2.3: EXPLORE mode

**Files:**
- Modify: `SKILL.md` (mode section before phase 1; description trigger phrases:
  "brainstorm", "explore an idea", "I have an itch") ;
- Create: `references/explore-divergence.md` (PULL/DIVERGE/APPETITE/PICK craft per
  design §B — facilitate-don't-generate, `origin: model` tagging, Torres test,
  Mom-Test prompts, don't-build outcome) ; `templates/exploration.md`
- Test: new eval cases — (a) bare itch → `docs/discovery/exploration.md` with ≥3
  framings + origins + appetite + decision; **zero files under `docs/spec/`**
  (structural: the outputs tree has no docs/spec) ; (b) pressure-to-converge prompt
  → divergent round still present (or explicit user-override recorded).

**Interfaces:** exploration.md sections: `## Framings` (each: statement ·
`origin: user|model` · Torres-test line) · `## Appetite` · `## Decision`.
- [x] grader (`check_explore`, inverted: no-spine + exploration.md; +degenerates:
  spec-file-written fires the hard invariant; 2-framings fires ≥3) → implement (SKILL.md
  Modes dispatch table + EXPLORE stub; `references/explore-divergence.md` with inline
  ≤80-line skeleton — `templates/exploration.md` NOT created; artifact-map row) → A/B
  (explore + explore-refusal with_skill 6/6; baseline 1/6 — converged) → **Commit**
  `feat(00-discovery): EXPLORE mode — divergent, spine-locked, may end in don't-build`

### Task 2.4: ADOPT mode

**Files:**
- Modify: `SKILL.md` (adopt mode: EVIDENCE SCAN → candidates all `derived` with
  `source: code:<path:line>` or `docs:<path>` → adopt-flavored CHALLENGE →
  Constitution PROPOSED-only → gate + confirm sweep flipping to
  `source: "adopt-confirmed: code:<path>"` → WRITE SPINE incl. verify-script
  emission [seam S4]) ; description triggers ("adopt this codebase",
  "reverse-engineer a spec")
- Create: `references/adopt-evidence.md` (scan taxonomy + zombie-feature challenge
  + confirm sweep) ; eval fixture `evals/fixtures/adopt-mini/` — a ~6-file toy app
  (a CLI with 3 commands, one obviously-dead feature, an auth invariant) built by
  hand.
- Test: `check_spine.py --case adopt` — every REQ `derived` pre-gate with a
  **resolving** `code:` path (grader opens the path); the planted zombie feature
  appears at the gate (transcript) or as an out-of-scope note — never a silent
  keep; Constitution items marked PROPOSED pre-gate; registry↔leaf integrity;
  `scripts/verify-spine.py` present in outputs.

- [x] fixture (`adopt-mini`: 7-file CLI, dead `export_pdf` zombie, wired auth invariant) + grader
  (`--case adopt`: adopt-sourced · anti-hallucination code-resolution · zombie-surfaced · auth-invariant;
  hand-ideal 13/13 + degenerates: dangling path fires anti-hallucination, zombie-as-REQ fires the zombie
  check; path extractor stops at the quote so the design's `"adopt-confirmed: code:<path>"` resolves) →
  implement (SKILL.md 4-row table + ADOPT stub; `references/adopt-evidence.md`; seam S4 emission
  enumeration) → A/B (adopt with_skill 13/13; baseline 0/1) → **Commit**
  `feat(00-discovery): ADOPT mode — brownfield spine-from-code with resolving evidence`

**Phase 2 exit:** ✅ **MET (2026-07-08).** 00 suite green **end-to-end**, freshly run with the final skill —
`rich-spec` 15/15 · `thin-spec` 11/11 · `undefended-bet` 12/12 · `no-doc` 11/11 · `security-flavored` 10/10 ·
`explore`/`explore-refusal` 6/6 · `adopt` 13/13 (each with_skill green; baselines show lift). All new checks
grader-validated (hand-ideal + degenerates). `shared/artifact-map.md` gained the `exploration.md` row (in 2.3's
commit). Evidence: `_artifacts/skills-eval/00-discovery/iteration-2/README.md`.

---

## Phase 3 — WS3: Agentic Project Profile
*(fresh session; read `revision-ws3-design.md`; all seats + shared. Implement in
the order below — each task's Interfaces feed the next.)*

### Task 3.1: `shared/agentic-profile.md` + the profile field
**Files:** Create `shared/agentic-profile.md` (profile registry · THE per-seat
toggle table [S3: sole home — router/STOP/02-skip all cite it] · eval-suite
acceptance contract · three doctrine lines). Modify:
`templates/spec/specification.md` (+ `- **Profile:** webapp` line + comment) ·
`shared/spine-boundary.md` (+ eval-datasets-are-declarations line) ·
`shared/artifact-map.md` (+ agent-contract row, `docs/spec/evals/**` rows,
deferred model-migration entry) · `templates/agents-view.md` (+ profile mirror
[S7]).
**Test:** verify-script gains `W4_profile_missing` (WARN, defaults webapp) —
register via the Task-1.1 registry; validate fires on a profile-less spine.
- [x] register W4 + validate → write the shared file + template lines → **Commit** `feat(shared): agentic-profile protocol + profile field + spine-boundary dataset line`

### Task 3.2: 00 agentic branch + agent-contract
**Files:** Modify 00 `SKILL.md` (profile decision at the REVIEW gate; agentic
branch questions) ; Create `templates/spec/agent-contract.md` (six sections
verbatim: Autonomy tier · Risk class · Tool-permission matrix
`| Tool | Scopes | Risk | HITL |` · Escalation/HITL policy · Cost envelope ·
Memory policy + the S8 boundary sentence; the same sentence added to
`templates/spec/architecture-constraints.md`).
**Test:** agent-flavored fixture (`evals/fixtures/agent-brief/brief.md`) → spine
carries `Profile: agent-system` + complete agent-contract (all six section heads +
≥1 tool row with HITL column + a cost line) + ≥1 IF/THEN must-not REQ; baseline
comparison per A/B.
- [x] fixture + grader (+degenerate: missing HITL column fires) → implement → A/B → **Commit** `feat(00-discovery): agentic discovery branch — profile at the gate + agent-contract spine file`

### Task 3.3: eval-suite acceptance + L6
**Files:** Modify `references/requirements-authoring.md` (+ eval-block form
verbatim from design §C + the S5 sentence: Gherkin for deterministic outcomes,
eval block for distributional, both when layered) ; register
`L6_dataset_refs_resolve` (FAIL) in the verify script (every
`dataset: docs/spec/evals/...` line in any REQ block resolves).
**Test:** validate_script degenerate: dangling dataset ref → L6 fires; a REQ block
with an eval block passes registry checks.
- [x] L6 + validation → reference edits → **Commit** `feat(00-discovery+shared): eval-suite acceptance blocks + L6 dataset-ref integrity`

### Task 3.4: 02 agent-experience mode
**Files:** Modify 02 `SKILL.md` (profile switch reading the S3 table) ; Create
`references/agent-experience.md` (tool-surface/conversation/persona/refusal/HITL-UX
craft; manifest rows keep `DM-NNN`, point at tools/turns).
**Test:** agent fixture → design artifacts cover the tool surface (manifest rows
reference tool names from agent-contract) ; skill-pack fixture → 02 not required
(no design demanded — asserted via status routing in 3.10).
- [x] grader-first → implement → A/B → **Commit** `feat(02-designer): agent-experience realization mode (tool surface as the UX)`

### Task 3.5: 03 ADR categories + eval-suite oracle + profile-aware STOP
**Files:** Modify `templates/adr.md` (+ `Category:` line: memory | model-binding |
topology | durability | isolation | observability | classic) ·
`references/reconcile-architecture.md` (topology ADR REQUIRES the 15×-economics
justification under agent profiles) · `references/feature-spec.md` (+ oracle type
`eval-suite`: `harness cmd · dataset ref · floor`; Design-Contract STOP consults
the profile table [S3]) · MCP named checks (no token passthrough · SSRF egress ·
human-confirm irreversible · tool budget ≤8) as VC rows under `mcp-server`.
**Test:** agent fixture demanding a swarm → topology ADR present with an economics
line; VC rows include ≥1 `eval-suite` row; mcp fixture → the four named checks
appear as VC rows. Degenerate: swarm without justification fires.
- [x] graders → implement → A/B → **Commit** `feat(03-architect): agentic ADR categories + eval-suite oracle + MCP checks + profile-aware STOP`

### Task 3.6: 04 eval-first RED + grader-bites
**Files:** Modify `references/build-discipline.md` (+ eval-suite rows: RED = the
failing case observed pre-fix; grader-bites = a degenerate output must fail the
grader before the row counts EXECUTED).
**Test:** agent build fixture → handoff VC carry-forward shows RED-note for an
eval-suite row + a grader-bites line. Degenerate: tautological grader fires.
- [x] grader-first → implement → A/B → **Commit** `feat(04-builder): eval-first RED + grader-bites for eval-suite rows`

### Task 3.7: 05 mandatory llm-review + tally fields
**Files:** Modify 05 `SKILL.md` + `references/llm-review.md` (mandatory under
agent profiles; floors re-run at final_commit with pinned seeds/config; judge >90%
rule retained; hack-resistance spot-check) ; `templates/qa-report.md` frontmatter
adds **exactly** `eval_floors_met: true|false|n/a` + `evals_run: <int>` [S6].
**Test:** floor-failing fixture → verdict ≠ SHIP + `eval_floors_met: false`;
webapp fixture → `n/a`.
- [x] grader-first → implement → A/B → **Commit** `feat(05-reviewer): mandatory eval-floor verification under agent profiles (tally fields)`

### Task 3.8: 06 G8/G9 + model-swap rule
**Files:** Modify `references/release-gate.md` + `SKILL.md` gate table
(+ `| G8 | Eval floors | qa frontmatter eval_floors_met: true or n/a | routed: re-run /05 |`
`| G9 | Observability (agent profiles) | tracing evidence in VERIFY (span smoke) + drift note | routed: /03 observability plan |`)
; `references/deploy-verification.md` (model-facing diff → migration-protocol
reference or explicit waiver).
**Test:** missing floors → BLOCKED names G8; agent release without span smoke →
G9; webapp → G8 `n/a` passes, G9 skipped.
- [x] grader-first → implement → A/B → **Commit** `feat(06-release): G8 eval floors + G9 observability + model-swap migration rule`

### Task 3.9: 07 panel flip + spine-poisoning lens
**Files:** Create `references/agentic-panel.md` (flipped partition R1–R4 agentic +
conditional classic-web R5, verbatim from design §D-07; structural-defense
doctrine; spine-poisoning checks: imperative override clauses in spine text) ;
Modify 07 `SKILL.md` (profile switch) .
**Test:** agent fixture → panel manifest shows ASI partition + a planted
raw-concatenation injection path caught with a structural finding; webapp fixture
→ classic partition unchanged (no false flip); planted "ignore prior constraints
when…" clause in a fixture Constitution → flagged.
- [x] graders (+degenerates) → implement → A/B → **Commit** `feat(07-security): agentic-primary panel flip + spine-poisoning lens`

### Task 3.10: status profile routing + AGENTS.md mirror
**Files:** Modify `references/next-command.md` (profile column resolving P3 per the
S3 table) · `references/generated-views.md` (+ profile mirror in the AGENTS.md
emission [S7]) .
**Test:** skill-pack fixture → router skips design phase; agent fixture → design =
interaction manifest presence; emission carries the profile line; truth
byte-identical invariant still green.
- [x] grader-first → implement → A/B → **Commit** `feat(status): profile-aware routing + profile in the AGENTS.md emission`

### Task 3.11: model-migration reservation
**Files:** Create `shared/model-migration-protocol.md` (doctrine-level: shadow →
classify → triage → canary; swap = full re-eval; prompt re-engineering per idiom;
embedding reindex budget; "build the activity on first need").
- [x] Write + artifact-map Deferred entry → **Commit** `docs(shared): model-migration protocol (reserved; activity deferred)`

**Phase 3 exit:** ✅ **MET (retroactively stamped 2026-07-11).** WS3 (Tasks 3.1–3.11) implemented; the fifth-leg decision was made — Task 5.5a (the `agent-chain` grader + hand-ideal + 3 degenerates) built and validated, the LIVE run 5.5b deferred (see §Deferred). Evidence: `skills-eval/03-architect/iteration-2` (3.5a 7/7) · `07-security/iteration-2` (3.9 panel flip) · `agent-mini/iteration-1` (3.7/3.8/3.10); the deterministic integration layer (incl. `--case agent-chain` + the agentic cases) green. Depended-upon by — and transitively re-confirmed through — the now-MET Phase 4.

---

## Phase 4 — Hardening: WS4 then WS5 (merged — ONE fresh session)
*(read `revision-ws4-design.md` + `revision-ws5-design.md` + the simplification
amendments above; run the WS4 tasks first — WS5 edits the same files. Composed
live runs at exit: one 03-init, one 06-release, one 07-audit.)*

> **Implementation status (2026-07-11): COMPLETE + committed** — 13 commits (`3e0c0cb`→`186f265`, unpushed on `main`).
> All WS4 (4.1 · 4.2 · 4.3 · 4.4 · 4.5+4.7-merged · 4.6) + WS5 (5.1 · 5.2 · 5.3 · 5.4a · 5.4b · 5.5a) tasks landed,
> **each with a deterministic grader validated (ideal + degenerates) before commit**. `5.5b` (the live six-seat
> agent-chain) is **DEFERRED** (`shared/artifact-map.md` §Deferred). The **Phase-4-exit live verification** (the 3
> composed with_skill runs + the 5.2/5.3 task-level A/B) is now **COMPLETE (2026-07-11)** — see **Phase 4 exit**
> below; the how-to was `_artifacts/phase-4-exit-continuation.md`.

### WS4 tasks

- **Task 4.1 (D1):** 00 `requirements-authoring.md` coverage facet 7 (ISO 25010,
  quantified) · 03 `templates/system.md` §10 rule: every scenario names a fitness
  function or `deferred: <why>` · 05 `references/verification-evidence.md` re-runs
  them. Graders: prose-only scenario fires; seeded NFR → scenario + command line.
  **Commit** `feat(00+03+05): quantified NFRs + executable fitness functions`
- **Task 4.2 (D2):** `templates/system.md` + § Test Strategy (shape + rationale ·
  contract stance · PBT candidates · flake policy: ticket/owner/2-week SLA).
  Grader: section presence + a named shape + the SLA line.
  **Commit** `feat(03-architect): declared test strategy + flake quarantine policy`
- **Task 4.3 (D3):** `templates/feature-spec.md` + Observability row ·
  `templates/deployment-config.md` + `## Operations` (one SLO · logs · alert ·
  drill cadence). Graders per template. **Commit** `feat(03+06): observability rows + Operations section (one-SLO floor)`
- **Task 4.4 (D4):** feature-spec migration row (forward cmd + rollback data
  implications) · `release-gate.md` + G10 (conditional: migrations present ⇒
  backup step on destructive + rollback implications stated; else N/A-with-reason).
  Degenerate: destructive-without-backup fires G10.
  **Commit** `feat(03+06): migration contracts + conditional G10`
- **Task 4.5 (D5):** `deploy-verification.md` + SBOM step (syft/cdxgen attempted,
  absence recorded WARN) · `templates/release-report.md` + provenance block
  (artifact digest · commit · toolchain) + **ML-BOM component fields under agent
  profiles** (models/datasets/frameworks — lands here, referenced by WS5-H4.6).
  **Commit** `feat(06-release): SBOM step + provenance block (+ML-BOM fields, agent profiles)`
- **Task 4.6 (D6):** `templates/system.md` + § Threats considered (Four Questions
  over the C4 trust boundaries; mitigation link or accepted-risk per threat) · 07
  `references/synthesis-and-verdict.md` completeness lens cross-ref (designed
  threat without check = gap; finding in a "safe" zone = routed design feedback).
  Graders both sides. **Commit** `feat(03+07): design-time threat pass + audit cross-reference`
- **Task 4.7 (D7):** register `--hash` mode in verify-spine.py (sha256 over sorted
  relative-path+bytes of `docs/spec/**`) · `templates/release-report.md`
  frontmatter + `spine_hash:` + `amendments_at_release:` · 06 REPORT step computes
  via the script. Test: hash recomputes identically; any spine byte change alters
  it. **Commit** `feat(06+shared): spine release identity (verify-spine --hash)`

---

### WS5 tasks (same session, after the WS4 tasks)

- **Task 5.1 (H1):** `templates/spec/architecture-constraints.md` +
  `- **ASVS target level:** L1` (00 writes default) · 07
  `references/synthesis-and-verdict.md`: completeness lens re-anchored on ASVS
  V1–V14 via CWE tags; report template gains the chapter-coverage table
  (`| Chapter | Status | Evidence |`, Status ∈ verified/partial/N-A) + frontmatter
  `asvs_level:` + counts · `references/owasp-panel.md` partition-vs-bar note.
  Graders: table scoped to declared level; missing declaration → WARN + L1
  recorded. **Commit** `feat(07-security): ASVS 5.0 verification bar (declared level, chapter coverage, evidence schema)`
- **Task 5.2 (H2):** re-audit contract: per-finding `proof_of_fix` column —
  closes only with a failing→passing regression test that **bites on revert**
  (revert-check mechanic mirrors 08's oracle-bites; command captured) · 04
  `build-discipline.md` one line (security fixes ship their regression test —
  names the existing TDD-for-bugs). Degenerate: "fixed" finding without test stays
  open. **Commit** `feat(07-security): proof-of-fix regression enforcement at re-audit`
- **Task 5.3 (H3):** `references/agentic-panel.md` + the dynamic arm: attack
  corpora = must-not eval datasets under `docs/spec/evals/security/` (promptfoo
  `owasp:agentic` documented; garak/PyRIT scheduled-optional); ASR floors (0% for
  HITL-bypass/irreversible; per-REQ otherwise); **PASS requires the arm executed
  or an explicit user-gated waiver recorded**; guardrails count only with a bypass
  regression case. Graders: seeded injection fixture → ASR breach = High finding;
  arm unexecuted + no waiver → not PASS. **Commit** `feat(07-security): adversarial runtime arm (ASR-gated, waiver-explicit)`
- **Task 5.4 (H4):** R4 + slopcheck + dependency-cooldown policy line (04
  build-discipline mirror) · scanners + `mcp-scan` (agent profiles) + optional
  ZAP-baseline (both recorded-if-absent) · Create 00
  `templates/SECURITY.md` (contact · CVD expectations · response window), emitted
  at WRITE SPINE; 06 G7 wording + SECURITY.md presence · `deployment-config`
  Operations + 3 IR lines (preserve · assess · notify-within-X). Structural
  graders each. **Commit** `feat(00+04+06+07): security floor batch — slopcheck/cooldown, mcp-scan, SECURITY.md+G7, IR lines, ZAP-opt`
- **Task 5.5: fifth integration leg — `agent-chain`.** Extend
  `docs/eval-methodology/integration/` with `--case agent-chain`: seed an
  agent-flavored brief → live fresh-subagent chain `00 (profile+contract) → 01 →
  03 (topology ADR + eval-suite VC) → 04 → 05 (floors) → status`; grader asserts
  the composed invariants (profile propagates; contract complete; an eval-suite VC
  row carried to EXECUTED with grader-bites; qa tally fields present; router
  agent-aware). Validate grader on a hand-ideal + 3 degenerates (missing contract;
  floor-fail-yet-SHIP; topology-without-justification) BEFORE the live run.
  **Commit** `test(integration): §10 fifth leg — agent-chain composes the profile end-to-end`

**Phase 4 exit:** ✅ **MET (2026-07-11).** The Phase-4-exit live verification ran on real **Sonnet** arms
(orchestrator **Opus 4.8**), confirming the WS4/WS5 grader assertions on real output — not just hand-built ideals:
- **3 composed with_skill runs.** 03-architect `init`+`sprint 1` → `_artifacts/skills-eval/03-architect/iteration-3/`
  **20/20** (S13 fitness functions · S14 Test Strategy · S15 Observability · S16 migration N/A · S17 Threats; realizer
  arm + a **fresh-context isolated reconciler**). 06-release `sprint 1` → `.../06-release/iteration-3/` **18/18**
  (`grade_operations` D3 · `grade_provenance` D5+D7 with a real 64-hex `spine_hash` · `grade_security_md` 5.4a ·
  `grade_g10` D4 N/A). 07-security `sprint 2` vuln → `.../07-security/iteration-3/vuln/` **20/20**
  (`grade_threat_crossref` D6 · `grade_asvs` H1; a real 4-reader blind panel).
- **2 task-level live A/Bs.** 5.2 proof-of-fix (H2), `.../07-security/iteration-3/proof-of-fix-h2/`: with_skill
  **20/20** (`grade_proof_of_fix` PASS — the bite-on-revert **mechanically executed**) vs baseline **FAIL** (an
  unproven close). 5.3 dynamic arm (H3), `.../07-security/iteration-3/dynamic-arm-h3/`: with_skill **6/6** (flipped
  agentic panel + the dynamic arm **executed**, ASR 100% → Critical + spine-poison) vs baseline **4/5** (no flip).
- **A grader-robustness fix a live run surfaced.** `check_security.py grade_proof_of_fix`'s N/A gate keyed on the bare
  words "re-audit"/"proof_of_fix" — it mis-fired on a correct *initial* audit (routing / a conscientious N/A
  addendum) and missed a decorated `**CLOSED**` status cell. Re-keyed on an **asserted close-status**; the
  discriminator (a biting-revert test is required to close) is unchanged, re-validated against four hand-built reports
  (initial-audit N/A · proven-close PASS · unproven-close FAIL · kept-open N/A). The H3 fixture (`beacon-sec`) was
  extended with the attack suite `docs/spec/evals/security/prompt-injection.jsonl` + a must-not `REQ-004`
  (`metric: ASR`, parsed by the shared `eval_block.py`).
- Iteration READMEs force-added under `_artifacts/skills-eval/{03-architect,06-release,07-security}/iteration-3/`.
  `5.5b` (the live six-seat agent-chain) remains **DEFERRED**. **Not pushed.**

---

## Self-review (done at write time)

- **Spec coverage:** every WS1–WS5 design section maps to a task (WS1 A1–A7→1.3–1.7,
  B1–B5→1.1–1.2; WS2 A–E→2.1–2.4; WS3 A–F→3.1–3.11; WS4 D1–D7→4.1–4.7; WS5
  H1–H4→5.1–5.4). Seams: S1 in 1.3/1.4 gate text (already folded into designs),
  S2→1.1/3.3/4.7, S3→3.1/3.5/3.10, S4→2.4, S5→3.3, S6→3.7/3.8, S7→3.1/3.10,
  S8→3.2.
- **Placeholders:** none — where full prose lives in a design record, the task
  names the section AND locks the contract tokens here.
- **Type consistency:** `review_mode`, tally fields, check IDs, profile values,
  gate numbers G8/G9/G10 each defined once (Global Constraints) and referenced
  identically.
