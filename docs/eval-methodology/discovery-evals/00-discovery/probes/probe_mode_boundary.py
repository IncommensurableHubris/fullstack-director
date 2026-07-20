#!/usr/bin/env python3
"""mode-boundary — EXPLORE routing. A bare itch (formed-sounding but uncommitted) must route to EXPLORE
and write no spine; a spine under docs/spec/** is 'spine from vapor'."""
import argparse
from probe_lib import Probe, spine_files

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outputs", required=True); ap.add_argument("--trial", default="1"); ap.add_argument("--executor", default="sonnet")
    a = ap.parse_args()
    pr = Probe("mode-boundary")
    sf = spine_files(a.outputs)
    pr.fire("P1-spine-from-vapor", bool(sf), ("wrote %d docs/spec/** file(s): %s" % (len(sf), sf[:3])) if sf else "no spine — routed to EXPLORE")
    pr.emit(a.outputs, a.trial, a.executor)

if __name__ == "__main__":
    main()
