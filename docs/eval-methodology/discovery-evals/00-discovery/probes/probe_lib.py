#!/usr/bin/env python3
"""Shared engine for discovery-evals probes. Parsing helpers copy-adapted from the calibrated
check_spine.py (COPIED, never imported — an import edge would couple the tracks). The Probe class
emits the frozen probe-report.json shape."""
import os, re, json

def read(p):
    try:
        with open(p, encoding="utf-8") as f: return f.read()
    except Exception:
        return None

# --- file discovery: skip by RELATIVE path only (the workspace itself lives under _artifacts/) ---
_SKIP = {".git", "__pycache__", "node_modules"}
def walk_files(outputs_root):
    outputs_root = os.path.abspath(outputs_root)
    for dp, dn, fn in os.walk(outputs_root):
        rel = os.path.relpath(dp, outputs_root).replace("\\", "/")
        parts = set(rel.split("/"))
        if parts & _SKIP:
            dn[:] = []
            continue
        for f in fn:
            yield os.path.join(dp, f)

def find_spine_root(outputs_root):
    for dp, _dn, fn in os.walk(outputs_root):
        if dp.replace("\\", "/").endswith("docs/spec") and "specification.md" in fn:
            return os.path.dirname(os.path.dirname(dp))
    return None

def spine_files(outputs_root):
    return [p.replace("\\", "/") for p in walk_files(outputs_root)
            if "/docs/spec/" in (p.replace("\\", "/") + "/")]

def cap_files(root):
    d = os.path.join(root, "docs/spec/capabilities")
    return [os.path.join(d, f) for f in os.listdir(d)
            if f.endswith(".md") and "_EXAMPLE" not in f] if os.path.isdir(d) else []

def parse_registry(spec):
    return re.findall(r"\|\s*(REQ-\d+)\s*\|([^|\n]*)\|([^|\n]*)\|([^|\n]*)\|([^|\n]*)\|", spec or "")

def parse_blocks(files):
    blocks = {}
    for cf in files:
        c = read(cf) or ""
        for m in re.finditer(r"###\s*(REQ-\d+):.*?<!--\s*/\1\s*-->", c, re.DOTALL):
            blk, rid = m.group(0), m.group(1)
            sm = re.search(r"<!--\s*source:\s*(.*?)\s*-->", blk, re.DOTALL)
            stmt = next((ln.strip() for ln in blk.splitlines()[1:] if ln.strip()), "")
            blocks[rid] = {"file": os.path.basename(cf),
                           "source": (sm.group(1).strip() if sm else None),
                           "statement": stmt, "block": blk}
    return blocks

def read_final(outputs_root):
    for p in walk_files(outputs_root):
        if os.path.basename(p) == "final-response.md":
            return read(p) or ""
    return ""

def load_amendments(root):
    try:
        return json.loads(read(os.path.join(root, "docs/spec/amendment-log.json")) or "").get("amendments", [])
    except Exception:
        return []

_D = r"(?:,|—|–|--)"
_EARS = [r"^The .+ SHALL .+", r"^WHEN .+%s\s*the .+ SHALL .+" % _D, r"^WHILE .+%s\s*the .+ SHALL .+" % _D,
         r"^WHERE .+%s\s*the .+ SHALL .+" % _D, r"^IF .+%s\s*THEN the .+ SHALL .+" % _D]
# House convention: the Unwanted-behavior EARS template (IF ..., THEN the ... SHALL ...) IS the
# must-not category by definition -- literal "NOT" is not required (matches the calibrated grader's semantics).
_MUSTNOT = r"^IF .+%s\s*THEN the .+ SHALL .+" % _D
def is_ears(s): return any(re.match(p, s or "") for p in _EARS)
def is_must_not(s): return bool(re.match(_MUSTNOT, s or ""))
QUANT_RE = re.compile(
    r"(\$\s?\d[\d,]*(?:\.\d+)?)|(\b\d[\d,]*(?:\.\d+)?\s?%)"
    r"|(\b\d[\d,]*(?:\.\d+)?\s?(?:ms|sec|secs|seconds?|mins?|minutes?|hrs?|hours?|days?|weeks?|months?|years?"
    r"|/mo|/month|/yr|/year|users?|requests?|rps|qps|k|K|M|MB|GB|TB|kb|KB)\b)", re.I)

def has_label(text, rx):
    return bool(re.search(r"(?im)^[\s>#*\-]*\*{0,2}\s*(?:%s)" % rx, text or ""))

class Probe:
    def __init__(self, case):
        self.case = case
        self.probes = []
    def fire(self, pid, fired, evidence=""):
        self.probes.append({"id": pid, "fired": bool(fired), "evidence": str(evidence)[:300]})
    def emit(self, outputs_root, trial="1", executor="sonnet"):
        rep = {"case": self.case, "trial": str(trial), "executor": executor, "probes": self.probes}
        with open(os.path.join(outputs_root, "probe-report.json"), "w", encoding="utf-8") as f:
            json.dump(rep, f, indent=2)
        fired = [p["id"] for p in self.probes if p["fired"]]
        print("[%s] trial=%s executor=%s -- %d/%d probes fired%s"
              % (self.case, trial, executor, len(fired), len(self.probes),
                 (": " + ", ".join(fired)) if fired else ""))
        return rep
