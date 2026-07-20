# The Director's Guide — running Fullstack Director on a real project

> **Who this is for.** You — the human director. Every other document in this framework is written for the
> agents ([`AGENTS.md`](../AGENTS.md) is their operating manual) or for a specific seat (each `SKILL.md`). This
> one explains what *you* do and see: how to onboard a project, what each seat produces, what its gates will ask
> of you, and how to read the project's state. It is a **manual, not law** — intent lives in
> [`charter.md`](charter.md), mechanics in each skill; if this guide ever disagrees with either, they win and
> the guide has drifted (fix it). It lives in the framework repo; read it from here — it is not vendored into
> consumers.
>
> Commands are written Claude-style (`/00-discovery`). On Codex type `$00-discovery`; on Gemini phrase the ask
> ("start discovery") and confirm the skill it proposes. Details: [`harness-support.md`](harness-support.md).

## 1 · What you are directing

Fullstack Director keeps one **spec spine** (`docs/spec/` in *your project*) as the single source of
**declaration-truth**: your requirements (`REQ-NNN` blocks), design intent, architecture constraints, project
non-negotiables (the Constitution), and — for agent products — the agent contract and golden eval datasets.

The one test that draws every boundary (`shared/spine-boundary.md`): **would you object if this changed without
anyone asking you?** Yes → it is a *declaration*, it lives in the spine, and it changes only through the
**amendment protocol**. No → it is a *realization* (a design system, an ADR, code, tests) — the seats derive it
freely, referencing your declarations by ID and never copying their text.

Each skill is one **verb on the spine** — specify, decompose, realize (UX), realize (system), build, verify,
ship, secure — with an exclusive write-path. When a seat's expertise collides with your declarations it does not
silently comply *or* silently fix; it files an **amendment** and the tier decides who acts:

| Tier | What it is | What happens | You |
|---|---|---|---|
| **1** | a clarification with exactly one defensible answer | auto-applied, logged | see it in the log |
| **2** | changes a behavior you'd observe, a named technology, anything you'd have an opinion on | **the run pauses** with a batched gate | decide now |
| **3** | scope — adds, removes, reprioritizes a capability | deferred as `pending` | decide at `/00-discovery reflect` |

Skills escalate when uncertain — you will occasionally be asked about something trivial; that is the designed
cost of never having your intent silently rewritten. Your standing role: **you hold every consequential gate**
(charter C4). The agents execute; you decide.

## 2 · Setup — putting the framework into a project

From the framework repo, one command vendors (or refreshes) a consumer project:

```
python tools/vendor.py sync  --target <your-project-root>
python tools/vendor.py check --target <your-project-root>   # read-only drift check
```

This emits the ten seat skills (both `.agents/skills/` and the `.claude/skills/` copy), `shared/` protocols, the
`fsd-*` subagent definitions, a seed `docs/framework-feedback.md` ledger, and a provenance manifest. It
deliberately does **not** emit `AGENTS.md`/`CLAUDE.md` — in your project those are *generated views of your own
spine*, created by discovery. First session in a fresh consumer: run the smoke checklist in
[`harness-support.md`](harness-support.md) (skills listed, `/status` routes to discovery, subagent types
present). A locally-edited vendored file is skipped-and-reported on the next sync — framework fixes flow
**master-first** through the feedback loop (§7), never patched downstream.

## 3 · Starting a project — one front door, three starting materials

Everything starts at `/00-discovery`. What you bring picks the path; all paths converge on the same
challenge-then-gate machinery, and none writes the spine before you say so.

| You have | Run | What happens |
|---|---|---|
| a spec, PRD, brief — or a formed idea | `/00-discovery` | ingest → challenge → gate → write spine |
| a bare itch, pre-commitment | `/00-discovery explore` | divergence only — **never writes the spine** |
| an existing codebase, no spine | `/00-discovery adopt` | evidence-sourced reverse-engineering → gate → write spine |
| a backlog of deferred decisions | `/00-discovery reflect` | you disposition Tier-3 rows, one by one |

