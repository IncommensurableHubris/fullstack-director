# The Release Gate — protection rules over recorded state

> Load at step 1 (GATE). This is the contract `shared/spec-amendment-protocol.md` § "Release gate (skill 06)"
> instantiates: **unresolved intent must not ship silently.** The gate is a set of **named, machine-checkable
> protection rules** evaluated against **recorded state** — the industry shape of a deployment gate (required
> checks before the job referencing the environment proceeds), applied to the spine's own artifacts.

## Semantics (before the checks)

1. **Fail-closed.** A missing file, an unparseable JSON, an absent frontmatter field — every one is a **FAIL** of
   its check, never an assumption of innocence. The gate refuses what it cannot verify.
2. **Evaluate ALL checks.** Never stop at the first failure. A blocked release reports the **full table** — every
   check, PASS or FAIL, with evidence — so one `06` run gives the director the complete repair list, not the first
   item of it.
3. **Never re-derive.** The gate reads recorded machine state; it does **not** re-review code, re-run the test
   suite, re-litigate `05`'s severity calls, or re-classify amendments. `05` executed the oracles at the exact
   commit G5 pins — identity substitutes for re-execution. If the gate distrusts the recorded state, the answer is
   fail-closed + route (G2), never a fresh judgment of its own.
4. **Every FAIL is routed.** The reason names the artifact + the ID (`AMD-NNN`, the marker's file, the verdict
   token) and the exact next command. `06` is a **non-amender**: it never resolves what it blocks on.
5. **A BLOCK still writes the report.** The refusal is a release event: `docs/release/release-report-sprint-NN.md`
   with `status: BLOCKED`, the full gate table, and the routed next commands. An auditable record of *why the ship
   did not happen* is as load-bearing as one of why it did.
6. **Evidence per row.** Each gate row records what was read: the file + the field value (`verdict: SHIP`), the
   count (`pending: 0`), the SHA compared, the scan result (`0 matches`). "Checked" without the read value is not
   evidence.

## The checks

### G1 — QA verdict (the `05` handoff)

- **Read:** `docs/quality/qa-report-sprint-NN.md` frontmatter — the machine tally, never the prose sections.
- **PASS:** the file exists and `verdict: SHIP`.
- **FAIL:** report missing (fail-closed: "sprint N not verified") or verdict `FIX REQUIRED` / `BLOCK`.
- **Route:** `/04-builder sprint N` (the fix pass) then a **fresh** `/05-reviewer sprint N` — never "fix and ship";
  the loop's isolation rules hold (a fresh reviewer, no prior-verdict inheritance).

### G2 — QA tally consistency (fail-closed cross-check)

- **Read:** the same frontmatter: `findings_high` · `must_gap` · `ledger_inferred` · `spec_slice_hash`.
- **PASS:** `findings_high == 0` **and** `must_gap: false` **and** `ledger_inferred == 0` **and**
  `spec_slice_hash: match`.
- **Why:** `06` trusts `05`'s verdict **only when the tally agrees with it**. A report claiming SHIP while carrying
  high findings, a MUST-gap, unverified behaviors, or a drifted spec slice is *self-contradictory state* — the gate
  refuses contradictions rather than adjudicating them.
- **Route:** re-run `/05-reviewer sprint N` (the report is wrong, whichever way).
- Note: `findings_medium`/`findings_low` do **not** block a SHIP verdict — severity judgment is `05`'s seat; `06`
  only refuses *inconsistency*.

### G3 — Amendments (the spine's open-intent ledger)

- **Read:** `docs/spec/amendment-log.json` → every row's `disposition`.
- **PASS:** the file parses and **zero** rows have `disposition ∈ {pending, deferred}`. (Terminal dispositions —
  `auto-applied`, `approved` — pass; an empty amendments array passes; a missing or unparseable file FAILS.)
- **Route:** per row — "unresolved amendment `AMD-NNN` (tier T, from `<skill>`) — resolve at `00 reflect` (Tier 3)
  / the Tier-2 gate". List **every** open row, not the first.

### G4 — Clarification markers (unresolved spec intent)

- **Read:** scan `docs/spec/**` for the literal token `[NEEDS CLARIFICATION`.
- **PASS:** zero matches.
- **Route:** per match — "unresolved `[NEEDS CLARIFICATION]` in `<file>` (REQ-NNN's block) — resolve via
  `/00-discovery`". The marker is a promise the spec made to come back to something; shipping over it breaks the
  promise silently.

### G5 — Code identity (deploy exactly what `05` reviewed)

