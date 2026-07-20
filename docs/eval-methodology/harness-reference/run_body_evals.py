#!/usr/bin/env python3
"""Run the 08-refactor body evals as claude.exe subprocesses.

Layout produced under <workspace>/iteration-N/:

    eval-<name>/
      with_skill/run-1/
        project/             — fresh copy of the eval's fixture dir
        outputs/             — files newly created by the run (diffed vs fixture)
        transcript.md
        timing.json
        eval_metadata.json
      without_skill/run-1/   (same)

with_skill    — points Claude at the 08-refactor SKILL.md and runs the user prompt.
without_skill — runs the same user prompt with NO skill context (generic Claude).

The skill-creator's scripts.aggregate_benchmark reads this layout directly.

## Gate-split evals (v1.3.0+)

`eval-full-sprint` was replaced in v1.3.0 with four gate-scoped sub-evals.
Each gate eval uses its own fixture directory — the prior gates' outputs
are pre-seeded so a one-shot subagent can start mid-sprint:

    eval 2 (gate1-diagnose)   uses mock-project/               (fresh state)
    eval 4 (gate2-prepare)    uses mock-project-gate2-input/   (+ health-assessment)
    eval 5 (gate3-execute)    uses mock-project-gate3-input/   (+ char tests + ADR-004)
    eval 6 (gate4-reconcile)  uses mock-project-gate4-input/   (+ refactored services)

Evals 1 (assess) and 3 (targeted) remain single-fixture (mock-project).

Usage:
    python run_body_evals.py --iteration 3                # all 6 evals × 2 configs
    python run_body_evals.py --iteration 3 --eval 4       # gate-2 eval only
    python run_body_evals.py --eval 2 --config with_skill # single run
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
SKILL_DIR = REPO_ROOT / ".claude" / "skills" / "08-refactor"
EVALS_DIR = SKILL_DIR / "evals"
MOCK_PROJECT = EVALS_DIR / "mock-project"

# Workspace moved out of .claude/ in v1.3.1 to avoid the path heuristic:
# when the with_skill subagent loads SKILL.md from .claude/skills/08-refactor/,
# it subsequently refuses to Write to fixture project dirs that ALSO live under
# .claude/skills/** — even though --dangerously-skip-permissions is in effect.
# See RESULTS.md §v1.3.0 "Gate-split caveat" and memory:feedback_skill_eval_path_heuristic.
# The old location ( .claude/skills/08-refactor-workspace/ ) was abandoned but
# remains gitignored for anyone reproducing v1.3.0.
WORKSPACE_BASE = REPO_ROOT / "_artifacts" / "skills-eval" / "08-refactor"


EVAL_NAMES = {
    1: "eval-assess-mode",
    2: "eval-sprint-gate1-diagnose",
    3: "eval-targeted",
    4: "eval-sprint-gate2-prepare",
    5: "eval-sprint-gate3-execute",
    6: "eval-sprint-gate4-reconcile",
    7: "eval-sprint-gate2-prepare-thin",
}


# Per-eval fixture directory. Gate-scoped evals use pre-seeded fixtures so
# a one-shot subagent starts with the prior gate's outputs already in place.
EVAL_FIXTURES = {
    1: EVALS_DIR / "mock-project",
    2: EVALS_DIR / "mock-project",
    3: EVALS_DIR / "mock-project",
    4: EVALS_DIR / "mock-project-gate2-input",
    5: EVALS_DIR / "mock-project-gate3-input",
    6: EVALS_DIR / "mock-project-gate4-input",
    7: EVALS_DIR / "mock-project-gate2-input-thin",
}


def load_evals() -> list[dict]:
    with open(EVALS_DIR / "evals.json", encoding="utf-8") as f:
        return json.load(f)["evals"]


def build_with_skill_prompt(user_prompt: str, project_path: Path) -> str:
    return (
        "<SUBAGENT-STOP>\n"
        "You are a subagent executing a specific task. Do NOT invoke /status, do NOT use the Skill tool, "
        "do NOT invoke any slash commands. Read the files below and execute the 08-refactor skill directly.\n"
        "</SUBAGENT-STOP>\n\n"
        "Execute the 08-refactor skill against a simulated project. Follow these steps exactly:\n\n"
        f"1. Read the skill instructions at: {SKILL_DIR / 'SKILL.md'}\n"
        f"2. Read any referenced files you need from: {SKILL_DIR / 'references'}\n"
        f"3. Read any rules the skill references from: {REPO_ROOT / '.claude' / 'rules'}\n"
        f"4. The project under test is at: {project_path}\n"
        f"   Read: {project_path / 'CLAUDE.md'}, then explore all files under "
        f"{project_path / 'docs'} and {project_path / 'src'} plus {project_path / 'package.json'}.\n"
        f"5. Execute the user request (below) using the skill's process. Any files you write should go "
        f"inside the project dir ({project_path}) at the paths the skill prescribes "
        f"(e.g. docs/refactoring/health-assessment-SPRINT-NN.md). Do NOT write anywhere outside the project dir.\n"
        "6. If the skill has gates that normally require user approval and you are running non-interactively "
        "(you are), proceed through the gates without pausing — but document the gate decisions in your output.\n"
        "7. End with a clear session summary of what you produced.\n\n"
        "User request:\n"
        '"""\n'
        f"{user_prompt}\n"
        '"""\n'
    )


