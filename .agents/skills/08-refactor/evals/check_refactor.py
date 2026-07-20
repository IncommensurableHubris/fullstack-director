#!/usr/bin/env python3
"""Deterministic grader for 08-refactor evals. Grades the two properties a strong baseline refactorer does NOT
reliably deliver — never refactor beauty, no LLM judge:

  (1) BEHAVIOR PRESERVED, provably. The pre-existing behavior oracle (test/api.test.js) is blob-SHA-UNCHANGED vs the
      pre-refactor root commit (the refactor did not rewrite the tests to fake green), `node --test` is GREEN at the
      working tree, and the suite still BITES (a single-point source mutation makes it fail). This reuses 04's
      run_node_test + mutation_kills. Polarity vs 07: 07 proves value by src/** BYTE-IDENTICAL (read-only); 08 proves
      it by src/** CHANGED (the smell is gone) WHILE behavior holds.
  (2) CORRECTLY-ROUTED RECONCILE. A code<->doc drift is fixed LOCALLY (system.md) with NO amendment row; a DECLARATION
      contradiction (a stated constraint the realization can't honor) is escalated as a Tier-2 amendment row + a
      resolving ADR. This reuses 03's amendment-row / token-in-named-field checks. The eval asserts BOTH directions.

Four cases — a two-axis F1 (act? collapse?) + the appender arm:
  needs-refactor — true smells (verbatim duplication + a dead export) + a planted system.md drift -> refactored
                   (behavior preserved), smells gone, system.md reconciled LOCALLY, ZERO amendment rows.
  clean          — the hardened app/ -> ACCEPT: src unchanged (crying-wolf guard), zero amendments, oracle green.
  reconcile      — a datastore(in-memory) vs multi-instance-scale contradiction -> a Tier-2 GATED amendment row +
                   a resolving ADR naming a client-server store (the appender; NOT a silent local edit).
  behavior-trap  — a FALSE duplication (dailyView exact-day vs cumulativeView up-to-day) the oracle pins -> the
                   tempting collapse breaks a path; 08 must PRESERVE behavior (refrain / parameterize) + keep both
                   divergent operators. Behavior-preservation as a DISCRIMINATOR, not just a gate.

Input = a seeded PRE-REFACTOR project state (build_fixture.py): a git repo whose ROOT commit carries the spine +
realization docs + a built, green, biting slice. The arm runs `08-refactor sprint 2` (or `assess`), refactors src/**,
reconciles docs, and (only for a declaration contradiction) appends docs/spec/amendment-log.json.

Usage:
    python check_refactor.py --outputs <dir> --case <needs-refactor|clean|reconcile|behavior-trap>
Writes grading.json ({"expectations":[{text,passed,evidence}]}) into --outputs and prints a report.
"""
import os, re, json, argparse, sys, subprocess, glob

try:  # keep prints from crashing a legacy (cp1252) Windows console — grading.json is always utf-8
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

results = []
def check(text, passed, evidence=""):
    results.append({"text": text, "passed": bool(passed), "evidence": str(evidence)[:400]})

def read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None


# ---------- root / docs / git ----------

def find_root(base):
    for dp, dn, fn in os.walk(base):
        if dp.replace("\\", "/").endswith("docs/spec") and "specification.md" in fn:
            return os.path.dirname(os.path.dirname(dp))
    return base

def find_doc(root, *globs):
    for g in globs:
        cands = [c for c in glob.glob(os.path.join(root, g), recursive=True) if os.path.isfile(c)]
        cands.sort(key=len)
        if cands:
            return cands[0], read(cands[0])
    return None, None

def git(root, *args):
    """Return (returncode, stdout, stderr) SEPARATELY — porcelain parsing must read stdout only, or a benign stderr
    warning (e.g. 'LF will be replaced by CRLF') pollutes a --name-only path list."""
    try:
        p = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=60)
        return p.returncode, (p.stdout or ""), (p.stderr or "")
    except Exception as e:
        return 1, "", str(e)

def root_commit(root):
    rc, out, _ = git(root, "rev-list", "--max-parents=0", "HEAD")
    return out.strip().splitlines()[0] if rc == 0 and out.strip() else None

def blob_at(root, commit, path):
    rc, out, _ = git(root, "rev-parse", f"{commit}:{path}")
    return out.strip() if rc == 0 else None