- **Read:** the qa-report frontmatter `final_commit` (the SHA the oracles ran at) + git state.
- **PASS:** `final_commit` present **and** resolves in this repo **and** the working tree is clean **and**
  the `src/**` tree is unchanged between `final_commit` and HEAD (docs may move after review — the report itself
  lands after the reviewed commit; the product must not).
- **FAIL:** field missing (a pre-fold or hand-rolled report — fail-closed), SHA unresolvable, dirty tree, or any
  `src/**` change since review.
- **Route:** a fresh `/05-reviewer sprint N` (the verdict no longer describes this code).
- **Why not re-run the tests instead?** Because that re-derives `05`'s seat with a weaker instrument. The suite
  passing *now* proves nothing about design fidelity, coverage honesty, or the anti-tautology properties `05`
  established; identity to the reviewed commit inherits **all** of it.

### G6 — Security audit (when one exists)

- **Read:** `docs/security/security-audit-sprint-NN.md` (or `-full.md`) frontmatter/verdict, **if present**.
- **PASS:** no audit exists (sprint mode does not require one) **or** the audit verdict is `PASS`.
- **FAIL:** an audit exists with `REMEDIATE` / `BLOCK` — a recorded security verdict cannot be shipped over.
- **Route:** the `/07-security` remediation loop.
- `full` mode: when **no** audit exists, still PASS but **record the recommendation** ("run `/07-security full`
  before a public release") in the gate row's evidence — visible, not blocking.

### G7 — Secrets hygiene (pre-flight on `06`'s own lane)

- **Check:** `.env*` (and platform-equivalent secret files) are gitignored; nothing `06` is about to write
  (deployment-config, the report, the plan, log excerpts) contains a secret-shaped **value** — env-var **names**
  only, everywhere.
- **Also (5.4a) — `SECURITY.md` present.** The vulnerability-disclosure **CVD floor** 00 emits at WRITE SPINE must be
  **present at the project root**; **absent ⇒ FAIL**, routed to `/00-discovery` to emit it (a public project with no
  disclosure policy is a release-hygiene gap — the CRA reporting trajectory's solo floor). Name it in the G7 row.
- **FAIL examples:** an un-ignored `.env`; a token value pasted into a config table; a deploy log excerpt echoing a
  credential; **no `SECURITY.md` at the root.**
- **Route:** fix the hygiene finding before any push/deploy; if a real secret was already committed, the remediation
  is **rotate first** (history scrubbing does not invalidate a credential), then clean.
- Scope note: the *full* multi-gate secret-scanning stack (pre-commit scanner, CI diff scan, history scan) is CI's
  and `07`'s territory; G7 is `06`'s bounded pre-flight over what this release touches.

### G8 — Eval floors (every profile)

- **Read:** the qa-report frontmatter `eval_floors_met` (05 stamps it — Task 3.7).
- **PASS:** `eval_floors_met: true` **or** `n/a` (a `webapp` slice with no eval-suite REQ). **`false` FAILS** — a
  missed floor or a hollow grader means the distributional behavior is unverified.
- **Route:** re-run `/05-reviewer sprint N` (re-execute the floors + the grader hack-resistance bite).
- **Why here:** the eval floor is the agent's acceptance; shipping below it is shipping an unverified system, exactly
  the intent-not-shipped-silently failure the gate exists to catch.

### G9 — Observability & Operations

Two clauses — one every profile, one agent-only.

- **Operations completeness (every profile).** Read `docs/release/deployment-config.md` → its `## Operations` section.
  - **PASS:** the section exists and declares the **ONE SLO** on the critical user journey (Google SRE small-team
    floor) — alongside where logs live · one alert (a burn-rate note) · a rollback-drill cadence · the
    **drift/sampling line** (its single home). **Fail-closed** on a missing section or a missing SLO.
  - **Route:** complete `## Operations` in `deployment-config.md` at SETUP (`references/deploy-verification.md`).
- **Observability span-smoke (`Profile: agent-system` only; skipped for `webapp`).** Read the release report's
  VERIFY evidence.
  - **PASS:** the **OTel span smoke** is captured — one traced run shows the `invoke_agent → chat → execute_tool`
    span tree emitting **before traffic** — and VERIFY **references** the `## Operations` drift/sampling line (its
    single home — no duplicate note).
  - **Route:** add the observability plan via `/03-architect` (the `observability`-category ADR) and re-verify.
- **Model-facing changes:** a model/provider swap in the diff → the plan references `shared/model-migration-protocol.md`
  or records an explicit waiver (`references/deploy-verification.md` § model-facing changes) — a swap is never a
  like-for-like config change.

### G10 — Migrations (conditional; the G6 "if present" pattern)

- **Read:** the deploy plan + the release diff for a **schema/data migration**. **Evaluates only when a migration is
  present**; otherwise **N/A**, recorded (never silently skipped). *(A model/provider swap is G9's concern, not a
  migration — G10 does not fire on the `model-migration-protocol` reference.)*
- **PASS (when it applies):** the plan **identifies** the pending migration(s); a **destructive** migration (a drop /
  rename / alter-type / truncate) carries a **backup step** *before* it runs; and the **rollback path states its data
  implications** (does rollback need a data action? is it forward-only? is data loss possible?). **Fail-closed** when
  it applies — a destructive migration with no backup, or a rollback with unstated data implications, FAILS.
- **Route:** complete the plan — add the pre-migration backup step and state the rollback's data implications
  (`references/deploy-verification.md`); the migration contract itself is 03's feature-spec **Migration** row.

### G11 — Live-source verification (conditional; the G6 "if present" pattern)

- **Read:** `docs/spec/architecture-constraints.md` for a `## Verify-live` block. **Evaluates only when one is
  declared**; otherwise **N/A**, recorded. The confabulation guardrail's ship gate (`shared/live-source-verification.md`).
- **PASS (when it applies):** run the **emitted** `python scripts/verify-spine.py --json` and read **L7** — it must
  be `ok` (every declared verify-live tech has a resolving, cited `docs/verification/<tech>.md`; no orphan record; no
  uncited claim). **Plus the currency clause:** each record's `verified_against` version matches the project's
  version of the tech **where mechanically determinable** (the dependency manifest — e.g. `package.json` — or a
  Stack-mandates version pin); where the project pins no version the clause is **N/A**, recorded. **06 does not
  re-parse the records** — L7 is the single implementation, `06` and `status` are its two readers (no drift surface).
- **Fail-closed when it applies:** L7 not `ok`, or a determinable version mismatch (a **stale** record), FAILS.
- **Route:** re-verify — `/00-discovery` re-seeds a missing/uncited record; `/03-architect` re-verifies on a
  tech-mandate. A stale record: re-fetch live docs/source and update `verified_against` + the cited claims.

## `full` mode (the pre-release gate)

`06-release full` gates the **whole shipped surface**, then ships the current state:

- **G1/G2 sweep:** every sprint the backlog marks shipped/built must have its qa-report at `verdict: SHIP` with a
  consistent tally — or one `qa-report-full.md` from an `05-reviewer full` pass covers the set. Any sprint missing
  its report FAILS (fail-closed), named per sprint.
- **G3/G4:** unchanged (they are already global).
- **G5:** against the most recent qa-report's `final_commit`.
- **G6:** as above, with the run-`/07-security full` recommendation recorded when absent.
- The report filename is `release-report-full.md`; `release_mode: full` in the frontmatter.

## Patch releases (the expedite lane reaches the same gate)

A certified patch (`docs/planning/patches/patch-NNN.md`) ships through **the identical seven-check table — nothing
waived, nothing added**: G1/G2/G5 read `docs/quality/qa-report-patch-NNN.md` (the patch review's tally +
`final_commit`); G3/G4 are global as ever (note the S1 additive-regression-case row is Tier-1 `auto-applied` —
terminal, so it passes G3); G6 accepts a `security-audit-patch-NNN.md` when one exists; G7 unchanged. Every routed
reason names "patch NNN" where it would say "sprint N". The report filename is `release-report-patch-NNN.md`
(`release_mode: patch`, `patch: patch-NNN` in the frontmatter); the tag is `release/patch-NNN`. **A verdict-only or
"it's just a patch" shortcut is exactly the misclassification the lane's asymmetry forbids** — the gate is the half
of the doctrine that never scales down.

## What the gate is not

- **Not a re-review.** G1/G2 read `05`'s tally; the prose findings are `05`'s evidence, not `06`'s input.
- **Not an amendment channel.** G3/G4 failures route to `00` / the Tier-2 gate; `06` appends no row
  (`shared/spec-amendment-protocol.md`).
- **Not a test runner.** G5's identity pin replaces re-execution (above).
- **Not skippable in parts.** "The director said ship it anyway" does not remove a row from the table — a human can
  read the BLOCKED report and act outside the framework, but `06` never emits `RELEASED` past a failing gate.
