#!/usr/bin/env python3
"""Deterministic grader for the CROSS-SKILL INTEGRATION evals — the §10 safety net the per-skill unit evals cannot
provide (each of those isolates one seat). No LLM judge. It grades the COMPOSITION — the handoffs a later seat
mechanically reads — over a chain-produced (or governance/pivot) end-state, and where it fits it COMPOSES `/status`
as the integrity/routing oracle (grading its emission) rather than re-deriving integrity logic.

Six cases (mirroring the plan §Verification surface):

  spec-first     — 00 intake -> 01 -> 02 -> 03 -> /status over the seeded PRD. Asserts the composition invariants:
                   spine populated; registry<->leaf integrity (via /status PASS AND directly); REQ-ID allocation
                   coherent across seats; the planted Tier-2 surfaced+resolved (gated/approved row + resolving ADR,
                   never auto-applied — THE cross-skill discriminator); backlog ledger + frozen sprint snapshot;
                   handoff fidelity (manifest DM -> spec coverage; REQ -> spec coverage); the retired-artifacts guard;
                   and /status routes to /04-builder on the marker-free, Tier-2-resolved end-state. (Test 1 + 3/5.)
  governance     — /status AND 06 both gate the SAME governance-blocked chain state (a deferred amendment + a
                   surviving marker): /status routes to resolve + counts the blockers; 06 ends BLOCKED, nothing
                   deployed. (Test 3, end-to-end cross-seat agreement.)
  spine-collapse — after an upstream pivot + a 00 re-run: the spine regenerates anchored to the unchanged charter
                   JTBD, the registry stays integral through the pivot (no shatter), and the pivot is logged as an
                   amendment (not a silent rewrite). (Test 4.)
  isolation-chain — a fresh 05 (dispatched from the pipeline) reviews a BUILT slice it never built: attestation
                   present + valid, verdict not-SHIP, the planted violation named. (Test 2; delegates the built-slice
                   grading to the 05-reviewer grader — see the integration README.)
  agent-chain    — the §10 FIFTH leg (5.5a): the agent-system composition (00 profile+contract -> 01 -> 03 topology+
                   eval-suite VC -> 04 -> 05 floors -> status). AC1-AC6: the profile propagates; the agent-contract is
                   complete; an eval-suite VC row reaches EXECUTED with grader-bites; the qa tally is present +
                   floor-consistent; a topology ADR carries its ~15x economics justification; the router is
                   agent-aware. Grader + hand-ideal + 3 degenerates built here; the LIVE six-seat run is DEFERRED (5.5b).
  verify-live    — WS6: the live-source verification chain (00 declares+seeds -> 03 cites -> 04 verifies -> 06 gates).
                   VL1-VL5: one declared verify-live tech flows coherently across the chain, anchored on a single
                   docs/verification/<tech>.md record (declared+cited; ADR Verified-against; handoff `verified:`
                   EXECUTED; 06 G11 PASS; record version current vs the manifest). Grader + hand-ideal + 4 degenerates
                   built here; the LIVE 00-seed A/B (fetch+cite vs confabulate) is DEFERRED (6.6b — first verify-live project).

Usage:
    python check_integration.py --outputs <dir> --case <spec-first|governance|spine-collapse|isolation-chain|agent-chain|verify-live>
Writes grading.json ({"expectations":[{text,passed,evidence}]}) into --outputs and prints a report.
"""
import os, re, json, argparse, sys, subprocess

try:  # keep prints from crashing a legacy (cp1252) Windows console — grading.json is always utf-8
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

results = []
def check(text, passed, evidence=""):
    results.append({"text": text, "passed": bool(passed), "evidence": str(evidence)[:400]})

def read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None


# ---------- root / git ----------

def find_root(base):
    """The dir containing docs/spec/specification.md under base (the produced spine), else base."""
    for dp, dn, fn in os.walk(base):
        if dp.replace("\\", "/").endswith("docs/spec") and "specification.md" in fn:
            return os.path.dirname(os.path.dirname(dp))
    return base

def git(root, *args):
    try:
        p = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=60)
        return p.returncode, (p.stdout or ""), (p.stderr or "")
    except Exception as e:
        return 1, "", str(e)


# ---------- spine parsing (from check_spine.py / check_status.py — kept identical) ----------

def spec_md(root):
    return read(os.path.join(root, "docs/spec/specification.md")) or ""

def parse_registry(spec):
    """Registry rows: | REQ-001 | name | MUST | stated | capabilities/x.md |."""
    return re.findall(r"\|\s*(REQ-\d+)\s*\|([^|\n]*)\|([^|\n]*)\|([^|\n]*)\|([^|\n]*)\|", spec or "")

def capability_files(root):
    d = os.path.join(root, "docs/spec/capabilities")
    return [os.path.join(d, f) for f in os.listdir(d)
            if f.endswith(".md") and "_EXAMPLE" not in f] if os.path.isdir(d) else []

def parse_blocks(cap_files):
    """rid -> {file, source} for each delimited `### REQ-NNN: ... <!-- /REQ-NNN -->` block."""
    blocks = {}
    for cf in cap_files:
        c = read(cf) or ""
        for m in re.finditer(r"###\s*(REQ-\d+):.*?<!--\s*/\1\s*-->", c, re.DOTALL):
            blk, rid = m.group(0), m.group(1)
            sm = re.search(r"<!--\s*source:\s*(.*?)\s*-->", blk, re.DOTALL)
            blocks[rid] = {"file": os.path.basename(cf), "source": (sm.group(1).strip() if sm else None)}
    return blocks

def block_present(root, req, rel):
    """Leaf-level integrity for one registry row: the file resolves AND carries the heading + closing delimiter."""
    leaf = read(os.path.join(root, "docs/spec", rel))
    if leaf is None:
        return None
    return bool(re.search(r"(?m)^#{2,4}\s+" + re.escape(req) + r"\b", leaf)) and (f"<!-- /{req} -->" in leaf)

def markers(root):
    """Count surviving `[NEEDS CLARIFICATION ...]` markers in docs/spec — matches BOTH the bare `[NEEDS CLARIFICATION]`
    label form and the canonical `[NEEDS CLARIFICATION: <question>]` colon form (so a real marker with a question is
    not missed)."""
    n = 0
    specdir = os.path.join(root, "docs/spec")
    for dp, dn, fn in os.walk(specdir):
        for f in fn:
            n += len(re.findall(r"\[NEEDS CLARIFICATION\b", read(os.path.join(dp, f)) or ""))
    return n


# ---------- amendments / architecture (from check_architecture.py — kept identical) ----------

def amendments(root):
    al = read(os.path.join(root, "docs/spec/amendment-log.json"))
    if al is None:
        return None
    try:
        a = json.loads(al)
        return a.get("amendments") if isinstance(a.get("amendments"), list) else None
    except Exception:
        return None

def tier2_rows(rows):
    return [r for r in (rows or []) if str(r.get("tier")) == "2"]

