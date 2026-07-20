#!/usr/bin/env python3
"""Deterministic grader for `status` evals. Grades the derived state a strong baseline does NOT reliably produce — no
refactor beauty, no LLM judge, no node (status runs no code). Three deterministic pillars:

  (1) READ-ONLY W.R.T. TRUTH (the honesty gate). After /status, `git diff` shows docs/spec/** + every realization
      BYTE-IDENTICAL to the pre-status root commit; ONLY CLAUDE.md + AGENTS.md may change. This is the inverse of 08
      (src changed) and the same shape as 07 (src byte-identical) — a pure git assertion. On `corrupted` it doubles as
      the report-don't-repair check: status must NOT "fix" the missing delimiter (that would change docs/spec).
  (2) THE MACHINE-READABLE DERIVED STATE. status emits the graded fields into CLAUDE.md § Current State — the
      integrity verdict (PASS, or FAIL naming the offending REQ-ID), the pending/deferred amendment + surviving-marker
      counts, and the single routed next command. A baseline summarizes in prose; it does not emit the structured,
      gate-readable contract. That gap is the lift.
  (3) THE FAITHFUL GENERATED VIEW. status re-emits AGENTS.md as a faithful projection of the spine Constitution (the
      generated-view integrity check) — verified on the PASS cases.

Four cases — a two-axis F1 (integrity × routing) + the governance arm:
  healthy     — integral spine, 0 blockers, sprint-02 qa SHIP → next `/06-release sprint 2`.
  corrupted   — REQ-021's closing delimiter removed (L2) → integrity FAIL naming REQ-021; NOT a ship route; and the
                read-only proxy proves status REPORTED, didn't repair.
  blocked     — a deferred amendment + a surviving marker (else ship-ready) → counts reported + route to RESOLVE
                (/00-discovery reflect), NOT /06-release.
  backlog-gap — spine only → integrity PASS, next `/01-planner`.

Input = a seeded PRE-STATUS project state (build_fixture.py): a git repo whose ROOT commit carries the mid-chain
chain. The arm runs `/status`, deriving state and writing ONLY the two generated views.

Usage:
    python check_status.py --outputs <dir> --case <healthy|corrupted|blocked|backlog-gap>
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
    for dp, dn, fn in os.walk(base):
        if dp.replace("\\", "/").endswith("docs/spec") and "specification.md" in fn:
            return os.path.dirname(os.path.dirname(dp))
    return base

def git(root, *args):
    """(returncode, stdout, stderr) SEPARATELY — porcelain/name-only parsing reads stdout only, so a benign stderr
    warning (e.g. 'LF will be replaced by CRLF') can't pollute a path list (the 08 grader lesson)."""
    try:
        p = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=60)
        return p.returncode, (p.stdout or ""), (p.stderr or "")
    except Exception as e:
        return 1, "", str(e)

def root_commit(root):
    rc, out, _ = git(root, "rev-list", "--max-parents=0", "HEAD")
    return out.strip().splitlines()[0] if rc == 0 and out.strip() else None


# The realization + spine paths that MUST stay byte-identical (status writes ONLY CLAUDE.md + AGENTS.md).
TRUTH_PATHS = ["docs/spec", "docs/planning", "docs/design", "docs/architecture", "src",
               "docs/quality", "docs/release", "docs/security", "docs/refactoring",
               "docs/discovery", "docs/README.md"]

def _under_truth(path):
    p = path.replace("\\", "/")
    return any(p == t or p.startswith(t + "/") for t in TRUTH_PATHS)

def truth_changed(root):
    """Union of (diff vs ROOT) and (porcelain untracked/modified), filtered to TRUTH_PATHS. Empty == read-only held."""
    changed = set()
    rc0 = root_commit(root)
    if rc0:
        rc, out, _ = git(root, "diff", "--name-only", rc0)
        if rc == 0:
            for ln in out.splitlines():
                if ln.strip() and _under_truth(ln.strip()):
                    changed.add(ln.strip().replace("\\", "/"))
    rc, out, _ = git(root, "status", "--porcelain")
    if rc == 0:
        for ln in out.splitlines():
            # porcelain: 'XY <path>' (or ' -> ' for renames) — take the final token
            path = ln[3:].strip() if len(ln) > 3 else ""
            if " -> " in path:
                path = path.split(" -> ")[-1]
            path = path.strip().strip('"')
            if path and _under_truth(path):
                changed.add(path.replace("\\", "/"))
    return sorted(changed)


