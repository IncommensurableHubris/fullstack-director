#!/usr/bin/env python3
"""Deterministic grader for 05-reviewer evals. Grades the VERDICT + isolation + honesty + false-positive control — the
objective properties of a review that can gate a ship — never review prose, no LLM judge.

05's lift is NOT "reviews code" (a strong baseline does that too). It is the isolated, honest, FP-controlled verdict:
provably (a) not self-preferring (an auditable context attestation), (b) caught the planted defect (sensitivity),
(c) didn't cry wolf on a clean build (specificity → F1), (d) verified honestly (SHIP unreachable while any behavior is
INFERRED or a MUST REQ is uncovered). So we grade those, all structurally.

Input = a seeded BUILT slice (produced by build_fixture.py): a git repo (baseline=docs, final=+src/tests) + a
build-handoff. The arm (05) reviews it and writes docs/quality/qa-report-sprint-01.md (+ a reproducing RED test for a
testable defect). This grader reads that report + the repo.

Three cases, F1-framed (specificity AND sensitivity):
  clean-ship   — a sound slice → SHIP, ~0 findings (the crying-wolf / false-positive guard).
  defective-fix — 3 orthogonal plants → FIX REQUIRED/BLOCK, each named + a reproducing RED test (over-approval guard).
  isolation    — the context attestation present + valid (reviewed baseline == handoff; "build conversation not
                 provided"); the parent-transcript-absence half is a MANUAL check (per shared/subagent-protocol.md).

Usage:
    python check_review.py --outputs <dir> --case <clean-ship|defective-fix|isolation>
Writes grading.json ({"expectations":[{text,passed,evidence}]}) into --outputs and prints a report.
"""
import os, re, json, argparse, sys, subprocess, hashlib, glob

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


# ---------- WS6: doc-integrity self-test (the check_build 5.4b idiom) ----------
# verification-evidence.md is a REFERENCE (not in an eval workspace), so its verify-live rule is graded by a
# self-test that reads the sibling reference by path. The rule: verify-live usage not backed by a current record
# grades like INFERRED (SHIP unreachable). See shared/live-source-verification.md.
VERIFICATION_EVIDENCE_MD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references",
                                        "verification-evidence.md")
VERIFY_LIVE_RE = re.compile(r"(?is)verify-live.{0,400}(?:docs/verification|verified:).{0,200}"
                            r"(?:INFERRED|SHIP is unreachable|unreachable)")

def _self_test():
    txt = read(VERIFICATION_EVIDENCE_MD) or ""
    present = bool(VERIFY_LIVE_RE.search(txt))
    degen = bool(VERIFY_LIVE_RE.search("INFERRED counts as not verified; SHIP is unreachable while any is INFERRED.\n"))
    ok = present and not degen
    print("== check_review verify-live discipline self-test (WS6) ==")
    print("  [%s] verification-evidence.md names the verify-live rule (uncited/INFERRED usage → SHIP unreachable)"
          % ("PASS" if present else "FAIL"))
    print("  [%s] the check FIRES on a reference without the verify-live rule (non-vacuous)"
          % ("PASS" if not degen else "FAIL"))
    print("ALL GOOD" if ok else "SELF-TEST FAILED")
    return 0 if ok else 1


# ---------- root / report / handoff ----------

def find_root(base):
    for dp, dn, fn in os.walk(base):
        if dp.replace("\\", "/").endswith("docs/spec") and "specification.md" in fn:
            return os.path.dirname(os.path.dirname(dp))
    return base

def find_report(root):
    cands = glob.glob(os.path.join(root, "docs", "quality", "qa-report*.md"))
    if not cands:
        cands = glob.glob(os.path.join(root, "**", "qa-report*.md"), recursive=True)
    cands = [c for c in cands if os.path.isfile(c)]
    cands.sort(key=len)
    return (cands[0], read(cands[0])) if cands else (None, None)

