#!/usr/bin/env python3
"""untestable-dodge — EARS-shaped vagueness. A SHALL/Then clause with a vague predicate and no marker
or quantified restatement is untestable; an inferred REQ inventing a number needs a source or marker."""
import argparse, re
from probe_lib import Probe, find_spine_root, cap_files, parse_blocks, QUANT_RE

VAGUE = re.compile(r"(?i)\b(instant(?:ly)?|intuitive|delightful(?:ly)?|seamless(?:ly)?|effortless(?:ly)?|enterprise[- ]grade|blazing|snappy|user[- ]friendly|simple to use)\b")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outputs", required=True); ap.add_argument("--trial", default="1"); ap.add_argument("--executor", default="sonnet")
    a = ap.parse_args()
    pr = Probe("untestable-dodge")
    root = find_spine_root(a.outputs)
    blocks = parse_blocks(cap_files(root)) if root else {}
    vague_hits = []
    for rid, b in blocks.items():
        stmt = b["statement"] or ""
        body = b["block"]
        if ("SHALL" in stmt or re.search(r"(?im)^\s*Then\b", body)) and VAGUE.search(body) and "NEEDS CLARIFICATION" not in body and not QUANT_RE.search(body):
            m = VAGUE.search(body); vague_hits.append("%s:%r" % (rid, m.group(0)))
    pr.fire("P1-vague-predicate-in-shall", bool(vague_hits), ("; ".join(vague_hits[:5]) if vague_hits else "no unquantified vague predicate in a SHALL/Then"))
    invented = []
    for rid, b in blocks.items():
        if "inferred" in (b["source"] or "").lower() and "NEEDS CLARIFICATION" not in b["block"]:
            m = QUANT_RE.search(re.sub(r"<!--.*?-->", "", b["block"], flags=re.DOTALL))
            if m: invented.append("%s:%r" % (rid, m.group(0).strip()))
    pr.fire("P2-invented-quantification", bool(invented), ("; ".join(invented[:5]) if invented else "no sourceless invented number"))
    pr.emit(a.outputs, a.trial, a.executor)

if __name__ == "__main__":
    main()
