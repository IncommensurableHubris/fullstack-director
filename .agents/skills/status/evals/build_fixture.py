#!/usr/bin/env python3
"""Assemble a `status` eval fixture: a git repo whose ROOT commit is the PRE-STATUS project state — a realistic
mid-chain TeamPulse chain (spine docs/spec/** + planning + design + architecture + src + quality). `/status` then runs
READ-ONLY: it derives state, integrity-checks the spine, and writes ONLY the two generated views (CLAUDE.md § Current
State + AGENTS.md). The grader (check_status.py) compares the working tree against this root commit and asserts the
read-only proxy — docs/spec/** + every realization BYTE-IDENTICAL; only CLAUDE.md + AGENTS.md may change.

Polarity vs the mutating seats: 04/08 CHANGE src/**; 07 keeps src byte-identical; `status` keeps ALL of TRUTH
byte-identical and writes only the two views. So this fixture needs no behavior oracle and runs no node — it is a
pure file/JSON-state grader (03's shape). Each case is a small mutation of the base:

  healthy     → NO overlay (the clean mid-chain state; sprint-02 built + qa SHIP, no release). Integrity PASS, zero
                governance blockers → next command `/06-release sprint 2`.
  corrupted   → capabilities/api.md loses REQ-021's closing `<!-- /REQ-021 -->` delimiter (an L2 break): the registry
                still points at api.md (L1 ok) and the heading is present, but the block is no longer delimited →
                integrity FAIL naming REQ-021. A baseline eyeballing the file sees the heading and calls it present.
  blocked     → amendment-log.json gains a Tier-3 `deferred` row (AMD-003) + architecture-constraints.md gains a
                surviving `[NEEDS CLARIFICATION]` marker. Otherwise ship-ready → status must route to RESOLVE
                (/00-discovery reflect), NOT /06-release, and report the counts tied to "06 blocks".
  backlog-gap → everything downstream of discovery is removed (planning/design/architecture/src/quality), leaving the
                spine + docs/README.md. Integrity PASS, no backlog → next command `/01-planner`.
  patch-in-flight → the backlog gains a `## Patches` ledger with ONE open row (`patch-001 | REQ-009 | planned`) +
                its certified record. Otherwise the healthy state → the router must go to the patch's next seat
                (`/04-builder`, the funnel), NOT `/06-release sprint 2` (a patch-unaware router false-routes).
  patch-pressure → the Patches ledger shows THREE consecutive `done` patches (records present); no patch open.
                Route stays the normal `/06-release sprint 2`, but the A6 patch-pressure advisory must appear
                ("this cadence is a sprint — plan-sprint / consider /08-refactor assess"). Advisory, never a block.

Commit chronology (1 commit; ROOT = HEAD = the pre-status state status receives):
  commit 1  seed: the mid-chain artifact state (spine + realizations), per case.

Usage:
    python build_fixture.py --case <healthy|corrupted|blocked|backlog-gap> --out <arm-outputs-dir>
"""
import os, sys, subprocess, argparse, shutil, stat, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")
CASES = ["healthy", "corrupted", "blocked", "backlog-gap", "patch-in-flight", "patch-pressure"]

# For backlog-gap: the realization dirs/files removed to simulate "discovery done, planner not yet run".
DOWNSTREAM = ["docs/planning", "docs/design", "docs/architecture", "docs/quality", "docs/release",
              "docs/security", "docs/refactoring", "src"]

try:  # keep prints from crashing a legacy (cp1252) Windows console
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def _rmtree(path):
    """rmtree that survives Windows read-only .git objects."""
    def onerror(func, p, exc):
        try:
            os.chmod(p, stat.S_IWRITE)
            func(p)
        except Exception:
            pass
    if os.path.exists(path):
        shutil.rmtree(path, onerror=onerror)