def find_handoff(root):
    cands = glob.glob(os.path.join(root, "_artifacts", "exports", "build-handoff*.md"))
    if not cands:
        cands = glob.glob(os.path.join(root, "**", "build-handoff*.md"), recursive=True)
    cands = [c for c in cands if os.path.isfile(c)]
    cands.sort(key=len)
    return (read(cands[0]) if cands else None)

def fm(text, key):
    """A frontmatter/prose `key: value` line's value (stops at a trailing #/<!-- comment). Tolerant of markdown bold."""
    m = re.search(r"(?im)^\s*[-*]?\s*[`*]*" + re.escape(key) + r"[`*]*\s*[:=]\s*[`*]*([^#<\n|]+?)\s*(?:[#<|]|$)", text or "")
    return m.group(1).strip().strip("`*") if m else ""

def int_fm(text, key):
    v = fm(text, key)
    m = re.search(r"-?\d+", v or "")
    return int(m.group(0)) if m else None


# ---------- verdict / sections ----------

def verdict_of(report):
    """SHIP | FIX REQUIRED | BLOCK — from the frontmatter `verdict:` first, else a 'Verdict: X' line anywhere."""
    v = fm(report, "verdict").upper()
    for tok in ("FIX REQUIRED", "BLOCK", "SHIP"):
        if tok in v:
            return tok
    m = re.search(r"(?im)verdict[^A-Za-z0-9]{0,8}(SHIP|FIX\s*REQUIRED|BLOCK)", report or "")
    if m:
        t = re.sub(r"\s+", " ", m.group(1)).upper()
        return "FIX REQUIRED" if t.startswith("FIX") else t
    # last resort: a bare token in a short report
    for tok in ("FIX REQUIRED", "BLOCK", "SHIP"):
        if re.search(r"\b" + tok.replace(" ", r"\s+") + r"\b", (report or "").upper()):
            return tok
    return None

def section(report, name):
    """Text of a `## (x) <name>` .. next `## ` section (case-insensitive), else ''."""
    m = re.search(r"(?ims)^#{1,6}\s*(?:\([a-z0-9]\)\s*)?" + name + r"\b(.*?)(?:^#{1,6}\s|\Z)", report or "")
    return m.group(1) if m else ""

def finding_rows(report):
    """Data rows of the (d) Findings table — a `|`-row that carries a severity token or a REQ/VC ref (not the header
    / separator / the 'no findings' line). Returns [] when the report has NO explicit Findings section, so a
    Traceability/Ledger table is never miscounted as findings (an unstructured report scores its lift on the missing
    machine-readable tally, not a phantom finding count)."""
    sec = section(report, "Findings")
    if not sec:
        return []
    rows = []
    for line in sec.splitlines():
        if not line.strip().startswith("|"):
            continue
        low = line.lower()
        if re.match(r"^\s*\|[\s:\-|]+\|?\s*$", line):      # separator ---|---
            continue
        if "severity" in low and "route" in low:            # header
            continue
        # Count only DEFECT rows (a re-derived severity high/medium/low/critical). A ROUTING-NOTE row — a spec
        # ambiguity or a pre-existing [NEEDS CLARIFICATION] marker escalated to 03/06 per the honest-escalation
        # discipline — is NOT a defect and must not trip the crying-wolf guard: a sound build can legitimately carry
        # a routing note. Routing rows are typed "routing"/"note" and carry no severity, so requiring a severity token
        # (and excluding an explicit routing row) cleanly separates the two.
        if re.search(r"\b(high|medium|low|critical)\b", low) and not re.search(r"\brouting\b", low):
            rows.append(line)
    return rows


# ---------- git + node ----------

def git(root, *args):
    try:
        p = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=60)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except Exception as e:
        return 1, str(e)

def is_test(p):
    p = p.replace("\\", "/")
    b = os.path.basename(p)
    return bool(re.search(r"\.[cm]?js$", b)) and (".test." in b or "-test." in b or "test-" in b
                                                  or re.search(r"(^|/)(tests?|__tests__|review)/", p))

