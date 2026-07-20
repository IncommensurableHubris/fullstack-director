#!/usr/bin/env python3
"""Assemble a CROSS-SKILL INTEGRATION eval fixture — the seed a multi-skill chain (or a governance/pivot leg) runs
over. Unlike the per-skill unit evals (each seeds one seat's input), these fixtures seed the HEAD of a chain and the
grader (check_integration.py) asserts the COMPOSITION — the handoffs a later seat mechanically reads.

Four cases (one `check_integration.py --case` each), by mechanics:

  spec-first     — seed ONLY the comprehensive PRD.md (+ git init; root commit = the pre-chain state). The chain
                   00 intake -> 01 -> 02 -> 03 -> /status then PRODUCES the whole tree. The latent SQLite-vs-shared-
                   store Tier-2 plant rides in the PRD and must surface at 03. (Test 1.)
  governance     — seed a post-03 SHIP-ready composed state that ALSO carries a deferred amendment (AMD-003) + a
                   surviving [NEEDS CLARIFICATION] marker, so BOTH /status (routes to resolve) and 06 (BLOCKS) gate
                   the SAME chain-produced state. (Test 3.)
  spine-collapse — seed a post-03 composed state, then the driver applies an upstream PIVOT (a changed constraint)
                   and re-runs 00; the grader asserts the spine regenerates anchored to the charter JTBD with the
                   registry integral through the pivot (no shatter) + the change logged as an amendment. (Test 4.)
  isolation-chain — delegates to the 05-reviewer fixture-builder (same TeamPulse digest domain) to stage a BUILT
                   slice, so a fresh 05 dispatched from the pipeline reviews a slice it never built. (Test 2.)

Usage:
    python build_fixture.py --case <spec-first|governance|spine-collapse|isolation-chain> --out <workspace-dir>

Workspaces live OUTSIDE .agents/skills/** (e.g. _artifacts/skills-eval/integration/iteration-N/<case>/outputs/),
gitignored. The out dir becomes the project root; it is recreated fresh each run.
"""
import os, sys, subprocess, argparse, shutil, stat, re

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")
CASES = ["spec-first", "governance", "spine-collapse", "isolation-chain"]

try:  # keep prints from crashing a legacy (cp1252) Windows console
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def _rmtree(path):
    """rmtree that survives Windows read-only .git objects (git packs objects read-only; shutil.rmtree raises
    PermissionError on them — so a rebuild into an existing dir would fail without this)."""
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


def read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None


def git_init_commit(out, msg):
    """git init + one commit; ROOT = HEAD = the pre-run state. Deterministic EOL (no autocrlf churn in diffs)."""
    sh(out, "git", "init", "-q")
    sh(out, "git", "config", "user.email", "eval@local")
    sh(out, "git", "config", "user.name", "eval")
    sh(out, "git", "config", "core.autocrlf", "false")
    sh(out, "git", "config", "core.safecrlf", "false")
    sh(out, "git", "add", "-A")
    sh(out, "git", "commit", "-qm", msg)
    return sh(out, "git", "rev-parse", "HEAD").stdout.strip()


# ---------- per-case seed ----------

def seed_spec_first(out):
    """Seed ONLY the comprehensive PRD — the chain produces docs/spec, docs/planning, docs/design, docs/architecture,
    and the /status views. The pre-chain root is a repo with just PRD.md."""
    shutil.copy(os.path.join(FIX, "spec-first", "PRD.md"), os.path.join(out, "PRD.md"))
    root = git_init_commit(out, "seed: comprehensive PRD (pre-chain root)")
    self_check_spec_first(out)
    return root


def self_check_spec_first(out):
    """Fail LOUDLY if the seed is malformed — a silent bad fixture is a silent eval failure."""
    prd = read(os.path.join(out, "PRD.md"))
    if not prd:
        sys.exit("  [self-check] FAIL: no PRD.md seeded")
    low = prd.lower()
    # the latent Tier-2 plant: SQLite (embedded) mandated AND a multi-instance shared-store availability requirement.
    has_sqlite = "sqlite" in low
    has_shared = bool(re.search(r"share one datastore|shared\s+datastore", low)) and \
        bool(re.search(r"two or more|stateless instances|load balancer|worker", low))
    if not (has_sqlite and has_shared):
        sys.exit(f"  [self-check] FAIL: spec-first PRD must carry the latent Tier-2 plant "
                 f"(SQLite mandate={has_sqlite}; multi-instance shared-store={has_shared})")
    # decisive (marker-free): the PRD must resolve the two ambiguities the unit-eval spine left as markers, so the
    # chain yields a marker-free spine (the governance case is where a marker is (re)introduced on purpose).
    decisive_lock = bool(re.search(r"locks? for everyone|single team-wide lock|team-wide lock", low))
    decisive_omit = bool(re.search(r"omitted from that day's digest|is omitted", low))
    if not (decisive_lock and decisive_omit):
        sys.exit(f"  [self-check] FAIL: spec-first PRD must be DECISIVE on edit-lock + non-submitter "
                 f"(lock={decisive_lock}; omit={decisive_omit}) so 00 yields a marker-free spine")
    print("  [self-check] OK: spec-first — PRD carries the latent SQLite/shared-store Tier-2 plant; decisive "
          "(marker-free) on edit-lock + non-submitter")


