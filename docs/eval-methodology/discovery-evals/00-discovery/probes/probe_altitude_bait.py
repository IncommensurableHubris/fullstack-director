#!/usr/bin/env python3
"""altitude-bait — spine-boundary Rule 2 (Gherkin altitude). Realization detail (UI click-paths,
SQL DDL, named internal patterns) must not be transcribed into docs/spec/**."""
import argparse, re
from probe_lib import Probe, find_spine_root, spine_files, cap_files, parse_blocks, read

CLICK = re.compile(r"(?i)\b(clicks?|taps?|presses?|selects?)\b.*\b(icon|button|menu|gear|tab|link|dropdown)\b")
SQL = re.compile(r"(?im)```sql|^\s*CREATE\s+TABLE\b|\bALTER\s+TABLE\b")
INTERNAL = re.compile(r"(?i)\b(redux|reducer|slice|useState|useEffect|component\b|/api/[a-z]|endpoint\s+POST|mongoose|prisma schema)\b")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outputs", required=True); ap.add_argument("--trial", default="1"); ap.add_argument("--executor", default="sonnet")
    a = ap.parse_args()
    pr = Probe("altitude-bait")
    sfiles = spine_files(a.outputs)
    joined = "\n".join(read(p) or "" for p in sfiles)
    click_hit = CLICK.search(joined)
    pr.fire("P1-ui-steps-in-gherkin", bool(click_hit), (click_hit.group(0)[:120] if click_hit else "no UI click-path in docs/spec/**"))
    sql_hit = SQL.search(joined)
    pr.fire("P2-sql-in-spine", bool(sql_hit), (sql_hit.group(0)[:80] if sql_hit else "no SQL DDL in docs/spec/**"))
    root = find_spine_root(a.outputs)
    blocks = parse_blocks(cap_files(root)) if root else {}
    int_hits = ["%s:%r" % (rid, INTERNAL.search(b["block"]).group(0)) for rid, b in blocks.items() if INTERNAL.search(b["block"])]
    pr.fire("P3-internal-pattern-in-req", bool(int_hits), ("; ".join(int_hits[:4]) if int_hits else "no named internal pattern inside a REQ block"))
    pr.emit(a.outputs, a.trial, a.executor)

if __name__ == "__main__":
    main()
