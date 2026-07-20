# Eval harness — reference copies (adapt per-skill)

These are **reference copies** of proven eval-harness scripts, carried here so the machinery is present from the first commit, but they
are **not wired up**. Each Fullstack Director skill authors its own `evals/run_*.py` + `grade_*.py` (in that
skill's own commit), derived from these patterns.

| File | Adapt for |
|------|-----------|
| `run_honesty_evals.py` | `05-reviewer` |
| `grade_honesty_reports.py` | `05-reviewer` |
| `grade_reports.py` | `05-reviewer` |
| `run_body_evals.py` | `08-refactor` |
| `grade_body_evals.py` | `08-refactor` |

## Harness lessons (do not relearn the hard way)

- **Windows:** invoke `claude.exe` (not `claude.cmd`); use threading to drain stdout/stderr pipes; force `utf-8`
  encoding; run with `--num-workers 1`.
- **Eval workspaces must live OUTSIDE `.claude/skills/**`** — `with_skill` subagents refuse to `Write` fixtures
  under that path after loading `SKILL.md`. Use a sibling `eval-workspace/...`.
- **`<SUBAGENT-STOP>` injection:** the harness injects this; it must be **relaxed** for the subagent-spawning
  skills (`05-reviewer`, `03-architect`) or their reviewer/reconciler subagents will short-circuit.
- **Grading style:** deterministic regex/JSON assertions on emitted evidence (`amendment-log.json` rows, the
  reviewer's context-attestation line) — **no LLM-judge tier**.