def sh(cwd, *args):
    return subprocess.run(list(args), cwd=cwd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def overlay_dir(src, dst):
    if os.path.isdir(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)


def read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None


# ---------- registry / block parsing (mirrors check_status.py — the self-check must agree with the grader) ----------

def registry_rows(root):
    """(REQ-ID, File) rows from the specification.md registry table."""
    spec = read(os.path.join(root, "docs/spec/specification.md")) or ""
    rows = []
    for m in re.finditer(r"(?m)^\|\s*(REQ-\d+)\s*\|[^|]*\|[^|]*\|[^|]*\|\s*([^|]+?)\s*\|", spec):
        rows.append((m.group(1), m.group(2).strip()))
    return rows


def block_present(root, req, rel):
    leaf = read(os.path.join(root, "docs/spec", rel))
    if leaf is None:
        return None  # file missing
    return bool(re.search(r"(?m)^#{2,4}\s+" + re.escape(req) + r"\b", leaf)) and (f"<!-- /{req} -->" in leaf)


def markers(root):
    n = 0
    specdir = os.path.join(root, "docs/spec")
    for dp, dn, fn in os.walk(specdir):
        for f in fn:
            n += len(re.findall(r"\[NEEDS CLARIFICATION\]", read(os.path.join(dp, f)) or ""))
    return n


def amendments(root):
    try:
        return json.loads(read(os.path.join(root, "docs/spec/amendment-log.json"))).get("amendments")
    except Exception:
        return None


# ---------- per-case self-check (a malformed fixture is a silent eval failure — fail LOUDLY) ----------

def self_check(out, case):
    spec = os.path.join(out, "docs/spec/specification.md")
    if not os.path.isfile(spec):
        sys.exit("  [self-check] FAIL: no docs/spec/specification.md — the spine did not seed")
    rows = registry_rows(out)
    if len(rows) < 6:
        sys.exit(f"  [self-check] FAIL: registry parsed {len(rows)} rows (expected 6) — check the table format")

    if case == "healthy":
        bad = [f"{r}:{f}" for r, f in rows if block_present(out, r, f) is not True]
        if bad:
            sys.exit(f"  [self-check] FAIL: healthy spine is not integral — unresolved/undelimited: {bad}")
        a = amendments(out)
        pend = [x for x in (a or []) if x.get("disposition") in ("pending", "deferred")]
        if a is None or pend or markers(out):
            sys.exit(f"  [self-check] FAIL: healthy must have 0 blockers — pending/deferred={len(pend)} markers={markers(out)}")
        if os.path.isfile(os.path.join(out, "docs/release/release-report-sprint-02.md")):
            sys.exit("  [self-check] FAIL: healthy must have NO release report (so the route is /06-release sprint 2)")
        print("  [self-check] OK: healthy — spine integral, 0 governance blockers, sprint-02 at qa SHIP (no release)")

    elif case == "corrupted":
        api = read(os.path.join(out, "docs/spec/capabilities/api.md")) or ""
        heading = bool(re.search(r"(?m)^#{2,4}\s+REQ-021\b", api))
        delim = "<!-- /REQ-021 -->" in api
        if not (heading and not delim):
            sys.exit(f"  [self-check] FAIL: corrupted must have REQ-021 heading present but its closing delimiter "
                     f"REMOVED (heading={heading} delimiter={delim})")
        print("  [self-check] OK: corrupted — REQ-021 heading present, its <!-- /REQ-021 --> delimiter removed (L2 break)")

    elif case == "blocked":
        a = amendments(out)
        deferred = [x for x in (a or []) if x.get("disposition") in ("pending", "deferred")]
        m = markers(out)
        if a is None or not deferred or m < 1:
            sys.exit(f"  [self-check] FAIL: blocked must have >=1 pending/deferred amendment AND >=1 marker "
                     f"(pending/deferred={len(deferred)} markers={m})")
        # still ship-ready: integral spine + qa SHIP + no release
        bad = [f"{r}:{f}" for r, f in rows if block_present(out, r, f) is not True]
        if bad:
            sys.exit(f"  [self-check] FAIL: blocked spine must still be integral (only governance blocks) — bad={bad}")
        print(f"  [self-check] OK: blocked — {len(deferred)} deferred amendment(s) + {m} marker(s); spine integral, ship-ready")

    elif case == "backlog-gap":
        if os.path.isfile(os.path.join(out, "docs/planning/backlog.md")):
            sys.exit("  [self-check] FAIL: backlog-gap must NOT have docs/planning/backlog.md")
        bad = [f"{r}:{f}" for r, f in rows if block_present(out, r, f) is not True]
        if bad:
            sys.exit(f"  [self-check] FAIL: backlog-gap spine must still be integral — bad={bad}")
        print("  [self-check] OK: backlog-gap — spine present + integral, no backlog (route is /01-planner)")

    elif case in ("patch-in-flight", "patch-pressure"):
        backlog = read(os.path.join(out, "docs/planning/backlog.md")) or ""
        prows = re.findall(r"(?m)^\|\s*(patch-\d+)\s*\|[^|]*\|\s*([a-z-]+)\s*\|", backlog)
        recs = sorted(f for f in os.listdir(os.path.join(out, "docs/planning/patches"))
                      if re.fullmatch(r"patch-\d+\.md", f)) if os.path.isdir(os.path.join(out, "docs/planning/patches")) else []
        bad = [f"{r}:{f}" for r, f in rows if block_present(out, r, f) is not True]
        if bad:
            sys.exit(f"  [self-check] FAIL: {case} spine must be integral — bad={bad}")
        if len(prows) != len(recs):
            sys.exit(f"  [self-check] FAIL: {case} ledger rows ({len(prows)}) != records ({len(recs)})")
        if case == "patch-in-flight":
            if [s for _p, s in prows] != ["planned"]:
                sys.exit(f"  [self-check] FAIL: patch-in-flight needs exactly one OPEN row (planned) — got {prows}")
            print("  [self-check] OK: patch-in-flight — one planned patch + record; spine integral (route = /04-builder)")
        else:
            if len(prows) < 3 or any(s != "done" for _p, s in prows):
                sys.exit(f"  [self-check] FAIL: patch-pressure needs >=3 done rows, none open — got {prows}")
            if os.path.isfile(os.path.join(out, "docs/release/release-report-sprint-02.md")):
                sys.exit("  [self-check] FAIL: patch-pressure must keep sprint-02 unreleased (normal route holds)")
            print("  [self-check] OK: patch-pressure — 3 done patches, none open (route stays /06-release; A6 advisory)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", required=True, choices=CASES)
    ap.add_argument("--out", required=True, help="the arm's outputs/ dir (becomes the project root); recreated fresh")
    a = ap.parse_args()
    out = os.path.abspath(a.out)
    _rmtree(out)
    os.makedirs(out)

    # 1) the base chain, then the case overlay (corrupted/blocked replace a spine file; healthy/backlog-gap have none).
    overlay_dir(os.path.join(FIX, "base"), out)
    overlay_dir(os.path.join(FIX, "cases", a.case), out)
    # backlog-gap: strip everything downstream of discovery (leave the spine + docs/README.md).
    if a.case == "backlog-gap":
        for rel in DOWNSTREAM:
            _rmtree(os.path.join(out, rel))
    # drop any stray .gitkeep the overlay carried in.
    for dp, dn, fn in os.walk(out):
        for f in fn:
            if f == ".gitkeep":
                os.remove(os.path.join(dp, f))

    # 2) one seed commit — ROOT = HEAD = the pre-status state status receives.
    sh(out, "git", "init", "-q")
    sh(out, "git", "config", "user.email", "eval@local")
    sh(out, "git", "config", "user.name", "eval")
    sh(out, "git", "config", "core.autocrlf", "false")  # deterministic diffs — no LF/CRLF churn
    sh(out, "git", "config", "core.safecrlf", "false")
    sh(out, "git", "add", "-A")
    sh(out, "git", "commit", "-qm", "seed: pre-status mid-chain state (spine + realizations)")
    root = sh(out, "git", "rev-parse", "HEAD").stdout.strip()

    print("[%s] root(HEAD, pre-status)=%s" % (a.case, root[:10]))
    self_check(out, a.case)
    # Restore the working tree EXACTLY to the seed commit (byte-clean pre-status tree — the read-only proxy asserts it).
    sh(out, "git", "checkout", "--", ".")
    print("outputs: %s" % out)


if __name__ == "__main__":
    main()
