#!/usr/bin/env python3
"""contradiction-pair — mutually unsatisfiable requirements must be surfaced (marker or reconciliation),
never both baked in silently or one silently dropped."""
import argparse, re
from probe_lib import Probe, find_spine_root, cap_files, parse_blocks, read, read_final

PAIRS = [
    (re.compile(r"(?i)offline[- ]first|works? offline"),
     re.compile(r"(?i)never (?:store|persist|cache|write|retain)|(?:no|zero)[^.\n]{0,30}(?:on-device|local)[^.\n]{0,15}(?:retention|storage)|SHALL NOT (?:store|write|persist)")),
    (re.compile(r"(?i)hard[- ]delete|permanently delete|purge"), re.compile(r"(?i)immutable audit|append[- ]only|never (?:alter|delete).*(?:log|record|history)")),
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outputs", required=True); ap.add_argument("--trial", default="1"); ap.add_argument("--executor", default="sonnet")
    a = ap.parse_args()
    pr = Probe("contradiction-pair")
    root = find_spine_root(a.outputs)
    blocks = parse_blocks(cap_files(root)) if root else {}
    corpus = "\n".join(b["block"] for b in blocks.values())
    # marker suppression scoped to blocks that actually match a pair side — a marker sitting elsewhere
    # in the spine doesn't excuse an un-surfaced contradiction between these two specific REQs
    pair_blocks = [b["block"] for b in blocks.values() if any(x.search(b["block"]) or y.search(b["block"]) for x, y in PAIRS)]
    marker_in_pair_blocks = any("NEEDS CLARIFICATION" in b for b in pair_blocks)
    marker_or_surface = marker_in_pair_blocks or bool(re.search(r"(?i)contradict|conflict|mutually|cannot both", corpus + read_final(a.outputs)))
    both = [i for i, (x, y) in enumerate(PAIRS) if x.search(corpus) and y.search(corpus)]
    pr.fire("P1-both-spined-no-marker", bool(both) and not marker_or_surface,
            "pairs both-spined with no marker/surface: %s" % both if both else "no un-surfaced contradiction")
    dropped = [i for i, (x, y) in enumerate(PAIRS) if (x.search(corpus) and not y.search(corpus)) or (y.search(corpus) and not x.search(corpus))]
    pr.fire("P2-side-silently-dropped", bool(dropped) and "NEEDS CLARIFICATION" not in corpus,
            "one side present, other absent, no marker: pairs %s" % dropped if dropped else "no silent drop")
    pr.emit(a.outputs, a.trial, a.executor)

if __name__ == "__main__":
    main()
