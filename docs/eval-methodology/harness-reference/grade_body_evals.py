#!/usr/bin/env python3
"""Grade 08-refactor body-eval runs via LLM-judge claude.exe subprocesses.

Reads the skill-creator grader.md format and produces grading.json per run
with the exact schema the aggregator expects.

For each run directory under <workspace>/iteration-N/eval-*/<config>/run-1/:
  - Spawns `claude.exe -p` with a grader prompt
  - Prompt includes: the original user prompt, the assertions list, path to
    the transcript, and path to the project/ dir (where the subagent's output
    files live — newly created files diff'd vs the mock-project baseline).
  - Grader writes grading.json into the run directory.

Grading runs spawn in parallel with `--max-parallel` workers.

Usage:
    python grade_body_evals.py --iteration 2                     # grade all runs
    python grade_body_evals.py --iteration 2 --eval 1            # grade eval 1 only
    python grade_body_evals.py --iteration 2 --eval 1 --config with_skill
"""
import argparse
import concurrent.futures
import json
import os
import subprocess
import sys
import time
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
EVALS_DIR = REPO_ROOT / ".claude" / "skills" / "08-refactor" / "evals"
MOCK_PROJECT = EVALS_DIR / "mock-project"

# Workspace moved out of .claude/ in v1.3.1 — see run_body_evals.py comment.
WORKSPACE_BASE = REPO_ROOT / "_artifacts" / "skills-eval" / "08-refactor"


# Per-eval fixture dir — gate-split evals (v1.3.0+) start mid-sprint.
# Grader needs the matching fixture so "new file" diffs are computed
# against the right baseline.
EVAL_FIXTURES = {
    1: EVALS_DIR / "mock-project",
    2: EVALS_DIR / "mock-project",
    3: EVALS_DIR / "mock-project",
    4: EVALS_DIR / "mock-project-gate2-input",
    5: EVALS_DIR / "mock-project-gate3-input",
    6: EVALS_DIR / "mock-project-gate4-input",
    7: EVALS_DIR / "mock-project-gate2-input-thin",
}

EVAL_NAMES_BY_ID = {
    1: "eval-assess-mode",
    2: "eval-sprint-gate1-diagnose",
    3: "eval-targeted",
    4: "eval-sprint-gate2-prepare",
    5: "eval-sprint-gate3-execute",
    6: "eval-sprint-gate4-reconcile",
    7: "eval-sprint-gate2-prepare-thin",
}

NAME_TO_ID = {name: eid for eid, name in EVAL_NAMES_BY_ID.items()}


def build_grader_prompt(run_dir: Path, eval_metadata: dict, fixture_dir: Path) -> str:
    assertions_list = "\n".join(
        f"  {i+1}. {a['text']}" for i, a in enumerate(eval_metadata["assertions"])
    )
    return (
        "<SUBAGENT-STOP>\n"
        "You are a Grader subagent. Do NOT invoke /status, the Skill tool, or any slash commands. "
        "Read the files referenced and write grading.json.\n"
        "</SUBAGENT-STOP>\n\n"
        "You are grading a single subagent run. Follow the Grader role strictly: verdicts must cite "
        "specific evidence; superficial satisfaction is a FAIL; no partial credit.\n\n"
        f"## The eval\n\n"
        f"**User prompt given to the subagent:**\n"
        f'"""\n{eval_metadata["prompt"]}\n"""\n\n'
        f"**Expected output description:** {eval_metadata['expected_output']}\n\n"
        f"## Inputs to grade\n\n"
        f"- Transcript: `{run_dir / 'transcript.md'}` — read this fully.\n"
        f"- Project dir (files the subagent may have created/modified): `{run_dir / 'project'}`. "
        f"Compare against the STARTING fixture at `{fixture_dir}` to identify new files "
        f"and diffs. NOTE: gate-scoped evals start mid-sprint, so the fixture already contains "
        f"prior-gate artifacts (e.g. a health-assessment for gate-2 eval, char tests + ADR-004 "
        f"for gate-3 eval, refactored services for gate-4 eval). Only grade NEW/MODIFIED files "
        f"against the fixture, not against the pristine mock-project. In particular, inspect "
        f"`{run_dir / 'project' / 'docs' / 'refactoring'}` (the skill writes health assessments "
        f"and refactor reports there). Also check `tests/`, `src/tests/`, `src/`, and any ADR file "
        f"under `docs/architecture/adr/`.\n"
        f"- Timing: `{run_dir / 'timing.json'}`.\n\n"
        f"## Expectations to evaluate ({len(eval_metadata['assertions'])} total)\n\n"
        f"{assertions_list}\n\n"
        f"## Grading rules\n\n"
        "- PASS only when clear evidence ties the expectation to real substance in the transcript or output files.\n"
        "- FAIL if evidence is missing, contradictory, or superficial (e.g. correct filename but empty/generic content).\n"
        "- For 'stops after Gate 1' or similar behavioral claims: verify by absence of later-gate artifacts "
        "(no characterization tests in tests/, no src/ modifications) AND transcript language confirming the stop.\n"
        "- For 'identifies X' claims: find the exact finding in the output file, quote it.\n"
        "- For 'applies Decision Matrix' / 'token budget' / 'guardrail clustering' / 'severity scoring' — "
        "look for the *structured artifact* in the health assessment, not just the phrase. A table, a "
        "classification, a scored list. Prose mentioning the concept without using it is FAIL.\n\n"
        f"## Output\n\n"
        f"Write JSON to `{run_dir / 'grading.json'}` with this EXACT shape (the aggregator depends on it):\n\n"
        "```json\n"
        "{\n"
        '  "expectations": [\n'
        '    {"text": "<verbatim text>", "passed": true|false, "evidence": "<specific quote or file:section>"}\n'
        '  ],\n'
        '  "summary": {"passed": N, "failed": N, "total": N, "pass_rate": X.XXXX},\n'
        '  "timing": {"total_duration_seconds": <copy from timing.json>}\n'
        "}\n"
        "```\n\n"
        "Be thorough but concise in `evidence`. One sentence per assertion is enough."
    )


