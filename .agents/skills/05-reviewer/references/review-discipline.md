# Review discipline — verifying a change you did not write

> Loaded by skill 05 (reviewer) during the review (steps SEED → PASS 2 of the flow). The **method + the why**;
> `SKILL.md` is the spine, `references/verification-evidence.md` is the evidence machinery (the EXECUTED/OBSERVED/
> INFERRED ladder, the Capability Probe, the fallback cascade, browser verification, the honesty gate), and
> `templates/qa-report.md` is the shape of the output. 05 reads **only** the build-handoff + the spec-slice paths
> (`shared/subagent-protocol.md`) — **never** the build conversation — and writes **only** the QA report + attestation
> (+ verification tests). It **never edits implementation**: a real defect loops back to `04` (below). 05's graded
> value is **not** "reviews code" — a strong reviewer does that too — it is the **isolated, honest, false-positive-
> controlled verdict** that can gate a ship: provably not self-preferring, provably evidence-backed.

## Why isolation is the whole game

A reviewer earns the right to gate a ship by **not having written the code**. The value of a second look is *fresh
judgment*; inheriting "I tried X, it felt wrong, so I did Y" re-derives the builder's conclusions instead of testing
them, and re-acquires the anchoring bias the review exists to escape. So the seed is engineered for a stranger: the
handoff (`_artifacts/exports/build-handoff-sprint-NN.md`) + the spec-slice paths, and **nothing else**. Isolation is
real **only because the spawner is fresh** (`shared/subagent-protocol.md`) — a reviewer spawned from the build session
inherits the builder's reasoning whether or not a subagent tool exists. Self-preference is *heterogeneous* (measured
reviewer bias runs both directions); the robust lever is not assuming a bias direction but **anonymizing authorship**,
which a fresh context delivers for free.

**The corollary: re-derive everything, trust nothing the builder asserted.** The handoff provides *evidence* (a
command that exits 0, a `file:line`); the isolated reviewer renders the *verdict*. A row is trustworthy because its
oracle re-runs green under your hand — not because the builder wrote "EXECUTED".

## Read-only — the authority comes from not writing the code

05 writes **only**: the QA report (`docs/quality/qa-report-sprint-NN.md`), the context attestation (inside it), and —
as **verification assets** — new tests / browser checks that escalate an INFERRED behavior to EXECUTED/OBSERVED via
05's *own* runtime (`references/verification-evidence.md`). It **never edits implementation code**, and it never edits
the spine or the realization docs. This is a notable, deliberate design choice (unlike a QA skill that
fixed and simplified): a reviewer that fixes re-enters the writer role, re-acquires anchoring bias on its own patch,
and **launders its own false positives into the code**. A real defect — impl wrong, hollow test, uncovered REQ — is a
**FIX REQUIRED finding routed to `04`**, not a reviewer edit. Style and structure hardening is `08`'s seat, not a
finding here; a deep security audit is `07`'s.

| 05 writes | 05 never writes |
|---|---|
| `docs/quality/qa-report-sprint-NN.md` (verdict + ledger + tally + attestation) | any `src/**` **implementation** file |
| `src/**` **tests only** (verification assets: RED tests, escalation tests) | `docs/spec/**` (the spine) |
| `_artifacts/screenshots/qa-sprint-NN/` (browser evidence) | `docs/architecture/**`, `docs/design/**` (realizations) |
| appends `.claude/rules/quality-guardrails.md` | `docs/spec/amendment-log.json` (05 escalates, appends **no** row) |

## SEED — the isolation gate (step 1)

Read the handoff + the spec-slice **only**. Then two mechanical tamper checks, before any judgment:

1. **`baseline_commit` resolves** — `git cat-file -t <baseline_commit>` is a commit, and it is an ancestor of
   `final_commit`. The diff you review is exactly `git diff baseline_commit..final_commit`; you never reconstruct it
   from memory or narrative.
