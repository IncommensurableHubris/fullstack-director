#!/usr/bin/env python3
"""Grader-validation for check_integration.py (the `feedback_grader_validate_on_real_outputs` +
`feedback_mutation_grader_robustness` discipline, applied to a COMPOSITION). Proves each case's grader is neither
over-strict (a hand-ideal composed state passes every assertion) nor vacuous (each degenerate composed state fires
its target assertion). Chain-free + deterministic — runs with NO live skill execution, so it is the safety net the
live chain runs demonstrate.

Per case: stage a composed ideal (the spec-first canonical tree + small case overlays) into a temp dir, optionally
mutate it, run `check_integration.py --case <case>` as a subprocess, parse grading.json, and assert.

Usage:
    python validate_grader.py [--case spec-first|governance|spine-collapse|isolation-chain|all]
Exit 0 iff every expectation holds; prints a validation table per case.
"""
import os, sys, json, shutil, subprocess, tempfile, re, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")
IDEAL_SPEC_FIRST = os.path.join(FIX, "_ideal", "spec-first")
GRADER = os.path.join(HERE, "check_integration.py")

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
    for dp, dn, fn in os.walk(src):
        rel = os.path.relpath(dp, src)
        for f in fn:
            d = os.path.join(dst, f) if rel == "." else os.path.join(dst, rel, f)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy(os.path.join(dp, f), d)


# ---------- spec-first mutations ----------

def m_broken_registry(root):
    p = os.path.join(root, "docs/spec/capabilities/digest.md")
    write(p, read(p).replace("<!-- /REQ-010 -->", "<!-- (delimiter removed by validator) -->"))

def m_silent_swap(root):
    write(os.path.join(root, "docs/spec/amendment-log.json"), '{\n  "amendments": []\n}\n')
    ac = os.path.join(root, "docs/spec/architecture-constraints.md")
    write(ac, re.sub(r"(?m)^- \*\*Datastore:\*\* .*$",
                     "- **Datastore:** SQLite (embedded, single-file; no external database server).", read(ac)))

def m_retired_artifacts(root):
    write(os.path.join(root, "docs/planning/user-stories/US-001.md"),
          "# US-001: Submit a standup\n\nAs a member, I want to submit a standup...\n")

def m_dropped_req(root):
    p = os.path.join(root, "docs/planning/backlog.md")
    write(p, "".join(ln for ln in read(p).splitlines(keepends=True) if not re.match(r"\|\s*REQ-010\s*\|", ln)))

def m_missing_gemini_bridge(root):
    """The GEMINI.md bridge (`@./AGENTS.md`) is missing -> Invariant 9 fires (the projection can't reach Gemini)."""
    os.remove(os.path.join(root, "GEMINI.md"))


# ---------- governance mutations (operate on the composed governance ideal) ----------

def gm_ships(root):
    p = os.path.join(root, "CLAUDE.md")
    write(p, re.sub(r"(?im)^(\s*-?\s*\*\*Next command:\*\*).*$", r"\1 `/06-release sprint 1`", read(p)))

def gm_06_deployed(root):
    p = os.path.join(root, "docs/release/release-report-sprint-01.md")
    txt = read(p)
    txt = re.sub(r"(?im)^status:\s*BLOCKED\s*$", "status: RELEASED", txt)
    txt = re.sub(r"(?im)^deployed_commit:\s*none\s*$", "deployed_commit: a1b2c3d4e5", txt)
    write(p, txt)
    write(os.path.join(root, "_deploy/live/release.json"), '{"sprint":"01"}\n')

def gm_missed_blockers(root):
    p = os.path.join(root, "CLAUDE.md")
    txt = read(p)
    txt = re.sub(r"(?im)^(\s*-?\s*\*\*Amendments:\*\*).*$", r"\1 0 pending · 0 deferred.", txt)
    txt = re.sub(r"(?im)^(\s*-?\s*\*\*Open \[NEEDS CLARIFICATION\]:\*\*).*$", r"\1 0", txt)
    write(p, txt)

