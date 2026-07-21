# How Fullstack Director relates to the field

> A comparison written for two readers at once: the domain expert deciding whether this framework is for
> them, and the engineer their community sends to check our claims. Every claim about another framework
> traces to that framework's own current documents, read live on **2026-07-21** (versions and commits in
> [§ Sources](#sources-read--as-of-2026-07-21)); every claim about Fullstack Director links the file that
> implements it. If we've gotten something wrong about a framework, [open an
> issue](https://github.com/IncommensurableHubris/fullstack-director/issues) — corrections are a favor,
> and we'll take them.

**The short version.** Spec-driven development is a real, thriving field — GitHub Spec Kit, BMAD-METHOD,
OpenSpec, and Kiro are serious tools, and Fullstack Director adopted ideas from each of them, credited
below. What FD adds is a position none of them occupies: **full SDLC discipline designed for the domain
expert as director** — the lawyer, clinician, or analyst whose expertise becomes the spec, who holds every
consequential gate, and who gets evidence they can read without being able to read the code. To our
knowledge it is the first framework built for that seat. That claim is meant to be falsifiable — the axes
below are checkable, and the corrections line above is not decorative.

## The map — audience × discipline

The obvious objection to *designed for domain experts* is that non-developers are already served: the
prompt-to-app builders — Lovable, Bolt, v0, the Replit class — exist precisely for people who don't write
code. The objection deserves a straight answer, not a dodge. Two questions sort the field: **who is the
tool designed for**, and **how much lifecycle discipline does it impose**?

| | **Designed for developers** | **Designed for domain experts** |
|---|---|---|
| **Governed SDLC** | GitHub Spec Kit · BMAD-METHOD · OpenSpec · Kiro | **Fullstack Director** |
| **Prompt-to-app** | — | Lovable · Bolt · v0 · Replit-class builders |

**The top-left quadrant** is where the serious spec-driven tools live, in their own words — the evidence is
[axis 1 below](#1--stated-audience--in-their-words). Two of the four are visibly broadening what their
*output* can be (Spec Kit's "any business process", Kiro's student designers), and that broadening is real.
But all four still assume the hands on the wheel belong to someone at home in developer tooling — a terminal
and Python for Spec Kit, BMAD, and OpenSpec; a developer IDE/CLI for Kiro — and all four hand the *is the
work actually right?* question back to an operator who is assumed able to judge code.

**The bottom-right quadrant** deserves genuine respect: the prompt-to-app builders opened software creation
to people the industry had locked out, and for a landing page, a prototype, an internal tool, they are
exactly the right call. What the class does not carry is the discipline half of this grid: no spec of *your*
rules that fights back when a new feature collides with an old declaration, no verification gate you can
read without reading code, no release or security seat. The result is directed by your prompts, but not
governed by your rules.

**The top-right quadrant is the empty one** — full SDLC discipline, designed for the domain expert as
director. That is the seat Fullstack Director is built for, and to our knowledge it is the first framework
built for it. The claim is deliberately falsifiable: if a framework already occupies this quadrant, [tell
us](https://github.com/IncommensurableHubris/fullstack-director/issues) and this document will say so.

## Credit first — what FD adopted, and from whom

FD did not invent spec-first discipline. These are the specific ideas it took from the field, by name,
and where each now lives in this repo:

| From | What FD adopted | Where it lives here |
|---|---|---|
| **GitHub Spec Kit** | The project **Constitution** as a first-class artifact; **`[NEEDS CLARIFICATION]` markers** for honest gaps; the spec→plan→tasks **spec-first flow**; the *durable artifacts visible, machinery hidden* **layout rule** | Constitution: [`shared/spine-boundary.md`](../shared/spine-boundary.md) (the spine's `specification.md`); markers: originated at [`00-discovery`](../.agents/skills/00-discovery/SKILL.md), **hardened into a release blocker** at [`06-release` gate G4](../.agents/skills/06-release/SKILL.md); layout: [README § Layout](../README.md) |
| **BMAD-METHOD** | The **structural lint** over spec documents (BMAD's `lint_spine`); **ADR enforceability** — an architecture decision must be checkable, *enforceable rather than a diary entry*; lean-invariants documentation discipline; the **full-SDLC team ambition** | Lint: [`check_spine.py`](../.agents/skills/00-discovery/evals/check_spine.py) + the architecture edition at [`reconcile-architecture.md` §1b](../.agents/skills/03-architect/references/reconcile-architecture.md); ADRs: same file, § MADR; invariants: [`system-architecture.md`](../.agents/skills/03-architect/references/system-architecture.md) |
| **OpenSpec** | The **brownfield mindset** — spec only what you're about to change, never document-the-world first (informed FD's ADOPT entry path); the visible-artifacts layout convention | ADOPT: [`adopt-evidence.md`](../.agents/skills/00-discovery/references/adopt-evidence.md); design record: [`revision-ws2-design.md`](../_artifacts/revision-ws2-design.md) |
| **Kiro** (lineage: EARS is older, Kiro made it native to AI IDEs) | **EARS requirement notation** — adopted, then made *lintable*: FD's spine lint machine-checks the five EARS patterns; **dependency-ordered task discipline** ("tasks build upon each other") | EARS: [`requirements-authoring.md`](../.agents/skills/00-discovery/references/requirements-authoring.md) + enforced in [`check_spine.py`](../.agents/skills/00-discovery/evals/check_spine.py); tasks: [`slicing.md`](../.agents/skills/01-planner/references/slicing.md) § Sources |
| **obra/superpowers · wshobson/agents** | The **`.agents/skills/` packaging convergence** — independent evidence that portable skill trees are where the ecosystem is heading; and FD's own **construction process** (see [Complementary, not competing](#complementary-not-competing)) | [`docs/harness-support.md`](harness-support.md) |

Adoption is dated: FD drew these as of early-to-mid 2026, and the field moves fast — where a framework has
since changed, the axes below describe its **current** state, not the state FD learned from.

## The axes

Eight checkable axes. The table is the scan; the sections after it carry the evidence — their docs' own
words for every "they" claim, this repo's files for every FD claim. Where we say *not found*, it means not
found in the pages read on 2026-07-21 (listed in [§ Sources](#sources-read--as-of-2026-07-21)) — treat it
as a dated observation, never an accusation, and correct us if we missed it.

| # | Axis | Spec Kit | BMAD-METHOD | OpenSpec | Kiro | Fullstack Director |
|---|---|---|---|---|---|---|
| 1 | Stated audience | "your whole organization"; outputs broadening beyond software | "comfortable with basic software development concepts" | "you and your AI coding assistant" | "developers and teams" | the domain expert directing |
| 2 | Spec granularity | per-feature dirs + one constitution | spine docs + per-story files | `specs/` truth + `changes/` deltas | per-spec 3-file folders | one living spine, declarations only |
| 3 | Change management | markers + clarify; persistence is team convention | update intents surface conflicts | propose→apply→archive; review by convention | refine + sync; gates skippable | 3-tier amendments, quoted, logged, release-blocking |
| 4 | Verification | read-only consistency, same context | multi-lens review, fresh context where supported | structural blocks; semantic optional | EARS→property tests; supervised modes | evidence states + isolated reviewer; ship blocks on inference |
| 5 | Roles | verb commands (+ role bundles) | named personas + verb skills | verb commands only | modes, not personas | functional verbs only |
| 6 | Lifecycle coverage | spec→implement core; rest via extensions | analysis→implementation (+ TEA module) | the change loop | spec→build→test; partial security/deploy | discovery→security→release + refactor/status |
| 7 | Framework self-testing | strong CLI tests; prompt-output evals not found | structural CI; behavioral evals not found | code-level tests; evals not found | not found | per-skill A/B evals + adversarial track, published |
| 8 | Portability | 34 integrations, per-tool generation | installer, many tools + web bundles | 34 tools, one abstraction | own five surfaces + ACP; third-party harnesses prohibited | open `.agents/skills`; three verified harnesses |

### 1 · Stated audience — in their words

None of the four says *for developers* as a bare sentence; the field's actual words are more interesting.
Spec Kit's README pitches a toolkit "built for your whole organization", and its docs have broadened past
code — "guiding it across your SDLC or any business process", "you're never locked to SDD, or even to
software" — with community presets reaching as far as fiction writing. Kiro's homepage says "Kiro helps
developers and teams do their best work", while its Students page runs testimonials from designers crossing
into building. BMAD's docs state the baseline most plainly: "You should be comfortable with basic software
development concepts like version control, project structure, and agile workflows." OpenSpec defines itself
as "A lightweight layer that gets you and your AI coding assistant to agree on what to build, in writing,
before any code is written." — and answers the vibe-coder question with honest terms: "If you're looking
for a magic tool that plans everything for you without any effort on your part, this isn't it. […] it works
best when you meet it halfway."

The pattern across all four: the *output* audience is broadening — Spec Kit and Kiro visibly so — but the
designed *operator* is still a technically fluent builder who installs from developer tooling and judges
the work as a developer would. Fullstack Director is designed from the opposite end: the director is
assumed expert in law, health, finance — not in code ([README](../README.md)); discovery interviews them
and writes the spec in their words ([`00-discovery`](../.agents/skills/00-discovery/SKILL.md)); every gate
they hold is phrased as a domain decision, not a diff.

**For a domain-expert director:** the question is not whether a tool *can* produce non-software output —
it's who the tool assumes is steering, and what that person must already know for their rules to bind.

### 2 · Spec granularity — many files or one spine

Spec Kit gives each feature its own auto-numbered directory (`spec.md`, `plan.md`, `tasks.md`, and friends)
plus one project constitution; what happens to those files after requirements change is explicitly a team
choice among three models — "None is the default, and none is required by Spec Kit." OpenSpec keeps two
folders — "Two folders. `specs/` is what's true. `changes/` is what you're proposing." — and truth grows
one archived delta at a time. BMAD mixes single living documents (`ARCHITECTURE-SPINE.md`, a five-field
`SPEC.md` kernel) with per-story files. Kiro creates a three-file folder per spec (`requirements.md` in
EARS, `design.md`, `tasks.md`).

FD's bet is stricter: **one living spine** (`docs/spec/`) holds *all* declarations — Constitution, REQ
registry, design intent, architecture constraints — and nothing else lives there. Everything derived
(designs, ADRs, code, tests) is a *realization* that references `REQ-NNN` and may never restate spine
prose. The boundary has a test a non-engineer can apply — *would you object if this changed without your
say-so?* — written down as the framework's keystone ([`shared/spine-boundary.md`](../shared/spine-boundary.md)).

**For a domain-expert director:** your rules live in one place with one history — you never have to
remember which of thirty feature folders holds the current version of your confidentiality rule.

### 3 · Change management — how your declarations change

Spec Kit ships honesty machinery we adopted and credit above: `[NEEDS CLARIFICATION]` markers in the spec
template and a `/speckit.clarify` command to burn them down; its constitution template's example governance
line reads "Amendments require documentation, approval, migration plan", and its workflow engine has a
first-class human `gate` step. BMAD's update intents "reconcile an existing PRD with a change signal,
surfacing conflicts before applying changes", with a PASS/CONCERNS/FAIL readiness check and a decision-log
pattern. OpenSpec's whole lifecycle is change-shaped — propose → apply → sync → archive, deltas merged
mechanically — and its docs are candid that the two human review moments are convention: verify "does not
block archiving". Kiro specs are "designed for continuous refinement" with approval gates between phases —
and a Quick Plan mode that legitimately skips them.

FD treats a change to the spine as a governed event, not an edit: every skill that finds the spine wrong
files an **amendment row** in one of three tiers — auto-apply (one defensible answer), gate (user-visible
change: pause for the director), defer (scope change: decided row-by-row at reflect) — each row carrying
the source quote that motivated it, with **escalate-when-uncertain** as the classification rule
([`shared/spec-amendment-protocol.md`](../shared/spec-amendment-protocol.md)). A patch lane keeps urgent
fixes inside the same discipline. And the release seat refuses to ship while any row is unresolved
([`06-release` gates G3/G4](../.agents/skills/06-release/SKILL.md)).

**For a domain-expert director:** everyone's specs can change. The axis is whether a change to *your*
declarations can happen — or ship — without you. Here it structurally can't.

### 4 · Verification — belief, review, or evidence

Spec Kit's core checks are read-only consistency passes over the artifacts (`/speckit.analyze`, checklists
it frames as unit tests for plain-English requirements) run in the *same* agent context that produced the
work. Its changelog shows honest engineering here: a forked-subagent `/analyze` for Claude shipped
2026-06-19 and was reverted a week later "to prevent long-session freezes" — so isolation was tried, and
same-context is the current state. BMAD is the closest to FD on this axis, and says why in one line: "Run
reviews with fresh context (no access to original reasoning) so you evaluate the artifact, not the intent"
— multi-lens review runs in parallel subagents where the harness supports it, with real candor about
adversarial review's false-positive cost ("You decide what's real."). OpenSpec separates a structural
`openspec validate` (which blocks archiving) from a semantic `/opsx:verify` (optional, same-context,
non-blocking). Kiro executes: EARS requirements feed property-based testing that "generates hundreds or
thousands of random test cases", with stated limits ("PBT cannot guarantee the absence of all bugs") —
the strongest code-versus-spec loop of the four.

FD's verification stands on two legs at once. **Evidence states:** every acceptance item lands in exactly
one of `EXECUTED` / `OBSERVED` / `INFERRED` — reading code is inference, never evidence — and release is
unreachable while anything material is inferred
([`verification-evidence.md`](../.agents/skills/05-reviewer/references/verification-evidence.md),
[`06-release`](../.agents/skills/06-release/SKILL.md)). **Isolation:** the reviewer is seeded fresh — build
handoff and spec slice only, never the build conversation — and states its inputs in a context attestation
([`shared/subagent-protocol.md`](../shared/subagent-protocol.md)). BMAD shares the second leg's principle;
Kiro shares the first leg's execution instinct; FD's distinct move is wiring both to a release gate that
fails closed.

**For a domain-expert director:** you can't audit code, but you can audit evidence. *Ran, observed,
inferred* is a vocabulary a non-engineer can hold a gate with.

### 5 · Roles — personas or verbs

BMAD staffs named specialists — Mary the analyst, Winston the architect, Amelia the developer — and the
choice is deliberate and defended ("you can’t rename her — that’s deliberate"); Party Mode even ships an
anti-groupthink rationale for running personas in separate subagents ("one model voicing five personas can
quietly converge: they share a mind"). Spec Kit's core is verb commands (`specify`, `plan`, `implement`…),
with role names appearing only in its Bundles packaging. OpenSpec is verbs all the way down — "Actions,
not phases." Kiro has session modes (Vibe / Spec) and execution modes (Autopilot / Supervised) rather than
personas.

FD sides with the verbs, harder: each skill is **one verb on the spine** (specify, decompose, realize,
build, verify, ship, secure) with an exclusive write-path and sole ID allocators — no characters, by
charter ([C5](charter.md)); FD's position is that personas tax correctness, a bet BMAD's docs would
dispute, so we mark it as a position, not a finding. What's checkable is the structure: every seat's
authority — what it may write, what it must ask — is enumerable
([`shared/artifact-map.md`](../shared/artifact-map.md)).

**For a domain-expert director:** you're directing seats, not befriending characters — what matters is
that each seat's authority has edges you can point to.

### 6 · Lifecycle coverage — how much of the firm

Spec Kit's core runs constitution → specify → clarify → plan → tasks → analyze → implement → converge,
with GitHub-issue handoff; security review, architecture guards, and deployment live in its 138-extension
community catalog rather than core. BMAD covers analysis → planning → solutioning → implementation with a
fast lane, plus an optional Test Architect module (nine workflows up to a release gate); security surfaces
as an enterprise-track concern and an opt-in reviewer persona, not a standing seat. OpenSpec deliberately
governs the change loop only — no UX, security, or release phases. Kiro covers spec → build → test with
hooks and CI/CD reach; security is partnership-and-hooks (a Snyk integration announced 2026-07-20), release
is pipeline-adjacent — both real, neither a first-class artifact.

FD's ten seats run discovery → planning → design → architecture → build → review → release → security,
plus refactor and status as cross-cutting activities — and the two seats where domain stakes concentrate
are load-bearing: security is a bounded read-only OWASP panel with a single synthesizer
([`07-security`](../.agents/skills/07-security/SKILL.md)), and release fails closed on unresolved
amendments, markers, or missing evidence ([`06-release`](../.agents/skills/06-release/SKILL.md)).

**For a domain-expert director:** collisions with your domain's rules don't cluster in the build phase —
they cluster at security and release. Those seats shouldn't be optional extras.

### 7 · Does the framework test its own skills

Everyone tests their *software* seriously — credit where due: Spec Kit runs a large pytest suite across a
3-OS matrix plus CodeQL, and dogfoods agentic automation on its own repository; OpenSpec runs a 3-OS Vitest
suite and even regression-tests its generated skill files for drift; BMAD's CI compiles every agent and
validates every reference on each PR. What we could not find for any of the four, as of 2026-07-21, is a
published *behavioral* eval harness — one that grades what the framework's own prompts and templates
actually produce (BMAD's changelog hints at internal eval expectations for one skill; nothing published was
found). For Kiro, no self-eval evidence was found at all; its property-based testing runs on *your* code,
not on Kiro's prompts.

FD treats its skills as the product and evals them like one: every skill ships a deterministic suite run as
`with_skill` vs. no-skill baseline A/B arms; graders are validated on real model output and required to
*bite* (a deliberately wrong output must fail them); a cross-skill integration chain covers the seams; and
a separate adversarial diagnostic track exists to *make the skills fail* and log findings. The records are
published, not claimed ([`docs/eval-methodology/`](eval-methodology/)).

**For a domain-expert director:** the seats steering your build are instructions. Evals are how anyone —
including you — knows the instructions survive contact, before your project is the test.

### 8 · Cross-harness portability — whose tool, whose rules

Spec Kit integrates with 34 named agents plus a generic escape hatch, generating each tool's files in that
tool's own convention, SHA-256-tracked for safe upgrades. OpenSpec generates skills and slash commands for
34 tools from one abstraction and calls skills "the emerging cross-tool standard". BMAD's installer targets
a wide IDE/CLI roster and repackages planning skills as web bundles for chat apps; its docs are honest that
capability varies (its unattended dev loop halts where subagents don't exist). Kiro is the different one:
it *is* the harness — IDE, CLI, web, mobile, pipelines — reaching other editors via the Agent Client
Protocol, while its FAQ prohibits use through third-party agent harnesses.

FD ships as plain `SKILL.md` trees under [`.agents/skills/`](../.agents/skills/) — the same open Agent
Skills convention Kiro imports and OpenSpec emits — deployed by one command
([`tools/vendor.py`](../tools/vendor.py)) into the project, with **three harnesses verified end-to-end**
(Claude Code, Codex CLI, Gemini CLI — [`docs/harness-support.md`](harness-support.md)). Three is a smaller
number than thirty-four; it is also a *verified* number, and the convention is the portable part. Where a
harness lacks a capability, the framework says exactly what degrades and how isolation is preserved anyway
([`shared/subagent-protocol.md`](../shared/subagent-protocol.md)).

**For a domain-expert director:** your field's rules — data residency, procurement, confidentiality — may
choose your harness for you. The discipline should survive that choice, and degrade loudly where it must.

## What each does better

Respect is credibility. If your seat is the developer's seat, several of these tools will serve you better
than FD — here is where, genuinely.

**GitHub Spec Kit** has the ecosystem FD doesn't: 34 named agent integrations under active management, 138
community extensions and 25 presets behind a checksummed catalog, a real workflow engine (human gates,
fan-out/fan-in, resumable runs, `--json` for CI), and GitHub's backing with a very high shipping tempo
(~40 releases in the seven weeks before this was written). Its engineering hygiene — 3-OS CI, CodeQL, a
changelog that even documents its own reversals — is the standard the field should copy.

**BMAD-METHOD** is the deepest agent-team experience: named specialists across the whole arc from analysis
to implementation, first-class brownfield support (it scans your existing codebase's conventions before
touching it), the field's most explicit anti-groupthink review design short of FD's isolation contract, and
a large community (~51k stars) with unusually disciplined, PR-linked release notes. If you want a full
simulated firm speaking to a developer, this is it.

**OpenSpec** is the lightest honest tool here: the delta model attacks the real failure mode of living
documentation (stale specs) by never documenting more than you're changing; its dependency graph is
user-forkable without touching source; and its machine-readable CLI contract is audited against the code
and candid about its own inconsistencies. For an engineer adding spec discipline to a mature codebase this
afternoon, OpenSpec is the shortest path.

**Kiro** is the most integrated product: one account from IDE to CLI to web to mobile, EARS requirements
wired to generated property-based tests (the strongest automated code-versus-spec loop of the four), a
genuinely layered context system (steering / skills / powers) that names and solves MCP context bloat, and
AWS-grade enterprise trust — HIPAA eligibility, GovCloud, SSO, output indemnity — that no independent
framework matches on day one.

FD's answer to all four is not "worse tools" — it's a different seat. They optimize the developer's
experience of directing agents; FD optimizes the domain expert's.

## Complementary, not competing

Two projects in this space are not alternatives to FD at all, and deserve a different kind of credit.

**[obra/superpowers](https://github.com/obra/superpowers)** (v6.1.1, 2026-07-02) is "a complete software
development methodology for your coding agents" — 14 composable process skills (brainstorming,
test-driven development, systematic debugging, subagent-driven development, writing-plans, …) shipped
across ten coding-agent platforms. It governs *how an agent works minute-to-minute*; FD governs *what a
project is and who decides*. They compose — and the credit here is concrete: **FD was itself built using
superpowers' workflows.** The brainstorming, TDD, and subagent-driven-development disciplines ran during
this framework's own construction. That is the transparency the evidence culture demands.

**[wshobson/agents](https://github.com/wshobson/agents)** ships "Production-ready agentic workflow
building blocks: 94 plugins, 203 agents, 175 skills, 109 commands" from a single Markdown source consumed
by six harnesses. It is a *capability library* — domain agents you summon for a task — where FD is a
*governance spine* — seats that answer to one spec. A director could use wshobson's specialists inside an
FD-governed build without either project noticing a conflict.

Both projects also independently converged on portable, Markdown-first skill/agent trees — the same
packaging bet FD makes with [`.agents/skills/`](../.agents/skills/) ([details](harness-support.md)).

## Sources read — as of 2026-07-21

Every framework fact above traces to these reads. If a framework has shipped past what's cited here, the
date-stamp is the context — file an issue and we'll update.

| Framework | Version / commit read | Primary pages read |
|---|---|---|
| GitHub Spec Kit | v0.13.0 (2026-07-17); `main` @ `57cc518` (2026-07-17) | README, docs site (index, integrations, workflows, agentic-sdd, spec-persistence, evolving-specs), spec-driven.md, CHANGELOG, shipped templates |
| BMAD-METHOD | v6.10.0 (2026-07-03, stable); `main` @ `8b4da79` (2026-07-19) | README, docs.bmad-method.org (full reference dump + getting-started, agents, workflow-map, core-tools, testing, party-mode, adversarial-review, upgrade guide), releases API (38 tags), CI workflow, package.json, LICENSE |
| OpenSpec | v1.6.0 (2026-07-10); `main` @ `60f720c` (2026-07-20) | README, docs (overview, concepts, commands, how-commands-work, cli, supported-tools, reviewing-changes, opsx, faq, glossary, stores guide, agent-contract), CHANGELOG, openspec.dev |
| Kiro | no public repo — dated by the site's own stamps: CLI 2.13.0 changelog (2026-07-17), newest blog post (2026-07-20), per-page "Page updated" footers (2025-11 → 2026-07) | kiro.dev home, /faq, /pricing, /about, /enterprise, /startups, /students, docs (specs, feature-specs, best-practices, correctness, steering, hooks, chat, custom-agents, skills, powers, MCP, ACP), both changelogs, GA announcement |
| obra/superpowers | v6.1.1 (2026-07-02); `d884ae0` | README, releases API |
| wshobson/agents | no releases; `c4b82b0` (2026-07-18) | README, repo page, commits API |

FD-side claims cite this repository at the linked files; the framework's eval records are under
[`docs/eval-methodology/`](eval-methodology/).