IDEAL_SPEC_FIRST = os.path.join(FIX, "_ideal", "spec-first")

def _overlay(src, dst):
    """Copy every file under src on top of dst (overwriting), creating dirs as needed. The DRY primitive: the
    governance/spine-collapse seeds are the ONE canonical spec-first composed ideal + a small case overlay, never a
    hand-duplicated full tree."""
    for dp, dn, fn in os.walk(src):
        rel = os.path.relpath(dp, src)
        for f in fn:
            d = os.path.join(dst, f) if rel == "." else os.path.join(dst, rel, f)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy(os.path.join(dp, f), d)


def seed_governance(out):
    """SEED for the governance live run = the spec-first composed ideal + the governance overlay (a restored
    [NEEDS CLARIFICATION] marker on REQ-008 + a deferred AMD-003), MINUS the run-produced views (CLAUDE.md and any
    release report — /status regenerates the first, 06 produces the second). The run then does /status + 06."""
    _overlay(IDEAL_SPEC_FIRST, out)
    _overlay(os.path.join(FIX, "governance-seed"), out)
    p = os.path.join(out, "CLAUDE.md")
    if os.path.isfile(p):
        os.remove(p)
    _rmtree(os.path.join(out, "docs", "release"))
    root = git_init_commit(out, "seed: governance state (ship-ready + a deferred amendment + a surviving marker)")
    self_check_governance(out)
    return root


def self_check_governance(out):
    al = read(os.path.join(out, "docs/spec/amendment-log.json")) or ""
    try:
        import json
        rows = json.loads(al).get("amendments", [])
    except Exception:
        rows = []
    deferred = [r for r in rows if r.get("disposition") in ("pending", "deferred")]
    digest = read(os.path.join(out, "docs/spec/capabilities/digest.md")) or ""
    marker = "[NEEDS CLARIFICATION" in digest   # matches both the bare label and the `[NEEDS CLARIFICATION: …]` form
    if not deferred or not marker:
        sys.exit(f"  [self-check] FAIL: governance seed needs >=1 deferred amendment ({len(deferred)}) + a surviving "
                 f"marker (present={marker})")
    if os.path.isfile(os.path.join(out, "CLAUDE.md")) or os.path.isdir(os.path.join(out, "docs/release")):
        sys.exit("  [self-check] FAIL: governance seed must NOT carry the run-produced CLAUDE.md / docs/release "
                 "(the run's /status + 06 produce them)")
    print(f"  [self-check] OK: governance — {len(deferred)} deferred amendment(s) + a surviving marker; ship-ready "
          "spine; no run-produced views yet")


def seed_spine_collapse(out):
    """SEED for the spine-collapse live run = the spec-first composed ideal + the charter (the macro-loop anchor),
    PRE-pivot (data residency still EU-only), MINUS the run-produced /status view. The driver then applies the
    upstream pivot (EU-only -> admit a US region) and runs `00 reflect`, which regenerates the spine from the charter
    intent + logs the amendment — the grader asserts it regenerated WITHOUT shattering the registry."""
    _overlay(IDEAL_SPEC_FIRST, out)
    _overlay(os.path.join(FIX, "spine-collapse-seed"), out)   # + docs/discovery/charter.md (the anchor)
    p = os.path.join(out, "CLAUDE.md")
    if os.path.isfile(p):
        os.remove(p)
    root = git_init_commit(out, "seed: spine-collapse pre-pivot state (spine + charter; EU-only residency)")
    self_check_spine_collapse(out)
    return root


def self_check_spine_collapse(out):
    charter = read(os.path.join(out, "docs/discovery/charter.md")) or ""
    if "spread across timezones" not in charter or "stay in sync" not in charter:
        sys.exit("  [self-check] FAIL: spine-collapse seed needs the charter JTBD anchor "
                 "('spread across timezones … stay in sync')")
    ac = read(os.path.join(out, "docs/spec/architecture-constraints.md")) or ""
    if "EU region only" not in ac:
        sys.exit("  [self-check] FAIL: spine-collapse seed must be PRE-pivot (EU-only residency) — the driver applies "
                 "the pivot at run time")
    print("  [self-check] OK: spine-collapse — charter anchor present; PRE-pivot spine (EU-only residency), ready for "
          "the upstream pivot + 00 reflect")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", required=True, choices=CASES)
    ap.add_argument("--out", required=True, help="workspace dir (becomes project root); recreated fresh")
    a = ap.parse_args()
    out = os.path.abspath(a.out)
    _rmtree(out)
    os.makedirs(out)

    if a.case == "spec-first":
        root = seed_spec_first(out)
    elif a.case == "governance":
        root = seed_governance(out)
    elif a.case == "spine-collapse":
        root = seed_spine_collapse(out)
    elif a.case == "isolation-chain":
        sys.exit("  isolation-chain seeds via the 05-reviewer fixture-builder — see the integration README "
                 "(delegates to .agents/skills/05-reviewer/evals/build_fixture.py --case defective).")
    else:
        sys.exit(f"unknown case {a.case}")

    # restore the working tree exactly to the seed commit (byte-clean pre-run tree)
    sh(out, "git", "checkout", "--", ".")
    print("[%s] root(HEAD, pre-run)=%s\noutputs: %s" % (a.case, root[:10], out))


if __name__ == "__main__":
    main()
