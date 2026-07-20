#!/usr/bin/env python3
"""Deterministic grader for 02-designer evals. Structural + amendment-aware assertions over a realized design.

02-designer's lift is a *structured design contract* the next skills consume — a tiered-token design system that
references REQs, per-screen specs, a DM-ID manifest, owner-tagged DDRs — PLUS the debut of the amendment protocol:
the dual-pass Reconcile emits `amendment-log.json` rows. Design *beauty* is subjective and is NOT graded (a strong
baseline also designs well). So we grade structure + amendment semantics, never aesthetics — no LLM judge.

The one move that makes a *design* contradiction gradeable deterministically is the **WCAG contrast computation**
(sRGB -> relative luminance -> ratio): a `stated` brand color that fails AA against a `stated` a11y mandate is a
*computed* contradiction, so "did the skill catch it and log a Tier-2 amendment row?" is an objective check.

Usage:
    python check_design.py --outputs <dir> --case <clean-intent|contrast-conflict|derived-intent>

The --outputs dir is the project root: it is seeded with the spine (docs/spec/, docs/planning/sprints/) and the
skill ADDS docs/design/ and APPENDS docs/spec/amendment-log.json. Writes grading.json
({"expectations":[{text,passed,evidence}]}) into --outputs and prints a report.
"""
import os, re, json, argparse

results = []
def check(text, passed, evidence=""):
    results.append({"text": text, "passed": bool(passed), "evidence": str(evidence)[:300]})

def read(p):
    try:
        with open(p, encoding="utf-8") as f: return f.read()
    except Exception: return None


# ---------- WCAG 2.x contrast (the deterministic heart) ----------

def _channel_lin(v8):
    """One 8-bit sRGB channel -> linear-light value (WCAG definition)."""
    cs = v8 / 255.0
    return cs / 12.92 if cs <= 0.03928 else ((cs + 0.055) / 1.055) ** 2.4

def luminance(hexstr):
    h = hexstr.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return 0.2126 * _channel_lin(r) + 0.7152 * _channel_lin(g) + 0.0722 * _channel_lin(b)

def contrast(hex1, hex2):
    """Contrast ratio (1..21) of two hex colors."""
    l1, l2 = luminance(hex1), luminance(hex2)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


# ---------- spine / design parsing ----------

