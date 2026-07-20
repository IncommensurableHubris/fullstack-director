#!/usr/bin/env python3
"""Shared engine for the 03-architect diagnostic probes.

Structure mirrors 00-discovery/probes/probe_lib.py: generic run-infrastructure (identical) + skill-specific
parsers (replaced wholesale — 00 parses a SPINE, 03 parses an ARCHITECTURE REALIZATION).

The architecture parsers are **copy-adapted** from the calibrated `check_architecture.py`. COPIED, never
imported: an import edge would couple this track to the regression bridge that judges its own fixes
(discovery-evals README, hard rule 5). Nothing here may read or write `.agents/skills/03-architect/evals/**`.

Probes are SENSORS, not gates. A fired probe is a lead for the auditor; a silent probe clears nothing.
"""
import os, re, json

# ---------------------------------------------------------------- generic infra (identical to 00-discovery)

def read(p):
    try:
        with open(p, encoding="utf-8") as f: return f.read()
    except Exception:
        return None

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
    """The project root — the dir containing docs/spec/specification.md (03's outputs carry the seeded
    spine alongside the produced docs/architecture/)."""
    for dp, _dn, fn in os.walk(outputs_root):
        if dp.replace("\\", "/").endswith("docs/spec") and "specification.md" in fn:
            return os.path.dirname(os.path.dirname(dp))
    return None

def read_final(outputs_root):
    for p in walk_files(outputs_root):
        if os.path.basename(p) == "final-response.md":
            return read(p) or ""
    return ""

def has_label(text, rx):
    return bool(re.search(r"(?im)^[\s>#*\-]*\*{0,2}\s*(?:%s)" % rx, text or ""))

def table_rows(text):
    """Every markdown table row in `text` (the structured commitment loci — never prose)."""
    return [ln.strip() for ln in (text or "").splitlines() if re.match(r"\s*\|", ln)]

def paragraphs(text):
    return re.split(r"\n\s*\n", text or "")

# ---------------------------------------------------------------- the spine side (read-only declarations)

def specification(root):
    return read(os.path.join(root, "docs/spec/specification.md")) or ""

def spec_line(root, label):
    """A declared `- **<label>:** value` line from specification.md — Profile / Embedded agent / Data."""
    m = re.search(r"(?im)^\s*-\s*\*\*%s:\*\*\s*(.+)$" % re.escape(label), specification(root))
    return m.group(1).strip() if m else ""

def constraints(root):
    return read(os.path.join(root, "docs/spec/architecture-constraints.md")) or ""

def constraint_field(root, label):
    m = re.search(r"^\s*[-*]\s*\*\*" + re.escape(label) + r"[^:]*:\*\*\s*(.+)$", constraints(root), re.I | re.M)
    return m.group(1).strip() if m else ""

def capability_files(root):
    d = os.path.join(root, "docs/spec/capabilities")
    return sorted(os.path.join(d, f) for f in os.listdir(d) if f.endswith(".md")) if os.path.isdir(d) else []

def _norm(s):
    return (s or "").replace("\r\n", "\n").replace("\r", "\n")

def capabilities_changed(root, fixture_docs):
    """REQ text is read-only to 03. Returns the list of capability files whose content differs from the
    fixture (EOL-normalized — the threat is edits, not line endings). Empty list == untouched."""
    fx = os.path.join(fixture_docs, "spec", "capabilities")
    changed = []
    if not os.path.isdir(fx):
        return changed
    for dp, _dn, fn in os.walk(fx):
        for f in fn:
            rel = os.path.relpath(os.path.join(dp, f), fx).replace("\\", "/")
            if _norm(read(os.path.join(dp, f))) != _norm(read(os.path.join(root, "docs/spec/capabilities", rel))):
                changed.append(rel)
    return changed

def load_amendments(root):
    try:
        return json.loads(read(os.path.join(root, "docs/spec/amendment-log.json")) or "").get("amendments", [])
    except Exception:
        return []

def tier_rows(rows, tier="2"):
    return [r for r in (rows or []) if str(r.get("tier")) == str(tier)]

def row_blob(r):
    return json.dumps(r, ensure_ascii=False).lower()

# ---------------------------------------------------------------- the realization side (what 03 produces)

def system_md(root):
    return read(os.path.join(root, "docs/architecture/system.md")) or ""

def adr_dir(root):
    return os.path.join(root, "docs/architecture/adr")

def adr_files(root):
    d = adr_dir(root)
    return [os.path.join(d, f) for f in sorted(os.listdir(d))
            if re.match(r"ADR-\d+\.md$", f)] if os.path.isdir(d) else []

