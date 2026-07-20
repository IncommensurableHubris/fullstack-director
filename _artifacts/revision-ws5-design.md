# WS5 Design — Security-Seat Hardening

> Revision workstream 5 (added at the user's request after the WS1–4 coherence
> review): close the gap between `07-security` (+ the WS2–4 security additions) and
> gold-standard AppSec practice for classic web AND agentic systems, at solo scale.
> Status: **APPROVED** (user, 2026-07-06) — all three defaults confirmed.
> Research grounding: OWASP's own Top-10-vs-ASVS positioning (awareness doc vs
> verification standard) · ASVS 5.0 (14 chapters, CWE-tagged, ~60–70% automatable,
> L1 realistic for solo) · OWASP GenAI Red Teaming Guide + Q2-2026 AI Security
> Landscape ("traditional AppSec no longer sufficient"; static-only inadequate —
> +37.6% critical vulns over five AI revision loops, IEEE-ISTAS 2025) · promptfoo
> `owasp:agentic` (ASI01–10 plugins; PR-gateable) · garak / PyRIT · proof-of-fix
> regression doctrine ("a red-team suite that prints results is documentation; one
> that fails the build is a guardrail") · slopcheck (19.7% dep-hallucination rate;
> the react-codeshift incident spread via AI-generated skill files) · Snyk
> Agent Scan / mcp-scan · CycloneDX ML-BOM (v1.5+, stable; Agent-BOM only a
> proposal) · CRA reporting trajectory (Sep 2026 / Dec 2027) · SECURITY.md/CVD as
> the solo floor.

---

## H1 — ASVS 5.0 becomes the verification bar (the structural fix)

**The gap:** OWASP itself positions the Top 10 as an *awareness* document and ASVS
as the *verification standard*. 07 partitions readers over Top-10 categories — it
divides work by the awareness artifact and measures completeness against it too.
For a seat whose verb is *verify*, that is sub-gold-standard.

**The fix (partition stays, the bar changes):**
- **New declaration: `ASVS target level`** in `architecture-constraints.md` —
  default **L1** (the researched solo bar: "modern framework defaults + targeted
  hardenings already comply with most of it"); **L2 only with recorded
  justification** (sensitive data), a Tier-2 decision. 00 writes the default at
  spine time.
- **Reader partition unchanged** (Top-10 / ASI areas divide the work well); the
  **synthesizer's completeness lens re-anchors on ASVS chapters V1–V14** via their
  CWE tags. The report's checklist section becomes an **ASVS chapter-coverage
  table** scoped to the declared level: per chapter — verified / partial / N-A +
  the evidence pointer (test, scanner, or reader judgment).
- **Per-release evidence schema:** machine frontmatter in the audit report — level
  target, chapters covered, requirement-check counts, audit date (staleness
  visible; G6 semantics unchanged).
- The ~58% test-automatable / ~10% scanner-automatable / ~30% judgment-only split
  is made explicit: the readers' manual remit IS the judgment-only band (business
  logic, authz consistency, architectural intent) — exactly what a fresh-context
  panel is for.

## H2 — Proof-of-fix: a finding closes only with a regression proof

**The gap:** 07 routes findings to `/04` but nothing requires the fix to carry
proof; remediation is unverified until someone re-audits from scratch.

**The fix:** a REMEDIATE finding **closes only when the fix includes a
failing→passing regression test** (or, for agentic findings, an ASR-gated
red-team case — H3). 04's fix pass already does TDD-for-bugs, so the *builder*
side is free; the **enforcement lands in 07's re-audit**: per finding, verify the
regression proof exists and bites (fails on revert — the 08 oracle-bites
mechanic). The re-audit report gains a per-finding `proof_of_fix` column; a fixed
finding without proof stays open. Enforcement belongs to the re-auditor, not the
fixer (segregation of duties, again).

## H3 — The adversarial runtime arm (agent profiles; static-only is inadequate)

**The gap:** the panel — including WS3's flipped agentic partition — *reads*; it
cannot catch what only fires at runtime. 2025–26 consensus is explicit that
static-only agentic security audit is inadequate.

