# Artifact Map — canonical storage & naming (Fullstack Director)

> The **single source** for *where every durable artifact lives and how it's named.* Every skill cites this for its
> read/write paths; `/status` integrity-checks reality against it. This file deliberately **replaces** a
> hand-maintained "Document Flow Table" (which silently drifts). Here the map is one referenced
> artifact, and each `SKILL.md` *also* self-declares its own I/O — the skill is the source of truth for its own
> paths; this map is the cross-skill index.

## Two layers (never collide — the framework repo is not itself a target project)

- **Project artifacts (Layer B)** — what skills create *in the user's project*. Governed by SDLC/SDD practice.
- **Framework layout (Layer A)** — the Fullstack Director repo itself. Governed by skill-creator conventions.

## Project artifacts (Layer B)

**Role:** D = declaration (spine; amendment-gated) · R = realization (references REQs; drift-gated) ·
K = decision/learning · gen = generated view · E = ephemeral (gitignored). **Owner** = the skill that writes it.

| Path | Owner | Role | Notes |
|------|-------|------|:------|
| `docs/spec/specification.md` | 00 | D | index: Constitution + REQ registry (authoritative ID→file) |
| `docs/spec/capabilities/<domain>.md` | 00 | D | REQ blocks, by domain; **outcome-level** Gherkin |
| `docs/spec/design-intent.md` | 00 | D | 02 may only *amend* |
| `docs/spec/architecture-constraints.md` | 00 | D | 03 may only *amend* (Tier-2 gate + ADR); holds the **`## Verify-live`** block (WS6 — too-new techs; adding/changing the set = Tier-2) |
| `docs/verification/<tech>.md` | 00 seeds · 03/04 append | R | **WS6** — per-tech live-source ledger (`verified_against` + cited **Verified claims** table); a realization **outside `docs/spec/**`** (excluded from `spine_hash`; a patch may update it). L7 + 06 G11 read it |
| `docs/verification/judges/<judge>.md` | 04/05 write · 05 reads | R | judge-validation record (pinned model · TPR/TNR · splits · `validated_at_commit`); realization outside `docs/spec/**`; backs `grader: judge(validated)` (`shared/agentic-profile.md` §eval-suite) |
| `docs/spec/agent-contract.md` | 00 | D | **`agent-system` profiles only** — the agency declaration (autonomy tier · tool-permission matrix · HITL · cost envelope · memory policy); 02/03 may only *amend* (Tier-2). See [`agentic-profile.md`](agentic-profile.md) |
| `docs/spec/evals/<domain>/<name>.jsonl` | 00 seeds · 05 grows | D | **golden eval datasets** (distributional / agent behaviors); a dataset *is* the behavioral spec — edits = amendments; a patch may only ADD cases (Tier-1 auto-row). Verify-script `L6` checks every REQ `dataset:` ref resolves |
| `docs/spec/amendment-log.json` | 00 init · 02/03/08 append | D | structured rows; no date (git is the trail) |
| `docs/discovery/charter.md` | 00 | K | product charter + go/pivot/kill decisions + reflect log |
| `docs/discovery/exploration.md` | 00 | K | EXPLORE-mode divergence record (framings · origins · appetite · decision); **never writes `docs/spec/**`** |
| `docs/discovery/*.md` | 00 | K | discovery working artifacts (e.g. `assumption-map.md`) |
| `docs/README.md` | 00 | R | legibility index: "spec/ = truth; the rest references REQ-NNN" |
| `scripts/verify-spine.py` | 00 | gen | standing spine gate (L1–L7 FAIL / W1–W5 WARN; L6 = eval `dataset:` refs resolve; **L7** = verify-live records resolve, bidirectional + cited — WS6); emitted **verbatim, always** at WRITE SPINE |
| `scripts/hooks/{pre-commit.sample,spine-verify.yml}` | 00 | gen | **opt-in** wiring samples (git hook · GH Actions); user copies to activate |
| `SECURITY.md` | 00 | gen | vulnerability-disclosure **CVD floor** (contact · CVD window · scope boundary); emitted **always** at WRITE SPINE; **06 G7** checks its presence |
| `docs/planning/backlog.md` | 01 | R | execution ledger REQ→epic→sprint→status (**status originates here**); + the `## Patches` ledger (sole patch-status origin) |
| `docs/planning/sprints/sprint-NN.md` | 01 | R | slice: REQ refs + frozen outcome-acceptance snapshot |
| `docs/planning/patches/patch-NNN.md` | 01 | R | certified patch record (P1–P5 evidence; **no status field** — status lives in the Patches ledger) |
| `docs/design/design-system.md` | 02 | R | references REQs |
| `docs/design/<screen>.md` | 02 | R | kebab-case screen names |
| `docs/design/approved/sprint-NN/{manifest.md,*.png,prototype/}` | 02 | R | design contract (DM-NNN manifest) |
| `docs/architecture/system.md` | 03 | R | C4 + domain model |
| `docs/architecture/adr/ADR-NNN.md` | 03 | R | **03 = sole ADR allocator**; 08 requests `max+1` |
| `docs/architecture/adr/README.md` | 03 | R | ADR index (allocation source) |
| `docs/architecture/specs/<feature>.md` | 03 | R | feature spec + detailed Verification Contracts |
| `src/**` | 04 | R | source + tests |
| `docs/quality/qa-report-sprint-NN.md` | 05 | R | verdict SHIP/FIX/BLOCK; verification states |
| `docs/release/deployment-config.md` | 06 | R | platform/server/env-var names (no secrets) |
| `docs/release/release-report-sprint-NN.md` | 06 | R | deploy / health / smoke results |
| `docs/security/security-audit-sprint-NN.md` (or `-full.md`) | 07 | R | OWASP + risk matrix; PASS/REMEDIATE/BLOCK |
| `docs/refactoring/{health-assessment,refactor-plan,refactor-report}-sprint-NN.md` | 08 | R | optional skill |
| `AGENTS.md` | 00 (+ `/status`) | gen | read-only emission of the Constitution; **"do not edit"** header. Consumed natively by Codex; Claude/Gemini consume it via the bridges below |
| `CLAUDE.md` | 00 creates-if-absent · status § Current State | gen | line 1 = **`@AGENTS.md`** (the Claude Code bridge — created by 00, `templates/claude-bridge.md`) + `§ Current State` (derived status only, written by `/status`); an existing user file is **never edited** (advisory only) |
| `GEMINI.md` | 00 | gen | the Gemini CLI bridge — one line `@./AGENTS.md` (`templates/gemini-bridge.md`), create-if-absent; zero-file alternative = `.gemini/settings.json` `context.fileName` (documented in `docs/harness-support.md`, not emitted) |
| `_artifacts/screenshots/<phase>-sprint-NN/` | 02/05/08 | E | gitignored |
| `_artifacts/exports/build-handoff-sprint-NN.md` | 04 | E | the reviewer subagent's seed (build→review contract) |
| `.claude/rules/quality-guardrails.md` | 05 | R | accumulated guardrails |
| `.claude/rules/deployment-guardrails.md` | 06 | R | accumulated deploy guardrails (failure → rule; read before every deploy plan) |
| `.claude/rules/security-guardrails.md` | 07 | R | accumulated security guardrails (recurring vuln class → a pre-audit check) |

