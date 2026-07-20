#!/usr/bin/env python3
"""Assemble a 07-security eval fixture: a git repo carrying a REVIEWED, DEPLOYED-shape project state whose src/**
is the audit target. 07 is a read-only static audit, so — unlike 05 (runs tests) / 06 (runs deploy) — the fixture
just needs realistic, readable code carrying (or not carrying) planted OWASP vulnerabilities, plus a spine that
gives the panel its trust-boundary + data-sensitivity context.

TeamPulse's sprint-01 domain is PURE functions with no attack surface, so this fixture extends it with a small
zero-dep node:http API (src/server.js + auth.js + store.js over the sprint-01 digest.js) — the sprint-02 delivery.
The clean `app/` is a genuinely hardened baseline (verified session auth, server-side per-team authz, SSRF
allowlist, env-var secret, no injection surface). Each case overlays specific vulnerable files:

  vuln        → 5 orthogonal, code-fixable HIGH plants (IDOR / reflected XSS / hardcoded secret / SSRF /
                slopsquat dependency)         → REMEDIATE, routed to /04-builder.
  clean       → NO overlay (the hardened app/)                                    → PASS, ~0 findings.
  block-arch  → a Critical ARCHITECTURAL flaw (client-trusted identity + role; no server-side authz layer)
                                              → BLOCK, routed to /03-architect.
  synthesis   → a single SSRF that sits in TWO readers' remits (A10 SSRF and, under 2025, A01) → the synthesizer
                must de-dupe it to ONE finding.

Commit chronology (2 commits; HEAD = the audited commit):
  commit 1  seed: spine + system.md + qa-report (docs)     (baseline)
  commit 2  build: src/** + tests + package.json (+ overlay) (HEAD — audited_commit; .env copied but gitignored)

Usage:
    python build_fixture.py --case <vuln|clean|block-arch|synthesis> --out <arm-outputs-dir>
"""
import os, sys, subprocess, argparse, shutil, stat

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")

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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", required=True, choices=["vuln", "clean", "block-arch", "synthesis"])
    ap.add_argument("--out", required=True, help="the arm's outputs/ dir (becomes the project root); recreated fresh")
    a = ap.parse_args()
    out = os.path.abspath(a.out)
    _rmtree(out)
    os.makedirs(out)
    casedir = os.path.join(FIX, "cases", a.case)

    # 1) seed docs: the spine + system.md + the SHIP qa-report → baseline commit
    shutil.copytree(os.path.join(FIX, "base", "docs"), os.path.join(out, "docs"))
    sh(out, "git", "init", "-q")
    sh(out, "git", "config", "user.email", "eval@local")
    sh(out, "git", "config", "user.name", "eval")
    sh(out, "git", "add", "-A")
    sh(out, "git", "commit", "-qm", "seed: spine + system + qa-report (sprint-02 baseline)")
    baseline = sh(out, "git", "rev-parse", "HEAD").stdout.strip()

    # 2) the built slice: the hardened app/ (src, test, package.json, package-lock, .gitignore, .env), then the
    #    case's code overlay (vuln/block-arch/synthesis replace specific src files + package.json; clean = none).
    for sub in ("src", "test"):
        overlay_dir(os.path.join(FIX, "app", sub), os.path.join(out, sub))
    for f in ("package.json", "package-lock.json", ".gitignore"):
        src_f = os.path.join(FIX, "app", f)
        if os.path.isfile(src_f):
            shutil.copyfile(src_f, os.path.join(out, f))
    # Synthesize the gitignored .env (a FAKE session key) at build time — deliberately NOT a checked-in file, so the
    # framework repo carries no `.env` (no secret-scanner noise) yet a fresh clone still reproduces the "secret lives
    # in a gitignored .env; docs record the NAME only" scenario the R3 reader + the no-secret grader check depend on.
    with open(os.path.join(out, ".env"), "w", encoding="utf-8", newline="\n") as f:
        f.write("TEAMPULSE_SESSION_KEY=s3cr3t-tp-live-4b8f21aa90c7\n")
    # case overlay — only known code paths (never the case's .gitkeep/docs)
    for sub in ("src", "test"):
        overlay_dir(os.path.join(casedir, sub), os.path.join(out, sub))
    case_pkg = os.path.join(casedir, "package.json")
    if os.path.isfile(case_pkg):
        shutil.copyfile(case_pkg, os.path.join(out, "package.json"))

    sh(out, "git", "add", "-A")
    sh(out, "git", "commit", "-qm", "build: sprint-02 HTTP API surface (audited commit)")
    head = sh(out, "git", "rev-parse", "HEAD").stdout.strip()

    print("[%s] baseline=%s audited(HEAD)=%s" % (a.case, baseline[:10], head[:10]))
    print("outputs: %s" % out)


if __name__ == "__main__":
    main()