def adr_files_loose(root):
    """Every ADR-ish file anywhere under docs/architecture/, whatever the naming or layout
    (`ADR-0001-slug.md`, `decisions/`, …) — for CONTENT probes.

    Why two finders: a content probe (e.g. "the topology ADR lacks the ~15x justification") that used the
    strict finder would go SILENT on a misnamed ADR — silent because it could not FIND the artifact, not
    because the clause was present. That is a false negative wearing a clean run's clothes. Allocation and
    registry probes must use the strict `adr_files()`: non-canonical naming is precisely what they detect.
    """
    out, arch = [], os.path.join(root, "docs/architecture")
    if os.path.isdir(arch):
        for dp, _dn, fn in os.walk(arch):
            for f in fn:
                if f.lower().endswith(".md") and re.match(r"(?i)adr[-_ ]?\d+", f):
                    out.append(os.path.join(dp, f))
    return sorted(out)

def adr_index(root):
    return read(os.path.join(adr_dir(root), "README.md"))

def adr_ids(root):
    return sorted(int(re.search(r"ADR-(\d+)", os.path.basename(f)).group(1)) for f in adr_files(root))

def strip_comments(text):
    """HTML comments are not claims. Wave-1 hygiene: `altitude-bait` P1 false-fired inside a
    `<!-- source: -->` block."""
    return re.sub(r"<!--.*?-->", "", text or "", flags=re.S)

def adr_index_ids(text):
    """ADR ids the register CLAIMS — parsed from register table ROWS only.

    Wave-1 hygiene, learned again here: a real register says `> **ADR-012**.` in prose and
    `<!-- Allocation: the next ADR is ADR-012 -->` in a comment. Neither is an allocation; a naive
    `findall(ADR-\\d+)` reads both and reports a phantom 12th ADR against 11 files — a guaranteed
    false fire for any allocation probe. Match on the WRITE (a register row), not the label.
    """
    ids = set()
    for row in table_rows(strip_comments(text)):
        if re.match(r"\s*\|[\s|:-]+\|?\s*$", row):          # separator row
            continue
        m = re.match(r"\s*\|\s*\[?\s*ADR-(\d+)", row)        # id must be the row's FIRST cell
        if m:
            ids.add(int(m.group(1)))
    return sorted(ids)

def adr_blob(root):
    return "\n\n".join(read(f) or "" for f in adr_files(root))

def adr_section(txt, heading):
    """A named ADR section's body (`## Decision Outcome`, `## Considered Options`, …), or ''."""
    m = re.search(r"##+\s*%s(.+?)(?:\n##\s|\Z)" % heading, txt or "", re.I | re.S)
    return m.group(1) if m else ""

def adr_field(txt, label):
    """A `- **<label>:** value` ADR front-field (Category / Review-Trigger / Verified-against / Status)."""
    m = re.search(r"(?im)^\s*[-*]?\s*\*\*%s:\*\*\s*(.+(?:\n(?![ \t]*[-*#]).+)*)" % re.escape(label), txt or "")
    return m.group(1).strip() if m else ""

def adr_decisions(root):
    """Concatenated Decision-Outcome bodies — the named field a token check reads."""
    return "\n".join(adr_section(read(f) or "", r"Decision\s+Outcome") or (read(f) or "") for f in adr_files(root))

def spec_files(root):
    d = os.path.join(root, "docs/architecture/specs")
    return [os.path.join(d, f) for f in sorted(os.listdir(d))
            if f.endswith(".md")] if os.path.isdir(d) else []

def specs_blob(root):
    return "\n\n".join(read(f) or "" for f in spec_files(root))

def feature_dirs_offspec(root):
    """Feature specs written somewhere other than the canonical docs/architecture/specs/ (a baseline tell:
    wave-1-style `features/` or `decisions/` layouts)."""
    arch = os.path.join(root, "docs/architecture")
    out = []
    if os.path.isdir(arch):
        for name in sorted(os.listdir(arch)):
            p = os.path.join(arch, name)
            if os.path.isdir(p) and name not in ("adr", "specs"):
                out.append(name)
    return out

def vc_rows(text):
    """Verification-Contract table rows — the mechanically-gradeable contract 04/05 consume."""
    m = re.search(r"(?is)#{1,6}[^\n]*verification\s+contract[^\n]*\n(.*?)(?:\n#{1,6}\s|\Z)", text or "")
    if not m:
        return []
    return [r for r in table_rows(m.group(1)) if not re.match(r"\s*\|[\s|:-]+\|?\s*$", r)]

def realization_blob(root):
    return system_md(root) + "\n" + adr_blob(root) + "\n" + specs_blob(root)

# ---------------------------------------------------------------- the probe report (frozen shape)

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