def gm_06_resolved(root):
    p = os.path.join(root, "docs/spec/amendment-log.json")
    data = json.loads(read(p))
    for r in data["amendments"]:
        if r.get("id") == "AMD-003":
            r["disposition"] = "approved"
    write(p, json.dumps(data, indent=2) + "\n")


# ---------- spine-collapse mutations (operate on the composed post-pivot ideal) ----------

def sm_shatter(root):
    p = os.path.join(root, "docs/spec/capabilities/digest.md")
    write(p, read(p).replace("<!-- /REQ-010 -->", "<!-- (delimiter removed by validator) -->"))

def sm_dangling(root):
    p = os.path.join(root, "docs/planning/backlog.md")
    write(p, read(p).replace(
        "| REQ-010 | Read current and past digests | SHOULD | 3 | 02 | planned |",
        "| REQ-010 | Read current and past digests | SHOULD | 3 | 02 | planned |\n"
        "| REQ-999 | Bogus dangling ref | MAY | 3 | 02 | planned |"))

def sm_silent_pivot(root):
    p = os.path.join(root, "docs/spec/amendment-log.json")
    data = json.loads(read(p))
    data["amendments"] = [r for r in data["amendments"] if r.get("id") != "AMD-004"]
    write(p, json.dumps(data, indent=2) + "\n")

def sm_charter_drift(root):
    p = os.path.join(root, "docs/discovery/charter.md")
    write(p, read(p).replace("spread across timezones", "in the same office").replace("stay in sync", "run better meetings"))

def sm_not_applied(root):
    p = os.path.join(root, "docs/spec/architecture-constraints.md")
    write(p, re.sub(r"(?im)^- \*\*Regions / data residency:\*\* .*$",
                    "- **Regions / data residency:** EU region only (data residency requirement).", read(p)))


# ---------- isolation-chain mutations (operate on the fresh-05 QA report / handoff) ----------

def icm_rubber_stamp(root):
    p = os.path.join(root, "docs/quality/qa-report-sprint-01.md")
    write(p, re.sub(r"(?im)^verdict:\s*FIX REQUIRED\s*$", "verdict: SHIP", read(p)))

def icm_no_attestation(root):
    p = os.path.join(root, "docs/quality/qa-report-sprint-01.md")
    write(p, re.sub(r"(?im)^.*build conversation.*not provided.*$", "- (attestation omitted by validator)", read(p)))

def icm_baseline_mismatch(root):
    p = os.path.join(root, "docs/quality/qa-report-sprint-01.md")
    write(p, re.sub(r"(?im)^baseline_commit:\s*abc1234567\s*$", "baseline_commit: 9999999999", read(p)))


# ---------- agent-chain mutations (WS5 5.5a — operate on the composed agent-system ideal) ----------

def acm_missing_contract(root):
    """The agent-contract is gutted — the six-section completeness check (AC2) must fire."""
    write(os.path.join(root, "docs/spec/agent-contract.md"), "# Agent Contract\n\n(to be written)\n")

def acm_floor_fail_ship(root):
    """A missed eval floor stamped SHIP — the floor-consistency guard (AC4) must fire."""
    p = os.path.join(root, "docs/quality/qa-report-sprint-01.md")
    write(p, read(p).replace("eval_floors_met: true", "eval_floors_met: false"))

def acm_topology_no_justification(root):
    """The topology ADR loses its ~15x token-economics justification (AC5) must fire."""
    p = os.path.join(root, "docs/architecture/adr/ADR-002.md")
    write(p, re.sub(r"(?is)## Token economics.*", "## Token economics\n\n(TBD — not yet weighed)\n", read(p)))


# ---------- verify-live mutations (WS6 — operate on the composed verify-live ideal) ----------