**New product (default).** Discovery captures the job-to-be-done, extracts candidate requirements *by domain*
(from your doc, or by interviewing you — a strong doc flows through almost silently; a thin one earns real
questions), stress-tests the undefended assumptions, and marks every requirement `stated` (traceable to you) or
`derived` (inferred — flagged for your confirmation). Then **one batched review gate**:

- **PROCEED / CLARIFY / PIVOT** — never KILL; the go/no-go belonged to EXPLORE, before commitment.
- **The Profile** — the deliverable's shape: `webapp` (default) or `agent-system` (an agent/multi-agent product;
  §6). Presented, not assumed.
- **The Data line and, if its three-part trigger fired, the embedded-agent module** (§6) — also presented, never
  silent.

Only after your answer does WRITE SPINE run. What appears in your repo: `docs/spec/**` (the spine),
`docs/README.md`, your project's `AGENTS.md` (a generated view of the Constitution — regenerated, never
hand-edit it), `scripts/verify-spine.py` (a standing integrity gate; opt-in git-hook/CI samples beside it),
`SECURITY.md`, the `CLAUDE.md`/`GEMINI.md` one-line bridges, and — for agent products — `agent-contract.md`
plus seeded eval datasets.

**Brownfield (`adopt`).** The codebase is the evidence: every candidate REQ is authored from a resolving
`code:<path:line>` source and enters as `derived` — code proves *existence*, never *intent*. Your job is the
**confirm sweep** at the gate: confirm what you actually want (flips it to `stated`), and rule on what the code
contains but nobody wants — **zombie features surface as removal candidates, never a silent keep**. Invariants
the code observes (rate limits, retention windows) arrive as *proposed* Constitution items for you to accept or
reject. Then the same WRITE SPINE as above.

**Not sure you should build at all (`explore`).** Forces ≥3 distinct problem framings before any commitment,
ends at a PICK gate, and **"don't build" is a legitimate outcome**. Its only artifact is
`docs/discovery/exploration.md` — the spine stays unwritten by hard rule.

## 4 · The build loop

After discovery, the chain per sprint — with `/status` at any moment telling you exactly where you are and what
to run next:

| Seat | You run | It produces | You decide |
|---|---|---|---|
| **01 · plan** | `/01-planner` | build-order epics · sprint slices (sprint 1 = the walking skeleton, aimed at your riskiest assumption) · the backlog ledger | **PROCEED / ADJUST** on the build shape — declarations were already gated in 00 |
| **02 · design** | `/02-designer sprint N` | tiered design system · per-screen specs · the `DM-NNN` design manifest | **Gate 1:** foundation + its batched Tier-2 amendments · **Gate 2:** screen coverage — approval **locks** the design contract |
| **03 · architect** | `/03-architect init`, then `sprint N` | `system.md` (C4 + bounded contexts) · MADR ADRs with checkable Rules · per-feature specs with Verification Contracts | the batched Tier-2 amendments — an approved tech conflict amends the constraint line **and** records the resolving ADR, both or neither |
| **04 · build** | `/04-builder sprint N` | the working slice under `src/**`, tests written RED-first, and the evidence-bearing **build-handoff** | nothing — no gate by design; it HALTs and surfaces rather than pushing through a contradiction |
| **05 · review** | `/05-reviewer sprint N` — **from a fresh session** | the QA report: verdict + severity tally + a RED test per defect + the isolation attestation | act on **SHIP / FIX REQUIRED / BLOCK** |
| **06 · release** | `/06-release sprint N` | the fail-closed gate table, then deploy config · **one** deploy plan · captured execution + health/smoke evidence · the release report | **one approval of the deploy plan** (rollback path stated up front, or the plan is invalid) |
| **07 · security** | `/07-security sprint N` (or `full`) | a blind 4-reader OWASP panel (+ a 5th for LLM/agentic surface) reduced to a severity-keyed audit | act on **PASS / REMEDIATE / BLOCK**; each finding arrives routed to its owning seat |

