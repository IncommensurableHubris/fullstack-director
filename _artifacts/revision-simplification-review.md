# Revision Simplification Review — WS1–WS5 (approved 2026-07-07)

> Second review pass (after coherence): three blind fresh-context Fable reviewers
> — merge/redundancy · YAGNI/defer · per-seat complexity budget — over the five
> approved designs + plan, with user-approved decisions fenced from re-litigation.
> Sequential synthesis; every finding surfaced; user approved the full set,
> explicitly including #14. This file is the authoritative delta log; the design
> records carry per-record delta sections; the plan carries the operational edits.

## Approved deltas

**A · Mechanism unifications**
1. ASR = a `metric:` value in the ONE WS3 eval-block schema (floors incl. the 0%
   HITL-bypass/irreversible defaults are stated once in requirements-authoring).
2. Security suites execute ONCE: `docs/spec/evals/security/**` carved out of 05's
   re-run remit; 07's dynamic arm is the sole executor (forced by
   PASS-requires-arm). 05's remaining re-runs (functional floors + fitness
   functions) merge into one "re-execute declared verifications" section.
3. One `## Provenance` release-report block: artifact digest · commit ·
   `spine_hash` · `amendments_at_release`; toolchain line cut; ML-BOM = one
   reserved line (deferred).
4. The "bite" rule defined once in `shared/agentic-profile.md`; 04/05/07/08 cite
   it with their seat-specific object.
5. One-home fixes: latency/throughput targets live in architecture-constraints
   only (agent-contract cost envelope references them; S8 sentence extended);
   patch record carries NO `status:` (ledger = sole origin); EXPLORE decision
   lives in exploration.md (charter gets a one-line pointer); ASVS evidence has
   no date field (git + `audited_commit`); CVD window stated once (SECURITY.md).
6. G9 ordering bug fixed: the drift/sampling line's single home is
   deployment-config `## Operations`; G9 = span-smoke evidence (Phase 3) + an
   Operations-completeness clause added when Operations lands (Phase 4).

**B · Seat packaging + terseness**
7. 00-discovery: 4-row mode dispatch table; EXPLORE/ADOPT = 5–8-line stubs
   (invariant + gate marker) with flows AND checklists in their references;
   agentic branch = +2 lines at the REVIEW gate; NOT separate skills. ≈140 lines.
8. 07-security: the profile-selected panel reference IS the manifest; only the
   two verdict preconditions (arm-or-waiver · proof-of-fix) + ONE checklist (two
   profile-conditional items) in SKILL.md; ASVS replaces the completeness-lens
   wording; coverage table template-enforced. ≤175 lines.
9. Terseness invariant (new plan Task 1.8): template budget headers +
   `W5_spine_density` (WARN, lines-per-REQ>40) in verify-spine.py + one shared
   `check_budget()` grader helper (hard in Layer-A graders only).
10. Late-step protection: WRITE SPINE checklist enumerates all five emissions
    (spec · docs/README · AGENTS.md · verify-spine.py · SECURITY.md; adopt path
    too); named checklist lines for 05 floor-re-run/hack-check, 06 span-smoke +
    spine_hash, 07 arm/proof-of-fix, 01 dispatch; 03's checklist names §Test
    Strategy + §Threats considered + the topology-justification gate check.

**C · Eval economics + plan shape**
11. A/B policy: per-task graders (validated: hand-ideal + degenerates) stay;
    task-level live A/B only for the 11 genuinely-new behaviors (1.3, 2.1–2.4,
    3.2, 3.4, 3.5a, 3.6, 3.9, 5.2, 5.3); all template/mechanical tasks are
    covered by ONE composed with_skill live run per phase; baseline arms dropped
    for template-presence assertions (structural-lift doctrine). ~40 runs saved.
    Shared helpers: EARS regexes · eval-block parser · check_budget.
12. Phases 4+5 merge into one hardening session (WS4 tasks first) → 4 sessions.
13. Task shape: 5.4 → 5.4a (00↔06) + 5.4b (04↔07); 3.5 → 3.5a (agent-system) +
    3.5b reserved; 4.5+4.7 merge; 3.9 leaves a `## Dynamic arm — WS5, reserved`
    stub and does not touch the verdict table; plan header recount (34 → ~31
    post-merge/split).

**D · Deferrals (trigger recorded per item)**
14. **mcp-server + skill-pack REALIZATIONS reserved** (user-confirmed): the
    4-value enum, W4 parsing, and toggle-table rows stay (marked "reserved —
    build on first project declaring this profile"); per-seat content defers.
    `mcp-scan` stays under agent-system (it audits CONSUMED servers — R4 remit).
15. Fifth integration leg split: 5.5a (grader + hand-ideal + 3 degenerates) now;
    5.5b (live 6-seat chain) deferred — trigger: first real agent-system project
    or first composed-invariant bug.
16. Also deferred/cut: ASVS machine frontmatter counts (keep table + declared
    level; trigger: first automation consuming them) · ML-BOM fields (reserved
    line; trigger: first agent-system release with a running SBOM step or an
    external provenance consumer) · IR lines marked `on-demand(first release
    with real users/data)` · provenance toolchain line (cut; trigger: SLSA
    attestation consumer) · graders for optional-scanner doc mentions (cut).
17. Core/on-demand template convention: every template section marked `core` or
    `on-demand(<trigger>)`; graders assert core-only on small fixtures. The
    minimum-viable-spine valve.

## Checked and kept (do-not-cut consensus)
Patch 5-check gate ≠ amendment tiers · H3 waiver ≠ Tier-2 (+1 line: reuses 02's
Gate presentation) · S1 dual rows · status inline L1–L5 fallback + parity eval ·
G8 separate from 05's execution · hooks templates (named in a settled decision) ·
W3 padding WARN · cooldown line · SECURITY.md + G7 · exploration.md as artifact
(its template folds into explore-divergence.md) · 02 agent-experience mode ·
model-migration reservation · fitness-function `deferred:` escape.

## Follow-up logged (out of revision scope)
Six existing seat descriptions exceed the Agent Skills 1024-char convention
(07=2294, status=2290); verify no harness truncates — separate maintenance item.