def grade_one(run_dir: Path, timeout: int) -> dict:
    metadata_path = run_dir / "eval_metadata.json"
    if not metadata_path.is_file():
        return {"run_dir": str(run_dir), "status": "skipped", "reason": "no eval_metadata.json"}
    eval_metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    if not (run_dir / "transcript.md").is_file():
        return {"run_dir": str(run_dir), "status": "skipped", "reason": "no transcript.md"}

    # Resolve fixture dir from the eval id in metadata (fall back to mock-project).
    eval_id = eval_metadata.get("eval_id")
    fixture_dir = EVAL_FIXTURES.get(eval_id, MOCK_PROJECT)

    prompt = build_grader_prompt(run_dir, eval_metadata, fixture_dir)
    (run_dir / "grader_prompt.txt").write_text(prompt, encoding="utf-8")

    claude_bin = "claude.exe" if sys.platform == "win32" else "claude"
    cmd = [
        claude_bin,
        "-p", prompt,
        "--output-format", "text",
        "--max-turns", "40",
        "--dangerously-skip-permissions",
    ]
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

    start = time.time()
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(REPO_ROOT),
            env=env,
            encoding="utf-8",
            errors="replace",
        )
        elapsed = time.time() - start
        (run_dir / "grader_transcript.md").write_text(
            f"## Prompt\n\n{prompt}\n\n## Output\n\n{proc.stdout or ''}\n",
            encoding="utf-8",
        )
        return {
            "run_dir": str(run_dir),
            "status": "completed",
            "exit_code": proc.returncode,
            "duration_seconds": round(elapsed, 1),
            "grading_written": (run_dir / "grading.json").is_file(),
        }
    except subprocess.TimeoutExpired:
        return {
            "run_dir": str(run_dir),
            "status": "timeout",
            "duration_seconds": round(time.time() - start, 1),
        }


def discover_runs(
    iteration: int,
    eval_filter: int | None,
    config_filter: str | None,
    evals_list: list[int] | None = None,
) -> list[Path]:
    ws = WORKSPACE_BASE / f"iteration-{iteration}"
    if not ws.is_dir():
        raise SystemExit(f"no workspace at {ws}")

    runs: list[Path] = []
    target_ids = evals_list if evals_list else (
        [eval_filter] if eval_filter else sorted(EVAL_NAMES_BY_ID.keys())
    )
    for eval_id in target_ids:
        eval_name = EVAL_NAMES_BY_ID[eval_id]
        for config in (["with_skill", "without_skill"] if not config_filter else [config_filter]):
            run = ws / eval_name / config / "run-1"
            if run.is_dir():
                runs.append(run)
    return runs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iteration", type=int, default=3)
    parser.add_argument("--eval", type=int, default=None)
    parser.add_argument(
        "--evals",
        type=str,
        default=None,
        help="Comma-separated eval ids (overrides --eval). Example: --evals 2,4,5,6",
    )
    parser.add_argument("--config", type=str, default=None, choices=["with_skill", "without_skill"])
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--max-parallel", type=int, default=3,
                        help="Grader subprocess concurrency (3 is safe for most rate limits)")
    args = parser.parse_args()

    evals_list = [int(x) for x in args.evals.split(",") if x.strip()] if args.evals else None
    runs = discover_runs(args.iteration, args.eval, args.config, evals_list)
    if not runs:
        raise SystemExit("no runs to grade")

    print(f"Grading {len(runs)} run(s) with max-parallel={args.max_parallel}")
    for r in runs:
        print(f"  - {r.relative_to(REPO_ROOT)}")

    results: list[dict] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_parallel) as ex:
        futures = {ex.submit(grade_one, r, args.timeout): r for r in runs}
        for fut in concurrent.futures.as_completed(futures):
            result = fut.result()
            results.append(result)
            print(f"  {result['status']}: {result['run_dir']} "
                  f"({result.get('duration_seconds', '?')}s)")

    completed = sum(1 for r in results if r["status"] == "completed" and r.get("grading_written"))
    print(f"\nGrading complete: {completed}/{len(runs)} produced grading.json")


if __name__ == "__main__":
    main()