def blob_worktree(root, path):
    rc, out, _ = git(root, "hash-object", path)
    return out.strip() if rc == 0 else None

def diff_paths(root, commit, *paths):
    rc, out, _ = git(root, "diff", "--name-only", commit, "--", *paths)
    return [ln.strip().replace("\\", "/") for ln in out.splitlines() if ln.strip()] if rc == 0 else ["?"]


# ---------- node:test smoke-run + mutation (reused from 04's proven grader) ----------

SKIP_TOP = ("docs", "_artifacts", "node_modules", ".git")

def _iter_files(root):
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn
                 if os.path.relpath(os.path.join(dp, d), root).replace("\\", "/").split("/")[0] not in SKIP_TOP]
        for f in fn:
            yield os.path.join(dp, f)

def test_files(root):
    out = []
    for full in _iter_files(root):
        f = os.path.basename(full)
        rel = os.path.relpath(full, root).replace("\\", "/")
        if re.search(r"\.[cm]?js$", f) and (".test." in f or "-test." in f or "test-" in f
                                            or re.search(r"(^|/)(tests?|__tests__)/", rel)):
            out.append(full)
    return sorted(set(out))

def source_files(root):
    tests = set(test_files(root))
    return sorted({full for full in _iter_files(root)
                   if re.search(r"\.[cm]?js$", os.path.basename(full)) and full not in tests})

def run_node_test(root):
    tfs = test_files(root)
    cmd = ["node", "--test", *[os.path.relpath(t, root) for t in tfs]] if tfs else ["node", "--test"]
    try:
        p = subprocess.run(cmd, cwd=root, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=120)
    except Exception as e:
        return 1, 0, f"node --test failed to launch: {e}"
    out = (p.stdout or "") + (p.stderr or "")
    m = re.search(r"(?m)^#\s*pass\s+(\d+)", out)
    passc = int(m.group(1)) if m else len(re.findall(r"(?m)^ok\s+\d+", out))
    return p.returncode, passc, out

def suite_green(root):
    rc, passc, _ = run_node_test(root)
    return rc == 0 and passc > 0

def node_eval(root, expr):
    """Run `node -e <expr>` in the project root; return (exit, output). For behavioral probes that are robust to how
    the code was refactored (parameterized, inlined, renamed) — we check BEHAVIOR, not source syntax."""
    try:
        p = subprocess.run(["node", "-e", expr], cwd=root, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=60)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except Exception as e:
        return 1, str(e)

MUT_RULES = [
    (re.compile(r"==="), "!=="), (re.compile(r"!=="), "==="),
    (re.compile(r"(?<![=!<>])==(?!=)"), "!="), (re.compile(r"(?<![=!<>])!=(?!=)"), "=="),
    (re.compile(r">="), "<="), (re.compile(r"<="), ">="),
    (re.compile(r"(?<![-=<>])>(?![=>])"), "<"), (re.compile(r"(?<![-=<>/])<(?![=/])"), ">"),
    (re.compile(r"&&"), "||"), (re.compile(r"\|\|"), "&&"),
    (re.compile(r"\btrue\b"), "false"), (re.compile(r"\bfalse\b"), "true"),
]

def test_imported_files(root):
    """Source files a test file `require`s — mutating THESE is what proves the oracle bites. Returned as a set of
    absolute paths so mutation_kills can try them first (an untested util must not exhaust the budget)."""
    imported = set()
    for t in test_files(root):
        txt = read(t) or ""
        for m in re.finditer(r"require\(\s*['\"]([^'\"]+)['\"]\s*\)|from\s+['\"]([^'\"]+)['\"]", txt):
            spec = m.group(1) or m.group(2)
            if spec and spec.startswith("."):
                cand = os.path.normpath(os.path.join(os.path.dirname(t), spec))
                for ext in ("", ".js", ".mjs", ".cjs"):
                    if os.path.isfile(cand + ext):
                        imported.add(os.path.abspath(cand + ext))
    return imported

