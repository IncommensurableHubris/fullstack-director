"""Programmatic grader for quality skill design-drift-catch evals."""
import json
import re
from pathlib import Path

BENCH_DIR = Path(__file__).parent / "benchmarks" / "2026-04-10-drift-catch"

EVALS = {
    "eval-drift-catch": {
        "assertions": [
            ("Design Fidelity section with DM-ID table", lambda t: "### Design Fidelity" in t and bool(re.search(r"DM-00[1-5].*\|.*(?:PRESENT|MISSING|DRIFTED)", t))),
            ("DM-003 flagged MISSING", lambda t: bool(re.search(r"DM-003.*MISSING", t, re.IGNORECASE)) or bool(re.search(r"DM-003.*\*\*MISSING\*\*", t))),
            ("DM-004 flagged MISSING", lambda t: bool(re.search(r"DM-004.*MISSING", t, re.IGNORECASE)) or bool(re.search(r"DM-004.*\*\*MISSING\*\*", t))),
            ("DM-005 flagged MISSING", lambda t: bool(re.search(r"DM-005.*MISSING", t, re.IGNORECASE)) or bool(re.search(r"DM-005.*\*\*MISSING\*\*", t))),
            ("DM-001 marked PRESENT", lambda t: bool(re.search(r"DM-001.*PRESENT", t, re.IGNORECASE))),
            ("DM-002 marked PRESENT", lambda t: bool(re.search(r"DM-002.*PRESENT", t, re.IGNORECASE))),
            ("UX dimension mentions Design Fidelity as sub-gate", lambda t: bool(re.search(r"Design Fidelity.*FAIL|Design Fidelity.*sub-gate|\(a\).*Design Fidelity", t))),
            ("References approved mockup at docs/design/approved/sprint-1/", lambda t: "docs/design/approved/sprint-1/" in t or "dashboard-desktop.png" in t),
            ("Verdict is FIX REQUIRED", lambda t: bool(re.search(r"\*\*Verdict:\*\*.*FIX REQUIRED|Verdict.*FIX REQUIRED", t))),
            ("Design Fidelity summary shows <5/5 PRESENT", lambda t: bool(re.search(r"[0-4]/5 manifest elements PRESENT|2/5.*PRESENT", t))),
        ]
    },
    "eval-clean-sprint": {
        "assertions": [
            ("Design Fidelity section with DM-ID table", lambda t: "### Design Fidelity" in t and bool(re.search(r"DM-00[1-5].*\|.*(?:PRESENT|MISSING|DRIFTED)", t))),
            ("All 5 DM-IDs marked PRESENT", lambda t: all(bool(re.search(rf"DM-00{i}.*PRESENT", t)) for i in range(1, 6))),
            ("No MISSING or DRIFTED elements", lambda t: not bool(re.search(r"\| *(MISSING|DRIFTED) *\|", t)) and not bool(re.search(r"\*\*(MISSING|DRIFTED)\*\*", t))),
            ("UX dimension mentions Design Fidelity as sub-gate", lambda t: bool(re.search(r"Design Fidelity.*PASS|Design Fidelity.*sub-gate|\(a\).*Design Fidelity", t))),
            ("References approved mockup at docs/design/approved/sprint-1/", lambda t: "docs/design/approved/sprint-1/" in t or "dashboard-desktop.png" in t),
            ("UX dimension scores PASS", lambda t: bool(re.search(r"User Experience.*PASS", t))),
            ("Verdict is SHIP", lambda t: bool(re.search(r"\*\*Verdict:\*\*.*SHIP|\*\*SHIP\*\*", t)) and "FIX REQUIRED" not in t.split("Verdict")[1][:200] if "Verdict" in t else False),
            ("Design Fidelity summary shows 5/5 PRESENT", lambda t: bool(re.search(r"5/5 manifest elements PRESENT|5/5.*PRESENT", t))),
        ]
    },
    "eval-undersized": {
        "assertions": [
            ("Design Fidelity section with DM-ID table", lambda t: "### Design Fidelity" in t and bool(re.search(r"DM-00[1-5].*\|.*(?:PRESENT|MISSING|DRIFTED)", t))),
            ("DM-003 flagged DRIFTED", lambda t: bool(re.search(r"DM-003.*DRIFTED", t, re.IGNORECASE)) or bool(re.search(r"DM-003.*\*\*DRIFTED\*\*", t))),
            ("DM-004 flagged DRIFTED", lambda t: bool(re.search(r"DM-004.*DRIFTED", t, re.IGNORECASE)) or bool(re.search(r"DM-004.*\*\*DRIFTED\*\*", t))),
            ("DM-005 flagged DRIFTED", lambda t: bool(re.search(r"DM-005.*DRIFTED", t, re.IGNORECASE)) or bool(re.search(r"DM-005.*\*\*DRIFTED\*\*", t))),
            ("DM-001 marked PRESENT", lambda t: bool(re.search(r"DM-001.*PRESENT", t, re.IGNORECASE))),
            ("DM-002 marked PRESENT", lambda t: bool(re.search(r"DM-002.*PRESENT", t, re.IGNORECASE))),
            ("UX dimension mentions Design Fidelity as sub-gate", lambda t: bool(re.search(r"Design Fidelity.*FAIL|Design Fidelity.*sub-gate|\(a\).*Design Fidelity", t))),
            ("References approved mockup at docs/design/approved/sprint-1/", lambda t: "docs/design/approved/sprint-1/" in t or "dashboard-desktop.png" in t),
            ("Verdict is FIX REQUIRED", lambda t: bool(re.search(r"\*\*Verdict:\*\*.*FIX REQUIRED|Verdict.*FIX REQUIRED", t))),
            ("DRIFTED status explicitly used", lambda t: t.count("DRIFTED") >= 3),
        ]
    },
}