def source_quotes(rows):
    return " ".join(str(r.get("source_quote", "")) for r in tier2_rows(rows))

def row_blob(r):
    return json.dumps(r, ensure_ascii=False).lower()

DB_CLIENT_SERVER = ["postgresql", "postgres", "mysql", "mariadb", "cockroachdb", "cockroach",
                    "sql server", "mssql", "aurora", "client-server", "client/server"]
DB_EMBEDDED = ["sqlite"]

def tokens_in(text, tokens):
    if not text:
        return []
    t = text.lower()
    hits = []
    for tok in tokens:
        if re.search(r"[ /-]", tok):
            if tok in t:
                hits.append(tok)
        elif re.search(r"\b" + re.escape(tok) + r"\b", t):
            hits.append(tok)
    return hits

def constraint_field(root, label):
    ac = read(os.path.join(root, "docs/spec/architecture-constraints.md")) or ""
    m = re.search(r"^\s*[-*]\s*\*\*" + re.escape(label) + r"[^:]*:\*\*\s*(.+)$", ac, re.I | re.M)
    return m.group(1).strip() if m else ""

def adr_dir(root):
    return os.path.join(root, "docs/architecture/adr")

def adr_files(root):
    d = adr_dir(root)
    out = []
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if re.match(r"ADR-\d+\.md$", f):
                out.append(os.path.join(d, f))
    return out

def resolving_adr_decisions(root, rows):
    """Decision-Outcome sections of the ADRs a Tier-2 row's `resolved_by` names (read the Decision field, not the
    whole file, so a migration ADR naming SQLite as the SUPERSEDED option isn't misread as re-affirming it)."""
    out = []
    for r in tier2_rows(rows):
        m = re.search(r"ADR-(\d+)", str(r.get("resolved_by") or ""))
        if m:
            txt = read(os.path.join(adr_dir(root), f"ADR-{int(m.group(1)):03d}.md")) or ""
            dm = re.search(r"##+\s*Decision\s+Outcome(.+?)(?:\n##\s|\Z)", txt, re.I | re.S)
            out.append(dm.group(1) if dm else txt)
    return out

def feature_specs(root):
    d = os.path.join(root, "docs/architecture/specs")
    return [os.path.join(d, f) for f in sorted(os.listdir(d))
            if f.endswith(".md")] if os.path.isdir(d) else []

def specs_blob(root):
    return "\n\n".join(read(f) or "" for f in feature_specs(root))

def system_md(root):
    return read(os.path.join(root, "docs/architecture/system.md")) or ""

def sprint_reqs(root):
    """The in-scope REQ-IDs — the sprint-01 frozen `### REQ-NNN:` headers."""
    sp = read(os.path.join(root, "docs/planning/sprints/sprint-01.md")) or ""
    return sorted(set(re.findall(r"(?m)^#{2,4}\s+(REQ-\d+)\b", sp)))

def manifest_required_dms(root):
    man = read(os.path.join(root, "docs/design/approved/sprint-01/manifest.md")) or ""
    req = []
    for line in man.splitlines():
        m = re.match(r"\s*\|\s*(DM-\d+)\s*\|", line)
        if m and "required" in line.lower() and "optional" not in line.lower().split("required")[0]:
            req.append(m.group(1))
    return sorted(set(req)) or sorted(set(re.findall(r"DM-\d+", man)))


# ---------- backlog ledger (compact port of check_backlog.parse_ledger) ----------

EXEC_STATUS = {"planned", "in-progress", "in progress", "done"}
FIDELITY_STATUS = {"stated", "derived"}

def _split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]

def _first_int(s):
    m = re.search(r"\d+", s or "")
    return int(m.group(0)) if m else None

def parse_ledger(backlog):
    """{req: {'epic':int|None,'sprint':int|None,'status':str}} from the flat REQ+Epic+Sprint+Status table."""
    out = {}
    lines = (backlog or "").splitlines()
    for i, line in enumerate(lines):
        if "|" not in line:
            continue
        header = [c.lower() for c in _split_row(line)]
        if not ("req" in header and "status" in header and ("epic" in header or "sprint" in header)):
            continue
        col = {name: idx for idx, name in enumerate(header)}
        for dl in lines[i + 1:]:
            if "|" not in dl:
                break
            cells = _split_row(dl)
            if not cells or set("".join(cells)) <= set("-: "):
                continue
            rowtext = " ".join(cells)
            rm = re.search(r"REQ-\d+", rowtext)
            if not rm:
                if re.search(r"\bREQ\b|name|priority", rowtext, re.I):
                    continue
                break
            def cell(name):
                idx = col.get(name)
                return cells[idx] if idx is not None and idx < len(cells) else ""
            out[rm.group(0)] = {"epic": _first_int(cell("epic")), "sprint": _first_int(cell("sprint")),
                                "status": cell("status").lower()}
        if out:
            return out
    return out


# ---------- the /status emission (CLAUDE.md § Current State — from check_status.py) ----------

def claude_md(root):
    return read(os.path.join(root, "CLAUDE.md")) or ""

def field(root, label):
    m = re.search(r"(?im)^\s*[-*]?\s*\*{0,2}" + re.escape(label) + r"\*{0,2}\s*:\s*(.+)$", claude_md(root))
    return m.group(1).strip() if m else ""

def integrity_verdict(root):
    v = field(root, "Spine integrity") or field(root, "Integrity")
    if re.search(r"\bFAIL\b", v, re.I) or (not v and re.search(r"(?i)integrity[^\n]{0,40}\bFAIL\b", claude_md(root))):
        return "FAIL"
    if re.search(r"\bPASS\b", v, re.I) or re.search(r"(?i)integrity[^\n]{0,40}\bPASS\b", claude_md(root)):
        return "PASS"
    return None

def next_command(root):
    v = field(root, "Next command") or field(root, "Next")
    if v:
        return v
    txt = claude_md(root)
    m = re.search(r"(?m)^\s*(?:→|->|Run:)\s*`?(/?\d{2}[-\w]*[^`\n]*)`?", txt)
    if m:
        return m.group(1).strip()
    m = re.search(r"`(/(?:00-discovery|01-planner|02-designer|03-architect|04-builder|05-reviewer|06-release|"
                  r"07-security|08-refactor)[^`]*)`", txt)
    return m.group(1).strip() if m else ""

def amendment_counts(root):
    t = claude_md(root)
    p = re.search(r"(\d+)\s*[`*]*\s*pending", t, re.I)
    d = re.search(r"(\d+)\s*[`*]*\s*deferred", t, re.I)
    return (int(p.group(1)) if p else None, int(d.group(1)) if d else None)

def marker_count(root):
    t = claude_md(root)
    m = re.search(r"(?:\[?needs clarification\]?[`*\s]*|markers?)\s*[:=]\s*[`*\s]*(\d+)", t, re.I)
    if m:
        return int(m.group(1))
    m = re.search(r"(\d+)\s+(?:surviving\s+|open\s+)*(?:[`*]*\[?needs clarification\]?[`*]*\s+)?markers?", t, re.I)
    if m:
        return int(m.group(1))
    if re.search(r"(?:markers?|needs clarification[`*\]]*)\s*[:=]?\s*[`*\s]*(?:none|no)\b", t, re.I):
        return 0
    return None


