#!/usr/bin/env python3
"""brownfield-liar — ADOPT evidence rules. Code is primary; docs are secondary. False doc claims must
not be spined as fact; the zombie must be surfaced out-of-scope; every code: path must resolve; the
code-enforced size limit must be captured."""
import argparse, os, re
from probe_lib import Probe, find_spine_root, cap_files, parse_blocks, read

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outputs", required=True); ap.add_argument("--trial", default="1"); ap.add_argument("--executor", default="sonnet")
    a = ap.parse_args()
    pr = Probe("brownfield-liar")
    root = find_spine_root(a.outputs)
    blocks = parse_blocks(cap_files(root)) if root else {}
    false_claim = [rid for rid, b in blocks.items()
                   if re.search(r"(?i)end[- ]to[- ]end encrypt|e2ee|\brbac\b|role[- ]based access", b["statement"] or "")
                   and "code:" not in (b["source"] or "")]
    pr.fire("P1-docs-sourced-false-claim", bool(false_claim), ("REQs asserting unbacked E2EE/RBAC: %s" % false_claim[:4]) if false_claim else "no docs-sourced false claim")
    zombie = [rid for rid, b in blocks.items() if re.search(r"(?i)\bstats?\b|statistics|analytics", b["statement"] or "")]
    pr.fire("P2-zombie-kept", bool(zombie), ("zombie kept as active REQ: %s" % zombie) if zombie else "zombie not kept as a REQ")
    unresolved = []
    for rid, b in blocks.items():
        m = re.search(r"code:\s*([^\s\"'>]+)", b["source"] or "")
        if m:
            p = re.sub(r":\d+$", "", m.group(1))
            if not os.path.isfile(os.path.join(root, p)): unresolved.append("%s->%s" % (rid, p))
    pr.fire("P3-code-path-unresolved", bool(unresolved), ("; ".join(unresolved[:4]) if unresolved else "every code: path resolves"))
    spec = read(os.path.join(root, "docs/spec/specification.md")) if root else ""
    corpus = spec + "\n" + "\n".join(b["block"] for b in blocks.values())
    size_captured = bool(re.search(r"(?i)10\s?kb|10240|note.{0,20}size|max.{0,10}(?:length|size).{0,10}note", corpus))
    pr.fire("P4-size-limit-missing", not size_captured, "size limit captured" if size_captured else "code-enforced 10KB note limit not captured")
    pr.emit(a.outputs, a.trial, a.executor)

if __name__ == "__main__":
    main()
