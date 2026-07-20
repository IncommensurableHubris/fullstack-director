# Deploy & Verification — SETUP · PLAN · EXECUTE · VERIFY · LEARN

> Load at step 2 (SETUP) and keep through step 6. The craft half of `06`: how the platform is resolved, how the one
> approved plan is written and executed, what "verified" means before a release may be called RELEASED, and how
> failures become guardrails. The gate half is `references/release-gate.md`.

## SETUP — first run only (`docs/release/deployment-config.md` absent)

### Platform resolution (a named technology is never `06`'s call)

Resolve in strict order; record **which source decided** in the config:

1. **Spine mandate** — `docs/spec/architecture-constraints.md` names hosting/platform ("deploy to the user's
   Hetzner VPS via Coolify", "Vercel", "the local stand-in platform under `scripts/`"). Follow it.
2. **ADR** — `docs/architecture/adr/**` records a platform decision `03` already made. Follow it.
3. **Neither** — **pause and ask the user.** Present the honest 2026 trade (managed PaaS: near-zero ops, cost
   scales with usage · self-hosted PaaS on a VPS: cheapest for multiple apps, but you own updates/backups/patching
   — and platform CVEs make version currency a real duty). Record the user's choice in the config **and recommend
   back-filling it upstream** (an `architecture-constraints.md` mandate via `00 reflect`, or an ADR via `03`) so
   the next project state carries the decision where it belongs. `06` is a non-amender — it recommends the
   back-fill; it never writes the spine.

### Interface resolution (live, never memorized)

Platform APIs and CLIs move; a baked-in command set goes stale and then fails at the worst moment. At SETUP (and
whenever a deploy command errors unexpectedly):

- Resolve the platform's **current** deploy interface from its live documentation or CLI help (use the project's
  configured doc tooling where available; otherwise fetch the platform's docs). *(This is **verify-before** applied
  to the deploy platform — the same move `shared/live-source-verification.md` mandates for declared verify-live
  build dependencies; the confabulation guardrail generalizes this instance, it did not invent it.)*
- Record the resolved commands **in `deployment-config.md`** — the config is the project's durable deploy
  **runbook**; the skill carries the *shape* (create app → configure domain/SSL/env → deploy → verify → rollback),
  the config carries the *commands*.

### What SETUP records (`templates/deployment-config.md`)

Platform + decision source · repo/remote (the deploy source of truth) · app/service identity · domain + SSL ·
**environment variable NAMES** with purpose (values live in the platform's secret store and are set **by the
user** — `06` never sees, echoes, or stores a value) · health endpoints + expected responses · the resolved deploy
commands · the rollback procedure (platform mechanism first, `git revert` as the floor) · the **`## Operations`
runbook** (below).

### The `## Operations` runbook — one journey, one SLO (G9)

SETUP also writes a short **`## Operations`** section — the steady-state runbook G9's Operations-completeness clause
checks (every profile). Google SRE small-team guidance: resist a wall of dashboards; pick the **ONE critical user
journey** and put **one SLO** on it. The section records: the **SLO** (the graded floor) · where **logs** live · one
**alert** (a burn-rate note on the SLO's error budget) · the **rollback-drill cadence** · and the **drift & sampling
line** — production trace/log sampling + one drift signal (data/behavior/model) routing to `/00-discovery reflect`.
The drift line's **single home** is here; the agent-profile span-smoke (VERIFY) *references* it, never restates it.
Incident-response lines (preserve · assess · notify-within-X) are `on-demand(first release with real users/data)`.

## PLAN — one plan, one approval (plan/apply)

The plan is the **action preview** for the single human approval — the only gate between `06` and the outside
world. It is invalid without every one of:

- **Ordered steps with exact commands** — copy-runnable, from the config's runbook; placeholders resolved.
- **Expected evidence per step** — what PASS looks like (exit 0, a deployment ID, a 200 with the expected body),
  so EXECUTE captures against a stated expectation, not vibes.
- **Blast radius** — what this deploy can affect (the app, the domain, data, third parties); anything irreversible
  is named as such (a DNS cutover, a migration).
- **The rollback path** — the concrete restore procedure *for this deploy*, pre-stated. **A plan without a
  rollback path must not be presented for approval.**
- **Guardrail conformance** — every rule in `.claude/rules/deployment-guardrails.md` explicitly satisfied or
  explicitly flagged.

Present the plan; **pause**. The approval is **one** decision on the whole plan (batch, like the amendment
protocol's Tier-2 gate — never one confirmation per command). Nothing irreversible or externally visible runs
before it: no push, no deploy trigger, no DNS, no tag-push. After approval, execute *that* plan; a material
deviation (a command changed, a step added) is a **new plan** needing a new approval — silent drift from the
approved preview is the exact failure the pattern exists to prevent.

### Migrations — the conditional G10 gate

When the release diff or the plan contains a **schema/data migration**, the plan must satisfy **G10**: identify the
pending migration(s); for a **destructive** one (a drop / rename / alter-type / truncate), put a **backup step before
it runs**; and state the **rollback path's data implications** (does rollback need a data action? is it forward-only?
is data loss possible?). G10 is **conditional** — no migration ⇒ N/A, recorded, never silently skipped. The migration
*contract* (the forward command + the rollback-compatibility statement) is authored upstream in 03's feature-spec
**Migration** row; the plan here operationalizes it (the backup step + the ordered commands). *(A model/provider swap
is the next subsection's concern, not a migration — G10 does not fire on it.)*

### Model-facing changes — a swap requires re-eval or an explicit waiver

If the release diff **swaps a model or provider** (a changed model id / endpoint / provider SDK in `src/**` or the
deploy config), the plan must **reference the model-migration protocol** (`shared/model-migration-protocol.md`:
shadow → classify → canary → full) **or record an explicit waiver with a reason**. Evals alone demonstrably miss
co-adaptation regressions (~15% divergence outside the eval distribution), so a model swap is **not** a like-for-like
config change — shipping one silently ships an un-re-evaluated system. (The EU AI Act GPAI checklist attaches here
**only when** `architecture-constraints.md` declares EU-market distribution — documented, off by default.)

## EXECUTE — captured evidence, step by step

- Run each step; capture `command · exit code · output excerpt` into the deploy log **as it happens**. An excerpt
  is enough (IDs, statuses, the failing line) — but it must be the **real output**, never a paraphrase.
- Scrub secrets from every captured excerpt (names fine, values never) — G7 applies to the log too.
- **Failure handling:** a step fails **before** anything went live (build failed, push rejected) →
  `status: FAILED`, stop cleanly, write the report + a guardrail row. A step fails **after** the new version is
  live or traffic moved → the rollback drill (below).

## VERIFY — health before traffic, smoke after, rollback on failure

Deploy ≠ release. The order is fixed:

1. **Health, pre-traffic** (where the platform exposes the new version before cutover — a preview URL, the
   inactive color, a staging slot): liveness ("is it up") **and** readiness ("are its dependencies reachable"),
   with expected status + body from the config. On a platform with no pre-traffic surface, health runs immediately
   post-cutover and the rollback window is declared in the plan.
2. **Switch** — the platform's cutover (traffic to the new version). Only after health passes.
3. **Smoke, on the live surface** — few, critical, fast: the health endpoint(s) again *through the public route*,
   plus the sprint's highest-impact flows (derive from the slice's REQ outcomes — the digest renders, the login
   round-trips). Each smoke row: the command/probe, expected, actual, PASS/FAIL — captured.
4. **On any verification failure:** execute the plan's rollback path **now** (don't debug live) → re-verify health
   on the restored version → `status: ROLLED-BACK`. Debugging happens afterwards, from the captured log, routed to
   the owning skill. A rollback that itself fails ⇒ `status: FAILED`, and the session summary **leads** with
   "requires manual intervention" + exactly what state the system is in.