# ---------- shared integrity + release-report helpers ----------

def direct_integrity_ok(root):
    """(ok, evidence) — every registry File resolves + carries its <!-- /REQ --> block; no orphan/dup IDs. The
    belt-and-suspenders half of the integrity check (independent of the /status emission)."""
    spec = spec_md(root)
    reg_ids = [r[0].strip() for r in parse_registry(spec)]
    reg_file = {r[0].strip(): r[4].strip() for r in parse_registry(spec)}
    blocks = parse_blocks(capability_files(root))
    unresolved = [rid for rid in reg_ids if block_present(root, rid, reg_file.get(rid, "")) is not True]
    dup_ids = sorted({x for x in reg_ids if reg_ids.count(x) > 1})
    orphan = sorted(set(blocks) - set(reg_ids))
    ok = bool(reg_ids) and not unresolved and not dup_ids and not orphan
    return ok, f"unresolved={unresolved or 'none'}; dup IDs={dup_ids or 'none'}; orphan blocks={orphan or 'none'}"

def find_release_report(root):
    import glob
    cands = glob.glob(os.path.join(root, "docs", "release", "release-report*.md"))
    cands = [c for c in cands if os.path.isfile(c) and os.sep + "_deploy" + os.sep not in c]
    cands.sort(key=len)
    return (cands[0], read(cands[0])) if cands else (None, None)

def fm(text, key):
    """A frontmatter/prose `key: value` line's value (tolerant of markdown bold; stops at a #/<!-- comment)."""
    m = re.search(r"(?im)^\s*[-*]?\s*[`*]*" + re.escape(key) + r"[`*]*\s*[:=]\s*[`*]*([^#<\n|]+?)\s*(?:[#<|]|$)", text or "")
    return m.group(1).strip().strip("`*") if m else ""

def status_of_report(report):
    """RELEASED | ROLLED-BACK | FAILED | BLOCKED — from the report's `status:` frontmatter, else a heading line."""
    v = fm(report, "status").upper().replace(" ", "-")
    for tok in ("ROLLED-BACK", "RELEASED", "BLOCKED", "FAILED"):
        if tok in v:
            return tok
    m = re.search(r"(?im)^\s*\**\s*(RELEASED|ROLLED[- ]BACK|FAILED|BLOCKED)\b", report or "")
    return (m.group(1).upper().replace(" ", "-")) if m else None

def section(report, name):
    """Text of a `## (x) <name>` .. next `## ` section (case-insensitive), else ''."""
    m = re.search(r"(?ims)^#{1,6}\s*(?:\([a-z0-9]\)\s*)?" + name + r"\b(.*?)(?:^#{1,6}\s|\Z)", report or "")
    return m.group(1) if m else ""

def is_discovery(cmd):
    return "00-discovery" in (cmd or "").lower()

def is_release(cmd):
    return "06-release" in (cmd or "").lower()

def is_builder(cmd):
    return "04-builder" in (cmd or "").lower()


# ==================================================================================================
# CASE: spec-first — the flagship composition invariants
# ==================================================================================================

