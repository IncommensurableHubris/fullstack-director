#!/usr/bin/env python3
"""Validation for the emitted spine-integrity script (00-discovery's `templates/scripts/verify-spine.py`) — the
`validate_grader.py` discipline applied to the SCRIPT: proves it is neither over-strict (the hand-ideal composed
spine exits 0 with every check ok) nor vacuous (each degenerate spine fires exactly its named check id at its
declared severity). Deterministic, no live skill execution — this is the WS1 §B4 parity eval: the script and
`status`'s FAIL checks must never diverge (every FAIL-class check the script gains joins status's load-bearing
set in the same workstream — L6 in Task 3.10), and both are held to the same fixtures.

Per case: stage the spec-first canonical ideal into a temp dir, copy the script template to `scripts/verify-spine.py`
(exactly where 00-discovery emits it), optionally mutate the spine, run `python scripts/verify-spine.py --json` from
the project root, and assert exit code + per-check `ok`/severity from the JSON contract:
    {"result": "PASS|FAIL", "checks": [{"id", "severity", "ok", "detail"}]}

Usage:
    python validate_script.py
Exit 0 iff every expectation holds; prints a validation table.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
IDEAL = os.path.join(HERE, "fixtures", "_ideal", "spec-first")
SCRIPT_TEMPLATE = os.path.join(REPO, ".agents", "skills", "00-discovery", "templates", "scripts", "verify-spine.py")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)


def overlay(src, dst):
    for dp, _dn, fn in os.walk(src):
        rel = os.path.relpath(dp, src)
        for f in fn:
            d = os.path.join(dst, f) if rel == "." else os.path.join(dst, rel, f)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy(os.path.join(dp, f), d)


# ---------- degenerate mutations (each targets exactly one check id) ----------

def m_l1_unresolvable_file(root):
    """Registry row's File cell points at a file that does not exist -> L1."""
    p = os.path.join(root, "docs/spec/specification.md")
    write(p, read(p).replace(
        "| REQ-010 | Read current and past digests | SHOULD | stated | capabilities/digest.md |",
        "| REQ-010 | Read current and past digests | SHOULD | stated | capabilities/ghost.md |"))


def m_l2_broken_delimiter(root):
    """Leaf loses REQ-010's closing delimiter (the broken-registry seed) -> L2."""
    p = os.path.join(root, "docs/spec/capabilities/digest.md")
    write(p, read(p).replace("<!-- /REQ-010 -->", "<!-- (delimiter removed by validator) -->"))


def m_l3_orphan_block(root):
    """A delimited block with no registry row -> L3."""
    p = os.path.join(root, "docs/spec/capabilities/digest.md")
    write(p, read(p) + "\n### REQ-999: Orphaned capability   (MAY)\n\nPlanted by the validator.\n<!-- /REQ-999 -->\n")


def m_l4_duplicate_id(root):
    """The same REQ id appears twice in the registry -> L4."""
    p = os.path.join(root, "docs/spec/specification.md")
    row = "| REQ-010 | Read current and past digests | SHOULD | stated | capabilities/digest.md |"
    write(p, read(p).replace(row, row + "\n" + row))


def m_l5_malformed_json(root):
    """amendment-log.json is not valid JSON -> L5."""
    write(os.path.join(root, "docs/spec/amendment-log.json"), '{ "amendments": [ {"id": "AMD-001",\n')


def m_l5_schema_drift(root):
    """An amendment row grows a field outside the frozen schema -> L5."""
    p = os.path.join(root, "docs/spec/amendment-log.json")
    data = json.loads(read(p))
    data["amendments"][0]["date"] = "2026-07-07"
    write(p, json.dumps(data, indent=2) + "\n")


# WS3 Task 3.3 — the eval-suite acceptance block (in-spine golden dataset) that L6 checks.
_EVAL_BLOCK_LINES = (
    "\n**Acceptance (eval-suite):**\n"
    "dataset: docs/spec/evals/digest/{name}.jsonl   (versioned, in-spine)\n"
    "grader: code\n"
    "metric: pass@k\n"
    "floor: 95%          class: regression\n"
    "negatives: >=1 must-not case in the dataset\n"
)