2. **`spec_slice_hash` matches** — recompute the hash over the graded spec slice and compare it to the handoff's. A
   mismatch means **the spec slice drifted between build and review** — you would be grading against a different
   contract than `04` built against — so the verdict is **BLOCK** ("spec slice drift; re-slice or re-build"), not a
   silent pass. This is the one gap the prior art left open (Tessl's tamper-evidence, applied to the spec).

**The `spec_slice_hash` contract (identical to `04`'s emit side — `04/references/build-handoff.md`).** Both skills
compute it the same way, or the check is meaningless:

- **Inputs, in order:** the sprint-slice file the handoff names in `spec_slice_path`
  (`docs/planning/sprints/sprint-NN.md` — it carries the frozen outcome-Gherkin + "Done When"), then, **if a design
  contract exists**, the manifest (`docs/design/approved/sprint-NN/manifest.md`).
- **Normalize** each file's bytes to LF line endings (`\r\n`→`\n`, `\r`→`\n`) — nothing else; the files are frozen and
  read-only, so no other normalization is needed.
- **Concatenate** sprint-slice `+ "\n" +` manifest (omit the manifest half when there is none).
- **Hash:** `spec_slice_hash = "sha256:" + SHA256(payload_utf8).hexdigest()[:16]`.
- **One-liner** (either runtime reproduces it):
  `python -c "import hashlib,sys; d=[open(p,'rb').read().decode('utf-8').replace('\r\n','\n').replace('\r','\n') for p in sys.argv[1:]]; print('sha256:'+hashlib.sha256(('\n'.join(d)).encode()).hexdigest()[:16])" docs/planning/sprints/sprint-NN.md docs/design/approved/sprint-NN/manifest.md`

Record the seed manifest (which files you opened) for the attestation.

**Patch variant (`review_mode: patch` — the WS1 expedite lane).** The lane changes the seed's *contents*, never its
*discipline*: inputs = the patch-keyed handoff (`build-handoff-patch-NNN.md`) + the **patch record**
(`docs/planning/patches/patch-NNN.md`, named in `spec_slice_path`) + the **owning REQ blocks** the record's `reqs:`
list names. The `spec_slice_hash` payload is the **record alone** (no manifest half — 02 is skipped by construction
on a patch). Scope is bounded to the patch's behaviors: a defect outside the owning REQs is a **routed note**, not
review scope-creep. The report lands patch-keyed (`docs/quality/qa-report-patch-NNN.md`). Every honesty gate —
INFERRED ⇒ not SHIP · MUST-gap ⇒ not SHIP · hash mismatch ⇒ BLOCK — holds **unchanged**: ceremony scales down by
change class; independent verification never does.

## The two passes — cheap structural gate before expensive judgment

Re-establish evidence deterministically (Pass 1) **before** rendering judgment (Pass 2). Structural facts are cheap
and catch the crude failures; semantic judgment is expensive and is where the reviewer's value concentrates — running
it first on a build that fails the arithmetic wastes it.

### Pass 1 — deterministic, inline

Runs in *this* context (no subagent needed — it is mechanical). Full mechanics in
`references/verification-evidence.md`; the checks:

- **Capability Probe** — attempt every runtime (unit runner, integration, dev server, browser); capture the exact
  command + exit code + output. No row may read "NOT_ATTEMPTED" in the report.
- **Re-run the handoff's oracles** — every row *claimed* EXECUTED must actually be green at `final_commit` (catches
  "claimed passing, actually red"). Recompute each **oracle hash** and confirm it matches the handoff's (the builder
  did not quietly rewrite the test after claiming it).
- **File List ↔ diff** — the declared File List must equal `git diff --name-status baseline..final` (an undeclared
  write *or* a hallucinated claim both fail here), and the diff must touch **no** `docs/spec | docs/architecture |
  docs/design` file.
- **Coverage arithmetic** — every in-scope REQ → its claimed test; every manifest DM-ID → its claimed `file:line`. A
  REQ claimed FULL whose cited test does not exist (or does not assert the behavior) is a **dishonest coverage claim**,
  a finding in its own right.
- **Anti-tautology litmus** — for a changed behavior's test, mutate or comment the line it guards and re-run: a suite
  that stays green is **hollow**, and its "EXECUTED" is worthless. This is the mechanized honest replacement for a
  green bar (coverage is necessary, never sufficient).

### Pass 2 — semantic judgment, fresh-context reviewer subagent

The judgment pass runs in a **spawned fresh-context reviewer subagent** (the `03` dual-pass pattern,
`shared/subagent-protocol.md`), seeded with only the realization + the spec-slice declarations, returning findings +
verdict + the context attestation. It judges three tracks against the outcome-Gherkin + the design contract:

- **Acceptance conformance** (the Acceptance-Auditor track) — each in-scope REQ's outcome-Gherkin is met, evidenced by
  a cited `file:line` and a re-run oracle, not by naming.
- **Correctness that affects requirements** — logic errors, off-by-ones, unhandled boundaries **that break a REQ**.
  This is *not* a style sweep: readability, SOLID, naming, and simplification are `08`'s seat, never a finding here.
- **Design fidelity — deterministic** — every manifest DM-ID **PRESENT and not DRIFTED** vs the approved mockup
  (manifest coverage + a visual diff, a *defined rule*; `references/verification-evidence.md` §design-fidelity). A
  design criterion that "two agents could disagree about" is a **spec defect the reviewer flags**, never an LLM-judge
  score.

## The judgment discipline (the four false-positive levers)

False positives are the #1 failure of AI review — a reviewer that cries wolf gets ignored, and real-world acceptance
of LLM review comments has been measured in the single digits. A missed defect and an invented one are *equally*
disqualifying; the eval is F1-framed for exactly this. Four levers keep the verdict honest:

1. **Re-derive severity centrally.** Rate each finding `low / medium / high` by its **consequence for the artifact's
   consumer** — never inherit a severity the builder or a sub-reviewer asserted. Structural asymmetry: a blind reader
   lacks the context to set final severity; the central reviewer holds it.
