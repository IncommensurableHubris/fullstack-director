# Data-architecture Phase 1 — calibrated data eval cases: implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (fresh-session execution per this
> repo's convention) to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Land the grader-first calibrated data eval cases for `03-architect` (DA-T01–T08 checks + `data-modules`/
`data-nogate` fixtures + self-tests) plus the two fold-in fixes (S18 label normalization + convention line; README
`/21` re-record), then run the 2×2 A/B.

**Architecture:** One grader file grows a focused `grade_data_arch` path (the `--case agent` pattern) with a
`_self_test_data` mutation-style bite proof; two beacon-derived fixture trees; doctrine gains exactly one
convention line. Spec (the *what/why*): `_artifacts/data-architecture-phase1-design.md`.

**Tech Stack:** Python 3 (stdlib only — `os re json argparse tempfile shutil`), git worktree, native Agent-tool
Sonnet subagents for arms.

## Global Constraints

- **Teeth text verbatim** — DA-T01–T08 are cited by ID; never paraphrased into prompts, never restated in case
  prompts (or the eval tests the prompt, not the doctrine).
- **No product names in grader REQUIRED tokens.** Self-test tree content and the S18 degenerate MAY be
  real-output-shaped (`BGE-M3 (embedding model)` is deliberately so); `check()` pass conditions must key on
  structure/generic tokens only.
- **Grader-first order is absolute:** grader + self-tests green → real-output validation → fixtures → arms.
- **Writes to the calibrated tree** only under `.agents/skills/03-architect/evals/**` + the ONE line in
  `shared/live-source-verification.md`. Run workspaces live under gitignored `_artifacts/skills-eval/**`
  (`git add -f` for run records that must survive).
- **Windows hygiene:** all file writes `encoding="utf-8", newline="\n"`; a `.gitattributes` (`* text=auto eol=lf`)
  in each run workspace; grader invoked as `python .agents/skills/03-architect/evals/check_architecture.py`.
- **No push (the repo has zero remotes). Never merge to `main` without asking the user.** Commit per task on the
  worktree branch with `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.
- Arms are **native Agent-tool subagents** (general-purpose, `model: sonnet`), sequential, one per message — the
  smoke recipe, not the CLI scripts.

---

### Task 1: Worktree setup

**Files:** none (git plumbing only).

- [ ] **Step 1: Create the worktree + branch off `main`**

```bash
cd /d/_CODE/2026-06-29_fullstack-director
git worktree add .claude/worktrees/data-eval-cases -b worktree-data-eval-cases main
cd .claude/worktrees/data-eval-cases
git status --short --branch && git log --oneline -1
```
Expected: `## worktree-data-eval-cases`, clean, HEAD = main's tip (`ad8ae73` or later). All later tasks run from
this worktree root.

- [ ] **Step 2: Sanity — the grader self-test is green pre-change**

```bash
python .agents/skills/03-architect/evals/check_architecture.py --self-test
```
Expected: `ALL GOOD — S18 bites …`, exit 0.

---

### Task 2: S18 label normalization (TDD via the self-test)

**Files:**
- Modify: `.agents/skills/03-architect/evals/check_architecture.py` (`verify_live_techs` ~line 101;
  `grade_verify_live_adr` ~line 322; `_self_test_s18` ~line 637)

**Interfaces:**
- Produces: `verify_live_techs(root) -> set[str]` now returns **normalized lowercase slugs** (trailing
  parenthetical stripped). All later tasks rely on lowercase slugs.

- [ ] **Step 1: Extend `_self_test_s18` with three failing scenarios (RED).** Replace the scenario plumbing so each
scenario carries its own record path, and add the qualified-label + case-mismatch cases. Replace from
`AC_DECL = (` through the `scenarios = [ … ]` list close with:

```python
    AC_DECL = ("# Architecture Constraints\n\n## Verify-live\n\n"
               "- **openclaw:** docs: https://openclaw.dev/docs · source: https://github.com/example/openclaw\n")
    AC_NONE = "# Architecture Constraints\n\n## Stack mandates\n\n- **Datastore:** PostgreSQL 16 (client-server).\n"
    AC_QUAL = ("# Architecture Constraints\n\n## Verify-live\n\n"
               "- **BGE-M3 (embedding model):** docs: https://example.dev/bge · source: https://github.com/example/bge\n")
    AC_UPPER = ("# Architecture Constraints\n\n## Verify-live\n\n"
                "- **BGE-M3:** docs: https://example.dev/bge · source: https://github.com/example/bge\n")
    ADR_CITED = ("# ADR-002: Adopt OpenClaw for the agent loop\n\n"
                 "- **Verified-against:** docs/verification/openclaw.md (openclaw@0.4.2)\n\n"
                 "## Decision Outcome\n\n**Chosen:** OpenClaw, because it is the mandated host framework.\n")
    ADR_UNCITED = ("# ADR-002: Adopt OpenClaw for the agent loop\n\n"
                   "## Decision Outcome\n\n**Chosen:** OpenClaw, because it is the mandated host framework.\n")
    ADR_BGE_CITED = ("# ADR-003: Embedding model\n\n"
                     "- **Verified-against:** docs/verification/bge-m3.md (bge-m3@1.0)\n\n"
                     "## Decision Outcome\n\n**Chosen:** BGE-M3, for one-pass dense+sparse embedding.\n")
    ADR_BGE_UNCITED = ("# ADR-003: Embedding model\n\n"
                       "## Decision Outcome\n\n**Chosen:** BGE-M3, for one-pass dense+sparse embedding.\n")
    RECORD = ("---\nverified_against: openclaw@0.4.2\n---\n\n## Verified claims\n\n"
              "| claim | citation | corrects |\n|---|---|---|\n"
              "| Claw.run(task) is the entry point | https://openclaw.dev/docs#loop | — |\n")
    RECORD_BGE = ("---\nverified_against: bge-m3@1.0\n---\n\n## Verified claims\n\n"
                  "| claim | citation | corrects |\n|---|---|---|\n"
                  "| emits dense and sparse vectors in one pass | https://example.dev/bge#modes | — |\n")

    def build(tmp, ac, adr, record, record_rel):
        def w(rel, s):
            p = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(s)
        w("docs/spec/architecture-constraints.md", ac)
        if adr is not None:
            w("docs/architecture/adr/ADR-002.md", adr)
        if record:
            w(record_rel, record)

    # name, ac, adr, record_text, record_rel, want_passed, want_na
    scenarios = [
        ("ideal (ADR cites a resolving record)", AC_DECL, ADR_CITED, RECORD,
         "docs/verification/openclaw.md", True, False),
        ("degenerate (verify-live ADR, no citation)", AC_DECL, ADR_UNCITED, RECORD,
         "docs/verification/openclaw.md", False, False),
        ("degenerate (citation to a missing record)", AC_DECL, ADR_CITED, None,
         "docs/verification/openclaw.md", False, False),
        ("N/A (no verify-live declared)", AC_NONE, ADR_CITED, RECORD,
         "docs/verification/openclaw.md", True, True),
        ("qualified label links + validates (real-output-shaped)", AC_QUAL, ADR_BGE_CITED, RECORD_BGE,
         "docs/verification/bge-m3.md", True, False),
        ("qualified label FIRES on an uncited ADR", AC_QUAL, ADR_BGE_UNCITED, RECORD_BGE,
         "docs/verification/bge-m3.md", False, False),
        ("uppercase bare label links the lowercase record", AC_UPPER, ADR_BGE_CITED, RECORD_BGE,
         "docs/verification/bge-m3.md", True, False),
    ]
```

And update the loop body's build call + tuple unpack:

```python
    for name, ac, adr, record, record_rel, want_passed, want_na in scenarios:
        tmp = tempfile.mkdtemp(prefix="s18-")
        try:
            build(tmp, ac, adr, record, record_rel)
```

- [ ] **Step 2: Run — confirm exactly the three new scenarios fail**

```bash
python .agents/skills/03-architect/evals/check_architecture.py --self-test
```
Expected: FAIL on `qualified label links…` (got na=True), `qualified label FIRES…` (got na=True), `uppercase bare
label…` (got passed=False); the original four still PASS; exit 1.

- [ ] **Step 3: Fix `verify_live_techs` (normalize the slug).** Replace the whole function with:

