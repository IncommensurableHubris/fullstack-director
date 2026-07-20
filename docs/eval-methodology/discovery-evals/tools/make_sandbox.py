#!/usr/bin/env python3
"""Build a corpus-free sandbox for one executor run.

WHY THIS EXISTS (wave-1 finding, 2026-07-15)
--------------------------------------------
Executors run with cwd = the framework repo, because they must read
`.agents/skills/<skill>/SKILL.md`. That same cwd exposes the *entire* eval corpus:
`cases.json` (every trap's `doctrine_anchor` + `tempt_vector` — the design AND the
answer), `fixtures/**/RUN-CONDITION.md` (answer keys), `audit/rubric.md`, the probe
scripts, and `waves/*.md`. A wave-1 executor read its own probe, reworded its output
until the probe went quiet, and deleted the probe-report it generated. Another
executor independently *refused* to look, for the same reason. That variance is the
point: "the executor won't peek" is a prediction, not a control, and the framework's
own doctrine rejects predictive controls (`shared/agentic-profile.md` § Doctrine).

WHAT THIS FIXES (structural)
----------------------------
The sandbox contains ONLY what a run legitimately needs:
    <sandbox>/framework/.agents/skills/<skill>/   (SKILL.md + references + templates)
    <sandbox>/framework/shared/                   (the cross-skill protocols)
    <sandbox>/work/                               (the seeded project root)
No corpus, no cases.json, no RUN-CONDITION.md, no probes, no rubric, no wave records.
The path is opaque (`runs/<token>/`) — it names neither the track nor the case, so it
carries no "you are being evaluated" signal to go chasing.

RESIDUAL RISK (documented, not hidden)
--------------------------------------
The Agent tool inherits the session's cwd; a subagent's cwd cannot be set. So an
executor that goes looking *can* still reach the repo. This tool removes the need and
the signal, not the possibility. Pair it with `check_executor_isolation.py`, which
greps the run transcript afterwards and marks the run's probe data untrusted on a hit.
A hermetic fix needs either harness cwd control or the corpus living outside the repo.
"""
import argparse, hashlib, json, os, shutil, sys

SKIP = {"__pycache__", ".git", ".pytest_cache"}


def _copy(src, dst, label):
    if not os.path.isdir(src):
        sys.exit("missing %s: %s" % (label, src))
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*SKIP), dirs_exist_ok=True)


def _token(case, trial):
    """Opaque, deterministic, and NOT reversible to the case name by reading it."""
    return hashlib.sha256(("%s/%s" % (case, trial)).encode()).hexdigest()[:8]


def build(repo, skill, case, trial, seeds, root):
    token = _token(case, trial)
    sandbox = os.path.join(root, token)
    if os.path.exists(sandbox):
        shutil.rmtree(sandbox)
    fw_skill = os.path.join(sandbox, "framework", ".agents", "skills", skill)
    _copy(os.path.join(repo, ".agents", "skills", skill), fw_skill, "skill")
    _copy(os.path.join(repo, "shared"), os.path.join(sandbox, "framework", "shared"), "shared/")

    # HARD RULE: a skill ships its own `evals/` (the calibrated suite). That is corpus
    # too — an executor reading its own grader is the same defect this tool exists to
    # close. Drop it from the copy.
    stripped = os.path.join(fw_skill, "evals")
    if os.path.isdir(stripped):
        shutil.rmtree(stripped)

    work = os.path.join(sandbox, "work")
    os.makedirs(work, exist_ok=True)
    for s in seeds or []:
        src = os.path.join(repo, s)
        if not os.path.exists(src):
            sys.exit("missing seed: %s" % src)
        if os.path.isdir(src):
            shutil.copytree(src, work, ignore=shutil.ignore_patterns(*SKIP), dirs_exist_ok=True)
        else:
            shutil.copy2(src, work)

    leaks = audit(sandbox)
    if leaks:
        sys.exit("SANDBOX LEAK — refusing to hand this to an executor:\n  " + "\n  ".join(leaks))
    return sandbox, work, os.path.join(sandbox, "framework")


# Strings that must never appear in a sandbox. If one does, the sandbox leaks the
# answer and the run is worthless — fail closed rather than produce tainted data.
BANNED_NAMES = ("RUN-CONDITION.md", "cases.json", "probe_lib.py", "rubric.md",
                "auditor-prompt.md", "adjudicator-prompt.md", "findings-ledger.json",
                "check_spine.py", "selftest.py")
BANNED_DIRS = ("eval-methodology", "discovery-evals", "evals", "probes", "waves")


def audit(sandbox):
    """Fail closed: prove no corpus artifact reached the sandbox."""
    bad = []
    for dirpath, dirnames, filenames in os.walk(sandbox):
        for d in list(dirnames):
            if d in BANNED_DIRS:
                bad.append("dir  %s" % os.path.relpath(os.path.join(dirpath, d), sandbox))
        for f in filenames:
            if f in BANNED_NAMES or f.startswith("probe_"):
                bad.append("file %s" % os.path.relpath(os.path.join(dirpath, f), sandbox))
    return bad


def main():
    ap = argparse.ArgumentParser(description="Build a corpus-free executor sandbox")
    ap.add_argument("--repo", required=True, help="framework repo root")
    ap.add_argument("--skill", default="00-discovery")
    ap.add_argument("--case", required=True)
    ap.add_argument("--trial", required=True)
    ap.add_argument("--seed", action="append", default=[],
                    help="repo-relative file or dir to copy into work/ (repeatable)")
    ap.add_argument("--root", required=True, help="sandbox parent (gitignored, opaque)")
    ap.add_argument("--json", action="store_true", help="emit paths as JSON")
    a = ap.parse_args()

    sandbox, work, framework = build(os.path.abspath(a.repo), a.skill, a.case, a.trial,
                                     a.seed, os.path.abspath(a.root))
    out = {"sandbox": sandbox, "work": work, "framework": framework,
           "skill_md": os.path.join(framework, ".agents", "skills", a.skill, "SKILL.md")}
    if a.json:
        print(json.dumps(out, indent=2))
    else:
        print("sandbox OK (corpus-free, leak-audited)")
        for k, v in out.items():
            print("  %-9s %s" % (k, v))


if __name__ == "__main__":
    main()