def grade_spec_first(root):
    spec = spec_md(root)
    reg = parse_registry(spec)
    reg_ids = [r[0].strip() for r in reg]
    reg_file = {r[0].strip(): r[4].strip() for r in reg}
    cap_files = capability_files(root)
    blocks = parse_blocks(cap_files)
    rows = amendments(root)
    reqs = sprint_reqs(root)

    # ---- Invariant 1: the spine tree is populated ----
    const = re.search(r"^#+\s*Constitution", spec, re.M | re.I)
    const_items = re.findall(r"^\s*\d+\.\s+\S", re.split(r"\n---", spec[const.end():], maxsplit=1)[0], re.M) if const else []
    di = read(os.path.join(root, "docs/spec/design-intent.md"))
    ac = read(os.path.join(root, "docs/spec/architecture-constraints.md"))
    populated = (bool(spec) and len(const_items) >= 3 and len(reg) >= 6 and len(cap_files) >= 1
                 and len(blocks) > 0 and di is not None and ac is not None and rows is not None)
    check("Invariant 1 — the spine tree is populated: specification.md (Constitution >=3 + registry >=6) + "
          "capabilities/*.md delimited REQ blocks + design-intent.md + architecture-constraints.md + valid "
          "amendment-log.json (the chain produced a whole spine, not a stub)",
          populated, f"const items={len(const_items)}; registry rows={len(reg)}; cap files={len(cap_files)}; "
                     f"REQ blocks={len(blocks)}; design-intent={di is not None}; arch-constraints={ac is not None}; "
                     f"amendment-log valid={rows is not None}")

    # ---- Invariant 2: registry<->leaf integrity — via /status PASS AND directly ----
    iv = integrity_verdict(root)
    direct_ok, direct_ev = direct_integrity_ok(root)
    check("Invariant 2 — registry<->leaf integrity holds, confirmed TWO ways: /status emits `Spine integrity: PASS` "
          "AND the direct check (every registry File resolves + carries its <!-- /REQ --> block; no orphan/dup IDs)",
          iv == "PASS" and direct_ok, f"/status integrity={iv}; {direct_ev}")

    # ---- Invariant 3: REQ-ID allocation coherent across the chain ----
    backlog = read(os.path.join(root, "docs/planning/backlog.md")) or ""
    ledger = parse_ledger(backlog)
    led_set = set(ledger.keys())
    reg_set = set(reg_ids)
    missing = sorted(reg_set - led_set)
    extra = sorted(led_set - reg_set)               # invented IDs
    raw = re.findall(r"^\s*\|.*?(REQ-\d+)", backlog, re.M)
    led_dup = sorted({x for x in raw if raw.count(x) > 1})
    # every REQ referenced by a downstream realization exists in the registry (no dangling refs across seats)
    downstream = system_md(root) + "\n" + specs_blob(root) + "\n" + \
        (read(os.path.join(root, "docs/planning/sprints/sprint-01.md")) or "")
    dangling = sorted({r for r in re.findall(r"REQ-\d+", downstream) if r not in reg_set})
    coherent = bool(reg_set) and not missing and not extra and not led_dup and not dangling
    check("Invariant 3 — REQ-ID allocation is coherent across seats: the backlog carries every spine REQ exactly "
          "once (none dropped/duplicated/invented) and every REQ a downstream realization references resolves to the "
          "registry (no dangling cross-seat refs — the corruption guard)",
          coherent, f"missing from ledger={missing or 'none'}; invented={extra or 'none'}; "
                    f"duplicated={led_dup or 'none'}; dangling downstream refs={dangling or 'none'}")

    # ---- Invariant 4: the planted Tier-2 surfaced + resolved (THE cross-skill discriminator) ----
    datastore = constraint_field(root, "Datastore")
    availability = constraint_field(root, "Availability")
    sqs = source_quotes(rows)
    emb = tokens_in(datastore, DB_EMBEDDED) or tokens_in(sqs, DB_EMBEDDED)
    shared = bool(re.search(r"share one datastore|shared|two or more|stateless instances|worker", availability + " " + sqs, re.I))
    t2 = tier2_rows(rows)
    cites = [r for r in t2 if re.search(r"sqlite|datastore|embedded", row_blob(r))]
    gated = [r for r in cites if r.get("disposition") in ("gated", "approved")]
    not_auto = [r for r in cites if r.get("disposition") == "auto-applied"]
    with_adr = [r for r in gated if re.search(r"adr-\d+", str(r.get("resolved_by") or ""), re.I)]
    adr_fixed = any(tokens_in(t, DB_CLIENT_SERVER) for t in resolving_adr_decisions(root, rows))
    tier2_ok = bool(emb) and shared and bool(with_adr) and not not_auto and adr_fixed
    check("Invariant 4 — the planted Tier-2 surfaced + resolved through the amendment channel (NOT silent prose): a "
          "tier-2 row cites the SQLite/shared-store contradiction, gated/approved (never auto-applied), resolved_by "
          "an ADR whose Decision names a client-server datastore — the cross-skill discriminator",
          tier2_ok, f"embedded token (file|source_quote)={emb}; shared-store req={shared}; tier-2 citing rows="
                    f"{len(cites)}; gated+ADR={len(with_adr)}; auto-applied(bad)={len(not_auto)}; "
                    f"resolving ADR names client-server DB={adr_fixed}")

    # ---- Invariant 5: backlog ledger + frozen sprint snapshot ----
    statuses = {v["status"] for v in ledger.values() if v["status"]}
    exec_ok = bool(statuses) and not (statuses - EXEC_STATUS) and not (statuses & FIDELITY_STATUS)
    # Build-order, NUMBERING-AGNOSTIC: the team/access domain (the foundation) precedes the digest domain (the
    # consumer payoff). Anchor by the registry File (the PRD's domain), NOT a hardcoded REQ-ID — a live 00 is free to
    # number/derive differently than the seeded unit fixtures (e.g. it may not mint a separate auth REQ).
    def domain_min_epic(kw):
        eps = [ledger[r]["epic"] for r in ledger
               if kw in reg_file.get(r, "").lower() and ledger[r]["epic"] is not None]
        return min(eps) if eps else None
    fe, ce = domain_min_epic("team"), domain_min_epic("digest")
    build_order = fe is not None and ce is not None and fe < ce
    sp = read(os.path.join(root, "docs/planning/sprints/sprint-01.md")) or ""
    has_gherkin = ("```gherkin" in sp) or bool(re.search(r"given\b.*\bwhen\b.*\bthen\b", sp, re.I | re.S))
    has_done = bool(re.search(r"done\s*when", sp, re.I))
    ledger_ok = bool(ledger) and exec_ok and build_order and bool(reqs) and has_gherkin and has_done
    check("Invariant 5 — backlog ledger + frozen sprint snapshot written: the ledger maps REQ->epic/sprint/status "
          "(execution vocab, never fidelity), the foundation epic precedes the consuming epic, and sprint-01 carries "
          "a frozen outcome-Gherkin snapshot + a Done When",
          ledger_ok, f"ledger rows={len(ledger)}; exec-vocab-only={exec_ok}; build-order(foundation<consumer)="
                     f"{build_order} (fe={fe},ce={ce}); sprint REQs={reqs}; frozen gherkin={has_gherkin}; done_when={has_done}")

    # ---- Invariant 6: handoff fidelity (02 manifest -> 03 specs; REQ -> specs) ----
    sb = specs_blob(root)
    req_dms = manifest_required_dms(root)
    spec_dms = set(re.findall(r"DM-\d+", sb))
    missing_dms = sorted(set(req_dms) - spec_dms)
    spec_all_reqs = set(re.findall(r"REQ-\d+", sb))
    uncovered_reqs = sorted(set(reqs) - spec_all_reqs)
    sys_reqs = bool(re.findall(r"REQ-\d+", system_md(root)))
    handoff_ok = bool(feature_specs(root)) and bool(req_dms) and not missing_dms and bool(reqs) \
        and not uncovered_reqs and sys_reqs
    check("Invariant 6 — handoff fidelity: every REQUIRED 02-manifest DM-ID is covered by a 03 feature spec, every "
          "in-scope sprint REQ is covered by >=1 feature spec, and the architecture references the spine by REQ-ID "
          "(traceability, not copied prose)",
          handoff_ok, f"feature specs={[os.path.basename(s) for s in feature_specs(root)] or 'none'}; required DMs="
                      f"{req_dms}; uncovered DMs={missing_dms or 'none'}; uncovered REQs={uncovered_reqs or 'none'}; "
                      f"system.md has REQ refs={sys_reqs}")

    # ---- Invariant 7: retired-artifacts guard ----
    brief = os.path.join(root, "docs/planning/requirements-brief.md")
    us_dir = os.path.join(root, "docs/planning/user-stories")
    us_files = []
    if os.path.isdir(us_dir):
        us_files = [f for f in os.listdir(us_dir) if re.match(r"US-\d+\.md$", f)]
    # also scan anywhere for a stray US-NNN.md (a regression could put it elsewhere)
    stray_us = []
    for dp, dn, fn in os.walk(os.path.join(root, "docs")):
        for f in fn:
            if re.match(r"US-\d+\.md$", f):
                stray_us.append(os.path.relpath(os.path.join(dp, f), root))
    retired_absent = (not os.path.isfile(brief)) and not us_files and not stray_us
    check("Invariant 7 — retired-artifacts guard: NO docs/planning/requirements-brief.md and NO user-stories/US-*.md "
          "anywhere (a regression to the old flat topology fails here)",
          retired_absent, f"requirements-brief.md present={os.path.isfile(brief)}; US-*.md files={us_files or stray_us or 'none'}")

    # ---- Invariant 8: /status routes correctly on the marker-free, Tier-2-resolved end-state ----
    nc = next_command(root)
    p, d = amendment_counts(root)
    m = marker_count(root)
    routes_build = "04-builder" in (nc or "").lower()
    clean_gov = ((p == 0 and d == 0) or p is None and d is None) and (m == 0 or m is None) and markers(root) == 0
    route_ok = routes_build and iv == "PASS" and clean_gov
    check("Invariant 8 — /status routes correctly (Tests 3+5 composed): on a marker-free, Tier-2-RESOLVED end-state "
          "the routed Next command is `/04-builder` (not a repair/resolve route), integrity PASS, and the governance "
          "counts reflect the real state (0 pending/deferred, 0 surviving markers)",
          route_ok, f"next command={nc or 'none'}; integrity={iv}; pending={p}; deferred={d}; "
                    f"emitted markers={m}; actual spine markers={markers(root)}")

    # ---- Invariant 9: the instructions-file bridges — the Constitution projection reaches every harness ----
    # Claude Code reads CLAUDE.md (not AGENTS.md): line 1 must be the live `@AGENTS.md` import (the officially
    # recommended pattern). Gemini CLI reads GEMINI.md: the one-line `@./AGENTS.md` bridge. Codex reads AGENTS.md
    # natively (no bridge). Both bridges are 00-discovery WRITE-SPINE emissions (create-if-absent).
    cm_lines = [ln.strip() for ln in claude_md(root).splitlines() if ln.strip()]
    cm_first = cm_lines[0] if cm_lines else ""
    gm = read(os.path.join(root, "GEMINI.md")) or ""
    check("Invariant 9 — instructions-file bridges emitted: CLAUDE.md line 1 is the live `@AGENTS.md` import "
          "(Claude Code bridge) and GEMINI.md carries `@./AGENTS.md` (Gemini bridge)",
          cm_first == "@AGENTS.md" and "@./AGENTS.md" in gm,
          f"CLAUDE.md first non-blank line={cm_first[:40]!r}; GEMINI.md bridge present={'@./AGENTS.md' in gm}")