# ---------- the machine emission (CLAUDE.md § Current State) ----------

def claude_md(root):
    return read(os.path.join(root, "CLAUDE.md")) or ""

def current_state_section(root):
    """The text of the `## Current State` (or `## Current Project State`) section of CLAUDE.md (to EOF or the next H2)."""
    txt = claude_md(root)
    m = re.search(r"(?im)^#{1,3}\s+Current (?:Project )?State\b(.*?)(?=^\#{1,3}\s|\Z)", txt, re.S | re.M)
    return m.group(1) if m else ""

def field(root, label):
    """The remainder of the first `- **<label>:** …` (or `<label>:`) line, searched across the whole CLAUDE.md."""
    txt = claude_md(root)
    m = re.search(r"(?im)^\s*[-*]?\s*\*{0,2}" + re.escape(label) + r"\*{0,2}\s*:\s*(.+)$", txt)
    return m.group(1).strip() if m else ""

def integrity_verdict(root):
    """PASS / FAIL / None from the `Spine integrity:` field (or anywhere it is stated)."""
    v = field(root, "Spine integrity") or field(root, "Integrity")
    blob = v or claude_md(root)
    if re.search(r"\bFAIL\b", v, re.I) or (not v and re.search(r"(?i)integrity[^\n]{0,40}\bFAIL\b", claude_md(root))):
        return "FAIL"
    if re.search(r"\bPASS\b", v, re.I) or re.search(r"(?i)integrity[^\n]{0,40}\bPASS\b", claude_md(root)):
        return "PASS"
    return None

def next_command(root):
    """The routed command — from the `Next command:` field, else the report's `→` line, else a backticked /NN-… token."""
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
    """(pending, deferred) from the emitted 'N pending' / 'N deferred' form (number-then-word), tolerant of
    surrounding backticks/bold. Returns None where the arm did not emit that numeric form — we credit SUBSTANCE
    (a real count) over the exact label, but we do NOT invent a count the arm never wrote
    (feedback_grader_validate_on_real_outputs: credit substance, not delimiter)."""
    t = claude_md(root)
    p = re.search(r"(\d+)\s*[`*]*\s*pending", t, re.I)
    d = re.search(r"(\d+)\s*[`*]*\s*deferred", t, re.I)
    return (int(p.group(1)) if p else None, int(d.group(1)) if d else None)

def zero_blockers_stated(root):
    """The arm explicitly stated ZERO governance blockers — credits '0 open', 'governance blockers: 0', 'no
    pending/deferred', 'release is unblocked' (a strong reader states the zero in varied ways; we credit the
    substance, not the exact 'N pending · N deferred' template phrasing)."""
    t = claude_md(root).lower()
    return bool(
        re.search(r"governance[- ]block\w*\s*[:=]?\s*(?:is\s*)?[`*]*\s*0\b", t)
        or re.search(r"\b0\s*(?:open\s*)?governance[- ]block", t)
        or re.search(r"\b0\s*open\b", t)
        or re.search(r"\bno\s+(?:open\s+)?(?:pending|deferred|governance)", t)
        or "release is unblocked" in t or "otherwise unblocked" in t or "nothing that would block" in t
    )

def marker_count(root):
    """The surviving-marker count the arm emitted — tolerant of the template label ('Open [NEEDS CLARIFICATION]: N'),
    the synonym label ('markers: N' / 'Open clarification markers: N'), backticks/bold, and either order."""
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


# ---------- command matchers (lenient on the leading slash + sprint token) ----------

def has(cmd, tok):
    return tok in (cmd or "").lower()

def is_release_sprint2(cmd):
    c = (cmd or "").lower()
    return "06-release" in c and bool(re.search(r"sprint[-\s]*0?2\b", c))

def is_release_any(cmd):
    return "06-release" in (cmd or "").lower()

def is_planner(cmd):
    c = (cmd or "").lower()
    return "01-planner" in c

def is_discovery(cmd):
    return "00-discovery" in (cmd or "").lower()


# ---------- the faithful AGENTS.md emission (a generated-view integrity check) ----------

CONSTITUTION_PHRASES = ["async over synchronous", "daily digest is the one artifact", "timezone-fair",
                        "eu data residency", "passwordless by design", "least data, least access"]

def agents_faithful(root):
    ag = read(os.path.join(root, "AGENTS.md"))
    if ag is None:
        return False, 0, "no AGENTS.md written"
    low = ag.lower()
    hits = [p for p in CONSTITUTION_PHRASES if p in low]
    header = bool(re.search(r"generated|do not edit", ag, re.I))
    ok = header and len(hits) >= 5
    return ok, len(hits), f"header={header}; constitution phrases matched={len(hits)}/6"