def vlm_orphan_record(root):
    """Remove the ## Verify-live declaration but keep docs/verification/openclaw.md → an orphan record (VL1)."""
    p = os.path.join(root, "docs/spec/architecture-constraints.md")
    write(p, re.sub(r"(?ims)^##\s+Verify-live\b.*?(?=^##\s|\Z)", "", read(p)))

def vlm_uncited_claim(root):
    """Blank the citation cell of the record's first claims row → an uncited claim (VL1, the confabulation guard)."""
    p = os.path.join(root, "docs/verification/openclaw.md")
    write(p, read(p).replace("| https://openclaw.dev/docs/agents#loop | assumed `Claw.start()` from memory — the docs show `Claw.run` |",
                             "|  | assumed `Claw.start()` from memory — the docs show `Claw.run` |"))

def vlm_stale_version(root):
    """Downgrade the record's verified_against below the manifest pin → a stale record (VL5 currency)."""
    p = os.path.join(root, "docs/verification/openclaw.md")
    write(p, read(p).replace("verified_against: openclaw@0.4.2", "verified_against: openclaw@0.3.0"))

def vlm_inferred_build_claim(root):
    """Flip the handoff's verify-live VC row EXECUTED → INFERRED → a cited-but-inferred claim (VL3)."""
    p = os.path.join(root, "_artifacts/exports/build-handoff-sprint-01.md")
    write(p, read(p).replace("| EXECUTED | `node --test test/agent.test.js` | verified: docs/verification/openclaw.md",
                             "| INFERRED | — (no runtime) | verified: docs/verification/openclaw.md"))


# ---------- case config: ideal staging (overlay dirs) + negatives (name, mutation, target label) ----------

CASES = {
    "spec-first": {
        "overlays": [IDEAL_SPEC_FIRST],
        "negatives": [
            ("broken-registry", m_broken_registry, "Invariant 2"),
            ("silent-swap", m_silent_swap, "Invariant 4"),
            ("retired-artifacts", m_retired_artifacts, "Invariant 7"),
            ("dropped-req", m_dropped_req, "Invariant 3"),
            ("missing-gemini-bridge", m_missing_gemini_bridge, "Invariant 9"),
        ],
    },
    "governance": {
        "overlays": [IDEAL_SPEC_FIRST, os.path.join(FIX, "governance-seed"), os.path.join(FIX, "_ideal", "governance")],
        "negatives": [
            ("gov-ships", gm_ships, "Governance G3"),
            ("gov-06-deployed", gm_06_deployed, "Governance G4"),
            ("gov-missed-blockers", gm_missed_blockers, "Governance G2"),
            ("gov-06-resolved", gm_06_resolved, "Governance G7"),
        ],
    },
    "spine-collapse": {
        "overlays": [IDEAL_SPEC_FIRST, os.path.join(FIX, "spine-collapse-seed"), os.path.join(FIX, "_ideal", "spine-collapse")],
        "negatives": [
            ("sc-charter-drift", sm_charter_drift, "Spine-collapse SC1"),
            ("sc-shatter", sm_shatter, "Spine-collapse SC2"),
            ("sc-dangling", sm_dangling, "Spine-collapse SC3"),
            ("sc-silent-pivot", sm_silent_pivot, "Spine-collapse SC4"),
            ("sc-not-applied", sm_not_applied, "Spine-collapse SC5"),
        ],
    },
    # isolation-chain validates the CROSS-SEAT isolation properties (IC1-6) of grade_isolation_chain. The FULL
    # built-slice review grading (oracle re-run, anti-tautology litmus, ledger<->verdict) reuses 05-reviewer's
    # check_review.py — validated in .agents/skills/05-reviewer/evals/README.md; the integration README drives it.
    "isolation-chain": {
        "overlays": [IDEAL_SPEC_FIRST, os.path.join(FIX, "_ideal", "isolation-chain")],
        "negatives": [
            ("ic-rubber-stamp", icm_rubber_stamp, "Isolation-chain IC4"),
            ("ic-no-attestation", icm_no_attestation, "Isolation-chain IC2"),
            ("ic-baseline-mismatch", icm_baseline_mismatch, "Isolation-chain IC6"),
        ],
    },
    # agent-chain (WS5 5.5a) — the §10 fifth leg. Self-contained composed agent-system ideal (no spec-first base).
    "agent-chain": {
        "overlays": [os.path.join(FIX, "_ideal", "agent-chain")],
        "negatives": [
            ("ac-missing-contract", acm_missing_contract, "Agent-chain AC2"),
            ("ac-floor-fail-ship", acm_floor_fail_ship, "Agent-chain AC4"),
            ("ac-topology-no-justification", acm_topology_no_justification, "Agent-chain AC5"),
        ],
    },
    # verify-live (WS6) — the live-source verification chain (00 declares+seeds → 03 cites → 04 verifies → 06 gates).
    # Self-contained composed ideal; the 4 degenerates break one chain link each.
    "verify-live": {
        "overlays": [os.path.join(FIX, "_ideal", "verify-live")],
        "negatives": [
            ("vl-orphan-record", vlm_orphan_record, "Verify-live VL1"),
            ("vl-uncited-claim", vlm_uncited_claim, "Verify-live VL1"),
            ("vl-stale-version", vlm_stale_version, "Verify-live VL5"),
            ("vl-inferred-build-claim", vlm_inferred_build_claim, "Verify-live VL3"),
        ],
    },
}


