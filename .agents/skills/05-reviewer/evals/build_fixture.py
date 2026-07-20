#!/usr/bin/env python3
"""Assemble a 05-reviewer eval fixture: a git repo with a BUILT slice (two commits) + a generated build-handoff.

05 reviews an ALREADY-BUILT slice, so — unlike 04's seed-then-build — the fixture needs a real two-commit history
(baseline = docs only; final = + src/tests) and a build-handoff carrying the REAL baseline/final SHAs, a recomputed
`spec_slice_hash`, and the test file's oracle hash. This script produces exactly that, so 05's diff-reconstruction,
oracle re-run, and hash verification are all real (not mocked). The handoff is written to _artifacts/exports/ and is
ephemeral (not committed) — the reviewer reads it from disk.

Usage:
    python build_fixture.py --case <clean|defective> --out <arm-outputs-dir>

`clean` → a sound slice, every VC honestly EXECUTED (05 should verify SHIP, ~0 findings).
`defective` → three orthogonal plants: a REQ-008 grouping bug (A), a tautological VC-01 test (B), and an uncovered
REQ-009 falsely claimed FULL (C). The handoff optimistically claims all EXECUTED — 05 must re-derive and catch them.
The `isolation` eval case reuses the `clean` fixture (it grades the attestation, not a defect).
`patch` → the WS1 patch funnel: baseline = the SHIPPED sprint-01 state (green tests + the at-lock boundary bug) +
the certified patch record + the Patches ledger row (`in-progress`); final = 04's patch fix (inclusive boundary +
the reproducing regression test). The handoff is patch-keyed (`build-handoff-patch-001.md`, `review_mode: patch`,
`spec_slice_path`/`hash` binding the PATCH RECORD — the hash payload is the record alone, no manifest half).
"""
import os, sys, subprocess, hashlib, argparse, shutil, stat


def _rmtree(path):
    """rmtree that survives Windows read-only .git objects (git packs its objects read-only, and shutil.rmtree
    raises PermissionError on them — so a fixture rebuild into an existing dir would fail without this)."""
    def onerror(func, p, exc):
        try:
            os.chmod(p, stat.S_IWRITE)
            func(p)
        except Exception:
            pass
    if os.path.exists(path):
        shutil.rmtree(path, onerror=onerror)

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")

try:  # keep prints from crashing a legacy (cp1252) Windows console
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def sh(cwd, *args):
    return subprocess.run(list(args), cwd=cwd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def norm(path):
    """EOL-normalized (LF) text of a file — the one normalization the spec_slice_hash / oracle_hash contract uses."""
    return open(path, "rb").read().decode("utf-8", "replace").replace("\r\n", "\n").replace("\r", "\n")


def spec_slice_hash(root):
    """sha256:<16 hex> over LF-normalized sprint-slice (+ manifest if present) — identical to 04's emit side and 05's
    verify side (04/references/build-handoff.md · 05/references/review-discipline.md)."""
    sprint = os.path.join(root, "docs/planning/sprints/sprint-01.md")
    manifest = os.path.join(root, "docs/design/approved/sprint-01/manifest.md")
    payload = norm(sprint)
    if os.path.isfile(manifest):
        payload += "\n" + norm(manifest)
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def patch_slice_hash(root):
    """The patch funnel's binding: the payload is the PATCH RECORD alone (no manifest half — 02 is skipped by
    construction on the expedite lane)."""
    record = os.path.join(root, "docs/planning/patches/patch-001.md")
    return "sha256:" + hashlib.sha256(norm(record).encode("utf-8")).hexdigest()[:16]


def oracle_hash(path):
    return "sha256:" + hashlib.sha256(norm(path).encode("utf-8")).hexdigest()[:12]


def overlay(src, dst):
    for dp, _dn, fn in os.walk(src):
        rel = os.path.relpath(dp, src)
        for f in fn:
            d = os.path.join(dst, f) if rel == "." else os.path.join(dst, rel, f)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy(os.path.join(dp, f), d)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", required=True, choices=["clean", "defective", "patch"])
    ap.add_argument("--out", required=True, help="the arm's outputs/ dir (becomes the project root); recreated fresh")
    a = ap.parse_args()
    out = os.path.abspath(a.out)
    _rmtree(out)
    os.makedirs(out)
    casedir = os.path.join(FIX, a.case)

    # 1) seed docs (spine + slice[, + the patch record/ledger]) [+ the patch's PRE state] → commit (baseline_commit)
    shutil.copytree(os.path.join(FIX, "base", "docs"), os.path.join(out, "docs"))
    if a.case == "patch":
        overlay(os.path.join(casedir, "docs"), os.path.join(out, "docs"))
        overlay(os.path.join(casedir, "pre"), out)   # the SHIPPED sprint-01 state 04 patched from
    sh(out, "git", "init", "-q")
    sh(out, "git", "config", "user.email", "eval@local")
    sh(out, "git", "config", "user.name", "eval")
    sh(out, "git", "add", "-A")
    sh(out, "git", "commit", "-qm", "seed: spine + slice (baseline)")
    baseline = sh(out, "git", "rev-parse", "HEAD").stdout.strip()

    # 2) add the BUILT slice (src + tests) / the patch fix → commit (final_commit)
    if a.case == "patch":
        overlay(os.path.join(casedir, "post"), out)  # the fix + the reproducing regression test
    else:
        for sub in ("src", "test"):
            s = os.path.join(casedir, sub)
            if os.path.isdir(s):
                shutil.copytree(s, os.path.join(out, sub))
    sh(out, "git", "add", "-A")
    sh(out, "git", "commit", "-qm", "build: %s slice (final)" % a.case)
    final = sh(out, "git", "rev-parse", "HEAD").stdout.strip()

    # 3) render the handoff with the REAL SHAs + recomputed hashes → _artifacts/exports/ (ephemeral, not committed)
    tmpl = norm(os.path.join(casedir, "handoff.tmpl.md"))
    slice_hash = patch_slice_hash(out) if a.case == "patch" else spec_slice_hash(out)
    tmpl = (tmpl.replace("{{baseline_commit}}", baseline)
                .replace("{{final_commit}}", final)
                .replace("{{spec_slice_hash}}", slice_hash)
                .replace("{{oracle_hash}}", oracle_hash(os.path.join(out, "test", "digest.test.js"))))
    if a.case == "patch":
        tmpl = tmpl.replace("{{patch_oracle_hash}}",
                            oracle_hash(os.path.join(out, "test", "patch-001-lock-boundary.test.js")))
    hd = os.path.join(out, "_artifacts", "exports")
    os.makedirs(hd, exist_ok=True)
    name = "build-handoff-patch-001.md" if a.case == "patch" else "build-handoff-sprint-01.md"
    with open(os.path.join(hd, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(tmpl)

    print("[%s] baseline=%s final=%s spec_slice_hash=%s" % (a.case, baseline[:10], final[:10], slice_hash))
    print("outputs: %s" % out)


if __name__ == "__main__":
    main()