def mutation_kills(root, budget=40):
    """A kill = the suite (green on the original) FAILS on a single-point mutant. Robust by construction: it tries
    EVERY operator occurrence (not just the first — an agent comment like `(=== day)` must not shield the code
    operator), across files, TEST-IMPORTED FILES FIRST (an untested util must not exhaust the budget). Byte-exact
    restore (no LF/CRLF churn)."""
    if not suite_green(root):
        return False, 0, "suite not green on original — cannot assess tautology"
    imported = test_imported_files(root)
    files = sorted(source_files(root), key=lambda f: (os.path.abspath(f) not in imported, f))  # tested files first
    attempts = 0
    for f in files:
        try:
            raw = open(f, "rb").read()
        except Exception:
            continue
        original = raw.decode("utf-8", "replace")
        cands = sorted({(m.start(), m.end(), repl) for rx, repl in MUT_RULES for m in rx.finditer(original)})
        for (s, e, repl) in cands:
            if attempts >= budget:
                break
            attempts += 1
            mutated = original[:s] + repl + original[e:]
            try:
                with open(f, "wb") as fh:
                    fh.write(mutated.encode("utf-8"))
                rc, passc, _ = run_node_test(root)
                killed = not (rc == 0 and passc > 0)
            finally:
                with open(f, "wb") as fh:
                    fh.write(raw)
            if killed:
                rel = os.path.relpath(f, root).replace("\\", "/")
                return True, attempts, f"mutant '{original[s:e]}'->'{repl}' in {rel} killed the suite"
        if attempts >= budget:
            break
    return False, attempts, f"no mutant killed the suite over {attempts} attempts (tests may be tautological)"

def tests_have_assertions(root):
    blob = "\n".join(read(t) or "" for t in test_files(root))
    n = len(re.findall(r"\bassert\b|\.(strictEqual|deepStrictEqual|deepEqual|equal|ok|match|throws|rejects)\b"
                       r"|expect\s*\(", blob))
    return n, bool(test_files(root))

def src_blob(root):
    return "\n".join(read(f) or "" for f in source_files(root))


# ---------- amendment / token-in-named-field (reused from 03's proven grader) ----------

def amendments(root):
    al = read(os.path.join(root, "docs/spec/amendment-log.json"))
    if al is None:
        return None
    try:
        a = json.loads(al)
        return a.get("amendments") if isinstance(a.get("amendments"), list) else None
    except Exception:
        return None

def new_rows(root):
    """Rows present at the working tree that are NOT in the root commit (by id) — the rows THIS run appended."""
    now = amendments(root) or []
    rc = root_commit(root)
    base = []
    if rc:
        txt = git(root, "show", f"{rc}:docs/spec/amendment-log.json")[1]
        try:
            base = json.loads(txt).get("amendments", [])
        except Exception:
            base = []
    base_ids = {r.get("id") for r in base}
    return [r for r in now if r.get("id") not in base_ids]

def tier2(rows):
    return [r for r in (rows or []) if str(r.get("tier")) == "2"]

def row_blob(r):
    return json.dumps(r, ensure_ascii=False).lower()

def source_quotes(rows):
    return " ".join(str(r.get("source_quote", "")) for r in (rows or []))

DB_EMBEDDED = ["in-memory", "in memory", "embedded", "single-process", "single process", "sqlite"]
DB_CLIENT_SERVER = ["postgresql", "postgres", "redis", "mysql", "mariadb", "mongodb", "dynamodb",
                    "cockroachdb", "client-server", "client/server", "external database server", "external db server"]

def tokens_in(text, tokens):
    if not text:
        return []
    t = text.lower()
    hits = []
    for tok in tokens:
        if re.search(r"[ /-]", tok):
            if tok in t:
                hits.append(tok)
        elif re.search(r"\b" + re.escape(tok) + r"\b", t):
            hits.append(tok)
    return hits

def resolving_adr_decisions(root, rows):
    out = []
    for r in tier2(rows):
        m = re.search(r"ADR-(\d+)", str(r.get("resolved_by") or ""))
        if m:
            txt = read(os.path.join(root, "docs/architecture/adr", f"ADR-{int(m.group(1)):03d}.md")) or ""
            dm = re.search(r"##+\s*Decision\s+Outcome(.+?)(?:\n##\s|\Z)", txt, re.I | re.S)
            out.append(dm.group(1) if dm else txt)
    return out


# ---------- verdict ----------

def verdict_of(report):
    m = re.search(r"(?im)^\s*[-*]?\s*[`*]*verdict[`*]*\s*[:=]\s*[`*]*([A-Za-z]+)", report or "")
    if m:
        return m.group(1).upper()
    m = re.search(r"(?im)verdict[^A-Za-z0-9]{0,8}(CLEAN|PARTIAL|BLOCKED|ACCEPT)", report or "")
    return m.group(1).upper() if m else None