def m_l6_valid_dataset(root):
    """A REQ carries an eval block whose in-spine dataset resolves -> L6 ok, every check ok, exit 0."""
    p = os.path.join(root, "docs/spec/capabilities/digest.md")
    write(p, read(p).replace("<!-- /REQ-010 -->", _EVAL_BLOCK_LINES.format(name="quality") + "<!-- /REQ-010 -->"))
    write(os.path.join(root, "docs/spec/evals/digest/quality.jsonl"), '{"input": "x", "expect": "y"}\n')


def m_l6_dangling_dataset(root):
    """A REQ's eval-block dataset ref does not resolve on disk -> L6 fires (FAIL, exit 1)."""
    p = os.path.join(root, "docs/spec/capabilities/digest.md")
    write(p, read(p).replace("<!-- /REQ-010 -->", _EVAL_BLOCK_LINES.format(name="ghost") + "<!-- /REQ-010 -->"))


# WS6 Task 6.2 — verify-live declaration (architecture-constraints §Verify-live) + docs/verification/<tech>.md record.
_VERIFY_LIVE_BLOCK = (
    "\n## Verify-live\n\n"
    "> Technologies too new for reliable training-data recall — live-source-verify + record before use.\n"
    "> See shared/live-source-verification.md.\n\n"
    "- **openclaw:** docs: https://openclaw.dev/docs · source: https://github.com/example/openclaw\n"
)
_RECORD = (
    "---\n"
    "verified_against: openclaw@0.4.2\n"
    "docs_fetched:\n"
    "  - https://openclaw.dev/docs/agents#loop\n"
    "---\n\n"
    "## Verified claims\n\n"
    "| claim (an API/config/behavior fact) | citation | corrects |\n"
    "|--------------------------------------|----------|----------|\n"
    "| the agent loop entry point is `Claw.run(task)` | %s | — |\n"
)


def _declare_verify_live(root):
    p = os.path.join(root, "docs/spec/architecture-constraints.md")
    write(p, read(p) + _VERIFY_LIVE_BLOCK)


def m_l7_valid(root):
    """A declared verify-live tech + a resolving, cited record -> L7 ok, every check ok, exit 0."""
    _declare_verify_live(root)
    write(os.path.join(root, "docs/verification/openclaw.md"), _RECORD % "https://openclaw.dev/docs/agents#loop")


def m_l7_declared_no_record(root):
    """A verify-live declaration with no docs/verification/<tech>.md -> L7 FAIL."""
    _declare_verify_live(root)


def m_l7_uncited_row(root):
    """A record whose claims-table row has an empty citation -> L7 FAIL (the confabulation guard)."""
    _declare_verify_live(root)
    write(os.path.join(root, "docs/verification/openclaw.md"), _RECORD % "")


def m_l7_orphan_record(root):
    """A docs/verification/*.md with no declaration row -> L7 FAIL (the orphan direction)."""
    write(os.path.join(root, "docs/verification/openclaw.md"), _RECORD % "https://openclaw.dev/docs/agents#loop")


def m_w1_marker(root):
    """A surviving [NEEDS CLARIFICATION] marker -> W1 fires in JSON, exit stays 0."""
    p = os.path.join(root, "docs/spec/specification.md")
    write(p, read(p).replace(
        "- _(none)_",
        "- [NEEDS CLARIFICATION: what instant locks the day's standups?]"))


def m_w2_ledger_drift(root):
    """Ledger loses REQ-010's row (the dropped-req seed) -> W2 fires in JSON, exit stays 0."""
    p = os.path.join(root, "docs/planning/backlog.md")
    write(p, "".join(ln for ln in read(p).splitlines(keepends=True) if not re.match(r"\|\s*REQ-010\s*\|", ln)))


def m_w3_unpadded_id(root):
    """An id drops its zero-padding -> W3 fires in JSON, exit stays 0."""
    p = os.path.join(root, "docs/spec/amendment-log.json")
    write(p, read(p).replace('"id": "AMD-001"', '"id": "AMD-1"'))


def m_w4_profile_missing(root):
    """specification.md loses its `- **Profile:**` field -> W4 fires in JSON, exit stays 0 (defaults webapp)."""
    p = os.path.join(root, "docs/spec/specification.md")
    write(p, re.sub(r"(?im)^\s*-\s*\*\*Profile:\*\*.*\n", "", read(p)))


