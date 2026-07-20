# Workstream B — Vendor CLI + Claude bridge + subagent files + the dogfood feedback loop (design record)

> **Approved 2026-07-12** (user, at the design gate; scope confirmed "all three pieces", harnesses narrowed to
> **Claude Code · OpenAI Codex CLI · Gemini CLI**). Evidence base: `_artifacts/wsb-vendor-research.md` (three
> Sonnet research agents, live-verified citations). This closes the long-deferred packaging item
> (`shared/artifact-map.md` § Deferred; the coherence review's "cost is rising" flag) and adds the piece the
> ecosystem itself lacks: a disciplined dogfood→distill→upstream loop.

## Problem

The framework is complete and eval-green but **unusable in place**: Claude Code doesn't discover `.agents/skills/`
(no `/00-discovery` while developing this repo), skills 03/05/07 fall back to "fresh top-level invocation" instead
of real subagents, and deploying to a consumer project is a manual 4-step recipe (`docs/harness-support.md`) with
no version stamp, no drift detection, and no route for dogfooding learnings to flow back upstream.

## Research-driven simplification (the design's pivot)

Live verification (2026-07-12) shows **Codex CLI and Gemini CLI both natively discover repo `.agents/skills/`**
(Gemini even prefers it over `.gemini/skills` on name collisions), and our SKILL.md files are already spec-minimal
(`name` + `description` ≤1024 — commit `877301f` is load-bearing). So there is **no per-harness content
templating**: the generator's job is *placement, filtering, provenance* — not transformation. Only Claude Code
needs a physical duplicate (`.claude/skills/`); symlinks are ruled out (win32 + Codex #8369 + Claude #25367).

## ① The tool — `tools/vendor.py` (stdlib Python 3.8+, three verbs)

- **`sync --target <consumer-root> [--source-ref <sha>]`** — vendor/refresh the framework into a consumer repo.
- **`sync --self`** — dogfood #0: refresh THIS repo's own `.claude/skills/` bridge from `.agents/skills/`.
- **`check --target <consumer-root> | --self`** — read-only drift detection, **exit 1 on drift** (the cruft
  pattern): (a) consumer-side — re-hash managed files vs the manifest; (b) upstream-side — manifest
  `source_commit` vs the framework repo HEAD (passed via `--upstream <path>`; no network).
- **`--self-test`** — staged temp trees; ideal passes, each degenerate fires (the repo's grader-first DNA).

**Sync semantics (Spec-Kit-validated):** delete-and-recreate each managed `dest_path`, EXCEPT any file whose
current hash ≠ the hash *we last wrote* (per the previous manifest) — that file is **locally modified: skip +
report** (never clobber; `--force` overrides). Write the new manifest only after a successful sync. Idempotent:
a second sync is a no-op.

## ② What sync emits (per consumer)

| # | Emission | Serves | Notes |
|---|----------|--------|-------|
| 1 | `.agents/skills/<seat>/` — **runtime-only**: `SKILL.md` + `references/` + `templates/`, **never `evals/`** | Codex + Gemini (native discovery) | 10 seats, byte-identical to canonical |
| 2 | `.claude/skills/<seat>/` — byte-identical copy of #1 | Claude Code | no `.agents/` discovery exists (issue #31005) |
| 3 | `shared/*.md` → consumer root | all seats' repo-root-relative reads | includes the new `shared/feedback-loop.md` |
| 4 | `.claude/agents/fsd-{reviewer,reconciler,owasp-reader}.md` | Claude Code subagent tier (03/05/07) | canonical home = this repo's own `.claude/agents/` |
| 5 | `docs/framework-feedback.md` — the seeded feedback ledger | the loop | **created once, never overwritten** |
| 6 | `.director/vendor-manifest.json` + a provenance `README.md` in each managed root + `.gitattributes` `linguist-generated` entries | provenance + drift | Chromium/Go conventions |

**Never emitted:** this repo's `AGENTS.md` / `CLAUDE.md` (reserved for the consumer's Layer-B generated views —
recipe rule 3, now enforced by code), `evals/`, `docs/eval-methodology/`, `_artifacts/`.

**Manifest schema** (`.director/vendor-manifest.json`): `generator` (`fullstack-director-vendor`) ·
`generator_version` · `source_repo` · `source_commit` (full SHA — the load-bearing pin) · `source_ref` ·
`vendored_at` (ISO-8601) · `items[] {name, kind ∈ skill|shared|agents|ledger, source_path, dest_path,
files {relpath: "sha256:…"}}`. No in-file stamps — emitted files stay **byte-identical to canonical** (provenance
lives in the manifest + README; local-modification is *derived* by re-hashing, never hand-authored).

## ③ The Claude bridge (this repo) — `sync --self`

Emissions #2 (from #1's canonical source, runtime-only) into this repo's own `.claude/skills/`, **committed** like
a lockfile (a fresh clone works in Claude Code immediately), guarded by **`vendor check --self` joining the
session-close validators** (the WS6 precedent) so bridge↔canonical parity can never silently drift. The
gitignore's existing `.claude/skills/*-workspace/` rule is unaffected. Editing rule: **canonical only** —
`.agents/skills/` is where skills are edited; the bridge is regenerated, never hand-edited.

## ④ The subagent definitions — `.claude/agents/fsd-*.md` (canonical here, vendored to consumers)

Per `shared/subagent-protocol.md` (the spawn branch, now concretely wired; the `skills:` preload field is
confirmed to exist):

| File | Backs | Tools | Preload |
|------|-------|-------|---------|
| `fsd-reviewer.md` | 05's Pass-2 semantic reviewer (seeded with handoff + spec-slice paths; returns verdict + attestation) | read-only (Read/Grep/Glob) + Bash (re-run oracles) | `05-reviewer` |
| `fsd-reconciler.md` | 03's Reconcile judgment pass (realization + declarations in; Tier rows + attestation out) | read-only | `03-architect` |
| `fsd-owasp-reader.md` | 07's panel readers (one definition; each spawn gets its area-slice via prompt; cap 3–5) | read-only + Bash (deterministic scanners) | `07-security` |

`shared/subagent-protocol.md` gains one line naming these files (the "where the harness supports subagents" branch
becomes concrete). **No skill body changes** — the protocol already says "use a `subagent_type` backed by a
`.claude/agents/*.md` definition".

## ⑤ The feedback loop — `shared/feedback-loop.md` (one contract, vendored to both sides)

1. **Capture (consumer, at the point of friction):** append an entry to `docs/framework-feedback.md` — `date ·
   framework_sha (from the manifest) · harness ∈ claude-code|codex|gemini-cli · seat · expected · actual · repro ·
   severity ∈ blocks-gate|wrong-but-recoverable|friction-only · artifact pointer`. Entries are **append-only /
   immutable** (supersede, never edit — the ADR rule; never summarize the ledger — the context-collapse guard).
2. **Upstream-first:** vendored files are never edited in the consumer. An emergency local patch is permitted but
   MUST be ledgered — and is mechanically visible anyway (`vendor check` hash drift). Fixes land in the master
   repo and arrive by re-vendor.
3. **Triage ritual (master, batched — before each re-vendor):** read the consumers' ledgers; dispose EVERY entry:
   **fix / eval-case / doctrine-line / defer (with a revisit trigger)** — logged append-only in
   `_artifacts/dogfood-triage.md`. The durability rule: **every `fix` terminates in an eval case (ONE
   representative per failure cluster — anti-bloat) or a dated doctrine line** in the owning skill's
   `references/` or `shared/`.
4. **Re-vendor (batched, tag-gated):** after triage lands, tag the master (`vendor/YYYY-MM-DD`), `sync` each
   consumer as one atomic act, mark its ledger entries `resolved-in <sha>`. Never drip-vendor (erodes the stamp).

The loop is our own amendment-protocol pattern (tiered dispositions + structured append-only log) applied to the
framework itself. Research confirms no published post-deployment skill-iteration process exists — this is ahead of
the ecosystem, deliberately.

## ⑥ Verification (grader-first)

`vendor.py --self-test` (staged temp source + consumer trees): **ideal** — full sync then: runtime-only holds (no
`evals/` anywhere under managed paths) · `.agents`↔`.claude` byte-parity · `shared/` + agents + ledger + manifest
present · manifest hashes == disk · `AGENTS.md`/`CLAUDE.md` NOT emitted · second sync = no-op · `check` exits 0.
**Degenerates** — (a) consumer-modified file → re-sync skips + reports (and `--force` clobbers); (b) `check` after
a local edit → exit 1 naming the file; (c) `check` after upstream moves → exit 1; (d) a planted `evals/` dir in a
source skill never reaches the consumer; (e) ledger present → sync leaves it untouched. Wired into
`validate_script.py`'s session-close block + `check --self` as the standing bridge guard.

**Live validation = the dogfooding itself:** a per-harness smoke checklist lands in `docs/harness-support.md`
(open each harness in a vendored repo → skills listed/activatable → one skill reads `shared/` successfully — the
Gemini ambient-access uncertainty is smoke item #1).

## ⑦ Docs + exit

`docs/harness-support.md` rewritten: the **verified** 3-harness discovery table (research findings, incl. Gemini's
`activate_skill` consent model + Codex's read-only `.agents/` sandbox note) + "deploy = `python tools/vendor.py
sync --target <repo>`" replacing the manual recipe (kept as an appendix). `shared/artifact-map.md`: § Deferred
(CLI generator + dev bridge + subagent files) → **built**; new rows (`tools/vendor.py`, `.claude/agents/fsd-*`,
`shared/feedback-loop.md`, and Layer-B rows for `.director/vendor-manifest.json` + `docs/framework-feedback.md`).
`README.md` status line. `_artifacts/deferred-backlog.md`: packaging item → done.

## Delta — §③ reversed at user review (2026-07-12, same day)

**The master repo commits NO `.claude/skills` bridge.** §③ as designed (committed bridge + `check --self`
session-close parity row) was built, then reversed when the user clarified this repo's purpose: it *only develops
the framework* and never runs the SDLC chain on itself. The decisive argument (observed live, minutes after the
bridge commit): the seat skills' descriptions are engineered to auto-trigger on phrases framework-development
conversations use constantly *about the framework* ("new project", "plan the build", "review sprint N") — a
committed bridge injects all 10 into every dev session here and invites misfires. It also doubled every skill
edit (canonical + 73-file mirror churn). Resolution: `.claude/skills/` + `.director/` **gitignored** in the
master; `sync --self` demoted to an optional local convenience; the parity guard replaced by a **stronger**
standing check — self-test case 10 syncs the REAL tree into a temp consumer and asserts the full EMIT map
(seats + parity + no-evals + fsd agents + shared + no Layer-A) on true content. Consumers are unaffected: they
always get both trees, where the skills SHOULD auto-trigger. `.claude/agents/fsd-*.md` stay committed here — they
are canonical vendor source, inert without the bridge.

## Scope / non-goals

- **No copier/cruft/vendir/npm dependency** — mechanics stolen, runtimes rejected (stdlib-only convention).
- **No Claude plugin-marketplace channel** — plugins are cached outside the repo and cannot resolve repo-root
  `shared/` reads (rejected, not deferred).
- **No `.gemini/` or `.codex/` emissions** — `.agents/skills/` serves both natively (re-verify at each re-vendor
  against release notes; the table records what was researched 2026-07-12).
- **No symlinks, anywhere** (win32 + both harnesses' issues).
- **Consumer-side hotfix tooling** (3-way merge à la copier) — YAGNI at skip-and-report + upstream-first scale.