def new_test_files(root, final):
    """Test files 05 added since final_commit (committed-since-final ∪ untracked) — its verification assets."""
    paths = set()
    rc, out = git(root, "diff", "--name-only", final)
    if rc == 0:
        paths |= {ln.strip().replace("\\", "/") for ln in out.splitlines() if ln.strip()}
    rc, out = git(root, "ls-files", "--others", "--exclude-standard")
    if rc == 0:
        paths |= {ln.strip().replace("\\", "/") for ln in out.splitlines() if ln.strip()}
    return sorted(p for p in paths if is_test(p))

def run_test_file(root, relpath):
    try:
        p = subprocess.run(["node", "--test", relpath], cwd=root, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=120)
        out = (p.stdout or "") + (p.stderr or "")
        failm = re.search(r"(?m)^#\s*fail\s+(\d+)", out)
        fails = int(failm.group(1)) if failm else (0 if p.returncode == 0 else 1)
        return p.returncode, fails, out
    except Exception as e:
        return 1, 1, str(e)


# ---------- spec_slice_hash (recompute — identical to build_fixture / 04 emit / 05 verify) ----------

def norm_file(path):
    return open(path, "rb").read().decode("utf-8", "replace").replace("\r\n", "\n").replace("\r", "\n")

def recompute_hash(root, handoff=None):
    """Sprint slice: sprint file (+ manifest). Patch funnel: the handoff's spec_slice_path names the PATCH RECORD —
    the payload is that record alone (no manifest half; 02 is skipped by construction on the expedite lane)."""
    sp = fm(handoff or "", "spec_slice_path").replace("\\", "/")
    if "planning/patches/" in sp:
        record = os.path.join(root, *sp.split("/"))
        return ("sha256:" + hashlib.sha256(norm_file(record).encode("utf-8")).hexdigest()[:16]
                if os.path.isfile(record) else None)
    sprint = os.path.join(root, "docs/planning/sprints/sprint-01.md")
    manifest = os.path.join(root, "docs/design/approved/sprint-01/manifest.md")
    if not os.path.isfile(sprint):
        return None
    payload = norm_file(sprint)
    if os.path.isfile(manifest):
        payload += "\n" + norm_file(manifest)
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


# ---------- shared assertions ----------

def grade_common(root, report_path, report, handoff):
    check("QA report written at docs/quality/qa-report-sprint-NN.md (the verdict a human/06 acts on)",
          bool(report), report_path or "no qa-report*.md under the outputs root")
    report = report or ""

    verdict = verdict_of(report)
    check("The report states a verdict — SHIP | FIX REQUIRED | BLOCK",
          verdict in ("SHIP", "FIX REQUIRED", "BLOCK"), f"verdict parsed = {verdict or 'none'}")

    # context attestation — the isolation proof: inputs are the handoff + spec slice; the build conversation was NOT provided
    attest = bool(re.search(r"(?is)build\s+conversation[^\n]{0,40}not\s+provided", report)) \
        or bool(re.search(r"(?im)^\s*build_conversation\s*:\s*not[-\s]?provided", report))
    check("Context attestation present: 'build conversation: not provided' (the auditable isolation proof)",
          attest, "attestation marker found" if attest else "no 'build conversation not provided' marker")

    # the reviewed baseline_commit equals the handoff's (05 reviewed the seed it was handed, not something else)
    hb = fm(handoff or "", "baseline_commit")
    rb = fm(report, "baseline_commit")
    base_ok = bool(hb) and bool(rb) and rb[:10] == hb[:10]
    check("Attested baseline_commit matches the handoff's baseline_commit (reviewed the handed-off diff anchor)",
          base_ok, f"handoff baseline={hb[:12] or '—'}; report baseline={rb[:12] or '—'}")

    # spec_slice_hash: the grader recomputes over the seeded slice and confirms the handoff's hash is real (fixture
    # honesty); a valid review records the comparison result (match, for these fixtures).
    recomputed = recompute_hash(root, handoff)
    hh = fm(handoff or "", "spec_slice_hash")
    fixture_ok = bool(recomputed) and bool(hh) and recomputed == hh
    check("spec_slice_hash: the grader's recompute over the seeded slice equals the handoff's (a real binding)",
          fixture_ok, f"recomputed={recomputed or '—'}; handoff={hh or '—'}")
    report_hash = fm(report, "spec_slice_hash").lower()
    check("The report records the spec_slice_hash verification (match, for a slice that did not drift)",
          "match" in report_hash and "mismatch" not in report_hash, f"report spec_slice_hash = {report_hash or 'none'}")

    return verdict