**The fix (maximum reuse of WS2/WS3 machinery):**
- **Attack corpora are must-not eval datasets**: each high-risk must-not REQ
  (WS2's EARS Unwanted-behavior form) may carry an eval block (WS3) whose dataset
  is an **attack suite** under `docs/spec/evals/security/` — prompt-injection,
  jailbreak, tool-misuse cases. The floor inverts: **attack-success-rate ASR ≤ X%**
  (default 0% for HITL-bypass and irreversible-action cases).
- **07 gains a dynamic arm** under agent profiles: run the adversarial suites
  (promptfoo `owasp:agentic` covers ASI01–10 natively; garak/PyRIT documented for
  scheduled deep runs, optional). Executing probes is verification-asset work —
  the 05 fallback-cascade precedent — and leaves 07 read-only w.r.t. code.
- **Verdict integration:** an ASR breach is a High/Critical finding (severity from
  the violated must-not REQ's priority). For agent profiles, **PASS requires the
  adversarial arm to have executed** — or an explicit, user-gated waiver recorded
  in the report (capability-probe honesty: absence is recorded, never silent).
- **Guardrail doctrine extension:** a guardrail (Llama Guard / NeMo / etc.) counts
  as defense-in-depth only — its presence is verified AND it must be
  regression-tested by a bypass case; it never substitutes for the structural
  defenses WS3 requires.

## H4 — The cheap-additions batch (one line each, mapped to the seat)

1. **slopcheck at the install boundary** (verify dep names against the real
   registry before install) + a **dependency-cooldown policy line** (security
   patches immediate; other bumps after a minimum package age) → R4 supply-chain
   reader + one line in 04's `build-discipline.md`.
2. **`mcp-scan` (Snyk Agent Scan)** as the deterministic scanner behind WS3's named
   MCP checks (tool poisoning, rug pulls, shadowing, toxic flows) — recorded-if-
   absent like every scanner → scanners layer, agent profiles.
3. **`SECURITY.md` (contact + CVD expectations)** emitted by 00 at WRITE SPINE
   (template in 00's bundle); presence checked in 06 G7 (release hygiene) → CRA
   trajectory floor.
4. **One-page incident-response lines** in deployment-config `## Operations`
   (WS4 D3): preserve-what, assess, notify-within-X → no new artifact.
5. **ZAP-baseline DAST** as an optional staging scanner (recorded-if-absent) —
   correctly *optional* for solo (SCA → SAST/secrets → DAST priority order).
6. **ML-BOM component fields** in WS4 D5's SBOM step for agent profiles (models,
   datasets, agent frameworks as CycloneDX components — declare, don't build
   bespoke AI-BOM machinery; Agent-BOM is still only a spec proposal).

## Explicitly SKIPPED (recorded as non-goals — gold standard ≠ maximal)

ASVS L2/L3 as default targets · bespoke AI-BOM/Agent-BOM tooling · formal
PSIRT/CVD programs, IR SLAs, threat-intel feeds, red-team staffing · full-scan or
commercial DAST gating · continuous whole-repo scanning platforms. (Solo + AI
scale: PR-gate suites + scheduled deep runs suffice.)

## Eval strategy

1. **ASVS anchor:** audit fixture → report carries the chapter-coverage table
   scoped to the declared level; missing declaration → WARN + default L1 recorded.
2. **Proof-of-fix:** re-audit fixture where a "fixed" finding lacks its regression
   test → the finding stays open (verdict still REMEDIATE); with the test present
   and biting → closes.
3. **Adversarial arm:** agent fixture with a seeded injection path → the attack
   suite fires it (ASR breach → High finding); agent-profile audit with the arm
   unexecuted and no waiver → verdict cannot be PASS.
4. **One-liners:** structural presence checks (SECURITY.md emitted + G7 row;
   cooldown policy line; mcp-scan/ZAP recorded-or-absent).

## Seat-contract deltas

- **07:** `references/synthesis-and-verdict.md` (ASVS completeness lens + evidence
  schema + proof-of-fix column) · `references/owasp-panel.md` (partition note:
  work-division vs verification-bar) · `references/agentic-panel.md` (WS3 file:
  + dynamic arm + ASR + waiver rule + guardrail doctrine) · scanner list (+
  mcp-scan, + optional ZAP-baseline) · report template (ASVS table + frontmatter
  schema).
- **00:** constraints template (+ ASVS level line, default L1) · new
  `templates/SECURITY.md` emitted at WRITE SPINE · artifact-map row.
- **04:** `build-discipline.md` (+ slopcheck + cooldown lines; fix-pass note:
  security findings need the regression proof — already TDD-for-bugs, now named).
- **06:** G7 wording (+ SECURITY.md presence) · D3 Operations section (+ IR lines)
  · D5 SBOM step (+ ML-BOM fields, agent profiles).
- **shared/agentic-profile.md:** the dynamic-arm + ASR rows in the 07 toggle.

## Dependencies

Designs against WS2 (must-not REQs), WS3 (eval blocks, flipped panel, profile),
WS4 (D3 Operations, D5 SBOM). Implements after them; independent of WS1 except the
usual verify-script check registry (no new checks here).

## Resolved decisions (review, 2026-07-06 — all confirmed by user)

1. **ASVS target level defaults to L1**; L2 only with recorded justification
   (a Tier-2 decision).
2. **PASS-requires-adversarial-arm holds in the hard form** for agent profiles:
   the arm executed, or an explicit user-gated waiver recorded in the report —
   never a soft WARN.
3. **ASR floor 0%** for HITL-bypass and irreversible-action must-nots (a breach
   there is never acceptable); other must-nots carry per-REQ floors.

## Simplification deltas (approved 2026-07-07 — authoritative log: revision-simplification-review.md)

- **H1:** keep the chapter-coverage table + declared `asvs_level`; DEFER the
  machine frontmatter counts (trigger: first automation consuming them); no
  date field — git + `audited_commit` carry staleness.
- **H3:** ASR is expressed through the WS3 eval-block `metric:`; the waiver
  reuses 02's Gate *presentation* pattern (one line); plan Task 3.9 leaves a
  reserved `## Dynamic arm — WS5` stub — the arm and the PASS precondition land
  only in Task 5.3, with one shared eval-block parser.
- **H4:** Task 5.4 splits token-paired — 5.4a (00↔06: SECURITY.md + G7 wording +
  IR-on-demand) and 5.4b (04↔07: slopcheck + cooldown + mcp-scan + ZAP); NO
  graders for optional-scanner doc mentions; `mcp-scan` is agent-system scope;
  the CVD window is stated once in SECURITY.md (+ an S8-style boundary sentence).
- ML-BOM: one reserved line in the merged Provenance block (deferred).
