#!/usr/bin/env python3
"""check_budget — the terseness invariant's shared grader helper (WS1 §B6).

Templates carry a budget header:  <!-- budget: ≤N lines ... -->  (either the whole artifact, or
"per REQ block" for capabilities files, where each `### REQ-NNN:` ... `<!-- /REQ-NNN -->` block is measured).
Graders that verify a big-producer artifact (00 spine leaves · 03 system/feature specs · 05 qa-reports ·
06 release reports · the integration grader) import this and assert the produced artifact respects the budget
its template declares.

    from check_budget import check_budget
    check_budget(artifact_path, template_path)   # None = within budget (or no budget declared); raises AssertionError

Policy (locked in the simplification review): the density signal is WARN-only in the emitted verify-spine.py
(hard-failing USERS on length invites truncation-gaming), but HARD in Layer-A graders — the framework's own
artifacts must hold the line.

Self-test:  python check_budget.py --self-test   (exit 0 iff in-budget passes, over-budget raises, no-budget no-ops)
"""
import re
import sys
import tempfile
import os


def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def parse_budget(template_text):
    """(limit, per_block) from the template's budget header, or (None, False) when it declares none."""
    m = re.search(r"<!--\s*budget:\s*[≤<=]*\s*(\d+)\s*lines?\s*(per\s+REQ\s+block)?", template_text or "", re.I)
    if not m:
        return None, False
    return int(m.group(1)), bool(m.group(2))


def check_budget(artifact_path, template_path):
    """Assert the produced artifact respects its template's declared line budget. No budget line -> no-op."""
    limit, per_block = parse_budget(_read(template_path))
    if limit is None:
        return None
    text = _read(artifact_path)
    if per_block:
        spans = [(m.group(1), m.group(0).count("\n") + 1)
                 for m in re.finditer(r"(?ms)^###\s+(REQ-\d+):.*?<!--\s*/\1\s*-->", text)]
        over = [(rid, n) for rid, n in spans if n > limit]
        assert not over, ("budget exceeded (per REQ block <= %d lines): %s in %s — likely restated methodology "
                          "or copied prose; one home per fact"
                          % (limit, ", ".join("%s=%d" % o for o in over), artifact_path))
        return None
    n = len(text.splitlines())
    assert n <= limit, ("budget exceeded: %d lines > <= %d declared by %s — likely restated methodology or "
                        "copied prose; one home per fact" % (n, limit, template_path))
    return None


def _self_test():
    tmp = tempfile.mkdtemp(prefix="budget-")
    def w(name, s):
        p = os.path.join(tmp, name)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(s)
        return p
    tmpl = w("tmpl.md", "<!-- budget: ≤5 lines -->\n# T\n")
    ok_art = w("ok.md", "a\nb\nc\n")
    over_art = w("over.md", "\n".join("line %d" % i for i in range(9)) + "\n")
    nob_tmpl = w("nob.md", "# no budget here\n")
    blk_tmpl = w("blk.md", "<!-- budget: ≤4 lines per REQ block -->\n# T\n")
    ok_blocks = w("okblk.md", "### REQ-001: a\nbody\n<!-- /REQ-001 -->\n### REQ-002: b\nbody\n<!-- /REQ-002 -->\n")
    over_blocks = w("overblk.md", "### REQ-001: a\n" + "prose\n" * 6 + "<!-- /REQ-001 -->\n")

    check_budget(ok_art, tmpl)                       # in budget -> None
    check_budget(over_art, nob_tmpl)                 # no budget declared -> no-op
    check_budget(ok_blocks, blk_tmpl)                # per-block, all inside
    for art, t in ((over_art, tmpl), (over_blocks, blk_tmpl)):
        try:
            check_budget(art, t)
        except AssertionError:
            pass
        else:
            print("SELF-TEST FAIL: over-budget artifact did not raise (%s)" % art)
            return 1
    print("check_budget self-test: ALL GOOD (in-budget passes; over-budget raises; no-budget no-ops; per-block works)")
    return 0


if __name__ == "__main__":
    sys.exit(_self_test() if "--self-test" in sys.argv else 0)