# ---------- common assertions ----------

def grade_common(root, case):
    # (1) the read-only proxy — the honesty gate (all cases)
    tc = truth_changed(root)
    check("READ-ONLY w.r.t. truth: after /status, docs/spec/** + every realization is byte-identical to the "
          "pre-status commit — only CLAUDE.md + AGENTS.md may change (status derives, it never mutates truth)",
          tc == [], f"truth paths changed vs root = {tc or 'none (clean)'}")

    # (2) the machine emission exists with the graded fields
    cs = current_state_section(root)
    has_section = bool(cs.strip()) or bool(re.search(r"(?im)^#{1,3}\s+Current (?:Project )?State\b", claude_md(root)))
    check("CLAUDE.md § Current State written (the machine-readable derived state — a generated view, derived status "
          "only)",
          has_section, "found ## Current State" if has_section else "no ## Current State section in CLAUDE.md")

    nc = next_command(root)
    check("A single next command is emitted (the routed command the next seat runs)",
          bool(nc), f"next command = {nc or 'none found'}")

    iv = integrity_verdict(root)
    check("The spine-integrity verdict is emitted (PASS or FAIL)",
          iv in ("PASS", "FAIL"), f"integrity verdict = {iv}")

    # (3) faithful AGENTS.md — the PASS cases (on `corrupted` the skill leads with the repair; not required there;
    #     `agent` uses a non-TeamPulse spine, so it does its own faithful + profile-mirror check in grade_agent)
    if case not in ("corrupted", "agent"):
        ok, hits, ev = agents_faithful(root)
        check("AGENTS.md re-emitted as a FAITHFUL projection of the spine Constitution (the generated-view integrity "
              "check: the 'do not edit' header + the Constitution items)",
              ok, ev)
    return iv, nc


# ---------- per-case ----------

def grade_healthy(root, iv, nc):
    check("Integrity PASS: the mid-chain spine is integral (every registry File resolves + carries its delimited "
          "REQ block)",
          iv == "PASS", f"integrity = {iv}")
    check("Routed correctly: sprint-02 is built + qa SHIP with no release report → next command `/06-release sprint 2`",
          is_release_sprint2(nc), f"next command = {nc}")
    p, d = amendment_counts(root)
    check("Governance emitted as zero blockers: 0 pending · 0 deferred (or an explicit 'no blockers / unblocked' — "
          "credit the substance, not the exact template phrasing)",
          (p == 0 and d == 0) or zero_blockers_stated(root),
          f"pending={p}; deferred={d}; zero-blockers-stated={zero_blockers_stated(root)}")
    m = marker_count(root)
    check("Open [NEEDS CLARIFICATION] count emitted and zero",
          m == 0, f"markers={m}")


def grade_corrupted(root, iv, nc):
    check("Integrity FAIL: the deleted `<!-- /REQ-021 -->` delimiter is caught — the registry claims REQ-021 but its "
          "leaf no longer carries a delimited block (a baseline sees the heading and calls it present)",
          iv == "FAIL", f"integrity = {iv}")
    named = bool(re.search(r"REQ-0*21\b", claude_md(root)))
    check("The FAIL NAMES the offending REQ-ID (REQ-021) — an actionable break, not a bare 'FAIL'",
          named, "REQ-021 named in CLAUDE.md" if named else "offending REQ-021 not named")
    check("Did NOT sail past the corruption to a ship route: the next command is not `/06-release` (P1 halts routing "
          "and routes to repair — `/00-discovery`)",
          bool(nc) and not is_release_any(nc), f"next command = {nc}")
    # the read-only proxy (graded in common) is ALSO the report-don't-repair discriminator here — restate for clarity:
    api = read(os.path.join(root, "docs/spec/capabilities/api.md")) or ""
    still_broken = bool(re.search(r"(?m)^#{2,4}\s+REQ-021\b", api)) and ("<!-- /REQ-021 -->" not in api)
    check("Reported, did NOT repair: the missing REQ-021 delimiter is STILL missing — status flags the break, it "
          "never silently edits the spine to 'fix' it (that is /00-discovery's write-path)",
          still_broken, f"REQ-021 heading present & delimiter still absent = {still_broken}")


