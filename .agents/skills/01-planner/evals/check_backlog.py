#!/usr/bin/env python3
"""Deterministic grader for 01-planner evals. Structural assertions over a produced build plan.

The lift of 01-planner is a *structured contract* the next skills consume — a backlog ledger keyed by REQ-ID
(REQ -> epic -> sprint -> execution status), build-order epics, and sprint files carrying a frozen Gherkin
snapshot + a "Done When". A baseline (no skill) writes an ad-hoc plan that does not satisfy this contract. So we
grade structure, not prose — no LLM judge.

Usage:
    python check_backlog.py --outputs <dir> --case <teampulse|foundation-chain>

The --outputs dir is the project root: it is seeded with the spine (docs/spec/, docs/discovery/) and the skill
adds docs/planning/. Writes grading.json ({"expectations":[{text,passed,evidence}]}) into --outputs and prints a
report.
"""
import os, re, json, argparse

results = []
def check(text, passed, evidence=""):
    results.append({"text": text, "passed": bool(passed), "evidence": str(evidence)[:300]})

def read(p):
    try:
        with open(p, encoding="utf-8") as f: return f.read()
    except Exception: return None

# Per-case anchors: the foundation REQ (built first), a consuming REQ (built later), and the core end-to-end
# thread the walking-skeleton sprint 1 must thread through. Pairs allow either canonical anchor to satisfy.
CASES = {
    "teampulse": {
        "foundation": ["REQ-007", "REQ-004"],   # magic-link auth / create-team — the access foundation
        "consumer":   ["REQ-010", "REQ-009"],   # read digests / needs-help surfacing — consuming features
        "thread":     ["REQ-007", "REQ-001", "REQ-008"],  # sign in -> submit standup -> generate digest
    },
    "foundation-chain": {
        "foundation": ["REQ-005"],              # connect a bank account — the root dependency (sorts LAST in registry)
        "consumer":   ["REQ-001", "REQ-002"],   # monthly summary / budgets — consuming features
        "thread":     ["REQ-005", "REQ-003", "REQ-001"],  # connect -> categorize -> see summary
    },
}
EXEC_STATUS = {"planned", "in-progress", "in progress", "done"}
FIDELITY_STATUS = {"stated", "derived"}


def find_root(base):
    """Return the dir containing docs/spec/specification.md (the seeded spine) under base; fall back to base."""
    for dp, dn, fn in os.walk(base):
        if dp.replace("\\", "/").endswith("docs/spec") and "specification.md" in fn:
            return os.path.dirname(os.path.dirname(dp))
    return base


def parse_registry(spec):
    """Spine registry rows: | REQ-001 | name | MUST | stated | capabilities/x.md |."""
    return re.findall(r"\|\s*(REQ-\d+)\s*\|([^|\n]*)\|([^|\n]*)\|([^|\n]*)\|([^|\n]*)\|", spec or "")


def _split_row(line):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells


def _first_int(s):
    m = re.search(r"\d+", s or "")
    return int(m.group(0)) if m else None


