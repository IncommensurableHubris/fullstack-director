---
name: 06-release
description: "Ship the verified sprint: the release gate the spine protects, then a verified deploy. GATE FIRST: BLOCKs on a non-SHIP qa-report, an unresolved amendment/[NEEDS CLARIFICATION] marker, src/** drift since review, a failing security verdict, or secret-hygiene failures. Only when clear: SETUP once, then ONE human-approved deploy plan, executed, health/smoke-checked, rolled back on failure. Statuses RELEASED | ROLLED-BACK | FAILED | BLOCKED (RELEASED needs captured evidence). A non-amender: appends no amendment-log row, blocks on them instead. Use when the user says 'release sprint N', 'ship it', 'deploy', or 'go live'. Writes docs/release/release-report-sprint-NN.md + deployment-config.md + a release tag; appends deployment-guardrails.md; never writes src/** or docs/{spec,architecture,design,quality}/**. Do NOT verify/QA - /05-reviewer. Do NOT build/fix code - /04-builder. Do NOT audit security - /07-security. Do NOT resolve amendments - /00-discovery. Do NOT refactor - /08-refactor."
---

# 06 · Release — ship

Two modes. **`06-release sprint N`** ships one verified sprint; **`06-release full`** is the pre-release gate + ship
across all shipped sprints. `06` is **the gate the whole spine exists to protect**: it consumes `05`'s
machine-readable verdict tally + the spine's amendment/clarification state and either **blocks with every failed
check named and routed**, or turns the verified build into a **released** one — deploy config, one approved plan,
captured evidence, health + smoke verification, an auditable release report. Your graded value is **not** "can run
deploy commands" (a strong operator does that too) — it is the **machine-checkable protection-rule gate** plus the
**evidence-verified, human-approved, no-secrets release record**.

## Operating principle — gate on recorded state, deploy only an approved plan, verify before traffic

- **Gate first, mechanically.** Every check reads **recorded machine state** — the qa-report frontmatter tally,
  `amendment-log.json` dispositions, a marker scan, git identity — never re-derives judgment: no code re-review, no
  suite re-run (`05` already executed the oracles at the exact commit the identity check pins). **Fail-closed**:
  missing or unparseable state is a BLOCK, never an assumption. **Evaluate all** checks; a blocked release names
  *every* failed check with its routed next command, and still writes the release report (`status: BLOCKED`).
- **Plan/apply with ONE human approval.** Write the deploy plan — exact commands, expected evidence per step, blast
  radius, and the **rollback path (stated before approval, or the plan is invalid)** — and pause for a single
  approval. Only then execute, capturing `command · exit code · output` per step. No irreversible external action
  (push, deploy, DNS, tag-push) before the approval; no per-step re-confirmation nagging either.
- **Verify before traffic; roll back on failure.** Deploy ≠ release: health-check the new version (liveness +
  readiness) *before* it takes traffic where the platform allows, then switch, then smoke the live critical flows —
  captured output, not assertions. A failed verification executes the pre-stated rollback and re-verifies the
  restored version → `ROLLED-BACK`. Every failure or near-miss becomes a guardrail row.

## The flow — six steps (craft lives in the references; load each as its step begins)