# ==================================================================================================
# CASE stubs (built in later passes — governance / spine-collapse / isolation-chain)
# ==================================================================================================

def grade_governance(root):
    """Test 3 — the two governance-consuming seats agree on the SAME chain-produced state. The state is ship-ready
    EXCEPT for a deferred amendment (AMD-003) + a surviving [NEEDS CLARIFICATION] marker; /status must route to
    RESOLVE (not ship) and 06 must BLOCK (deploy nothing). The killer is cross-seat AGREEMENT: a state one seat
    passes and the other blocks would be an incoherent governance boundary."""
    rows = amendments(root)
    iv = integrity_verdict(root)
    direct_ok, direct_ev = direct_integrity_ok(root)

    # G1 — integrity PASS: this is a GOVERNANCE block, not corruption (both witnesses agree).
    check("Governance G1 — integrity PASS (the block is governance, not corruption): /status PASS AND the direct "
          "registry<->leaf check holds",
          iv == "PASS" and direct_ok, f"/status integrity={iv}; {direct_ev}")

    # G2 — /status counted the blockers the release gate exists for (>=1 pending/deferred, >=1 surviving marker).
    p, d = amendment_counts(root)
    m = marker_count(root)
    actual = markers(root)
    log_deferred = len([r for r in (rows or []) if r.get("disposition") in ("pending", "deferred")])
    check("Governance G2 — /status counted the blockers: >=1 pending/deferred amendment AND >=1 surviving "
          "[NEEDS CLARIFICATION] marker (the two things 06 blocks on, surfaced early)",
          (p or 0) + (d or 0) >= 1 and (m or 0) >= 1 and actual >= 1 and log_deferred >= 1,
          f"emitted pending={p} deferred={d}; emitted markers={m}; actual spine markers={actual}; "
          f"log pending/deferred rows={log_deferred}")

    # G3 — /status routed to RESOLVE, not ship: /00-discovery reflect, NOT /06-release, NOT /04-builder.
    nc = next_command(root)
    g3 = is_discovery(nc) and not is_release(nc) and not is_builder(nc)
    check("Governance G3 — /status routes to RESOLVE (`/00-discovery reflect`), NOT a ship/build route: the block is "
          "enforced before the gate",
          g3, f"next command={nc or 'none'}")

    # G4 — 06 BLOCKED, nothing deployed.
    rpath, report = find_release_report(root)
    st = status_of_report(report)
    deployed_dir = os.path.isdir(os.path.join(root, "_deploy"))
    dep = fm(report or "", "deployed_commit").lower()
    g4 = bool(report) and st == "BLOCKED" and not deployed_dir and (dep in ("", "none", "n/a", "-", "—") or "none" in dep)
    check("Governance G4 — 06 ends BLOCKED with nothing deployed (no _deploy/, deployed_commit: none) — the "
          "never-proceed-past-unresolved-intent property",
          g4, f"release report={'yes' if report else 'no'}; status={st}; _deploy present={deployed_dir}; "
              f"deployed_commit={dep or '(absent)'}")

    # G5 — 06 cited the SAME blockers by ID (AMD-003 + the marker), so the two seats block on the same evidence.
    cites_amd = bool(re.search(r"AMD-0*3\b", report or ""))
    cites_marker = bool(re.search(r"(?i)NEEDS\s*CLARIFICATION", report or ""))
    check("Governance G5 — 06 cited the blockers by ID (the deferred AMD + a surviving [NEEDS CLARIFICATION] "
          "marker) — the same evidence /status surfaced",
          cites_amd and cites_marker, f"AMD cited={cites_amd}; marker cited={cites_marker}")

    # G6 — CROSS-SEAT AGREEMENT (the integration point): /status routes-to-resolve AND 06 blocks on the SAME state.
    check("Governance G6 — cross-seat AGREEMENT: /status (routes to resolve) and 06 (BLOCKED) gate the SAME "
          "governance-blocked state — a coherent governance boundary, not one seat passing what the other blocks",
          g3 and g4, f"status-resolves={g3}; 06-blocks={g4}")

    # G7 — non-amender: 06 blocked ON the deferred amendment; it did not resolve it (still pending/deferred).
    still = any(str(r.get("id", "")).replace("-", "").upper().endswith("003")
                and r.get("disposition") in ("pending", "deferred") for r in (rows or []))
    check("Governance G7 — non-amender: the deferred amendment is STILL pending/deferred in the log — 06 blocked on "
          "it, it did not silently resolve it",
          still, f"deferred AMD still open={still}")