# ---------- common ----------

def grade_common(root):
    hpath, health = find_doc(root, "docs/refactoring/health-assessment*.md", "**/health-assessment*.md")
    rpath, report = find_doc(root, "docs/refactoring/refactor-report*.md", "**/refactor-report*.md")
    check("Health assessment written at docs/refactoring/health-assessment-sprint-NN.md",
          bool(health), hpath or "no health-assessment*.md under docs/refactoring/")
    check("Refactor report written at docs/refactoring/refactor-report-sprint-NN.md with a machine verdict "
          "(CLEAN/PARTIAL/BLOCKED/ACCEPT)",
          bool(report) and verdict_of(report) in ("CLEAN", "PARTIAL", "BLOCKED", "ACCEPT"),
          f"report={rpath or '—'}; verdict={verdict_of(report)}")
    check("amendment-log.json is valid JSON with an 'amendments' array",
          amendments(root) is not None, "valid" if amendments(root) is not None else "missing/invalid")
    return health, report


def grade_behavior_preserved(root, oracle="test/api.test.js"):
    """The layered behavior-preservation oracle: unchanged + green + biting + real assertions."""
    rc0 = root_commit(root)
    base_blob = blob_at(root, rc0, oracle) if rc0 else None
    now_blob = blob_worktree(root, oracle)
    unchanged = bool(base_blob) and base_blob == now_blob
    check("Behavior oracle UNCHANGED: test/api.test.js is blob-identical to the pre-refactor commit (the refactor "
          "did not rewrite its own tests to fake green)",
          unchanged, f"root blob={ (base_blob or '—')[:12] }; worktree blob={ (now_blob or '—')[:12] }")

    rc, passc, out = run_node_test(root)
    check("Behavior preserved: `node --test` is GREEN at HEAD with a positive test count (the suite still passes "
          "after the refactor)",
          rc == 0 and passc > 0, f"exit={rc}; pass={passc}; out={out.strip()[-160:]}")

    killed, attempts, desc = mutation_kills(root)
    check("Oracle BITES (anti-tautology): a single-point source mutation makes the suite FAIL — the green is a real "
          "behavior check, not vacuous",
          killed, desc)

    n_assert, has = tests_have_assertions(root)
    check("Test files carry real assertions (no assertion-free suite)",
          has and n_assert > 0, f"test files={len(test_files(root))}; assertion calls={n_assert}")


def grade_non_amender(root, expect_rows=2):
    """needs-refactor / clean / behavior-trap: a code<->doc drift stays LOCAL — the amendment log is unchanged."""
    rc0 = root_commit(root)
    spec_diff = diff_paths(root, rc0, "docs/spec") if rc0 else ["?"]
    nr = new_rows(root)
    rows = amendments(root)
    check("Reconcile stayed LOCAL: no amendment row appended and docs/spec/** unchanged (a code↔doc drift is a "
          "realization fix, not a spine amendment)",
          not nr and spec_diff == [] and rows is not None and len(rows) == expect_rows,
          f"new rows={[r.get('id') for r in nr] or 'none'}; docs/spec diff={spec_diff or 'clean'}; total rows={len(rows or [])}")


# ---------- per-case ----------

# The verbatim-duplicated block (present TWICE in the needs-refactor seed digest.js) — after Extract-Function it
# must appear ONCE. The distinctive needs-help mapping is the signature (never a bare 'duplication' word).
DUP_SIG = re.compile(r"member:\s*e\.member\s*,\s*blocker:\s*e\.blocker")