def grade_report(report_path: Path, assertions: list) -> dict:
    text = report_path.read_text(encoding="utf-8")
    results = []
    for name, check in assertions:
        try:
            passed = check(text)
        except Exception as e:
            passed = False
        results.append({"text": name, "passed": passed, "evidence": ""})

    passed_count = sum(1 for r in results if r["passed"])
    return {
        "expectations": results,
        "summary": {
            "passed": passed_count,
            "failed": len(results) - passed_count,
            "total": len(results),
            "pass_rate": round(passed_count / len(results), 4) if results else 0,
        }
    }

def main():
    all_results = {}
    for eval_name, config in EVALS.items():
        for skill_type in ["with_skill", "old_skill"]:
            report_path = BENCH_DIR / eval_name / skill_type / "outputs" / "qa-report-sprint-01.md"
            if not report_path.exists():
                print(f"SKIP {eval_name}/{skill_type}: report not found")
                continue

            grading = grade_report(report_path, config["assertions"])
            key = f"{eval_name}/{skill_type}"
            all_results[key] = grading

            # Save grading.json
            grading_path = BENCH_DIR / eval_name / skill_type / "grading.json"
            grading_path.write_text(json.dumps(grading, indent=2), encoding="utf-8")

            status = "PASS" if grading["summary"]["pass_rate"] == 1.0 else f'{grading["summary"]["passed"]}/{grading["summary"]["total"]}'
            print(f"{key}: {status} (pass_rate={grading['summary']['pass_rate']})")
            for exp in grading["expectations"]:
                mark = "PASS" if exp["passed"] else "FAIL"
                print(f"  [{mark}] {exp['text']}")

    print("\n=== DISCRIMINATION ANALYSIS ===")
    for eval_name in EVALS:
        ws = all_results.get(f"{eval_name}/with_skill", {}).get("summary", {})
        os = all_results.get(f"{eval_name}/old_skill", {}).get("summary", {})
        delta = (ws.get("pass_rate", 0) - os.get("pass_rate", 0)) * 100
        print(f"{eval_name}: with_skill={ws.get('pass_rate',0)*100:.0f}% old_skill={os.get('pass_rate',0)*100:.0f}% delta={delta:+.0f}%")

if __name__ == "__main__":
    main()
