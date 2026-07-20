<!-- Filename: docs/release/deployment-config.md — written at SETUP (first 06-release run); updated when the
     platform story changes. This is the project's durable deploy RUNBOOK: the skill carries the shape, this file
     carries the resolved commands. NO SECRETS — env-var NAMES only, values live in the platform's secret store. -->

# Deployment Config

> Owned by **skill 06 (release)**. Platform + interface resolved at SETUP (`references/deploy-verification.md`):
> constraint → ADR → user decision, commands from **live** platform docs (never memorized). `06-release sprint N`
> reads this to write the deploy plan; a human approves that plan before anything irreversible runs.

## Platform

| Field | Value |
|-------|-------|
| Platform | _<e.g. Coolify v4 on user's VPS · Vercel · Railway · local stand-in>_ |
| Decision source | _<architecture-constraints.md §… · ADR-NNN · user decision (recommend back-fill via 00 reflect / 03)>_ |
| Interface resolved from | _<the live doc/CLI-help consulted at SETUP + the date>_ |

## Deploy source (GitOps anchor)

| Field | Value |
|-------|-------|
| Repository / remote | _<e.g. github.com/org/repo — or "local repo, no remote (platform deploys the working tree)">_ |
| Deploy branch | _<e.g. main>_ |
| App / service identity | _<platform app ID / project name / service UUID>_ |

## Domain & TLS

| Field | Value |
|-------|-------|
| Domain(s) | _<e.g. app.example.com — or n/a>_ |
| TLS | _<e.g. Let's Encrypt via platform · platform-managed · n/a>_ |

## Environment variables — NAMES ONLY (values live in the platform's secret store, set by the user)

| Name | Purpose | Where the value lives |
|------|---------|----------------------|
| _<`DATABASE_URL`>_ | _<primary datastore>_ | _<platform secret store>_ |
| _<`API_TOKEN_X`>_ | _<external service auth>_ | _<platform secret store>_ |

<!-- G7: never a value here, in the report, or in any captured log excerpt. -->

## Health

| Probe | Endpoint / command | Expected |
|-------|--------------------|----------|
| Liveness | _<e.g. GET /health/liveness · `node scripts/health.mjs`>_ | _<200 `{"status":"ok"}` · exit 0>_ |
| Readiness (dependencies) | _<e.g. GET /health/readiness>_ | _<200, every dependency `ok`>_ |

## Deploy commands (resolved at SETUP — the runbook)

| Step | Command | Expected evidence |
|------|---------|-------------------|
| 1 _<push>_ | _<`git push origin main`>_ | _<remote up to date>_ |
| 2 _<deploy>_ | _<platform deploy command / API call>_ | _<deployment ID · exit 0>_ |
| 3 _<await build>_ | _<platform status poll>_ | _<state: running/healthy>_ |

## Rollback procedure (pre-stated; the plan is invalid without one)

1. _<platform mechanism first: redeploy previous deployment / switch back to the previous color / `vercel rollback`>_
2. _<verify health on the restored version (the same probes above)>_
3. _<floor: `git revert` the release commit + redeploy>_

## Smoke set (the live-surface critical flows)

| # | Flow (from the slice's REQ outcomes) | Probe / command | Expected |
|---|--------------------------------------|-----------------|----------|
| 1 | _<health through the public route>_ | _<curl the live URL>_ | _<200 + expected body>_ |
| 2 | _<the sprint's highest-impact flow>_ | _<command / scripted probe>_ | _<captured PASS>_ |

## Operations (`core` — the steady-state runbook: one journey, one SLO)

> Google SRE small-team guidance: pick the ONE critical user journey and put one SLO on it — resist a wall of
> dashboards. G9 (Operations-completeness) checks this section exists with its SLO. The **drift/sampling line lives
> here** (its single home); the agent-profile span-smoke references it rather than restating it.

- **SLO (`core`):** _<the one SLO on the critical journey — e.g. "99.5% of digest reads succeed < 300 ms over 30 days">_.
- **Logs:** _<where logs live — the platform log drain / a file / a service>_.
- **Alert (`core`):** _<one alert — a burn-rate alert on the SLO's error budget>_.
- **Rollback-drill cadence:** _<how often the pre-stated rollback is rehearsed — e.g. quarterly>_.
- **Drift & sampling (single home):** _<production trace/log sampling rate + one drift signal (data / behavior /
  model) that routes to `/00-discovery reflect`>_.

### Incident response · `on-demand(first release with real users/data)`

> A one-page IR floor — add at the first release that touches real users or data (not before). Three lines, no
> runbook ceremony.

- **Preserve:** _<what to capture first, before any change — logs, the affected DB snapshot, the running config>_.
- **Assess:** _<who triages + the severity call — scope · data touched · is it still ongoing>_.
- **Notify within X:** _<the window + who — e.g. "the operator immediately; affected users within 72 h" (align with
  `SECURITY.md`'s CVD window)>_.
