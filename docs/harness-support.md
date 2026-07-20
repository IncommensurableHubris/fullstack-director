# Harness support — verified discovery paths, the vendor CLI, and the dogfood smoke checklist

> Layer-A reference: how the canonical `.agents/skills/` + root `shared/` reach each AI harness, and how the
> framework deploys into a **consumer project**. Discovery facts below were **live-verified 2026-07-12** (three
> research agents, official sources — full citations in `_artifacts/wsb-vendor-research.md`); re-verify against
> release notes when it matters — this table records what was researched, not a live contract.

## The three supported harnesses (verified 2026-07-12)

| Harness | Discovery (precedence) | Invocation | Notes for this framework |
|---|---|---|---|
| **Claude Code** | enterprise → `~/.claude/skills/` → project **`.claude/skills/`** → plugins. **Does NOT discover `.agents/skills/`** | auto (description) or `/skill-name` | needs the physical `.claude/skills/` copy (the vendored duplicate / this repo's committed bridge); `.claude/agents/fsd-*.md` gives 03/05/07 real subagents; listing truncates description+when_to_use at 1,536 chars |
| **OpenAI Codex CLI** | repo **`.agents/skills/`** (CWD→root) → `~/.agents/skills` + legacy `~/.codex/skills` → `/etc/codex/skills` | `$skill-name` or implicit | the canonical tree works as-is; parses only `name`+`description`; `.agents/` is **read-only** under the default sandbox (fine — skills write to project paths, never into `.agents/`) |
| **Gemini CLI** | built-in → extensions → user (`~/.gemini/skills` \| `~/.agents/skills`) → workspace (`.gemini/skills` \| **`.agents/skills`**); within a tier `.agents/skills` **wins** | **model-driven only**: the `activate_skill` tool + a user consent prompt — no user-typed `/skill-name` | the canonical tree works as-is (skills default-on since v0.26.0, 2026-01); descriptions carry the full trigger weight — ours embed "Use when the user says…" phrases |

**Consequence (the design pivot):** one canonical `.agents/skills/` copy serves **Codex + Gemini**; only Claude
Code needs a duplicate. SKILL.md needs **no per-harness variants** — ours are spec-minimal (`name` +
`description` ≤1024, per [agentskills.io/specification](https://agentskills.io/specification); `name` == the
directory name). **No symlinks anywhere** (win32 + Codex #8369 + Claude #25367 — real-copy only).

Standards: `SKILL.md` per [agentskills.io](https://agentskills.io/specification) · `AGENTS.md` per
[agents.md](https://agents.md).

## Instructions files (verified 2026-07-12) — how the Constitution projection reaches each harness

In a consumer, `00-discovery` emits the project's **`AGENTS.md`** (a generated view of the spine Constitution)
plus two **one-line bridges** (create-if-absent, never overwriting a user's file):

| Harness | Native file | Reads AGENTS.md natively? | The bridge |
|---|---|---|---|
| **Codex CLI** | `AGENTS.md` | **Yes** — no bridge needed | — (note: combined instructions cap `project_doc_max_bytes` defaults to **32 KiB** — the projection stays lean) |
| **Claude Code** | `CLAUDE.md` | **No** ("Claude Code reads CLAUDE.md, not AGENTS.md" — official docs; #6235/#31005 open) | `CLAUDE.md` line 1 = **`@AGENTS.md`** — the **officially recommended** import pattern (max 4 hops); `/status` owns its `## Current State` section |
| **Gemini CLI** | `GEMINI.md` | **No** (default; configurable) | `GEMINI.md` = **`@./AGENTS.md`** (the Memory Import Processor; use the explicit `./` prefix). **Zero-file alternative:** project-committable `.gemini/settings.json` → `{"context": {"fileName": ["AGENTS.md", "GEMINI.md"]}}` (the official docs' own example names AGENTS.md). Verify either with `/memory show` (a closed bug, #19872, once claimed the key was ignored) |

- **⚠ Gemini CLI access (2026-06-18):** consumer access (free/Pro/Ultra personal login) was shut down; the CLI
  remains fully supported **via paid Gemini API keys / Gemini Enterprise / Code Assist Standard-Enterprise**
  (releases continue — v0.50.0, 2026-07-08). Google's consumer replacement (Antigravity CLI) is a **different,
  unevaluated product**. Budget a paid key for the Gemini dogfood leg.
- **Skip `claude /init` in consumers.** `/init` *paraphrases* an existing AGENTS.md into CLAUDE.md — a second home
  for Constitution facts and a drift risk. The line-1 `@AGENTS.md` import keeps **one home**; the framework emits
  it for you.

## Deployment — `tools/vendor.py` (replaces the manual recipe)

```
python tools/vendor.py sync  --target <consumer-root>    # vendor/refresh a consumer project
python tools/vendor.py check --target <consumer-root>    # read-only drift check (exit 1: names every file)
python tools/vendor.py --self-test                        # hermetic cases + a real-tree emission (session-close suite)
```

> **The master repo commits no `.claude/skills` bridge** (decision 2026-07-12): the seat skills are engineered to
> auto-trigger on phrases like "new project" / "plan the build", which framework-development conversations use
> constantly *about the framework* — a committed bridge misfires them. The SDLC chain runs in **consumer** repos
> only; `sync --self` exists as an optional, gitignored local convenience, and the vendor self-test's real-tree
> case is the standing emission guard.

`sync` emits: runtime-only `.agents/skills/<seat>/` (never `evals/`) · the byte-identical `.claude/skills/` copy ·
`shared/` at the consumer root (incl. `feedback-loop.md`) · `.claude/agents/fsd-*.md` · a seed-once
`docs/framework-feedback.md` ledger · `.director/vendor-manifest.json` (source commit + per-file EOL-normalized
SHA-256) · provenance README + `linguist-generated` .gitattributes in each managed root. It **never** emits this
repo's `AGENTS.md`/`CLAUDE.md` (reserved in a consumer for the Layer-B generated views: `00-discovery` emits the
project's `AGENTS.md`; `status` writes `CLAUDE.md § Current State`). A locally-modified vendored file is
**skipped and reported** (exit 2; `--force` overwrites) — fixes flow master-first per `shared/feedback-loop.md`.

**Update flow:** triage the consumers' feedback ledgers in the master → land fixes (+ eval cases / doctrine
lines) → tag `vendor/YYYY-MM-DD` → `sync --target` each consumer → mark ledger entries `resolved-in <sha>`.

## Dogfood smoke checklist (run per harness, first session in a freshly-vendored consumer)

1. **Gemini CLI — `shared/` ambient access** *(the one inferred-not-documented fact — check it FIRST)*: activate
   any skill (ask for its verb), then have it read `shared/spine-boundary.md`. Expected: reads without an access
   error. If blocked: file an FB entry (severity `blocks-gate`) — the fallback is bundling `shared/` per-skill.
2. **Listing:** Claude `/skills` (or type `/00-`) · Codex `/skills` · Gemini `/skills list` — all 10 seats appear.
3. **Invocation:** Claude `/00-discovery` · Codex `$00-discovery` · Gemini: phrase the ask ("intake this spec /
   start discovery") and confirm `activate_skill` proposes `00-discovery` (consent prompt shows its directory).
3b. **Bridges (post-discovery):** Claude — fresh session, ask "what are this project's non-negotiables?"
   (the answer must come from the imported Constitution via `CLAUDE.md` line-1 `@AGENTS.md`) · Gemini —
   `/memory show` lists AGENTS.md content (tests `@./AGENTS.md`; if it misbehaves, fall back to the
   `context.fileName` settings key) · Codex — native AGENTS.md pickup, combined size < 32 KiB.
4. **A real read-chain:** run `/status` (or its Gemini phrasing) on the empty consumer — expected: P0 route
   ("no spine — start `/00-discovery`"), proving SKILL.md → references → `shared/` resolution end-to-end.
5. **Subagents (Claude only):** confirm `fsd-reviewer` / `fsd-reconciler` / `fsd-owasp-reader` appear as agent
   types; 03/05/07 will spawn them per `shared/subagent-protocol.md`.
6. Any friction → say **"framework friction: …"** — the vendored **`feedback` skill** writes the SHA-stamped FB
   entry into `docs/framework-feedback.md` at the moment it happens (never hand-written; seats also self-report a
   framework-caused HALT/BLOCK — `shared/feedback-loop.md` § Activation).

## Appendix — the manual recipe (what `sync` automates)

1. Copy each skill **runtime-only** (`SKILL.md` + `templates/` + `references/`, never `evals/`) into
   `.agents/skills/<NN-role>/` **and** `.claude/skills/<NN-role>/`.
2. Copy `shared/` to the target repo root; copy `.claude/agents/fsd-*.md`.
3. Do **NOT** copy this repo's `AGENTS.md` / `CLAUDE.md` (reserved for the Layer-B generated views).
4. Start with `/00-discovery`; run `/status` anytime for the derived state + next command.
