# Workstream B — Vendor CLI + Claude bridge + subagent files: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: `superpowers:executing-plans` (inline — the tasks are
> contract-coupled around one tool; the WS6 precedent). First read `_artifacts/wsb-vendor-design.md` (approved
> 2026-07-12) + `_artifacts/wsb-vendor-research.md` (the evidence), then this plan. Steps track with `- [ ]`.
> **Grader-first every task; never push.**

**Goal:** One stdlib-Python command that vendors the framework (runtime-only, version-stamped, drift-guarded)
into consumer repos for Claude Code + Codex + Gemini CLI, plus this repo's own committed Claude bridge, the
`.claude/agents/` subagent definitions, and the vendored dogfood→upstream feedback-loop contract.

**Architecture:** `tools/vendor.py` (sync/check/--self-test) does placement + filtering + provenance — no content
templating (SKILL.md is already cross-harness portable). One canonical `.agents/skills/` emission serves
Codex+Gemini; a byte-identical `.claude/skills/` copy serves Claude Code. Per-file SHA-256 manifest
(EOL-normalized) makes local modification and upstream drift pure hash comparisons.

**Tech Stack:** Python 3.8+ stdlib only (`argparse`, `hashlib`, `json`, `shutil`, `pathlib`, `subprocess` for
`git rev-parse` provenance, `tempfile` for the self-test). Markdown content files. No new dependencies.

## Global Constraints (apply to every task)

- **SEATS** (locked, 10): `00-discovery 01-planner 02-designer 03-architect 04-builder 05-reviewer 06-release
  07-security 08-refactor status`.
- **RUNTIME set per seat** (locked): `SKILL.md` + `references/**` + `templates/**` — **never** `evals/`,
  `__pycache__/`, `*.pyc`.
- **EMIT map** (locked, design §②): `.agents/skills/<seat>/` (runtime) · `.claude/skills/<seat>/` (byte-identical
  copy) · `shared/*.md` → consumer root · `.claude/agents/fsd-{reviewer,reconciler,owasp-reader}.md` ·
  `docs/framework-feedback.md` (seed once, never overwrite) · `.director/vendor-manifest.json` · a provenance
  `README.md` + `.gitattributes` (`* linguist-generated=true` + `**/* linguist-generated=true`) in each managed
  root (`.agents/skills/`, `.claude/skills/`). **Never emitted:** master `AGENTS.md`/`CLAUDE.md`, `evals/`,
  `docs/eval-methodology/`, `_artifacts/`.
- **`--self` mode** = emissions #2-bridge only (`.agents/skills` → this repo's `.claude/skills`) + the manifest;
  shared/ + agents are already canonical here; no ledger in the master.
- **Manifest** (locked schema): `{"generator": "fullstack-director-vendor", "generator_version": "1.0.0",
  "source_repo": <git remote or path>, "source_commit": <full sha>, "source_ref": <branch>, "vendored_at":
  <ISO-8601 UTC>, "hash_normalization": "crlf-to-lf", "items": [{"name", "kind": "skill|shared|agents|ledger",
  "source_path", "dest_path", "files": {<relpath>: "sha256:<hex>"}}]}`.
- **Hashing** (locked): `sha256(content.replace(b"\r\n", b"\n"))` — EOL-insensitive (the Windows-EOL grader-churn
  lesson); copies are done in **bytes** (`shutil.copyfile`).
- **Drift semantics** (locked): `check` exits 1 listing (a) **consumer drift** — on-disk dest hashes ≠ manifest;
  (b) **upstream drift** — current master canonical-source hashes ≠ manifest. `source_commit` is provenance
  metadata only, never the drift signal (content hashes are — no false-stale on unrelated commits).
- **Sync protection** (locked, Spec-Kit semantics): a dest file whose current hash ≠ the previous manifest's hash
  is **locally modified → skip + report** (exit 2 with the list); `--force` overwrites. Manifest written only
  after a successful sync. Second sync = no-op.
- Conventional commits; small + atomic; **never push**.

---

### Task B.1 — `shared/feedback-loop.md` (the loop's single home)

**Files:** Create `shared/feedback-loop.md`.
**Interfaces:** Produces the file `vendor.py` ships in its `shared` item (B.3) and the entry format the triage
ritual (master-side) consumes.

