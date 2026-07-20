# Workstream B research — harness verification · vendoring patterns · dogfood feedback loop

> Three parallel Sonnet research agents, 2026-07-12, all claims live-verified against official sources (URLs
> inline). This is the evidence base for the workstream-B design (`wsb-vendor-design.md`). Condensed from the
> agents' full findings; load-bearing facts + citations preserved, prose trimmed.

## A · Harness verification (Claude Code · Codex CLI · Gemini CLI)

**The headline: one canonical `.agents/skills/` copy serves Codex AND Gemini CLI natively; only Claude Code needs
a physical duplicate.**

| Harness | Discovery (precedence) | Status | Invocation | Constraints |
|---|---|---|---|---|
| **Claude Code** | enterprise → `~/.claude/skills` → project `.claude/skills` (walks up + nested) → plugins. **`.agents/skills` NOT discovered** (6+ community issues, 3k+ upvotes, zero Anthropic response — [issue #31005](https://github.com/anthropics/claude-code/issues/31005)) | GA | auto (description) or `/skill-name` | Many Claude-only frontmatter extensions exist; listing truncates description+when_to_use at 1,536 chars. Symlinks documented-supported but community-reported flaky ([#25367](https://github.com/anthropics/claude-code/issues/25367)) |
| **Codex CLI** | repo `.agents/skills` (CWD→root) → `~/.agents/skills` ([PR #10437](https://github.com/openai/codex/pull/10437), 2026-02-03) + legacy `~/.codex/skills` → `/etc/codex/skills` | GA (since 2025-12) | `$skill-name` or implicit | Parses only `name`+`description`; optional `agents/openai.yaml` side-file for Codex metadata; listing budget 2% of context / 8k chars; `allowed-tools` NOT honored; **`.agents/` mounted read-only under default sandbox** (skills must not self-write); symlinks likely broken ([#8369](https://github.com/openai/codex/issues/8369)) — [developers.openai.com/codex/skills](https://developers.openai.com/codex/skills) |
| **Gemini CLI** | built-in → extension → user (`~/.gemini/skills` \| `~/.agents/skills`) → workspace (`.gemini/skills` \| `.agents/skills`); **within a tier `.agents/skills` WINS over `.gemini/skills`** | experimental v0.23.0 (2026-01-07) → **default-on v0.26.0 (2026-01-27)** → unmarked/stable at v0.50.0 (2026-07-08) | **model-driven only** via `activate_skill` tool + user consent prompt; NO user-typed `/skill-name` | recognizes `name` (must match dir) + `description`; no documented description cap — [geminicli.com/docs/cli/skills](https://geminicli.com/docs/cli/skills/), [changelogs](https://geminicli.com/docs/changelogs/) |
| **agentskills.io spec** | — | open standard (~2025-12-18, Anthropic-published), 46+ adopters incl. all 3 targets | — | required: `name` (≤64, kebab, = dir name) + `description` (1–1024); optional `license`, `compatibility`, `metadata` (arbitrary map — THE extension point), experimental `allowed-tools`. Extra dirs (`templates/`) explicitly legal |

**vs. our `docs/harness-support.md` table:** Claude `.claude/skills` CONFIRMED (dev-bridge framing still accurate);
Codex `.agents/skills` CONFIRMED (+ new user-level `~/.agents/skills`); Gemini both paths CONFIRMED (+ precedence
detail + stable-now). New finding: `.claude/agents/*.md` supports a **`skills:` preload array** (inject full skill
content into a subagent's startup context) — exactly what `shared/subagent-protocol.md` § spawn assumed.

**Emitter gotchas:** keep SKILL.md spec-minimal (ours already are: `name`+`description` only — the ≤1024 trim
commit `877301f` is now validated as load-bearing for all three harnesses); `name` == dir name everywhere;
repo-root-relative `shared/` reads work on all three (Codex: read-only is fine — our skills write to project
paths, never into `.agents/`); **no symlinks** (win32 + Codex + Claude flakiness → real-copy vendoring validated);
Gemini's consent-prompt invocation means descriptions carry the full trigger weight there (ours embed "Use when
the user says…" phrases — good).

## B · Vendoring / distribution patterns

**Recommendation (validated by convergent evolution): plain-copy custom generator + per-file SHA-256 manifest +
a cruft-style non-mutating `check` verb.** ~150–300 lines of stdlib Python. Rejected: copier/cruft (external deps,
"render a project" abstraction mismatch), git subtree/submodule (can't exclude `evals/` cleanly; submodules want
live-tracking consumers), vendir/copybara (non-Python toolchains, org-scale), npm/pip (registry model fights
"read/patch locally in emergencies"; instruction-file packages already implicated in a supply-chain incident —
[Aikido](https://www.aikido.dev/blog/agent-skills-spreading-hallucinated-npx-commands)).

Patterns stolen from the leaders:
- **Spec-Kit** ([integrations](https://github.github.io/spec-kit/reference/integrations.html)): per-integration
  manifest JSON with per-file **SHA-256 as-installed**; on upgrade/uninstall, files whose hash drifted (user-edited)
  are **skipped and reported, never clobbered**; `integration status` = dedicated read-only drift verb. Per-agent
  variance = 3 axes (directory · context-file · invocation syntax), inheritance not string-templating.
- **BMAD** ([install docs](https://docs.bmad-method.org/how-to/install-bmad/)): single owned root (`_bmad/`),
  `manifest.yaml` records version tag + **git SHA** + channel + repo URL — enough to reproduce the install.
- **cruft** ([cruft.github.io](https://cruft.github.io/cruft/)): the two-verb split — mutating `update` vs
  read-only `check` (exit 1 on drift, CI-able).
- **Chromium** ([README.chromium.template](https://chromium.googlesource.com/chromium/src/+/HEAD/third_party/README.chromium.template)):
  human-readable provenance README in the vendored tree (Name/URL/Version/Revision/**Local Modifications**).
- **Go generated-code convention** ([golang/go#13560](https://github.com/golang/go/issues/13560)) +
  `.gitattributes` `linguist-generated=true` ([linguist overrides](https://github.com/github-linguist/linguist/blob/main/docs/overrides.md)).
- **Claude plugin marketplaces** ([docs](https://code.claude.com/docs/en/plugin-marketplaces)): Claude-only; plugins
  are **copied to `~/.claude/plugins/cache`** and cannot reference repo-root `../shared` — structurally wrong for
  our repo-root-relative doctrine. Not a distribution channel for us (recorded, not deferred).

**Manifest schema (recommended fields + why):** `generator` + `generator_version` (forward-compat) ·
`source_repo` + `source_commit` (full SHA — the load-bearing pin; refs drift, SHAs don't) + `source_ref` (human
label) · `vendored_at` (ISO-8601) · `items[]` each `{name, kind, source_path, dest_path, files{relpath: sha256}}`.
"Local modifications" is **derived** at check time by re-hashing (never hand-authored — unlike Chromium's prose).

**Idempotence:** delete-and-recreate each managed `dest_path`, with the Spec-Kit protection: any file whose
current hash ≠ what WE last wrote is locally-modified → skip + report (`--force` to clobber). Write the new
manifest only after a successful sync. Drift check = two hash comparisons: consumer-side (disk vs manifest) and
upstream-side (manifest `source_commit` vs the framework repo's HEAD).

## C · Dogfood → distill → upstream feedback loop

- **Upstream-first** (Chromium [adding_to_third_party](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/adding_to_third_party.md),
  Android [upstream policy](https://source.android.com/docs/setup/contribute/contribute-upstream)): never silently
  patch the vendored copy — divergence makes future syncs unreviewable and loses fixes. Emergency local patches
  are allowed but must be **enumerated** (Chromium's `Local Modifications`) — for us, mechanically enforced: the
  hash manifest makes any local edit visible to `vendor check`.
- **Version-stamped feedback** ([Stapelberg 2026-04-05](https://michael.stapelberg.ch/posts/2026-04-05-stamp-it-all-programs-must-report-their-version/)):
  the VCS SHA is the one version fact that makes a report falsifiable; feedback without it is noise.
- **High-signal capture** (Mozilla [bug-writing](https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html):
  repro-steps + expected/actual + severity; Centercode [dogfooding-101](https://www.centercode.com/blog/dogfooding-101):
  one low-friction home; **closing the loop is the #1 signal lever** — un-responded feedback kills reporting).
- **Google's dogfood loop** ([Testing Blog 2014](https://testing.googleblog.com/2014/01/the-google-test-and-development.html)):
  a dogfood finding's terminal state is "the automated suite now covers this" — not just "fixed."
- **Eval-driven refinement** ([Husain evals-FAQ 2026-01-15](https://hamel.dev/blog/posts/evals-faq/): open-code
  traces → axial-code a failure taxonomy → saturation; build automated evaluators **only for failures that persist
  after the text fix** — not blanket; [Braintrust](https://www.braintrust.dev/articles/turn-llm-production-failures-into-regression-tests):
  one representative eval case per failure **cluster**, threshold-gated in CI; Anthropic
  [demystifying-evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents): capability evals
  graduate into the regression suite; [equipping-agents](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills):
  watch real trajectories, convergent workarounds across independent runs = the signal to harden a skill;
  **no published post-deployment skill-versioning process exists** — we are ahead of the ecosystem here).
- **ACE / self-improving playbooks** ([arXiv:2510.04618](https://arxiv.org/abs/2510.04618)): credible research,
  no independent replication — adopt only its transferable rule: **append structured deltas to doctrine; never
  periodically summarize/rewrite** (their named failure modes: brevity bias, context collapse). Matches ADR
  immutability ([adr.github.io](https://adr.github.io/)): supersede, don't edit.
- **Anti-patterns (each source-backed):** silent downstream patches · unstamped feedback · fix without a
  regression guard · collected-but-unanswered feedback (defer needs a revisit trigger) · eval-case bloat (one per
  cluster) · summarizing the lessons log · overfitting a fix to one transcript (skill-creator's warning) ·
  free-text scattered feedback · continuous unbatched re-vendoring (erodes the version stamp).

**Recommended loop shape (solo + 3 consumers, git-only):** append-only, SHA-stamped ledger per consumer
(`docs/framework-feedback.md`; fields: date · framework_sha · harness · seat · expected · actual · repro ·
severity ∈ blocks-gate/wrong-but-recoverable/friction-only · artifact pointer) → batched triage ritual in the
master repo before each re-vendor (disposition per entry: **fix / eval-case / doctrine-line / defer(+trigger)**,
logged append-only) → **every fix terminates in an eval case (one per cluster) or a dated doctrine line** →
tag master → re-vendor all consumers as one atomic act each → mark ledger entries resolved-in `<sha>`.
Note the isomorphism: this is our own amendment-protocol pattern (tiered dispositions + structured log) applied
to the framework itself.

## Uncertainties carried into the design

- Codex symlink support: conflicting evidence → treat as unsupported (we don't use symlinks anyway).
- `agents/openai.yaml`: secondary-source corroborated only → we don't need it (name+description suffice); revisit
  if Codex UX wants display metadata.
- Gemini: repo-nested skill's ambient access to sibling `shared/` inferred from [issue #15868](https://github.com/google-gemini/gemini-cli/issues/15868),
  not doc-stated → **smoke-test on first dogfood** (in the checklist).
- Spec-Kit manifest field names reconstructed via summarization → we copy the mechanism, not the field names.