**The one operational rule that is yours to keep: run `/05-reviewer` from a fresh session** — not the chat that
built the code. The reviewer is seeded only with 04's handoff + the spec slice; spawned from the build
conversation it inherits the builder's reasoning and the isolation becomes fictional (charter C6/C7). The same
applies to a re-review after a fix pass: fresh again.

**The build↔review loop.** FIX REQUIRED → `/04-builder sprint N` (the fix pass drives the reviewer's RED tests
green without ever editing them) → a fresh `/05-reviewer sprint N`. A finding that survives a full fix round is
a spec or architecture problem — expect a BLOCK routed upstream, not another lap.

**The second rhythm — the patch lane.** For a small fix, skip the sprint machinery: `/01-planner patch "<what>"`
certifies it patch-class against five checks (existing REQs · spine untouched · no new dependency · bounded size
· fixes existing behavior — any doubt escalates up), records it, and dispatches `/04-builder` → fresh
`/05-reviewer` → `/06-release`. Ceremony scales down; **the fresh review and the release gate are never waived**
(charter C12).

**Cross-cutting, when needed:** `/08-refactor` (structure-only improvement under a behavior-preservation oracle,
after debt accrues across sprints) · `/07-security full` periodically · `/status` anytime.

## 5 · The gates you hold — what good decisions look like

**A Tier-2 batch (from 02, 03, or 08).** Each finding arrives as a structured row: the exact `source_quote` of
your declaration, the contradiction or gap in one sentence, and a proposed resolution. Deciding well:

- **Approve** when the expert is right — for an architecture tech-mandate, know that approval changes *two*
  things: your stated constraint line **and** a new ADR recording the decision. Both, or neither.
- **Adjust / reject** when the expert misread your intent — rejection costs nothing; the realization must then
  honor the declaration as written.
- If the "conflict" is really *new scope*, say so — it becomes a Tier-3 row for reflect, not an on-the-spot
  redesign.

**Reflect (`/00-discovery reflect`).** Deferred Tier-3 rows are presented **one at a time** for
apply / re-defer / drop. A blanket "apply them all" will not be honored — by design: each row is a scope
decision only you can make, and a hedge you recorded earlier is evidence you *hadn't* decided.

**The review verdict (05).** SHIP is only reachable on real execution evidence — no `INFERRED` behaviors, no
uncovered MUST requirement, hashes matching. Trust a SHIP; read a FIX REQUIRED's findings table (each has a
severity, a `file:line`, and a committed RED test); treat a BLOCK as "the problem is upstream of the code."

**The release gate (06).** Eleven fail-closed checks over *recorded* state — QA verdict and tally, unresolved
amendments, `[NEEDS CLARIFICATION]` markers, code identity since review, the security verdict, secrets hygiene +
`SECURITY.md`, eval floors, operations/observability, migrations (when the diff carries one — a destructive
migration needs its backup step and rollback data-implications stated), and verify-live records. A blocked
release names **every**
failed check with the exact command that clears it. When the gate is clear you make exactly **one** decision:
approving the deploy plan — commands, expected evidence, blast radius, rollback path — before anything
irreversible runs. Statuses are honest: `RELEASED` needs captured health + smoke evidence; a failed verification
rolls back and says so.

**What you never have to police.** The write-path discipline is structural: 01 never edits the spine, 04 never
edits specs or design, 05 never edits implementation, 06 never edits code, `status` never edits anything but its
two generated views. `scripts/verify-spine.py` (and `/status`) will tell you if anything is off.

## 6 · Profiles and declared lines — one spine field each, every seat adapts

Set at discovery's review gate, recorded in `specification.md`, changing later = Tier-2 minimum. The per-seat
consequences live in one table — `shared/agentic-profile.md` — which every seat reads; the short version:

