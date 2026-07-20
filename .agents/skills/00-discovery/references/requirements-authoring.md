# Requirements-authoring craft

> Loaded by skill 00, phases 2 & 4 (INGEST, FIDELITY). How to turn source material into well-formed REQ blocks. Folds
> in proven story-writing craft + 2026 BDD best practice — but at the spine's **outcome altitude** (see
> `shared/spine-boundary.md`, Rule 2 — repo-root-relative, per the framework's no-`../` rule).

## A REQ is an EARS statement + outcome-level acceptance

Write each REQ as an **EARS statement line** (the one-sentence capability, in one of the five patterns in the next
section) plus **outcome-level Gherkin** — not a user-story:

- **Statement line (EARS — MANDATED):** the capability in one closed SHALL-form, e.g. "WHEN a returning user submits
  valid credentials, the system SHALL start a session." The five patterns and when to use each are the next section.
- **Acceptance (outcome Gherkin):**
  - `Given` — a **specific** precondition ("Given a registered user with a verified email", not "Given a user").
  - `When` — **exactly one** user-observable action. Two `When`s ⇒ two scenarios.
  - `Then` — an **observable** outcome ("Then they land on their dashboard", not "Then a row is written to the DB").
  - **Behavior, not implementation:** "When the user submits valid credentials", never "When they click `#submit`".
  - **1–3 scenarios** per REQ (a happy path + the key edge). Needing 4+ usually means it's **two REQs** — split it.

The "As a / I want / so that" rationale is **not** repeated per REQ — it lives once in the charter JTBD.

## EARS statement syntax (the mandated form)

EARS keeps the statement line machine-checkable **and** readable — a small closed grammar around `SHALL`. **Every REQ
statement line MUST match one of these five patterns** (the registry stays parseable; graders check the SHALL-form):

| Pattern | Shape | Use for |
|---|---|---|
| **Ubiquitous** | `The <system> SHALL <response>` | always-on invariants |
| **Event-driven** | `WHEN <trigger>, the <system> SHALL <response>` | the common case — a response to an action/event |
| **State-driven** | `WHILE <state>, the <system> SHALL <response>` | behavior that holds *during* a state |
| **Optional-feature** | `WHERE <feature>, the <system> SHALL <response>` | `MAY`-priority / config-gated REQs |
| **Unwanted-behavior** | `IF <undesired condition>, THEN the <system> SHALL <mitigation/refusal>` | **must-not REQs** (negative / abuse cases) |

Keep `<system>` a concrete subject (the service, the digest, the API) and the SHALL-clause **user-observable** — the
**outcome altitude** rule below still governs *what* the clause may say. Mandated EARS constrains the statement's
*shape*, never its altitude. Uppercase the keywords (`WHEN`/`WHILE`/`WHERE`/`IF`/`THEN`/`SHALL`); one `WHEN` per REQ
(two triggers ⇒ two REQs, mirroring the one-`When`-per-scenario rule).

### Must-not REQs — the home for negative & abuse declarations

The **Unwanted-behavior** pattern (`IF … THEN the … SHALL <refuse / deny / reject / bound>`) is where a *negative*
requirement lives: "IF a request lacks a valid session, THEN the system SHALL deny access." Reach for it whenever the
spec says the system must **refuse, deny, reject, or limit** something. This gives 07-security a template slot to
route a *missing security declaration* into — closing the loop ("missing declaration → route to /00" now has
somewhere to land) — and it is the natural output of an adopt-mode auth invariant or a CHALLENGE abuse case.

### Numbers need sources

