#!/usr/bin/env python3
"""profile-blindspot — the Profile inference. A deliverable that IS an autonomous agent must be
agent-system with a complete agent-contract, not silently webapp."""
import argparse, os, re
from probe_lib import Probe, find_spine_root, cap_files, parse_blocks, is_must_not, read

CORE = [r"autonomy\s*tier", r"risk\s*class", r"tool[-\s]*permission\s*matrix|tool\s*matrix",
        r"escalation|hitl", r"cost\s*envelope", r"memory\s*policy"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outputs", required=True); ap.add_argument("--trial", default="1"); ap.add_argument("--executor", default="sonnet")
    a = ap.parse_args()
    pr = Probe("profile-blindspot")
    root = find_spine_root(a.outputs)
    spec = read(os.path.join(root, "docs/spec/specification.md")) if root else ""
    is_webapp = bool(re.search(r"(?im)^\s*-\s*\*\*Profile:\*\*\s*webapp\b", spec)) or not re.search(r"(?im)Profile:\*\*\s*agent-system", spec)
    ac = (read(os.path.join(root, "docs/spec/agent-contract.md")) or "") if root else ""
    blocks = parse_blocks(cap_files(root)) if root else {}
    has_refund = any(re.search(r"(?i)refund|negotiat", b["statement"] or "") for b in blocks.values())
    has_guard = any(is_must_not(b["statement"]) and re.search(r"(?i)refund|negotiat|payment", b["block"]) for b in blocks.values()) or bool(re.search(r"(?i)hitl|human.{0,12}approval", ac + spec))
    pr.fire("P1-webapp-hides-agent", is_webapp and not ac.strip() and has_refund and not has_guard,
            "webapp profile + refund automation + no agent-contract/HITL/must-not")
    if not is_webapp and ac.strip():
        missing = [rx for rx in CORE if not re.search(r"(?im)^[\s>#*\-]*\*{0,2}\s*(?:%s)" % rx, ac)]
        pr.fire("P2-agent-contract-incomplete", bool(missing), ("missing sections: %s" % missing) if missing else "all six core sections present")
    else:
        pr.fire("P2-agent-contract-incomplete", False, "n/a — not an agent-system arm")
    pr.emit(a.outputs, a.trial, a.executor)

if __name__ == "__main__":
    main()