```python
def verify_live_techs(root):
    """The verify-live tech slugs declared in architecture-constraints.md's `## Verify-live` section (WS6). Each
    row `- **<tech>:** docs: … · source: …` names a tech whose record basename is `<tech>`. Labels may carry a
    descriptive qualifier (`- **BGE-M3 (embedding model):**`); the slug is normalized — trailing parenthetical
    stripped, lowercased — to the record-basename convention (shared/live-source-verification.md). Empty ⇒ none."""
    ac = read(os.path.join(root, "docs/spec/architecture-constraints.md")) or ""
    m = re.search(r"(?ims)^##\s+Verify-live\b.*?(?=^##\s|\Z)", ac)
    techs = set()
    if m:
        for line in m.group(0).splitlines():
            tm = re.match(r"^\s*-\s*\*\*([^*]+?):\*\*", line)
            if not tm:
                continue
            slug = re.sub(r"\s*\([^)]*\)\s*$", "", tm.group(1)).strip().lower()
            if re.fullmatch(r"[a-z0-9][\w.-]*", slug):
                techs.add(slug)
    return techs
```

- [ ] **Step 4: Fix the citation match in `grade_verify_live_adr`.** Replace the `ok = …` statement with:

```python
        ok = bool(va) and any(("docs/verification/%s.md" % t) in txt.lower()
                              and os.path.isfile(os.path.join(root, "docs/verification/%s.md" % t))
                              for t in named)
```
(`named` already matches case-insensitively; slugs are now lowercase, so `txt.lower()` links an uppercase-path
citation and `isfile` targets the lowercase record file per the convention.)

- [ ] **Step 5: Run — all seven scenarios pass**

```bash
python .agents/skills/03-architect/evals/check_architecture.py --self-test
```
Expected: `ALL GOOD`, exit 0.

- [ ] **Step 6: Commit**

```bash
git add .agents/skills/03-architect/evals/check_architecture.py
git commit -m "fix(03-evals): S18 verify-live slug normalization — qualified labels link + validate

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: The Verify-live label convention (doctrine, one line)

**Files:**
- Modify: `shared/live-source-verification.md` (the Declaration bullet, ~line 18)

- [ ] **Step 1: Edit.** In the bullet beginning `- **Declaration (a `03`-governed constraint):**`, after the
sentence ending `row under §\n  Verify-live.` insert:

```markdown
 **The `<tech>` label IS the record's lowercase basename** (`- **bge-m3:**` →
  `docs/verification/bge-m3.md`); descriptive text belongs after the colon, never inside the label — a qualified
  label breaks the mechanical label↔record linkage (the S18 check).
```

- [ ] **Step 2: Verify + commit**

```bash
grep -n "lowercase basename" shared/live-source-verification.md
git add shared/live-source-verification.md
git commit -m "docs(shared): Verify-live label = lowercase record basename (S18 linkage convention)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```
Expected: one grep hit inside the Declaration bullet. DA-T08's text in `references/data-architecture.md` is NOT
touched.

---

### Task 4: Data-case plumbing + core + DA-T01 (+ the `_self_test_data` skeleton)

**Files:**
- Modify: `.agents/skills/03-architect/evals/check_architecture.py`

**Interfaces:**
- Produces: `data_line_values(root) -> list[str]` (subset of `["retrieval","grounded-writes","memory"]`);
  `_attestation_recorded(root) -> bool`; `_norm(s) -> str`;
  `grade_capabilities_untouched(root, fixture_docs)`; `grade_data_arch(root, reqs, case, fixture_docs) -> rows`;
  `DATA_FIXTURES = {"data-modules": "beacon-data", "data-nogate": "beacon-nogate"}`; CLI gains
  `--case data-modules|data-nogate` and `--fixture-docs <dir>` (override; default derives from `DATA_FIXTURES`
  relative to the script). `_self_test_data()` joins `--self-test` (which now runs S18 + data, exit 0 iff both).

- [ ] **Step 1: Write the failing self-test skeleton (RED).** Add `_self_test_data` with the ideal-modules tree
builder and the first scenarios. Insert after `_self_test_s18`:

```python
def _ideal_modules_tree(tmp):
    """The ONE ideal data-modules tree; degenerates are single-element deletions of it (the mutation principle,
    design §6). Every DA check's positive element lives in exactly one place so a deletion isolates one clause."""
    def w(rel, s):
        p = os.path.join(tmp, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(s)
    w("docs/spec/specification.md",
      "# Specification — Beacon\n\n- **Profile:** agent-system\n"
      "- **Data:** retrieval(source-search) · grounded-writes(report-synthesis) · memory\n")
    w("docs/spec/capabilities/research.md",
      "# Research\n\n### REQ-001: Fan out research\nWorkers cover sources concurrently.\n"
      "### REQ-002: Grounded synthesis\nEvery claim cited.\n")
    w("docs/planning/sprints/sprint-01.md", "# Sprint 01\n\n## REQ-001: Fan out research\n## REQ-002: Grounded synthesis\n")
    w("docs/spec/architecture-constraints.md",
      "# Architecture Constraints — Beacon\n\n## Verify-live\n\n"
      "- **bge-m3:** docs: https://example.dev/bge · source: https://github.com/example/bge\n\n"
      "## Data architecture\n\n"
      "- **Retrieval corpus:** a persistent semantic index of fetched content; grows daily.\n"
      "- **Operator profiles:** per-operator research-interest profiles; operators may request deletion of their profile.\n")
    w("docs/spec/evals/research/synthesis.jsonl", '{"q": "seed", "expect_grounded": true}\n')
    w("docs/spec/amendment-log.json",
      '{"amendments": [{"id": "AMD-001", "req": null, "skill": "03-architect", "tier": 2,\n'
      '  "disposition": "approved", "source_quote": "Verify-live set", "supersedes": null, "resolved_by": "ADR-002"}]}\n')
    w("docs/verification/bge-m3.md",
      "---\nverified_against: bge-m3@1.0\n---\n\n## Verified claims\n\n| claim | citation | corrects |\n"
      "|---|---|---|\n| emits dense and sparse vectors in one pass | https://example.dev/bge#modes | — |\n")
    w("docs/architecture/system.md",
      "# System — Beacon\n\n## 9 · Reconcile\n\ncontext attestation: inputs [architecture realization, "
      "architecture-constraints + in-scope REQ blocks]; realization conversation: not provided\n")
    w("docs/architecture/adr/README.md", "# ADR index\n\n| ADR-001 | datastore |\n| ADR-002 | retrieval |\n| ADR-003 | memory |\n")
    w("docs/architecture/adr/ADR-001.md",
      "# ADR-001: Primary datastore\n\n- **Category:** classic\n"
      "- **Review-Trigger:** autovacuum lag persistently exceeds a healthy bound on the index table\n\n"
      "## Context & Problem Statement\n\nREQ-001 needs persistence. Decisive driver: data-model fit "
      "(rubric dimension 2) for REQ-001.\n\n"
      "## Considered Options\n\n1. PostgreSQL 16 (client-server)\n2. SQLite (embedded)\n\n"
      "## Decision Outcome\n\n**Chosen:** PostgreSQL 16 (client-server), the relational default.\n\n"
      "The durable commitment (relational + extensions) and the vendor/hosting pick (managed vs self-hosted) are "
      "two separate decisions — the vendor pick is deferred.\n\n"
      "Exit / migration cost: two-way door — standard SQL.\n")
    w("docs/architecture/adr/ADR-002.md",
      "# ADR-002: Retrieval — Stage-2 hybrid\n\n- **Category:** classic\n"
      "- **Verified-against:** docs/verification/bge-m3.md (bge-m3@1.0)\n\n"
      "## Decision Outcome\n\n**Chosen:** Stage 2 hybrid retrieval — lexical + dense fused by RRF; BGE-M3, "
      "1024 dimensions; reindex on an embedding swap or a chunking change.\n\n"
      "Chunking: a 512-token / 15% overlap baseline; short pages use document-level retrieval (an explicit "
      "no-chunk rationale).\n\nk-consistency: the eval metric's k equals the k sent to the generator.\n")
    w("docs/architecture/adr/ADR-003.md",
      "# ADR-003: Agent memory — semantic profiles\n\n- **Category:** memory\n\n"
      "## Context & Problem Statement\n\nGate-0 trigger: persistent entities across calls (operator profiles).\n\n"
      "## Decision Outcome\n\n**Chosen:** the semantic kind only, on a relational table; episodic and procedural "
      "have no fired trigger.\n\nLifecycle: a decay rule (with a TTL fallback) — unbounded retention is a named "
      "failure mode.\n\nSharing + authorization: shared read for the orchestrator; only the consolidator writes "
      "it (the authorization boundary).\n\nDeletion: an operator deletion request reaches derived forms — "
      "summaries, indices, and profile caches, not just source rows.\n")
    w("docs/architecture/specs/research.md",
      "# Feature Spec — Research\n\nServes: REQ-001, REQ-002 — the grounded-writes(report-synthesis) module.\n\n"
      "## Data-model changes\n\n| Table / field | Type | Constraints | Notes |\n|---|---|---|---|\n"
      "| research_jobs.id | uuid | pk | |\n\n"
      "## Components\n\n| Component | Layer | Responsibility | Location |\n|---|---|---|---|\n"
      "| CitationGate | backend | admission gate | src/gate.py |\n\n"
      "## Verification Contract\n\n| VC-ID | REQ | Method | Assertion |\n|---|---|---|---|\n"
      "| VC-01 | REQ-002 | eval-suite | dataset: docs/spec/evals/research/synthesis.jsonl; floor: 80% |\n\n"
      "Write-path admission rule: a schema check, then a referential check, then commit — enforced in code "
      "(the CitationGate component), which the model cannot bypass.\n\n"
      "Named ground-truth source: the job's own source-index snapshot, never sources generically.\n\n"
      "Threshold: 0 tolerance — a claim with an unresolvable citation is dropped before assembly.\n\n"
      "Fallback: refuse (drop the claim, terminal); no silent retry.\n")
    return tmp


def _self_test_data():
    """Grader-first bite proof for the data checks: the ideal passes everything; each degenerate is a
    single-element mutation and must flip exactly its target check (design §6, the mutation principle)."""
    import tempfile, shutil

    def run_case(tree, case, fixture_docs=None):
        results.clear()
        grade_data_arch(tree, sprint_reqs(tree), case, fixture_docs or os.path.join(tree, "docs"))
        grade_verify_live_adr(tree)
        return list(results)

    def entry(res, key):
        return next((r for r in res if key in r["text"]), None)

    rows, ok = [], True

    def expect(name, res, key, want_passed):
        nonlocal ok
        e = entry(res, key)
        good = e is not None and e["passed"] == want_passed
        rows.append((name, "%s passed=%s" % (key, want_passed), good,
                     "" if good else "got %s" % ("missing entry" if e is None else e["passed"])))
        ok = ok and good

    # 1 — the ideal tree passes every check
    tmp = tempfile.mkdtemp(prefix="da-")
    try:
        _ideal_modules_tree(tmp)
        res = run_case(tmp, "data-modules")
        bad = [r["text"] for r in res if not r["passed"]]
        good = not bad
        rows.append(("ideal data-modules tree: ALL checks pass", "all passed", good,
                     "" if good else "failing: %s" % bad[:3]))
        ok = ok and good
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    results.clear()
    w = max(len(r[0]) for r in rows)
    print("\n== check_architecture.py data (DA-T01..T08) self-test ==")
    for name, exp, good, note in rows:
        print("  [%s] %s  %s  %s" % ("PASS" if good else "FAIL", name.ljust(w), exp, note))
    print("\n%s" % ("ALL GOOD — data checks bite" if ok else "DATA SELF-TEST FAILED"))
    return ok
```

- [ ] **Step 2: Run to verify it fails**

```bash
python - <<'EOF'
import importlib.util, sys
spec = importlib.util.spec_from_file_location("ca", ".agents/skills/03-architect/evals/check_architecture.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
sys.exit(0 if m._self_test_data() else 1)
EOF
```
Expected: `NameError`/`AttributeError` — `grade_data_arch` not defined. (The `--self-test` flag is wired in Step 4.)

- [ ] **Step 3: Implement the plumbing + core + DA-T01.** Add after the `# ---------- shared structural
assertions` block (before `grade_agent_arch`):

```python
# ---------- Phase-1 data cases (design: _artifacts/data-architecture-phase1-design.md) ----------

DATA_FIXTURES = {"data-modules": "beacon-data", "data-nogate": "beacon-nogate"}

def data_line_values(root):
    """The declared `Data:` module values (the routing line; shared/agentic-profile.md § The Data line)."""
    sp = read(os.path.join(root, "docs/spec/specification.md")) or ""
    m = re.search(r"(?im)^\s*-\s*\*\*Data:\*\*\s*(.+)$", sp)
    if not m:
        return []
    return [v for v in ("retrieval", "grounded-writes", "memory")
            if re.search(r"\b" + v + r"\b", m.group(1), re.I)]

def _norm(s):
    return (s or "").replace("\r\n", "\n").replace("\r", "\n")

def _attestation_recorded(root):
    """The S12 attestation scan, shared by grade_structure and grade_data_arch."""
    blob = (system_md(root) or "") + "\n" + adr_blob(root) + "\n" + specs_blob(root) + "\n"
    for dp, dn, fn in os.walk(os.path.join(root, "docs/architecture")):
        for f in fn:
            if re.search(r"reconcile", f, re.I):
                blob += (read(os.path.join(dp, f)) or "") + "\n"
    return bool(re.search(r"context attestation|(realization|build)\s+conversation[^\n]{0,30}not provided",
                          blob, re.I))

def grade_capabilities_untouched(root, fixture_docs):
    """Spine integrity: capabilities/** content-identical (EOL-normalized) to the fixture — the smoke's manual
    REQ-text eyeball made deterministic. Content compare, not byte compare: the threat is edits, not CRLF."""
    fx = os.path.join(fixture_docs, "spec", "capabilities")
    ws = os.path.join(root, "docs", "spec", "capabilities")
    fx_files, diffs, extra = [], [], []
    for dp, dn, fn in os.walk(fx):
        for f in fn:
            rel = os.path.relpath(os.path.join(dp, f), fx).replace("\\", "/")
            fx_files.append(rel)
            if _norm(read(os.path.join(dp, f))) != _norm(read(os.path.join(ws, rel))):
                diffs.append(rel)
    if os.path.isdir(ws):
        for dp, dn, fn in os.walk(ws):
            for f in fn:
                rel = os.path.relpath(os.path.join(dp, f), ws).replace("\\", "/")
                if rel not in fx_files:
                    extra.append(rel)
    check("Spine integrity: docs/spec/capabilities/** content-identical to the fixture (EOL-normalized)",
          bool(fx_files) and not diffs and not extra,
          f"fixture files={len(fx_files)}; changed={diffs or 'none'}; extra={extra or 'none'}")

def grade_data_arch(root, reqs, case, fixture_docs):
    """Phase-1 data cases — a focused path like grade_agent_arch: a small core + the DA checks. The full webapp
    contract is the TeamPulse cases' job; topology economics is the agent case's job."""
    sysmd = system_md(root) or ""
    check("system.md written at docs/architecture/system.md", bool(sysmd.strip()), f"{len(sysmd)} chars")
    idx = read(os.path.join(adr_dir(root), "README.md"))
    check("ADR registry present (adr/README.md index + >=1 ADR)",
          idx is not None and bool(adr_files(root)),
          f"index={'yes' if idx else 'no'}; adrs={[os.path.basename(f) for f in adr_files(root)]}")
    rows = amendments(root)
    check("amendment-log.json is valid JSON with an 'amendments' array",
          rows is not None, "valid" if rows is not None else "missing/invalid amendment-log.json")
    check("Reconciler isolation: a context attestation is recorded (fresh-spawner proxy; transcript check is manual)",
          _attestation_recorded(root),
          "attestation marker found" if _attestation_recorded(root) else "no marker in docs/architecture/")
    sb = specs_blob(root)
    spec_reqs = sorted(set(re.findall(r"REQ-\d+", sb)) & set(reqs))
    has_vc = bool(re.search(r"(?i)verification contract", sb))
    check("A feature spec references the sprint's REQs and carries a Verification Contract",
          bool(feature_specs(root)) and bool(spec_reqs) and has_vc,
          f"specs={[os.path.basename(s) for s in feature_specs(root)] or 'none'}; "
          f"sprint-REQ refs={spec_reqs or 'none'}; VC={has_vc}")
    grade_capabilities_untouched(root, fixture_docs)

    declared = data_line_values(root)
    blob = sysmd + "\n" + adr_blob(root) + "\n" + sb
    missing = [v for v in declared if not re.search(r"\b" + v + r"\b", blob, re.I)]
    check("DA-T01 pairing: every declared Data: value appears in the realization (realized, or explicitly "
          "declined — silent omission fails either way)",
          bool(declared) and not missing, f"declared={declared}; unaddressed={missing or 'none'}")

    if case == "data-modules":
        grade_da_t02(root, sb + "\n" + adr_blob(root))
        grade_da_t03(sb + "\n" + adr_blob(root))
        grade_da_t04(root)
        grade_da_t05(root, blob)
        grade_da_t06(root, blob)
        grade_da_t07(root)
    else:
        grade_da_t04(root)
        grade_nogate(rows, sb)
    return rows
```

Also, in `grade_structure`, replace the S12 block (the `arch_blob` build + `attest` + its `check(…)`) with:

```python
    attest = _attestation_recorded(root)
    check("Reconciler isolation: a context attestation is recorded (fresh-spawner proxy; transcript check is manual)",
          attest, "attestation marker found" if attest else "no context-attestation marker in docs/architecture/")
```

And in `main()`: add the two cases to `--case` choices, add
`ap.add_argument("--fixture-docs", help="override the fixture docs/ dir for the capabilities check")`, extend the
`--self-test` branch to `raise SystemExit(0 if (_self_test_s18() and _self_test_data()) else 1)`, and add the
dispatch before the webapp-case block:

```python
    if a.case in DATA_FIXTURES:
        fixture_docs = a.fixture_docs or os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "fixtures", DATA_FIXTURES[a.case], "docs")
        grade_data_arch(root, reqs, a.case, fixture_docs)
        grade_verify_live_adr(root)
        return emit(a)
```

For this task only, stub the not-yet-written checks so the ideal scenario can run (each is fully implemented in
Tasks 5–8 — the stubs exist so RED stays scoped to one task):

```python
def grade_da_t02(root, blob): pass
def grade_da_t03(blob): pass
def grade_da_t04(root): pass
def grade_da_t05(root, blob): pass
def grade_da_t06(root, blob): pass
def grade_da_t07(root): pass
def grade_nogate(rows, sb): pass
```

- [ ] **Step 4: Run — the skeleton is green**

```bash
python .agents/skills/03-architect/evals/check_architecture.py --self-test
```
Expected: S18 `ALL GOOD` + data `ALL GOOD` (1 scenario: ideal tree, 7 core/T01/S18 checks all pass), exit 0.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/03-architect/evals/check_architecture.py
git commit -m "feat(03-evals): data-case plumbing — grade_data_arch core + DA-T01 + self-test skeleton

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 5: DA-T02 + DA-T03 (pairing checks) — the declared-but-unrealized degenerates

**Files:**
- Modify: `.agents/skills/03-architect/evals/check_architecture.py`

**Interfaces:**
- Consumes: `grade_data_arch` calls `grade_da_t02(root, blob)` / `grade_da_t03(blob)` (Task 4 signatures — note
  T02 gains `blob` over the stub's `sb`; keep the Task-4 call sites `grade_da_t02(root, sb + "\n" + adr_blob(root))`).

- [ ] **Step 1: Add the failing scenarios (RED).** In `_self_test_data`, after the ideal scenario, add the
mutation helper + three scenarios:

```python
    def mutated(mutate):
        """Build the ideal tree, apply one mutation, grade it, tear down."""
        t = tempfile.mkdtemp(prefix="da-")
        try:
            _ideal_modules_tree(t)
            mutate(t)
            return run_case(t, "data-modules")
        finally:
            shutil.rmtree(t, ignore_errors=True)

    def edit(t, rel, old, new):
        p = os.path.join(t, rel)
        s = read(p) or ""
        assert old in s, "mutation anchor missing: %s in %s" % (old[:40], rel)
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(s.replace(old, new))

    expect("T01 fires: memory declared, ADR-003 deleted (unrealized)",
           mutated(lambda t: os.remove(os.path.join(t, "docs/architecture/adr/ADR-003.md"))),
           "DA-T01", False)
    expect("T02 fires: dataset ref points at a missing file",
           mutated(lambda t: edit(t, "docs/architecture/specs/research.md",
                                  "docs/spec/evals/research/synthesis.jsonl",
                                  "docs/spec/evals/research/missing.jsonl")),
           "DA-T02", False)
    expect("T03 fires: the admission-rule paragraph removed",
           mutated(lambda t: edit(t, "docs/architecture/specs/research.md",
                                  "Write-path admission rule: a schema check, then a referential check, then "
                                  "commit — enforced in code (the CitationGate component), which the model "
                                  "cannot bypass.\n\n", "")),
           "DA-T03", False)
```
Run `--self-test`: expected FAIL — the stubs emit no `DA-T02`/`DA-T03` entries (`missing entry`), and T01's
scenario passes already (its check landed in Task 4 — it must PASS here and stay green).

- [ ] **Step 2: Implement.** Replace the `grade_da_t02` / `grade_da_t03` stubs:

```python
def grade_da_t02(root, blob):
    """DA-T02 — retrieval declared ⇒ >=1 eval-suite VC row whose golden-set dataset ref resolves on disk."""
    has_es = bool(re.search(r"(?i)eval-suite", blob))
    paths = sorted(set(re.findall(r"(docs/spec/evals/[\w./-]+\.jsonl)", blob)))
    resolving = [p for p in paths if os.path.isfile(os.path.join(root, p))]
    check("DA-T02 pairing: retrieval declared => an eval-suite VC row whose golden-set dataset ref resolves on disk",
          has_es and bool(resolving),
          f"eval-suite mentioned={has_es}; dataset refs={paths or 'none'}; resolving={resolving or 'none'}")

def grade_da_t03(blob):
    """DA-T03 — grounded-writes declared ⇒ a named write-path admission rule: >=2 chain stages + admit/commit,
    within one blank-line-delimited block."""
    ok, ev = False, "no admission-rule block found"
    for para in re.split(r"\n\s*\n", blob):
        stages = set(m.group(1).lower().replace(" ", "-")
                     for m in re.finditer(r"(?i)\b(schema|referential|business[- ]rule)\b", para))
        if len(stages) >= 2 and re.search(r"(?i)\b(admission|admit(s|ted)?|commit)\b", para):
            ok, ev = True, f"stages={sorted(stages)}"
            break
    check("DA-T03 pairing: grounded-writes declared => a named write-path admission rule (>=2 of "
          "schema/referential/business-rule + admit/commit in one block)", ok, ev)
```

- [ ] **Step 3: Run `--self-test` — all green (ideal still all-pass; T01/T02/T03 degenerates fire).**
- [ ] **Step 4: Commit** — `feat(03-evals): DA-T02/T03 pairing checks + declared-but-unrealized degenerates`.

---

### Task 6: DA-T04 (datastore ADR content) — five clause degenerates

**Files:**
- Modify: `.agents/skills/03-architect/evals/check_architecture.py`

- [ ] **Step 1: Add the failing scenarios (RED).** In `_self_test_data`:

```python
    expect("T04 fires: only one considered option",
           mutated(lambda t: edit(t, "docs/architecture/adr/ADR-001.md", "2. SQLite (embedded)\n", "")),
           "DA-T04", False)
    expect("T04 fires: Review-Trigger line removed",
           mutated(lambda t: edit(t, "docs/architecture/adr/ADR-001.md",
                                  "- **Review-Trigger:** autovacuum lag persistently exceeds a healthy bound on "
                                  "the index table\n", "")),
           "DA-T04", False)
    expect("T04 fires: Review-Trigger is 'review periodically'",
           mutated(lambda t: edit(t, "docs/architecture/adr/ADR-001.md",
                                  "autovacuum lag persistently exceeds a healthy bound on the index table",
                                  "review periodically each quarter")),
           "DA-T04", False)
    expect("T04 fires: exit-cost statement removed",
           mutated(lambda t: edit(t, "docs/architecture/adr/ADR-001.md",
                                  "Exit / migration cost: two-way door — standard SQL.\n", "")),
           "DA-T04", False)
    expect("T04 fires: durable-vs-vendor split paragraph removed",
           mutated(lambda t: edit(t, "docs/architecture/adr/ADR-001.md",
                                  "The durable commitment (relational + extensions) and the vendor/hosting pick "
                                  "(managed vs self-hosted) are two separate decisions — the vendor pick is "
                                  "deferred.\n\n", "")),
           "DA-T04", False)
```
Run: all five report `missing entry` (stub).

- [ ] **Step 2: Implement.** Replace the `grade_da_t04` stub:

```python
DIMENSION_MARKERS = (r"(?i)dimension|§ ?1\b|rubric|workload shape|data-model fit|pacelc|scale envelope"
                     r"|operational maturity|team[- ]skill|choose[- ]boring|boring[- ]tech")

def grade_da_t04(root):
    """DA-T04 — the datastore ADR walks the §1 rubric. Candidate = an ADR whose Decision Outcome names a
    datastore token (the token-in-named-field pattern); >=1 candidate must satisfy every clause. Always-on."""
    best = None  # (score, name, clauses)
    for f in adr_files(root):
        txt = read(f) or ""
        dm = re.search(r"##+\s*Decision\s+Outcome(.+?)(?:\n##\s|\Z)", txt, re.I | re.S)
        dec = dm.group(1) if dm else txt
        if not tokens_in(dec, DB_CLIENT_SERVER + DB_EMBEDDED):
            continue
        om = re.search(r"##+\s*Considered\s+Options(.+?)(?:\n##\s|\Z)", txt, re.I | re.S)
        n_opts = len(re.findall(r"(?m)^\s*(?:\d+\.|[-*])\s+\S", om.group(1))) if om else 0
        rt = re.search(r"(?im)^\s*[-*]?\s*\*\*Review-Trigger:\*\*\s*(.+(?:\n(?![ \t]*[-*#]).+)*)", txt)
        clauses = {
            "alts>=2": n_opts >= 2,
            "driver-REQ": bool(re.search(r"REQ-\d+", txt)),
            "dimension-map": bool(re.search(DIMENSION_MARKERS, txt)),
            "review-trigger(symptom)": bool(rt) and not re.search(
                r"(?i)periodic|every\s+\d+\s*(day|week|month|quarter)|quarterly|annually", rt.group(1)),
            "exit-cost": bool(re.search(
                r"(?i)one[- ]way|two[- ]way door|exit\s*/?\s*(cost|migration)|migration cost|reversib|lock[- ]in", txt)),
            "durable-vs-vendor": any(
                re.search(r"(?i)vendor|managed|hosting|self[- ]hosted", para) and
                re.search(r"(?i)separate|two (separate )?decisions|deferred|distinct|its own (adr|decision)", para)
                for para in re.split(r"\n\s*\n", txt)),
        }
        score = sum(clauses.values())
        if best is None or score > best[0]:
            best = (score, os.path.basename(f), clauses)
    ok = best is not None and all(best[2].values())
    check("DA-T04: a datastore ADR walks the §1 rubric (>=2 alternatives · driver REQ + dimension map · symptom "
          "Review-Trigger · exit-cost · durable-vs-vendor split)",
          ok, "no ADR Decision names a datastore token" if best is None
          else "%s: %s" % (best[1], {k: v for k, v in best[2].items()}))
```

- [ ] **Step 3: Run `--self-test` — green.** If `durable-vs-vendor` cannot be made to bite here (a degenerate
passing, or the ideal failing), this is the design's pre-authorized demote point: drop that key from `clauses`,
note "durable-vs-vendor: demoted to reconciler territory (could not bite deterministically)" in the run record,
and keep the other five. Do NOT silently weaken any other clause.
- [ ] **Step 4: Commit** — `feat(03-evals): DA-T04 datastore-ADR content check + five clause degenerates`.

---

### Task 7: DA-T05 + DA-T06 + DA-T07 (content clauses + conditional directions)

**Files:**
- Modify: `.agents/skills/03-architect/evals/check_architecture.py`

- [ ] **Step 1: Add the failing scenarios (RED).**

```python
    expect("T05 fires: dims+reindex sentence removed",
           mutated(lambda t: edit(t, "docs/architecture/adr/ADR-002.md",
                                  "; BGE-M3, 1024 dimensions; reindex on an embedding swap or a chunking change",
                                  "")),
           "DA-T05", False)
    expect("T05 fires: chunking paragraph removed",
           mutated(lambda t: edit(t, "docs/architecture/adr/ADR-002.md",
                                  "Chunking: a 512-token / 15% overlap baseline; short pages use document-level "
                                  "retrieval (an explicit no-chunk rationale).\n\n", "")),
           "DA-T05", False)
    expect("T06 fires: threshold paragraph removed",
           mutated(lambda t: edit(t, "docs/architecture/specs/research.md",
                                  "Threshold: 0 tolerance — a claim with an unresolvable citation is dropped "
                                  "before assembly.\n\n", "")),
           "DA-T06", False)
    expect("T06 fires: LLM-issued queries added with no driver-layer rule (conditional, required direction)",
           mutated(lambda t: edit(t, "docs/architecture/specs/research.md",
                                  "Fallback: refuse (drop the claim, terminal); no silent retry.\n",
                                  "Fallback: refuse (drop the claim, terminal); no silent retry.\n\n"
                                  "Workers issue LLM-generated SQL queries against the corpus database.\n")),
           "DA-T06", False)
    expect("T07 fires: sharing+authz paragraph removed",
           mutated(lambda t: edit(t, "docs/architecture/adr/ADR-003.md",
                                  "Sharing + authorization: shared read for the orchestrator; only the "
                                  "consolidator writes it (the authorization boundary).\n\n", "")),
           "DA-T07", False)
    expect("T07 fires: deletion promised but derived-reach paragraph removed",
           mutated(lambda t: edit(t, "docs/architecture/adr/ADR-003.md",
                                  "Deletion: an operator deletion request reaches derived forms — summaries, "
                                  "indices, and profile caches, not just source rows.\n", "")),
           "DA-T07", False)

    def _mut_no_promise_no_reach(t):
        edit(t, "docs/spec/architecture-constraints.md",
             "- **Operator profiles:** per-operator research-interest profiles; operators may request deletion "
             "of their profile.\n", "")
        edit(t, "docs/architecture/adr/ADR-003.md",
             "Deletion: an operator deletion request reaches derived forms — summaries, indices, and profile "
             "caches, not just source rows.\n", "")
    expect("T07 N/A direction: no promise in the spine + no reach paragraph still PASSES",
           mutated(_mut_no_promise_no_reach), "DA-T07", True)
    expect("Capabilities check fires on an edited REQ file",
           None, "capabilities", False)  # placeholder wiring — replaced by the two-tree scenario below
```
For the capabilities scenario, replace that last `expect` with a two-tree run (fixture vs mutated workspace):

```python
    t_fx, t_ws = tempfile.mkdtemp(prefix="da-fx-"), tempfile.mkdtemp(prefix="da-ws-")
    try:
        _ideal_modules_tree(t_fx); _ideal_modules_tree(t_ws)
        edit(t_ws, "docs/spec/capabilities/research.md", "Every claim cited.", "Every claim cited, mostly.")
        results.clear()
        grade_data_arch(t_ws, sprint_reqs(t_ws), "data-modules", os.path.join(t_fx, "docs"))
        res = list(results)
    finally:
        shutil.rmtree(t_fx, ignore_errors=True); shutil.rmtree(t_ws, ignore_errors=True)
    expect("Capabilities check fires on an edited REQ file", res, "content-identical", False)
```
(`expect` accepts the pre-computed `res` — give it the signature `expect(name, res, key, want)` and pass
`mutated(...)`'s return everywhere, as already shown.)
Run: T05/T06/T07 scenarios report `missing entry`; the capabilities scenario PASSES already (Task 4) and must
stay green.

- [ ] **Step 2: Implement.** Replace the three stubs:

```python
def grade_da_t05(root, blob):
    """DA-T05 — retrieval content clauses. `Stage N` is doctrine vocabulary the tooth itself mandates
    ("the stage declared") — a structural-lift discriminator, not corpus leakage."""
    stages = sorted(set(int(n) for n in re.findall(r"(?i)\bStage\s*([0-6])\b", blob)))
    chunk_ok = (bool(re.search(r"(?i)\d+[\s-]?token", blob)) and bool(re.search(r"(?i)overlap", blob))) \
        or bool(re.search(r"(?i)no[- ]chunk", blob))
    dims = bool(re.search(r"(?i)\b\d{3,4}\s*-?\s*dim(?:ension)?s?\b|vector\(\d{3,4}\)", blob))
    reindex = bool(re.search(r"(?i)re-?index|re-?embed", blob))
    k_ok = bool(re.search(r"(?i)k[- ]consisten", blob)) \
        or bool(re.search(r"(?i)\bk\b[^\n.]{0,80}(equal|same|match)", blob))
    hi = [s for s in sorted(set(int(n) for n in re.findall(r"(?i)\bStage\s*([0-6])\b", adr_decisions(root))))
          if s >= 3]
    esc_ok, esc_ev = True, "committed stage <3 => why-not-simpler N/A"
    if hi:
        esc_ok = bool(re.search(r"(?i)why not|simpler|measured gap|not justified", blob))
        esc_ev = f"stage {hi} committed; why-not-simpler={esc_ok}"
    check("DA-T05: retrieval content clauses (stage declared · chunking params or no-chunking rationale · "
          "embedding dims + reindex trigger · k-consistency · why-not-simpler on Stage>=3)",
          bool(stages) and chunk_ok and dims and reindex and k_ok and esc_ok,
          f"stages={stages or 'none'}; chunking={chunk_ok}; dims={dims}; reindex={reindex}; k={k_ok}; {esc_ev}")

def grade_da_t06(root, blob):
    """DA-T06 — grounding content clauses. The driver-layer clause is conditional on LLM-issued queries
    existing in the realization (its required direction is proven by the self-test's ADDITION degenerate)."""
    gt = bool(re.search(r"(?i)ground[- ]truth", blob))
    thr = any(re.search(r"(?i)threshold|tolerance", para)
              and re.search(r"(?i)\b(\d+(\.\d+)?%?|zero)\b", para)
              and re.search(r"(?i)\b(block(s|ed)?|drop(s|ped)?|refus\w+|regenerat\w+|auto-correct\w*|rout(e|ed|ing)|flag(s|ged)?)\b", para)
              for para in re.split(r"\n\s*\n", blob))
    fb = bool(re.search(r"(?i)fallback", blob)) and bool(re.search(r"(?i)refus|retry|degrade|escalat|drop", blob))
    llmq = bool(re.search(r"(?i)(llm|model)[- ](issued|generated)\s*(sql|quer)|text[- ]to[- ]sql|nl2sql", blob))
    if llmq:
        drv = bool(re.search(r"(?i)read[- ]only", blob)) and bool(re.search(r"(?i)driver|connection|permission", blob))
        drv_ev = f"LLM-issued queries present; driver-layer read-only={drv}"
    else:
        drv, drv_ev = True, "no LLM-issued queries in the realization => driver-layer clause N/A"
    check("DA-T06: grounding content clauses (named ground-truth source · numeric threshold + action · fallback "
          "per failure mode · driver-layer read-only when LLM-issued queries exist)",
          gt and thr and fb and drv, f"ground-truth={gt}; threshold+action={thr}; fallback={fb}; {drv_ev}")

def grade_da_t07(root):
    """DA-T07 — memory content clauses, on the Category: memory ADR (the doctrine's own contract: `Data: memory`
    backs the Category: memory ADR). The deletion pairing gates on the SPINE's promise line — structure, not
    vocabulary: present => the pairing is required; absent => N/A."""
    mem = None
    for f in adr_files(root):
        txt = read(f) or ""
        if re.search(r"(?im)^\s*[-*]?\s*\*\*Category:\*\*\s*memory\b", txt):
            mem = (os.path.basename(f), txt)
            break
    if mem is None:
        check("DA-T07: memory content clauses (Gate-0 trigger cited · per-kind substrate · lifecycle floor · "
              "sharing+authz named together · deletion=>derived-reach when promised)",
              False, "no Category: memory ADR found")
        return
    name, txt = mem
    paras = re.split(r"\n\s*\n", txt)
    gate0 = bool(re.search(r"(?i)gate[- ]?0", txt)) and bool(re.search(r"(?i)trigger", txt))
    kinds = bool(re.search(r"(?i)\b(semantic|episodic|procedural)\b", txt))
    substrate = bool(re.search(r"(?i)relational|table|store|\bkv\b|vector|graph|file", txt))
    life = bool(re.search(r"(?i)\bttl\b|decay|expir|retention", txt))
    share = any(re.search(r"(?i)\bshared?\b|private", p) and
                re.search(r"(?i)authori[sz]|sole writer|only .{0,40}writes|write[- ]path", p) for p in paras)
    promise = bool(re.search(r"(?i)request\s+deletion",
                             read(os.path.join(root, "docs/spec/architecture-constraints.md")) or ""))
    if promise:
        reach = any(re.search(r"(?i)delet", p) and re.search(r"(?i)derived|summar|index|profile|cache|reach", p)
                    for p in paras)
        reach_ev = f"deletion promised in the spine; derived-reach pairing={reach}"
    else:
        reach, reach_ev = True, "no user-facing deletion promise in the spine => pairing N/A"
    check("DA-T07: memory content clauses (Gate-0 trigger cited · per-kind substrate · lifecycle floor · "
          "sharing+authz named together · deletion=>derived-reach when promised)",
          gate0 and kinds and substrate and life and share and reach,
          f"{name}: gate0={gate0}; kinds={kinds}; substrate={substrate}; lifecycle={life}; "
          f"sharing+authz={share}; {reach_ev}")
```

- [ ] **Step 3: Run `--self-test` — all green.**
- [ ] **Step 4: Commit** — `feat(03-evals): DA-T05/T06/T07 content checks + conditional-direction degenerates`.

---

### Task 8: The nogate checks + the ideal-nogate tree

**Files:**
- Modify: `.agents/skills/03-architect/evals/check_architecture.py`

- [ ] **Step 1: Add the ideal-nogate builder + failing scenarios (RED).**

```python
def _ideal_nogate_tree(tmp):
    """The declined-direction ideal: Data declared, every trigger denied, need-gate declines with reasons.
    No Verify-live (S18 N/A), no substrate commitments, <=1 amendment row."""
    def w(rel, s):
        p = os.path.join(tmp, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(s)
    w("docs/spec/specification.md",
      "# Specification — Beacon\n\n- **Profile:** agent-system\n"
      "- **Data:** retrieval(handbook-lookup) · memory\n")
    w("docs/spec/capabilities/research.md",
      "# Research\n\n### REQ-001: Fan out research\nWorkers cover sources concurrently.\n"
      "### REQ-002: Grounded synthesis\nEvery claim cited.\n")
    w("docs/planning/sprints/sprint-01.md", "# Sprint 01\n\n## REQ-001: Fan out research\n## REQ-002: Grounded synthesis\n")
    w("docs/spec/architecture-constraints.md",
      "# Architecture Constraints — Beacon\n\n## Data architecture\n\n"
      "- **Reference handbook:** ~40 short, stable documents, revised quarterly; fits in a context window.\n"
      "- **Cross-session learning:** questions are independent; operators value a from-scratch read; no "
      "personalization is wanted.\n")
    w("docs/spec/amendment-log.json", '{"amendments": []}\n')
    w("docs/architecture/system.md",
      "# System — Beacon\n\n## 11 · Deferred\n\nretrieval declined: the handbook fits in context (Stage 0 — "
      "cache-and-stuff); memory declined: no Gate-0 trigger fires (independent questions, reproducibility "
      "valued).\n\n## 9 · Reconcile\n\ncontext attestation: inputs [architecture realization, "
      "architecture-constraints + in-scope REQ blocks]; realization conversation: not provided\n")
    w("docs/architecture/adr/README.md", "# ADR index\n\n| ADR-001 | datastore |\n")
    w("docs/architecture/adr/ADR-001.md",
      "# ADR-001: Primary datastore\n\n- **Category:** classic\n"
      "- **Review-Trigger:** autovacuum lag persistently exceeds a healthy bound on the jobs table\n\n"
      "## Context & Problem Statement\n\nREQ-001 needs persistence. Decisive driver: data-model fit "
      "(rubric dimension 2) for REQ-001.\n\n"
      "## Considered Options\n\n1. PostgreSQL 16 (client-server)\n2. SQLite (embedded)\n\n"
      "## Decision Outcome\n\n**Chosen:** PostgreSQL 16 (client-server), the relational default.\n\n"
      "The durable commitment (relational + extensions) and the vendor/hosting pick (managed vs self-hosted) are "
      "two separate decisions — the vendor pick is deferred.\n\n"
      "Exit / migration cost: two-way door — standard SQL.\n")
    w("docs/architecture/specs/research.md",
      "# Feature Spec — Research\n\nServes: REQ-001, REQ-002.\n\n"
      "## Data-model changes\n\n| Table / field | Type | Constraints | Notes |\n|---|---|---|---|\n"
      "| research_jobs.id | uuid | pk | |\n\n"
      "## Components\n\n| Component | Layer | Responsibility | Location |\n|---|---|---|---|\n"
      "| Orchestrator | backend | dispatches workers | src/orchestrator.py |\n\n"
      "## Verification Contract\n\n| VC-ID | REQ | Method | Assertion |\n|---|---|---|---|\n"
      "| VC-01 | REQ-001 | api-contract | POST /research returns 202 |\n")
    return tmp
```

Scenarios (a second `mutated_ng` helper mirroring `mutated` but building `_ideal_nogate_tree` and running
`run_case(t, "data-nogate")`):

```python
    expect("ideal data-nogate tree: ALL checks pass", run_all_nogate(), None, True)   # like the modules all-pass row
    expect("selectivity fires: a vector-index Data-model row added",
           mutated_ng(lambda t: edit(t, "docs/architecture/specs/research.md",
                                     "| research_jobs.id | uuid | pk | |\n",
                                     "| research_jobs.id | uuid | pk | |\n"
                                     "| source_index.embedding | vector(1024) | HNSW index | |\n")),
           "selectivity", False)
    expect("selectivity fires: a memory-store Components row added",
           mutated_ng(lambda t: edit(t, "docs/architecture/specs/research.md",
                                     "| Orchestrator | backend | dispatches workers | src/orchestrator.py |\n",
                                     "| Orchestrator | backend | dispatches workers | src/orchestrator.py |\n"
                                     "| MemoryStore | backend | profile store | src/memory.py |\n")),
           "selectivity", False)
    expect("amendment bound fires: 2 rows on a declined line",
           mutated_ng(lambda t: edit(t, "docs/spec/amendment-log.json", '{"amendments": []}',
                                     '{"amendments": [{"id": "AMD-001", "tier": 2, "disposition": "approved", '
                                     '"source_quote": "a", "resolved_by": "ADR-001"}, {"id": "AMD-002", "tier": 2, '
                                     '"disposition": "approved", "source_quote": "b", "resolved_by": "ADR-001"}]}')),
           "False-positive bound", False)
    expect("T01 fires on nogate: silent omission (decline mentions scrubbed)",
           mutated_ng(lambda t: edit(t, "docs/architecture/system.md",
                                     "retrieval declined: the handbook fits in context (Stage 0 — "
                                     "cache-and-stuff); memory declined: no Gate-0 trigger fires (independent "
                                     "questions, reproducibility valued).", "data modules: none adopted.")),
           "DA-T01", False)
```
(For the all-pass row, mirror the ideal-modules loop: build, `run_case(t, "data-nogate")`, assert no failing
entries.) Run: `selectivity` / `False-positive bound` rows report `missing entry`; the T01 nogate scenario and the
all-pass row must already behave (T01 green from Task 4; all-pass fails only on stubs — none left after Task 7).

- [ ] **Step 2: Implement.** Replace the `grade_nogate` stub:

```python
def grade_nogate(rows, sb):
    """Selectivity (design §5 principle 2): absence is read ONLY from structured commitment loci — Data-model +
    Components table rows — never prose, where a decline legitimately mentions stores in negation."""
    trows = [ln for ln in sb.splitlines() if re.match(r"\s*\|", ln)]
    r_hits = [ln.strip()[:80] for ln in trows if re.search(r"(?i)vector\s*\(|embedding|tsvector|hnsw|ivfflat", ln)]
    m_hits = [ln.strip()[:80] for ln in trows if re.search(r"(?i)memor|reliab|profile", ln)]
    check("Need-gate selectivity: no retrieval/memory substrate commitment in the structured loci "
          "(Data-model/Components table rows) — the declined modules stay declined",
          not r_hits and not m_hits,
          f"retrieval-commitment rows={r_hits or 'none'}; memory-commitment rows={m_hits or 'none'}")
    n = len(rows or [])
    check("False-positive bound: a declined Data: line yields <=1 amendment row (one line-narrowing proposal is "
          "defensible; invented findings are not)",
          rows is not None and n <= 1, f"{n} amendment row(s)")
```

- [ ] **Step 3: Run `--self-test` — all green (both ideals all-pass; every degenerate fires its target).**
- [ ] **Step 4: Commit** — `feat(03-evals): data-nogate selectivity + amendment-bound checks + declined-direction ideal`.

---

### Task 9: Real-output validation (zero-token) — the smoke tree + old-vs-new re-grades

**Files:** none in the calibrated tree (validation only; grader fixes loop back to Tasks 5–8 if triage demands).

- [ ] **Step 1: The smoke tree under the new data grader**

```bash
python .agents/skills/03-architect/evals/check_architecture.py \
  --outputs _artifacts/skills-eval/03-architect/smoke-2026-07-18/with_skill/outputs \
  --case data-modules \
  --fixture-docs .agents/skills/03-architect/evals/fixtures/beacon-agent/docs
```
Expected: **14/14** — with in-evidence: DA-T07 `no user-facing deletion promise … => pairing N/A`, DA-T06
`no LLM-issued queries … N/A`, and **S18 PASS** (`cited=ADR-002…→pgvector / ADR-005…→bge-m3…`) — the flip from
the smoke's silent `N/A — no verify-live tech declared`. Any FAIL = grader bug first: fix the check (Tasks 5–8
pattern: add a scenario reproducing it, fix, re-run), never tweak the smoke tree.

- [ ] **Step 2: Old-vs-new no-drift proof over every saved tree**

```bash
git show main:.agents/skills/03-architect/evals/check_architecture.py > /tmp/old_check.py
for d in _artifacts/skills-eval/03-architect/iteration-1/*/*/outputs \
         _artifacts/skills-eval/03-architect/iteration-3/clean-constraint/with_skill/outputs; do
  case="$(basename "$(dirname "$(dirname "$d")")")"
  python /tmp/old_check.py --outputs "$d" --case "$case" > /dev/null && cp "$d/grading.json" /tmp/old.json
  python .agents/skills/03-architect/evals/check_architecture.py --outputs "$d" --case "$case" > /dev/null
  diff /tmp/old.json "$d/grading.json" && echo "STABLE: $d" || echo "DRIFT: $d"
done
```
Expected: `STABLE` for all 7 trees (S18 was N/A on every TeamPulse tree — no Verify-live sections there — and the
S12 refactor is behavior-identical). Any `DRIFT` line: read the diff; only an S18 evidence-string change caused by
normalization on a tree that *declares* verify-live techs is acceptable — anything else is a regression to fix.

- [ ] **Step 3: Record.** Write the outcomes (smoke 14/14 + the S18 flip evidence line + 7×STABLE) into
`_artifacts/skills-eval/03-architect/iteration-data-1/VALIDATION.md` (created now; the run record grows in
Task 12). `git add -f` it and commit — `test(03-evals): real-output validation — smoke 14/14, S18 flip, 7 saved trees stable`.

---

### Task 10: The two fixture trees

**Files:**
- Create: `.agents/skills/03-architect/evals/fixtures/beacon-data/docs/**` and
  `.agents/skills/03-architect/evals/fixtures/beacon-nogate/docs/**`

- [ ] **Step 1: Copy the base**

```bash
cp -r .agents/skills/03-architect/evals/fixtures/beacon-agent/docs .agents/skills/03-architect/evals/fixtures/beacon-data/docs
cp -r .agents/skills/03-architect/evals/fixtures/beacon-agent/docs .agents/skills/03-architect/evals/fixtures/beacon-nogate/docs
```

- [ ] **Step 2: `beacon-data` — edit 3 files.**
`specification.md`: after the `- **Profile:** agent-system …` line, insert:

```markdown
- **Data:** retrieval(source-search) · grounded-writes(report-synthesis) · memory   <!-- data-module routing; see shared/agentic-profile.md § The Data line. -->
```

`architecture-constraints.md`: append at end of file:

```markdown

## Data architecture

> Declaration-truth for Beacon's data needs. The `Data:` line in `specification.md` routes these to skill 03's
> data modules; skill 03 realizes each into ADRs/specs (it does not decide *whether* — the need below is stated here).

- **Retrieval corpus (drives `retrieval(source-search)`):** Beacon maintains a **persistent semantic index** of
  previously-fetched source content. A worker queries this index before re-fetching, and newly-fetched sources
  are added to it continuously — so the corpus **grows daily-plus** and its contents age. Retrieval quality is
  measured on the versioned golden query set that already backs REQ-002.
- **Learned memory (drives `memory`):** Beacon persists **per-topic source-reliability signals** across sessions
  — which sources proved authoritative for which subject areas — so worker routing and grounding **improve on
  repeat questions in the same domain**. These signals are **operator-correctable**, and raw fetched content is
  not memory (it lives in the retrieval index cache under its own freshness policy).
- **Operator profiles (drives `memory`):** per-operator research-interest profiles personalize source routing on
  repeat use. Profiles are personal data, and operators **may request deletion of their profile**.
```

`agent-contract.md` §6: replace the two existing bullets with:

```markdown
- **Persists across sessions:** (a) the retrieval index cache of fetched source content (under its own freshness
  policy — an infrastructure cache, not "memory"); (b) per-topic source-reliability signals (operator-correctable);
  (c) per-operator research-interest profiles (deletable on operator request). See `architecture-constraints.md`
  § Data architecture.
- **Never persists:** raw fetched source content beyond the index cache's freshness policy; any reliability or
  profile signal derived from a source's self-description rather than Beacon's own admission outcomes.
```

- [ ] **Step 3: `beacon-nogate` — edit 2 files (agent-contract.md stays VERBATIM — the design pins this).**
`specification.md`: insert after the Profile line:

```markdown
- **Data:** retrieval(handbook-lookup) · memory   <!-- data-module routing; see shared/agentic-profile.md § The Data line. -->
```

`architecture-constraints.md`: append:

```markdown

## Data architecture

> Declaration-truth for Beacon's data needs. The `Data:` line in `specification.md` routes these to skill 03's
> data modules; the need-gate still decides whether each module is warranted (03's data craft, §0).

- **Reference handbook (candidate for `retrieval(handbook-lookup)`):** operators keep a small internal source
  handbook — ~40 short, stable reference documents, revised roughly quarterly — that a research run may consult.
  It fits comfortably in a model context window and sees low query volume.
- **Cross-session learning (candidate for `memory`):** each research question is independent and self-contained.
  Operators explicitly value a from-scratch read on every question (reproducibility of the research method); no
  personalization, no repeat-topic learning, and no cross-session accumulated state is wanted.
```

- [ ] **Step 4: Fixture sanity — grade the pure seeds.** For each case, seed a scratch workspace from the fixture
and grade it: every realization check must FAIL (the grader is not vacuous on a bare spine) while the
capabilities check PASSES (seed == fixture):

```bash
mkdir -p /tmp/fx-sanity/dm && cp -r .agents/skills/03-architect/evals/fixtures/beacon-data/docs /tmp/fx-sanity/dm/docs
python .agents/skills/03-architect/evals/check_architecture.py --outputs /tmp/fx-sanity/dm --case data-modules
mkdir -p /tmp/fx-sanity/ng && cp -r .agents/skills/03-architect/evals/fixtures/beacon-nogate/docs /tmp/fx-sanity/ng/docs
python .agents/skills/03-architect/evals/check_architecture.py --outputs /tmp/fx-sanity/ng --case data-nogate
```
Expected `data-modules`: 2/14 (capabilities + S18-N/A pass; all realization checks fail). Expected `data-nogate`:
5/11 (capabilities, S18-N/A, selectivity, amendment-bound pass on the empty tree; core realization + T01 + T04
fail). Exact counts recorded in VALIDATION.md.

- [ ] **Step 5: Commit** — `feat(03-evals): beacon-data + beacon-nogate fixture trees (enriched / denial facts)`.

---

### Task 11: `evals.json` + README

**Files:**
- Modify: `.agents/skills/03-architect/evals/evals.json`, `.agents/skills/03-architect/evals/README.md`

- [ ] **Step 1: Append the two case entries** to the `"evals"` array (after id 3):

```json
    {
      "id": 4,
      "name": "data-modules",
      "prompt": "The Beacon spec spine is already in docs/spec/ (Profile: agent-system; the Data: line declares retrieval(source-search) · grounded-writes(report-synthesis) · memory), with the sprint-1 slice in docs/planning/sprints/sprint-01.md. Run the architect: `03-architect init` then `03-architect sprint 1`. Realize the system architecture under docs/architecture/ and run the Reconcile pass against docs/spec/architecture-constraints.md, whose ## Data architecture section states the declared data needs.",
      "expected_output": "The focused data contract: system.md + ADR registry + >=1 feature spec with a Verification Contract; every declared Data: value realized (DA-T01); an eval-suite VC row whose golden-set dataset ref resolves on disk (DA-T02); a named write-path admission rule (DA-T03); a datastore ADR walking the seven-dimension rubric (DA-T04); retrieval clauses — stage, chunking or no-chunking rationale, dims + reindex trigger, k-consistency (DA-T05); grounding clauses — named ground-truth source, numeric threshold + action, fallback (DA-T06); a Category: memory ADR with the Gate-0 trigger cited, per-kind substrate, lifecycle floor, sharing+authz named together, and — because the spine promises operator profile deletion — the deletion=>derived-reach pairing (DA-T07); volatile-class picks carry resolving Verified-against citations (DA-T08 via S18). docs/spec/capabilities/ is untouched.",
      "files": ["evals/fixtures/beacon-data/docs/**"],
      "assertions": [
        "system.md written; ADR registry + index; valid amendment-log.json; context attestation recorded",
        "A feature spec references the sprint's REQs and carries a Verification Contract",
        "Spine integrity: docs/spec/capabilities/** content-identical to the fixture",
        "DA-T01: every declared Data: value appears in the realization",
        "DA-T02: an eval-suite VC row whose golden-set dataset ref resolves on disk",
        "DA-T03: a named write-path admission rule (chain + admit/commit)",
        "DA-T04: a datastore ADR walks the rubric (alternatives, driver REQ + dimension, symptom Review-Trigger, exit-cost, durable-vs-vendor)",
        "DA-T05: retrieval content clauses (stage, chunking, dims + reindex, k-consistency)",
        "DA-T06: grounding content clauses (ground-truth source, threshold + action, fallback; driver-layer conditional)",
        "DA-T07: memory content clauses (Gate-0, per-kind substrate, lifecycle, sharing+authz, deletion=>derived-reach)",
        "DA-T08/S18: verify-live ADR citations resolve (post label-normalization)"
      ]
    },
    {
      "id": 5,
      "name": "data-nogate",
      "prompt": "The Beacon spec spine is already in docs/spec/ (Profile: agent-system; the Data: line declares retrieval(handbook-lookup) · memory), with the sprint-1 slice in docs/planning/sprints/sprint-01.md. Run the architect: `03-architect init` then `03-architect sprint 1`. Realize the system architecture under docs/architecture/ and run the Reconcile pass against docs/spec/architecture-constraints.md, whose ## Data architecture section states the project's data facts.",
      "expected_output": "The need-gate selectivity direction: the ## Data architecture facts deny every trigger (the handbook fits in context — Stage 0; no cross-session learning is wanted — no Gate-0 trigger), so the correct realization DECLINES both declared modules with stated reasons (absence is correct, not a gap): no retrieval or memory substrate commitment appears in the structured loci (Data-model/Components rows), at most one amendment row (a line-narrowing proposal is defensible), while the always-on datastore rubric still yields a DA-T04-compliant ADR and the structural core (system.md, ADR registry, spec + VC, attestation) is intact. grounded-writes is undeclared and not asserted either way.",
      "files": ["evals/fixtures/beacon-nogate/docs/**"],
      "assertions": [
        "system.md written; ADR registry + index; valid amendment-log.json; context attestation recorded",
        "A feature spec references the sprint's REQs and carries a Verification Contract",
        "Spine integrity: docs/spec/capabilities/** content-identical to the fixture",
        "DA-T01: both declared values are addressed (explicit decline counts; silent omission fails)",
        "DA-T04: the always-on datastore ADR walks the rubric",
        "Selectivity: no retrieval/memory substrate commitment in Data-model/Components table rows",
        "False-positive bound: <=1 amendment row",
        "DA-T08/S18: N/A or resolving citations (no verify-live tech is expected on a declined line)"
      ]
    }
```
Also update the top-level `"note"` field: append one sentence — `"Cases 4-5 (data-modules / data-nogate) grade the
data-architecture craft through the focused grade_data_arch path — design record:
_artifacts/data-architecture-phase1-design.md."`

- [ ] **Step 2: README.** (a) Under the `## iteration-1` heading, insert immediately after the heading line:

```markdown
> **Stale-baseline note (2026-07-19):** the table below predates WS4 (D1–D6) and WS6 (S18), which grew the grader
> to **21 checks/case** — it is history, not the current baseline. The current baseline is the 2026-07-18
> re-baseline below.
```

(b) After the iteration-1 section, append:

```markdown
## Re-baseline (2026-07-18, /21 grader)

Fresh with_skill arms on the current 21-check grader (the data-architecture regression bridge; design record §7.1):

| Case | with_skill |
|------|:----------:|
| `clean-constraint` | 20/21 |
| `forbidden-token` | **21/21** |
| `underspecified-constraint` | **21/21** |

The single miss — `clean`'s D1 (one §10 quality scenario written prose-only) — is a WS4 check the data craft never
touches, confirmed run-variance (the other two arms passed D1).

## Data cases (`data-modules` · `data-nogate`)

Phase-1 calibrated cases for the data-architecture craft (DA-T01–T08; design record:
`_artifacts/data-architecture-phase1-design.md`). Beacon-derived fixtures; graded by the focused
`grade_data_arch` path (`--case data-modules|data-nogate`), validated by `--self-test` (S18 + the data mutation
suite). The `data-modules` fixture arms the DA-T07 deletion→derived-reach pairing via a spine-level deletion
promise; `data-nogate` is the need-gate selectivity direction (declared-but-denied modules must be declined, not
realized). Known gap, noted not fixed here: `--case agent` has a fixture + grader path but no `evals.json` entry.
```

- [ ] **Step 3: Validate JSON + commit**

```bash
python -c "import json; json.load(open('.agents/skills/03-architect/evals/evals.json', encoding='utf-8')); print('valid')"
git add .agents/skills/03-architect/evals/evals.json .agents/skills/03-architect/evals/README.md
git commit -m "feat(03-evals): register data-modules + data-nogate cases; README /21 re-record + data-case docs

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 12: The A/B runs (2 cases × 2 arms, sequential)

**Files:** run workspaces under `_artifacts/skills-eval/03-architect/iteration-data-1/` (gitignored; records
`git add -f`).

- [ ] **Step 1: Seed all four workspaces** (the README recipe — never pre-create `outputs/docs`):

```bash
ROOT=_artifacts/skills-eval/03-architect/iteration-data-1
printf '* text=auto eol=lf\n' > $ROOT/.gitattributes 2>/dev/null || { mkdir -p $ROOT; printf '* text=auto eol=lf\n' > $ROOT/.gitattributes; }
for pair in "data-modules beacon-data" "data-nogate beacon-nogate"; do
  set -- $pair
  for arm in with_skill baseline; do
    mkdir -p "$ROOT/$1/$arm/outputs"
    cp -r ".agents/skills/03-architect/evals/fixtures/$2/docs" "$ROOT/$1/$arm/outputs/docs"
  done
done
```

- [ ] **Step 2: Run the four arms, one at a time,** each a native Agent-tool `general-purpose` subagent,
`model: sonnet`, synchronous. **with_skill prompt** (substitute `<WT>` = the worktree's absolute path, `<CASE>` =
the case name):

```text
You are running a Fullstack Director skill-evaluation arm.
FRAMEWORK ROOT: <WT> — resolves .agents/skills/**, shared/**, and the skill's references/ and templates/.
PROJECT ROOT: <WT>/_artifacts/skills-eval/03-architect/iteration-data-1/<CASE>/with_skill/outputs — the project
you are architecting. ALL project reads/writes happen under PROJECT ROOT.
1. Load and follow FRAMEWORK ROOT/.agents/skills/03-architect/SKILL.md IN FULL, loading its references/ files as
   it directs.
2. The project spine is at PROJECT ROOT/docs/spec/ (with the sprint slice in docs/planning/). Run
   `03-architect init`, then `03-architect sprint 1`.
3. Run autonomously past both gates: proceed without waiting for a user; approve your own batched Tier-2
   amendments so they land as `approved` rows.
4. Run the Reconcile Pass-2 judgment from a FRESH-CONTEXT reconciler subagent (subagent_type: fsd-reconciler)
   that receives ONLY the realization + the slice declarations (architecture-constraints.md + the in-scope REQ
   blocks) — never this conversation — and record its one-line context attestation in system.md §9.
5. Never edit PROJECT ROOT/docs/spec/capabilities/**. ADRs are adr/ADR-NNN.md + an adr/README.md index (max+1
   allocation). Amendment rows are AMD-NNN with source_quote and resolved_by.
6. When done, reply with a short summary only: files written, ADRs allocated, amendment rows logged.
```

**baseline prompt** (same PROJECT ROOT, `baseline` arm dir):

```text
You are an expert software architect.
PROJECT ROOT: <WT>/_artifacts/skills-eval/03-architect/iteration-data-1/<CASE>/baseline/outputs. The project's
spec is at PROJECT ROOT/docs/spec/ (sprint slice in docs/planning/). Ignore any framework or skill files
elsewhere in the repository — do not read .agents/** or shared/**.
Produce the sprint-1 system architecture under PROJECT ROOT/docs/architecture/: a system overview (system.md),
architecture decision records, and per-feature specs with verification, honoring
docs/spec/architecture-constraints.md (including its ## Data architecture section). Record any spec conflicts or
gaps you find in docs/spec/amendment-log.json. Do not edit docs/spec/capabilities/**. Reply with a short summary
only.
```
(The case prompts in `evals.json` stay the canonical task statement; these wrappers add only harness mechanics —
no teeth, no check hints.)

- [ ] **Step 3: Grade all four + build the viewer**

```bash
for c in data-modules data-nogate; do for arm in with_skill baseline; do
  python .agents/skills/03-architect/evals/check_architecture.py \
    --outputs "$ROOT/$c/$arm/outputs" --case "$c"
  cp "$ROOT/$c/$arm/outputs/grading.json" "$ROOT/$c/$arm/grading.json"
done; done
python "<home>/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/skill-creator/eval-viewer/generate_review.py" \
  "$ROOT" --skill-name 03-architect --static _artifacts/skills-eval/03-architect/data-eval-review.html
```

- [ ] **Step 4: Triage before recording.** Success criteria (design §8): with_skill passes every non-N/A check on
both cases; baselines fail the pairing/content discriminators. **Any check a correct arm fails is a grader bug
first:** reproduce it as a `_self_test_data` scenario, fix the check, re-run `--self-test` + re-grade — never
tweak fixtures to fit an arm, and grep any fix's diff for arm-output verbatims before accepting it (the
anti-tautology discipline). A with_skill DOCTRINE failure (the arm didn't do what the teeth demand) is a finding
for the design record, not a grader edit.

- [ ] **Step 5: Record + commit.** Extend `$ROOT/VALIDATION.md` into the run record (scores table, N/A-by-design
list, baseline-gap summary, any triage), append the iteration table to the README's Data-cases section
(`| data-modules | N/14 | N/14 |`-style), then:

```bash
git add -f _artifacts/skills-eval/03-architect/iteration-data-1/VALIDATION.md
git add .agents/skills/03-architect/evals/README.md
git commit -m "test(03-evals): data-case A/B — with_skill vs baseline results + run record

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 13: Wrap-up — anti-tautology sweep + final gates

**Files:** none (verification + the stop).

- [ ] **Step 1: Anti-tautology grep over the whole branch diff**

```bash
git diff main...HEAD -- .agents shared | grep -nE \
  "Source Index snapshot|CitationGate|source_reliability|ReliabilityRouter|ReliabilityConsolidator|synthesis-grounding|pg_duckdb"
```
Audit every hit: **allowed homes** = self-test tree content (real-output-shaped by design) and fixture
declaration text; **disallowed** = any `check()` pass-condition/regex (a grader requiring a smoke coinage grades
the calibration set, not the doctrine). `CitationGate` in the ideal-tree spec content is expected; anywhere in a
check regex it is a defect — remove it.

- [ ] **Step 2: Final self-test + JSON gates**

```bash
python .agents/skills/03-architect/evals/check_architecture.py --self-test
python -c "import json; json.load(open('.agents/skills/03-architect/evals/evals.json', encoding='utf-8')); print('valid')"
git status --short
```
Expected: both self-tests `ALL GOOD`; JSON valid; working tree clean (everything committed on
`worktree-data-eval-cases`).

- [ ] **Step 3: STOP — report and ask.** Summarize: commits on the branch, the A/B table, the S18 flip, any
demotions/triage. **Do not merge to `main`, do not push (no remote exists) — ask the user for the merge
decision.** Post-merge follow-ups to name in the report: the full-suite regression posture (existing cases proven
by the Task-9 re-grades; a live full-suite re-run is a user call), and the memory-file update for
`project_data_architecture_gap`.

---

## Self-review record (writing-plans checklist)

- **Spec coverage:** design §2 decisions → Tasks 4–8 (suite shape, self-test-degenerate home), Task 10
  (enriched fixture); §3 scope table → Tasks 2–11 file-for-file; §5 keying + both principles → Tasks 4–8; §6
  ladder → Tasks 2/4–8 (self-tests) + 9 (real outputs, saved-tree re-grades) + 13 (anti-tautology); §7 fixes →
  Tasks 2–3 (S18) + 11 (README, agent-gap note); §8 run plan → Task 12; §9 tightenings → Task 4 (`_norm`
  content-identical), Tasks 5–8 (mutation-style degenerates), Task 10 (fixture coherence both directions), Task 4
  core (spec+VC check). No uncovered spec section.
- **Placeholder scan:** none — every step carries code, exact paths, or exact expected output. The Task-4 stubs
  are explicit scoped scaffolding removed by Tasks 5–8.
- **Type consistency:** `grade_data_arch(root, reqs, case, fixture_docs)` consistent across Tasks 4/7/9–12;
  `grade_da_t02(root, blob)` / `grade_da_t03(blob)` / `grade_nogate(rows, sb)` match their call sites;
  `expect(name, res, key, want_passed)` uniform; `DATA_FIXTURES` names = fixture dirs = `--case` values.
