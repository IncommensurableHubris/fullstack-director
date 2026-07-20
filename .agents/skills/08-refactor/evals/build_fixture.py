#!/usr/bin/env python3
"""Assemble an 08-refactor eval fixture: a git repo whose ROOT commit is the PRE-REFACTOR project state — the spine
(docs/spec/**), the realization docs (docs/architecture/**), and a built, green, tested slice under src/** + test/**.
08 then refactors src/** in place; the grader (check_refactor.py) compares the working tree against this root commit.

Unlike 07 (read-only audit → src byte-identical) and 04 (build from scratch), 08 CHANGES src/** while preserving
behavior — so the fixture ships a real behavior ORACLE (test/api.test.js) that is green AND biting at the root commit;
08 must keep it green WITHOUT editing it. The clean app/ is the hardened sprint-02 surface; each case overlays files:

  needs-refactor → digest.js grows verbatim duplication + a dead export; system.md documents a phantom module
                   (a code↔doc drift). 08 must dedupe + delete dead code + reconcile system.md LOCALLY, no amendment.
  clean          → NO overlay (the hardened app/). 08 must ACCEPT — no invented refactor, no invented amendment.
  reconcile      → architecture-constraints.md gains a Datastore (in-memory) + a multi-instance Scale mandate that
                   contradict → 08 surfaces a Tier-2 amendment (amend the datastore + a resolving ADR).
  behavior-trap  → digest.js grows a FALSE duplication (dailyView === day vs cumulativeView <= day) the oracle
                   pins; a naive "de-dup" collapse breaks a path → 08 must preserve behavior (refrain / parameterize).

Commit chronology (1 commit; ROOT = HEAD = the pre-refactor state 08 receives):
  commit 1  seed: spine + realization docs + the built, tested slice (docs + src + test + package.json; .env gitignored)

Usage:
    python build_fixture.py --case <needs-refactor|clean|reconcile|behavior-trap> --out <arm-outputs-dir>
"""
import os, sys, subprocess, argparse, shutil, stat, re

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")
CASES = ["needs-refactor", "clean", "reconcile", "behavior-trap"]

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


def node_test(cwd):
    """Run `node --test`; return (exit, pass_count, output). exit -1 if node is unavailable."""
    try:
        p = subprocess.run(["node", "--test"], cwd=cwd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=120)
    except FileNotFoundError:
        return -1, 0, "node not found"
    except Exception as e:
        return 1, 0, str(e)
    out = (p.stdout or "") + (p.stderr or "")
    m = re.search(r"(?m)^#\s*pass\s+(\d+)", out)
    passc = int(m.group(1)) if m else len(re.findall(r"(?m)^ok\s+\d+", out))
    return p.returncode, passc, out


# Mutation rules mirror check_refactor.py / 04's grader — we pass the biting check if ANY single-point mutant kills
# the suite (breadth over depth), so a rule that happens to land in a comment first is simply skipped, not a false
# "not biting". (The real grader iterates files x rules with an early-exit; this is the same semantics, digest.js only.)
_MUT = [("===", "!=="), ("!==", "==="), ("<=", ">="), (">=", "<="), ("&&", "||"), ("||", "&&")]


def self_check(out):
    """The seeded oracle must be GREEN and BITING (some single-point mutation of digest.js flips it red) — a malformed
    fixture is a silent eval failure, so fail loudly here instead."""
    rc, passc, _ = node_test(out)
    if rc == -1:
        print("  [self-check] node unavailable — SKIPPED (grader will still run node)")
        return
    if not (rc == 0 and passc > 0):
        sys.exit("  [self-check] FAIL: seeded suite is not green (exit=%s pass=%s) — fix the fixture" % (rc, passc))
    dj = os.path.join(out, "src", "digest.js")
    original = open(dj, encoding="utf-8").read()
    for pat, repl in _MUT:
        i = original.find(pat)
        if i < 0:
            continue
        with open(dj, "w", encoding="utf-8") as f:
            f.write(original[:i] + repl + original[i + len(pat):])
        rc2, passc2, _ = node_test(out)
        with open(dj, "w", encoding="utf-8") as f:
            f.write(original)
        if not (rc2 == 0 and passc2 > 0):
            print("  [self-check] OK: seeded suite is green (%d tests) and biting ('%s'->'%s' mutant killed it)"
                  % (passc, pat, repl))
            return
    sys.exit("  [self-check] FAIL: seeded suite is NOT biting (no mutant killed it) — the oracle is tautological; "
             "strengthen test/api.test.js")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", required=True, choices=CASES)
    ap.add_argument("--out", required=True, help="the arm's outputs/ dir (becomes the project root); recreated fresh")
    a = ap.parse_args()
    out = os.path.abspath(a.out)
    _rmtree(out)
    os.makedirs(out)
    casedir = os.path.join(FIX, "cases", a.case)

    # 1) the spine + realization docs (base), then the built slice (hardened app/), then the case overlay.
    shutil.copytree(os.path.join(FIX, "base", "docs"), os.path.join(out, "docs"))
    for sub in ("src", "test"):
        overlay_dir(os.path.join(FIX, "app", sub), os.path.join(out, sub))
    for f in ("package.json", "package-lock.json", ".gitignore"):
        srcf = os.path.join(FIX, "app", f)
        if os.path.isfile(srcf):
            shutil.copyfile(srcf, os.path.join(out, f))
    # the case overlay — src/test code AND any docs (constraints/system.md) it replaces.
    for sub in ("src", "test", "docs"):
        overlay_dir(os.path.join(casedir, sub), os.path.join(out, sub))
    # Synthesize the gitignored .env (a FAKE session key) so a fresh clone runs, without a checked-in secret.
    with open(os.path.join(out, ".env"), "w", encoding="utf-8", newline="\n") as f:
        f.write("TEAMPULSE_SESSION_KEY=s3cr3t-tp-live-4b8f21aa90c7\n")

    # 2) one seed commit — ROOT = the pre-refactor state 08 receives.
    sh(out, "git", "init", "-q")
    sh(out, "git", "config", "user.email", "eval@local")
    sh(out, "git", "config", "user.name", "eval")
    sh(out, "git", "config", "core.autocrlf", "false")  # deterministic diffs — no LF/CRLF churn on refactor writes
    sh(out, "git", "config", "core.safecrlf", "false")
    sh(out, "git", "add", "-A")
    sh(out, "git", "commit", "-qm", "seed: pre-refactor state (spine + realization docs + built tested slice)")
    root = sh(out, "git", "rev-parse", "HEAD").stdout.strip()

    print("[%s] root(HEAD, pre-refactor)=%s" % (a.case, root[:10]))
    self_check(out)
    # Restore the working tree EXACTLY to the seed commit — the self-check's mutate/restore can leave a line-ending
    # churn (Windows text-mode write), and 08 must receive a byte-clean pre-refactor tree (the clean case asserts it).
    sh(out, "git", "checkout", "--", ".")
    print("outputs: %s" % out)


if __name__ == "__main__":
    main()
