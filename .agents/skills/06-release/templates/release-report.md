<!-- Filename: docs/release/release-report-sprint-NN.md  (release-report-full.md for release_mode: full;
     release-report-patch-NNN.md for a patch release — which also swaps `sprint:` for `patch: patch-NNN`).
     Written on EVERY 06-release run — including a BLOCKED one (the refusal is an auditable release event). -->

---
status:            RELEASED    # RELEASED | ROLLED-BACK | FAILED | BLOCKED
sprint:            NN          # patch releases: replace with  patch: patch-NNN
release_mode:      sprint      # sprint | full | patch
gate:              pass        # pass | fail  (fail ⇒ status MUST be BLOCKED)
gate_qa_verdict:   SHIP        # what G1 read: SHIP | FIX REQUIRED | BLOCK | missing
gate_amendments_pending: 0     # G3: count of pending + deferred rows
gate_markers:      0           # G4: surviving [NEEDS CLARIFICATION] count
gate_code_identity: match      # G5: match | drift | unverifiable
gate_security:     absent      # G6: pass | fail | absent
deployed_commit:   <SHA|none>  # none unless EXECUTE ran
health:            pass        # pass | fail | n/a  (n/a only when BLOCKED/FAILED before deploy)
smoke_passed:      0
smoke_failed:      0
rollback_exercised: false      # true ⇒ status ROLLED-BACK (or FAILED if the rollback itself failed)
spine_hash:        <sha256|none>  # D7: scripts/verify-spine.py --hash over docs/spec/** (none only when BLOCKED pre-hash)
amendments_at_release: 0       # D5: amendment-log row count at release (the ledger depth that shipped)
---

# Release Report — Sprint NN

> **The auditable record a human, `/status`, and `00 reflect` act on.** Owned by **skill 06 (release)**. The
> frontmatter is the machine-readable state; the sections are the evidence. GATE HONESTY: `status: RELEASED`
> requires every gate row PASS **and** captured evidence in (d)/(e) — if they disagree, the report is wrong; fix it
> before emitting. Craft: `references/release-gate.md` + `references/deploy-verification.md`.

## (a) Status

**RELEASED | ROLLED-BACK | FAILED | BLOCKED** — _<one line: the single most decision-relevant fact. e.g. "BLOCKED —
AMD-003 is still pending and REQ-008 carries a [NEEDS CLARIFICATION] marker; nothing was deployed." or "RELEASED —
sprint 01 live at <url>, health + 3/3 smoke green, tagged release/sprint-01.">_

## (b) Gate table (all checks, evaluated in full — evidence per row)

