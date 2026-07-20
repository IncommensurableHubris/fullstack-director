# TeamPulse — docs legibility index

> Where every declaration lives and how to check it. Produced by **skill 00 (discovery)**. The **spine**
> (`docs/spec/`) is the single source of declaration-truth; everything else references it by `REQ-NNN`.

## The spec spine (`docs/spec/`)

| File | What it holds |
|------|---------------|
| [`spec/specification.md`](spec/specification.md) | **Index** — the Constitution (project non-negotiables) + the authoritative **REQ registry** (ID → file). |
| [`spec/capabilities/standups.md`](spec/capabilities/standups.md) | Standups domain — REQ-001…004 (submit, edit, lock, needs-help). |
| [`spec/capabilities/team.md`](spec/capabilities/team.md) | Team domain — REQ-005…007 (create+invite, configure digest, join). |
| [`spec/capabilities/digest.md`](spec/capabilities/digest.md) | Digest domain — REQ-008…010 (generate, surface help, read any day). |
| [`spec/capabilities/access.md`](spec/capabilities/access.md) | Access & identity — REQ-011 (magic-link sign-in), REQ-012 (tenant isolation, `derived`). |
| [`spec/design-intent.md`](spec/design-intent.md) | Declared look/feel & key moments (mostly `derived` — the PRD says little on UI). |
| [`spec/architecture-constraints.md`](spec/architecture-constraints.md) | Stack (TS/Node/PostgreSQL), hosting (Dockerized VPS, EU-only), auth, scale mandates. |
| [`spec/amendment-log.json`](spec/amendment-log.json) | Structured change history (git is the dated trail). Currently empty. |

## Discovery record (`docs/discovery/`)

- [`discovery/charter.md`](discovery/charter.md) — JTBD, problem/user, scope, and the gate **decision log**.
- [`discovery/assumption-map.md`](discovery/assumption-map.md) — the CHALLENGE output: the three Unknown+Important
  bets (tenant isolation, distributed day-boundary, non-submitter handling) and the PROCEED decision.

## Open clarifications

Two `[NEEDS CLARIFICATION]` markers survive (REQ-001 day boundary; REQ-008 non-submitter handling) and one `derived`
REQ (REQ-012 tenant isolation) awaits confirmation. These are legitimate pre-release, but **06-release blocks deploy**
on any survivor — resolve them before shipping.

## Standing gate — `scripts/verify-spine.py`

Mechanical integrity check over `docs/spec/` (registry ↔ block resolution, no orphans/dupes, amendment-log schema,
plus WARN-level terseness/marker checks). Stdlib-only, Python 3.8+.

```sh
python scripts/verify-spine.py            # human-readable; exit 0 = pass (warnings allowed)
python scripts/verify-spine.py --json     # machine-readable for CI
python scripts/verify-spine.py --root .   # explicit project root
```

### Opt-in wiring (samples in `scripts/hooks/` — activate if you want the gate enforced)

- **Pre-commit hook** — [`scripts/hooks/pre-commit.sample`](../scripts/hooks/pre-commit.sample). Activate:
  ```sh
  cp scripts/hooks/pre-commit.sample .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
  ```
  A FAIL-severity check (L1–L5) blocks the commit; WARN checks print but never block.
- **GitHub Actions** — [`scripts/hooks/spine-verify.yml`](../scripts/hooks/spine-verify.yml). Activate:
  ```sh
  cp scripts/hooks/spine-verify.yml .github/workflows/spine-verify.yml
  ```
  Runs `verify-spine.py` on every push / pull request.

## Governance

`docs/spec/` is amendment-gated declaration-truth; skill artifacts (design, architecture, code, tests) are
drift-gated realizations that reference REQs by ID. On any product/scope question, the Constitution wins.
[`AGENTS.md`](../AGENTS.md) at the repo root is a **generated** read-only projection of the Constitution — never
hand-edit it; edit `spec/specification.md` and regenerate.