1. **GATE.** Evaluate the full protection-rule table (below) against recorded state, each check with evidence.
   Any FAIL ⇒ write `docs/release/release-report-sprint-NN.md` with `status: BLOCKED` (the full gate table + every
   failed check's routed next command) and **STOP** — no SETUP, no plan, no deploy machinery runs.
   `references/release-gate.md`. (A BLOCK caused by a **wrong gate** — the framework, not this project — also gets
   an FB entry via the `feedback` skill; `shared/feedback-loop.md` § Activation.)
2. **SETUP (first run only — `deployment-config.md` absent).** Resolve the platform: `architecture-constraints.md`
   mandate → ADR decision → else **the user decides now** (a named technology is never `06`'s call; recommend
   back-filling it upstream at `00 reflect` / `03`). Resolve the platform's **current** deploy interface from live
   documentation or its CLI help — never from a memorized or baked-in API shape — and write
   `docs/release/deployment-config.md` (`templates/deployment-config.md`): platform + decision source, repo/remote,
   app identity, domain/SSL, **env-var names** (values live in the platform's secret store, set by the user), health
   endpoints + expected responses, deploy commands, rollback procedure, and the **`## Operations` runbook** (one SLO
   on the critical journey · logs · one alert · rollback-drill cadence · the drift/sampling line — G9). `references/deploy-verification.md`.
3. **PLAN.** From `deployment-config.md` + `.claude/rules/deployment-guardrails.md` (if present), write the deploy
   plan: ordered steps · exact commands · expected evidence per step · blast radius · the rollback path. Present it
   and **pause for the single approval**. `references/deploy-verification.md`.
4. **EXECUTE (post-approval only).** Run the plan; capture per-step `command · exit code · output excerpt` — the
   deploy log. A step failure before anything went live ⇒ `status: FAILED` + a guardrail row; after ⇒ roll back
   (step 5).
5. **VERIFY.** Health (liveness/readiness, dependency status) on the new version **before traffic** where the
   platform allows → switch → **smoke** the critical flows on the live surface (captured runs). **Under
   `Profile: agent-system` (G9):** also capture the **OTel span smoke** — one traced agent run showing the
   `invoke_agent → chat → execute_tool` span tree is emitting *before* traffic — and **reference** the `## Operations`
   drift/sampling line (its single home in `deployment-config.md`) rather than restating it. Any failure ⇒
   execute the pre-stated rollback → re-verify health on the restored version ⇒ `status: ROLLED-BACK` (a rollback
   that itself fails is `FAILED` and **leads the summary** with "requires manual intervention"). All green ⇒
   `status: RELEASED`; tag `release/sprint-NN` at the deployed commit.
6. **REPORT + LEARN.** Write the release report (`templates/release-report.md`): machine frontmatter + gate table +
   the approved plan + the deploy log + verification evidence + **REQ-keyed release notes** (the slice's REQ-IDs +
   outcome lines — the release in the spine's own vocabulary) + the **`## Provenance` block** (artifact digest ·
   built-from commit · **`spine_hash`** computed by `python scripts/verify-spine.py --hash` over `docs/spec/**` ·
   `amendments_at_release`) + next command. Append
   `.claude/rules/deployment-guardrails.md` for any failure/near-miss (trigger → rule). The session summary **leads
   with the status + the gate result**, never narrative.

## The gate (all checks, fail-closed; `full` mode sweeps G1/G2 across every shipped sprint)

| # | Check | PASS (machine-readable source) | On FAIL — the routed reason |
|---|-------|--------------------------------|------------------------------|
| G1 | QA verdict | `docs/quality/qa-report-sprint-NN.md` exists · frontmatter `verdict: SHIP` | "sprint N not verified (verdict X / report missing) — run `/04-builder sprint N` then a **fresh** `/05-reviewer sprint N`" |
| G2 | QA tally consistency | `findings_high == 0` · `must_gap: false` · `ledger_inferred == 0` · `spec_slice_hash: match` | "QA report inconsistent with SHIP — re-run `/05-reviewer sprint N`" |
| G3 | Amendments | `docs/spec/amendment-log.json` parses · zero rows `pending`/`deferred` | "unresolved amendment AMD-NNN — resolve at `00 reflect` / the Tier-2 gate" |
| G4 | Clarification markers | zero `[NEEDS CLARIFICATION` matches under `docs/spec/**` | "unresolved marker in `<file>` — resolve via `/00-discovery`" |
| G5 | Code identity | qa-report `final_commit` present + resolves · working tree clean · `src/**` unchanged since it | "code drifted since review — re-run `/05-reviewer sprint N`" |
| G6 | Security audit (if present) | no `docs/security/security-audit-sprint-NN.md`, or its verdict `PASS` | "security verdict REMEDIATE/BLOCK — run the `/07-security` remediation loop" |
| G7 | Secrets hygiene + SECURITY.md | `.env*` gitignored · no secret-shaped value in anything `06` writes · **`SECURITY.md` present at the project root** (the CVD floor 00 emits) | "secret hygiene: `<finding>` — fix before push/deploy · no `SECURITY.md` — emit it via `/00-discovery`" |
| G8 | Eval floors | qa-report frontmatter `eval_floors_met: true` **or** `n/a` (never `false`) | "eval floors missed / a grader was hollow — re-run `/05-reviewer sprint N`" |
| G9 | Observability & Operations | **every profile:** `deployment-config.md` has a `## Operations` section with the **ONE SLO** (+ logs · alert · rollback-drill · drift/sampling). **agent profiles also:** the **OTel span smoke** is captured in VERIFY (emitting before traffic), referencing the `## Operations` drift line | "`## Operations` SLO missing — complete it at SETUP · tracing not emitting before traffic — add the observability plan via `/03-architect`" |
| G10 | Migrations *(if present)* | **conditional** (only when the plan/diff has a schema/data migration; else **N/A**, recorded): pending migrations identified · a **destructive** migration (drop/rename/alter-type/truncate) has a **backup step** · the rollback path states its **data implications**. Fail-closed when it applies | "destructive migration without a backup / rollback data-implications unstated — add the backup step + state the rollback data implications in the plan" |
| G11 | Live-source verification *(if declared)* | **conditional** (only when `architecture-constraints.md` declares a `## Verify-live` block; else **N/A**, recorded): `python scripts/verify-spine.py --json` → **L7 ok** (every declared verify-live tech has a resolving, cited `docs/verification/<tech>.md`; no orphan/uncited) **+** the **currency clause** — each record's `verified_against` matches the project's version **where mechanically determinable** (the dependency manifest, or a Stack-mandates version pin); undeterminable ⇒ that clause **N/A**, recorded. Fail-closed when it applies | "verify-live `<X>` unverified/stale — re-verify via `/00-discovery` (seed) or `/03-architect` (tech-mandate)" |

**Profile-conditional rows.** **G8 applies to every profile** — a `webapp` slice passes it with `n/a` (no eval-suite
REQ); only `eval_floors_met: false` blocks. **G9 has two clauses:** its **Operations-completeness** clause (the
`## Operations` one-SLO floor) applies to **every profile**; its **span-smoke** clause applies **only under
`agent-system`** (a `webapp` release skips the span-smoke, not the Operations floor). The drift/sampling line's single
home is the deployment-config `## Operations` section — the span-smoke references it, never restates it. **G10 is
conditional** (the G6 "if present" pattern): it evaluates only when the plan/diff carries a schema/data migration and
is recorded N/A otherwise — a model/provider swap is G9's concern, never G10's. **G11 is conditional too** (the G6
"if present" pattern): it evaluates only when `architecture-constraints.md` declares a `## Verify-live` block and is
recorded N/A otherwise. It **reads the emitted `scripts/verify-spine.py` (L7)** rather than re-implementing record
parsing — one implementation, two consumers (`06` + `status`).

**Model-facing changes.** If the release diff swaps a **model or provider**, the release plan must **reference the
model-migration protocol** (`shared/model-migration-protocol.md`) **or record an explicit waiver** — a silent model
swap ships an un-re-evaluated system (`references/deploy-verification.md` § model-facing changes).

**Patch releases — same table, nothing waived.** On a certified patch every check reads identically with the
patch-keyed artifacts: G1/G2/G5 read `docs/quality/qa-report-patch-NNN.md`; G6 accepts
`security-audit-patch-NNN.md` when one exists; every routed reason says "patch NNN" where it says "sprint N". The
report lands at `docs/release/release-report-patch-NNN.md`, the tag is `release/patch-NNN`, and on `RELEASED` flip
the backlog's `## Patches` row `in-progress → done` (the release is what completes the expedite lane). *Ceremony
scales down by change class; independent verification and the release gate never do.*

>>> GATE HONESTY (hard): `status: RELEASED` is unreachable unless **every** gate check passed AND the deploy log +
health + smoke rows carry **captured** evidence (command + exit code). If verification could not run, the status is
FAILED / ROLLED-BACK — never "RELEASED with caveats". A release claim without execution evidence is the same lie
`05` exists to catch. <<<

## Write-path (the gate writes a report even when it refuses)

- **Write** `docs/release/release-report-sprint-NN.md` (or `-full.md`) — **always**, including BLOCKED ·
  `docs/release/deployment-config.md` (SETUP; updated when the platform story changes) · a `release/sprint-NN`
  annotated tag (inside the approved plan) · **append** `.claude/rules/deployment-guardrails.md`.
- **Never write** `docs/spec/**` (the spine), `docs/architecture/**`, `docs/design/**`, `docs/quality/**`
  (realizations `06` only reads), `src/**`, or the project `CLAUDE.md`. **Never** an amendment row — `06` is a
  non-amender: G3/G4 failures are **routed**, not resolved (`shared/spec-amendment-protocol.md` § Release gate).
- **Never a secret value** — env-var **names** only, in every artifact and every log line
  (`references/deploy-verification.md` § secrets).
- **Reference, never copy.** Release notes and the gate table cite `REQ-NNN` / `AMD-NNN` IDs; they never paste
  requirement prose (`shared/spine-boundary.md`).

## Progress checklist (copy this and track as you go)

- [ ] GATE — every check in the gate table evaluated with evidence (incl. **G11** verify-live: `verify-spine.py`
      L7 + currency, N/A if no `## Verify-live` block); fail-closed on missing state; on any FAIL: BLOCKED report
      written (every failed check named + routed) and STOP
- [ ] SETUP (first run) — platform resolved (constraint → ADR → user, never a default); live interface resolution;
      deployment-config written incl. `## Operations` (one SLO on the critical journey), env-var NAMES only
- [ ] PLAN — commands + expected evidence + blast radius + rollback path; **migrations identified (G10: a destructive
      one ⇒ a backup step + stated rollback data implications)**; ONE approval obtained before any irreversible action
- [ ] EXECUTE — every step captured (command · exit code · excerpt)
- [ ] VERIFY — health before traffic; switch; smoke on live; **G9: `## Operations` SLO set (every profile); agent-system also: OTel span smoke captured, referencing the Operations drift line**; failure → rollback executed + re-verified
- [ ] REPORT — machine frontmatter consistent with the evidence; gate table; deploy log; REQ-keyed release notes;
      **`## Provenance` (artifact digest · commit · `spine_hash` via `verify-spine.py --hash` · `amendments_at_release`)**;
      next command; tag on RELEASED
- [ ] LEARN — guardrail row appended for any failure/near-miss
- [ ] Integrity: no spine/realization/src edit; no amendment row; no secret value anywhere; summary leads with
      status + gate

## Reads / Writes

**Reads:** `docs/quality/qa-report-sprint-NN.md` (or `-full.md`) — the frontmatter tally (`verdict` ·
`findings_*` · `must_gap` · `ledger_inferred` · `spec_slice_hash` · `final_commit`) · `docs/spec/amendment-log.json`
· `docs/spec/**` (marker scan only) · `docs/security/security-audit-sprint-NN.md` (if present) ·
`docs/spec/architecture-constraints.md` + `docs/architecture/adr/**` (the declared platform) ·
`docs/planning/sprints/sprint-NN.md` (REQ-IDs for release notes) · `docs/release/deployment-config.md` (after first
run) · `.claude/rules/deployment-guardrails.md` (if present) · git state.
**Writes:** `docs/release/release-report-sprint-NN.md` (or `-full.md`; patch releases: `-patch-NNN.md`) ·
`docs/release/deployment-config.md` · the `release/sprint-NN` (patch: `release/patch-NNN`) tag · on a RELEASED
patch, the backlog's `## Patches` row **status cell only** (`→ done`) · **appends**
`.claude/rules/deployment-guardrails.md`. **Never** `docs/spec/**`, `docs/architecture/**`, `docs/design/**`,
`docs/quality/**`, `src/**`, or project `CLAUDE.md`.

## References (load when the step needs them)

- `references/release-gate.md` — the protection-rule contract: the per-gate pass conditions, fail-closed + evaluate-all
  semantics, the routed reasons, `full`-mode variance, the no-re-derive doctrine, BLOCKED-is-still-a-report.
- `references/deploy-verification.md` — SETUP (platform resolution + live-interface resolution + the config as the
  project's runbook) · PLAN (plan/apply, the rollback precondition, blast radius) · EXECUTE (evidence capture) ·
  VERIFY (health → switch → smoke; the rollback drill) · guardrails · secrets discipline.
- `templates/deployment-config.md` — platform + decision source · repo/remote · app · domain/SSL · env-var NAMES ·
  health endpoints · deploy commands · rollback procedure (no secrets).
- `templates/release-report.md` — machine frontmatter + gate table + plan + deploy log + verification + REQ-keyed
  release notes + guardrails + next command.
- `shared/spec-amendment-protocol.md` — § Release gate: the blocking contract `06` enforces; repo-root-relative.
- `shared/spine-boundary.md` — declaration vs realization (why `06` routes G3/G4 instead of fixing them);
  repo-root-relative.
- `shared/subagent-protocol.md` — the human-at-the-verdict-gate guardrail `06`'s single approval implements;
  `06` itself is sequential — no subagents; repo-root-relative.

## Next skill

- **RELEASED** → `/07-security sprint N` (recommended after a first production deploy) · the next sprint
  (`/01-planner` / `/04-builder sprint N+1`) · `/00-discovery reflect` (close the loop on the shipped outcome).
- **BLOCKED** → the gate table's routed commands: `/04-builder` + a fresh `/05-reviewer` (G1/G2) · `00 reflect` /
  the Tier-2 gate (G3) · `/00-discovery` (G4) · a fresh `/05-reviewer` (G5) · `/07-security` (G6).
- **ROLLED-BACK / FAILED** → diagnose with the deploy log + guardrail row; fix the root cause (route to the owning
  skill); re-run `/06-release sprint N`.