def grade_needs_refactor(root, health, report):
    grade_behavior_preserved(root)

    src = src_blob(root)
    dups = len(DUP_SIG.findall(src))
    check("Smell removed — DUPLICATION collapsed: the copy-pasted needs-help mapping now appears once, not twice "
          "(Extract Function)",
          dups <= 1, f"needs-help mapping occurrences in src={dups} (seed had 2)")

    dead_gone = "legacyDigestText" not in src
    check("Smell removed — DEAD CODE deleted: the unused `legacyDigestText` export is gone from src/**",
          dead_gone, "legacyDigestText absent from src" if dead_gone else "legacyDigestText still present in src")

    h = health or ""
    named_dup = bool(re.search(r"(?i)duplicat|copy[- ]?past|assembleTeamDigest", h))
    named_dead = bool(re.search(r"(?i)dead code|unused|legacyDigestText", h))
    named_drift = bool(re.search(r"(?i)drift|reporting\.js|documented[- ]but|phantom|does not exist|missing module", h))
    check("Health assessment NAMED the duplication (a copy-pasted assembly / assembleTeamDigest)",
          named_dup, f"named={named_dup}")
    check("Health assessment NAMED the dead code (the unused legacyDigestText / a dead export)",
          named_dead, f"named={named_dead}")
    check("Health assessment NAMED the doc↔code drift (system.md documents a src/reporting.js that was never built)",
          named_drift, f"named={named_drift}")

    sys_path, sysmd = find_doc(root, "docs/architecture/system.md")
    # The phantom is gone when no TABLE ROW (a `| ... reporting.js ... |` line) references it — a prose reconcile
    # note that mentions "removed src/reporting.js" is fine, so we check the module-inventory row, not the raw string.
    phantom_row = re.search(r"(?m)^\s*\|[^\n|]*reporting\.js[^\n|]*\|", sysmd or "")
    phantom_gone = sysmd is not None and not phantom_row
    rc0 = root_commit(root)
    sys_changed = "docs/architecture/system.md" in diff_paths(root, rc0, "docs/architecture/system.md") if rc0 else False
    check("LOCAL reconcile: system.md was corrected to the refactored code — the phantom `src/reporting.js` module "
          "row is gone and the file changed vs the pre-refactor commit",
          phantom_gone and sys_changed, f"reporting.js module-row gone={phantom_gone}; system.md changed={sys_changed}")

    grade_non_amender(root)


def grade_clean(root, health, report):
    rc0 = root_commit(root)
    src_diff = diff_paths(root, rc0, "src") if rc0 else ["?"]
    check("Crying-wolf guard: the hardened app/ is left UNCHANGED — no invented refactor (src/** byte-identical to "
          "the pre-refactor commit)",
          src_diff == [], f"src changed={src_diff or 'clean'}")

    rc, passc, _ = run_node_test(root)
    check("The suite still passes (a no-op refactor did not break the clean build)",
          rc == 0 and passc > 0, f"exit={rc}; pass={passc}")

    grade_non_amender(root)

    v = verdict_of(report)
    accept = v in ("ACCEPT", "CLEAN") or bool(re.search(r"(?i)\baccept\b|no refactor|nothing to refactor|no action|"
                                                        r"already (clean|healthy)|do not (refactor|fix)", (report or "") + (health or "")))
    check("Verdict is ACCEPT/CLEAN — the assessment concluded the code is healthy (don't fix what isn't broken)",
          accept, f"verdict={v}")


def grade_reconcile(root, health, report):
    rows = amendments(root)
    nr = new_rows(root)
    t2 = tier2(nr)
    # 1) validity — the planted contradiction is real: an embedded/in-memory datastore vs a multi-instance mandate.
    #    The tech-mandate flow amends the Datastore line, so the embedded token is preserved in the row source_quote.
    sqs = source_quotes(nr)
    emb = tokens_in(sqs, DB_EMBEDDED)
    multi = bool(re.search(r"(?i)multi[- ]?instance|stateless instances|multiple instances|load balancer|horizontal|"
                           r"shared (store|state|datastore)|single[- ]process", sqs))
    check("Validity: the amendment source_quote preserves the real contradiction — an in-memory/embedded datastore "
          "against a multi-instance / shared-store requirement",
          bool(emb) and multi, f"embedded token in source_quote={emb}; multi-instance evidence={multi}")

    # 2) the appender — a Tier-2 row, GATED (not auto-applied), citing the datastore, resolved_by an ADR.
    cites = [r for r in t2 if re.search(r"datastore|in-memory|in memory|embedded|store|single-process", row_blob(r))]
    gated = [r for r in cites if r.get("disposition") in ("gated", "approved", "pending")]
    not_auto = [r for r in cites if r.get("disposition") == "auto-applied"]
    with_adr = [r for r in gated if re.search(r"adr-\d+", str(r.get("resolved_by") or ""), re.I)]
    check("Appender: a NEW Tier-2 amendment row cites the datastore contradiction, GATED (not auto-applied), "
          "resolved_by an ADR — surfaced through the amendment channel, not a silent local edit",
          bool(with_adr) and not not_auto,
          f"new tier-2 rows={len(t2)}; citing-datastore={len(cites)}; gated+ADR={len(with_adr)}; "
          f"dispositions={[r.get('disposition') for r in cites] or 'none'}")

    # 3) tech-mandate — the resolving ADR's Decision names a client-server datastore (not still in-memory).
    adr_decs = resolving_adr_decisions(root, nr)
    adr_fixed = any(tokens_in(t, DB_CLIENT_SERVER) for t in adr_decs)
    check("Tech-mandate flow: the resolving ADR's Decision names a client-server / shared datastore (not still "
          "in-memory)",
          adr_fixed, f"resolving ADR decisions={len(adr_decs)}; names a client-server store={adr_fixed}")

    # 4) the log GREW — 08 IS an appender here (the inverse of the local-drift cases).
    check("08 acted as an APPENDER: the amendment log grew by a declaration-level row (the inverse of the "
          "local-drift cases, where it must stay unchanged)",
          bool(nr), f"new rows={[r.get('id') for r in nr] or 'none'}")

    # 5) sanity — the audit/refactor did not break the build.
    rc, passc, _ = run_node_test(root)
    check("The suite still passes (surfacing the contradiction did not break the build)",
          rc == 0 and passc > 0, f"exit={rc}; pass={passc}")