- [ ] **Step 1: Write the protocol file.** Sections (from design §⑤, each with the research citation baked into
  prose): **Capture** — the ledger `docs/framework-feedback.md`, append-only/immutable entries, the exact entry
  template:

  ```markdown
  ### FB-NNN · <date> · <one-line title>
  - **framework:** <source_commit from .director/vendor-manifest.json>
  - **harness:** claude-code | codex | gemini-cli
  - **seat:** <00-discovery … status | shared | vendor>
  - **severity:** blocks-gate | wrong-but-recoverable | friction-only
  - **expected:** <what the framework/skill should have done>
  - **actual:** <what happened>
  - **repro:** <minimal steps / the command>
  - **artifact:** <path to transcript/diff/spine file>
  - **status:** open | superseded-by FB-NNN | resolved-in <master sha>
  ```

  **Upstream-first** — vendored files are never edited in a consumer; an emergency local patch MUST get a ledger
  entry (severity blocks-gate) and is mechanically visible to `vendor.py check` regardless. **Triage (master,
  batched before each re-vendor)** — every entry disposed exactly once: `fix / eval-case / doctrine-line /
  defer(<revisit trigger>)`, logged append-only in `_artifacts/dogfood-triage.md`; the durability rule: **every
  `fix` terminates in an eval case (ONE representative per failure cluster) or a dated doctrine line**. **Re-vendor**
  — batched + tag-gated (`vendor/YYYY-MM-DD`), one atomic `sync` per consumer, ledger entries marked
  `resolved-in <sha>`. **Anti-patterns** list (the 9 from research §C, one line each).
- [ ] **Step 2: Cross-check** — the entry template's field names match B.3's seeded-ledger constant verbatim.
- [ ] **Step 3: Commit** — `docs(shared): feedback-loop protocol — the dogfood→distill→upstream contract`.

### Task B.2 — `.claude/agents/fsd-*.md` + the protocol pointer

**Files:** Create `.claude/agents/fsd-reviewer.md`, `.claude/agents/fsd-reconciler.md`,
`.claude/agents/fsd-owasp-reader.md`; Modify `shared/subagent-protocol.md` (one sentence in § Spawn pattern).
**Interfaces:** Produces the three files B.3 emits under its `agents` item. Frontmatter contract (verified: the
`skills:` preload field exists): `name`, `description`, `tools` (allowlist), `skills` (preload array).

