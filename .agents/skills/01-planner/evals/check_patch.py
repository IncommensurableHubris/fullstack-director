#!/usr/bin/env python3
"""Deterministic grader for 01-planner PATCH-MODE evals (WS1 delta path).

The lift is the *certified expedite lane*: a small fix gets a patch record (five-check classification gate,
P1-P5, each evidenced), a Patches ledger row (the sole status origin), and a dispatch to /04-builder — while a
fix that secretly needs a new REQ is REFUSED and routed to /00-discovery reflect, and no sprint/design/
architecture ceremony is spun up either way. A baseline improvises some of this; it does not satisfy the
structured contract, refuse hidden scope, or keep the spine byte-identical. Structural assertions — no LLM judge.

Usage:
    python check_patch.py --outputs <dir> --case <patch-small|patch-hidden-scope|patch-ceremony-decline>
                          [--fixture <evals/fixtures/patchable>]

--outputs is the project root (seeded with the patchable fixture; the skill adds docs/planning/patches/ etc.).
--fixture enables the byte-identity check of docs/spec/** against the seed (P2's mechanical form).
Writes grading.json into --outputs and prints a report.
"""
import os, re, json, argparse

results = []
def check(text, passed, evidence=""):
    results.append({"text": text, "passed": bool(passed), "evidence": str(evidence)[:300]})

def read(p):
    try:
        with open(p, encoding="utf-8") as f: return f.read()
    except Exception: return None

def find_root(base):
    for dp, dn, fn in os.walk(base):
        if dp.replace("\\", "/").endswith("docs/spec") and "specification.md" in fn:
            return os.path.dirname(os.path.dirname(dp))
    return base

