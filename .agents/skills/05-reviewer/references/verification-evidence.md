# Verification evidence — the honesty layer

> Loaded by skill 05 (reviewer) for PASS 1 and the FALLBACK CASCADE. The **evidence machinery** behind the verdict:
> the EXECUTED/OBSERVED/INFERRED ladder, the Capability Probe, the fallback cascade, browser verification, the
> anti-tautology litmus, design-fidelity determinism, and the honesty gate. `references/review-discipline.md` is the
> judgment method; this file is *how a behavior earns a state*. This is the moat over checkbox-belief review (Spec Kit
> can't run a test; a self-verifying builder grades its own homework): **only execution or observation confirms a
> behavioral contract — reading code is inference, never evidence.**

## The three verification states — 05's exact vocabulary

Every "Done When" item and every VC row is in exactly one state. The states are the same three `04` stamped in the
handoff (05 consumes them 1:1), re-established here under 05's own hand — the handoff *claims* a state; 05 *confirms*
it.

| State | Definition | Admissible evidence |
|---|---|---|
| **EXECUTED** | a test ran, went green, and is known to exercise the behavior (cleared the anti-tautology litmus) | `test_file:line → PASS` + the reproduction command's output excerpt |
| **OBSERVED** | you drove the real system (dev server, browser, CLI, API) and *watched* the behavior happen | a screenshot path, a curl/console transcript, or a Playwright return payload |
| **INFERRED** | source was read and argued to satisfy the behavior; **no execution occurred** | `file:line` pointers — and **INFERRED always counts as NOT verified** |

**The scoring rule that makes it bite:** any in-scope behavior in state **INFERRED** counts as a FAIL for functional
completeness, and **the verdict cannot be SHIP while any in-scope behavior is INFERRED.** INFERRED is admissible as an
honest *intermediate* — it is exactly where the fallback cascade starts — but never as a ship-sufficient endpoint.

**Verify-live usage (WS6).** A behavior exercising a spine-declared **verify-live** tech
(`architecture-constraints.md` § Verify-live) is verified only if the handoff row carries a **`verified:
docs/verification/<tech>.md`** ref to a *current* record. Usage **not** backed by a current record — an uncited
verify-live API call, or a row left `INFERRED` — is treated **exactly like an INFERRED behavior: SHIP is
unreachable.** This is the confabulation guard at the review boundary; you flag it from the **seed as-is** (the
handoff + the record set), while declared-set *completeness* is `verify-spine.py` L7 / `06` G11's job, not the
reviewer's widened scope. `shared/live-source-verification.md`.

## Capability Probe — attempt every runtime, capture the evidence

Before you may claim a runtime capability is unavailable, you must **attempt it and capture the evidence** (mirrors
`superpowers:verification-before-completion` — evidence before assertions, always). Fill the Capability Probe table in
the report: for each runtime, the exact command, its exit code, an output excerpt.

| Capability | Command attempted | Exit code | Output excerpt |
|---|---|---|---|
| Unit runner | e.g. `node --test test/digest.test.js` | 0 / non-zero | … |
| Integration suite | … | … | … |
| Dev server start | … | … | … |
| Browser (Playwright MCP) | e.g. `browser_navigate http://localhost:PORT` | … | … |

**The rule: no row may read "NOT_ATTEMPTED" in the final report.** If a capability truly will not run, the row holds
the actual failing command and its output — a *cited* fact, not an excuse. If you have not tried it yet, try it now.
A silently-skipped probe is a hidden INFERRED masquerading as a pass.

## The anti-tautology litmus — the mechanized honesty check

A green bar proves nothing if the test cannot go red. For each changed behavior whose test the handoff marks EXECUTED:
**mutate or comment the line the behavior lives on and re-run.** A suite that stays green is **hollow** — its
"EXECUTED" is worthless and the behavior is really INFERRED. Reject and flag:

- **assertion-free** tests (exercise the code, assert nothing),
- **assert-the-mock** tests (verify the test's own setup, not the code),
- **tautological** assertions (`expect(true).toBe(true)`, or an expected value computed the same way the code computes
  it — both wrong together).

On core domain logic this is a **single-point mutation** (flip a comparison / boolean, return a constant) — the honest
replacement for a coverage %, which routinely masks logically hollow tests. A hollow test is a **FIX REQUIRED finding
routed to `04`** (05 does not rewrite it — that would be editing under review); where the defect is *testable*, 05
attaches its own **reproducing RED test** as the executable finding (`references/review-discipline.md` §findings
interface).

## The fallback cascade — escalate INFERRED via 05's OWN runtime (verify, never fix)

The reviewer *uniquely* holds runtime capability the headless builder lacked (a browser, a dev server). For every
behavior still INFERRED after Pass 1, climb this ladder — prefer the highest tier the behavior can reach (durable
tests over ephemeral checks), drop down only when a tier cannot cover it. Each rung is a **verification asset** (a
test 05 writes, a check 05 runs) — **never** an implementation edit; 05 did not write the code, so running its own
oracle against it is isolation-safe.

- **Tier 1 — a test via the CLI → EXECUTED** *(most durable)*. Write/fix a `node:test` / unit / Playwright-CLI test and
  run it in the shell. Evidence: the test path + stdout excerpt. Preferred whenever the behavior is a repeatable
  assertion — it becomes a regression asset.
- **Tier 2 — Playwright MCP exploration → OBSERVED** *(ephemeral)*. Drive the running app step-by-step via
  `mcp__plugin_playwright_playwright__*`. Evidence: screenshots + the tool-call transcript. Use only when a full Tier-1
  test is genuinely overkill; carry a **"promote to EXECUTED before next sprint"** note — an MCP check is not a
  regression asset on its own.
- **Tier 3 — Claude in Chrome → OBSERVED** *(narrow specialist)*. Real logged-in Chrome via `mcp__claude-in-chrome__*`
  — only when the behavior needs real user state (OAuth/SSO, a deployed instance). Not for sensitive-data pages; do not
  trigger JS dialogs (they break the extension).
- **Tier 4 — CLI dogfooding → OBSERVED** *(non-UI)*. `curl`, a direct API call, a REPL function call. Capture request
  and response verbatim.

If **all applicable tiers fail** for a behavior — with the attempts captured in the Capability Probe — the behavior
**stays INFERRED**, and the verdict is **BLOCK** ("cannot execute runtime verification for X, Y, Z"). Silent skipping
is never permitted: the Verification Ledger is the single source of truth and the session summary reports its counts
verbatim.

## Browser verification (when a UI slice exists)

> Skip when there is no frontend — check `system.md` for a web container; mark the UI tracks N/A. A headless slice
> (the `node:test` digest core) has no browser row to run — say so in the probe, don't invent one.

Pick the right tool per scenario (they are **not** interchangeable):

| Tool | Invoked via | Result state | When |
|---|---|---|---|
| **Playwright CLI** | `npx playwright test …` (Bash) | EXECUTED | default for any UI behavior expressible as a repeatable assertion — durable, CI-ready |
| **Playwright MCP** | `mcp__plugin_playwright_playwright__*` | OBSERVED | one-off visual checks where a full test is overkill; flag "promote to EXECUTED" |
| **Claude in Chrome** | `mcp__claude-in-chrome__*` | OBSERVED | only when real user state is required |

**Procedure:** start the app from the handoff's start command; for each browser VC step, navigate → screenshot →
act → screenshot → compare to expected → record PASS/FAIL with screenshot paths; spot-check three viewports (desktop
1280×800 · tablet 768×1024 · mobile 375×812) for layout breaks. Save to `_artifacts/screenshots/qa-sprint-NN/` as
`[feature]-[page]-[viewport]-[action].png`. Responsive **reflow** (elements rearranging while all remain visible) is
**not** a failure — only element loss or visible drift counts.

## Design fidelity — deterministic, not an aesthetic score

Fidelity is **binary**: does the build match the approved visual contract? It is *not* the subjective "is this design
good" question (that was `02`'s call at approval; re-litigating it here is out of scope). If a manifest exists at
`docs/design/approved/sprint-NN/manifest.md`, verify **every DM-ID** against the mockup and the build:

- **PRESENT** — matches the mockup in appearance, size, and prominence.
- **MISSING** — not found in the build.
- **DRIFTED** — exists but is visually subordinate, undersized, or mispositioned vs the mockup. **DRIFTED explicitly
  covers UNDERSIZED / DEEMPHASIZED** — an element rendered at 3–8px where the mockup shows it prominent is DRIFTED, not
  PRESENT.

Manifest coverage (every DM-ID PRESENT) + a visual diff is a **defined rule** — deterministic, gradeable, no judge. A
design criterion that "two agents could disagree about" is a **spec defect the reviewer flags** (route to `02`/`03`),
never a fidelity call 05 invents. For a headless text-render slice the "elements" are structural parts of the rendered
text (a dated header, per-member sections) — verify them by a `unit` assertion over the rendered string, no browser
needed.

## The honesty gate (hard) — the verdict follows the ledger

Assemble the **Verification Ledger**: Executed / Observed / Inferred counts over all "Done When" items + VC rows. Then:

- **SHIP** requires **Inferred = 0** over in-scope behaviors **and** no uncovered MUST/P0 REQ. Real execution evidence
  for every in-scope behavior — no exceptions.
- **`Inferred > 0`** (any behavior 05 could not execute or observe) **⇒ FIX REQUIRED or BLOCK**, never SHIP.
- **A MUST/P0 REQ uncovered** ⇒ FIX REQUIRED regardless of the aggregate coverage % (risk-priority-keyed).

**The consistency rule:** if you are about to write "SHIP" while `Inferred > 0` or a MUST-gap exists, **stop** — the
verdict is inconsistent with the ledger; rewrite it. The session summary leads with the ledger counts and the verdict,
because the QA report may go unread but the summary is the surface the user always sees — any gap not on that line is
effectively hidden.

## LLM/AI error analysis — an optional module

If (and only if) the project has LLM / RAG / agent components (`system.md` names them), a leaner error-analysis pass
applies — see `references/llm-review.md`. For a pure-domain slice, skip it entirely; do not invent AI-quality findings
where there are no AI components.