def parse_ledger(backlog):
    """Header-driven parse of the ledger table(s). Returns {req: {'epic':int|None,'sprint':int|None,'status':str}}.

    Primary: one flat table with REQ + Epic + Sprint + Status columns (the template). Fallback: per-`## Epic N`
    sections whose rows carry Sprint/Status columns (epic taken from the section header).
    """
    out = {}
    lines = (backlog or "").splitlines()

    # --- primary: flat table, header-driven columns ---
    for i, line in enumerate(lines):
        if "|" not in line:
            continue
        header = [c.lower() for c in _split_row(line)]
        if not ("req" in header and "status" in header and ("epic" in header or "sprint" in header)):
            continue
        col = {name: idx for idx, name in enumerate(header)}
        # consume following data rows
        for dl in lines[i + 1:]:
            if "|" not in dl:
                break
            cells = _split_row(dl)
            if not cells or set("".join(cells)) <= set("-: "):  # separator row
                continue
            rowtext = " ".join(cells)
            rm = re.search(r"REQ-\d+", rowtext)
            if not rm:
                if re.search(r"\bREQ\b|name|priority", rowtext, re.I):
                    continue  # a second header line
                break
            req = rm.group(0)
            def cell(name):
                idx = col.get(name)
                return cells[idx] if idx is not None and idx < len(cells) else ""
            epic = _first_int(cell("epic"))
            sprint = _first_int(cell("sprint"))
            status = cell("status").lower()
            if not status:  # status keyword anywhere in the row
                for kw in EXEC_STATUS:
                    if kw in rowtext.lower():
                        status = kw; break
            out[req] = {"epic": epic, "sprint": sprint, "status": status}
        if out:
            return out

    # --- fallback: per-`## Epic N` sections ---
    cur_epic = None
    for line in lines:
        hm = re.match(r"^#{1,4}\s+.*epic\s*(\d+)", line, re.I)
        if hm:
            cur_epic = int(hm.group(1)); continue
        bm = re.match(r"^\s*\d+\.\s+.*epic\s*(\d+)", line, re.I)
        if bm:
            cur_epic = int(bm.group(1))
        if "|" in line:
            rm = re.search(r"REQ-\d+", line)
            if rm:
                req = rm.group(0)
                low = line.lower()
                status = next((kw for kw in EXEC_STATUS if kw in low), "")
                sprint = None
                sm = re.search(r"sprint[-\s]?(\d+)", low) or re.search(r"\|\s*0*(\d+)\s*\|", line)
                if sm:
                    sprint = int(sm.group(1))
                out.setdefault(req, {"epic": cur_epic, "sprint": sprint, "status": status})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outputs", required=True)
    ap.add_argument("--case", required=True, choices=list(CASES.keys()))
    a = ap.parse_args()
    cfg = CASES[a.case]
    root = find_root(a.outputs)

    spec = read(os.path.join(root, "docs/spec/specification.md")) or ""
    reg = parse_registry(spec)
    reg_reqs = [r[0] for r in reg]
    reg_status = {r[0]: r[3].strip().lower() for r in reg}
    reg_file = {r[0]: os.path.basename(r[4].strip()) for r in reg}

    backlog = read(os.path.join(root, "docs/planning/backlog.md"))
    if backlog is None:
        check("Backlog ledger written at docs/planning/backlog.md", False,
              f"no docs/planning/backlog.md under {root}")
        # still try sprint + spine checks below with empty ledger
        backlog = ""
        ledger = {}
    else:
        check("Backlog ledger written at docs/planning/backlog.md", True, f"{len(backlog)} chars")
        ledger = parse_ledger(backlog)

    # A1 — ledger table present with REQ rows mapping epic/sprint/status
    has_cols = any(v["epic"] is not None or v["sprint"] is not None for v in ledger.values())
    check("Ledger maps REQ -> epic/sprint/status (the contract the next skills consume)",
          len(ledger) > 0 and has_cols,
          f"{len(ledger)} REQ rows; epic/sprint columns present={has_cols}")

    # A2 — every spine REQ appears exactly once
    led_set = set(ledger.keys())
    reg_set = set(reg_reqs)
    missing = sorted(reg_set - led_set)
    extra = sorted(led_set - reg_set)
    dup = len(ledger) != len(led_set)  # parse keys are unique; dup rows collapse — check raw row count instead
    raw_reqs = re.findall(r"^\s*\|.*?(REQ-\d+)", backlog, re.M)
    dup_ids = sorted({x for x in raw_reqs if raw_reqs.count(x) > 1})
    check("Every spine REQ appears in the ledger exactly once (none dropped, none duplicated)",
          reg_set and not missing and not extra and not dup_ids,
          f"missing={missing or 'none'}; extra={extra or 'none'}; duplicated={dup_ids or 'none'}")

    # A3 — no invented REQ-IDs
    check("No invented REQ-IDs: every ledger REQ exists in the spine registry",
          bool(led_set) and not extra, f"unknown IDs={extra or 'none'}")

    # A4 — ledger status is execution vocab, never fidelity vocab
    statuses = {v["status"] for v in ledger.values() if v["status"]}
    leaked = sorted(s for s in statuses if s in FIDELITY_STATUS)
    nonexec = sorted(s for s in statuses if s and s not in EXEC_STATUS)
    check("Ledger status is execution-only (planned/in-progress/done), never spine fidelity (stated/derived)",
          bool(statuses) and not leaked and not nonexec,
          f"statuses={sorted(statuses) or 'none'}; fidelity-leak={leaked or 'none'}")

    # A5 — sprint-01.md: canonical path, REQ refs, frozen Gherkin, Done When
    sp_path = os.path.join(root, "docs/planning/sprints/sprint-01.md")
    sp = read(sp_path)
    if sp is None:
        # report what sprint files exist, if any
        sdir = os.path.join(root, "docs/planning/sprints")
        found = sorted(os.listdir(sdir)) if os.path.isdir(sdir) else []
        check("sprint-01.md written at docs/planning/sprints/ (zero-padded)", False,
              f"sprint-01.md absent; sprints dir={found or 'missing'}")
        sp1_reqs = []
    else:
        sp1_reqs = sorted(set(re.findall(r"REQ-\d+", sp)))
        has_gherkin = ("```gherkin" in sp) or bool(re.search(r"given\b.*\bwhen\b.*\bthen\b", sp, re.I | re.S))
        has_done = bool(re.search(r"done\s*when", sp, re.I))
        check("sprint-01.md: references REQ-IDs + frozen Gherkin snapshot + a 'Done When'",
              bool(sp1_reqs) and has_gherkin and has_done,
              f"reqs={sp1_reqs}; gherkin={has_gherkin}; done_when={has_done}")

    # A6 — two-status separation: the seeded spine registry is uncorrupted (still only stated/derived)
    spine_leak = sorted({rid for rid, st in reg_status.items() if st and st not in FIDELITY_STATUS})
    check("Two-status separation: spine registry Status untouched (only stated/derived; no execution status leaked in)",
          bool(reg_status) and not spine_leak,
          f"spine REQs with non-fidelity status={spine_leak or 'none'}")

    # A7 — build-order epics: foundation epic precedes consuming epic
    def epic_of(reqs):
        vals = [ledger[r]["epic"] for r in reqs if r in ledger and ledger[r]["epic"] is not None]
        return min(vals) if vals else None
    fe, ce = epic_of(cfg["foundation"]), epic_of(cfg["consumer"])
    check("Build-order epics: the foundation epic is ordered before the consuming epic",
          fe is not None and ce is not None and fe < ce,
          f"epic(foundation {cfg['foundation']})={fe} < epic(consumer {cfg['consumer']})={ce}")

    # A8 — sprint 1 is a thin vertical slice that includes its foundation
    # sprint-1 membership: prefer the ledger (Sprint==1); fall back to REQ refs in sprint-01.md
    s1 = {r for r, v in ledger.items() if v["sprint"] == 1}
    if not s1:
        s1 = set(sp1_reqs)
    found_foundation = [r for r in cfg["foundation"] if r in s1]
    domains = {reg_file.get(r) for r in s1 if reg_file.get(r)}
    thread_in = [r for r in cfg["thread"] if r in s1]
    vertical = len(domains) >= 2
    foundation_in = bool(found_foundation)
    thread_ok = len(thread_in) >= max(2, len(cfg["thread"]) - 1)  # the core thread (allow one slack)
    check("Sprint 1 is a thin vertical slice including its foundation (spans >=2 domains; foundation + core thread present)",
          bool(s1) and foundation_in and vertical and thread_ok,
          f"sprint1={sorted(s1)}; foundation_in={found_foundation}; domains={sorted(d for d in domains if d)}; thread={thread_in}")

    emit(a)


def emit(a):
    ok = sum(1 for r in results if r["passed"])
    print(f"\n=== {a.case}: {ok}/{len(results)} assertions passed ===")
    for r in results:
        print(f"  [{'PASS' if r['passed'] else 'FAIL'}] {r['text']}")
        if r["evidence"]:
            print(f"         -> {r['evidence']}")
    gj = os.path.join(a.outputs, "grading.json")
    try:
        with open(gj, "w", encoding="utf-8") as f:
            json.dump({"expectations": results}, f, indent=2)
        print(f"\nwrote {gj}")
    except Exception as e:
        print(f"\n(could not write grading.json: {e})")


if __name__ == "__main__":
    main()