# ---------- per-case ----------

DEFECT_A = r"req-008|vc-02"                          # the grouping logic bug
TEST_INTEGRITY = r"tautolog|hollow|assertion[-\s]?free|asserts?\s+nothing|mutation|still\s+green|green.{0,24}mutat"
COVERAGE = r"uncovered|no\s+(covering\s+)?test|not\s+(tested|covered)|missing\s+test|coverage\s+gap|claimed\s+(full|executed)|dishonest"

def grade_agent_review(root, report_path, report):
    """WS3 Task 3.7 — under Profile: agent-system, 05 re-executes the declared verifications at final_commit and
    stamps the eval-floor tally. Grades the qa-report frontmatter tally + the fail-closed rule (a missed floor or a
    hollow grader cannot SHIP). Handoff/oracle machinery is the webapp cases' remit; this focuses on the tally."""
    report = report or ""
    check("qa-report exists (the verdict 06 acts on)", bool(report.strip()), report_path or "no qa-report*.md")
    efm = fm(report, "eval_floors_met").lower().replace("\\", "/")
    check("Frontmatter carries eval_floors_met (true|false|n/a) — the exact token 06's G8 reads",
          efm in ("true", "false", "n/a", "na"), f"eval_floors_met={efm or '—'}")
    er = int_fm(report, "evals_run")
    check("Frontmatter carries evals_run: <int>", er is not None, f"evals_run={er}")
    v = verdict_of(report)
    check("Fail-closed: eval_floors_met: false ⇒ the verdict is NOT SHIP (a missed floor blocks ship)",
          not (efm == "false" and v == "SHIP"), f"eval_floors_met={efm}; verdict={v}")
    if efm in ("true", "false"):
        rerun = bool(re.search(r"(?i)eval[- ]?floor|re-?run|re-?execut", report))
        bite = bool(re.search(r"(?i)grader[- ]?bite|hack-resist|degenerate", report))
        check("agent floors: the report attests the final_commit floor re-run AND the grader hack-resistance bite",
              rerun and bite, f"floor re-run attested={rerun}; hack-resistance/bite attested={bite}")
    else:
        check("n/a path: eval_floors_met n/a with evals_run 0 (no eval-suite REQ in scope — nothing to re-run)",
              efm in ("n/a", "na") and er == 0, f"eval_floors_met={efm}; evals_run={er}")