def parse_frontmatter(text):
    """Regex-parse the YAML frontmatter block: top-level keys, the reqs list, the size_budget fields."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text or "", re.S)
    if not m:
        return None
    block = m.group(1)
    keys = re.findall(r"(?m)^([A-Za-z_][\w-]*):", block)
    def section(key):
        sm = re.search(r"(?ms)^%s:(.*?)(?=^[A-Za-z_][\w-]*:|\Z)" % key, block)
        return sm.group(1) if sm else ""
    reqs = re.findall(r"REQ-\d+", section("reqs"))
    sb = section("size_budget")
    files = re.search(r"files\D*(\d+)", sb)
    loc = re.search(r"loc\D*(\d+)", sb)
    pm = re.search(r"patch-\d+", section("patch"))
    return {
        "keys": keys,
        "patch": pm.group(0) if pm else None,
        "reqs": reqs,
        "budget_files": int(files.group(1)) if files else None,
        "budget_loc": int(loc.group(1)) if loc else None,
    }

def norm(s):
    return (s or "").replace("\r\n", "\n")

def spine_identical(root, fixture):
    """Byte-compare docs/spec/** (newline-normalized) between the produced root and the fixture seed."""
    diffs = []
    fix_spec = os.path.join(fixture, "docs", "spec")
    out_spec = os.path.join(root, "docs", "spec")
    fix_files, out_files = {}, {}
    for base, store in ((fix_spec, fix_files), (out_spec, out_files)):
        for dp, dn, fn in os.walk(base):
            for f in fn:
                store[os.path.relpath(os.path.join(dp, f), base).replace("\\", "/")] = os.path.join(dp, f)
    for rel in sorted(set(fix_files) | set(out_files)):
        if rel not in out_files:
            diffs.append("missing: " + rel)
        elif rel not in fix_files:
            diffs.append("added: " + rel)
        elif norm(read(fix_files[rel])) != norm(read(out_files[rel])):
            diffs.append("changed: " + rel)
    return diffs

def list_patches(root):
    pdir = os.path.join(root, "docs", "planning", "patches")
    if not os.path.isdir(pdir):
        return pdir, []
    return pdir, sorted(f for f in os.listdir(pdir) if f.endswith(".md"))

def ledger_patch_rows(backlog):
    """Rows of the ## Patches table: (patch_id, full row text)."""
    return [(m.group(1), m.group(0)) for m in re.finditer(r"(?m)^\|\s*`?(patch-\d+)`?\s*\|[^\n]*\|", backlog or "")]

def ceremony_artifacts(root, fixture=None, seeded_sprints=("sprint-01.md",)):
    """New sprint files beyond the seed, plus design/ or architecture/ trees the PATCH created. With a fixture (the
    seed), a design/architecture tree counts as ceremony only if it is NEW vs the seed — a mid-life project
    legitimately already has them; a patch must not ADD one. Without a fixture, any such tree is flagged (the
    greenfield unit-fixture assumption)."""
    found = []
    sdir = os.path.join(root, "docs", "planning", "sprints")
    if os.path.isdir(sdir):
        found += ["docs/planning/sprints/" + f for f in sorted(os.listdir(sdir)) if f not in seeded_sprints]
    for tree in ("docs/design", "docs/architecture"):
        in_seed = bool(fixture) and os.path.isdir(os.path.join(fixture, tree))
        if os.path.isdir(os.path.join(root, tree)) and not in_seed:
            found.append(tree + "/")
    return found

EXEC_VOCAB = {"planned", "in-progress", "in progress", "done", "escalated"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outputs", required=True)
    ap.add_argument("--case", required=True,
                    choices=["patch-small", "patch-hidden-scope", "patch-ceremony-decline"])
    ap.add_argument("--fixture", default=None, help="fixture root for the docs/spec byte-identity check")
    a = ap.parse_args()
    root = find_root(a.outputs)

    spec = read(os.path.join(root, "docs/spec/specification.md")) or ""
    registry = set(re.findall(r"(?m)^\|\s*(REQ-\d+)\s*\|", spec))
    backlog = read(os.path.join(root, "docs/planning/backlog.md")) or ""
    pdir, patches = list_patches(root)
    rows = ledger_patch_rows(backlog)

    # -- every case: the spine is untouched (P2's mechanical form) and no ceremony is spun up --
    if a.fixture:
        diffs = spine_identical(root, a.fixture)
        check("Spine untouched: docs/spec/** byte-identical to the seed (P2)", not diffs,
              "; ".join(diffs[:6]) if diffs else "identical")
    cere = ceremony_artifacts(root, a.fixture)
    check("Ceremony declined: no new sprint files, no docs/design/, no docs/architecture/",
          not cere, "; ".join(cere[:6]) if cere else "none created")

    if a.case in ("patch-small", "patch-ceremony-decline"):
        # A1 — exactly one record, max(patches)+1 numbering from an empty dir => patch-001.md
        check("Patch record written at docs/planning/patches/patch-001.md (max+1, zero-padded, exactly one)",
              patches == ["patch-001.md"], f"patches dir: {patches or 'empty/absent'}")
        rec = read(os.path.join(pdir, "patch-001.md")) or ""
        fm = parse_frontmatter(rec)

        # A2 — ledger row exactly once, execution vocabulary, planned at certification
        p1_rows = [r for r in rows if r[0] == "patch-001"]
        statuses = [next((kw for kw in EXEC_VOCAB if kw in r[1].lower()), "") for r in p1_rows]
        check("Ledger: exactly one `## Patches` row for patch-001, status `planned` (sole status origin)",
              len(p1_rows) == 1 and statuses == ["planned"],
              f"rows={[r[1] for r in rows][:4]}")

        if a.case == "patch-small":
            check("Record frontmatter: patch id + owning reqs + size_budget (files/loc)",
                  bool(fm) and fm["patch"] == "patch-001" and bool(fm["reqs"])
                  and fm["budget_files"] is not None and fm["budget_loc"] is not None,
                  f"fm={ {k: v for k, v in (fm or {}).items() if k != 'keys'} }")
            check("Record carries NO status field (the ledger is the sole status origin)",
                  bool(fm) and "status" not in [k.lower() for k in fm["keys"]],
                  f"frontmatter keys={fm['keys'] if fm else None}")
            dangling = sorted(set(fm["reqs"]) - registry) if fm else ["(no frontmatter)"]
            check("Every owning REQ resolves in the spine registry (P1)",
                  bool(fm) and bool(fm["reqs"]) and not dangling,
                  f"reqs={fm['reqs'] if fm else None}; dangling={dangling or 'none'}")
            missing_checks = [f"P{n}" for n in range(1, 6)
                              if not re.search(r"(?m)^.*\bP%d\b.{15,}$" % n, rec)]
            check("All five gate checks P1-P5 evidenced on the record",
                  not missing_checks, f"missing/unevidenced: {missing_checks or 'none'}")
            check("Dispatch names /04-builder on the record",
                  bool(re.search(r"/0?4-builder", rec)), "found" if re.search(r"/0?4-builder", rec) else "absent")

    if a.case == "patch-hidden-scope":
        check("No patch certified: docs/planning/patches/ absent or empty", not patches,
              f"patches dir: {patches or 'empty/absent'}")
        check("No `## Patches` ledger row added", not rows, f"rows={[r[1] for r in rows][:4]}")
        # the refusal must be routed, visibly: any produced .md (incl. the saved final response) outside docs/spec
        esc_hits = []
        for dp, dn, fn in os.walk(root):
            rel = os.path.relpath(dp, root).replace("\\", "/")
            if rel.startswith("docs/spec"):
                continue
            for f in fn:
                if f.endswith(".md"):
                    t = read(os.path.join(dp, f)) or ""
                    if re.search(r"00[-\s]?(discovery\s+)?reflect", t, re.I):
                        esc_hits.append(os.path.join(rel, f).replace("\\", "/").lstrip("./"))
        check("Escalation routed to /00-discovery reflect (Tier-3 scope signal), recorded visibly",
              bool(esc_hits), f"found in: {esc_hits[:4] or 'nowhere'}")

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