HEX = re.compile(r"#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
SEMANTIC_TOK = re.compile(r"--(?:text|bg|primary|secondary|border|error|success|warning|info)[\w-]*")
PRIMITIVE_TOK = re.compile(r"--color-[\w-]*")

def find_root(base):
    """Return the dir containing docs/spec/specification.md (the seeded spine) under base; fall back to base."""
    for dp, dn, fn in os.walk(base):
        if dp.replace("\\", "/").endswith("docs/spec") and "specification.md" in fn:
            return os.path.dirname(os.path.dirname(dp))
    return base

def amendments(root):
    """The amendment-log.json rows (list), or None if the file is missing/invalid."""
    al = read(os.path.join(root, "docs/spec/amendment-log.json"))
    if al is None:
        return None
    try:
        a = json.loads(al)
        return a.get("amendments") if isinstance(a.get("amendments"), list) else None
    except Exception:
        return None

def sprint_reqs(root):
    """REQ-IDs in the seeded sprint-01 slice (what the screens must reference)."""
    sp = read(os.path.join(root, "docs/planning/sprints/sprint-01.md")) or ""
    return sorted(set(re.findall(r"REQ-\d+", sp)))

def declared_brand_hex(root):
    """The brand/primary hex declared in design-intent.md (prefer a brand/primary/link/cta line)."""
    intent = read(os.path.join(root, "docs/spec/design-intent.md")) or ""
    for line in intent.splitlines():
        if re.search(r"brand|primary|link|cta|accent|button", line, re.I):
            m = HEX.search(line)
            if m:
                return m.group(0)
    m = HEX.search(intent)
    return m.group(0) if m else None

def design_screens(root):
    """Top-level docs/design/*.md screen files (exclude design-system.md and the approved/ contract)."""
    ddir = os.path.join(root, "docs/design")
    out = []
    if os.path.isdir(ddir):
        for f in sorted(os.listdir(ddir)):
            if f.endswith(".md") and f != "design-system.md":
                out.append(os.path.join(ddir, f))
    return out

def manifest_text(root):
    """Concatenated text of any manifest.md under docs/design/approved/."""
    adir = os.path.join(root, "docs/design/approved")
    blob = ""
    if os.path.isdir(adir):
        for dp, dn, fn in os.walk(adir):
            for f in fn:
                if f == "manifest.md":
                    blob += (read(os.path.join(dp, f)) or "") + "\n"
    return blob


# ---------- shared structural assertions (the contract the next skills consume) ----------

def grade_structure(root, reqs):
    ds = read(os.path.join(root, "docs/design/design-system.md"))
    if ds is None:
        check("design-system.md written at docs/design/design-system.md", False,
              f"no docs/design/design-system.md under {root}")
        ds = ""
    else:
        check("design-system.md written at docs/design/design-system.md", True, f"{len(ds)} chars")

    # S2 — tiered tokens: a primitive layer AND a semantic role layer (the governed vocabulary)
    sem = sorted(set(SEMANTIC_TOK.findall(ds)))
    prim = sorted(set(PRIMITIVE_TOK.findall(ds)))
    has_sem = len(sem) >= 3 or bool(re.search(r"^#{1,6}.*\bsemantic\b", ds, re.I | re.M))
    has_prim = bool(prim) or bool(re.search(r"^#{1,6}.*\b(primitive|raw)\b", ds, re.I | re.M))
    check("Tiered tokens: design-system has a primitive layer AND a semantic role layer (governed vocabulary)",
          has_sem and has_prim,
          f"semantic tokens={sem[:6]}{'…' if len(sem) > 6 else ''}; primitive tokens={prim[:4] or 'via heading'}")

    # S3 — the design references the spine by REQ-ID (traceability, not copied prose)
    ds_reqs = sorted(set(re.findall(r"REQ-\d+", ds)))
    check("design-system references the spine by REQ-ID (traceability, not copied requirement prose)",
          bool(ds_reqs), f"REQ refs in design-system={ds_reqs or 'none'}")

    # S4 — >=1 screen file references this sprint's REQs
    screens = design_screens(root)
    screen_hits = {}
    for sf in screens:
        srefs = set(re.findall(r"REQ-\d+", read(sf) or ""))
        inter = sorted(srefs & set(reqs))
        if inter:
            screen_hits[os.path.basename(sf)] = inter
    check("At least one docs/design/<screen>.md references this sprint's REQs",
          bool(screen_hits),
          f"screens={[os.path.basename(s) for s in screens] or 'none'}; sprint-REQ refs={screen_hits or 'none'}")

    # S5 — DM-ID manifest present
    man = manifest_text(root)
    dm_ids = sorted(set(re.findall(r"DM-\d+", man)))
    check("DM-ID manifest present under docs/design/approved/sprint-NN/ with DM-IDs",
          bool(dm_ids), f"DM-IDs={dm_ids[:8]}{'…' if len(dm_ids) > 8 else ''}")

    # S6 — DDR section (owner-tagged design decisions)
    check("Design Decision Records (DDR) section present in design-system.md",
          bool(re.search(r"DDR-\d+", ds)) or bool(re.search(r"design decision", ds, re.I)),
          "found DDR marker" if re.search(r"DDR-\d+|design decision", ds, re.I) else "no DDR section")

    # S7 — amendment log is valid and was appended to (or validly empty)
    rows = amendments(root)
    check("amendment-log.json is valid JSON with an 'amendments' array",
          rows is not None, "valid" if rows is not None else "missing/invalid amendment-log.json")
    return ds, rows


# ---------- WS3 Task 3.4: agent-experience mode (tool surface as the UX) ----------

def agent_contract_tools(root):
    """Tool names from the agent-contract tool-permission matrix's first column (the interface to cover)."""
    ac = read(os.path.join(root, "docs/spec/agent-contract.md")) or ""
    lines, hdr = ac.splitlines(), None
    for i, ln in enumerate(lines):
        low = ln.strip().lower()
        if low.startswith("|") and "tool" in low and "hitl" in low and "risk" in low:
            hdr = i
            break
    tools = []
    if hdr is not None:
        for dl in lines[hdr + 1:]:
            s = dl.strip()
            if not s.startswith("|"):
                break
            if re.match(r"^\|[\s:\-|]+\|?\s*$", s):
                continue
            first = re.sub(r"_<.*?>_", "", s.strip("|").split("|")[0]).strip().strip("`").strip()
            if first:
                tools.append(first)
    return tools


def grade_agent_experience(root, reqs):
    """Under Profile: agent-system, 02 realizes the TOOL SURFACE + conversation + persona + refusal-UX + HITL
    touchpoints — not screens. The manifest keeps DM-NNN but rows point at tools/turns; Reconcile targets the
    design-intent voice + the agent-contract HITL rows. WCAG applies only where a GUI exists (not asserted here)."""
    ddir = os.path.join(root, "docs/design")
    design_files = [os.path.join(dp, f) for dp, _dn, fn in os.walk(ddir) for f in fn if f.endswith(".md")] \
        if os.path.isdir(ddir) else []
    design_blob = "\n".join(read(f) or "" for f in design_files)
    check("A docs/design/ agent-experience artifact was written",
          bool(design_blob.strip()), f"{len(design_files)} design file(s)")

    man = manifest_text(root)
    dm_ids = sorted(set(re.findall(r"DM-\d+", man)))
    check("DM-ID manifest present (kept under agent profiles; rows point at tools/turns, not screens)",
          bool(dm_ids), f"DM-IDs={dm_ids[:8]}{'…' if len(dm_ids) > 8 else ''}")

    # CORE discriminator — the design covers the TOOL SURFACE, tracing to the agent-contract's tools.
    tools = agent_contract_tools(root)
    blob_l = (design_blob + "\n" + man).lower()

    def _stem(t):
        return re.split(r"[.\s_/]", t.strip("`").lower())[0]

    covered = sorted({t for t in tools if t.lower() in blob_l or (_stem(t) and _stem(t) in blob_l)})
    need = max(2, (len(tools) + 1) // 2)
    check("Tool surface covered: the design references the agent-contract's tools (>= half — tools are the interface)",
          len(tools) > 0 and len(covered) >= need,
          f"agent-contract tools={tools}; covered={covered} (need >= {need})")

    check("Persona / voice realized (the agent's conversational manner — its 'look & feel')",
          bool(re.search(r"(?i)persona|voice|tone|conversational|register", design_blob)),
          "voice/persona covered" if re.search(r"(?i)persona|voice|tone", design_blob) else "no persona/voice section")

    check("Error-and-refusal UX designed (how the agent declines / escalates, not a dead end)",
          bool(re.search(r"(?i)refus|decline|escalat|fallback|error(?:\s|-)", design_blob)),
          "refusal/error UX covered" if re.search(r"(?i)refus|decline|escalat", design_blob) else "no refusal UX")

    check("HITL touchpoint UX designed (the human-approval / hand-off moments)",
          bool(re.search(r"(?i)hitl|human[ -]in|human approv|approval|hand-?off|confirm", design_blob)),
          "HITL touchpoints covered" if re.search(r"(?i)hitl|approv|hand-?off", design_blob) else "no HITL UX")

    rows = amendments(root)
    check("amendment-log.json valid (Reconcile targets the design-intent voice + agent-contract HITL rows)",
          rows is not None, "valid" if rows is not None else "missing/invalid amendment-log.json")
    return design_blob, rows


# ---------- per-case assertions ----------

def tier2_rows(rows):
    return [r for r in (rows or []) if str(r.get("tier")) == "2"]

def row_blob(r):
    return json.dumps(r, ensure_ascii=False).lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outputs", required=True)
    ap.add_argument("--case", required=True,
                    choices=["clean-intent", "contrast-conflict", "derived-intent", "agent"])
    a = ap.parse_args()
    root = find_root(a.outputs)
    reqs = sprint_reqs(root)

    if a.case == "agent":
        grade_agent_experience(root, reqs)
        return emit(a)

    ds, rows = grade_structure(root, reqs)
    brand = declared_brand_hex(root)

    if a.case == "clean-intent":
        # The declared brand passes AA -> a clean, fully-stated intent should yield ~zero amendments.
        if brand:
            ratio = contrast(brand, "#ffffff")
            check("Validity: the declared brand color passes WCAG AA as text on white (a clean intent)",
                  ratio >= 4.5, f"{brand} on #ffffff = {ratio:.2f}:1 (AA text floor 4.5:1)")
        # False-positive check: no invented amendments on a clean spine (<=1 tolerated).
        n = len(rows or [])
        check("False-positive check: a clean, AA-passing intent yields no invented amendments (<=1)",
              rows is not None and n <= 1, f"{n} amendment row(s) emitted")

    elif a.case == "contrast-conflict":
        # 1) Validity — the planted contradiction is real (grader recomputes the WCAG ratio).
        ratio = contrast(brand, "#ffffff") if brand else None
        check("Validity: the declared brand color FAILS WCAG AA as text on white (the planted contradiction is real)",
              brand is not None and ratio is not None and ratio < 4.5,
              f"{brand} on #ffffff = {ratio:.2f}:1 < 4.5:1" if ratio else "no brand hex found in design-intent")
        # 2) Discriminating core — a Tier-2 row catches the brand-vs-a11y contradiction, gated (not auto-applied).
        t2 = tier2_rows(rows)
        cites = [r for r in t2 if (brand and brand.lower() in row_blob(r))
                 or re.search(r"contrast|wcag|\baa\b|a11y|accessib|brand", row_blob(r))]
        gated = [r for r in cites if r.get("disposition") in ("gated", "approved", "pending")]
        not_auto = [r for r in cites if r.get("disposition") == "auto-applied"]
        # The discriminator AND the proof it wasn't silently swallowed: a strong baseline may *reason out* the same
        # contrast fix, but buries it as prose in the design doc — invisible to /status, the release gate, and the
        # next skills. The structured, gated row (not auto-applied) is the lift: the contradiction is surfaced
        # through the amendment channel, not silently resolved.
        check("Reconcile caught it: a Tier-2 amendment row cites the brand-vs-a11y contrast contradiction, gated "
              "(not auto-applied) — surfaced through the amendment channel, not silently resolved in prose",
              bool(gated) and not not_auto,
              f"tier-2 rows={len(t2)}; citing-contradiction={len(cites)}; "
              f"dispositions={[r.get('disposition') for r in cites] or 'none'}")

    elif a.case == "derived-intent":
        # 1) Flesh-out — a Tier-2 row resolves the derived / [NEEDS CLARIFICATION] brand intent.
        t2 = tier2_rows(rows)
        flesh = [r for r in t2 if re.search(r"needs clarification|brand|adjective|feel|design-intent|derived|"
                                            r"tone|calm|fast|unobtrusive", row_blob(r))]
        check("Flesh-out: a Tier-2 amendment row resolves the derived/[NEEDS CLARIFICATION] brand intent",
              bool(flesh),
              f"tier-2 rows={len(t2)}; resolving-brand-intent={len(flesh)}; "
              f"dispositions={[r.get('disposition') for r in flesh] or 'none'}")
        # 2) Concrete tokens — the realization produced a concrete brand color the thin intent lacked.
        brand_concrete = bool(re.search(r"(?:primary|brand)[^\n]{0,80}#[0-9a-fA-F]{3,6}", ds, re.I)) or \
                         bool(re.search(r"#[0-9a-fA-F]{3,6}[^\n]{0,80}(?:primary|brand)", ds, re.I))
        check("Concrete tokens: design-system gives the brand a concrete color the thin design-intent lacked",
              brand_concrete and bool(HEX.search(ds)),
              f"concrete brand hex present={brand_concrete}; total hexes in design-system={len(HEX.findall(ds))}")

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