def m_w5_bloated_spine(root):
    """The spine balloons past 40 prose lines per REQ (restated methodology) -> W5 fires, exit stays 0."""
    p = os.path.join(root, "docs/spec/design-intent.md")
    filler = "\n".join("The framework's methodology, restated here at length for the %dth time." % i
                       for i in range(300))
    write(p, read(p) + "\n" + filler + "\n")


# name, mutation (None = ideal), expected check id (None = all ok), expected severity, expected exit code
EXPECTATIONS = [
    ("ideal", None, None, None, 0),
    ("l1-unresolvable-file", m_l1_unresolvable_file, "L1_registry_file_resolves", "FAIL", 1),
    ("l2-broken-delimiter", m_l2_broken_delimiter, "L2_leaf_contains_block", "FAIL", 1),
    ("l3-orphan-block", m_l3_orphan_block, "L3_no_orphan_blocks", "FAIL", 1),
    ("l4-duplicate-id", m_l4_duplicate_id, "L4_no_duplicate_req_ids", "FAIL", 1),
    ("l5-malformed-json", m_l5_malformed_json, "L5_amendment_log_valid", "FAIL", 1),
    ("l5-schema-drift", m_l5_schema_drift, "L5_amendment_log_valid", "FAIL", 1),
    ("l6-valid-eval-block", m_l6_valid_dataset, None, None, 0),
    ("l6-dangling-dataset", m_l6_dangling_dataset, "L6_dataset_refs_resolve", "FAIL", 1),
    ("l7-valid-record", m_l7_valid, None, None, 0),
    ("l7-declared-no-record", m_l7_declared_no_record, "L7_verify_live_records", "FAIL", 1),
    ("l7-uncited-row", m_l7_uncited_row, "L7_verify_live_records", "FAIL", 1),
    ("l7-orphan-record", m_l7_orphan_record, "L7_verify_live_records", "FAIL", 1),
    ("w1-marker", m_w1_marker, "W1_surviving_markers", "WARN", 0),
    ("w2-ledger-drift", m_w2_ledger_drift, "W2_ledger_registry_sync", "WARN", 0),
    ("w3-unpadded-id", m_w3_unpadded_id, "W3_id_zero_padding", "WARN", 0),
    ("w4-profile-missing", m_w4_profile_missing, "W4_profile_missing", "WARN", 0),
    ("w5-bloated-spine", m_w5_bloated_spine, "W5_spine_density", "WARN", 0),
]

CHECK_BUDGET = os.path.join(REPO, "docs", "eval-methodology", "harness-reference", "check_budget.py")
EVAL_BLOCK = os.path.join(REPO, "docs", "eval-methodology", "harness-reference", "eval_block.py")
CHECK_BUILD = os.path.join(REPO, ".agents", "skills", "04-builder", "evals", "check_build.py")
CHECK_REVIEW = os.path.join(REPO, ".agents", "skills", "05-reviewer", "evals", "check_review.py")
CHECK_ARCH = os.path.join(REPO, ".agents", "skills", "03-architect", "evals", "check_architecture.py")
CHECK_RELEASE = os.path.join(REPO, ".agents", "skills", "06-release", "evals", "check_release.py")
CHECK_STATUS = os.path.join(REPO, ".agents", "skills", "status", "evals", "check_status.py")
VENDOR = os.path.join(REPO, "tools", "vendor.py")