- [ ] **Step 1: Write the three definitions.** Shape for each (full frontmatter + a short body restating the
  seat's I/O contract from `shared/subagent-protocol.md` — seed, return, and the attestation line):
  - `fsd-reviewer`: tools `Read, Grep, Glob, Bash` (re-runs oracles; writes nothing — the QA report is written by
    the 05 seat); preloads `05-reviewer`; body = the build→reviewer I/O contract (seeded ONLY with the handoff
    path + spec-slice paths; returns verdict + `inputs: [handoff, spec slice]; build conversation: not provided`).
  - `fsd-reconciler`: tools `Read, Grep, Glob`; preloads `03-architect`; body = the reconciler contract
    (realization + slice declarations in; Tier-classified amendment rows + source_quotes + attestation out).
  - `fsd-owasp-reader`: tools `Read, Grep, Glob, Bash` (deterministic scanners); preloads `07-security`; body =
    the reader contract (ONE area-slice per spawn via the prompt; findings = `file:line + source_quote +
    proposed_severity`; blind to other readers; never edits code; cap 3–5 concurrent).
- [ ] **Step 2: Add the pointer** to `shared/subagent-protocol.md` § Spawn pattern: after "use a `subagent_type`
  backed by a `.claude/agents/*.md` definition", name the three concrete files.
- [ ] **Step 3: Verify** — frontmatter parses (yaml-shaped), names match filenames, each preloaded skill exists.
- [ ] **Step 4: Commit** — `feat(claude): fsd-{reviewer,reconciler,owasp-reader} subagent definitions`.

### Task B.3 — `tools/vendor.py` + `--self-test` (the core; grader-first)

**Files:** Create `tools/vendor.py` (single file, ~350 lines). Modify
`docs/eval-methodology/integration/validate_script.py` (two session-close rows).
**Interfaces:** Consumes B.1/B.2's files as emission content. Produces: CLI verbs `sync|check` with
`--target <path> | --self`, `--force`, `--self-test`; module functions `norm_hash(data: bytes) -> str`,
`runtime_files(seat_dir: Path) -> list[Path]`, `build_items(master: Path, target: Path, self_mode: bool) ->
list[dict]`, `do_sync(master, target, self_mode, force) -> int`, `do_check(master, target, self_mode) -> int`.

- [ ] **Step 1: Write the tool.** Module layout (locked): constants (SEATS, RUNTIME_DIRS = ("references",
  "templates"), EXCLUDE = ("evals", "__pycache__"), AGENTS_FILES, LEDGER_SEED string using B.1's exact template,
  README + .gitattributes templates) → helpers (`norm_hash`, `read_manifest`, `git_provenance(master)` via
  `git rev-parse HEAD` / `--abbrev-ref`, tolerant of failure → `"unknown"`) → `build_items` (walk canonical
  sources; per Global-Constraints EMIT map; self_mode = bridge item only) → `do_sync`: read previous manifest →
  compute locally-modified set (dest hash ≠ previous manifest hash) → if any and not force: print + **exit 2**,
  touch nothing → else delete-and-recreate each managed dest_path (but **never** delete the ledger; seed it only
  if absent) → byte-copy files → write README + .gitattributes into the two managed skill roots → write manifest
  (atomic: temp + replace) → print summary, exit 0 → `do_check`: consumer drift + upstream drift lists (per the
  locked semantics) → exit 1 if either non-empty, naming every file → `self_test()` (Step 2) → `main()` argparse.
- [ ] **Step 2: Write the self-test IN the same file** (staged hermetic trees under `tempfile`, the
  check_release/S18 precedent). Build a mini master: 2 seats (`00-discovery` with SKILL.md + references/a.md +
  templates/b.md + **a planted `evals/trap.py`**; `status` with SKILL.md), `shared/{x.md,y.md}`,
  `.claude/agents/fsd-reviewer.md`, an `AGENTS.md` + `CLAUDE.md` at master root (the must-not-ship plants), a git
  repo (`git init` + one commit; skip provenance assertions gracefully if git is unavailable). Cases (each prints
  a PASS/FAIL row; ALL GOOD / exit 1):
  1. `sync` ideal → all EMIT-map paths exist at target; **no `evals/` or `trap.py` anywhere under managed paths**;
     `AGENTS.md`/`CLAUDE.md` absent at target root; ledger seeded with the FB template header.
  2. `.agents/skills/**` ↔ `.claude/skills/**` **byte-identical** (walk + compare).
  3. Manifest: parses; every `files` hash == re-hashed disk content; `source_commit` is 40-hex (or "unknown"
     without git).
  4. **Idempotence**: second `sync` → exit 0 and zero byte changes (re-hash before/after).
  5. **Local-mod protection**: edit one vendored dest file → `sync` exits 2 naming it, file untouched;
     `sync --force` → exits 0, file restored to canonical.
  6. **check** consumer drift: edit a dest file → exit 1 naming it. Restore.
  7. **check** upstream drift: edit the mini-master's canonical SKILL.md → exit 1 naming it.
  8. **Ledger immunity**: append a fake FB entry to the ledger → `sync` again → entry survives.
  9. `--self` mode on the mini master → ONLY `.claude/skills/` + manifest written (no shared/agents/ledger items).
- [ ] **Step 3: Run** `python tools/vendor.py --self-test` → ALL GOOD, exit 0.
- [ ] **Step 4: Wire the session-close rows** into `validate_script.py` (after the WS6 block):
  `("vendor-self-test", [sys.executable, VENDOR, "--self-test"])` and
  `("vendor-bridge-parity", [sys.executable, VENDOR, "check", "--self"])` — the second stays green only while the
  committed bridge matches canonical (it is added in this task but B.4 creates the bridge; ORDER: add the
  bridge-parity row **in B.4** to keep every commit green. In THIS task add only `vendor-self-test`).
- [ ] **Step 5: Run** `python docs/eval-methodology/integration/validate_script.py` → ALL GOOD.
- [ ] **Step 6: Commit** — `feat(tools): vendor.py — sync/check/self-test vendoring CLI`.

### Task B.4 — the committed Claude bridge (dogfood #0)

**Files:** Generated: `.claude/skills/<seat>/**` (10 seats, runtime-only) + `.director/vendor-manifest.json`.
Modify: `validate_script.py` (+ the `vendor-bridge-parity` row), `.gitignore` (nothing to change — verify
`.claude/skills/*-workspace/` still covers eval workspaces and does not exclude the bridge).
**Interfaces:** Consumes B.3's `sync --self`.

- [ ] **Step 1: Run** `python tools/vendor.py sync --self` → summary lists 10 seats; exit 0.
- [ ] **Step 2: Verify** — `python tools/vendor.py check --self` → exit 0; spot-check: no `evals/` under
  `.claude/skills/`; `git status` shows only `.claude/skills/**`, `.director/`, and the managed-root README/
  .gitattributes files.
- [ ] **Step 3: Add the `vendor-bridge-parity` row** to validate_script.py; run the full validator → ALL GOOD.
- [ ] **Step 4: Negative probe (no commit):** edit one canonical reference file → `check --self` exits 1 naming
  it → revert → exit 0 again. (Proves the standing guard bites before we rely on it.)
- [ ] **Step 5: Commit** — `feat(bridge): committed .claude/skills dev bridge via vendor sync --self` (add
  `-f` not needed — verify nothing under `.claude/skills/` is ignored).

### Task B.5 — docs: verified harness table + CLI recipe + map/status updates

**Files:** Modify `docs/harness-support.md` (rewrite), `shared/artifact-map.md` (§ Deferred + new rows),
`README.md` (status ¶), `_artifacts/deferred-backlog.md` (packaging item → done).

- [ ] **Step 1: Rewrite `docs/harness-support.md`:** the verified 3-harness table (from
  `wsb-vendor-research.md` §A — discovery precedence, invocation model incl. Gemini's `activate_skill` consent +
  Codex's read-only `.agents/` sandbox, constraints, source links + verified-date 2026-07-12); deployment =
  `python tools/vendor.py sync --target <consumer-root>` (+ `check`, `--force`, the update flow); the **dogfood
  smoke checklist** (per harness: skills listed/activatable? invoke 00-discovery — Gemini via description match;
  one skill reads consumer-root `shared/` — the Gemini ambient-access uncertainty is item #1); the manual recipe
  kept as an appendix ("what sync automates"); the feedback pointer (`shared/feedback-loop.md`).
- [ ] **Step 2: `shared/artifact-map.md`:** § Deferred — CLI generator + dev bridge + subagent files → **built**
  (leave 5.5b/6.6b/model-migration entries); Layer-A rows: `tools/vendor.py`, `.claude/agents/fsd-*.md`,
  `.claude/skills/` (generated bridge — "regenerate via sync --self, never hand-edit"), `shared/feedback-loop.md`;
  Layer-B rows: `.director/vendor-manifest.json` (gen) + `docs/framework-feedback.md` (maintained ledger, consumer).
- [ ] **Step 3: `README.md`** status ¶: packaging shipped (vendor CLI + bridge + subagent files + feedback loop);
  deferred list shrinks to the two trigger-gated live runs. **`deferred-backlog.md`**: packaging row → ✅ done
  (2026-07-12), add the standing "dogfood triage before each re-vendor" ritual pointer.
- [ ] **Step 4: Run the full validator suite** (all four + the new vendor rows) → ALL GOOD.
- [ ] **Step 5: Commit** — `docs(harness): verified tri-harness table + vendor recipe + map/status updates`.

### Task B.6 — exit: continuation handoff

**Files:** Modify `_artifacts/next-session-continuation.md`.

- [ ] **Step 1:** Mark §4 DONE (built: vendor CLI · bridge · fsd-* agents · feedback loop; commits listed). New
  head-of-agenda: **create the 3 dogfood consumer repos** → `sync --target` each → run the smoke checklist per
  harness (Gemini `shared/`-access first) → build real projects → ledger entries → first triage ritual.
- [ ] **Step 2:** Full validator sweep once more; `git status` clean; **Commit** — `docs: workstream B complete —
  hand off to dogfooding`.

## Self-review (done at write time)

- **Spec coverage:** design §① → B.3 · §② EMIT map → B.3 (asserted in self-test 1–3, 9) · §③ bridge → B.4 ·
  §④ agents → B.2 · §⑤ loop → B.1 (+ ledger seed B.3, triage log named in B.1) · §⑥ verification → B.3 self-test
  + B.4 negative probe + validator wiring · §⑦ docs → B.5. No gap.
- **Type consistency:** `do_sync/do_check(master, target, self_mode[, force])` signatures match across B.3/B.4;
  manifest field names identical in Global Constraints, B.3 case 3, and B.1's `framework:` field description;
  exit codes: sync 0/2, check 0/1 — used consistently.
- **Placeholder scan:** none — every task names files, content shape, commands, expected exits, commit message.
- **Order-of-greenness:** bridge-parity validator row deliberately lands in B.4 (after the bridge exists) so every
  commit keeps the suite green.