def grade_spine_collapse(root):
    """Test 4 — the intent-anchoring hedge (the credible 2026 critique that pure SDD shatters on an upstream pivot).
    After the user pivots a constraint (EU-only data residency -> allow a US region) and 00 re-runs, the spine must
    regenerate ANCHORED to the unchanged charter JTBD, with the REQ registry INTEGRAL through the pivot (no shatter),
    the pivot LOGGED as an amendment (not a silent rewrite), and downstream refs still resolving."""
    charter = read(os.path.join(root, "docs/discovery/charter.md")) or ""
    rows = amendments(root)
    reg_ids = {r[0].strip() for r in parse_registry(spec_md(root))}

    # SC1 — the charter JTBD is UNCHANGED: the regeneration is anchored to the loop-doc intent, not rewritten.
    jtbd_ok = bool(re.search(r"spread across timezones", charter, re.I)) and \
        bool(re.search(r"stay in sync", charter, re.I)) and bool(re.search(r"(?is)when.*i\s+want.*so", charter))
    check("Spine-collapse SC1 — the charter JTBD is intact (the regeneration is ANCHORED to the unchanged loop-doc "
          "intent, not a rewrite from scratch): the same 'spread across timezones … stay in sync' job persists",
          jtbd_ok, f"charter present={bool(charter)}; JTBD anchor phrases intact={jtbd_ok}")

    # SC2 — the REQ registry is INTEGRAL through the pivot (no shatter): every File resolves + delimited block, no dup/orphan.
    direct_ok, direct_ev = direct_integrity_ok(root)
    check("Spine-collapse SC2 — the REQ registry stayed INTEGRAL through the pivot (no shatter): every registry File "
          "resolves + carries its delimited block; no orphaned/duplicated IDs",
          direct_ok, direct_ev)

    # SC3 — downstream refs still RESOLVE (no dangling REQ-ID after the pivot).
    downstream = (read(os.path.join(root, "docs/planning/backlog.md")) or "") + "\n" + \
        (read(os.path.join(root, "docs/planning/sprints/sprint-01.md")) or "") + "\n" + \
        system_md(root) + "\n" + specs_blob(root)
    dangling = sorted({r for r in re.findall(r"REQ-\d+", downstream) if r not in reg_ids})
    check("Spine-collapse SC3 — downstream realizations did NOT shatter: every REQ-ID the backlog/sprint/architecture "
          "reference still resolves to the (unchanged) registry — no dangling ref after the pivot",
          bool(reg_ids) and not dangling, f"dangling downstream refs={dangling or 'none'}")

    # SC4 — the pivot was LOGGED as an amendment (Tier-2+), not silently rewritten.
    pivot_rows = [r for r in (rows or [])
                  if str(r.get("tier")) in ("2", "3")
                  and re.search(r"region|residency|\beu\b|\bus\b|data\s+residency", row_blob(r))
                  and r.get("disposition") in ("gated", "approved")]
    check("Spine-collapse SC4 — the pivot went through the amendment channel (a Tier-2+ row cites the region/data-"
          "residency change, gated/approved) — a logged amendment, NOT a silent rewrite",
          bool(pivot_rows), f"region/residency amendment rows={len(pivot_rows)}; "
                            f"dispositions={[r.get('disposition') for r in pivot_rows] or 'none'}")

    # SC5 — the pivot TOOK EFFECT in the spine: the regions/residency constraint FIELD now names a US region.
    regions = constraint_field(root, "Regions") or constraint_field(root, "Regions / data residency")
    took_effect = bool(re.search(r"\bUS\b|united states|us-(east|west)", regions, re.I))
    check("Spine-collapse SC5 — the pivot took effect in the spine: the data-residency constraint now admits a US "
          "region (the declaration actually changed, downstream of the amendment)",
          took_effect, f"regions constraint now='{regions[:70]}'; US admitted={took_effect}")

def grade_isolation_chain(root):
    """Test 2 — a FRESH 05, dispatched from the pipeline, reviews a BUILT slice it never built. This grader owns the
    CROSS-SEAT ISOLATION properties (the auditable attestation + the reviewed-exactly-the-handed-diff anchor + the
    caught planted violation). The FULL built-slice review grading (oracle re-run, anti-tautology litmus, ledger<->
    verdict consistency) reuses 05-reviewer's own check_review.py — already validated in that skill's evals/README.md;
    the integration README drives it. The parent-transcript-absence half is MANUAL (per shared/subagent-protocol.md)."""
    import glob
    qcands = sorted(glob.glob(os.path.join(root, "docs", "quality", "qa-report*.md")), key=len)
    qpath = next((c for c in qcands if os.path.isfile(c)), None)
    report = read(qpath) if qpath else None
    hcands = sorted(glob.glob(os.path.join(root, "_artifacts", "exports", "build-handoff*.md")), key=len)
    handoff = read(next((c for c in hcands if os.path.isfile(c)), "")) or ""

    # IC1 — the fresh 05 wrote a QA report with a verdict.
    v = fm(report or "", "verdict").upper()
    verdict = next((t for t in ("FIX REQUIRED", "BLOCK", "SHIP") if t in v), None) \
        or (lambda m: ("FIX REQUIRED" if m and m.group(1).upper().startswith("FIX") else (m.group(1).upper() if m else None)))(
            re.search(r"(?im)verdict[^A-Za-z0-9]{0,8}(SHIP|FIX\s*REQUIRED|BLOCK)", report or ""))
    check("Isolation-chain IC1 — the fresh 05 wrote a QA report stating a verdict (SHIP | FIX REQUIRED | BLOCK)",
          bool(report) and verdict in ("SHIP", "FIX REQUIRED", "BLOCK"),
          f"qa-report={'yes' if report else 'no'}; verdict={verdict}")

    # IC2 — the isolation proof: a context attestation, 'build conversation: not provided'.
    attest = bool(re.search(r"(?is)build\s+conversation[^\n]{0,40}not\s+provided", report or "")) \
        or bool(re.search(r"(?im)^\s*build_conversation\s*:\s*not[-\s]?provided", report or ""))
    check("Isolation-chain IC2 — context attestation present ('build conversation: not provided') — the auditable "
          "isolation proof that the fresh 05 never read the build session",
          attest, "attestation marker found" if attest else "no 'build conversation not provided' marker")

    # IC3 — the attestation names its inputs (the handoff + the spec slice — the seed, and ONLY the seed).
    inputs = bool(re.search(r"(?is)inputs?\W+.{0,40}(handoff|build-handoff).{0,40}(spec|slice)", report or "")) \
        or bool(re.search(r"(?is)seeded\s+with\s+only", report or ""))
    check("Isolation-chain IC3 — the attestation names its inputs as the handoff + the spec slice (05 was seeded "
          "with the realization + declarations only — a cross-seat isolation, not a hand-seeded fixture)",
          inputs, "inputs marker found" if inputs else "no 'inputs: [handoff, spec slice]' marker")

    # IC4 — sensitivity: the fresh 05 CAUGHT the planted violation (not-SHIP).
    check("Isolation-chain IC4 — the fresh 05 CAUGHT the planted spec violation (verdict not-SHIP — the isolated "
          "reviewer is not self-preferring the build)",
          verdict in ("FIX REQUIRED", "BLOCK"), f"verdict={verdict}")

    # IC5 — the planted violation is named (traceable to the REQ it violates).
    fsec = section(report or "", "Findings") or (report or "")
    named = bool(re.search(r"REQ-0*8|vc-0*2|grouping", fsec, re.I))
    check("Isolation-chain IC5 — the planted violation is NAMED in a finding (traceable to the REQ-008/VC-02 it "
          "violates) — the reviewer localized it, it did not just vibe not-SHIP",
          named, f"finding names the plant={named}")

    # IC6 — cross-seat anchor: the reviewed baseline_commit == the handoff's (05 reviewed exactly the chain's handed
    #        diff anchor, from a fresh spawner — not some other tree).
    hb = fm(handoff, "baseline_commit")
    rb = fm(report or "", "baseline_commit")
    check("Isolation-chain IC6 — the reviewed baseline_commit matches the handoff's — the fresh 05 reviewed exactly "
          "the chain's handed-off diff anchor (the cross-seat binding)",
          bool(hb) and bool(rb) and rb[:10] == hb[:10], f"handoff baseline={hb[:12] or '—'}; report baseline={rb[:12] or '—'}")