def run_grader(root, case):
    subprocess.run([sys.executable, GRADER, "--outputs", root, "--case", case],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
    data = json.loads(read(os.path.join(root, "grading.json")))
    # label = the leading token before " — " (e.g. "Invariant 2", "Governance G3")
    return {e["text"].split(" — ")[0].strip(): e["passed"] for e in data["expectations"]}


def stage(case, mutation=None):
    tmp = tempfile.mkdtemp(prefix="int-val-")
    dst = os.path.join(tmp, "state")
    os.makedirs(dst)
    for ov in CASES[case]["overlays"]:
        overlay(ov, dst)
    if mutation:
        mutation(dst)
    try:
        return run_grader(dst, case)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def validate_case(case):
    rows, ok = [], True
    ideal = stage(case)
    ideal_pass = all(ideal.values())
    ok = ok and ideal_pass
    rows.append(("ideal", "all assertions PASS", "PASS" if ideal_pass else "FAIL",
                 "" if ideal_pass else f"failed: {[k for k, v in ideal.items() if not v]}"))
    for name, mut, target in CASES[case]["negatives"]:
        vec = stage(case, mut)
        fired = vec.get(target) is False
        others = sorted(k for k, v in vec.items() if k != target and v is False)
        ok = ok and fired
        rows.append((name, f"{target} FAILS", "PASS" if fired else "FAIL",
                     ("target fired" + (f"; also {others}" if others else "")) if fired
                     else f"{target} did NOT fail (vec={vec})"))
    w = max(len(r[0]) for r in rows)
    print(f"\n== check_integration grader-validation ({case}) ==")
    print(f"  {'case'.ljust(w)}  expectation                 result  notes")
    for name, exp, res, note in rows:
        print(f"  {name.ljust(w)}  {exp.ljust(26)}  {res.ljust(6)}  {note}")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", default="all",
                    choices=["spec-first", "governance", "spine-collapse", "isolation-chain", "agent-chain",
                             "verify-live", "all"])
    a = ap.parse_args()
    cases = list(CASES) if a.case == "all" else [a.case]   # spec-first, governance, spine-collapse, isolation-chain
    ok = all(validate_case(c) for c in cases)
    print(f"\n{'ALL GOOD — graders are sound (not over-strict, not vacuous)' if ok else 'VALIDATION FAILED'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