- **`Profile: webapp`** (default) — the classic shape: screens, deterministic oracles, classic OWASP.
- **`Profile: agent-system`** — the deliverable IS an agent or multi-agent system. The spine gains the
  **agent contract** (autonomy tier · tool-permission matrix · HITL policy · cost envelope · memory policy, with
  ≥1 must-not REQ per high-risk tool). Sprint 1 becomes the thinnest agent loop **with tracing and the eval
  harness wired**; 02 designs the tool surface and turns instead of screens; 03 adds agentic ADR categories (a
  multi-agent topology ADR must justify its ~15× token cost); distributional requirements get **eval-suite**
  acceptance (golden datasets in the spine, floors re-run at review, graders that provably bite); the security
  panel flips agentic-primary; release adds a tracing smoke.
- **`Embedded agent:`** — a webapp with one capability that acts unattended. Fires only on all three: it
  *decides* (non-deterministic judgment), *unreviewed* (no human on the specific action), and *reaches the world*
  (money, external state, outbound comms). Everything stays webapp except that capability, which gets the
  agent-contract treatment, the agentic ADR categories, eval-suite acceptance, and injection-primary security.
- **`Data:`** — declares `retrieval(…)` · `grounded-writes(…)` · `memory` needs; routes 03's data-architecture
  craft (each module still passes a need-gate — declining with a stated reason is a correct outcome, not a gap).
- **`## Verify-live`** — techs too new to trust from training data. Each declared tech gets a cited, versioned
  verification record; architecture and build must cite it, and release blocks on a missing one. Adding a tech
  to the set is itself Tier-2.

When unsure whether your product needs `agent-system` or just an `Embedded agent:` line — say what it does
unattended and let discovery present the call at the gate; the trigger test exists so this is never decided
silently.

## 7 · Day to day

**`/status` — run it whenever you're unsure.** Read-only against truth; it integrity-checks the spine (PASS, or
FAIL naming the exact REQ), counts the release-blockers early (`pending`/`deferred` amendments +
`[NEEDS CLARIFICATION]` markers), derives the phase from files on disk, and emits **the single next command**.
It also refreshes the two generated views (`CLAUDE.md § Current State`, `AGENTS.md`). If it reports an integrity
FAIL it will route you to repair — it never "fixes" the spine itself.

**Next sprint.** `/01-planner plan-sprint N` selects the next slice from the ledger (respecting epic order),
re-freezes any requirement amended since, and the loop repeats.

**When the framework itself rubs.** In a consumer repo, a wrong gate, a misrouting `/status`, a confusing
template — anything where the *fix would land in vendored files* — is **framework friction**, not a product bug.
Say **"framework friction: …"** (or let a seat self-report its own framework-caused HALT): the `feedback` skill
appends one SHA-stamped entry to `docs/framework-feedback.md` and returns you to work within a minute. Entries
are append-only and immutable; the framework master triages every ledger before each re-vendor, and fixes come
back on the next `sync`. Product bugs stay in the project's own chain; requirement changes stay in the amendment
protocol — the skill's routing test sorts this for you.

**What to commit.** Everything the seats write is commit-intended except `_artifacts/**` (gitignored scratch —
screenshots, build-handoffs). The spine, plans, designs, architecture, reports: all in.

## 8 · Command crib

| Moment | Command |
|---|---|
| explore a bare itch (pre-commitment) | `/00-discovery explore` |
| start from a doc / an idea | `/00-discovery` |
| adopt an existing codebase | `/00-discovery adopt` |
| decide deferred scope | `/00-discovery reflect` |
| plan the build / next sprint | `/01-planner` · `/01-planner plan-sprint N` |
| certify a small fix | `/01-planner patch "<description>"` |
| design the sprint's UX | `/02-designer sprint N` |
| architect | `/03-architect init` · `/03-architect sprint N` |
| build | `/04-builder sprint N` |
| review — **fresh session** | `/05-reviewer sprint N` (pre-release: `full`) |
| ship | `/06-release sprint N` (pre-release: `full`) |
| security audit | `/07-security sprint N` · `full` |
| structural cleanup | `/08-refactor assess` · `sprint N` |
| where am I / what's next | `/status` |
| log framework friction (consumers) | `feedback` — or just say "framework friction: …" |
