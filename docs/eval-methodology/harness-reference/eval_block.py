#!/usr/bin/env python3
"""Shared eval-block parser (WS3) — the single parser for a REQ's `**Acceptance (eval-suite):**` block.

Authored in Task 3.3 (00-discovery + verify-script L6), reused by Task 3.7 (05-reviewer's eval-floor re-run) and
Task 5.3 (07-security's ASR metric). One home for the eval-block grammar so the seats that read it never diverge.
The canonical schema + governance (datasets in-spine, floors, classes, the bite rule) live in
`shared/agentic-profile.md`; this module only *parses* the block.

Grammar (per REQ delimited block):

    **Acceptance (eval-suite):**
    dataset:   docs/spec/evals/<domain>/<name>.jsonl   (versioned, in-spine)
    grader:    code | judge(validated) | human
    metric:    pass@k | pass^k | score
    floor:     NN%          class: regression | capability
    negatives: >=1 must-not case in the dataset

    python eval_block.py --self-test        # proves the parser against a known sample; exit 0 iff sound

Stdlib only, Python 3.8+.
"""
import re
import sys

_REQ_BLOCK = re.compile(r"###\s*(REQ-\d+):.*?(?:<!--\s*/\1\s*-->|\Z)", re.DOTALL)
_EVAL_HEAD = re.compile(r"\*\*Acceptance\s*\(eval-suite\)\s*:\*\*(.*?)(?:```|<!--\s*/REQ|\Z)", re.DOTALL | re.IGNORECASE)


def _field(body, name):
    m = re.search(r"(?im)^\s*%s\s*:\s*(.+)$" % name, body)
    return m.group(1).strip() if m else None


def parse_eval_blocks(text):
    """Every REQ eval block in `text`. Returns a list of dicts, one per REQ carrying an eval-suite acceptance:
    {req, dataset, grader, metric, floor, floor_pct, klass, negatives}. Fields absent from the block are None."""
    out = []
    for bm in _REQ_BLOCK.finditer(text or ""):
        block, req = bm.group(0), bm.group(1)
        hm = _EVAL_HEAD.search(block)
        if not hm:
            continue
        body = hm.group(1)
        dataset = _field(body, "dataset")
        if dataset:
            dataset = re.split(r"\s+", dataset.strip().strip("`"))[0]     # drop any trailing "(parenthetical)"
        floor_line = _field(body, "floor") or ""
        pct = re.search(r"(\d+(?:\.\d+)?)\s*%", floor_line)
        km = re.search(r"(?i)class\s*:\s*(regression|capability)", floor_line + " " + (_field(body, "class") or ""))
        out.append({
            "req": req,
            "dataset": dataset,
            "grader": _field(body, "grader"),
            "metric": _field(body, "metric"),
            "floor": floor_line or None,
            "floor_pct": float(pct.group(1)) if pct else None,
            "klass": km.group(1).lower() if km else None,
            "negatives": _field(body, "negatives"),
        })
    return out


_SAMPLE = """\
### REQ-008: Draft a grounded reply   (MUST)

The system SHALL draft a reply grounded in help-center articles.

**Acceptance (eval-suite):**
dataset:   docs/spec/evals/triage/grounded.jsonl   (versioned, in-spine)
grader:    judge(validated)
metric:    pass@k
floor:     92%          class: capability
negatives: >=1 must-not case in the dataset
<!-- source: "draft a reply from our help-center articles" -->
<!-- /REQ-008 -->

### REQ-009: Read a digest   (SHOULD)

WHEN a member opens the app, the system SHALL show today's digest.

**Acceptance (outcome-level):**
```gherkin
Given a generated digest
When the member opens the app
Then they see it
```
<!-- /REQ-009 -->
"""


def _self_test():
    blocks = parse_eval_blocks(_SAMPLE)
    checks = []

    def want(label, cond):
        checks.append((label, bool(cond)))

    want("exactly one eval block found (the outcome-Gherkin REQ is skipped)", len(blocks) == 1)
    b = blocks[0] if blocks else {}
    want("req id parsed", b.get("req") == "REQ-008")
    want("dataset path parsed without the parenthetical", b.get("dataset") == "docs/spec/evals/triage/grounded.jsonl")
    want("grader parsed", b.get("grader") == "judge(validated)")
    want("metric parsed", b.get("metric") == "pass@k")
    want("floor pct parsed", b.get("floor_pct") == 92.0)
    want("class parsed", b.get("klass") == "capability")
    want("negatives parsed", "must-not" in (b.get("negatives") or ""))

    ok = all(c for _l, c in checks)
    print("== eval_block.py self-test ==")
    for label, good in checks:
        print("  [%s] %s" % ("PASS" if good else "FAIL", label))
    print("\n%s" % ("ALL GOOD — the eval-block parser is sound" if ok else "SELF-TEST FAILED"))
    return ok


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(0 if _self_test() else 1)
    print(__doc__)