Any **quantitative claim** entering the spine — a latency target, a scale figure, a price, a TAM — carries a source
quote (⇒ `stated`) or an explicit assumption / `[NEEDS CLARIFICATION]` tag. A number the skill *inferred* ("respond
within 200ms") is a `derived` fact and must be **marked**, never transcribed as if the user set it. This is just the
stated/derived discipline (below) applied to numbers — Topcu failure mode #2, unsubstantiated estimates.

## Acceptance for distributional behaviors — the eval block

Outcome-Gherkin declares a **deterministic** result: given X, the observable outcome is exactly Y. But many agent
behaviors have **no deterministic oracle** — "the reply is helpful and grounded" is *distributional*, graded over a
dataset of cases, never asserted on a single input. The rule (S5): **Gherkin for deterministic outcomes; an eval
block for distributional ones; both when a REQ layers a deterministic guard over a distributional behavior** (e.g. a
must-not that is hard-enforced *and* a quality bar that is measured).

A distributional REQ carries an **Eval block** in place of (or beside) its Gherkin. The contract + governance —
datasets live in-spine, floor classes, the bite rule, the escape hatch — live once in
[`shared/agentic-profile.md`](../../../../shared/agentic-profile.md); author the block in this shape:

````
**Acceptance (eval-suite):**
dataset:   docs/spec/evals/<domain>/<name>.jsonl   (versioned, in-spine)
grader:    code | judge(validated) | human
metric:    pass@k | pass^k | score
floor:     NN%          class: regression | capability
negatives: >=1 must-not case in the dataset
````

- **`dataset:` is in-spine** (`docs/spec/evals/**`) — a golden dataset **is** the behavioral spec, so it is
  amendment-gated; the standing gate's **L6** check fails on a dangling ref (same discipline as registry↔leaf).
- **`floor` / `class`:** a **regression** floor runs ≈100% (a regression is never acceptable); a **capability** floor
  starts deliberately low (a saturated floor gives no signal). Seed **20–50 cases from real failures**; the dataset
  grows through 05's error analysis (a patch may only ADD cases — the additive exception).
- **`negatives`:** every dataset carries **≥1 must-not (negative) case** — pair it with the REQ's IF/THEN must-not
  statement, so the abuse case is both *declared* (the statement) and *measured* (the dataset).
- **Greenfield bootstrap:** with no real failures yet, seed the dataset via the dimension→tuple synthetic
  method (evals-operations capability, `shared/agentic-profile.md` §eval-suite) — still 20–50 cases, negatives
  mandatory, and the seed grows error-analysis-first from real traces (seed, never spec).

## Outcome altitude (don't over-specify)

The spine holds *what the user can observably do*. Detailed, UI-specific steps ("click the gear, then Security…")
are **realization** — they belong in skill 03's feature-spec Verification Contracts, never in a REQ. If a scenario
names a selector, a screen layout, or an internal mechanism, it is at the wrong altitude.

## Fidelity: stated vs derived (+ source quote)

Every REQ carries a `<!-- source: … -->` line and a registry **Status**:
- **`stated`** — it traces to a real source: a **verbatim quote** from the user's doc, or `"interview: <topic>"` for
  something the user said. Both a doc and an interview are valid sources of `stated`.
- **`derived`** — the skill **inferred** it beyond what the user said or wrote. Mark `source: inferred`. A `derived`
  REQ is a flag for human confirmation at the gate — **never** a silent fact.

When unsure whether you're *stating* or *inferring*: you're inferring → `derived`.

## Coverage checklist (the retired brief's facets — now a fidelity check)

A complete spine covers all seven. A gap in any → a CLARIFY question, or a `[NEEDS CLARIFICATION]` marker if deferred:
- [ ] **Problem** — what's broken / painful (→ charter)
- [ ] **Target user** — a concrete segment (→ charter)
- [ ] **JTBD** — the canonical job (→ charter)
- [ ] **Scope** — in **and** out (→ charter; in-scope ⇒ the `MUST` REQs)
- [ ] **Success criteria** — = the REQs' outcome Gherkin
- [ ] **Constraints** — stack / hosting / compliance / scale (→ `architecture-constraints.md`). A technology **too
  new for reliable recall** also earns a `## Verify-live` row there — a *constraint*, not a REQ; its live-source
  seed craft lives in `shared/live-source-verification.md`, not here.
- [ ] **Quality attributes (NFRs)** — which **ISO/IEC 25010** characteristics are load-bearing for *this* product
  (performance · reliability · security · scalability · … ), **each with a number** ("p95 < 500 ms at 1k concurrent",
  "RPO ≤ 24 h") (→ `architecture-constraints.md` — quantified NFRs are declarations). A bare "-ility" with no target
  is not a declaration: quantify it or mark it `[NEEDS CLARIFICATION]`; every number obeys the sources rule above. 03
  realizes each as a **§10 measurable scenario with an executable fitness function**.

## Priority (RFC 2119 — drives skill 01's sprinting)

Map MoSCoW → registry priority: **Must → `MUST`**, **Should → `SHOULD`**, **Could → `MAY`**. **"Won't" → an explicit
out-of-scope note in the charter**, *not* a registry row. Smell-test: if >60% of REQs are `MUST`, push back on scope
— a lean MVP is closer to 40 / 30 / 30.

## A CLARIFY answer becomes spine content

When the user answers a gap at the gate, fold the answer into the REQ as now-`stated` content with
`source: "clarification: <topic>"`. The spine *is* the record — there is no separate "clarifications" file.
