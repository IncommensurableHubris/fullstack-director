#!/usr/bin/env python3
"""Self-test for the discovery-evals diagnostic track.
- check_isolation(): the calibrated eval tree must be byte-identical (never perturbed by this track).
- check_probes(): (added in Phase 2) every probe fires on its degenerate, stays silent on its ideal.
Exit nonzero on any failure."""
import subprocess, sys, os, json, importlib.util

CALIBRATED = ".agents/skills/00-discovery/evals"

def _repo_root():
    p = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    return (p.stdout or "").strip()

def _git(root, args):
    p = subprocess.run(["git", "-C", root] + args, capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "")

def check_isolation():
    fails = []
    root = _repo_root()
    # tracked modifications
    rc, out = _git(root, ["diff", "--name-only", "--", CALIBRATED])
    if out.strip():
        fails.append("tracked files modified under %s:\n%s" % (CALIBRATED, out.strip()))
    # untracked additions
    rc, out = _git(root, ["status", "--porcelain", "--", CALIBRATED])
    if out.strip():
        fails.append("working-tree changes under %s:\n%s" % (CALIBRATED, out.strip()))
    return fails

PROBE_DIR = os.path.dirname(os.path.abspath(__file__))
# (case, degenerate-subdir, expect_fire, extra_args)
CASES = [
    ("altitude-bait", "degenerate", True, []), ("altitude-bait", "ideal", False, []),
    ("silent-mutation", "degenerate", True, ["--seed", "../fixtures/silent-mutation/seed"]),
    ("silent-mutation", "degenerate-mislog", True, ["--seed", "../fixtures/silent-mutation/seed"]),
    ("silent-mutation", "ideal", False, ["--seed", "../fixtures/silent-mutation/seed"]),
    ("tier-bait", "degenerate", True, ["--seed", "../fixtures/tier-bait/seed"]),
    ("tier-bait", "degenerate-integrity", True, ["--seed", "../fixtures/tier-bait/seed"]),
    ("tier-bait", "ideal", False, ["--seed", "../fixtures/tier-bait/seed"]),
    ("sycophancy-pressure", "degenerate", True, []), ("sycophancy-pressure", "ideal", False, []),
    ("contradiction-pair", "degenerate", True, []),
    ("contradiction-pair", "degenerate-dropped", True, []),
    ("contradiction-pair", "ideal", False, []),
    ("untestable-dodge", "degenerate", True, []), ("untestable-dodge", "ideal", False, []),
    ("brownfield-liar", "degenerate", True, []), ("brownfield-liar", "ideal", False, []),
    ("mode-boundary", "degenerate", True, []), ("mode-boundary", "ideal", False, []),
    ("profile-blindspot", "degenerate", True, []),
    ("profile-blindspot", "degenerate-incomplete", True, []),
    ("profile-blindspot", "ideal", False, []),
    ("injected-doc", "degenerate", True, []), ("injected-doc", "ideal", False, []),
    ("gate-bulldoze", "degenerate", True, []), ("gate-bulldoze", "middle", True, []),
    ("gate-bulldoze", "ideal", False, []),
]

def _run_probe(case, outputs, extra):
    mod_path = os.path.join(PROBE_DIR, "probe_%s.py" % case.replace("-", "_"))
    spec = importlib.util.spec_from_file_location("p_%s" % case.replace("-", "_"), mod_path)
    mod = importlib.util.module_from_spec(spec)
    import sys as _s
    argv = _s.argv; _s.argv = ["probe", "--outputs", outputs] + extra
    try:
        spec.loader.exec_module(mod); mod.main()
    finally:
        _s.argv = argv
    rep = json.load(open(os.path.join(outputs, "probe-report.json"), encoding="utf-8"))
    return any(p["fired"] for p in rep["probes"])

def check_probes():
    fails = []
    for case, sub, expect_fire, extra in CASES:
        outdir = os.path.join(PROBE_DIR, "selftest-fixtures", case, sub)
        if not os.path.isdir(outdir):
            fails.append("missing selftest fixture: %s/%s" % (case, sub)); continue
        # run from PROBE_DIR so relative --seed paths resolve
        cwd = os.getcwd(); os.chdir(PROBE_DIR)
        try:
            fired = _run_probe(case, os.path.join("selftest-fixtures", case, sub), extra)
        finally:
            os.chdir(cwd)
        if fired != expect_fire:
            fails.append("VACUITY: %s/%s expected fire=%s got fire=%s" % (case, sub, expect_fire, fired))
    return fails

def main():
    fails = check_isolation() + check_probes()
    if fails:
        print("SELFTEST FAIL:")
        for f in fails: print("  " + f)
        sys.exit(1)
    print("selftest OK — isolation clean + every probe non-vacuous")

if __name__ == "__main__":
    main()