def run_script(root):
    proc = subprocess.run([sys.executable, os.path.join("scripts", "verify-spine.py"), "--json"],
                          cwd=root, capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        raise SystemExit("verify-spine.py --json emitted non-JSON stdout:\n%s\n%s" % (proc.stdout, proc.stderr))
    return proc.returncode, data


def run_hash(root):
    """Run `verify-spine.py --hash` and return (exit_code, digest)."""
    proc = subprocess.run([sys.executable, os.path.join("scripts", "verify-spine.py"), "--hash"],
                          cwd=root, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return proc.returncode, (proc.stdout or "").strip()


def stage_hash():
    """Stage the ideal spine + the emitted script into a fresh temp dir; caller mutates + reads, then rmtrees."""
    tmp = tempfile.mkdtemp(prefix="spine-hash-")
    dst = os.path.join(tmp, "state")
    os.makedirs(dst)
    overlay(IDEAL, dst)
    os.makedirs(os.path.join(dst, "scripts"), exist_ok=True)
    shutil.copy(SCRIPT_TEMPLATE, os.path.join(dst, "scripts", "verify-spine.py"))
    return tmp, dst


def stage_and_run(mutation):
    tmp = tempfile.mkdtemp(prefix="spine-val-")
    try:
        dst = os.path.join(tmp, "state")
        os.makedirs(dst)
        overlay(IDEAL, dst)
        os.makedirs(os.path.join(dst, "scripts"), exist_ok=True)
        shutil.copy(SCRIPT_TEMPLATE, os.path.join(dst, "scripts", "verify-spine.py"))
        if mutation:
            mutation(dst)
        return run_script(dst)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def validate():
    if not os.path.isfile(SCRIPT_TEMPLATE):
        print("FAIL: script template absent at %s" % os.path.relpath(SCRIPT_TEMPLATE, REPO))
        return False
    rows, ok = [], True
    for name, mutation, check_id, severity, want_exit in EXPECTATIONS:
        code, data = stage_and_run(mutation)
        checks = {c["id"]: c for c in data.get("checks", [])}
        if check_id is None:
            good = code == want_exit and data.get("result") == "PASS" and all(c["ok"] for c in checks.values())
            note = "" if good else "exit=%s result=%s not-ok=%s" % (
                code, data.get("result"), sorted(k for k, c in checks.items() if not c["ok"]))
            rows.append((name, "exit 0, every check ok", good, note))
        else:
            c = checks.get(check_id)
            fired = c is not None and c["ok"] is False and c["severity"] == severity
            good = fired and code == want_exit
            others = sorted(k for k, v in checks.items() if k != check_id and not v["ok"])
            if good:
                note = "target fired" + ("; also %s" % others if others else "")
            elif c is None:
                note = "%s missing from --json output" % check_id
            else:
                note = "ok=%s severity=%s exit=%s (want not-ok/%s/exit %s)" % (
                    c["ok"], c["severity"], code, severity, want_exit)
            rows.append((name, "%s fires as %s, exit %s" % (check_id, severity, want_exit), good, note))
        ok = ok and good
    # the terseness invariant's grader helper (WS1 §B6): in-budget passes, over-budget raises, no-budget no-ops
    proc = subprocess.run([sys.executable, CHECK_BUDGET, "--self-test"],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    good = proc.returncode == 0
    rows.append(("check-budget-helper", "self-test exits 0 (over-budget raises)", good,
                 "" if good else (proc.stdout + proc.stderr).strip()[-160:]))
    ok = ok and good
    # the shared eval-block parser (WS3 §3.3 helper; reused by 3.7/5.3): its self-test proves the grammar parse
    proc = subprocess.run([sys.executable, EVAL_BLOCK, "--self-test"],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    good = proc.returncode == 0
    rows.append(("eval-block-parser", "self-test exits 0 (parser is sound)", good,
                 "" if good else (proc.stdout + proc.stderr).strip()[-160:]))
    ok = ok and good
    # the WS5 5.4b build-discipline security-floor lines (slopcheck + dependency-cooldown) + the WS6 verify-live rule
    proc = subprocess.run([sys.executable, CHECK_BUILD, "--self-test"],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    good = proc.returncode == 0
    rows.append(("build-discipline-lines", "self-test exits 0 (slopcheck + cooldown + verify-live present)", good,
                 "" if good else (proc.stdout + proc.stderr).strip()[-160:]))
    ok = ok and good
    # the WS6 05-reviewer verify-live discipline (uncited/INFERRED verify-live usage → SHIP unreachable)
    proc = subprocess.run([sys.executable, CHECK_REVIEW, "--self-test"],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    good = proc.returncode == 0
    rows.append(("review-verify-live-rule", "self-test exits 0 (verification-evidence names the rule)", good,
                 "" if good else (proc.stdout + proc.stderr).strip()[-160:]))
    ok = ok and good
    # the WS6 03-architect S18 verify-live ADR citation grader (ideal passes; uncited/missing fire; no-decl N/A)
    proc = subprocess.run([sys.executable, CHECK_ARCH, "--self-test"],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    good = proc.returncode == 0
    rows.append(("arch-s18-verify-live", "self-test exits 0 (S18 bites)", good,
                 "" if good else (proc.stdout + proc.stderr).strip()[-160:]))
    ok = ok and good
    # the WS6 06-release G11 verify-live gate grader (N/A; L7-ok ships; L7-FAIL under RELEASED fires; fail-closed)
    proc = subprocess.run([sys.executable, CHECK_RELEASE, "--self-test"],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    good = proc.returncode == 0
    rows.append(("release-g11-verify-live", "self-test exits 0 (G11 bites)", good,
                 "" if good else (proc.stdout + proc.stderr).strip()[-160:]))
    ok = ok and good
    # the WS6 status L7-parity + coverage-line doc-integrity (the load-bearing set mirrors the emitted script)
    proc = subprocess.run([sys.executable, CHECK_STATUS, "--self-test"],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    good = proc.returncode == 0
    rows.append(("status-l7-parity", "self-test exits 0 (status names L7 + the coverage line)", good,
                 "" if good else (proc.stdout + proc.stderr).strip()[-160:]))
    ok = ok and good
    # the WSB vendoring CLI — hermetic staged trees (cases 1–9) + the REAL-tree emission (case 10: this repo →
    # temp consumer; the master commits NO bridge — 2026-07-12 — so case 10 is the standing emission guard)
    proc = subprocess.run([sys.executable, VENDOR, "--self-test"],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    good = proc.returncode == 0
    rows.append(("vendor-self-test", "self-test exits 0 (sound + real-tree emission clean)", good,
                 "" if good else (proc.stdout + proc.stderr).strip()[-160:]))
    ok = ok and good

    # ---------- WS4 Task 4.7: spine release identity (--hash) ----------
    # deterministic (same digest twice) · change-sensitive (a docs/spec byte flips it) · scoped (a change OUTSIDE
    # docs/spec leaves it unchanged — "which spec state shipped" must track the spine and nothing else).
    tmp, dst = stage_hash()
    try:
        c1, h1 = run_hash(dst)
        _c2, h2 = run_hash(dst)
        det = c1 == 0 and bool(re.fullmatch(r"[0-9a-f]{64}", h1 or "")) and h1 == h2
        rows.append(("hash-deterministic", "--hash exits 0 + identical sha256 twice", det,
                     "" if det else "code=%s h1=%s h2=%s" % (c1, h1, h2)))
        ok = ok and det
        sp = os.path.join(dst, "docs/spec/specification.md")
        write(sp, read(sp) + "\n<!-- one byte of spine drift -->\n")
        _c3, h3 = run_hash(dst)
        changed = bool(h3) and h3 != h1
        rows.append(("hash-change-sensitive", "a docs/spec byte change alters the hash", changed,
                     "" if changed else "h1=%s h3=%s" % (h1, h3)))
        ok = ok and changed
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    tmp, dst = stage_hash()
    try:
        _c, hb = run_hash(dst)
        bp = os.path.join(dst, "docs/planning/backlog.md")
        write(bp, read(bp) + "\n<!-- a change outside the spine -->\n")
        _c, hb2 = run_hash(dst)
        scoped = bool(hb) and hb == hb2
        rows.append(("hash-scoped-to-spec", "a change outside docs/spec leaves the hash unchanged", scoped,
                     "" if scoped else "hb=%s hb2=%s" % (hb, hb2)))
        ok = ok and scoped
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    w = max(len(r[0]) for r in rows)
    e = max(len(r[1]) for r in rows)
    print("\n== verify-spine.py script validation (spec-first ideal + degenerates) ==")
    print("  %s  %s  result  notes" % ("case".ljust(w), "expectation".ljust(e)))
    for name, exp, good, note in rows:
        print("  %s  %s  %s  %s" % (name.ljust(w), exp.ljust(e), ("PASS" if good else "FAIL").ljust(6), note))
    return ok


def main():
    ok = validate()
    print("\n%s" % ("ALL GOOD — the script is sound (not over-strict, not vacuous)" if ok else "VALIDATION FAILED"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