| # | Check | Result | Evidence (what was read) | On FAIL — routed next command |
|---|-------|--------|--------------------------|-------------------------------|
| G1 | QA verdict | _<PASS>_ | _<qa-report-sprint-NN.md: `verdict: SHIP`>_ | _<—>_ |
| G2 | QA tally consistency | _<PASS>_ | _<high 0 · must_gap false · inferred 0 · hash match>_ | _<—>_ |
| G3 | Amendments | _<PASS>_ | _<amendment-log.json: 0 pending / 0 deferred (N rows terminal)>_ | _<—>_ |
| G4 | Clarification markers | _<PASS>_ | _<docs/spec/** scan: 0 matches>_ | _<—>_ |
| G5 | Code identity | _<PASS>_ | _<final_commit <SHA> resolves · tree clean · src/** unchanged since>_ | _<—>_ |
| G6 | Security audit | _<PASS (absent)>_ | _<no security-audit-sprint-NN.md — not required in sprint mode>_ | _<—>_ |
| G7 | Secrets hygiene + SECURITY.md | _<PASS>_ | _<.env gitignored · names-only verified in every write · `SECURITY.md` present at the project root>_ | _<—>_ |
| G8 | Eval floors | _<PASS>_ | _<qa-report `eval_floors_met: true` (or `n/a` — no eval-suite REQ)>_ | _<—>_ |
| G9 | Observability & Operations | _<PASS>_ | _<every profile: `## Operations` SLO present; agent-system also: OTel span smoke captured before traffic, referencing the Operations drift line>_ | _<—>_ |
| G10 | Migrations _(if present)_ | _<PASS / N-A>_ | _<no migration → N/A; else: pending migration identified · destructive ⇒ backup step · rollback data implications stated>_ | _<—>_ |

<!-- BLOCKED: keep ALL rows (the full repair list), mark each FAIL with its routed command, and stop after (b) +
     (f-notes if useful) + (h). No plan/deploy sections are fabricated for a run that never deployed. -->

## (c) Deploy plan (as approved — the action preview the human said yes to)

> Approval: _<granted by the director on <context> — one approval for the whole plan>_. Blast radius: _<what this
> deploy can affect; irreversible steps named>_. **Rollback path:** _<the concrete restore procedure — stated
> before approval>_.

| Step | Command | Expected evidence |
|------|---------|-------------------|
| 1 | _<exact command>_ | _<what PASS looks like>_ |

## (d) Deploy log (captured, step by step)

| Step | Command | Exit | Output excerpt (secrets scrubbed) |
|------|---------|------|-----------------------------------|
| 1 | _<as run>_ | _<0>_ | _<the real output's relevant line(s)>_ |

## (e) Verification (health before traffic → switch → smoke on live)

| Probe | Command / endpoint | Expected | Actual (captured) | Result |
|-------|--------------------|----------|-------------------|--------|
| Liveness (pre-traffic) | _<…>_ | _<200 ok / exit 0>_ | _<…>_ | _<PASS>_ |
| Readiness | _<…>_ | _<deps ok>_ | _<…>_ | _<PASS>_ |
| Smoke 1 — _<flow>_ | _<…>_ | _<…>_ | _<…>_ | _<PASS>_ |

<!-- Any FAIL here ⇒ the rollback path was executed and re-verified; status ROLLED-BACK; the failing row keeps its
     captured actual. RELEASED with an empty (d)/(e) is a contradiction — the honesty gate forbids it. -->

## (f) Release notes (REQ-keyed — what shipped, in the spine's vocabulary)

| REQ | Outcome shipped |
|-----|-----------------|
| _<REQ-001>_ | _<the outcome line from the slice's frozen acceptance — e.g. "a member's day holds exactly one standup (latest answers)">_ |

**Tag:** _<`release/sprint-NN` at `deployed_commit` — or none (BLOCKED/FAILED)>_

## (i) Provenance (what shipped, pinned)

> The release's content identity — so "which spec + which build shipped in release N" is a lookup and
> spec-diff-between-releases becomes possible. `spine_hash` is `scripts/verify-spine.py --hash` over `docs/spec/**`
> (D7); `amendments_at_release` is the ledger depth (D5). Toolchain line intentionally omitted (restore trigger:
> an SLSA-attestation consumer).

| Field | Value |
|-------|-------|
| Artifact digest | _<sha256 of the built/deployed artifact — image digest / bundle hash>_ |
| Built-from commit | _<the `deployed_commit` SHA>_ |
| `spine_hash` | _<64-hex — `python scripts/verify-spine.py --hash`>_ |
| `amendments_at_release` | _<the amendment-log row count at release>_ |

<!-- agent-system (reserved, one line): ML-BOM components — models · datasets · agent frameworks as CycloneDX
     components. Deferred until an SBOM/attestation consumer needs it (do not build bespoke AI-BOM machinery). -->

## (g) Guardrails learned

_<none — clean run>_ · or per failure/near-miss: **Trigger:** _<what happened, cited from (d)/(e)>_ →
**Rule appended** to `.claude/rules/deployment-guardrails.md`: _<the concrete pre-deploy check>_

## (h) Next command (06 recommends; the director runs it)

- **RELEASED** → `/07-security sprint NN` _(recommended after a first production deploy)_ · next sprint ·
  `/00-discovery reflect`.
- **BLOCKED** → the failed rows' routed commands, in the table above.
- **ROLLED-BACK / FAILED** → fix the root cause via the owning skill, then re-run `/06-release sprint NN`.

## Session summary (paste as the conversational reply — lead with status + gate, never narrative)

```
RELEASE — SPRINT NN — <RELEASED | ROLLED-BACK | FAILED | BLOCKED>
Gate: <pass | fail — G# list of failures>   QA: <verdict> · amendments pending: N · markers: N · identity: <match>
Deploy: <deployed_commit | none>   Health: <pass|fail|n/a>   Smoke: <X/Y>   Rollback exercised: <no|yes>
<if BLOCKED: one line per failed check with its routed command>
Report: docs/release/release-report-sprint-NN.md   Next: <the (h) command>
```