2. **Reachability — read beyond the diff hunk before rating.** A line that looks wrong in isolation may be unreachable,
   guarded upstream, or dead. Rate the behavior in context, not the hunk.
3. **The verification-bar — a behavior claim needs a `file:line`, not an inference from naming.** "Looks like it
   handles the empty case" is not a finding; "returns `undefined` at `digest.js:22` when `entries` is empty, violating
   REQ-008" is. Vague rationale ("based on standard patterns", "similar to other code") **is not evidence** and forces
   the claim down. Applies to both directions: a *passing* claim needs the same pointer a *failing* one does.
4. **Self-verify each finding before emitting, and impose no quota.** Before a finding enters the report, confirm it
   against the *actual* behavior (re-run, re-read). A clean review is a **first-class honest outcome** — never
   manufacture findings to look thorough (the finding-quota bug). But never announce "clean" if a verification layer
   silently failed: a probe that could not run is an INFERRED behavior, not a pass.

## Honest escalation — the three-way+ verdict (05 is a non-amender)

A failing behavior is one of four things; classify it and route it — 05 writes neither the spine nor the specs and
appends **no** `amendment-log.json` row (appending stays with `00/02/03/08`, `shared/spec-amendment-protocol.md`):

| The wrong thing | What it means | Route (05 escalates, never edits) |
|---|---|---|
| **the code** | the implementation is buggy | **FIX REQUIRED → `04`** (with a reproducing RED test if testable) |
| **the test** | the test is hollow / encodes the wrong expectation | **FIX REQUIRED → `04`** |
| **the realization spec** | `03`'s feature spec / VC is wrong | **flag to `03`** — a finding routed to the architect; do not edit the spec |
| **the declaration** | a *spine* fact (a REQ, a constraint) is wrong | **surface a pending amendment for `00`/the release gate** — do not touch the spine |

This is Kiro's fix-code / fix-spec / fix-test triad, routed through our amendment protocol. `06-release` **blocks** on
any surfaced-but-unresolved declaration issue (a `pending`/`deferred` amendment) — so surfacing it is not a soft note,
it is a hard gate downstream.

## The build↔review loop — how FIX REQUIRED closes (generator↔evaluator)

The read-only verdict is half a system; the loop that turns FIX REQUIRED into a shipped slice is the other half. `04`
and `05` implement it together (`04` gained its **fix-pass** loop-half in the same session that built `05`). Five
invariants:

1. **The maker fixes; a *fresh* evaluator re-reviews.** 05 never fixes (isolation); the fix is `04`'s verb. The
   director re-invokes `04-builder sprint N`, which — seeing a FIX REQUIRED report for the sprint — runs a fix pass.
2. **The re-review does NOT inherit the prior verdict.** Each round spawns a **fresh** 05 that re-derives from the
   *new* handoff + the spec — it **does not read the previous QA report**. Reading it would anchor the new reviewer on
   stale findings and re-introduce the bias a fresh spawner exists to escape. A fixed behavior simply verifies
   EXECUTED; an unfixed one is caught again on its own terms.
3. **Findings are an executable, routed interface**, not prose: severity (re-derived) · the REQ/VC it violates · a
   `file:line` · the three-way routing. `06-release` gates on the machine-readable tally without re-reading prose.
4. **A human / `06` gate closes the loop; the agent never auto-drives it.** 05's report *recommends* the next command;
   the director runs it. Unbounded generator↔evaluator loops are a known agentic failure mode.
5. **A convergence guard.** A finding that **survives a fix round** is evidence it is a *spec/architecture* problem,
   not a code bug → escalate to **BLOCK → `03`/`00`/human** after a bounded number of rounds (~2).

### The findings interface — hybrid (the anti-circular-verification lever)

- **Testable defect → 05 writes the reproducing RED test.** A verification asset (a test, inside the read-only scope —
  not implementation), committed as a failing `*.test.js`; 05 runs it and confirms it is **RED** (it reproduces the
  defect against the current impl). `04` must make it green **and may not edit it** — so the fixer **cannot game an
  oracle it did not author** (defeats "circular verification", where the fixer rewrites the test to match buggy code).
  TDD-for-bugs is thus *split across the isolation boundary*: **05 owns RED, `04` owns GREEN.**
- **Non-testable finding** (browser / design-drift / edge / missing copy) **→ prose + `file:line` + evidence**
  (a screenshot, a transcript). `04` does full TDD-for-bugs (writes the reproducing test *and* the fix).

## The honesty gate (hard) — SHIP is earned, not asserted

The verdict cannot be **SHIP** while **any** in-scope behavior is still INFERRED, or **any MUST/P0 REQ is uncovered**
(risk-priority-keyed, not a flat coverage %). SHIP means real execution evidence for every in-scope behavior. The
session summary **leads with the Verification Ledger counts + the verdict**; if `Inferred > 0` (or a MUST-gap exists)
and the line says "SHIP", it is internally inconsistent — rewrite before emitting. Full mechanics:
`references/verification-evidence.md`.