def build_without_skill_prompt(user_prompt: str, project_path: Path) -> str:
    return (
        "<SUBAGENT-STOP>\n"
        "You are a subagent executing a specific task. Do NOT invoke /status, do NOT use the Skill tool, "
        "do NOT invoke any slash commands. Respond to the user's request directly using your own judgement.\n"
        "</SUBAGENT-STOP>\n\n"
        f"The project under test is at: {project_path}\n"
        f"Explore as needed: {project_path / 'CLAUDE.md'}, files under {project_path / 'docs'} and "
        f"{project_path / 'src'}, plus {project_path / 'package.json'}.\n"
        "Any files you write in response should go inside the project dir at whatever paths you think best. "
        "Do NOT write anywhere outside the project dir.\n"
        "End with a clear session summary of what you produced.\n\n"
        "User request:\n"
        '"""\n'
        f"{user_prompt}\n"
        '"""\n'
    )


def run_single(eval_id: int, config: str, iteration: int, timeout: int) -> dict:
    evals = {e["id"]: e for e in load_evals()}
    if eval_id not in evals:
        raise SystemExit(f"eval id {eval_id} not found in evals.json")
    eval_def = evals[eval_id]
    eval_name = EVAL_NAMES[eval_id]

    workspace = WORKSPACE_BASE / f"iteration-{iteration}"
    run_dir = workspace / eval_name / config / "run-1"
    project_dir = run_dir / "project"

    fixture_dir = EVAL_FIXTURES[eval_id]
    if not fixture_dir.is_dir():
        raise SystemExit(f"fixture dir missing for eval {eval_id}: {fixture_dir}")

    run_dir.mkdir(parents=True, exist_ok=True)
    if project_dir.exists():
        shutil.rmtree(project_dir)
    shutil.copytree(fixture_dir, project_dir)

    eval_metadata = {
        "eval_id": eval_id,
        "eval_name": eval_name,
        "prompt": eval_def["prompt"],
        "expected_output": eval_def["expected_output"],
        "assertions": [
            {"text": a, "passed": None, "evidence": ""} for a in eval_def["expectations"]
        ],
    }
    (run_dir / "eval_metadata.json").write_text(
        json.dumps(eval_metadata, indent=2), encoding="utf-8"
    )

    if config == "with_skill":
        prompt = build_with_skill_prompt(eval_def["prompt"], project_dir)
    elif config == "without_skill":
        prompt = build_without_skill_prompt(eval_def["prompt"], project_dir)
    else:
        raise SystemExit(f"unknown config {config!r}")

    (run_dir / "prompt.txt").write_text(prompt, encoding="utf-8")

    claude_bin = "claude.exe" if sys.platform == "win32" else "claude"
    cmd = [
        claude_bin,
        "-p", prompt,
        "--output-format", "text",
        "--max-turns", "80",
        "--dangerously-skip-permissions",
    ]
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

    print(f"\n{'='*60}")
    print(f"RUNNING: {eval_name} / {config} (iteration {iteration})")
    print(f"  cwd: {project_dir}")
    print(f"  out: {run_dir}")
    print(f"{'='*60}")

    start = time.time()
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(project_dir),
            env=env,
            encoding="utf-8",
            errors="replace",
        )
        elapsed = time.time() - start
        result_text = proc.stdout or ""
        (run_dir / "transcript.md").write_text(
            f"## Prompt\n\n{prompt}\n\n## Output\n\n{result_text}\n",
            encoding="utf-8",
        )
        if proc.stderr:
            (run_dir / "stderr.txt").write_text(proc.stderr, encoding="utf-8")
        timing = {
            "total_duration_seconds": round(elapsed, 1),
            "exit_code": proc.returncode,
        }
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        timing = {"total_duration_seconds": round(elapsed, 1), "exit_code": -1}
        print(f"  TIMEOUT after {elapsed:.1f}s")

    (run_dir / "timing.json").write_text(json.dumps(timing, indent=2), encoding="utf-8")
    print(f"  done in {timing['total_duration_seconds']}s -- exit {timing['exit_code']}")
    return timing


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iteration", type=int, default=3)
    parser.add_argument("--eval", type=int, default=None, help="Run only this eval id (1-6)")
    parser.add_argument("--config", type=str, default=None, choices=["with_skill", "without_skill"])
    parser.add_argument("--timeout", type=int, default=1200)
    parser.add_argument(
        "--evals",
        type=str,
        default=None,
        help="Comma-separated eval ids to run (overrides --eval). Example: --evals 2,4,5,6",
    )
    args = parser.parse_args()

    if args.evals:
        eval_ids = [int(x) for x in args.evals.split(",") if x.strip()]
    elif args.eval:
        eval_ids = [args.eval]
    else:
        eval_ids = sorted(EVAL_NAMES.keys())
    configs = [args.config] if args.config else ["with_skill", "without_skill"]

    print(f"Workspace: {WORKSPACE_BASE / f'iteration-{args.iteration}'}")
    print(f"Evals: {eval_ids}  Configs: {configs}")

    for eval_id in eval_ids:
        for config in configs:
            run_single(eval_id, config, args.iteration, args.timeout)

    print("\nDone. Next step: run grade_body_evals.py then scripts.aggregate_benchmark.")


if __name__ == "__main__":
    main()