# ==================================================================================================
# CASE: agent-chain — the §10 fifth leg (5.5a). The agent-system composition end-to-end.
# ==================================================================================================

def read_first(root, *parts):
    """Read the shortest-named file matching the glob `parts` under root (or '')."""
    import glob
    for c in sorted(glob.glob(os.path.join(root, *parts)), key=len):
        if os.path.isfile(c):
            return read(c) or ""
    return ""


def grade_agent_chain(root):
    """§10 fifth leg (5.5a) — the agent-flavored chain (00 profile+contract -> 01 -> 03 topology+eval-suite VC ->
    04 -> 05 floors -> status). Grades the COMPOSED invariants the per-seat unit evals cannot: the profile
    propagates; the agent-contract is complete; an eval-suite VC row reaches EXECUTED with grader-bites; the qa tally
    is present + floor-consistent; a topology ADR carries its economics justification; the router is agent-aware."""
    spec = spec_md(root)
    pm = re.search(r"(?im)^\s*-\s*\*\*Profile:\*\*\s*`?([a-z][a-z-]*)", spec)
    profile = pm.group(1) if pm else "webapp"
    cm = claude_md(root)
    mirror = bool(re.search(r"(?im)profile[^\n]{0,20}agent-system", cm))

    # AC1 — the profile PROPAGATES: the spine declares it AND the /status emission mirrors it.
    check("Agent-chain AC1 — the profile PROPAGATES: specification.md declares `Profile: agent-system` and the "
          "/status emission mirrors it (the profile survives the whole chain)",
          profile == "agent-system" and mirror, f"spine profile={profile}; /status mirrors it={mirror}")

    # AC2 — the agent-contract is complete: six sections + >=1 tool row with a HITL column.
    ac = read(os.path.join(root, "docs/spec/agent-contract.md")) or ""
    heads = sum(bool(re.search(p, ac, re.I)) for p in
                (r"autonomy", r"risk\s*class", r"tool[- ]permission|tool\s*matrix", r"escalation|\bHITL\b",
                 r"cost\s*envelope|budget", r"memory"))
    tool_hitl = bool(re.search(r"(?i)\bHITL\b", ac)) and bool(re.search(r"(?im)^\s*\|.*\|.*\|", ac))
    check("Agent-chain AC2 — the agent-contract is complete: six sections (autonomy · risk · tool-permission matrix · "
          "escalation/HITL · cost envelope · memory) + >=1 tool row carrying a HITL column",
          heads >= 6 and tool_hitl, f"section heads={heads}/6; tool row + HITL column={tool_hitl}")

    # AC3 — an eval-suite VC row reaches EXECUTED with grader-bites (the WS3 distributional contract, carried 03->04).
    sb = specs_blob(root)
    vc_eval = bool(re.search(r"(?i)eval-suite", sb))
    handoff = read_first(root, "_artifacts", "exports", "build-handoff*.md")
    executed = bool(re.search(r"(?is)eval-suite.{0,200}EXECUTED|EXECUTED.{0,80}eval-suite", handoff))
    bites = bool(re.search(r"(?i)grader[- ]bites|degenerate[^.\n]{0,40}(fail|scored\s*0|<\s*floor)", handoff))
    check("Agent-chain AC3 — an eval-suite Verification-Contract row is carried to EXECUTED with a grader-bites "
          "attestation (the distributional contract survived 03->04, non-tautologically)",
          vc_eval and executed and bites, f"eval-suite VC row in specs={vc_eval}; EXECUTED in handoff={executed}; grader-bites={bites}")

    # AC4 — the qa tally is present AND floor-consistent: eval_floors_met false is never SHIP.
    qa = read_first(root, "docs", "quality", "qa-report*.md")
    efm = fm(qa, "eval_floors_met").lower()
    ev_run = fm(qa, "evals_run")
    verdict = fm(qa, "verdict").upper()
    tally_present = efm in ("true", "false", "n/a", "na") and bool(re.search(r"\d", ev_run or ""))
    floor_consistent = not (efm == "false" and "SHIP" in verdict)
    check("Agent-chain AC4 — 05's qa tally carries eval_floors_met + evals_run AND is floor-consistent "
          "(eval_floors_met false is never SHIP — the floor-fail-yet-SHIP guard)",
          tally_present and floor_consistent,
          f"eval_floors_met={efm or '—'}; evals_run={ev_run or '—'}; verdict={verdict}; floor-consistent={floor_consistent}")

    # AC5 — a topology ADR carries the ~15x token-economics justification (the multi-agent decision is complete).
    topo = ""
    for f in adr_files(root):
        txt = read(f) or ""
        if re.search(r"(?im)^\s*[-*]?\s*\*\*Category:\*\*\s*[^\n]*topolog", txt) or \
           re.search(r"(?im)^#\s*ADR-\d+[^\n]*(topolog|orchestrat|swarm|multi-?agent)", txt):
            topo = txt
            break
    # require the actual cost MULTIPLIER (15x / Nx tokens / N-fold / order-of-magnitude), NOT the bare phrase "token
    # economics" — a heading with no multiplier is exactly the incomplete decision AC5 exists to catch (the Phase-3
    # grader-robustness lesson: anchor on the multiplier, not the mandated phrase).
    econ = bool(topo) and bool(re.search(r"15\s*[x×]|~\s*15|\b\d+\s*(?:times|-?fold)\b"
                                         r"|\d+\s*[x×]\s*(?:the\s*|more\s*)?tokens?|order[- ]of[- ]magnitude", topo, re.I))
    check("Agent-chain AC5 — a topology ADR carries the ~15x token-economics justification (a multi-agent topology "
          "decision weighing no cost multiplier is incomplete)",
          bool(topo) and econ, f"topology ADR present={bool(topo)}; economics justification={econ}")

    # AC6 — the router is agent-aware: integrity PASS + the profile mirror + a routed next command.
    iv = integrity_verdict(root)
    nc = next_command(root)
    check("Agent-chain AC6 — the router is agent-aware: /status emits integrity PASS, mirrors `Profile: agent-system`, "
          "and routes a next command (the profile reaches the derived-state view)",
          iv == "PASS" and mirror and bool(nc), f"integrity={iv}; profile mirrored={mirror}; next command={nc or 'none'}")


