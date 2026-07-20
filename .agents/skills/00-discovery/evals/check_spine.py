#!/usr/bin/env python3
"""Deterministic grader for 00-discovery evals. Checks objective assertions against a produced spine.
Usage: python check_spine.py --outputs <dir> --case <rich-spec|thin-spec|undefended-bet|no-doc> [--fixture <input doc>]
Writes grading.json ({"expectations":[{text,passed,evidence}]}) into --outputs and prints a report.
"""
import os, re, json, argparse, subprocess, sys

results = []
def check(text, passed, evidence=""):
    results.append({"text": text, "passed": bool(passed), "evidence": str(evidence)[:300]})

def run_verify_script(vs, root):
    """Execute the emitted standing gate against the produced spine; (exit_code|None, evidence)."""
    try:
        p = subprocess.run([sys.executable, vs, "--root", root, "--json"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        return p.returncode, (p.stdout or p.stderr or "").strip()
    except Exception as e:
        return None, f"could not execute: {e}"

def read(p):
    try:
        with open(p, encoding="utf-8") as f: return f.read()
    except Exception: return None

# --- WS2 Task 2.1: EARS statement-line shape + must-not form + numbers-need-sources ---
# The five EARS patterns (design §D). A REQ's statement line — the one-line capability just under the
# heading — must match one. Keyword case is significant (SHALL/WHEN/WHILE/WHERE/IF/THEN uppercase).
# The leading clause is separated from `[the ]<system> SHALL` by a delimiter — canonically a comma, or a
# dash aside (em/en/double-hyphen) that closes right before the main clause (a legitimate EARS prose form
# surfaced by a live A/B output). The structural property is a *delimited* clause; the exact char is not.
# The article before <system> is optional in the four delimited patterns: a system named by a proper noun
# ("TeamPulse SHALL ...") is as valid EARS as "the system SHALL ..." — only the ubiquitous pattern (which
# has no delimiter to anchor on) keeps `The .+ SHALL .+` as-is, so it doesn't also admit user-centric
# anti-patterns like "Users SHALL be able to log in".
_D = r"(?:,|—|–|--)"       # comma · em-dash · en-dash · double-hyphen
EARS_PATTERNS = [
    r"^The .+ SHALL .+",                                     # Ubiquitous — invariants
    r"^WHEN .+%s\s*(?:the )?.+ SHALL .+" % _D,               # Event-driven — the common case
    r"^WHILE .+%s\s*(?:the )?.+ SHALL .+" % _D,              # State-driven
    r"^WHERE .+%s\s*(?:the )?.+ SHALL .+" % _D,              # Optional-feature — MAY-priority
    r"^IF .+%s\s*THEN (?:the )?.+ SHALL .+" % _D,            # Unwanted-behavior — must-not / abuse REQs
]
_MUST_NOT_RE = r"^IF .+%s\s*THEN (?:the )?.+ SHALL .+" % _D
def is_ears(stmt):
    return any(re.match(p, stmt or "") for p in EARS_PATTERNS)
def is_must_not(stmt):
    return bool(re.match(_MUST_NOT_RE, stmt or ""))
# A "quantitative claim" for the numbers-need-sources rule: a digit with a unit / currency / percentage
# (spelled-out numbers like "three prompts" are fine — only measured claims need a source).
QUANT_RE = re.compile(
    r"(\$\s?\d[\d,]*(?:\.\d+)?)"
    r"|(\b\d[\d,]*(?:\.\d+)?\s?%)"
    r"|(\b\d[\d,]*(?:\.\d+)?\s?(?:ms|sec|secs|seconds?|mins?|minutes?|hrs?|hours?|days?|weeks?|months?|years?"
    r"|/mo|/month|/yr|/year|users?|requests?|rps|qps|k|K|M|MB|GB|TB)\b)", re.I)

def find_root(base):
    """Return the dir containing docs/spec/specification.md under base, else None."""
    for dp, dn, fn in os.walk(base):
        if dp.replace("\\", "/").endswith("docs/spec") and "specification.md" in fn:
            return os.path.dirname(os.path.dirname(dp))
    return None

def parse_registry(spec):
    # rows like: | REQ-001 | name | MUST | stated | capabilities/x.md |
    return re.findall(r"\|\s*(REQ-\d+)\s*\|([^|\n]*)\|([^|\n]*)\|([^|\n]*)\|([^|\n]*)\|", spec)

def _extract_statement(blk):
    """The REQ 'statement' — the EARS sentence just under the "### REQ-NNN:" heading — as ONE logical
    line. A naive first-non-blank-physical-line grab is defeated by two real-world shapes: (1) this
    repo wraps prose at ~110 chars, so a valid EARS sentence routinely spans 2+ physical lines, and the
    delimiter/SHALL keyword the EARS patterns anchor on can land on the second line; (2) a block may
    carry an HTML comment (single- or multi-line, e.g. a `<!-- Priority: ... -->` aside) BEFORE the
    real statement. So: skip blank lines and HTML comments while looking for where the statement
    starts, then accumulate consecutive non-blank, non-comment lines — collapsing the wrap into single
    spaces — until a blank line or the next structural element (`**Acceptance`, a ``` fence, an HTML
    comment such as the `<!-- source: ... -->` / `<!-- /REQ-NNN -->` tail, or the next `###` heading).
    """
    lines = blk.splitlines()[1:]  # drop the "### REQ-NNN: ... (MUST)" heading line itself
    stmt, in_comment = [], False
    for raw in lines:
        s = raw.strip()
        if in_comment:
            if "-->" in s:
                in_comment = False
            continue
        if not s:
            if stmt:
                break               # a blank line ends an already-started statement
            continue                # still looking for where the statement starts
        if s.startswith("<!--"):
            if "-->" not in s:
                in_comment = True   # opens here; closes on a later line
            continue
        if s.startswith("**Acceptance") or s.startswith("```") or s.startswith("###"):
            break
        stmt.append(s)
    return " ".join(stmt).strip()

def parse_blocks(cap_files):
    blocks = {}  # rid -> {file, source, statement, block}
    for cf in cap_files:
        c = read(cf) or ""
        for m in re.finditer(r"###\s*(REQ-\d+):.*?<!--\s*/\1\s*-->", c, re.DOTALL):
            blk, rid = m.group(0), m.group(1)
            sm = re.search(r"<!--\s*source:\s*(.*?)\s*-->", blk, re.DOTALL)
            stmt = _extract_statement(blk)
            blocks[rid] = {"file": os.path.basename(cf), "source": (sm.group(1).strip() if sm else None),
                           "statement": stmt, "block": blk}
    return blocks

def _section_body(text, heading_rx):
    """Body of the first heading matching heading_rx, up to the next heading of any level (or EOF)."""
    m = re.search(r"(?im)^#{1,6}\s.*(?:%s).*$" % heading_rx, text or "")
    if not m:
        return None
    rest = (text or "")[m.end():]
    nxt = re.search(r"(?im)^#{1,6}\s", rest)
    return rest[:nxt.start()] if nxt else rest


def check_explore(a):
    """WS2 Task 2.3 — EXPLORE mode grades INVERTED: the correct state is NO spine + a divergence artifact.
    Hard invariant: nothing under docs/spec/**. Artifact: docs/discovery/exploration.md with >=3 framings
    (each origin-tagged) + Appetite + Decision."""
    spec_files = [os.path.join(dp, f).replace("\\", "/")
                  for dp, _dn, fn in os.walk(a.outputs) for f in fn
                  if "/docs/spec/" in (os.path.join(dp, f).replace("\\", "/") + "/")]
    check("Hard invariant: EXPLORE writes nothing under docs/spec/**", not spec_files,
          ("wrote %d spec file(s): %s" % (len(spec_files), "; ".join(spec_files[:3]))) if spec_files else "no docs/spec/** — correct")

    exp = next((os.path.join(dp, "exploration.md") for dp, _dn, fn in os.walk(a.outputs) if "exploration.md" in fn), None)
    text = read(exp) or "" if exp else ""
    check("docs/discovery/exploration.md produced", bool(exp), exp or "no exploration.md under outputs")

    fr = re.search(r"(?im)^##\s+Framings", text)
    body = text[fr.end():] if fr else ""
    body = re.split(r"(?im)^##\s+", body)[0] if fr else ""       # the Framings section only
    framings = re.findall(r"(?im)^###\s+\S", body)
    check(">=3 problem framings in exploration.md (divergent round ran)", len(framings) >= 3,
          "%d framings under ## Framings" % len(framings))
    origins = len(re.findall(r"(?im)origin:\s*(?:user|model)", body))
    check("each framing carries an origin: user|model tag", origins >= 3 and origins >= len(framings),
          "%d origin tags for %d framings" % (origins, len(framings)))
    check("## Appetite recorded (a size, not an estimate)", bool(re.search(r"(?im)^##\s+Appetite", text)),
          "Appetite section present" if re.search(r"(?im)^##\s+Appetite", text) else "no ## Appetite")
    check("## Decision recorded (a pick / ranking / don't-build)", bool(re.search(r"(?im)^##\s+Decision", text)),
          "Decision section present" if re.search(r"(?im)^##\s+Decision", text) else "no ## Decision")
    return emit(a)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outputs", required=True)
    ap.add_argument("--case", required=True)
    ap.add_argument("--fixture", default=None)
    a = ap.parse_args()

    if a.case in ("explore", "explore-refusal"):
        return check_explore(a)

    root = find_root(a.outputs)
    if not root:
        check("Spine produced (docs/spec/specification.md exists)", False,
              f"no docs/spec/specification.md anywhere under {a.outputs}")
        return emit(a)
    check("Spine produced (docs/spec/specification.md exists)", True, f"root={root}")

    spec = read(os.path.join(root, "docs/spec/specification.md")) or ""
    cm = re.search(r"^#+\s*Constitution", spec, re.M | re.I)
    if cm:
        sec = re.split(r"\n---", spec[cm.end():], maxsplit=1)[0]  # Constitution section, to next hr
        const_items = re.findall(r"^\s*\d+\.\s+\S", sec, re.M)
    else:
        const_items = []
    check("specification.md has a Constitution with >=3 items", len(const_items) >= 3,
          f"{len(const_items)} numbered Constitution items")

    rows = parse_registry(spec)
    check("REQ registry table present with REQ rows", len(rows) > 0, f"{len(rows)} registry rows")

    cap_dir = os.path.join(root, "docs/spec/capabilities")
    cap_files = [os.path.join(cap_dir, f) for f in os.listdir(cap_dir)
                 if f.endswith(".md") and "_EXAMPLE" not in f] if os.path.isdir(cap_dir) else []
    blocks = parse_blocks(cap_files)
    min_caps = 2 if a.case == "rich-spec" else 1
    check(f">= {min_caps} capabilities file(s) with delimited REQ blocks",
          len(cap_files) >= min_caps and len(blocks) > 0, f"{len(cap_files)} cap files, {len(blocks)} REQ blocks")

    missing = [r[0].strip() for r in rows if r[0].strip() not in blocks]
    check("Registry-leaf integrity: every registry REQ resolves to a block",
          len(rows) > 0 and not missing, ("; ".join(missing[:6]) if missing else "all resolve"))

    # WS2 Task 2.1 — EARS statement-line shape: every REQ's one-line statement matches an EARS pattern.
    non_ears = ["%s:'%s'" % (rid, (b["statement"] or "")[:44]) for rid, b in blocks.items() if not is_ears(b["statement"])]
    check("EARS statement lines: every REQ statement matches one of the five EARS patterns",
          bool(blocks) and not non_ears,
          ("; ".join(non_ears[:5]) if non_ears else "all %d REQ statement lines are EARS-form" % len(blocks)))

    # WS2 Task 2.1 — numbers-need-sources: an *inferred* REQ may not transcribe a quantitative claim
    # (currency / percentage / measured unit) unless it carries a [NEEDS CLARIFICATION] marker. Stated,
    # interview-, clarification-, code-, and adopt-confirmed-sourced REQs trace the number to a real source.
    num_violations = []
    for rid, b in blocks.items():
        if "inferred" not in (b["source"] or "").lower():
            continue
        if "[NEEDS CLARIFICATION" in b["block"]:
            continue
        body = re.sub(r"<!--.*?-->", "", b["block"], flags=re.DOTALL)
        hit = QUANT_RE.search(body)
        if hit:
            num_violations.append("%s:%r" % (rid, hit.group(0).strip()))
    check("Numbers need sources: no inferred REQ states a quantitative claim without a source or marker",
          not num_violations, ("; ".join(num_violations[:5]) if num_violations else "no sourceless quantitative claims"))

    if a.case == "security-flavored":
        must_not = [rid for rid, b in blocks.items() if is_must_not(b["statement"])]
        check(">=1 must-not (Unwanted-behavior IF/THEN) REQ from the security-flavored fixture",
              len(must_not) >= 1, (", ".join(must_not) if must_not else "no IF..THEN must-not REQ found"))

    # Standing gate (WS1 B): the verify script is ALWAYS emitted at WRITE SPINE, and it passes on the fresh spine.
    vs = os.path.join(root, "scripts", "verify-spine.py")
    check("scripts/verify-spine.py emitted at the project root", os.path.isfile(vs),
          vs if os.path.isfile(vs) else "absent")
    if os.path.isfile(vs):
        code, out = run_verify_script(vs, root)
        check("emitted verify-spine.py exits 0 on the fresh spine", code == 0, f"exit={code}: {out[:240]}")
    else:
        check("emitted verify-spine.py exits 0 on the fresh spine", False, "script absent")

    # WS5 5.4a: SECURITY.md (contact + CVD expectations) is emitted at WRITE SPINE too — the CVD floor 06 G7 checks.
    sec_md = os.path.join(root, "SECURITY.md")
    check("SECURITY.md emitted at the project root (security contact + CVD expectations)", os.path.isfile(sec_md),
          sec_md if os.path.isfile(sec_md) else "absent")

    stated = [r for r in rows if "stated" in r[3].lower()]
    derived = [r for r in rows if "derived" in r[3].lower()]

    if a.case == "rich-spec":
        pct = (len(stated) / len(rows) * 100) if rows else 0
        check(">=80% of REQs are 'stated'", pct >= 80, f"{len(stated)}/{len(rows)} stated ({pct:.0f}%)")
        if a.fixture:
            prd_n = re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", (read(a.fixture) or "").lower()))
            bad = []
            for rid, b in blocks.items():
                s = b["source"] or ""
                if "inferred" in s.lower():
                    continue
                # the actual doc phrase is the innermost single-quoted span; fall back to double-quoted
                inner = re.search(r"'([^']{8,})'", s)
                if inner:
                    quote = inner.group(1)
                else:
                    dq = re.search(r'"([^"]+)"', s)
                    quote = dq.group(1) if dq else s
                probe = re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", quote.lower())).strip()[:35]
                if probe and probe not in prd_n:
                    bad.append(f"{rid}:'{probe}'")
            check("No invented scope: stated source quotes trace to PRD.md", not bad,
                  ("; ".join(bad[:5]) if bad else "all stated quotes trace to PRD"))
        ag = read(os.path.join(root, "AGENTS.md")) or ""
        check("AGENTS.md emitted (GENERATED header + Constitution)",
              "generated" in ag.lower() and "constitution" in ag.lower(), f"AGENTS.md len={len(ag)}")
        # The instructions-file bridges (WRITE SPINE emissions 8/9): Claude Code reads CLAUDE.md, not AGENTS.md —
        # line 1 must be the live `@AGENTS.md` import; Gemini CLI reads GEMINI.md — the `@./AGENTS.md` one-liner.
        # Codex needs no bridge (native AGENTS.md). Both are create-if-absent; fresh workspaces have neither.
        cm_lines = [ln.strip() for ln in (read(os.path.join(root, "CLAUDE.md")) or "").splitlines() if ln.strip()]
        gm = read(os.path.join(root, "GEMINI.md")) or ""
        check("CLAUDE.md bridge emitted: line 1 is the live `@AGENTS.md` import (the Claude Code bridge)",
              bool(cm_lines) and cm_lines[0] == "@AGENTS.md",
              f"first non-blank line={(cm_lines[0] if cm_lines else '(absent)')[:40]!r}")
        check("GEMINI.md bridge emitted: carries `@./AGENTS.md` (the Gemini CLI bridge)",
              "@./AGENTS.md" in gm, "present" if "@./AGENTS.md" in gm else "GEMINI.md absent or no import line")
        ch = read(os.path.join(root, "docs/discovery/charter.md")) or ""
        check("charter.md exists with a JTBD (When...I want...so)",
              bool(re.search(r"when.*i want.*so", ch, re.I | re.S)), f"charter len={len(ch)}")
        al = read(os.path.join(root, "docs/spec/amendment-log.json"))
        try: ok = isinstance(json.loads(al).get("amendments"), list)
        except Exception: ok = False
        check("amendment-log.json valid JSON with 'amendments' array", ok, "")
        am = read(os.path.join(root, "docs/discovery/assumption-map.md")) or ""
        ms = re.search(r"^##\s+Surfaced", am, re.M)
        if ms:
            sec = re.split(r"^##\s", am[ms.end():], flags=re.M)[0]
            n_surf = len(re.findall(r"^###\s", sec, re.M))
        else:
            n_surf = len(re.findall(r"^###\s", am, re.M))
        check("CHALLENGE near-silent (<=2 surfaced Unknown+Important bets)",
              n_surf <= 2, f"{n_surf} surfaced bet(s)")

    if a.case == "thin-spec":
        inferred_blocks = [r for r, b in blocks.items() if (b["source"] or "").lower().find("inferred") >= 0]
        check(">=1 derived REQ (source: inferred)", len(derived) >= 1 or len(inferred_blocks) >= 1,
              f"{len(derived)} derived rows, {len(inferred_blocks)} inferred blocks")
        allspine = spec + "".join(read(cf) or "" for cf in cap_files)
        check("[NEEDS CLARIFICATION] marker present", "NEEDS CLARIFICATION" in allspine, "")

    if a.case == "undefended-bet":
        am = read(os.path.join(root, "docs/discovery/assumption-map.md")) or ""
        kw = [k for k in ["pay", "$15", "15/month", "free", "switch"] if k in am.lower()]
        check("assumption-map surfaces the willingness-to-pay bet", bool(kw),
              f"keywords={kw}, assumption-map len={len(am)}")
        # WS2 Task 2.2 — CHALLENGE enrichments recorded as sections (heading or bold label at line start).
        def _has_label(text, rx):
            return bool(re.search(r"(?im)^[\s>#*\-]*\*{0,2}\s*(?:%s)" % rx, text))
        dissent = _has_label(am, r"devil'?s?\s*advocate|dissent\b|strongest case against")
        check("CHALLENGE records a devil's-advocate dissent against the leading position",
              dissent, "found in assumption-map" if dissent else "no devil's-advocate/dissent section in assumption-map.md")
        premortem = _has_label(am, r"pre-?mortem")
        check("CHALLENGE records a pre-mortem (assume it shipped and failed) pass",
              premortem, "found in assumption-map" if premortem else "no pre-mortem section in assumption-map.md")

    if a.case == "no-doc":
        bad = [r for r, b in blocks.items()
               if b["source"] and "inferred" not in b["source"].lower() and "interview" not in b["source"].lower()]
        check("No doc source quotes (interview/inferred only)", not bad, ("; ".join(bad[:5]) if bad else "ok"))
        ch = read(os.path.join(root, "docs/discovery/charter.md")) or ""
        check("charter.md has a JTBD", bool(re.search(r"when.*i want.*so", ch, re.I | re.S)), f"charter len={len(ch)}")

    if a.case == "adopt":
        # WS2 Task 2.4 — ADOPT: the existing repo IS the project; the spine is sourced from code evidence.
        non_adopt = [rid for rid, b in blocks.items()
                     if not re.search(r"(?:adopt-confirmed:\s*)?(?:code:|docs:)", b["source"] or "")]
        check("Every REQ is adopt-sourced (code:<path> or docs:<path>)", not non_adopt,
              ("; ".join(non_adopt[:5]) if non_adopt else "all REQs cite code:/docs: evidence"))
        # anti-hallucination: every code:<path> resolves relative to the project root (grader opens it)
        bad = []
        for rid, b in blocks.items():
            # stop at whitespace OR a wrapping quote/angle-bracket: the design's confirm-sweep form is
            # `source: "adopt-confirmed: code:<path>"`, so the value can be quote-wrapped. A citation can
            # also be one of several comma-separated `code:` refs (e.g. "code:a.py:1-2, code:b.py:3"), so
            # the capture may carry a trailing list-separator; strip that before dropping a :line or
            # :start-end range suffix.
            m = re.search(r"code:\s*([^\s\"'>]+)", b["source"] or "")
            if m:
                p = m.group(1).rstrip(",;.)")
                p = re.sub(r":\d+(?:-\d+)?$", "", p)
                if not os.path.isfile(os.path.join(root, p)):
                    bad.append("%s->%s" % (rid, p))
        check("Anti-hallucination: every adopt code:<path> resolves on disk", not bad,
              ("; ".join(bad[:5]) if bad else "every code: path resolves"))
        # the planted zombie feature (PDF export) is surfaced out-of-scope, never a silent keep or silent delete
        surfaced = (read(os.path.join(root, "docs/discovery/assumption-map.md")) or "") + "\n" + \
                   (read(os.path.join(root, "docs/discovery/charter.md")) or "")
        z_named = bool(re.search(r"(?i)export|pdf", surfaced))
        z_scoped = bool(re.search(r"(?i)out.of.scope|removal|zombie|dead|not adopt|excluded", surfaced))
        z_as_req = [rid for rid, b in blocks.items() if re.search(r"(?i)\b(?:export|pdf)\b", b["statement"] or "")]
        check("Zombie feature surfaced out-of-scope, not silently kept as a REQ",
              z_named and z_scoped and not z_as_req,
              "named=%s scoped=%s as_active_req=%s" % (z_named, z_scoped, z_as_req or "none"))
        # the auth/session invariant is captured — as a must-not REQ or a Constitution item
        mustnot_auth = [rid for rid, b in blocks.items()
                        if is_must_not(b["statement"]) and re.search(r"(?i)lock|session|unauth|passphrase", b["statement"])]
        const_auth = bool(re.search(r"(?i)unlocked session|requires? an? [^.]*session|while locked|passphrase", spec))
        check("Auth invariant captured (a must-not REQ or a Constitution item)",
              bool(mustnot_auth) or const_auth, "must-not=%s constitution=%s" % (mustnot_auth or "none", const_auth))

    if a.case == "agent":
        # WS3 Task 3.2 — the agentic branch: Profile: agent-system + a complete agent-contract.md.
        prof = re.search(r"(?im)^\s*-\s*\*\*Profile:\*\*\s*agent-system\b", spec)
        check("Profile is agent-system in specification.md", bool(prof),
              "declared agent-system" if prof else "no `- **Profile:** agent-system` line")
        ac = read(os.path.join(root, "docs/spec/agent-contract.md")) or ""
        check("agent-contract.md emitted at docs/spec/agent-contract.md", bool(ac.strip()),
              "len=%d" % len(ac) if ac.strip() else "absent")
        # the six CORE sections (agentic-profile.md: all six are core under agent-system)
        SECTIONS = [("autonomy tier", r"autonomy\s*tier"), ("risk class", r"risk\s*class"),
                    ("tool-permission matrix", r"tool[-\s]*permission\s*matrix|tool\s*matrix"),
                    ("escalation/HITL", r"escalation|hitl\s*policy"), ("cost envelope", r"cost\s*envelope"),
                    ("memory policy", r"memory\s*policy")]
        # a section head = a markdown heading OR a bold/numbered label at line start (robust to arm formatting)
        def _has_head(rx):
            return bool(re.search(r"(?im)^[\s>#*\-]*\*{0,2}\s*(?:\d+\s*[·.)\-]\s*)?(?:%s)" % rx, ac))
        missing_sec = [name for name, rx in SECTIONS if not _has_head(rx)]
        check("agent-contract has all six core section heads",
              bool(ac.strip()) and not missing_sec,
              ("missing: " + ", ".join(missing_sec)) if missing_sec else "autonomy·risk·tools·HITL·cost·memory all present")
        # tool-permission matrix: a header carrying a HITL column, + >=1 concrete (non-placeholder) tool row.
        # The degenerate (HITL column dropped) fails at header detection — this is the discriminating check.
        hdr_i, aclines = None, ac.splitlines()
        for i, ln in enumerate(aclines):
            low = ln.strip().lower()
            if low.startswith("|") and "tool" in low and "hitl" in low and "risk" in low and "scope" in low:
                hdr_i = i
                break
        rows = []
        if hdr_i is not None:
            for dl in aclines[hdr_i + 1:]:
                s = dl.strip()
                if not s.startswith("|"):
                    break
                if re.match(r"^\|[\s:\-|]+\|?\s*$", s):    # separator row
                    continue
                if re.search(r"_<.*?>_", s):               # unfilled template placeholder row
                    continue
                rows.append(s)
        check("Tool-permission matrix carries a HITL column + >=1 concrete tool row",
              hdr_i is not None and len(rows) >= 1,
              ("HITL header + %d tool row(s)" % len(rows)) if hdr_i is not None else "no `| Tool | Scopes | Risk | HITL |` header")
        # cost envelope substance: a token/spend budget AND a retry/step cap (the runaway-loop defense)
        cost = _section_body(ac, r"cost\s*envelope") or ""
        cost = re.sub(r"_<.*?>_", "", cost)               # ignore unfilled placeholders
        cost_budget = bool(re.search(r"(?i)token|spend|budget|\$|cost", cost))
        cost_cap = bool(re.search(r"(?i)retry|step|cap|loop|give up|hard stop|\bmax\b", cost))
        check("Cost envelope declares a budget + a retry/step cap (runaway-loop defense)",
              cost_budget and cost_cap, "budget=%s cap=%s" % (cost_budget, cost_cap))
        # >=1 must-not (IF/THEN Unwanted-behavior) REQ — the abuse/refusal guardrail
        must_not = [rid for rid, b in blocks.items() if is_must_not(b["statement"])]
        check(">=1 must-not (IF/THEN Unwanted-behavior) REQ for a high-risk tool",
              len(must_not) >= 1, (", ".join(must_not) if must_not else "no IF..THEN must-not REQ"))

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