def grade_blocked(root, iv, nc):
    check("Integrity PASS: the spine is integral — the block is a GOVERNANCE block, not corruption",
          iv == "PASS", f"integrity = {iv}")
    p, d = amendment_counts(root)
    check("Governance surfaced: >=1 pending/deferred amendment counted (the deferred AMD-003) — the release blocker "
          "06 gates on, made visible early",
          (d or 0) + (p or 0) >= 1, f"pending={p}; deferred={d}")
    m = marker_count(root)
    check("Surviving [NEEDS CLARIFICATION] marker counted (>=1)",
          (m or 0) >= 1, f"markers={m}")
    check("Routed to RESOLVE, not ship: an otherwise ship-ready sprint with a governance blocker routes to "
          "`/00-discovery reflect` (P2 override), NOT `/06-release` — the block is enforced before the gate",
          is_discovery(nc) and not is_release_any(nc), f"next command = {nc}")


def grade_backlog_gap(root, iv, nc):
    check("Integrity PASS: the spine (present) is integral",
          iv == "PASS", f"integrity = {iv}")
    check("Routed correctly: a spine with no backlog -> next command `/01-planner` (the master-plan's called-out row)",
          is_planner(nc) and not is_release_any(nc), f"next command = {nc}")
    p, d = amendment_counts(root)
    check("Governance emitted as zero blockers (no pending/deferred amendment)",
          (p == 0 and d == 0) or zero_blockers_stated(root),
          f"pending={p}; deferred={d}; zero-blockers-stated={zero_blockers_stated(root)}")


def grade_patch_in_flight(root, iv, nc):
    check("Integrity PASS: the spine is integral (the patch is planning state, not corruption)",
          iv == "PASS", f"integrity = {iv}")
    check("Routed to the patch's next seat: an open `planned` Patches row routes to `/04-builder` (the funnel) — "
          "NOT `/06-release sprint 2` (a patch-unaware router false-routes to the sprint chain)",
          "04-builder" in (nc or "").lower() and not is_release_any(nc), f"next command = {nc}")
    named = "patch-001" in claude_md(root)
    check("The in-flight patch is surfaced by id in the derived state (patch-001 named in CLAUDE.md)",
          named, "patch-001 named" if named else "patch-001 not named in CLAUDE.md")
    p, d = amendment_counts(root)
    check("Governance emitted as zero blockers (the patch preempts routing, it is not a governance blocker)",
          (p == 0 and d == 0) or zero_blockers_stated(root),
          f"pending={p}; deferred={d}; zero-blockers-stated={zero_blockers_stated(root)}")


def grade_patch_pressure(root, iv, nc):
    check("Integrity PASS: the spine is integral",
          iv == "PASS", f"integrity = {iv}")
    check("Routing UNBLOCKED by the advisory: no patch is open, so the normal route holds — `/06-release sprint 2` "
          "(A6 is advisory, never a block)",
          is_release_sprint2(nc), f"next command = {nc}")
    txt = claude_md(root)
    low = txt.lower()
    advisory = ("patch" in low) and bool(re.search(r"(?i)(cadence|pressure|consecutive)", txt)) \
        and bool(re.search(r"(?i)(plan-sprint|08-refactor)", txt))
    check("The A6 patch-pressure advisory is surfaced: >=3 consecutive done patches named as sprint pressure "
          "('this cadence is a sprint' — plan-sprint / consider /08-refactor assess)",
          advisory, f"patch={'patch' in low}; cadence-token={bool(re.search(r'(?i)(cadence|pressure|consecutive)', txt))}; "
                    f"route-suggestion={bool(re.search(r'(?i)(plan-sprint|08-refactor)', txt))}")


# ---------- WS3 Task 3.10: profile-aware routing + the AGENTS.md profile mirror ----------

def spine_profile(root):
    spec = read(os.path.join(root, "docs", "spec", "specification.md")) or ""
    m = re.search(r"(?im)^\s*-\s*\*\*Profile:\*\*\s*([a-z][a-z-]*)", spec)
    return m.group(1) if m else "webapp"