# Behavioral divergence probe — robust to ANY refactoring (parameterized predicate, inlined, renamed vars): it checks
# that dailyView (exact day) and cumulativeView (day + all before) STILL RETURN DIFFERENT results. A collapse of the
# false duplication makes the two agree -> the probe fails. (A syntactic `e.day === day` regex would false-negative a
# valid callback refactor like `(entryDay, cutoff) => entryDay === cutoff`.)
DIVERGENCE_PROBE = (
    "const d=require('./src/digest');"
    "const E=[{member:'a',day:'2026-07-02'},{member:'b',day:'2026-07-01'}];"
    "const dv=d.dailyView(E,'2026-07-02'),cv=d.cumulativeView(E,'2026-07-02');"
    "process.exit((dv&&cv&&dv.count===1&&cv.count===2)?0:1);"
)

def grade_behavior_trap(root, health, report):
    grade_behavior_preserved(root)

    rc, out = node_eval(root, DIVERGENCE_PROBE)
    check("Divergence PRESERVED (behavioral): dailyView (exact day) and cumulativeView (day + all before) still "
          "return DIFFERENT results — the false duplication was not collapsed into one shared filter",
          rc == 0, "dailyView.count==1 && cumulativeView.count==2" if rc == 0 else f"probe failed (rc={rc}): {out.strip()[-160:]}")

    grade_non_amender(root)

    # lenient recognition — the plan/report/assessment noted the two are NOT true duplicates (or refrained).
    blob = (health or "") + "\n" + (report or "")
    recognized = bool(re.search(r"(?i)not (a )?(true |real )?duplicat|not identical|look[- ]?alike|appears? duplicat|"
                                r"false duplicat|differ|divergen|cumulative|refrain|preserve.{0,20}behavior|two (distinct|different)",
                                blob))
    check("Recognition (lenient): the assessment/report noted the two look-alike paths are not true duplicates "
          "(or explicitly refrained from collapsing them)",
          recognized, f"recognition signal in health/report={recognized}")


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outputs", required=True)
    ap.add_argument("--case", required=True, choices=["needs-refactor", "clean", "reconcile", "behavior-trap"])
    a = ap.parse_args()
    root = find_root(os.path.abspath(a.outputs))
    health, report = grade_common(root)
    if a.case == "needs-refactor":
        grade_needs_refactor(root, health, report)
    elif a.case == "clean":
        grade_clean(root, health, report)
    elif a.case == "reconcile":
        grade_reconcile(root, health, report)
    else:
        grade_behavior_trap(root, health, report)

    passed = sum(1 for r in results if r["passed"])
    print("\n== check_refactor: %s — %d/%d ==" % (a.case, passed, len(results)))
    for r in results:
        print("  [%s] %s" % ("PASS" if r["passed"] else "FAIL", r["text"]))
        if not r["passed"]:
            print("         evidence: %s" % r["evidence"])
    with open(os.path.join(a.outputs, "grading.json"), "w", encoding="utf-8") as f:
        json.dump({"expectations": results}, f, indent=2)
    print("grading.json -> %s" % os.path.join(a.outputs, "grading.json"))


if __name__ == "__main__":
    main()