def grade_verify_live_chain(root):
    """WS6 — the live-source verification chain (00 declares+seeds -> 03 cites -> 04 verifies -> 06 gates). Grades the
    COMPOSED invariant the per-seat self-tests cannot: ONE declared verify-live tech flows coherently across the
    chain, anchored on a single docs/verification/<tech>.md record. See shared/live-source-verification.md."""
    ac = read(os.path.join(root, "docs/spec/architecture-constraints.md")) or ""
    m = re.search(r"(?ims)^##\s+Verify-live\b.*?(?=^##\s|\Z)", ac)
    techs = set()
    if m:
        for line in m.group(0).splitlines():
            tm = re.match(r"^\s*-\s*\*\*([A-Za-z0-9][\w.-]*?):\*\*", line)
            if tm:
                techs.add(tm.group(1))
    records = set()
    vdir = os.path.join(root, "docs/verification")
    if os.path.isdir(vdir):
        records = {fn[:-3] for fn in os.listdir(vdir) if fn.endswith(".md")}

    # VL1 — 00 declares + seeds: the L7 conditions, re-checked independently — every declared tech resolves to a
    #        cited record, no orphan record, no uncited claim (the confabulation anchor).
    problems = []
    if not techs and not records:
        problems.append("nothing declared and no records")
    problems += ["declared '%s': no docs/verification/%s.md" % (t, t) for t in sorted(techs - records)]
    problems += ["orphan record '%s' (no declaration)" % t for t in sorted(records - techs)]
    for t in sorted(techs & records):
        sec = re.search(r"(?ims)^##\s+Verified\s+claims\b.*?(?=^##\s|\Z)", read(os.path.join(vdir, t + ".md")) or "")
        cited = 0
        for line in (sec.group(0).splitlines() if sec else []):
            if not line.strip().startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 2 or set("".join(cells)) <= set("-: "):
                continue
            if cells[0].lower().startswith("claim") and cells[1].lower().startswith("citation"):
                continue
            if cells[1]:
                cited += 1
            else:
                problems.append("'%s': uncited claim" % t)
        if cited == 0:
            problems.append("'%s': no cited claim" % t)
    check("Verify-live VL1 — 00 declares + seeds: each `## Verify-live` tech resolves to a cited "
          "docs/verification/<tech>.md; no orphan record; no uncited claim (the confabulation anchor)",
          not problems, "declared=%s; records=%s; problems=%s" % (sorted(techs), sorted(records), problems or "none"))

    # VL2 — 03 cites: an ADR whose Decision names a declared tech carries a Verified-against citation to the record.
    adr_ok, adr_note = False, "no ADR Decision names a declared verify-live tech"
    for f in adr_files(root):
        txt = read(f) or ""
        dec = re.search(r"##+\s*Decision\s+Outcome(.+?)(?:\n##\s|\Z)", txt, re.I | re.S)
        dtxt = dec.group(1) if dec else txt
        named = [t for t in techs if re.search(r"\b" + re.escape(t) + r"\b", dtxt, re.I)]
        if named:
            ok = bool(re.search(r"(?im)Verified-against", txt)) and \
                any(("docs/verification/%s.md" % t) in txt for t in named)
            adr_ok, adr_note = ok, "%s names %s; cited=%s" % (os.path.basename(f), named, ok)
            if ok:
                break
    check("Verify-live VL2 — 03 cites: an ADR whose Decision names the verify-live tech carries a `Verified-against: "
          "docs/verification/<tech>.md` citation (the tech-mandate flow)", adr_ok, adr_note)

    # VL3 — 04 verifies: a handoff VC row carries `verified: docs/verification/<tech>.md` AND is EXECUTED/OBSERVED
    #        (never INFERRED — a cited-but-inferred verify-live claim is contradictory).
    handoff = read_first(root, "_artifacts", "exports", "build-handoff*.md")
    vl3_ok, vl3_note = False, "no `verified:` verify-live row in the handoff"
    for line in handoff.splitlines():
        if re.search(r"(?i)verified:\s*\S*docs/verification/", line):
            st = re.search(r"\b(EXECUTED|OBSERVED|INFERRED)\b", line)
            vl3_ok = bool(st) and st.group(1) in ("EXECUTED", "OBSERVED")
            vl3_note = "verified row state=%s" % (st.group(1) if st else "unstamped")
            break
    check("Verify-live VL3 — 04 verifies: a build-handoff VC row carries `verified: docs/verification/<tech>.md` and "
          "is EXECUTED/OBSERVED, never INFERRED (built against the record, not memory)", vl3_ok, vl3_note)

    # VL4 — 06 gates: the release report ships (RELEASED) with G11 recorded PASS over the verify-live record.
    report = read_first(root, "docs", "release", "release-report*.md")
    status = (fm(report, "status") or "").upper()
    g11_pass = bool(re.search(r"(?im)G11[^\n]*\bPASS\b", report)) and \
        bool(re.search(r"(?i)verify-live|docs/verification", report))
    check("Verify-live VL4 — 06 gates: the release report ships (RELEASED) with G11 recorded PASS over the verify-live "
          "record (the ship went through the gate, not around it)",
          "RELEASED" in status and g11_pass, "status=%s; G11 pass=%s" % (status or "—", g11_pass))

    # VL5 — currency: the record's verified_against version matches the dependency manifest (a stale record blocks;
    #        no manifest pin ⇒ N/A, recorded).
    pkg = read(os.path.join(root, "package.json")) or ""
    vl5_ok, vl5_note = bool(techs), "no verify-live tech to check"
    for t in sorted(techs):
        rec = read(os.path.join(vdir, t + ".md")) or ""
        rv = re.search(r"(?im)^verified_against:\s*%s@([\w.\-]+)" % re.escape(t), rec)
        pv = re.search(r'"%s"\s*:\s*"[~^]?([\w.\-]+)"' % re.escape(t), pkg)
        if rv and pv:
            vl5_ok, vl5_note = rv.group(1) == pv.group(1), "%s: record=%s manifest=%s" % (t, rv.group(1), pv.group(1))
        elif rv:
            vl5_ok, vl5_note = True, "%s: record=%s; no manifest pin — currency N/A" % (t, rv.group(1))
        else:
            vl5_ok, vl5_note = False, "%s: record has no verified_against version" % t
        if not vl5_ok:
            break
    check("Verify-live VL5 — currency: the record's verified_against version matches the dependency manifest (a stale "
          "record is caught; no manifest pin ⇒ N/A)", vl5_ok, vl5_note)


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outputs", required=True)
    ap.add_argument("--case", required=True,
                    choices=["spec-first", "governance", "spine-collapse", "isolation-chain", "agent-chain",
                             "verify-live"])
    a = ap.parse_args()
    root = find_root(os.path.abspath(a.outputs))
    {"spec-first": grade_spec_first, "governance": grade_governance,
     "spine-collapse": grade_spine_collapse, "isolation-chain": grade_isolation_chain,
     "agent-chain": grade_agent_chain, "verify-live": grade_verify_live_chain}[a.case](root)

    passed = sum(1 for r in results if r["passed"])
    print("\n== check_integration: %s — %d/%d ==" % (a.case, passed, len(results)))
    for r in results:
        print("  [%s] %s" % ("PASS" if r["passed"] else "FAIL", r["text"]))
        if not r["passed"]:
            print("         evidence: %s" % r["evidence"])
    with open(os.path.join(a.outputs, "grading.json"), "w", encoding="utf-8") as f:
        json.dump({"expectations": results}, f, indent=2)
    print("grading.json -> %s" % os.path.join(a.outputs, "grading.json"))


if __name__ == "__main__":
    main()