**Retired — do NOT create:** `docs/planning/requirements-brief.md`,
`docs/planning/user-stories/US-NNN.md`. Their content now lives in the spine + the backlog ledger.

## Framework layout (Layer A)

```
.agents/skills/<NN-role>/   SKILL.md · templates/ · references/ (per-skill) · evals/ (scripts+graders+fixture-defs)
                            # CANONICAL — open Agent Skills convention; discovered natively by Codex CLI + Gemini CLI
.claude/agents/fsd-*.md     the subagent definitions (fsd-reviewer · fsd-reconciler · fsd-owasp-reader) — the
                            spawn branch of shared/subagent-protocol.md; CANONICAL SOURCE, vendored to consumers
                            (their skills: preload resolves only in a consumer — inert here, by design)
                            # NOTE (2026-07-12): the master commits NO .claude/skills bridge — the seat skills
                            # auto-trigger and pollute framework-dev sessions; .claude/skills is a CONSUMER-only
                            # emission (gitignored here; the vendor self-test's real-tree case guards it)
tools/vendor.py             the vendoring CLI (sync/check/--self/--self-test) — placement + filtering + provenance;
                            per-file EOL-normalized sha256 manifest; skip-and-report local-mod protection
shared/                     spine-boundary.md · spec-amendment-protocol.md · subagent-protocol.md · artifact-map.md ·
                            agentic-profile.md · live-source-verification.md · feedback-loop.md (the dogfood→
                            upstream contract) · model-migration-protocol.md (reserved doctrine)
AGENTS.md                   framework-level cross-harness instructions — the Layer A entry point
CLAUDE.md                   line 1 = `@AGENTS.md` → Claude bridge + methodology/governance precedence
docs/                       eval-methodology/ (+ harness-reference/ — fallback only) · harness-support.md
README.md · LICENSE · .gitignore
```
Skills: `00-discovery` · `01-planner` · `02-designer` · `03-architect` · `04-builder` · `05-reviewer` ·
`06-release` · `07-security` · `08-refactor` · `status` · `feedback` (cross-cutting — the consumer-side capture
half of `shared/feedback-loop.md`; writes only the consumer's `docs/framework-feedback.md`).

**Built 2026-07-12 (formerly deferred):** the **vendor CLI** (`tools/vendor.py` — one command deploys a consumer:
runtime-only `.agents/skills/` for Codex+Gemini + the `.claude/skills/` copy for Claude + `shared/` + the fsd-*
subagent files + the seeded feedback ledger + the `.director/vendor-manifest.json` provenance/drift manifest), the
Claude **dev bridge** (this repo's committed `.claude/skills/`), and the **subagent definition files**. Scope note:
emission targets are the three verified harnesses (Claude Code · Codex CLI · Gemini CLI — `docs/harness-support.md`);
Windsurf/Cline/web bundles were cut, not deferred (no consumer). Consumer-repo artifacts the vendor owns:
`.director/vendor-manifest.json` (gen) · `docs/framework-feedback.md` (maintained ledger — the ONE vendored file a
consumer writes; append-only per `shared/feedback-loop.md`).

**Deferred activities (documented non-commitments — the doctrine is written; the activity is built only on
first need, and no roadmap is implied):**
- **Model migration** — [`shared/model-migration-protocol.md`](model-migration-protocol.md) is a doctrine-level
  spec (shadow → classify → triage → canary; a model/provider swap = a full re-eval). The **activity** (06's
  swap-detection gate wiring, the diff-classification harness) is a non-commitment, built only when a project
  actually swaps a model — 06's model-swap rule under `agent-system` names the moment.
- **Integration §10 fifth leg — the LIVE `agent-chain` run (5.5b)** — the `--case agent-chain` **grader** + a
  hand-ideal + 3 degenerates are **built** (`docs/eval-methodology/integration/`, validated deterministically). The
  **live** fresh-subagent six-seat chain (`00 profile+contract → 01 → 03 topology+eval-suite VC → 04 → 05 floors →
  status`) is a non-commitment, built only when: the first real `agent-system` project runs, or a
  composed-invariant bug appears that the deterministic grader cannot reproduce.

## Naming conventions

- **Sprint token:** `sprint-NN` — **lowercase, zero-padded — everywhere** (filenames, dirs, report suffixes).
  Zero-pad so `sprint-01 … sprint-10` sort correctly. (No more `SPRINT-NN`/`sprint-N` split.)
- **ID schemes:** `REQ-NNN` · `ADR-NNN` · `AMD-NNN` · `DM-NNN` — all `TYPE-NNN`, zero-padded.
- **Names:** kebab-case for screens, features, domains.
- **Ephemeral vs committed:** everything under `_artifacts/` is gitignored scratch; everything else is committed.

## Single-source & allocation rules

1. The **REQ registry** (`specification.md`) is authoritative for ID→file; updated in the **same step** as any REQ write.
2. **01 is the sole REQ-ID allocator; 03 is the sole ADR allocator.** Others request `max+1`.
3. **No hand-maintained cross-skill flow table.** Each `SKILL.md` self-declares its I/O; this map is the index;
   `/status` derives/verifies the live view. (A hand-synced table drifts — we don't do that.)
4. `AGENTS.md` and any amendment *table* are **generated views** — regenerated, never hand-edited.

## Eval conventions

- **Per-skill `evals/` exist** (graders + fixture definitions), built same-commit as each skill, plus the cross-skill
  integration chain under `docs/eval-methodology/integration/` — following **`/skill-creator` best practice** (the
  `with_skill`-vs-`baseline` A/B + deterministic graders validated on a hand-ideal + degenerates before commit).
- **Eval run-workspaces live OUTSIDE `.claude/skills/**` and `.agents/skills/**`** — `with_skill` subagents refuse to
  write fixtures there; use a top-level gitignored workspace under `_artifacts/skills-eval/` at eval-time.
- `docs/eval-methodology/harness-reference/` is a **fallback** for Windows / `<SUBAGENT-STOP>` edge cases only.

## What belongs in the spine vs. a skill artifact

See [`spine-boundary.md`](spine-boundary.md): the declaration-vs-realization test — *a declaration is anything the
user would object to changing silently.*