def grade_agent(root, iv, nc):
    """WS3 Task 3.10 — the router reads the profile, and the AGENTS.md emission mirrors it (S7). Byte-identical +
    Current State + next command are checked by grade_common; here: the profile mirror + a faithful, generated AGENTS.md."""
    profile = spine_profile(root)
    ag = read(os.path.join(root, "AGENTS.md")) or ""
    header = bool(re.search(r"generated|do not edit", ag, re.I))
    mirror = re.search(r"(?im)^\s*-\s*\*\*Profile:\*\*\s*([a-z][a-z-]*)", ag)
    check("AGENTS.md re-emitted with the 'do not edit' header (a faithful generated view of the spine)",
          header, "header present" if header else "no generated/do-not-edit header")
    check("AGENTS.md mirrors the spine Profile (the S7 mirror — the downstream harness reads the project's shape)",
          bool(mirror) and mirror.group(1) == profile,
          f"spine profile={profile}; AGENTS.md profile={(mirror.group(1) if mirror else '—')}")
    # the router read the profile: an agent-system project resolves its design phase (a valid routed command, not a
    # false 'no design' skip that a profile-unaware router would emit for a webapp).
    check("A next command is routed (the profile-aware router resolved the phase chain)",
          bool(nc), f"next command = {nc or 'none'}")


# ---------- main ----------

# ---------- WS6: the L7 parity + coverage-line doc-integrity self-test ----------
# status's load-bearing set must never diverge from the emitted verify-spine.py. This self-test proves status's
# integrity reference names L7 (the parity contract) and the SKILL documents the conditional verify-live coverage
# line. Deterministic, reads the sibling references by path (the check_build 5.4b idiom).
_SKILL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
INTEGRITY_MD = os.path.join(_SKILL_DIR, "references", "integrity-and-governance.md")
STATUS_SKILL = os.path.join(_SKILL_DIR, "SKILL.md")

def _self_test():
    integ = read(INTEGRITY_MD) or ""
    skill = read(STATUS_SKILL) or ""
    l7_parity = bool(re.search(r"(?im)\bL7\b.*verify-live", integ)) and \
        bool(re.search(r"(?i)never diverge", integ))
    l7_skill = bool(re.search(r"(?im)\bL7\b.*verify-live", skill))
    coverage = bool(re.search(r"(?i)Verify-live.{0,60}(verified|stale|missing)", skill))
    degen = bool(re.search(r"(?im)\bL7\b.*verify-live", "L5 amendment-log valid; L6 dataset refs resolve.\n"))
    ok = l7_parity and l7_skill and coverage and not degen
    print("== check_status L7-parity + coverage self-test (WS6) ==")
    print("  [%s] integrity-and-governance.md names L7 in the load-bearing set + the never-diverge parity contract"
          % ("PASS" if l7_parity else "FAIL"))
    print("  [%s] status SKILL.md names L7 (verify-live) in the load-bearing paragraph" % ("PASS" if l7_skill else "FAIL"))
    print("  [%s] status SKILL.md documents the conditional verify-live coverage line (verified/stale/missing)"
          % ("PASS" if coverage else "FAIL"))
    print("  [%s] the check FIRES on a reference without L7 (non-vacuous)" % ("PASS" if not degen else "FAIL"))
    print("ALL GOOD" if ok else "SELF-TEST FAILED")
    return 0 if ok else 1


def main():
    if "--self-test" in sys.argv:   # WS6 L7-parity + coverage-line doc-integrity
        sys.exit(_self_test())
    ap = argparse.ArgumentParser()
    ap.add_argument("--outputs", required=True)
    ap.add_argument("--case", required=True,
                    choices=["healthy", "corrupted", "blocked", "backlog-gap", "patch-in-flight", "patch-pressure",
                             "agent"])
    a = ap.parse_args()
    root = find_root(os.path.abspath(a.outputs))
    iv, nc = grade_common(root, a.case)
    if a.case == "agent":
        grade_agent(root, iv, nc)
    elif a.case == "healthy":
        grade_healthy(root, iv, nc)
    elif a.case == "corrupted":
        grade_corrupted(root, iv, nc)
    elif a.case == "blocked":
        grade_blocked(root, iv, nc)
    elif a.case == "patch-in-flight":
        grade_patch_in_flight(root, iv, nc)
    elif a.case == "patch-pressure":
        grade_patch_pressure(root, iv, nc)
    else:
        grade_backlog_gap(root, iv, nc)

    passed = sum(1 for r in results if r["passed"])
    print("\n== check_status: %s — %d/%d ==" % (a.case, passed, len(results)))
    for r in results:
        print("  [%s] %s" % ("PASS" if r["passed"] else "FAIL", r["text"]))
        if not r["passed"]:
            print("         evidence: %s" % r["evidence"])
    with open(os.path.join(a.outputs, "grading.json"), "w", encoding="utf-8") as f:
        json.dump({"expectations": results}, f, indent=2)
    print("grading.json -> %s" % os.path.join(a.outputs, "grading.json"))


if __name__ == "__main__":
    main()
