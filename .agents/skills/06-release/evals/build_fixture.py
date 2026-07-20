#!/usr/bin/env python3
"""Assemble a 06-release eval fixture: a git repo carrying a RELEASABLE (or blocked) project state with REAL SHAs.

06 gates on recorded state, so the fixture must be a real world: a spine (docs/spec incl. amendment-log +
architecture-constraints declaring the repo-local stand-in platform), the built+reviewed slice (src/** + test/**),
the stand-in platform scripts (scripts/deploy|health|smoke.js), a gitignored .env carrying a planted fake secret,
and 05's qa-report whose baseline/final_commit are the repo's REAL SHAs — so G5's code-identity check, the
deploy script's HEAD stamp, and the grader's diff assertions are all real (not mocked).

Commit chronology mirrors the real artifact chain:
  commit 1  seed: spine + slice docs            (baseline_commit)
  commit 2  build: src/test/scripts (+ overlay)  (final_commit — what 05 reviewed; the qa-report pins this)
  commit 3  review: the rendered qa-report        (HEAD moves; src/** identical to final_commit → G5 passes)

Usage:
    python build_fixture.py --case <clean|blocked-verdict|blocked-spine> --out <arm-outputs-dir>

`clean`           → SHIP report, terminal amendments, no markers → 06 should RELEASE via the stand-in platform.
`blocked-verdict` → a FIX REQUIRED report over a genuinely defective slice (+ the reviewer's RED test) → BLOCK.
`blocked-spine`   → a SHIP report BUT AMD-003 pending + a [NEEDS CLARIFICATION] marker → BLOCK on the spine alone.
`patch`           → the WS1 expedite lane: a certified patch record + an in-progress Patches ledger row + a SHIP
                    qa-report-patch-001.md → 06 should RELEASE with everything patch-keyed
                    (release-report-patch-001.md · tag release/patch-001 · the ledger row flipped to done).
"""
import os, sys, subprocess, argparse, shutil, stat

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")

# WS5 5.4a: 00 emits SECURITY.md at WRITE SPINE, so a post-00 project carries one at its root (06 G7 checks presence).
SECURITY_MD = """# Security Policy

> Coordinated-vulnerability-disclosure (CVD) floor for TeamPulse.

## Reporting a vulnerability

- **Contact:** security@teampulse.example (a monitored channel; do not open a public issue for a security report).
- Include the affected commit, a reproduction, and the impact you observed.

## What to expect (the CVD window)

- Acknowledgement within 3 business days; assessment + a remediation plan within 10.
- Coordinated disclosure with a default 90-day embargo; reporters credited.

## Scope

This policy governs the application code in this repository. Live-infrastructure hardening (TLS, network policy, OS
patching) is the deployment owner's responsibility — report infrastructure issues to the operator.
"""

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


def overlay(src, dst):
    if os.path.isdir(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", required=True, choices=["clean", "blocked-verdict", "blocked-spine", "patch"])
    ap.add_argument("--out", required=True, help="the arm's outputs/ dir (becomes the project root); recreated fresh")
    a = ap.parse_args()
    out = os.path.abspath(a.out)
    _rmtree(out)
    os.makedirs(out)
    casedir = os.path.join(FIX, "cases", a.case)

    # 1) seed docs: base spine + slice, then the case's docs overrides (blocked-spine: pending AMD + marker)
    shutil.copytree(os.path.join(FIX, "base", "docs"), os.path.join(out, "docs"))
    overlay(os.path.join(casedir, "docs"), os.path.join(out, "docs"))
    with open(os.path.join(out, "SECURITY.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(SECURITY_MD)  # 5.4a: the CVD-floor policy a post-00 project carries at root
    sh(out, "git", "init", "-q")
    sh(out, "git", "config", "user.email", "eval@local")
    sh(out, "git", "config", "user.name", "eval")
    sh(out, "git", "add", "-A")
    sh(out, "git", "commit", "-qm", "seed: spine + slice docs (baseline)")
    baseline = sh(out, "git", "rev-parse", "HEAD").stdout.strip()

    # 2) the built slice + the stand-in platform (+ the case's src/test overlay — blocked-verdict is defective and
    #    carries the reviewer's RED test). .env is copied but ignored by the .gitignore in the same commit.
    for sub in ("src", "test", "scripts"):
        overlay(os.path.join(FIX, "app", sub), os.path.join(out, sub))
    for f in (".gitignore", ".env"):
        shutil.copyfile(os.path.join(FIX, "app", f), os.path.join(out, f))
    for sub in ("src", "test", "scripts"):
        overlay(os.path.join(casedir, sub), os.path.join(out, sub))
    sh(out, "git", "add", "-A")
    sh(out, "git", "commit", "-qm", "build: sprint-01 slice + platform scripts (final)")
    final = sh(out, "git", "rev-parse", "HEAD").stdout.strip()

    # 3) render 05's qa-report with the REAL SHAs → docs/quality/ → commit (HEAD moves past final_commit;
    #    src/** stays identical to it — exactly the state G5 must accept)
    with open(os.path.join(casedir, "qa-report.tmpl.md"), "rb") as f:
        tmpl = f.read().decode("utf-8", "replace").replace("\r\n", "\n")
    tmpl = tmpl.replace("{{baseline_commit}}", baseline).replace("{{final_commit}}", final)
    qd = os.path.join(out, "docs", "quality")
    os.makedirs(qd, exist_ok=True)
    qa_name = "qa-report-patch-001.md" if a.case == "patch" else "qa-report-sprint-01.md"
    with open(os.path.join(qd, qa_name), "w", encoding="utf-8", newline="\n") as f:
        f.write(tmpl)
    sh(out, "git", "add", "-A")
    sh(out, "git", "commit", "-qm", "review: qa-report sprint-01 (05 output)")
    head = sh(out, "git", "rev-parse", "HEAD").stdout.strip()

    print("[%s] baseline=%s final=%s head=%s" % (a.case, baseline[:10], final[:10], head[:10]))
    print("outputs: %s" % out)


if __name__ == "__main__":
    main()