def main():
    if "--self-test" in sys.argv:   # WS6 doc-integrity: verification-evidence.md names the verify-live rule
        sys.exit(_self_test())
    ap = argparse.ArgumentParser()
    ap.add_argument("--outputs", required=True)
    ap.add_argument("--case", required=True,
                    choices=["clean-ship", "defective-fix", "isolation", "patch-review", "agent"])
    a = ap.parse_args()
    root = find_root(a.outputs)
    report_path, report = find_report(root)
    handoff = find_handoff(root)

    if a.case == "agent":
        grade_agent_review(root, report_path, report)
        emit(a)
        return
    verdict = grade_common(root, report_path, report, handoff)
    report = report or ""
    fsec = section(report, "Findings")
    rows = finding_rows(report)
    final = fm(handoff or "", "final_commit")

    if a.case == "clean-ship":
        # Specificity — a sound build must SHIP with ~zero findings (the crying-wolf / false-positive guard).
        check("clean-ship: verdict is SHIP (a sound build verifies cleanly)",
              verdict == "SHIP", f"verdict={verdict}")
        nf = (int_fm(report, "findings_high") or 0) + (int_fm(report, "findings_medium") or 0) \
            + (int_fm(report, "findings_low") or 0)
        few = (nf == 0) and (len(rows) == 0)
        check("clean-ship: ~zero findings (the false-positive / crying-wolf guard — no invented defects)",
              few, f"tally high+med+low={nf}; finding rows={len(rows)}")
        inf = int_fm(report, "ledger_inferred")
        check("clean-ship: Verification Ledger Inferred = 0 (SHIP requires real execution evidence for every behavior)",
              inf == 0, f"ledger_inferred={inf}")

    elif a.case == "defective-fix":
        # Sensitivity — must NOT ship, and must NAME each of the three orthogonal plants in a structured finding.
        check("defective-fix: verdict is NOT SHIP (FIX REQUIRED/BLOCK — the over-approval / self-preference guard)",
              verdict in ("FIX REQUIRED", "BLOCK"), f"verdict={verdict}")

        a_named = bool(re.search(DEFECT_A, fsec, re.I))
        check("defective-fix: PLANT A named — a finding cites the REQ-008 grouping bug (REQ-008 / VC-02)",
              a_named, f"findings-section names REQ-008/VC-02 = {a_named}")

        b_named = bool(re.search(r"vc-01|req-001", fsec, re.I)) and bool(re.search(TEST_INTEGRITY, report, re.I))
        check("defective-fix: PLANT B named — a finding flags the tautological/hollow VC-01 test (test integrity)",
              b_named, f"findings names VC-01/REQ-001={bool(re.search(r'vc-01|req-001', fsec, re.I))}; "
                       f"test-integrity keyword in report={bool(re.search(TEST_INTEGRITY, report, re.I))}")

        c_named = bool(re.search(r"req-009|vc-03", fsec, re.I)) and bool(re.search(COVERAGE, report, re.I))
        check("defective-fix: PLANT C named — a finding flags REQ-009 uncovered / falsely claimed FULL (coverage)",
              c_named, f"findings names REQ-009/VC-03={bool(re.search(r'req-009|vc-03', fsec, re.I))}; "
                       f"coverage keyword in report={bool(re.search(COVERAGE, report, re.I))}")

        # The executable findings interface — 05 committed a reproducing RED test that FAILS against the defective impl.
        nts = new_test_files(root, final) if final else []
        red = []
        for t in nts:
            rc, fails, _ = run_test_file(root, t)
            if rc != 0 or fails > 0:
                red.append(t)
        check("defective-fix: 05 emitted a reproducing RED test (a new *.test.js that FAILS against the defective impl)",
              bool(red), f"new test files={nts or 'none'}; RED (reproduce the defect)={red or 'none'}")

        # Ledger↔verdict consistency — a not-SHIP verdict with findings/inferred/MUST-gap is internally consistent.
        nf = (int_fm(report, "findings_high") or 0) + (int_fm(report, "findings_medium") or 0) \
            + (int_fm(report, "findings_low") or 0)
        must_gap = "true" in fm(report, "must_gap").lower()
        consistent = (verdict != "SHIP") and (nf > 0 or len(rows) > 0 or must_gap
                                              or (int_fm(report, "ledger_inferred") or 0) > 0)
        check("defective-fix: ledger↔verdict consistent (not-SHIP backed by findings / a MUST-gap / INFERRED > 0)",
              consistent, f"verdict={verdict}; tally={nf}; rows={len(rows)}; must_gap={must_gap}")

        # Every finding carries a pointer (a file:line, a test path, or the handoff location it violates).
        pointered = all(re.search(r"\.[cm]?js\b|:\d+|handoff|coverage|test", r, re.I) for r in rows) and bool(rows)
        check("defective-fix: every finding carries a pointer (file:line / test path / the handoff location)",
              pointered, f"finding rows={len(rows)}; all carry a pointer={pointered}")

    elif a.case == "patch-review":
        # The WS1 patch seed variant: same isolation + honesty machinery, scope bounded to the patch.
        # PR1 — the seed manifest names the patch record (the scope anchor 05 was seeded with)
        seeded = bool(re.search(r"planning/patches/patch-\d+\.md", report))
        check("patch-review: the seed manifest lists the patch record (docs/planning/patches/patch-NNN.md)",
              seeded, "patch record named in the report" if seeded else "no patches/patch-NNN.md path in the report")

        # PR2 — the review is patch-keyed: the report names the patch id and lands at qa-report-patch-NNN.md
        pid_named = bool(re.search(r"\bpatch-001\b", report))
        patch_keyed = bool(report_path) and "patch-001" in os.path.basename(report_path)
        check("patch-review: the review is patch-keyed (report names patch-001; filename qa-report-patch-NNN.md)",
              pid_named and patch_keyed,
              f"patch id named={pid_named}; report file={os.path.basename(report_path or '') or '—'}")

        # PR3 — the sound patch verifies cleanly within its bounded scope
        inf = int_fm(report, "ledger_inferred")
        check("patch-review: verdict SHIP with Ledger Inferred = 0 (the sound patch verifies cleanly, bounded scope)",
              verdict == "SHIP" and inf == 0, f"verdict={verdict}; ledger_inferred={inf}")

        # PR4 — the honesty gate is UNCHANGED on the expedite lane: SHIP is unreachable with any INFERRED behavior
        gate_holds = not (verdict == "SHIP" and (inf is None or inf > 0))
        check("patch-review: honesty gate unchanged — SHIP is unreachable while any behavior is INFERRED",
              gate_holds, f"verdict={verdict}; ledger_inferred={inf}")

    elif a.case == "isolation":
        # The isolation proof, made deterministic. (Reuses the clean fixture; the parent-transcript-absence half is a
        # MANUAL check per shared/subagent-protocol.md — Pass 2 judgment is never deterministically graded.)
        inputs_marker = bool(re.search(r"(?is)inputs?\W+.{0,40}(handoff|build-handoff).{0,40}(spec|slice)", report)) \
            or bool(re.search(r"(?is)seeded\s+with\s+only", report))
        check("isolation: the attestation names its inputs (the handoff + the spec slice — the seed)",
              inputs_marker, "inputs marker found" if inputs_marker else "no 'inputs: [handoff, spec slice]' marker")
        attest = bool(re.search(r"(?is)build\s+conversation[^\n]{0,40}not\s+provided", report)) \
            or bool(re.search(r"(?im)^\s*build_conversation\s*:\s*not[-\s]?provided", report))
        check("isolation: 'build conversation: not provided' — the reviewer never read the build session",
              attest, "attestation marker found" if attest else "no build-conversation-not-provided marker")
        hb = fm(handoff or "", "baseline_commit"); rb = fm(report, "baseline_commit")
        check("isolation: the attested baseline_commit resolves to the handoff's (reviewed exactly the handed diff)",
              bool(hb) and rb[:10] == hb[:10], f"handoff={hb[:12] or '—'}; report={rb[:12] or '—'}")
        # opened-files ⊆ seed is asserted in the report (the grader confirms the claim is present; a human confirms the
        # parent transcript carries no builder-reasoning markers — the manual half).
        opened = bool(re.search(r"(?is)opened[\s-]*files?\W+.{0,60}(seed|handoff|spec|src)", report)) \
            or bool(re.search(r"(?is)⊆\s*seed|subset of.{0,20}seed", report))
        check("isolation: the attestation asserts opened-files ⊆ seed (auditable scope of what 05 read)",
              opened, "opened-files ⊆ seed marker found" if opened else "no opened-files-subset-of-seed marker")

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
