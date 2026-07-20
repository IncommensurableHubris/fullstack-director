#!/usr/bin/env python3
"""Merge per-run audit.json + the adjudicator's keep/kill verdicts into the wave findings-ledger.json.
Validates the output shape against schemas/findings-ledger.schema.json (structural check, stdlib only).

Adjudication verdict maps are keyed by the compound key "<case>/<trial>/<cand_id>" — a candidate's
`id` (c1, c2, ...) is only unique within one run's audit.json array, never across the wave, so two
different runs can both emit a "c1" candidate that need distinct verdicts. Compound keys are the
only accepted key form; the lookup fails closed — a candidate whose compound key is absent from the
map is killed by default with an explanatory note (no bare-id fallback: a stray bare key like "c1"
could otherwise silently lend a different case's verdict to this candidate).
"""
import json, os, argparse

def _validate(ledger):
    """Minimal structural validation (no jsonschema dep): required keys + enums."""
    req_f = {"id", "case", "class", "doctrine_anchor", "evidence_quote", "status", "adjudication_note",
             "reproduction", "attribution", "disposition"}
    assert set(ledger) == {"wave", "findings"}, "ledger top-level keys"
    for f in ledger["findings"]:
        assert req_f <= set(f), "finding missing keys: %s" % (req_f - set(f))
        assert f["class"] in ("V", "B", "G", "C")
        assert f["status"] in ("confirmed", "killed")
        assert f["attribution"] in ("doctrine", "capability", "n/a")
        assert f["disposition"] in ("doctrine-edit", "calibrated-case-proposal", "defer", None)
        assert set(f["reproduction"]) == {"trials", "exhibited"}
    return True

def build_ledger(wave, audit_paths, adjudication, reproduction, attribution):
    findings, n = [], 0
    for ap in sorted(audit_paths):  # deterministic DF-NNN allocation regardless of shell glob order
        audit = json.load(open(ap, encoding="utf-8"))
        for c in audit["candidate_findings"]:
            # compound-key-only, fail-closed: cand ids are only unique within one run's array, so a
            # bare-id fallback could silently borrow a verdict from a different case's candidate.
            key = "%s/%s/%s" % (audit["case"], audit["trial"], c["id"])
            verdict = adjudication.get(key, {"keep": False, "note": "no adjudication for %s — defaulted killed" % key})
            n += 1
            findings.append({
                "id": "DF-%03d" % n, "case": audit["case"], "class": c["class"],
                "doctrine_anchor": c["doctrine_anchor"], "evidence_quote": c["evidence_quote"],
                "status": "confirmed" if verdict["keep"] else "killed",
                "adjudication_note": verdict.get("note", ""),
                "reproduction": reproduction.get(audit["case"], {"trials": 1, "exhibited": 1}),
                "attribution": attribution.get(audit["case"], "n/a"),
                "disposition": None,
            })
    ledger = {"wave": wave, "findings": findings}
    _validate(ledger)
    return ledger

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wave", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--audits", nargs="+", required=True)
    ap.add_argument("--adjudication", required=True, help="JSON file: {\"<case>/<trial>/<cand_id>\": {keep, note}}")
    ap.add_argument("--reproduction", default=None, help="JSON file: {case: {trials, exhibited}}")
    ap.add_argument("--attribution", default=None, help="JSON file: {case: doctrine|capability|n/a}")
    a = ap.parse_args()
    adj = json.load(open(a.adjudication, encoding="utf-8"))
    rep = json.load(open(a.reproduction, encoding="utf-8")) if a.reproduction else {}
    att = json.load(open(a.attribution, encoding="utf-8")) if a.attribution else {}
    led = build_ledger(a.wave, a.audits, adj, rep, att)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(led, f, indent=2)
    print("wrote %s — %d findings (%d confirmed)" % (a.out, len(led["findings"]),
          sum(1 for x in led["findings"] if x["status"] == "confirmed")))

if __name__ == "__main__":
    main()