5. **All green** ⇒ `status: RELEASED` · annotated tag `release/sprint-NN` at the deployed commit (tag-push only if
   it was in the approved plan).

**The evidence bar:** RELEASED requires the deploy log + health + smoke rows to carry captured output. "It
deployed fine" with an empty verification section is a FAILED report wearing the wrong status — the same
assertion-without-evidence `05`'s honesty gate exists to catch.

## REPORT — the release record

`templates/release-report.md`. Machine frontmatter first (the fields `status` / `gate_*` / `deployed_commit` /
`health` / `smoke_*` — what `status`, `00 reflect`, and the next `06` run read); then the gate table, the approved
plan, the deploy log, verification, **REQ-keyed release notes** (each in-scope REQ-ID + its outcome line — "what
shipped" in the spine's vocabulary, traceable, not marketing prose), the **Provenance block** (below), guardrails
learned, next command.

### Provenance — the release's content identity (D5 + D7)

The report's `## Provenance` block pins **what shipped**: the **artifact digest** (the built/deployed image or bundle
hash), the **built-from commit**, the **`spine_hash`** — `python scripts/verify-spine.py --hash` over `docs/spec/**`,
stamped into the frontmatter (D7) — and **`amendments_at_release`**, the amendment-log depth (D5). Together they make
"which spec + which build shipped in release N" a lookup and spec-diff-between-releases possible. If an SBOM tool is
available (syft / cdxgen), attempt it and record the result; **absence is recorded, not a hard gate**. The
**toolchain line is cut** (restore trigger: an SLSA-attestation consumer); under `agent-system`, **ML-BOM** component
fields (models · datasets · frameworks) are a **reserved** one-line note — declare, never build bespoke AI-BOM
machinery.

## LEARN — self-improving guardrails

`.claude/rules/deployment-guardrails.md` (append-only; created on first use; the `05` quality-guardrails pattern):

- **When:** any deploy failure, rollback, or near-miss (a step that needed a retry, an expectation that was wrong).
- **Row shape:** `### Guardrail NNN: <name>` · **Trigger:** what happened (one line, cited from the deploy log) ·
  **Rule:** the concrete pre-deploy check or constraint that would have prevented it. Specific and checkable —
  "verify the health endpoint path matches the config before deploying", never "be more careful".
- **Read-back:** step 3 (PLAN) conforms to every existing rule, explicitly.

## Secrets discipline (G7's craft)

- **Names in docs, values in the platform.** `deployment-config.md`, the report, the plan, and every log excerpt
  carry env-var **names** + purpose only. Values are set by the user directly in the platform's secret store.
- **`.env*` gitignored** — verify before any push; an example file uses obviously-fake placeholders
  (`your_api_key_here`), never realistic-looking tokens.
- **If a real secret was committed:** rotate the credential **first** (history scrubbing does not invalidate it),
  then clean the history; record a guardrail.
- **Never echo:** no `printenv`-style dumps into captured output; scrub any platform response that reflects a
  value back.
