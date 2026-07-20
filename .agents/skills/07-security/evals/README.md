# 07-security evals

Follows **`/skill-creator`'s A/B method** (deterministic grader; no LLM judge). The input is a **seeded reviewed
project state** — a git repo whose HEAD (the audited commit) carries TeamPulse's **sprint-02 HTTP API surface** (a
zero-dep `node:http` server + session auth + a team-scoped store over the sprint-01 digest core), a spine that gives
the panel its trust-boundary + data-sensitivity context, and `05`'s SHIP qa-report. For each case in
[`evals.json`](evals.json), run two arms and compare the skill's **lift**:

1. **with_skill** — a fresh agent loads `.agents/skills/07-security/SKILL.md` and runs `07-security sprint 2`: seeds
   from `system.md` + constraints (+ the R5 gate: no AI components → R5 stays off), spawns the **4-reader read-only
   OWASP panel** (blind, neutral evidence-required prompts), synthesizes (de-dupe · max severity · preserve quotes),
   and writes a severity-keyed **PASS/REMEDIATE/BLOCK** verdict + a panel manifest to
   `docs/security/security-audit-sprint-02.md`.
2. **baseline** — a fresh agent performs the same prompt with **no skill** (ignore framework files). Shows what the
   isolated, de-duplicated, false-positive-controlled, machine-verdicted audit adds over an ad-hoc security review.

## Why an extended HTTP API surface (and a fixture-builder, not `cp`)

The `05`/`06` TeamPulse domain is **pure zero-dep functions** (`recordStandup`, `assembleDigest`) with **no attack
surface** — OWASP areas (injection, broken access control, SSRF) have nothing to bite on. So this fixture **extends**
TeamPulse into the **sprint-02 HTTP delivery**: a `node:http` API (`src/server.js`), session auth (`src/auth.js`), a
team-scoped store (`src/store.js`). The clean `app/` is a **genuinely hardened** baseline (server-verified auth,
server-side per-team authz, SSRF allowlist, env-var secret, no injection surface) so the crying-wolf guard is
meaningful; each case overlays specific vulnerable files. [`build_fixture.py`](build_fixture.py) assembles the git
repo (seed spine → build the API surface + case overlay; HEAD = the audited commit; `.env` copied but gitignored).
**07 is a read-only static audit** — the code need not run, so read-only-ness is trivially checkable via `git diff`.

```
python build_fixture.py --case <vuln|clean|block-arch|synthesis> --out <arm>/outputs
# ... arm runs `07-security sprint 2` over outputs/ ...
python check_security.py --outputs <arm>/outputs --case <vuln|clean|block-arch|synthesis>
```

`check_security.py` writes `grading.json` (`{expectations:[{text,passed,evidence}]}`) into `--outputs`; copy it to
the arm root for `eval-viewer/generate_review.py`. **07 SPAWNS the panel** → **relax the harness `<SUBAGENT-STOP>`**
(the `03`/`05` precedent; `docs/eval-methodology/harness-reference/`) or the readers short-circuit. Workspaces live
**outside `.agents/skills/**`** (e.g. `_artifacts/skills-eval/07-security/iteration-N/<case>/<arm>/outputs/`).

## What the assertions check (the lift is the VERDICT + PANEL DISCIPLINE + READ-ONLY + F1, never audit prose)

`07`'s value is **not** "finds vulnerabilities" — a strong baseline does that too (and the FPR research shows ad-hoc
LLM review cries wolf 68–97% of the time). It is the **isolated, de-duplicated, false-positive-controlled,
machine-verdicted audit** `06`'s G6 can gate a ship on. The deterministic discriminators:

- **Verdict correctness (severity-keyed)** — `vuln` → **REMEDIATE** (code-fixable Highs); `clean` → **PASS**;
  `block-arch` → **BLOCK** (a Critical architectural flaw); the machine `verdict:` is what `06` G6 reads.
- **Sensitivity** — `vuln` **names each of the 5 orthogonal plants** in a structured finding with a `source_quote` +
  a re-derived severity (IDOR · reflected XSS · hardcoded secret · SSRF · slopsquat dependency). *The killer: the
  verdict is not PASS — a rubber-stamp "PASS with recommendations" false-proceeds `06` G6.*
- **Specificity (the crying-wolf guard)** — `clean` returns **PASS with ~0 findings** and the completeness lens
  recorded. Together with sensitivity this is the **F1 frame**: a rubber-stamp (miss) and a cry-wolf (false alarm)
  are *equally* disqualifying.
- **REMEDIATE↔BLOCK routing** — `block-arch` must **BLOCK** and route to **`/03-architect`** (architectural), not
  downgrade to a `/04-builder` code patch. A naive audit collapses the two.
- **Synthesis discipline** — `synthesis` plants **one** SSRF that sits in two readers' remits (A10 SSRF · A01:2025)
  → the report must show it **de-duped to exactly one finding** (max severity, quote preserved) + a **panel manifest**
  (≥ 4 readers). *(The "ran as N blind parallel subagents" half is **manual**, per `shared/subagent-protocol.md` —
  Pass-2 judgment is never deterministically graded; the deterministic proxy is the manifest + read-only.)*
- **Read-only, made auditable** — the audit modified **no code**: `git diff` on `src/**` is empty at HEAD (a strong,
  fully-deterministic isolation proxy — the analog of `05`'s context attestation).
- **No-secret + non-amender** — the planted hardcoded token + the `.env` key appear **nowhere** under `docs/**`
  (names only); `docs/spec/**` + `amendment-log.json` are byte-identical to the seed (`07` classifies + routes; it
  appends no row).

A baseline audits ad-hoc: it may find the vulns but drop an unassigned OWASP area, cry wolf on the clean build, emit
a prose verdict `06` can't gate on, collapse REMEDIATE↔BLOCK routing, produce no panel manifest / read-only
attestation, and reproduce the secret value. That gap is the graded lift.

## The four fixtures (F1-framed + the BLOCK arm)

- **`vuln`** (sensitivity — REMEDIATE) — 5 orthogonal, **code-fixable HIGH** plants across the HTTP surface: **A01
  IDOR** (`/digest` returns any member's data), **A03 reflected XSS** (`/search` echoes `?q` unescaped), **A02
  hardcoded secret** (`API_TOKEN` in `src/server.js`), **A10 SSRF** (`/notify` fetches a user URL, no allowlist), and
  a **supply-chain** plant (unverified/floating `teampulse-slackfmt`). → **REMEDIATE**, each named, routed to `/04`.
- **`clean`** (specificity — PASS) — the unmodified hardened `app/` → **PASS, ~0 findings**, completeness recorded.
- **`block-arch`** (the BLOCK arm) — a **Critical, architectural** flaw: identity + role taken from client-supplied
  headers with no server-side verification (`src/auth.js`), `/admin/export` gated on a client-controlled role → a
  complete auth bypass + privilege escalation, violating ADR-002. → **BLOCK → `/03-architect`**.
- **`synthesis`** (the panel's discipline) — one **SSRF** in two readers' remits (A10 + A01:2025) → **de-duped to one
  finding** + a **panel manifest**; read-only.

## Grader validated (not vacuous)

Before any A/B run, `check_security.py` was validated against **hand-built ideal reports** AND **degenerate** ones:

| Report | Case | Score |
|--------|------|:-----:|
| hand-ideal REMEDIATE (5 plants named + source quotes) | `vuln` | **17/17** |
| hand-ideal PASS (hardened, completeness recorded) | `clean` | **10/10** |
| hand-ideal BLOCK (Critical, routed to /03-architect) | `block-arch` | **12/12** |
| hand-ideal de-duped SSRF + panel manifest | `synthesis` | **12/12** |
| **rubber-stamp** (PASS on the vuln surface — missed every plant) | `vuln` | **7/17** — all 10 sensitivity discriminators fire |
| **crying-wolf** (REMEDIATE, invented Highs, on the hardened build) | `clean` | **8/10** — both specificity discriminators fire |
| **block-downgrade** (rated the Critical a High, routed to /04) | `block-arch` | **9/12** — all 3 REMEDIATE↔BLOCK discriminators fire |

> **Severity-label note.** The `vuln` case does **not** grade the exact REMEDIATE-vs-BLOCK label (whether a hardcoded
> `sk-live-…` token is a code-fixable **High** or a "live credential" **Critical** is genuine auditor judgment). It
> grades **sensitivity** — not-PASS, all five plants named with a `source_quote`, the multiple vulns recorded at
> severity, and the code fixes routed to `/04-builder`. The **REMEDIATE↔BLOCK routing discrimination is the
> `block-arch` case's job**, where the architectural answer (BLOCK → `/03-architect`) is unambiguous.

So the discriminators are **real, not vacuous**: the grader penalizes a rubber-stamp (miss), a cry-wolf (false
alarm), **and** a verdict-downgrade that collapses the REMEDIATE↔BLOCK routing — while crediting a correct, isolated,
de-duplicated, machine-verdicted audit. (A key grader hardening: the plant checks require the **specific vulnerability
signature** — `IDOR` / `entriesForMember(target)` / `teampulse-slackfmt` — never the bare OWASP area name, so a
rubber-stamp that merely lists "Injection: fine / Supply chain: fine" gets **coverage** credit but **not detection**
credit.)

## iteration-1

| Case | with_skill | baseline |
|------|:----------:|:--------:|
| `vuln` | **17/17** | 15/17 |
| `clean` | **10/10** | 7/10 |
| `block-arch` | **12/12** | 12/12 |
| `synthesis` | **12/12** | 11/12 |

**with_skill passed every assertion on all four cases (51/51, 100%); baselines averaged 88% (45/51).** The baselines
were **strong security auditors** — every one genuinely read the code and traced source→sink: the `vuln` baseline
caught all five plants **plus** a sixth (the zero-dep-mandate breach) and correctly refused to trust the in-source
`PLANT` comments; the `block-arch` baseline nailed the Critical client-trusted-authz defect, wrote **full machine
frontmatter**, and routed it to `/03-architect` (a legitimate **12/12 tie** — a strong baseline that happened to emit
the structured record). Detection quality was **not** the differentiator — exactly as the framework's eval doctrine
(`feedback_framework_skill_lift_is_structural`) predicts.

**The lift is the specificity + the machine-readable, de-duplicated contract the baselines produced inconsistently:**

- **Crying wolf on the hardened build (the headline lift, `clean` 10 vs 7).** The `clean` baseline rated the
  **gitignored, git-untracked** `.env` session key a ship-blocking **High** and returned **REMEDIATE** — a false
  alarm on genuinely hardened code — and invented the High with no machine `findings_*`/`areas_audited` record. The
  `with_skill` arm recognized the declared secrets model (`.env` ignored + untracked = per-mandate), verified the
  positives (server-verified HMAC identity, server-side per-team authz, the SSRF allowlist), and reached **PASS** with
  a recorded completeness lens. A security auditor that cries wolf on hardened code cannot be trusted to gate a ship.
- **No machine-readable verdict record (`vuln`, `synthesis`).** The `vuln` baseline wrote **pure prose** — no
  `verdict:`/`findings_*` frontmatter — so `06-release` G6 could not gate on it; the `synthesis` baseline reported the
  SSRF in ad-hoc prose rather than a **de-duped structured Findings row**. The `with_skill` arms emitted the machine
  frontmatter + a single de-duped SSRF finding (R1 A01:2025 + R2 A10:2021 → **one** finding, max severity, quote
  preserved) + the panel manifest + the read-only attestation.
- **No routed next-command (`vuln`).** The baseline gave generic "fix these" advice; the `with_skill` arm routed the
  code-fixable findings to **`/04-builder`** then a fresh `/07-security` re-audit (the framework's loop vocabulary).

Across every arm the `with_skill` audit was **read-only** (`src/**` byte-identical — the deterministic isolation
proxy), reproduced **no** secret value (env-var names only), and left the spine + amendment-log **byte-identical**
(non-amender). So a fresh `07` verdict can gate `06`; a baseline's cannot — reliably. That gap — specificity +
machine-readable + de-duplicated + routed — is the graded lift. (Run workspace:
`_artifacts/skills-eval/07-security/iteration-1/`, gitignored.)
